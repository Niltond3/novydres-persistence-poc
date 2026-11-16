#!/usr/bin/env node
/** MW-013: geometria local candidata dos Corredores do Ermo; sem dependências npm. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {dirname,join} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=dirname(fileURLToPath(import.meta.url));
const read=name=>{const buf=readFileSync(join(root,name));return {doc:JSON.parse(buf.toString('utf8')),sha:createHash('sha1').update(Buffer.concat([Buffer.from('blob '+buf.length+'\0'),buf])).digest('hex')}};
const e=read('macroermos-2010.proposal.json').doc;
const c=read('macrogeometria-litoral-baia-ilhas-2010.proposal.json');
const r=read('macrorelevo-2010.proposal.json');
const h=read('macrohidrografia-2010.proposal.json');
const cross=(a,b,p)=>(b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]);
const on=(a,b,p)=>cross(a,b,p)===0&&p[0]>=Math.min(a[0],b[0])&&p[0]<=Math.max(a[0],b[0])&&p[1]>=Math.min(a[1],b[1])&&p[1]<=Math.max(a[1],b[1]);
const hit=(a,b,c,d)=>{const s=Math.sign;return (s(cross(a,b,c))*s(cross(a,b,d))<0&&s(cross(c,d,a))*s(cross(c,d,b))<0)||on(a,b,c)||on(a,b,d)||on(c,d,a)||on(c,d,b)};
const edges=ring=>ring.map((p,i)=>[p,ring[(i+1)%ring.length]]);
const inside=(p,ring)=>{let v=false;for(let i=0,j=ring.length-1;i<ring.length;j=i++){if(on(ring[j],ring[i],p))return true;if((ring[i][1]>p[1])!==(ring[j][1]>p[1])&&p[0]<(ring[j][0]-ring[i][0])*(p[1]-ring[i][1])/(ring[j][1]-ring[i][1])+ring[i][0])v=!v;}return v};
const overlap=(a,b)=>inside(a[0],b)||inside(b[0],a)||edges(a).some(e=>edges(b).some(f=>hit(...e,...f)));
const intersectsLine=(ring,pts)=>pts.some(p=>inside(p,ring))||pts.slice(1).some((p,i)=>edges(ring).some(e=>hit(...e,pts[i],p)));
const distanceToSegment=(p,a,b)=>{const dx=b[0]-a[0],dy=b[1]-a[1],t=Math.max(0,Math.min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)));return Math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)};
assert.equal(e.schema,'NOVYDRES_LOCAL_WILDERNESS_PROPOSAL_V1');
assert.equal(e.subject_id,'world-atlas-novydres');
assert.equal(e.year,2010);
assert.equal(e.approval.workflow,'PROPOSED_PENDING_OWNER_REVIEW');
assert.equal(e.approval.canonical_status,'NOT_APPROVED');
assert.equal(e.approval.geometry_authority,'PROPOSAL_ONLY');
assert.equal(e.approval.owner_approval_for_this_geometry,null);
assert.equal(c.doc.approval.canonical_status,'NOT_APPROVED');
assert.equal(r.doc.approval.canonical_status,'NOT_APPROVED');
assert.equal(h.doc.approval.canonical_status,'NOT_APPROVED');
assert.equal(e.provenance.candidate_coast_blob_sha,c.sha);
assert.equal(e.provenance.candidate_relief_blob_sha,r.sha);
assert.equal(e.provenance.candidate_hydro_blob_sha,h.sha);
assert.equal(e.spatial_reference.crs,'NOVYDRES-LOCAL-2010');
assert.deepEqual(e.spatial_reference.study_frame,{xmin:-60000,ymin:-50000,xmax:60000,ymax:50000});
for(const key of ['geodetic_anchor','epsg','vertical_datum','municipal_boundary'])assert.equal(e.spatial_reference[key],null,key);
for(const key of Object.keys(e.explicitly_unassigned))assert.equal(e.explicitly_unassigned[key],null,key);
assert.equal(e.wilderness_model.natural_special_zone_not_raion,true);
assert.equal(e.wilderness_model.number_of_raions_in_canon,9);
assert.equal(e.wilderness_model.representation,'non_exhaustive_candidate_barrier_segments');
const segs=e.wilderness_model.corridor_segments;
assert.equal(segs.length,10);
assert.equal(new Set(segs.map(s=>s.feature_id)).size,segs.length);
assert.deepEqual(new Set(segs.map(s=>s.kind)),new Set(['rocky-pass','tundra-permafrost','wetlands','coastal']));
const shoreline=c.doc.proposed_geometry.mainland_coastline.points_xy_m;
const shoreEdges=shoreline.slice(1).map((p,i)=>[shoreline[i],p]);
const sea=[...shoreline,[-60000,50000],[-60000,-50000]];
const reliefs=r.doc.relief_model.relief_areas;
const waters=h.doc.hydro_model.waterbodies;
const rivers=h.doc.hydro_model.watercourses;
const xy=p=>Array.isArray(p)&&p.length===2&&p.every(Number.isInteger)&&p[0]>=-60000&&p[0]<=60000&&p[1]>=-50000&&p[1]<=50000;
let total=0;
for(const s of segs){
 assert.equal(s.geometry_type,'Polygon');
 assert.equal(s.approval_status,'PROPOSED_NOT_CANONICAL');
 assert.equal(s.municipal_or_raion_boundary,false);
 assert.equal(s.urban_gap_proven,false);
 const ring=s.ring_xy_m;
 assert(ring.length>=3&&ring.every(xy),s.feature_id+' invalid coordinates');
 assert(!(ring[0][0]===ring.at(-1)[0]&&ring[0][1]===ring.at(-1)[1]),s.feature_id+' duplicate closure');
 let twiceArea=0;for(let i=0;i<ring.length;i++)twiceArea+=ring[i][0]*ring[(i+1)%ring.length][1]-ring[(i+1)%ring.length][0]*ring[i][1];
 assert(Math.abs(twiceArea)>30e6,s.feature_id+' too small');
 total+=Math.abs(twiceArea)/2e6;
 const rr=s.relief_anchor_id?reliefs.find(x=>x.feature_id===s.relief_anchor_id):null;
 assert(!s.relief_anchor_id||rr,s.feature_id+' missing relief');
 for(const p of ring){assert(!inside(p,sea),s.feature_id+' offshore point');if(rr)assert(inside(p,rr.ring_xy_m),s.feature_id+' not in relief');}
 for(let i=0;i<ring.length;i++){
  const edge=edges(ring)[i],mid=[(edge[0][0]+edge[1][0])/2,(edge[0][1]+edge[1][1])/2];
  assert(!inside(mid,sea),s.feature_id+' offshore edge');
  if(rr){assert(inside(mid,rr.ring_xy_m),s.feature_id+' segment outside relief');for(const e2 of edges(rr.ring_xy_m))assert(!hit(...edge,...e2),s.feature_id+' crosses relief edge');}
  for(const shore of shoreEdges)assert(!hit(...edge,...shore),s.feature_id+' crosses shoreline');
  for(let j=i+1;j<ring.length;j++)if(j!==i+1&&!(i===0&&j===ring.length-1))assert(!hit(...edge,...edges(ring)[j]),s.feature_id+' self-intersection');
 }
 for(const w of waters)assert(!overlap(ring,w.ring_xy_m),s.feature_id+' waterbody overlap '+w.feature_id);
 for(const island of c.doc.proposed_geometry.secondary_islands)assert(!overlap(ring,island.ring_xy_m),s.feature_id+' island overlap');
 const streamIds=rivers.filter(f=>intersectsLine(ring,f.points_xy_m)).map(f=>f.feature_id);
 assert.deepEqual(s.natural_watercourse_ids_intersecting,streamIds,s.feature_id+' natural streams changed');
 if(s.kind==='coastal'){
  const ix=s.exposed_coast_segment_indices;
  assert(Array.isArray(ix)&&ix.length&&ix.every(i=>Number.isInteger(i)&&i>=0&&i<shoreline.length-1),s.feature_id+' invalid coast reference');
  assert(ring.every(p=>Math.min(...ix.map(i=>distanceToSegment(p,shoreline[i],shoreline[i+1])))<=15000),s.feature_id+' too far from exposed coast');
 }else assert.equal(s.exposed_coast_segment_indices,null);
}
for(let i=0;i<segs.length;i++)for(let j=i+1;j<segs.length;j++)assert(!overlap(segs[i].ring_xy_m,segs[j].ring_xy_m),'overlapping Ermos: '+segs[i].feature_id+' '+segs[j].feature_id);
assert(Math.abs(total-e.validation_summary.synthetic_total_km2)<0.001);
console.log('MW-013 macro-Ermo candidate PASS');
console.log(segs.length+' segments, four natural classes, '+total.toFixed(3)+' km2 synthetic/non-exhaustive');
console.log('Coast '+c.sha+' relief '+r.sha+' hydro '+h.sha);
console.log('No raions, transport or approval inferred');
