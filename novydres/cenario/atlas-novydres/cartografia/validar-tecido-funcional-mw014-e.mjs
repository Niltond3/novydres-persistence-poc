#!/usr/bin/env node
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const folder=path.dirname(fileURLToPath(import.meta.url));
const read=f=>fs.readFileSync(path.join(folder,f),'utf8');
const model=JSON.parse(read('ocupacao-funcional-mw014-e.proposal.json'));
const html=read('comparador-tecido-funcional-mw014-e.html');
const source=read('comparador-integral-nucleos-mw014-2010.html');
const extract=s=>JSON.parse(s.match(/<script id="map-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const a=extract(source), b=extract(html), same=(x,y)=>JSON.stringify(x)===JSON.stringify(y);
const keys=["land","islands","relief","crests","wild","rivers","water","thermal","basins","baymouth","cores","relations"];
if(keys.some(k=>!same(a[k],b[k])))throw Error("PHYSICAL_OR_NUCLEI_CHANGED");
if(!same(b.e_occupancy.runs,model.geometry.runs))throw Error("SOURCE_DATA_MISMATCH");
const {runs}=model.geometry;let count=[0,0,0,0,0,0],total=0;
for(const row of runs){let n=0;for(const [start,len,code] of row){if(start!==n||len<=0||code<0||code>5)throw Error('RLE_INVALID');n+=len;count[code]+=len;total+=len}if(n!==240)throw Error('BAD_WIDTH')}
if(runs.length!==200||total!==48000||!same(count,model.stats.class_cells))throw Error("GRID_COUNTS_INVALID");
if(model.approvals.urban_classes_and_shapes!=="CANDIDATE_OWNER_VISUAL_REVIEW_PENDING"||model.approvals.canonization!=="NOT_APPROVED")throw Error("BAD_APPROVAL");
console.log(JSON.stringify({status:"PASS",cells:total,runs:runs.reduce((n,row)=>n+row.length,0),counts:count,physical_layers_unchanged:keys.length,owner_approval:"PENDING",limitation:"RLE and physical vectors verified; no actual-browser screenshot verified."}));
