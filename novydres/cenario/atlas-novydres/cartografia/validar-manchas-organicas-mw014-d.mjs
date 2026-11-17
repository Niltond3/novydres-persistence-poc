#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url)),geo=JSON.parse(fs.readFileSync(path.join(root,'manchas-urbanas-organicas-mw014-d.proposal.json'),'utf8')),html=fs.readFileSync(path.join(root,'comparador-organico-mw014-d.html'),'utf8'),source=fs.readFileSync(path.join(root,'comparador-integral-nucleos-mw014-2010.html'),'utf8');
const parse=h=>JSON.parse(h.match(/<script id="map-data" type="application\/json">([\s\S]*?)<\/script>/)[1]),a=parse(source),b=parse(html);
const same=(x,y)=>JSON.stringify(x)===JSON.stringify(y);const keys=["land","islands","relief","crests","wild","rivers","water","thermal","basins","baymouth","cores","relations"];
if(keys.some(k=>!same(a[k],b[k])))throw Error('Regressão na geografia física ou nos nove pontos aprovados');
if(geo.polygons.length!==3||b.d_urban.length!==3)throw Error('Inventário de manchas incorreto');
const pin=(p,r)=>{let z=false;for(let i=0,j=r.length-1;i<r.length;j=i++){let x=r[i],y=r[j];if((x[1]>p[1])!==(y[1]>p[1])&&p[0]<(y[0]-x[0])*(p[1]-x[1])/(y[1]-x[1])+x[0])z=!z}return z};
const safe=p=>pin(p,a.land)&&!a.wild.some(r=>pin(p,r))&&!a.water.some(r=>pin(p,r));
let checks=0;for(let i=0;i<3;i++){let f=geo.polygons[i],ring=f.ring_xy_m.map(p=>p.map(n=>n/1000)),view=b.d_urban[i].ring;if(!same(view,ring))throw Error('Modelo visual diverge do JSON');
for(let j=0;j<ring.length-1;j++){let p=ring[j],q=ring[j+1],n=Math.max(1,Math.ceil(Math.hypot(q[0]-p[0],q[1]-p[1])/.05));for(let t=0;t<=n;t++){checks++;let v=t/n;if(!safe([p[0]+(q[0]-p[0])*v,p[1]+(q[1]-p[1])*v]))throw Error('Sobreposição de polígono com geografia física '+f.label)}}}
if(geo.approval.exact_polygon_geometry_owner_approved||geo.approval.canonical_status==='APPROVED')throw Error('Geometria erroneamente marcada como cânone');
console.log(JSON.stringify({status:'PASS',sampled_perimeters:checks,polygons:3,physical_layers:keys.length,unchanged_approved_nuclei:9,limitations:'Amostragem e não teste cadastral/GIS exato'}));
