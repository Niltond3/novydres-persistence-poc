#!/usr/bin/env node
/**
 * MW-006: integracao fisica das propostas MW-002..MW-005, 2010.
 * Requer apenas Node.js (ESM), nao canoniza nem georreferencia.
 *
 * Da raiz do repositorio:
 * node novydres/cenario/atlas-novydres/cartografia/validar-integracao-fisica.mjs
 *
 * Falha se algum validador de camada, SHA ou vinculo topologico falhar.
 * PASS_WITH_LIMITATIONS != certificacao de hidrologia, altitude, area ou urbanizacao.
 */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const load = (name) => {
  const bytes = readFileSync(join(here, name));
  return {
    doc: JSON.parse(bytes.toString('utf8')),
    git_blob_sha: createHash('sha1').update(
      Buffer.concat([Buffer.from('blob ' + bytes.length + '\0'), bytes])
    ).digest('hex'),
  };
};
const coastFile = load('macrogeometria-litoral-baia-ilhas-2010.proposal.json');
const reliefFile = load('macrorelevo-2010.proposal.json');
const hydroFile = load('macrohidrografia-2010.proposal.json');
const ermoFile = load('macroermos-2010.proposal.json');
const c = coastFile.doc, r = reliefFile.doc, h = hydroFile.doc, e = ermoFile.doc;
const errors = [], cautions = [];
const test = (predicate, message) => { if (!predicate) errors.push(message); };
const equals = (a,b) => a[0] === b[0] && a[1] === b[1];
const cross = (a,b,p) => (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]);
const on = (a,b,p) => cross(a,b,p)===0 && p[0]>=Math.min(a[0],b[0]) &&
  p[0]<=Math.max(a[0],b[0]) && p[1]>=Math.min(a[1],b[1]) && p[1]<=Math.max(a[1],b[1]);
const hit = (a,b,c,d) => {
  const s = Math.sign;
  return (s(cross(a,b,c))*s(cross(a,b,d))<0 && s(cross(c,d,a))*s(cross(c,d,b))<0)
    || on(a,b,c) || on(a,b,d) || on(c,d,a) || on(c,d,b);
};
const edges = ring => ring.map((p,i) => [p,ring[(i+1)%ring.length]]);
const inside = (p,ring) => {
  let contained = false;
  for(let i=0,j=ring.length-1;i<ring.length;j=i++){
    if(on(ring[j],ring[i],p))return true;
    if((ring[i][1]>p[1])!==(ring[j][1]>p[1]) &&
      p[0]<(ring[j][0]-ring[i][0])*(p[1]-ring[i][1])/(ring[j][1]-ring[i][1])+ring[i][0]) contained = !contained;
  }
  return contained;
};
const polygonOverlap = (a,b) => inside(a[0],b)||inside(b[0],a)||
  edges(a).some(x=>edges(b).some(y=>hit(...x,...y)));
const intersectsLine = (ring,points) => points.some(p=>inside(p,ring)) ||
  points.slice(1).some((p,i)=>edges(ring).some(edge=>hit(...edge,points[i],p)));

const layerFiles = [coastFile,reliefFile,hydroFile,ermoFile];
const candidateFrame = {xmin:-60000,ymin:-50000,xmax:60000,ymax:50000};
for(const item of layerFiles){
  const d=item.doc;
  test(d.subject_id==='world-atlas-novydres',d.document_id+' subject_id');
  test(d.year===2010,d.document_id+' year');
  test(d.approval.canonical_status==='NOT_APPROVED',d.document_id+' canonical approval drift');
  test(d.approval.truth_state==='GM_PREPARED',d.document_id+' truth state drift');
  test(d.approval.geometry_authority==='PROPOSAL_ONLY',d.document_id+' geometry authority drift');
  test(d.spatial_reference.crs==='NOVYDRES-LOCAL-2010',d.document_id+' CRS mismatch');
  test(d.spatial_reference.units==='m',d.document_id+' units mismatch');
  test(d.spatial_reference.geodetic_anchor===null,d.document_id+' geodetic anchor already fixed');
  test(d.spatial_reference.epsg===null,d.document_id+' EPSG already fixed');
}
const study = c.study_frame;
test(study.xmin===candidateFrame.xmin&&study.ymin===candidateFrame.ymin&&
  study.xmax===candidateFrame.xmax&&study.ymax===candidateFrame.ymax,'MW-002 working frame');
for(const item of [reliefFile,hydroFile,ermoFile]){
  test(JSON.stringify(item.doc.spatial_reference.study_frame)===
    JSON.stringify(candidateFrame),item.doc.document_id+' frame mismatch');
}
test(study.municipal_geometry===null,'MW-002 municipal boundary inadvertently added');
for(const item of [r,h,e])test(item.spatial_reference.municipal_boundary===null,
  item.document_id+' municipal boundary inadvertently added');

test(r.provenance.candidate_coast_blob_sha===coastFile.git_blob_sha,'MW-003 coast dependency SHA');
test(h.provenance.candidate_coast_blob_sha===coastFile.git_blob_sha,'MW-004 coast dependency SHA');
test(h.provenance.candidate_relief_blob_sha===reliefFile.git_blob_sha,'MW-004 relief dependency SHA');
test(e.provenance.candidate_coast_blob_sha===coastFile.git_blob_sha,'MW-005 coast dependency SHA');
test(e.provenance.candidate_relief_blob_sha===reliefFile.git_blob_sha,'MW-005 relief dependency SHA');
test(e.provenance.candidate_hydro_blob_sha===hydroFile.git_blob_sha,'MW-005 hydro dependency SHA');

const shore = c.proposed_geometry.mainland_coastline.points_xy_m;
const bay = c.proposed_geometry.sheltered_bay;
const bayRing = shore.slice(bay.coastline_vertices_inclusive_zero_based[0],
                           bay.coastline_vertices_inclusive_zero_based[1]+1);
const relief = r.relief_model.relief_areas;
const crests = r.relief_model.ridge_crest_axes;
const model = h.hydro_model, basins=model.catchment_areas,
  flows=model.watercourses, waters=model.waterbodies,
  warm=model.localized_thermal_reaches, ermos=e.wilderness_model.corridor_segments;
const registeredIds=[
  c.proposed_geometry.mainland_coastline.feature_id,
  c.proposed_geometry.sheltered_bay.feature_id,
  c.proposed_geometry.outer_sea.feature_id,
  ...c.proposed_geometry.secondary_islands.map(x=>x.feature_id),
  ...relief.map(x=>x.feature_id),...crests.map(x=>x.feature_id),
  ...basins.map(x=>x.feature_id),...flows.map(x=>x.feature_id),
  ...waters.map(x=>x.feature_id),...warm.map(x=>x.feature_id),
  ...ermos.map(x=>x.feature_id)
];
const ids = new Set(registeredIds);
test(ids.size===registeredIds.length,'Duplicate IDs across physical layers');
test(ids.size===44,'Spatial ID census changed; revise MW-006 report and checks');
test(c.proposed_geometry.secondary_islands.length===3,'Island count changed');
test(relief.length===7 && crests.length===3,'Relief census changed');
test(basins.length===5 && flows.length===9 && waters.length===3 && warm.length===1,
  'Hydro census changed');
test(ermos.length===10,'Ermo census changed');
const assertRef=(id,at)=>test(ids.has(id),at+' missing reference '+id);
for(const crest of crests)assertRef(crest.parent_region_id,crest.feature_id);
for(const river of flows){
  assertRef(river.basin_id,river.feature_id);
  if(river.downstream.target_feature_id)assertRef(river.downstream.target_feature_id,river.feature_id);
  if(river.downstream.waterbody_id)assertRef(river.downstream.waterbody_id,river.feature_id);
}
for(const water of waters)assertRef(water.basin_id,water.feature_id);
for(const span of warm){
  for(const field of ['river_feature_id','thermal_input_feature_id','relief_anchor_id'])
    assertRef(span[field],span.feature_id);
}
for(const ermo of ermos)if(ermo.relief_anchor_id)assertRef(ermo.relief_anchor_id,ermo.feature_id);
for(const key of Object.keys(e.explicitly_unassigned))
  test(e.explicitly_unassigned[key]===null,'Unexpectedly assigned MW-005 attribute '+key);

const vasyl = flows.find(x=>x.feature_id==='river-vasyl-main-001');
test(Boolean(vasyl),'Rio Vasyl not found');
if(vasyl){
  test(vasyl.downstream.type==='coast_vertex'&&
    vasyl.downstream.coast_feature_id===c.proposed_geometry.mainland_coastline.feature_id &&
    vasyl.downstream.waterbody_id===bay.feature_id,'Vasyl coastal target');
  test(equals(vasyl.points_xy_m.at(-1),shore[vasyl.downstream.vertex_index]),'Vasyl mouth point');
  test(vasyl.downstream.vertex_index>bay.mouth_vertex_indices_zero_based[0]&&
    vasyl.downstream.vertex_index<bay.mouth_vertex_indices_zero_based[1],'Vasyl outside bay');
  const valley=relief.find(x=>x.feature_id==='relief-thermal-valley-001');
  test(Boolean(valley),'Thermal valley missing');
  for(const s of warm.filter(x=>x.river_feature_id===vasyl.feature_id)){
    test(!!valley && vasyl.points_xy_m.slice(s.start_vertex_index,s.end_vertex_index+1)
      .every(p=>inside(p,valley.ring_xy_m)),s.feature_id+' warm range outside valley');
  }
}
for(const river of flows){
  const d=river.downstream;
  if(d.type==='coast_vertex'||d.type==='coast_segment'){
    const target=river.points_xy_m.at(-1);
    if(d.type==='coast_vertex')
      test(d.coast_feature_id===c.proposed_geometry.mainland_coastline.feature_id &&
        equals(target,shore[d.vertex_index]),river.feature_id+' coastline vertex');
    else test(d.coast_feature_id===c.proposed_geometry.mainland_coastline.feature_id &&
        on(shore[d.segment_start_index],shore[d.segment_start_index+1],target),
        river.feature_id+' coastline segment');
    if(d.waterbody_id===bay.feature_id)
      test(inside(target,bayRing),river.feature_id+' outlet not into bay');
    else if(d.waterbody_id===c.proposed_geometry.outer_sea.feature_id)
      test(!inside(target,bayRing),river.feature_id+' exposed coast outlet inside bay');
    else test(false,river.feature_id+' unknown receiving waterbody');
  }
}
const reliefById=new Map(relief.map(x=>[x.feature_id,x]));
const expectedErmoTypes=new Set(['rocky-pass','tundra-permafrost','wetlands','coastal']);
test(ermos.length===10&&new Set(ermos.map(x=>x.kind)).size===4&&
  ermos.every(x=>expectedErmoTypes.has(x.kind)),'Ermo class set changed');
test(e.wilderness_model.natural_special_zone_not_raion===true &&
  e.wilderness_model.number_of_raions_in_canon===9,'Ermo administrative semantics changed');
for(const ermo of ermos){
  const anchor=ermo.relief_anchor_id&&reliefById.get(ermo.relief_anchor_id);
  if(ermo.relief_anchor_id){
    test(Boolean(anchor)&&ermo.ring_xy_m.every(p=>inside(p,anchor.ring_xy_m)),
      ermo.feature_id+' relief anchor containment');
    if(anchor&&ermo.kind!=='coastal')test(anchor.possible_ermo_type===ermo.kind,
      ermo.feature_id+' relief class mismatch');
  }
  for(const body of waters)
    test(!polygonOverlap(ermo.ring_xy_m,body.ring_xy_m),
      ermo.feature_id+' overlaps '+body.feature_id);
  const crossingIds=flows.filter(x=>intersectsLine(ermo.ring_xy_m,x.points_xy_m))
    .map(x=>x.feature_id);
  test(JSON.stringify(crossingIds)===JSON.stringify(ermo.natural_watercourse_ids_intersecting),
    ermo.feature_id+' watercourse intersection inventory stale');
}

let crestStreamCrossings=0;
for(const crest of crests)for(const river of flows){
  let intersects=false;
  for(let i=1;i<crest.points_xy_m.length;i++)for(let j=1;j<river.points_xy_m.length;j++)
    intersects ||= hit(crest.points_xy_m[i-1],crest.points_xy_m[i],
                       river.points_xy_m[j-1],river.points_xy_m[j]);
  if(intersects){crestStreamCrossings++;cautions.push('Qualitative crest vs stream: '+
    crest.feature_id+' x '+river.feature_id);}
}
cautions.push('Sem MDE/cotas: declividades e divisores de aguas nao certificados.');
cautions.push('Sem nucleos urbanos: isolamento real por Ermos nao certificado.');
cautions.push('Sem limites municipais e ancoragem: area/georreferenciamento nao certificados.');

// A verificação integrada não substitui as verificações especificas MW-002 a MW-005.
for(const name of [
  'validar-macrogeometria-litoral.mjs','validar-macrorelevo.mjs',
  'validar-macrohidrografia.mjs','validar-macroermos.mjs'
]){
  const child=spawnSync(process.execPath,[join(here,name)],{encoding:'utf8',timeout:60000});
  if(child.error||child.status!==0){
    errors.push('Layer validator '+name+' failed: '+
      String(child.error?.message||child.stderr||child.stdout||child.status).slice(0,700));
  }
}
const result={
  document_id:'MW-006-PHYSICAL-INTEGRATION-2010',
  subject_id:'world-atlas-novydres',
  status:errors.length?'FAIL':'PASS_WITH_LIMITATIONS',
  canonical_status:'NOT_APPROVED',
  working_crs:'NOVYDRES-LOCAL-2010',
  source_blob_shas:{
    mw002:coastFile.git_blob_sha,mw003:reliefFile.git_blob_sha,
    mw004:hydroFile.git_blob_sha,mw005:ermoFile.git_blob_sha
  },
  counts:{islands:3,relief_areas:relief.length,crest_axes:crests.length,
    catchment_areas:basins.length,watercourses:flows.length,
    waterbodies:waters.length,warm_reaches:warm.length,
    ermo_polygons:ermos.length,unique_spatial_ids:ids.size,crest_stream_crossings:crestStreamCrossings},
  errors,cautions
};
console.log(JSON.stringify(result,null,2));
if(errors.length)process.exitCode=1;
