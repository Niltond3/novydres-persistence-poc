import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {execFileSync} from 'node:child_process';import {validateLatestV20} from './ORCHESTRATION_VALIDATOR_V20.mjs';
const C='novydres/chronicles/CHR-001/orchestration/CYCLE_V0045.json',P='novydres/chronicles/CHR-001/',M='novydres/MANIFEST_V63.json';
const fail=m=>{throw Error('CHR001_V23_BLOCK:'+m)};const insist=(v,m)=>{if(!v)fail(m)};
const b=(root,p)=>fs.readFileSync(path.join(root,p));const j=(root,p)=>JSON.parse(b(root,p).toString('utf8'));
const hash=x=>crypto.createHash('sha1').update(Buffer.from('blob '+x.length+'\0')).update(x).digest('hex');
const verify=(root,r)=>{insist(r?.path&&/^[0-9a-f]{40}$/.test(r.blob_sha),'bad ref');insist(hash(b(root,r.path))===r.blob_sha,'SHA pin '+r.path)};
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
export function validateC45(c,m,d,s,c44,t,k){
insist(c.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V22'&&c.cycle_id==='CHR001-CYCLE-0045'&&c.sequence===45,'identity');
insist(c.transition==='DRAMATURGO_REVIEW_COMPLETED'&&c.status==='READY_FOR_NARRATOR'&&c.next_role==='NARRADOR'&&c.narrator_prompt_required,'role');
insist(c.checkpoint.last_closed_scene==='C01'&&c.checkpoint.next_scene==='C02'&&c.checkpoint.next_scene_status==='NOT_STARTED','scene boundary');
insist(c.checkpoint.last_event_id===c44.checkpoint.last_event_id&&!c.checkpoint.pending_persistence&&c.checkpoint.mortal&&!c.checkpoint.embrace_occurred,'source state');
insist(equal(c.refs,c44.refs)&&equal(c.scene_commit,c44.scene_commit),'C44 six refs & G28 unchanged');
insist(c.previous_cycle.path===P+'orchestration/CYCLE_V0044.json'&&c.previous_cycle.blob_sha==='5bc4f59519fb7e7e3f017eea975a154e84e7efc1','C44 parent pin');
insist(c.manifest_path===M&&c.manifest_ref.path===M,'manifest ref');
insist(c.plan.validity==='READY_PROSPECTIVE_NO_EVENT'&&c.plan.dossier.path===P+'preparations/M3.02_DOSSIER_V6.json'&&c.plan.sidecar.path===P+'preparations/M3.02_LONGITUDINAL_SIDECAR_V6.json','plan');
insist(d.schema_id==='NOVYDRES_PROVOCATION_DOSSIER_V12'&&s.schema_id==='NOVYDRES_PROVOCATION_LONGITUDINAL_SIDECAR_V12','prep schemas');
insist(d.status==='SCENE_CAUSAL_ENTRY_READY_NO_EVENT'&&s.status==='READY_ONLY_AFTER_C45_PROMOTION','prep statuses');
insist(d.preparation_id===s.preparation_id&&d.preparation_id===c.plan.preparation_id,'prep identity');
insist(d.source_checkpoint.last_event_id===c.checkpoint.last_event_id&&s.source_checkpoint.last_event_id===c.checkpoint.last_event_id,'prep source');
insist(equal(d.source_checkpoint.state_refs,c44.refs)&&equal(s.source_checkpoint.state_refs,c44.refs),'six source refs');
insist(d.c02_causal_entry.admission_id==='PLOT-KUTHULUN-COERCION'&&c.causal_gate.admission_id===d.c02_causal_entry.admission_id,'D04 admission');
for(const key of ['historical_instruction_occurred','previously_sent_message','invitation_delivered','target_identity_verified','target_workplace_known','actual_scene_event','c01_replay','reporter_from_c01','pc_action_assumed','knowledge_delta'])insist(d.c02_causal_entry[key]===false,'invented '+key);
insist(d.c02_causal_entry.performer_can_fail_or_leave&&d.c02_causal_entry.authored_contact_attempt_only,'NPC agency');
insist(c.causal_gate.inquiry_only&&!c.causal_gate.historical_message_delivered&&!c.causal_gate.identity_known&&!c.causal_gate.c01_recycled&&!c.causal_gate.new_event_in_preparation,'causal gate');
insist(d.temporal_decision.mode==='CONTINUITY'&&s.temporal_policy.mode==='CONTINUITY'&&c.temporal_gate.mode==='CONTINUITY'&&!c.temporal_gate.significant_ellipsis&&!c.temporal_gate.new_time_committed,'continuity');
const ids=t.threads.map(x=>x.id),a=d.temporal_decision.threads,zz=s.temporal_policy.threads;
insist(ids.length===44&&new Set(ids).size===44&&c.temporal_gate.threads_open===44,'thread baseline');
for(const list of [a,zz])insist(list.length===44&&new Set(list.map(v=>v.id)).size===44&&list.every(v=>ids.includes(v.id)&&v.disposition==='CARRY_UNCHANGED'),'thread inventory');
insist(k.records.length===47&&k.last_event_id===c.checkpoint.last_event_id,'NPC ledger');
for(const gate of ['architecture_active','d07_active','story_preparation_ready','mechanical_scene_ready','scene_ready','narrator_permission'])insist(c.operational_gates[gate]&&d.operational_gates[gate]&&s.operational_gates[gate],'gate '+gate);
insist(c.guards.no_new_story_event&&c.guards.no_pc_decision&&c.guards.no_xp_fv_change&&c.guards.no_npc_knowledge_change&&c.guards.frozen_unchanged,'cycle guards');
insist(d.act_contracts[0].id==='A1'&&d.act_contracts[0].status==='OPEN_PENDING_ACT_RESOLUTION','A1 pending');
insist(d.mechanics.xp_total===675&&d.mechanics.xp_spent===270&&d.mechanics.xp_remaining===405&&d.mechanics.xp_credit===0,'XP');
insist(d.mechanics.willpower.max===6&&d.mechanics.willpower.superficial===2&&d.mechanics.willpower.aggravated===0&&d.mechanics.willpower.available===4,'FV');
insist(d.mechanics.mortality==='MORTAL'&&!d.mechanics.embrace_occurred,'no Embrace');
insist(m.status==='GITHUB_ACTIVE_PRIMARY_FULL_MIGRATION_PENDING'&&m.runtime.orchestration.current_cycle===C,'manifest cursor');
insist(m.runtime.orchestration.status==='READY_FOR_NARRATOR'&&m.runtime.orchestration.next_role==='NARRADOR'&&m.runtime.orchestration.next_scene_executable===true,'manifest role');
insist(m.runtime.orchestration.next_scene_status==='NOT_STARTED','manifest scene not played');
insist(m.runtime.orchestration.operational_gates.narrator_permission===true,'manifest permission');
insist(m.runtime.c02_causal_review?.scene_played===false&&m.runtime.c02_causal_review?.no_inferred_npc_transmission===true,'manifest not event');
return true;
}
export function validateLatestV23(root=process.cwd()){
const old=validateLatestV20(root);insist(old.ok&&old.threads===44&&old.predecessors===43,'C44 baseline regression');
const c=j(root,C),c44=j(root,P+'orchestration/CYCLE_V0044.json'),m=j(root,M),d=j(root,P+'preparations/M3.02_DOSSIER_V6.json'),s=j(root,P+'preparations/M3.02_LONGITUDINAL_SIDECAR_V6.json'),t=j(root,P+'knowledge/OPEN_THREADS_V24.json'),k=j(root,P+'knowledge/NPC_KNOWLEDGE_PROVENANCE_V22.json');
validateC45(c,m,d,s,c44,t,k);
verify(root,c.manifest_ref);verify(root,c.previous_cycle);verify(root,s.dossier_ref);verify(root,d.predecessor_ref);verify(root,s.predecessor_ref);
for(const r of Object.values(c.refs))verify(root,r);
for(const r of Object.values(c.architecture))if(r&&r.path)verify(root,r);
for(const r of Object.values(c.activation))if(r&&r.path)verify(root,r);
for(const r of Object.values(c.operational_gates.mechanical_sources))verify(root,r);
verify(root,c.operational_gates.mechanical_matrix_ref);
for(const r of Object.values(c.plan))if(r&&r.path)verify(root,r);
for(const r of Object.values(c.review))if(r&&r.path)verify(root,r);
let prev=c,links=0;for(let i=45;i>1;i--){verify(root,prev.previous_cycle);prev=j(root,prev.previous_cycle.path);insist(prev.sequence===i-1,'broken cycle link '+i);links++}
insist(links===44,'44 predecessors');
insist(m.supersedes==='novydres/MANIFEST_V62.json'&&m.previous_manifest_sha===hash(b(root,'novydres/MANIFEST_V62.json')),'manifest lineage');
for(const key of ['contract','entrypoint','cycle_schema','validator','tests','schema_tests']){const keyMap={contract:'orchestration_contract',entrypoint:'start_here',cycle_schema:'cycle_schema',validator:'cycle_validator',tests:'cycle_tests',schema_tests:'cycle_schema_tests'};const v=c.architecture[keyMap[key]];insist(m.runtime.orchestration[key]===v.path&&m.runtime.orchestration[key+'_blob_sha']===v.blob_sha,'manifest operational pin '+key)}
insist(m.runtime.current_m3_02_preparation.dossier.blob_sha===hash(b(root,c.plan.dossier.path))&&m.runtime.current_m3_02_preparation.sidecar.blob_sha===hash(b(root,c.plan.sidecar.path)),'prep manifest pins');
const git=(...args)=>execFileSync('git',['-C',root,...args],{encoding:'utf8'}).trim();
insist(git('rev-parse','HEAD:'+C)===hash(b(root,C)),'C45 Git HEAD blob');
insist(git('rev-parse','HEAD:'+M)===hash(b(root,M)),'V63 Git HEAD blob');
execFileSync('git',['-C',root,'merge-base','--is-ancestor',c.source_head_sha,'HEAD']);
return {ok:true,cycle:45,predecessors:44,c44_predecessors:43,threads:44,npc_records:47,g28_preserved:true,scene_started:false,ready_for_narrator:true,player_prompt_required:true};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname))console.log(JSON.stringify(validateLatestV23()));
