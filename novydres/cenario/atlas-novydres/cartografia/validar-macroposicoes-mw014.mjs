#!/usr/bin/env node
// MW-014: a cartografia é derivada de dados, nunca do HTML ou da arte.
import {readFileSync} from 'node:fs';
import {dirname,join} from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=dirname(fileURLToPath(import.meta.url)),load=f=>JSON.parse(readFileSync(join(dir,f),'utf8'));
const doc=load('macroposicoes-nucleos-urbanos-2010.proposal.json');
const ermo=load('malha-territorial-ermos-fis04-2010.refined.proposal.json');
const coast=load('macrogeometria-litoral-baia-ilhas-2010.proposal.json');
const hyd=load('macrohidrografia-2010.proposal.json');
const rel=load('macrorelevo-2010.proposal.json');
const inside=(p,ring)=>{let z=false;for(let i=0,j=ring.length-1;i<ring.length;j=i++){let a=ring[i],b=ring[j];if((a[1]>p[1])!==(b[1]>p[1])&&p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0])z=!z;}return z;};
const land=[...coast.proposed_geometry.mainland_coastline.points_xy_m,[60000,50000],[60000,-50000]];
const wilderness=ermo.geometry.segments.map(x=>x.ring_xy_m);
const water=hyd.hydro_model.waterbodies.map(x=>x.ring_xy_m);
let checks=0;
function assert(ok,reason){if(!ok)throw new Error('FAIL '+reason);checks++;}
const usable=p=>inside(p,land)&&!wilderness.some(x=>inside(p,x))&&!water.some(x=>inside(p,x));
assert(doc.approval.canonical_status==='NOT_APPROVED'&&!doc.approval.owner_geometry_approval,'never canonical without owner');
assert(doc.urban_nuclei.length===9,'nine named candidate nuclei');
assert(new Set(doc.urban_nuclei.map(x=>x.raion_subject_ref)).size===9,'distinct raion identifiers only (not polygons)');
assert(ermo.geometry.segments.length===10,'same refined ermo envelopes');
assert(rel.relief_model.relief_areas.length===7,'all relief areas unchanged');
assert(hyd.hydro_model.watercourses.length===9,'all waterways unchanged');
assert(hyd.hydro_model.waterbodies.length===3,'all waterbodies unchanged');
assert(coast.proposed_geometry.secondary_islands.length===3,'all islands unchanged');
for(const shape of [...doc.urban_nuclei,doc.conurbation_candidate]){
 const ring=shape.ring_xy_m;
 assert(ring.length>=4&&ring[0][0]===ring.at(-1)[0]&&ring[0][1]===ring.at(-1)[1],shape.feature_id+' closed ring');
 for(let i=0;i<ring.length-1;i++){
  let a=ring[i],b=ring[i+1],n=Math.max(1,Math.ceil(Math.hypot(b[0]-a[0],b[1]-a[1])/120));
  for(let j=0;j<=n;j++){let p=[a[0]+(b[0]-a[0])*j/n,a[1]+(b[1]-a[1])*j/n];assert(usable(p),shape.feature_id+' encroaches water/wilderness at '+JSON.stringify(p));}
 }
}
const center=id=>doc.urban_nuclei.find(x=>x.raion_subject_ref===id).center_xy_m;
function wildernessCount(a,b){let n=0;for(let i=0;i<=160;i++){let p=a.map((v,k)=>v+(b[k]-v)*i/160);if(wilderness.some(w=>inside(p,w)))n++;}return n;}
assert(wildernessCount(center('district-chelsea'),center('district-sulfok'))===0,'Kingswell-Sulfok direct contact clear of Ermo');
assert(wildernessCount(center('district-bukovie'),center('district-chelsea'))>0,'Bukovie-Kingswell direct separation');
assert(wildernessCount(center('district-bukovie'),center('district-alexandria'))>0,'Bukovie-Alexandria direct separation');
console.log(JSON.stringify({status:'PASS_SAMPLED_PREVALIDATION',checks,nuclei:9,ermo_parts:10,relief:7,watercourses:9,waterbodies:3,islands:3,limits:'Synthetic local candidate, no exact union or browser verification'}));
