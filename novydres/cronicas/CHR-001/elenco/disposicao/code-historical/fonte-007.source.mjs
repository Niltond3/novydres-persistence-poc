#!/usr/bin/env node
// NOVYDRES CHR-001 / V2: ativação por autorização explícita antes de C15.
import fs from 'node:fs';
import path from 'node:path';
import {validateState,gitBlobSha} from './VALIDATOR_V1.mjs';
const B='novydres/chronicles/CHR-001/npc-disposition/';
const fail=s=>{throw new Error('NPC_C15_ACTIVATION_BLOCK: '+s)};
const insist=(ok,s)=>{if(!ok)fail(s)};
function raw(root,p){
 insist(typeof p==='string'&&!p.includes('..')&&!p.includes('\\')&&!path.isAbsolute(p),'unsafe path');
 const target=path.resolve(root,p);insist(target.startsWith(path.resolve(root)+path.sep),'outside root');
 return fs.readFileSync(target);
}
const read=(root,p)=>JSON.parse(raw(root,p).toString('utf8'));
export function validateActivation(root){
 const m=read(root,B+'ACTIVATION_C15_V2.json');
 insist(m.schema_id==='CHR001_NPC_DISPOSITION_C15_ACTIVATION_V2'&&m.chronicle_id==='CHR-001'&&m.status==='ACTIVE_C15','bad scope');
 insist(m.authorization?.instruction==='Vamos reiniciar a C15 já com as mecanicas'&&m.authorization.kind==='EXPLICIT_ADMINISTRATIVE_NO_STORY_DELTA','player authorization');
 insist(m.allowed_scene==='C15'&&m.previous_scene==='C14'&&m.no_dramaturgo_replacement===true,'scene boundary');
 insist(m.activation_marker==='CHR001-ADMIN-C15-20261106-001','admin marker');
 insist(m.guards?.no_changes_to_closed_scenes&&m.guards.no_xp_fv_delta&&m.guards.no_g28_early_write&&m.guards.no_new_cycle_for_activation&&m.guards.no_pc_action_presumed,'guards');
 const paths={cycle:'novydres/chronicles/CHR-001/orchestration/CYCLE_V0012.json',live:'novydres/chronicles/CHR-001/LIVE_v027.json',episode:'novydres/chronicles/CHR-001/episodes/M2.04_v013.source.txt',stage_state:B+'STATE_V001.json',active_state:B+'STATE_V002.json'};
 for(const [k,p] of Object.entries(paths)){
  const ref=m.refs[k];insist(ref?.path===p&&/^[a-f0-9]{40}$/.test(ref.blob_sha),'bad '+k+' ref');
  insist(gitBlobSha(raw(root,p))===ref.blob_sha,'SHA mismatch '+k);
 }
 insist(validateState(root,paths.stage_state).status==='STAGED','stage invalid');
 const s=read(root,paths.stage_state),a=read(root,paths.active_state),c=read(root,paths.cycle),l=read(root,paths.live);
 insist(a.status==='ACTIVE'&&a.previous_version===paths.stage_state&&a.activation_event_id===m.activation_marker,'state activation mismatch');
 insist(JSON.stringify(a.checkpoint)===JSON.stringify(s.checkpoint)&&JSON.stringify(a.actors)===JSON.stringify(s.actors),'retroactive state mutation');
 insist(c.status==='READY_FOR_NARRATOR'&&c.next_role==='NARRADOR'&&c.checkpoint.next_scene==='C15'&&c.checkpoint.last_closed_scene==='C14'&&c.checkpoint.next_scene_status==='NOT_STARTED'&&c.checkpoint.pending_persistence===false,'C15 not ready');
 insist(c.checkpoint.last_event_id===l.last_confirmed_event_id&&a.checkpoint.last_event_id===c.checkpoint.last_event_id,'event drift');
 insist(['REVISED','VALIDATED'].includes(c.plan?.validity)&&c.plan.reviewed_against_event_id===c.checkpoint.last_event_id,'not reviewed');
 const cycles=fs.readdirSync(path.join(root,'novydres/chronicles/CHR-001/orchestration')).filter(x=>/^CYCLE_V\d{4}\.json$/.test(x)).sort();
 insist(cycles.at(-1)==='CYCLE_V0012.json','newer cycle, cannot restart C15');
 insist(!Object.hasOwn(l,'npc_disposition_state_ref'),'baseline LIVE mutated');
 return {ok:true,scene:'C15',status:'ACTIVE_C15',npc_count:Object.keys(a.actors).length};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){
 try{const i=process.argv.indexOf('--root');console.log(JSON.stringify(validateActivation(path.resolve(i<0?process.cwd():process.argv[i+1]))));}
 catch(e){console.error(String(e));process.exitCode=1;}
}
