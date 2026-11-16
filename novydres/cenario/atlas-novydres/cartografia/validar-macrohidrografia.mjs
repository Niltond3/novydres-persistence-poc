#!/usr/bin/env node
/** MW-004: verificador determinístico de proposta, sem dependências externas. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {dirname,join} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=dirname(fileURLToPath(import.meta.url));
const load=name=>{const buf=readFileSync(join(root,name));return {value:JSON.parse(buf.toString('utf8')),gitSha:createHash('sha1').update(Buffer.concat([Buffer.from('blob '+buf.length+'\0'),buf])).digest('hex')}};
const h=load('macrohidrografia-2010.proposal.json').value;
const c=load('macrogeometria-litoral-baia-ilhas-2010.proposal.json');
const r=load('macrorelevo-2010.proposal.json');
const exact=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const cross=(a,b,p)=>(b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]);
const on=(a,b,p)=>cross(a,b,p)===0&&p[0]>=Math.min(a[0],b[0])&&p[0]<=Math.max(a[0],b[0])&&p[1]>=Math.min(a[1],b[1])&&p[1]<=Math.max(a[1],b[1]);
const hit=(a,b,c,d)=>{const s=Math.sign;return (s(cross(a,b,c))*s(cross(a,b,d))<0&&s(cross(c,d,a))*s(cross(c,d,b))<0)||on(a,b,c)||on(a,b,d)||on(c,d,a)||on(c,d,b)};
const edges=ring=>ring.map((p,i)=>[p,ring[(i+1)%ring.length]]);
const inside=(p,ring)=>{let v=false;for(let i=0,j=ring.length-1;i<ring.length;j=i++){if(on(ring[j],ring[i],p))return true;if((ring[i][1]>p[1])!==(ring[j][1]>p[1])&&p[0]<(ring[j][0]-ring[i][0])*(p[1]-ring[i][1])/(ring[j][1]-ring[i][1])+ring[i][0])v=!v}return v};
const line=c.value.proposed_geometry.mainland_coastline.points_xy_m;
const shoreEdges=line.slice(1).map((p,i)=>[line[i],p]);
const sea=[...line,[-60000,50000],[-60000,-50000]];
const xy=p=>Array.isArray(p)&&p.length===2&&p.every(Number.isInteger)&&p[0]>=-60000&&p[0]<=60000&&p[1]>=-50000&&p[1]<=50000;
const onCoast=p=>shoreEdges.some(([a,b])=>on(a,b,p));
assert.equal(h.schema,'NOVYDRES_LOCAL_HYDROGRAPHY_PROPOSAL_V1');
assert.equal(h.subject_id,'world-atlas-novydres');
assert.equal(h.year,2010);
assert.equal(h.approval.workflow,'PROPOSED_PENDING_OWNER_REVIEW');
assert.equal(h.approval.canonical_status,'NOT_APPROVED');
assert.equal(h.approval.geometry_authority,'PROPOSAL_ONLY');
assert.equal(h.approval.owner_approval_for_this_geometry,null);
assert.equal(c.value.approval.canonical_status,'NOT_APPROVED');
assert.equal(r.value.approval.canonical_status,'NOT_APPROVED');
assert.equal(h.provenance.candidate_coast_blob_sha,c.gitSha);
assert.equal(h.provenance.candidate_relief_blob_sha,r.gitSha);
assert.equal(r.value.provenance.candidate_coast_blob_sha,c.gitSha);
assert.equal(h.spatial_reference.crs,'NOVYDRES-LOCAL-2010');
assert.deepEqual(h.spatial_reference.study_frame,{xmin:-60000,ymin:-50000,xmax:60000,ymax:50000});
for(const k of ['geodetic_anchor','epsg','municipal_boundary','vertical_datum','absolute_elevations_m'])assert.equal(h.spatial_reference[k],null,k);
for(const k of ['river_discharge_m3_s','river_width_m','thermal_water_temperature_c','formal_watershed_divides','raions_and_neighborhoods','roads_and_rail','ports_and_bridges','underground_channels'])assert.equal(h.explicitly_unassigned[k],null,k);
const {catchment_areas:basins,watercourses:flows,waterbodies:lakes,localized_thermal_reaches:warm}=h.hydro_model;
assert.equal(basins.length,5);
assert.equal(flows.length,9);
assert.equal(lakes.length,3);
assert.equal(new Set([...basins,...flows,...lakes,...warm].map(f=>f.feature_id)).size,basins.length+flows.length+lakes.length+warm.length);
for(const f of [...basins,...lakes]){
 const ring=f.ring_xy_m;
 assert.equal(f.geometry_type,'Polygon');
 assert.equal(f.approval_status,'PROPOSED_NOT_CANONICAL');
 assert(ring.length>=3&&ring.every(xy),f.feature_id+' invalid points');
 assert(!exact(ring[0],ring.at(-1)),f.feature_id+' duplicate closure');
 let doubleArea=0;
 for(let i=0;i<ring.length;i++){const p=ring[i],q=ring[(i+1)%ring.length];doubleArea+=p[0]*q[1]-q[0]*p[1]}
 assert(Math.abs(doubleArea)>=1000000,f.feature_id+' degenerate area');
 for(let i=0;i<ring.length;i++)for(let j=i+1;j<ring.length;j++)if(j!==i+1&&!(i===0&&j===ring.length-1))assert(!hit(...edges(ring)[i],...edges(ring)[j]),f.feature_id+' self intersection');
 for(const p of ring)assert(!inside(p,sea)||onCoast(p),f.feature_id+' in sea');
 for(const [p,q] of edges(ring)){
  assert(!inside([(p[0]+q[0])/2,(p[1]+q[1])/2],sea)||onCoast([(p[0]+q[0])/2,(p[1]+q[1])/2]),f.feature_id+' edge in sea');
  for(const [a,b] of shoreEdges)if(hit(p,q,a,b))assert(on(a,b,p)||on(a,b,q),f.feature_id+' crosses coastline');
 }
}
for(let i=0;i<basins.length;i++)for(let j=i+1;j<basins.length;j++){
 const a=basins[i].ring_xy_m,b=basins[j].ring_xy_m;
 assert(!inside(a[0],b)&&!inside(b[0],a),'basin containment');
 for(const e of edges(a))for(const f of edges(b))assert(!hit(...e,...f),'overlapping catchment envelopes');
}
const basinOf=id=>{const b=basins.find(x=>x.feature_id===id);assert(b,'basin missing '+id);return b};
const flowOf=id=>{const f=flows.find(x=>x.feature_id===id);assert(f,'flow missing '+id);return f};
const lakeOf=id=>{const b=lakes.find(x=>x.feature_id===id);assert(b,'lake missing '+id);return b};
for(const f of flows){
 assert.equal(f.geometry_type,'LineString');
 assert.equal(f.flow_direction,'first_to_last');
 assert.equal(f.approval_status,'PROPOSED_NOT_CANONICAL');
 const pts=f.points_xy_m, d=f.downstream;
 assert(pts.length>=2&&pts.every(xy));
 assert(pts.every(p=>inside(p,basinOf(f.basin_id).ring_xy_m)),f.feature_id+' outside basin');
 for(let i=0;i<pts.length-1;i++){
  assert(!exact(pts[i],pts[i+1]),f.feature_id+' zero edge');
  const mid=[(pts[i][0]+pts[i+1][0])/2,(pts[i][1]+pts[i+1][1])/2];
  assert(!inside(mid,sea),f.feature_id+' segment in sea');
  for(const [a,b] of shoreEdges)if(hit(pts[i],pts[i+1],a,b))assert(i===pts.length-2&&on(a,b,pts.at(-1)),f.feature_id+' illegal coast crossing');
 }
 const last=pts.at(-1);
 if(d.type==='coast_vertex'){assert.equal(d.coast_feature_id,'coast-mainland-001');assert(exact(last,line[d.vertex_index]));}
 else if(d.type==='coast_segment'){assert.equal(d.coast_feature_id,'coast-mainland-001');assert(on(line[d.segment_start_index],line[d.segment_start_index+1],last));}
 else if(d.type==='confluence'){assert(exact(last,flowOf(d.target_feature_id).points_xy_m[d.target_vertex_index]));}
 else if(d.type==='waterbody_inlet'){assert(lakeOf(d.waterbody_id).ring_xy_m.some(p=>exact(p,last)));}
 else assert.fail('unknown downstream type '+d.type);
 if(f.upstream_waterbody_id)assert(lakeOf(f.upstream_waterbody_id).ring_xy_m.some(p=>exact(p,pts[0])),f.feature_id+' starts outside lake');
}
for(const lake of lakes){
 const basin=basinOf(lake.basin_id).ring_xy_m;
 assert(lake.ring_xy_m.every(p=>inside(p,basin)),lake.feature_id+' outside basin');
}
for(const f of flows){
 for(let i=0;i<f.points_xy_m.length-1;i++)
 for(const lake of lakes)for(const [a,b] of edges(lake.ring_xy_m)){
  if(!hit(f.points_xy_m[i],f.points_xy_m[i+1],a,b))continue;
  const touchesStart=f.upstream_waterbody_id===lake.feature_id&&i===0&&on(a,b,f.points_xy_m[i]);
  const touchesEnd=f.downstream.type==='waterbody_inlet'&&f.downstream.waterbody_id===lake.feature_id&&i===f.points_xy_m.length-2&&on(a,b,f.points_xy_m[i+1]);
  assert(touchesStart||touchesEnd,'illegal flow through lake: '+f.feature_id+' '+lake.feature_id);
 }
}
for(let i=0;i<flows.length;i++)for(let j=i+1;j<flows.length;j++){
 const a=flows[i],b=flows[j],ap=a.points_xy_m,bp=b.points_xy_m;
 for(let k=0;k<ap.length-1;k++)for(let m=0;m<bp.length-1;m++){
  if(!hit(ap[k],ap[k+1],bp[m],bp[m+1]))continue;
  const valid=a.downstream.type==='confluence'&&a.downstream.target_feature_id===b.feature_id&&k===ap.length-2&&exact(ap.at(-1),bp[a.downstream.target_vertex_index])&&(m===a.downstream.target_vertex_index-1||m===a.downstream.target_vertex_index)
   ||b.downstream.type==='confluence'&&b.downstream.target_feature_id===a.feature_id&&m===bp.length-2&&exact(bp.at(-1),ap[b.downstream.target_vertex_index])&&(k===b.downstream.target_vertex_index-1||k===b.downstream.target_vertex_index);
  assert(valid,'unexpected stream crossing: '+a.feature_id+' '+b.feature_id);
 }
}
const reliefById=id=>{const a=r.value.relief_model.relief_areas.find(x=>x.feature_id===id);assert(a,'missing relief '+id);return a};
const valley=reliefById('relief-thermal-valley-001').ring_xy_m;
assert(lakeOf('pool-thermal-001').ring_xy_m.every(p=>inside(p,valley)));
assert(lakeOf('lake-freshwater-inland-001').ring_xy_m.every(p=>inside(p,reliefById('relief-southwestern-tundra-001').ring_xy_m)));
assert(inside(flowOf('river-vasyl-main-001').points_xy_m[0],reliefById('relief-northern-uplands-001').ring_xy_m));
assert(inside(flowOf('stream-southern-001').points_xy_m[0],reliefById('relief-southern-uplands-001').ring_xy_m));
for(const item of warm){const pts=flowOf(item.river_feature_id).points_xy_m;assert(item.start_vertex_index<item.end_vertex_index);assert(pts.slice(item.start_vertex_index,item.end_vertex_index+1).every(p=>inside(p,valley)));assert.equal(item.thermal_input_feature_id,'stream-thermal-pool-outlet-001');}
assert.equal(flows.find(x=>x.kind==='main_river').public_name,'Rio Vasyl');
assert.equal(flows.filter(x=>x.kind==='tributary').length,2);
assert.equal(flows.filter(x=>x.kind==='independent_stream').length,2);
assert.deepEqual(new Set(lakes.map(x=>x.kind)),new Set(['freshwater_inland_lake','brackish_coastal_lagoon','localized_thermal_pool']));
console.log('MW-004 hydrographic proposal PASS');
console.log(basins.length+' catchment envelopes; '+flows.length+' flowpaths; '+lakes.length+' waterbodies; '+warm.length+' localized warm reach');
console.log('Candidate coastline Git blob: '+c.gitSha);
console.log('Candidate relief Git blob: '+r.gitSha);
console.log('No canonical approval or hydrologic plausibility certification claimed');
