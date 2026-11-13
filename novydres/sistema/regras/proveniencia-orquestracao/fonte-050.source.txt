import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
const P='novydres/chronicles/CHR-001/';const D=P+'preparations/M3.02_DOSSIER_V5.json',S=P+'preparations/M3.02_LONGITUDINAL_SIDECAR_V5.json',C=P+'orchestration/CYCLE_V0044.json';
const fail=m=>{throw Error('CHR001_C02_PREFLIGHT_V21_BLOCK:'+m)};const ck=(x,m)=>{if(!x)fail(m)};const rd=(root,p)=>fs.readFileSync(path.join(root,p));const j=(root,p)=>JSON.parse(rd(root,p));const sha=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const pin=(root,x)=>{ck(x&&x.path&&/^[0-9a-f]{40}$/.test(x.blob_sha),'bad ref');ck(sha(rd(root,x.path))===x.blob_sha,'blob '+x.path)};
export function checkCausal(d,s,t,k,c){
ck(d.schema_id==='NOVYDRES_PROVOCATION_DOSSIER_V11'&&s.schema_id==='NOVYDRES_PROVOCATION_LONGITUDINAL_SIDECAR_V11','schemas');
ck(d.status==='PROSPECTIVE_CAUSAL_ENTRY_PREPARED_NOT_ACTIVE'&&s.status==='CAUSAL_PREFLIGHT_EDITORIAL_ONLY','not active');
ck(d.source_checkpoint.last_event_id===c.checkpoint.last_event_id&&s.source_checkpoint.last_event_id===c.checkpoint.last_event_id,'event source');
ck(d.source_checkpoint.next_scene_status==='NOT_STARTED'&&s.scene_queue.next_status==='NOT_STARTED','next scene');
ck(d.c02_causal_entry.admission_id==='PLOT-KUTHULUN-COERCION','D04 cause');
for(const x of ['historical_instruction_occurred','previously_sent_message','invitation_delivered','target_identity_verified','target_workplace_known','npc_believes_target_identified','actual_scene_event','c01_replay','reporter_from_c01','pc_action_assumed','knowledge_delta'])ck(d.c02_causal_entry[x]===false,'no invented '+x);
ck(d.c02_causal_entry.performer_can_fail_or_leave===true&&d.c02_causal_entry.physical_route.startsWith('PUBLIC_FRONTAGE'),'NPC agency and route');
ck(d.temporal_decision.mode==='CONTINUITY'&&!d.temporal_decision.significant_ellipsis&&!d.temporal_decision.world_changes&&!d.temporal_decision.pc_choices&&!d.temporal_decision.prelude_tests,'no temporal fiction');
ck(s.temporal_policy.mode==='CONTINUITY'&&!s.temporal_policy.significant_ellipsis,'sidecar continuity');
const ids=t.threads.map(x=>x.id),a=d.temporal_decision.threads,b=s.temporal_policy.threads;
ck(new Set(ids).size===44&&a.length===44&&b.length===44,'44 unique threads');
for(const x of [a,b])ck(new Set(x.map(y=>y.id)).size===44&&x.every(y=>ids.includes(y.id)&&y.disposition==='CARRY_UNCHANGED'),'44 exact dispositions');
ck(k.records.length===47&&k.last_event_id===c.checkpoint.last_event_id,'47 NPC provenance');
ck(s.protected_state.threads_open===44&&s.protected_state.npc_knowledge_unchanged,'protected ledger');
ck(s.scene_queue.scene_ready===false&&s.scene_queue.narrator_permission===false,'no early handoff');
ck(d.guards.no_new_event&&d.guards.no_pc_decision&&d.guards.no_knowledge_delta&&d.guards.no_xp_fv_delta&&!d.guards.narrator_handoff_ready,'guards');
ck(d.act_contracts[0].id==='A1'&&d.act_contracts[0].status==='OPEN_PENDING_ACT_RESOLUTION','A1 open');
ck(d.mechanics.xp_total===675&&d.mechanics.xp_spent===270&&d.mechanics.xp_remaining===405&&d.mechanics.xp_credit===0,'XP');
ck(d.mechanics.willpower.max===6&&d.mechanics.willpower.superficial===2&&d.mechanics.willpower.aggravated===0&&d.mechanics.willpower.available===4,'FV');
ck(d.mechanics.mortality==='MORTAL'&&d.mechanics.embrace_occurred===false,'mortal');
return true;
}
export function preflight(root=process.cwd()){
const c=j(root,C),d=j(root,D),s=j(root,S),t=j(root,P+'knowledge/OPEN_THREADS_V24.json'),k=j(root,P+'knowledge/NPC_KNOWLEDGE_PROVENANCE_V22.json');
ck(c.sequence===44&&c.status==='READY_FOR_DRAMATURGO'&&!c.operational_gates.narrator_permission,'C44 source');
ck(!fs.existsSync(path.join(root,P+'orchestration/CYCLE_V0045.json')),'C45 premature');
checkCausal(d,s,t,k,c);
let n=0,prev=c;for(let i=44;i>1;i--){pin(root,prev.previous_cycle);prev=j(root,prev.previous_cycle.path);ck(prev.sequence===i-1,'predecessor '+i);n++}ck(n===43,'43 links');
const source=Object.values(c.refs);ck(source.length===6,'six state refs');for(const x of source)pin(root,x);
for(const [key,r]of Object.entries(d.authority_refs)){pin(root,r)}
pin(root,d.predecessor_ref);pin(root,s.predecessor_ref);pin(root,s.dossier_ref);pin(root,d.source_checkpoint.cycle);pin(root,d.source_checkpoint.manifest);
ck(sha(rd(root,D))===s.dossier_ref.blob_sha,'dossier hash');
ck(JSON.stringify(d.source_checkpoint.state_refs)===JSON.stringify(s.source_checkpoint.state_refs),'state refs');
return {ok:true,status:'CAUSAL_PREPARED_ONLY',predecessors:43,threads:44,npc_records:47,scene:'NOT_STARTED',narrator_permission:false};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname))console.log(JSON.stringify(preflight()));
