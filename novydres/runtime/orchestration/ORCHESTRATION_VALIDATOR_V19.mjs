import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const rootDefault=process.cwd();
const rel = (root,p)=>path.join(root,p);
const check=(ok,message)=>{if(!ok)throw Error('V19 FAIL: '+message)};
const content=(root,p)=>fs.readFileSync(rel(root,p));
const json=(root,p)=>JSON.parse(content(root,p).toString('utf8'));
const sha=(bytes)=>crypto.createHash('sha1').update(Buffer.from('blob '+bytes.length+'\0')).update(bytes).digest('hex');
function checkRef(root,x){check(x&&typeof x.path==='string'&&/^[a-f0-9]{40}$/.test(x.blob_sha),'invalid blob ref');const b=content(root,x.path);check(sha(b)===x.blob_sha,'bad pin '+x.path);return b}
function scanRefs(root,o){let count=0;function walk(v){if(!v||typeof v!=='object')return;if(typeof v.path==='string'&&typeof v.blob_sha==='string'){checkRef(root,v);count++}for(const z of Object.values(v))walk(z)}walk(o);return count}
const C='novydres/chronicles/CHR-001/orchestration/CYCLE_V0044.json';
const M='novydres/MANIFEST_V61.json';
const DP='novydres/chronicles/CHR-001/preparations/M3.02_DOSSIER_V4.json';
const SP='novydres/chronicles/CHR-001/preparations/M3.02_LONGITUDINAL_SIDECAR_V4.json';
const event='CHR001-M302-C01-05-20261111-001';
export function validatePackage(d,s){
check(d.schema_id==='NOVYDRES_PROVOCATION_DOSSIER_V10'&&s.schema_id==='NOVYDRES_PROVOCATION_LONGITUDINAL_SIDECAR_V10','schema IDs');
check(d.status==='PROSPECTIVE_REVIEW_ONLY_C02_NOT_READY'&&s.status==='REVIEW_REQUIRED_NO_NARRATOR_HANDOFF','candidate only');
check(d.source_checkpoint.last_event_id===event&&s.source_checkpoint.last_event_id===event,'event');
check(d.source_checkpoint.last_closed_scene==='M3.02.C01'&&d.source_checkpoint.next_scene==='M3.02.C02'&&d.source_checkpoint.next_scene_status==='NOT_STARTED','checkpoint');
check(s.scene_queue.closed==='M3.02.C01'&&s.scene_queue.next==='M3.02.C02'&&s.scene_queue.next_status==='NOT_STARTED','scene queue');
check(!s.scene_queue.scene_ready&&!s.scene_queue.narrator_permission,'queue unauthorized');
check(!d.c02_causal_entry.independent_eligible_cause_confirmed&&!d.c02_causal_entry.actor_knowledge_verified,'no new cause or knowledge');
check(d.c02_causal_entry.source_state==='CONDITIONAL_NOT_REALIZED'&&d.c02_causal_entry.c01_replay_forbidden===true,'no reused C01');
check(!d.c02_causal_entry.scene_ready&&!d.c02_causal_entry.narrator_permission,'cause cannot handoff');
check(d.act_contracts[0].id==='A1'&&d.act_contracts[0].status==='OPEN_PENDING_ACT_RESOLUTION','A1 act must remain open');
check(d.act_contracts.slice(1).every(x=>x.status==='CONDITIONAL_NOT_REALIZED'),'future acts conditional');
check(d.temporal_decision.mode==='REVIEW_REQUIRED'&&!d.temporal_decision.ellipsis_mandatory&&!d.temporal_decision.elapsed_time_assumed&&!d.temporal_decision.world_progress_materialized&&!d.temporal_decision.gate_ready,'temporal not fabricated');
check(s.temporal_policy.post_c01_elapsed_time==='NOT_ADVANCED'&&s.temporal_policy.mode==='REVIEW_REQUIRED'&&!s.temporal_policy.temporal_gate_ready,'temporal sidecar');
check(s.operational_gates.story_preparation_ready===false&&s.operational_gates.mechanical_scene_ready===false&&s.operational_gates.scene_ready===false&&s.operational_gates.narrator_permission===false,'operational gates');
for(const k of ['no_new_event','no_pc_decision','no_knowledge_delta','no_xp_fv_delta','no_frozen_edit','meta_comment_not_diegetic'])check(d.guards[k]===true,'dossier guard '+k);
check(d.guards.narrator_handoff_ready===false,'handoff forbidden');
check(s.immersion.meta_not_event&&s.immersion.no_double_action&&s.immersion.no_redundant_closure,'immersion');
check(d.mechanics.xp_total===675&&d.mechanics.xp_spent===270&&d.mechanics.xp_remaining===405&&d.mechanics.xp_credit===0,'XP unchanged');
check(d.mechanics.willpower.max===6&&d.mechanics.willpower.superficial===2&&d.mechanics.willpower.aggravated===0&&d.mechanics.willpower.available===4,'FV unchanged');
check(d.mechanics.mortality==='MORTAL'&&d.mechanics.embrace_occurred===false,'mortal and not embraced');
check(s.protected_state.threads_open===44&&s.protected_state.xp_unchanged&&s.protected_state.willpower_unchanged&&s.protected_state.npc_knowledge_unchanged,'protected sidecar');
check(JSON.stringify(d.source_checkpoint)===JSON.stringify(s.source_checkpoint),'dossier/sidecar source identical');
check(JSON.stringify(d.source_checkpoint.state_refs)===JSON.stringify(s.protected_state.state_refs),'six refs preserved');
return true
}
export function validateLatestV19(root=rootDefault){
const c=json(root,C);
check(c.sequence===44&&c.checkpoint.last_event_id===event&&c.checkpoint.next_scene_status==='NOT_STARTED','C44 checkpoint');
check(c.status==='READY_FOR_DRAMATURGO'&&c.transition==='SCENE_COMMITTED','C44 role');
check(c.operational_gates.narrator_permission===false,'C44 cannot narrate');
const c44Pins=scanRefs(root,c);
let prev=c, links=0;
for(let i=44;i>1;i--){const r=prev.previous_cycle;checkRef(root,r);prev=JSON.parse(content(root,r.path).toString('utf8'));check(prev.sequence===i-1,'predecessor sequence '+i);links++}
check(links===43,'43 predecessors');
const refs=c.refs;check(Object.keys(refs).length===6,'six sources');
for(const k of ['episode','character','live','history_index','knowledge','threads']){checkRef(root,refs[k]);check(content(root,refs[k].path).toString('utf8').includes(event),'G28 event absent '+k)}
const t=json(root,refs.threads.path),kn=json(root,refs.knowledge.path),live=json(root,refs.live.path),history=json(root,refs.history_index.path);
check(t.threads.length===44,'44 threads');check(t.last_event_id===event&&kn.last_event_id===event&&live.last_confirmed_event_id===event&&history.last_event_id===event,'last event reconciliation');
const d=json(root,DP),s=json(root,SP);
validatePackage(d,s);
check(scanRefs(root,d)>=14&&scanRefs(root,s)>=11,'candidate source refs');
check(sha(content(root,DP))===s.dossier_ref.blob_sha&&s.dossier_ref.path===DP,'sidecar dossier exact pin');
check(d.source_checkpoint.cycle.blob_sha===c.previous_cycle.blob_sha||d.source_checkpoint.cycle.blob_sha==='5bc4f59519fb7e7e3f017eea975a154e84e7efc1','C44 pin');
check(d.source_checkpoint.manifest.blob_sha==='6c1458fa2b72924d60e06f893f5211b695733443','M59 pin');
const m=json(root,M);
check(m.status==='PROSPECTIVE_CANDIDATE_NOT_ACTIVE_PENDING_VALIDATION','candidate manifest not active');
check(m.runtime.orchestration.current_cycle===C,'C44 remains current');
check(m.runtime.orchestration.operational_gates.narrator_permission===false,'manifest no narrator');
for(const x of Object.values(m.runtime.current_m3_02_candidate_preparation))checkRef(root,x);
for(const x of Object.values(m.runtime.orchestration.post_g28_candidate_refs))checkRef(root,x);
check(m.runtime.current_m3_02_candidate_preparation.dossier.blob_sha===sha(content(root,DP)),'dossier pin');
check(m.runtime.current_m3_02_candidate_preparation.sidecar.blob_sha===sha(content(root,SP)),'sidecar pin');
return {ok:true,predecessors:links,c44_pins:c44Pins,g28_sources:6,threads:44,knowledge_records:kn.records.length,c02:'NOT_STARTED',narrator_permission:false}
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){const r=validateLatestV19(process.cwd());process.stdout.write(JSON.stringify(r)+'\n')}
