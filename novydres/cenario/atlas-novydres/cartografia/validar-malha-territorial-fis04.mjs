#!/usr/bin/env node
/** MW-013 — Validador reproduzível da malha dos Ermos, composto por dados GitHub.
 * Requer Node moderno. Confere topologia, referências e comparador integral,
 * sem promover a proposta a cânone ou atribuir raions/rotas. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {dirname,join} from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=dirname(fileURLToPath(import.meta.url));
const textFile=name=>readFileSync(join(dir,name),'utf8');
const read=name=>JSON.parse(textFile(name));

const old=read('malha-territorial-ermos-fis04-2010.proposal.json');
const geo=read('malha-territorial-ermos-fis04-2010.refined.proposal.json');
const c=read('macrogeometria-litoral-baia-ilhas-2010.proposal.json');
const r=read('macrorelevo-2010.proposal.json');
const h=read('macrohidrografia-2010.proposal.json');
const html=textFile('comparador-integral-ermos-fis04-2010.html');
const contents=html.match(/<script id="map-data" type="application\/json">([\s\S]*?)<\/script>/);
assert(contents,'HTML context must exist');
const screen=JSON.parse(contents[1]);
const coast=c.proposed_geometry.mainland_coastline.points_xy_m,land=[...coast,[60000,50000],[60000,-50000]];
const lakes=h.hydro_model.waterbodies.map(x=>x.ring_xy_m);
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const km=ring=>ring.map(p=>p.map(v=>v/1000));
const orient=(a,b,x)=>(b[0]-a[0])*(x[1]-a[1])-(b[1]-a[1])*(x[0]-a[0]);
const cross=(a,b,c,d)=>orient(a,b,c)*orient(a,b,d)<0&&orient(c,d,a)*orient(c,d,b)<0;
function inside(p,poly){let yes=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];if((a[1]>p[1])!== (b[1]>p[1])&&p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0])yes=!yes;}return yes;}
function bounds(ring){let lowX=Infinity,lowY=Infinity,hiX=-Infinity,hiY=-Infinity;for(const p of ring){lowX=Math.min(lowX,p[0]);lowY=Math.min(lowY,p[1]);hiX=Math.max(hiX,p[0]);hiY=Math.max(hiY,p[1]);}return[lowX,lowY,hiX,hiY];}
function overlap(a,b){return!(a[2]<b[0]||b[2]<a[0]||a[3]<b[1]||b[3]<a[1]);}
function touches(a,b){if(!overlap(bounds(a),bounds(b)))return false;for(const p of a)if(inside(p,b))return true;for(const p of b)if(inside(p,a))return true;for(let i=0;i<a.length;i++)for(let j=0;j<b.length;j++)if(cross(a[i],a[(i+1)%a.length],b[j],b[(j+1)%b.length]))return true;return false;}
assert.equal(old.approval.composition_status,'OWNER_APPROVED_WITH_MANDATORY_REFINEMENT');
assert.equal(geo.approval.canonical_status,'NOT_APPROVED');
assert.equal(geo.approval.geometry_authority,'OWNER_APPROVED_NONCANONICAL_WORKING_BASELINE');
assert.equal(geo.approval.owner_approval_for_refined_geometry.decision,'APPROVED_NONCANONICAL_WORKING_BASELINE');
assert.equal(geo.geometry.segments.length,10);
assert.equal(old.geometry.segments.length,10);
const rings=geo.geometry.segments.map(x=>x.ring_xy_m);
const edges=[];
let points=0,edgesTested=0,selfTested=0;
for(let k=0;k<10;k++){
 const oldSeg=old.geometry.segments[k],newSeg=geo.geometry.segments[k];
 assert.equal(oldSeg.id,newSeg.id);
 assert(same(oldSeg.centerline_xy_m,newSeg.centerline_xy_m),'Centerline changed '+k);
 assert(!same(oldSeg.ring_xy_m,newSeg.ring_xy_m),'Refinement did not change ring '+k);
 assert(same(screen.before[k].ring,km(oldSeg.ring_xy_m)),'HTML before geometry mismatch '+k);
 assert(same(screen.after[k].ring,km(newSeg.ring_xy_m)),'HTML after geometry mismatch '+k);
 const ring=newSeg.ring_xy_m,n=ring.length;
 for(let i=0;i<n;i++){
   const a=ring[i],b=ring[(i+1)%n];points++;
   assert(a[0]>-60000&&a[0]<60000&&a[1]>-50000&&a[1]<50000,'Out of study frame');
   assert(inside(a,land),'Ermo entered the sea '+newSeg.id);
   for(const w of lakes)assert(!inside(a,w),'Ermo vertex entered waterbody '+newSeg.id);
   for(let j=0;j<coast.length-1;j++){edgesTested++;assert(!cross(a,b,coast[j],coast[j+1]),'Ermo crosses coast '+newSeg.id);}
   for(const w of lakes)for(let j=0;j<w.length;j++){edgesTested++;assert(!cross(a,b,w[j],w[(j+1)%w.length]),'Ermo crosses waterbody '+newSeg.id);}
   for(let j=i+2;j<n;j++){if(i===0&&j===n-1)continue;selfTested++;assert(!cross(a,b,ring[j],ring[(j+1)%n]),'Self-crossing '+newSeg.id);}
 }
 for(const w of lakes)for(const p of w){points++;assert(!inside(p,ring),'Ermo contains waterbody '+newSeg.id);}
}
for(let i=0;i<rings.length;i++)for(let j=i+1;j<rings.length;j++)if(touches(rings[i],rings[j]))edges.push([i,j]);
const reachable=new Set([0]);let grew=true;
while(grew){grew=false;for(const[a,b]of edges)if(reachable.has(a)&&!reachable.has(b)){reachable.add(b);grew=true}else if(reachable.has(b)&&!reachable.has(a)){reachable.add(a);grew=true}}
assert.equal(reachable.size,10,'Polygon envelope union graph disconnected');
const ctx=screen.context;
assert(same(ctx.coast,km(coast)),'Coast is missing or changed');
assert.equal(ctx.islands.length,3);
assert(same(ctx.islands.map(x=>x.ring),c.proposed_geometry.secondary_islands.map(x=>km(x.ring_xy_m))),'Islands mismatch');
assert.equal(ctx.relief.length,7);
assert(same(ctx.relief.map(x=>x.ring),r.relief_model.relief_areas.map(x=>km(x.ring_xy_m))),'Relief mismatch');
assert.equal(ctx.crests.length,3);
assert(same(ctx.crests.map(x=>x.points),r.relief_model.ridge_crest_axes.map(x=>km(x.points_xy_m))),'Crests mismatch');
assert.equal(ctx.basins.length,5);
assert(same(ctx.basins.map(x=>x.ring),h.hydro_model.catchment_areas.map(x=>km(x.ring_xy_m))),'Basins mismatch');
assert.equal(ctx.rivers.length,9);
assert(same(ctx.rivers.map(x=>x.points),h.hydro_model.watercourses.map(x=>km(x.points_xy_m))),'Rivers mismatch');
assert.equal(ctx.waterbodies.length,3);
assert(same(ctx.waterbodies.map(x=>x.ring),lakes.map(km)),'Waterbody mismatch');
assert.equal(ctx.thermal.length,1);
assert.equal(screen.before.length,10);
assert.equal(screen.after.length,10);
const inline=html.match(/<script>([\s\S]*?)<\/script><\/body>/);
assert(inline,'Comparative JavaScript not found');
new Function(inline[1]);
assert(html.includes('id="map-before"')&&html.includes('id="map-after"'),'Before/after panels missing');
assert(same(old.geometry.segments.map(x=>x.centerline_xy_m),geo.geometry.segments.map(x=>x.centerline_xy_m)),'Centerlines modified');
assert.equal(geo.validation.details.length,10);
console.log(JSON.stringify({status:'PASS',branch_parts:rings.length,union_components:1,vertices:rings.reduce((n,x)=>n+x.length,0),points,coast_water_edge_checks:edgesTested,self_intersection_pairs:selfTested,full_visual:{islands:3,relief:7,crests:3,basins:5,watercourses:9,waterbodies:3,thermal:1}}));

