#!/usr/bin/env node
/**
 * MW-003 — validação determinística da macrogeometria de relevo candidata.
 * Sem pacotes externos. Não comprova plausibilidade geológica ou cânone.
 */
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import assert from 'node:assert/strict';

const here = dirname(fileURLToPath(import.meta.url));
const read = name => JSON.parse(readFileSync(join(here, name), 'utf8'));
const relief = read('macrorelevo-2010.proposal.json');
const coastFile = join(here, 'macrogeometria-litoral-baia-ilhas-2010.proposal.json');
const bytes = readFileSync(coastFile);
const gitBlobSha = createHash('sha1').update(Buffer.concat([
  Buffer.from('blob ' + bytes.length + '\0'), bytes
])).digest('hex');
const coast = JSON.parse(bytes.toString('utf8'));
const eq = (a, b) => a[0] === b[0] && a[1] === b[1];
const cross = (a,b,c) => (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);
const sign = (a,b,c) => Math.sign(cross(a,b,c));
const onSeg = (a,b,p) => sign(a,b,p)===0 &&
  p[0]>=Math.min(a[0],b[0]) && p[0]<=Math.max(a[0],b[0]) &&
  p[1]>=Math.min(a[1],b[1]) && p[1]<=Math.max(a[1],b[1]);
function intersects(a,b,c,d){
  const x=sign(a,b,c),y=sign(a,b,d),z=sign(c,d,a),w=sign(c,d,b);
  return (x!==y && z!==w) || onSeg(a,b,c) || onSeg(a,b,d) ||
    onSeg(c,d,a) || onSeg(c,d,b);
}
const ringEdges = ring => ring.map((p,i)=>[p,ring[(i+1)%ring.length]]);
function inside(p,poly){
  let hit=false;
  for(let i=0,j=poly.length-1;i<poly.length;j=i++){
    const a=poly[j],b=poly[i];
    if(onSeg(a,b,p)) return true;
    if((a[1]>p[1])!==(b[1]>p[1]) &&
       p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0]) hit=!hit;
  }
  return hit;
}
const validPoint=p=>Array.isArray(p)&&p.length===2&&
  p.every(Number.isInteger)&&
  p[0]>-60000&&p[0]<60000&&p[1]>-50000&&p[1]<50000;
function simpleRing(ring,id){
  assert(Array.isArray(ring)&&ring.length>=3,id+' invalid ring');
  assert(ring.every(validPoint),id+' point outside frame or noninteger');
  assert(!eq(ring[0],ring[ring.length-1]),id+' duplicates closing point');
  const edges=ringEdges(ring);
  for(let i=0;i<edges.length;i++)
    for(let j=i+1;j<edges.length;j++){
      if(j===i+1||(i===0&&j===edges.length-1)) continue;
      assert(!intersects(...edges[i],...edges[j]),id+' self intersects');
    }
  const shoelace=ring.reduce((v,p,i)=>{
    const q=ring[(i+1)%ring.length];return v+p[0]*q[1]-q[0]*p[1];
  },0);
  assert(Math.abs(shoelace)>100000000,id+' degenerately small');
  return Math.abs(shoelace)/2/1000000;
}

assert.equal(relief.schema,'NOVYDRES_LOCAL_RELIEF_PROPOSAL_V1');
assert.equal(relief.subject_id,'world-atlas-novydres');
assert.equal(relief.year,2010);
assert.equal(relief.approval.workflow,'PROPOSED_PENDING_OWNER_REVIEW');
assert.equal(relief.approval.canonical_status,'NOT_APPROVED');
assert.equal(relief.approval.geometry_authority,'PROPOSAL_ONLY');
assert.equal(relief.approval.owner_approval_for_this_geometry,null);
assert.equal(coast.approval.canonical_status,'NOT_APPROVED');
assert.equal(coast.approval.workflow ?? coast.approval.cartographic_workflow,'PROPOSED_PENDING_OWNER_REVIEW');
assert.equal(relief.provenance.candidate_coast_blob_sha,gitBlobSha);
assert.equal(relief.validation.geometry_dependency_sha,gitBlobSha);
assert.equal(relief.spatial_reference.crs,'NOVYDRES-LOCAL-2010');
assert.equal(relief.spatial_reference.geodetic_anchor,null);
assert.equal(relief.spatial_reference.epsg,null);
assert.equal(relief.spatial_reference.municipal_boundary,null);
assert.equal(relief.relief_model.vertical_datum,null);
assert.equal(relief.relief_model.absolute_altitudes_m,null);
assert.equal(relief.relief_model.raster_dem,null);
assert.deepEqual(relief.spatial_reference.study_frame,
  {xmin:-60000,ymin:-50000,xmax:60000,ymax:50000});
for(const field of ['river_geometries','raion_geometries','municipal_area_km2',
                   'roads_and_rail','ports','thermal_source_points']){
  assert.equal(relief.explicitly_unassigned[field],null,field+' must remain unassigned');
}
const line=coast.proposed_geometry.mainland_coastline.points_xy_m;
const sea=[...line,[-60000,50000],[-60000,-50000]];
const coastEdges=line.slice(1).map((p,i)=>[line[i],p]);
const islandRings=coast.proposed_geometry.secondary_islands.map(x=>x.ring_xy_m);
const areas=relief.relief_model.relief_areas;
const axes=relief.relief_model.ridge_crest_axes;
assert(Array.isArray(areas)&&areas.length>=5,'expected several macro areas');
assert(Array.isArray(axes)&&axes.length>=2,'expected ridge crests');
assert.equal(new Set(areas.map(x=>x.feature_id)).size,areas.length,'duplicate feature ids');
const knownTerrain=new Set([
 'terrain-thermal-valley','terrain-rocky-uplands','terrain-tundra-lowlands'
]);
const knownErmos=new Set(['not_an_admin_boundary','rocky-pass','tundra-permafrost','wetlands']);
const areasById=new Map(areas.map(a=>[a.feature_id,a]));
let totalKm2=0;
for(const a of areas){
  assert.equal(a.geometry_type,'Polygon',a.feature_id);
  assert.equal(a.approval_status,'PROPOSED_NOT_CANONICAL',a.feature_id);
  assert.equal(a.altitude_m,null,a.feature_id);
  assert.equal(a.effective_raion,null,a.feature_id);
  assert(knownTerrain.has(a.physiographic_class),a.feature_id+' unknown class');
  assert(knownErmos.has(a.possible_ermo_type),a.feature_id+' unknown Ermo type');
  const km2=simpleRing(a.ring_xy_m,a.feature_id);
  assert(km2>=20 && km2<=800,a.feature_id+' not macro scale');
  totalKm2+=km2;
  const edges=ringEdges(a.ring_xy_m);
  assert(a.ring_xy_m.every(p=>!inside(p,sea)),a.feature_id+' over study sea');
  for(const [p,q] of edges){
    assert(!coastEdges.some(([c,d])=>intersects(p,q,c,d)),
      a.feature_id+' intersects coast');
    for(const island of islandRings)
      assert(!ringEdges(island).some(([c,d])=>intersects(p,q,c,d)),
        a.feature_id+' intersects island');
  }
  for(const island of islandRings){
    assert(a.ring_xy_m.every(p=>!inside(p,island)),a.feature_id+' on island');
    assert(island.every(p=>!inside(p,a.ring_xy_m)),a.feature_id+' contains island');
  }
}
for(let i=0;i<areas.length;i++) for(let j=i+1;j<areas.length;j++){
  const a=areas[i],b=areas[j];
  assert(!ringEdges(a.ring_xy_m).some(([p,q])=>
    ringEdges(b.ring_xy_m).some(([u,v])=>intersects(p,q,u,v))),
    a.feature_id+' overlaps '+b.feature_id);
  assert(!inside(a.ring_xy_m[0],b.ring_xy_m) &&
         !inside(b.ring_xy_m[0],a.ring_xy_m),
    a.feature_id+' contained within '+b.feature_id);
}
const mustHave=new Set(areas.map(a=>a.physiographic_class));
for(const t of knownTerrain) assert(mustHave.has(t),'missing '+t);
for(const axis of axes){
  const parent=areasById.get(axis.parent_region_id);
  assert(parent,axis.feature_id+' missing parent region');
  assert.equal(axis.geometry_type,'LineString');
  assert.equal(axis.kind,'qualitative_crest_axis');
  assert.equal(axis.altitude_m,null);
  assert(Array.isArray(axis.points_xy_m)&&axis.points_xy_m.length>=2);
  assert(axis.points_xy_m.every(p=>validPoint(p)&&inside(p,parent.ring_xy_m)),
    axis.feature_id+' outside parent');
  for(let i=0;i<axis.points_xy_m.length-1;i++){
    const p=axis.points_xy_m[i],q=axis.points_xy_m[i+1];
    assert(!coastEdges.some(([c,d])=>intersects(p,q,c,d)),
      axis.feature_id+' crosses coastline');
    assert(!ringEdges(parent.ring_xy_m).some(([c,d])=>intersects(p,q,c,d)),
      axis.feature_id+' exits parent region');
  }
}
const coastal=relief.relief_model.coastal_context_references;
const bayRange=coast.proposed_geometry.sheltered_bay.coastline_vertices_inclusive_zero_based;
assert.deepEqual(coastal.sheltered_bay.coast_vertex_range_inclusive_zero_based,bayRange);
assert.equal(coastal.sheltered_bay.derived_feature_id,coast.proposed_geometry.sheltered_bay.feature_id);
assert.deepEqual(coastal.exposed_coast_segments.map(s=>s.coast_vertex_range_inclusive_zero_based),
  [[0,bayRange[0]],[bayRange[1],line.length-1]]);
assert(areas.every(a=>a.possible_ermo_type!=='coastal'),'coastal border must be derived');

console.log('MW-003 relief proposal PASS');
console.log(areas.length+' landform polygons, '+axes.length+' ridge axes');
console.log('Candidate sample macro-areas: '+totalKm2.toFixed(2)+' km², NOT municipal area');
console.log('Coast dependency Git blob: '+gitBlobSha);
