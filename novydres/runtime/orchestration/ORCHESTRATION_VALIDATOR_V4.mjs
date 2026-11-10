#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const fail=m=>{throw new Error('ORCHESTRATION_V4_BLOCK: '+m)};
const check=(v,m)=>{if(!v)fail(m)};
const read=(root,p)=>{check(typeof p==='string'&&!p.includes('..')&&!path.isAbsolute(p),'invalid path');const q=path.resolve(root,p);check(q.startsWith(path.resolve(root)+path.sep),'outside root');return fs.readFileSync(q)};
const json=(root,p)=>JSON.parse(read(root,p).toString('utf8'));
const blob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const verify=(root,r,label)=>{check(r&&blob(read(root,r.path))===r.blob_sha,'blob mismatch '+label)};
export function validateSourceReconciled(c,prev,live,prevLive,manifest){
 check(c.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V4','schema id');
 check(c.transition==='SOURCE_RECONCILED','transition');
 check(c.sequence===prev.sequence+1&&c.cycle_id===`CHR001-CYCLE-${String(c.sequence).padStart(4,'0')}`,'sequence/id');
 check(c.previous_cycle.path===`novydres/chronicles/CHR-001/orchestration/CYCLE_V${String(prev.sequence).padStart(4,'0')}.json`,'previous path');
 check(c.previous_cycle.blob_sha,'previous blob ref');
 check(c.status==='READY_FOR_DRAMATURGO'&&c.next_role==='DRAMATURGO','role/status');
 check(c.checkpoint.last_event_id===prev.checkpoint.last_event_id&&c.checkpoint.last_event_id===live.last_confirmed_event_id,'event id changed');
 check(c.checkpoint.last_closed_scene==='C05'&&c.checkpoint.next_scene==='C06'&&c.checkpoint.next_scene_status==='NOT_STARTED','scene cursor');
 check(c.checkpoint.pending_persistence===false&&c.checkpoint.mortal===true&&c.checkpoint.embrace_occurred===false,'persistence/mortality');
 check(c.plan.validity==='STALE'&&c.review.decision==='NOT_REVIEWED','plan/review');
 check(c.source_reconciliation?.approval_id==='APPROVAL-D06-003'&&c.source_reconciliation.source_only===true&&c.source_reconciliation.event_id_unchanged===true,'transition record');
 check(c.blocking?.code===null&&c.blocking?.reason===null,'obsolete blocking code');
 check(manifest.runtime.orchestration.current_cycle===c.manifest_path.replace('MANIFEST_V48.json',`chronicles/CHR-001/orchestration/CYCLE_V${String(c.sequence).padStart(4,'0')}.json`),'manifest cursor');
 check(manifest.runtime.orchestration.next_role==='DRAMATURGO'&&manifest.runtime.orchestration.next_scene_executable===false,'manifest role/scene flag');
 check(live.scene.status==='CLOSED'&&live.scene.last_event_id===c.checkpoint.last_event_id,'LIVE scene');
 check(live.stage.embrace_occurred===false&&live.stage.diegetic_period.includes('1970'),'LIVE chronology');
 check(JSON.stringify(live.character.resources)===JSON.stringify(prevLive.character.resources),'resource delta');
 return {ok:true,transition:'SOURCE_RECONCILED',cycle_id:c.cycle_id,last_event_id:c.checkpoint.last_event_id,next_role:c.next_role};
}
export function validateLatestV4(root=process.cwd()){
 const dir='novydres/chronicles/CHR-001/orchestration';
 const c=json(root,`${dir}/CYCLE_V0034.json`),prev=json(root,`${dir}/CYCLE_V0033.json`);
 const manifest=json(root,'novydres/MANIFEST_V48.json');
 for(const k of ['episode','character','knowledge','threads','history_index','live'])verify(root,c.refs[k],k);
 verify(root,c.previous_cycle,'previous cycle');
 const live=json(root,c.refs.live.path),prevLive=json(root,prev.refs.live.path);
 return validateSourceReconciled(c,prev,live,prevLive,manifest);
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){
 try{const i=process.argv.indexOf('--root');console.log(JSON.stringify(validateLatestV4(path.resolve(i<0?process.cwd():process.argv[i+1]))))}
 catch(e){console.error(String(e));process.exitCode=1}
}
