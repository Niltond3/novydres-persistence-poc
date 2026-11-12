#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';

const fail = m => { throw new Error(`ORCHESTRATION_V11_BLOCK: ${m}`); };
const check = (v,m) => { if (!v) fail(m); };
const sha = b => crypto.createHash('sha1').update(Buffer.from(`blob ${b.length}\0`)).update(b).digest('hex');
const safeRead = (root,p) => {
  check(typeof p==='string' && !path.isAbsolute(p) && !p.split(/[\\/]/).includes('..'),'invalid relative path');
  const q=path.resolve(root,p); check(q.startsWith(path.resolve(root)+path.sep),'path escapes repository');
  return fs.readFileSync(q);
};
const readJson=(root,p)=>JSON.parse(safeRead(root,p).toString('utf8'));
const verify=(root,r,label)=>check(r && sha(safeRead(root,r.path))===r.blob_sha,`blob mismatch: ${label}`);
const git=(root,args)=>{
 const p=spawnSync('git',['-C',root,...args],{encoding:'utf8',maxBuffer:4*1024*1024});
 check(p.status===0 && typeof p.stdout==='string',`git ${args.join(' ')} failed: ${(p.stderr||p.error?.message||'').trim()}`); return p.stdout.trim();
};
const jsonSchema=(root,schemaRef,document,label)=>{
 // Full Draft 2020-12 validation is an independent gate in ORCHESTRATION_SCHEMA_TESTS_V11.py.
 // Keep this runtime validator subprocess-free for schema evaluation; verify the exact schema blob
 // here and guard the cycle identity/required transition fields used by this contract.
 verify(root,schemaRef,`${label} schema`);
 for(const k of ['schema_id','cycle_id','sequence','manifest_path','manifest_ref','previous_cycle','transition','status','checkpoint','refs','architecture','episode_closure'])
  check(Object.prototype.hasOwnProperty.call(document,k),`${label} missing schema field ${k}`);
 check(document.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V11' && document.sequence===37,`${label} schema identity`);
};
const cyclePath=n=>`novydres/chronicles/CHR-001/orchestration/CYCLE_V${String(n).padStart(4,'0')}.json`;
const samePairs=(a,b,keys)=>keys.every(k=>a?.[k]?.path===b?.[k]?.path && a?.[k]?.blob_sha===b?.[k]?.blob_sha);
const mechanicalKeys=['rules_provenance','target_sheet','adjudication_gate','motor_manual','xp_policy','xp_audit','act_resolution_schema','xp_envelope','settlement_record'];
const stateKeys=['live','history_index','episode','character','knowledge','threads'];
const runtimePaths={
 orchestration_contract:'novydres/runtime/orchestration/ORCHESTRATION_CONTRACT_V9.md',
 cycle_schema:'novydres/runtime/orchestration/CYCLE_SCHEMA_V11.json',
 cycle_validator:'novydres/runtime/orchestration/ORCHESTRATION_VALIDATOR_V11.mjs',
 cycle_tests:'novydres/runtime/orchestration/ORCHESTRATION_TESTS_V11.mjs',
 cycle_schema_tests:'novydres/runtime/orchestration/ORCHESTRATION_SCHEMA_TESTS_V11.py',
 preparation_dossier_schema:'novydres/runtime/provocation-prep/PROVOCATION_DOSSIER_SCHEMA_V6.json',
 preparation_sidecar_schema:'novydres/runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V6.json',
 start_here:'novydres/runtime/orchestration/START_HERE_V8.md'
};

export function validateEpisodeClosureTransition(c,prev){
 check(c.transition==='EPISODIC_CLOSURE_APPROVED' && c.status==='PROVOCATION_EPISODE_CLOSED' && c.next_role==='NONE','closure transition/status/role');
 check(c.sequence===37 && c.cycle_id==='CHR001-CYCLE-0037' && c.provocation_id==='M3.01','closure cycle identity');
 check(prev?.sequence===36 && prev.cycle_id==='CHR001-CYCLE-0036' && prev.transition==='CLOSURE_RECOMMENDED' && prev.status==='PROVOCATION_CLOSURE_PENDING','source must be pending C36');
 check(prev.pending_player_decision==='CLOSE_M3_01_AS_ALTERNATE_OR_CONTINUE','C36 does not expose the reviewed choice');
 check(c.previous_cycle?.path===cyclePath(36) && c.previous_cycle?.blob_sha,'C37 must pin C36');
 check(c.checkpoint?.last_event_id==='CHR001-M301-C05-22-20261109-001' && JSON.stringify(c.checkpoint)===JSON.stringify(prev.checkpoint),'closure changed checkpoint/event/cursor');
 check(samePairs(c.refs,prev.refs,stateKeys),'closure changed a state ref');
 check(c.operational_gates?.mechanical_matrix_ref?.path===prev.operational_gates?.mechanical_matrix_ref?.path && c.operational_gates?.mechanical_matrix_ref?.blob_sha===prev.operational_gates?.mechanical_matrix_ref?.blob_sha,'closure changed mechanical matrix');
 check(samePairs(c.operational_gates?.mechanical_sources,prev.operational_gates?.mechanical_sources,mechanicalKeys),'closure changed mechanical source refs');
 check(samePairs(c.activation,prev.activation,['authorization','d07_activation','truth_package','architecture_contract']),'closure changed activation evidence');
 check(c.plan?.validity==='STALE' && c.plan?.reviewed_against_event_id===c.checkpoint.last_event_id,'closed episode plan must be stale at same event');
 check(c.review?.decision==='EPISODE_CLOSED' && c.review?.against_last_event_id===c.checkpoint.last_event_id,'closure review is not event-anchored');
 check(c.pending_player_decision===null && c.blocking?.code===null && c.blocking?.reason===null,'closure left an unresolved blocker');
 for(const k of ['architecture_active','d07_active']) check(c.operational_gates[k]===true,`closure lost active gate ${k}`);
 for(const k of ['story_preparation_ready','mechanical_scene_ready','scene_ready','narrator_permission']) check(c.operational_gates[k]===false,`closure opened gate ${k}`);
 for(const k of ['no_story_delta_in_prep','no_xp_fv_delta_in_prep','g28_scene_only','frozen_unchanged','no_public_spoilers']) check(c.guards?.[k]===true,`closure guard not preserved: ${k}`);
 const e=c.episode_closure;
 check(e?.closure_id==='CHR001-M301-EPISODIC-CLOSE-C05-22' && e.scope==='M3.01_EPISODE_ONLY' && e.decision==='CLOSE_M3_01_EPISODIC_ALTERNATE','episode closure scope/choice');
 check(e.creation_route_disposition==='UNCHANGED_PENDING' && e.scene_authorized===false && e.narrator_authorized===false && e.state_delta===false,'closure changed route or authority/state');
 check(e.source_cycle_ref?.path===cyclePath(36) && e.source_cycle_ref?.blob_sha===c.previous_cycle.blob_sha,'closure source ref differs from C36');
 check(e.preserved_threads_ref?.path===prev.refs.threads.path && e.preserved_threads_ref?.blob_sha===prev.refs.threads.blob_sha,'closure did not preserve thread ledger pin');
 check(c.architecture?.player_episode_closure_decision?.path==='novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_M301_EPISODIC_CLOSURE_V001_PLAYER_SAFE.json','missing exact player decision pin');
 return {ok:true,transition:c.transition,cycle_id:c.cycle_id,closed_episode:'M3.01',last_event_id:c.checkpoint.last_event_id,route_disposition:'UNCHANGED_PENDING',scene_ready:false,narrator_permission:false};
}

export function verifyHistory(root,current){
 let n=current.sequence-1, child=current, checked=1;
 while(n>=1){
  const p=cyclePath(n), bytes=safeRead(root,p), c=JSON.parse(bytes.toString('utf8'));
  check(c.sequence===n && c.cycle_id===`CHR001-CYCLE-${String(n).padStart(4,'0')}`,`history identity mismatch at ${p}`);
  check(child.previous_cycle?.path===p && child.previous_cycle?.blob_sha===sha(bytes),`predecessor link mismatch at ${p}`);
  checked++;
  if(n===1){check(c.previous_cycle===null || c.previous_cycle===undefined,'cycle 1 unexpectedly has a predecessor');break;}
  child=c; n--;
 }
 return checked;
}

export function validateLatestV11(root=process.cwd()){
 root=path.resolve(root);
 const dir=path.join(root,'novydres/chronicles/CHR-001/orchestration');
 const nums=fs.readdirSync(dir).map(x=>/^CYCLE_V(\d{4})\.json$/.exec(x)).filter(Boolean).map(x=>Number(x[1])).sort((a,b)=>b-a);
 check(nums[0]===37,'latest numeric cycle is not CYCLE_V0037');
 const cp=cyclePath(37), c=readJson(root,cp), prev=readJson(root,cyclePath(36));
 check(c.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V11','cycle schema id');
 check(c.manifest_path==='novydres/MANIFEST_V52.json' && c.manifest_ref?.path===c.manifest_path,'current manifest path');
 verify(root,c.manifest_ref,'current manifest');
 for(const [k,r] of Object.entries(c.refs)) verify(root,r,`state.${k}`);
 for(const [k,r] of Object.entries(c.architecture)) verify(root,r,`architecture.${k}`);
 for(const [k,r] of Object.entries(c.activation)) verify(root,r,`activation.${k}`);
 verify(root,c.plan.dossier,'preparation dossier'); verify(root,c.plan.sidecar,'preparation sidecar');
 verify(root,c.operational_gates.mechanical_matrix_ref,'mechanical matrix');
 for(const [k,r] of Object.entries(c.operational_gates.mechanical_sources)) verify(root,r,`mechanical.${k}`);
 jsonSchema(root,c.architecture.cycle_schema,c,'CYCLE_V0037');
 const manifest=readJson(root,c.manifest_path), orch=manifest.runtime?.orchestration, na=manifest.runtime?.narrative_architecture;
 check(manifest.branch==='master','manifest branch');
 check(orch?.current_cycle===cp && orch?.status===c.status && orch?.next_role===c.next_role && orch?.pending_player_decision===null,'manifest operational cursor/status');
 check(orch?.next_scene===c.checkpoint.next_scene && orch?.next_scene_status===c.checkpoint.next_scene_status && orch?.next_scene_executable===false,'manifest scene cursor/readiness');
 for(const k of ['architecture_active','d07_active','story_preparation_ready','mechanical_scene_ready','scene_ready','narrator_permission']) check(orch.operational_gates?.[k]===c.operational_gates[k],`manifest gate mismatch: ${k}`);
 for(const [k,p] of Object.entries(runtimePaths)){
  check(c.architecture[k]?.path===p,`fixed runtime path ${k}`);
  const m=na?.blob_refs?.[k]; check(m?.path===p && m?.blob_sha===c.architecture[k].blob_sha,`manifest runtime blob ${k}`);
 }
 check(orch.contract===runtimePaths.orchestration_contract && orch.contract_blob_sha===c.architecture.orchestration_contract.blob_sha,'manifest contract pin');
 check(orch.cycle_schema===runtimePaths.cycle_schema && orch.cycle_schema_blob_sha===c.architecture.cycle_schema.blob_sha,'manifest schema pin');
 check(orch.validator===runtimePaths.cycle_validator && orch.validator_blob_sha===c.architecture.cycle_validator.blob_sha,'manifest validator pin');
 check(orch.tests===runtimePaths.cycle_tests && orch.tests_blob_sha===c.architecture.cycle_tests.blob_sha,'manifest tests pin');
 check(orch.schema_tests===runtimePaths.cycle_schema_tests && orch.schema_tests_blob_sha===c.architecture.cycle_schema_tests.blob_sha,'manifest schema tests pin');
 check(orch.entrypoint===runtimePaths.start_here && orch.entrypoint_blob_sha===c.architecture.start_here.blob_sha,'manifest entrypoint pin');
 check(na?.d06===c.architecture.d06.path && na?.d08===c.architecture.d08.path && na?.d09===c.architecture.d09.path && na?.d10_schema_registry===c.architecture.d10_schema_registry.path && na?.d10_role_adapters===c.architecture.d10_role_adapters.path && na?.d10_validator===c.architecture.d10_validator.path && na?.d10_results===c.architecture.d10_results.path && na?.promotion_inventory===c.architecture.promotion_inventory.path,'manifest authoring/promotion pointers');
 for(const [k,r] of Object.entries(c.architecture)) check(na.blob_refs?.[k]?.path===r.path && na.blob_refs?.[k]?.blob_sha===r.blob_sha,`manifest architecture pin ${k}`);
 check(manifest.runtime.last_confirmed_narrative_event===c.checkpoint.last_event_id,'manifest last event');
 check(manifest.runtime.marco_M3_status==='M3.01_EPISODE_CLOSED_M3.02_NOT_STARTED','manifest Marco status');
 const prep=manifest.runtime.current_m3_01_preparation;
 check(prep?.validity==='STALE' && prep?.story_preparation_ready===false && prep?.scene_ready===false && prep?.narrator_permission===false,'manifest preparation/gates');
 const d06=readJson(root,c.architecture.d06.path),d09=readJson(root,c.architecture.d09.path),decision=readJson(root,c.architecture.player_episode_closure_decision.path);
 check(d06.document_id==='D06_CHRONICLE_BIBLE_V031' && d06.finite_progression.episode_closure_gate.status==='SATISFIED_FOR_M3_01_EPISODE_ONLY','D06 closure criteria');
 check(d09.document_id==='D09_GUIDED_CREATION_PROGRESSION_V024_PLAYER_SAFE' && d09.authorial_target_closure.status==='PENDING_UNTIL_ACTUAL_EVIDENCE','D09 target remains pending');
 check(d09.operational_gate.scene_ready===false && d09.operational_gate.narrator_permission===false,'D09 operational gates');
 check(decision.decision==='CLOSE_M3_01_EPISODIC_ALTERNATE' && decision.scope==='M3.01_EPISODE_ONLY','player decision receipt');
 validateEpisodeClosureTransition(c,prev);
 const head=git(root,['rev-parse','HEAD']), parent=git(root,['rev-parse','HEAD^']);
 check(c.source_head_sha===head || c.source_head_sha===parent,'source_head must be current precommit HEAD or its first parent');
 if(c.source_head_sha===parent){
  const refs=[{path:cp,blob_sha:sha(safeRead(root,cp))},c.manifest_ref,...Object.values(c.refs),...Object.values(c.architecture),...Object.values(c.activation),c.plan.dossier,c.plan.sidecar,c.operational_gates.mechanical_matrix_ref,...Object.values(c.operational_gates.mechanical_sources)];
  const seen=new Set(); for(const r of refs){const key=`${r.path}:${r.blob_sha}`;if(seen.has(key))continue;seen.add(key);check(git(root,['rev-parse',`${head}:${r.path}`])===r.blob_sha,`published tree pin mismatch: ${r.path}`);}
 }
 return {ok:true,cycle_id:c.cycle_id,transition:c.transition,status:c.status,next_role:c.next_role,last_event_id:c.checkpoint.last_event_id,history_cycles_checked:verifyHistory(root,c),architecture_pins_checked:Object.keys(c.architecture).length,state_refs_unchanged:true,mechanical_refs_unchanged:true,scene_ready:false,narrator_permission:false,source_head_sha:c.source_head_sha,published_tree_checked:c.source_head_sha===parent};
}
if(process.argv[1] && path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){
 try{const i=process.argv.indexOf('--root');const root=path.resolve(i<0?process.cwd():process.argv[i+1]);console.log(JSON.stringify(validateLatestV11(root)));}
 catch(e){console.error(String(e));process.exitCode=1;}
}
