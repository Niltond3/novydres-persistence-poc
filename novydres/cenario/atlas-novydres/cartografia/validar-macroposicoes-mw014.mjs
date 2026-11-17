#!/usr/bin/env node
// MW-014 B: validation of structured sources and exact HTML data projection.
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {dirname,join} from 'node:path';
const dir=dirname(fileURLToPath(import.meta.url));
const read=n=>readFileSync(join(dir,n),'utf8'),load=n=>JSON.parse(read(n));
const model=load('macroposicoes-nucleos-urbanos-2010.proposal.json');
const ermo=load('malha-territorial-ermos-fis04-2010.refined.proposal.json');
const coast=load('macrogeometria-litoral-baia-ilhas-2010.proposal.json');
const rel=load('macrorelevo-2010.proposal.json');
const hyd=load('macrohidrografia-2010.proposal.json');
const district=load('../raions-oficiais-2010.json');
const html=read('comparador-integral-nucleos-mw014-2010.html');
let checks=0;
function requireOk(v,msg){if(!v)throw Error('MW014_B_FAILURE: '+msg);checks++;}
const match=html.match(/<script id="map-data" type="application\/json">([\s\S]*?)<\/script>/);
requireOk(!!match,'visual model JSON exists');
const visual=JSON.parse(match[1]);
const km=ps=>ps.map(p=>p.map(q=>q/1000)),same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
requireOk(model.approval.canonical_status==='NOT_APPROVED'&&model.approval.owner_approval===false,'unapproved status');
requireOk(model.approval.previous_candidate_a==='REJECTED_BY_OWNER','A rejection is preserved');
requireOk(model.nuclei.length===9&&visual.cores.length===9,'nine nuclear points');
requireOk(model.nuclei.every(n=>n.geometry_type==='Point'),'no fabricated urban polygons');
requireOk(same(model.nuclei.map(n=>n.subject_id).sort(),district.raions.map(n=>n.subject_id).sort()),'canonical nine subject IDs');
const land=[...coast.proposed_geometry.mainland_coastline.points_xy_m,[60000,50000],[60000,-50000]],wild=ermo.geometry.segments.map(n=>n.ring_xy_m),waters=hyd.hydro_model.waterbodies.map(n=>n.ring_xy_m);
function inside(p,ring){let val=false;for(let i=0,j=ring.length-1;i<ring.length;j=i++){const a=ring[i],b=ring[j];if((a[1]>p[1])!==(b[1]>p[1])&&p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0])val=!val;}return val;}
const safe=p=>inside(p,land)&&!wild.some(n=>inside(p,n))&&!waters.some(n=>inside(p,n));
for(const item of model.nuclei){requireOk(safe(item.coordinates_xy_m),item.label+' is on safe mainland');
for(let i=0;i<48;i++){const theta=2*Math.PI*i/48,p=item.coordinates_xy_m;
requireOk(safe([p[0]+1400*Math.cos(theta),p[1]+1400*Math.sin(theta)]),item.label+' 1400m sample buffer');}}
const pairs=[
['land',land,'ring'],
['islands',coast.proposed_geometry.secondary_islands.map(n=>n.ring_xy_m),'polygon'],
['relief',rel.relief_model.relief_areas.map(n=>n.ring_xy_m),'polygon'],
['crests',rel.relief_model.ridge_crest_axes.map(n=>n.points_xy_m),'line'],
['wild',ermo.geometry.segments.map(n=>n.ring_xy_m),'polygon'],
['rivers',hyd.hydro_model.watercourses.map(n=>n.points_xy_m),'line'],
['water',hyd.hydro_model.waterbodies.map(n=>n.ring_xy_m),'polygon'],
['basins',hyd.hydro_model.catchment_areas.map(n=>n.ring_xy_m),'polygon']
];
for(const [key,source,kind] of pairs){
if(key==='land'){requireOk(same(visual.land,km(source)),key+' exact geometry');continue;}
requireOk(visual[key].length===source.length,key+' complete inventory');
requireOk(source.every((s,i)=>same(visual[key][i],km(s))),key+' exact coordinates');
}
const thermals=hyd.hydro_model.localized_thermal_reaches.map(t=>{
const river=hyd.hydro_model.watercourses.find(r=>r.feature_id===t.river_feature_id);
requireOk(!!river,'thermal reach parent river');
return river.points_xy_m.slice(t.start_vertex_index,t.end_vertex_index+1);
});
requireOk(thermals.length===visual.thermal.length,'thermal reach count');
requireOk(thermals.every((t,i)=>same(visual.thermal[i],km(t))),'thermal reach derived from source river');
requireOk(same(visual.baymouth,[coast.proposed_geometry.mainland_coastline.points_xy_m[6].map(v=>v/1000),coast.proposed_geometry.mainland_coastline.points_xy_m[33].map(v=>v/1000)]),'bay mouth');
requireOk(visual.cores.every((c,i)=>c.i===model.nuclei[i].number&&same(c.p,model.nuclei[i].coordinates_xy_m.map(v=>v/1000))),'all points derive from model');
function hit(a,b){let count=0;for(let i=0;i<=300;i++){let p=a.map((v,k)=>v+(b[k]-v)*i/300);if(wild.some(w=>inside(p,w)))count++;}return count;}
const loc=id=>model.nuclei.find(n=>n.subject_id===id).coordinates_xy_m;
requireOk(hit(loc('district-chelsea'),loc('district-sulfok'))===0,'direct Kingswell–Sulfok sample open');
requireOk(hit(loc('district-bukovie'),loc('district-chelsea'))>0,'Bukovie–Kingswell crosses Ermo');
requireOk(hit(loc('district-bukovie'),loc('district-alexandria'))>0,'Bukovie–Alexandria crosses Ermo');
requireOk(html.includes('grid-template-columns:1fr')&&html.includes('map-before')&&html.includes('map-after'),'mobile stacked before-after');
requireOk(!html.includes('urbanized_core_footprint_candidate'),'rejected geometry not copied');
console.log(JSON.stringify({status:'PASS_SYNTHETIC',checks,nuclei:9,ermo:visual.wild.length,islands:visual.islands.length,relief:visual.relief.length,rivers:visual.rivers.length,water:visual.water.length,thermal:visual.thermal.length,limit:'No actual-browser screenshot, geodesy or exact polygon-union certification'}));
