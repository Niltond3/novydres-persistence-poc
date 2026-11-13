#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';

const fail=m=>{throw new Error('CHR001_V14_BLOCK: '+m)};
const ok=(v,m)=>{if(!v)fail(m)};
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const hash=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const read=(root,p)=>{
 ok(typeof p==='string'&&p.length&&!path.isAbsolute(p)&&!p.split(/[\\/]/).includes('..'),'unsafe path '+p);
 const f=path.resolve(root,p);
 ok(f.startsWith(path.resolve(root)+path.sep),'path escape '+p);
 return fs.readFileSync(f);
};
const j=(root,p)=>JSON.parse(read(root,p).toString('utf8'));
const pin=(root,x,what)=>{
 ok(x?.path&&/^[a-f0-9]{40}$/.test(x.blob_sha),what+' malformed pin');
 ok(hash(read(root,x.path))===x.blob_sha,what+' SHA mismatch '+x.path);
};
const cycle=n=>'novydres/chronicles/CHR-001/orchestration/CYCLE_V'+String(n).padStart(4,'0')+'.json';
const keys=['live','history_index','episode','character','knowledge','threads'];
const mechanics=['rules_provenance','target_sheet','adjudication_gate','motor_manual','xp_policy','xp_audit','act_resolution_schema','xp_envelope','settlement_record'];
const allowedChanged=['d06','d07','d08','d09','start_here','orchestration_contract','cycle_schema','cycle_validator','cycle_tests','preparation_dossier_schema','preparation_sidecar_schema','cycle_schema_tests','causal_entry_review'];
const extra=['player_spotlight_direction'];

export function assessSpotlightFrame(x){
 ok(x&&typeof x==='object','scene frame required');
 if(x.important_pending_player_choice===true)return 'PENDING_PLAYER_CHOICE';
 if(x.last_checkpoint_reconciled!==true||x.admitted_plot!==true||x.prepared_actor_agency!==true||x.spatial_reach!==true||x.meaningful_stakes!==true||x.real_choices!==true)return 'BLOCKED_INSUFFICIENT_PREPARATION';
 if(x.routine_ellipsis_allowed!==true||x.offscreen_consequential_pc_action===true||x.unearned_npc_knowledge===true||x.precommitted_event===true||x.fictitious_xp_fv===true||x.fictitious_prior_time_record===true)return 'BLOCKED_AGENCY_OR_CHRONOLOGY';
 if(x.incident_already_realized===true)return 'BLOCKED_FUTURE_AS_FACT';
 return 'ELIGIBLE_FOR_SEPARATE_NARRATOR_GRANT';
}
export function validateSceneFrameGrant(c,prev){
 ok(c?.sequence===40&&c.cycle_id==='CHR001-CYCLE-0040'&&c.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V14','C40 identity');
 ok(c.provocation_id==='M3.02'&&c.transition==='SCENE_FRAME_GRANTED'&&c.status==='READY_FOR_NARRATOR'&&c.next_role==='NARRADOR','C40 grant or role');
 ok(prev?.sequence===39&&prev.status==='INTENTION_PENDING'&&prev.transition==='CAUSAL_ENTRY_INTENTION_REQUESTED'&&prev.next_role==='PLAYER_INTENTION','C39 origin');
 ok(c.previous_cycle.path===cycle(39),'predecessor path');
 ok(c.source_head_sha==='d6f6904c3cb3f8b02b707bef41b36abe4a7c0950','source master mismatch');
 ok(eq(c.checkpoint,prev.checkpoint),'played checkpoint changed');
 ok(c.checkpoint.last_event_id==='CHR001-M301-C05-22-20261109-001'&&c.checkpoint.last_closed_scene==='C05'&&c.checkpoint.next_scene==='C01'&&c.checkpoint.next_scene_status==='NOT_STARTED'&&c.checkpoint.mortal===true&&!c.checkpoint.embrace_occurred,'invented event/Embrace');
 for(const k of keys)ok(eq(c.refs?.[k],prev.refs?.[k]),'state changed '+k);
 for(const k of mechanics)ok(eq(c.operational_gates?.mechanical_sources?.[k],prev.operational_gates?.mechanical_sources?.[k]),'mechanical source changed '+k);
 ok(eq(c.operational_gates?.mechanical_matrix_ref,prev.operational_gates?.mechanical_matrix_ref),'mechanical matrix changed');
 for(const k of ['architecture_active','d07_active','story_preparation_ready','mechanical_scene_ready','scene_ready','narrator_permission'])
  ok(c.operational_gates?.[k]===true,'missing/false scene gate '+k);
 ok(c.pending_player_decision===null,'unjustified pending intention');
 ok(!('causal_handoff' in c)&&!('administrative_opening' in c)&&!('episode_closure' in c),'replayed historical workflow');
 ok(c.plan?.preparation_id==='CHR001-PREP-M302-20261111-V2'&&c.plan.validity==='REVISED'&&c.plan.reviewed_against_event_id===prev.checkpoint.last_event_id,'plan source/identity');
 ok(c.review?.decision==='SCENE_FRAME_AUTHORIZED'&&c.review.against_last_event_id===prev.checkpoint.last_event_id,'review not authorized');
 ok(c.blocking?.code===null&&c.blocking?.reason===null,'unexpected blocking');
 ok(eq(c.guards,prev.guards),'historical guards changed');
 ok(eq(c.activation,prev.activation),'truth activation modified');
 for(const [k,x] of Object.entries(prev.architecture))if(!allowedChanged.includes(k))ok(eq(c.architecture[k],x),'old authority changed '+k);
 ok(Object.keys(c.architecture).length===Object.keys(prev.architecture).length+extra.length,'unexpected architecture width');
 ok(c.architecture.player_spotlight_direction?.path?.includes('SIGNIFICANT_SCENE_SPOTLIGHT_V001_PLAYER_SAFE.json'),'missing user decision');
 const sf=c.scene_frame;
 ok(sf?.path==='A_DRAMATIC_SPOTLIGHT'&&sf.mode==='PROSPECTIVE_TEMPORAL_ELLIPSIS'&&sf.time_window==='LATER_WORKSHOP_EVENING_1970_CIVIL_DATE_UNKNOWN','spotlight path/time');
 ok(eq(sf.source_intention_cycle_ref,c.previous_cycle)&&sf.source_manifest_ref.path===prev.manifest_path,'source pins');
 ok(eq(sf.entry_review_ref,c.architecture.causal_entry_review)&&eq(sf.spotlight_decision_ref,c.architecture.player_spotlight_direction),'authority pins');
 for(const k of ['is_prospective_only','last_checkpoint_unchanged','independent_world_cause_prepared','meaningful_choice_available','routine_ellipsis_allowed','narrator_may_frame_only_after_player_prompt','no_forced_incident_outcome','previous_intention_not_received'])
  ok(sf[k]===true,'missing prospective guarantee '+k);
 for(const k of ['future_incident_realized','elapsed_time_persisted','pc_travel_assumed','consequential_pc_action_assumed','npc_contact_already_recorded','npc_knowledge_changed','open_threads_changed','xp_fv_changed','mortal_status_changed','scene_started'])
  ok(sf[k]===false,'fictional prior event or assumed PC agency '+k);
 return {ok:true,cycle:c.cycle_id,status:c.status,scene_ready:true,narrator_permission:true,last_event_unchanged:true,scene_started:false};
}
export function validateLatestV14(root){
 const dir=path.resolve(root,'novydres/chronicles/CHR-001/orchestration');
 const ns=fs.readdirSync(dir).map(n=>/^CYCLE_V(\d{4})\.json$/.exec(n)).filter(Boolean).map(x=>+x[1]);
 ok(Math.max(...ns)===40,'latest cycle is not C40');
 const c=j(root,cycle(40)),prev=j(root,cycle(39));
 validateSceneFrameGrant(c,prev);
 let links=0;
 for(let n=40;n>=2;n--){
  const obj=j(root,cycle(n));ok(obj.previous_cycle?.path===cycle(n-1),'predecessor path C'+n);
  pin(root,obj.previous_cycle,'predecessor C'+n);links++;
 }
 pin(root,c.manifest_ref,'current manifest');
 for(const [k,x] of Object.entries(c.refs))pin(root,x,'state '+k);
 for(const [k,x] of Object.entries(c.architecture))pin(root,x,'architecture '+k);
 for(const [k,x] of Object.entries(c.activation))pin(root,x,'activation '+k);
 for(const [k,x] of Object.entries(c.operational_gates.mechanical_sources))pin(root,x,'mechanics '+k);
 pin(root,c.operational_gates.mechanical_matrix_ref,'mechanical matrix');
 pin(root,c.plan.dossier,'dossier');pin(root,c.plan.sidecar,'sidecar');
 pin(root,c.scene_frame.source_manifest_ref,'source manifest');
 pin(root,c.scene_frame.spotlight_decision_ref,'player directive');
 pin(root,c.scene_frame.entry_review_ref,'scene review');
 const m=j(root,c.manifest_path),o=m.runtime?.orchestration,na=m.runtime?.narrative_architecture;
 ok(c.manifest_path===c.manifest_ref.path&&m.branch==='master','manifest identity');
 ok(o?.current_cycle===cycle(40)&&o.status===c.status&&o.next_role===c.next_role,'manifest cycle pointer');
 ok(o.next_scene==='C01'&&o.next_scene_status==='NOT_STARTED'&&o.next_scene_executable===true,'manifest scene pointer');
 ok(m.runtime.last_confirmed_narrative_event===c.checkpoint.last_event_id&&m.runtime.marco_M3_status==='M3.02_C01_READY_FOR_NARRATOR_NOT_STARTED','manifest story checkpoint');
 for(const k of ['architecture_active','d07_active','story_preparation_ready','mechanical_scene_ready','scene_ready','narrator_permission'])
  ok(o.operational_gates?.[k]===c.operational_gates[k],'manifest gate '+k);
 for(const [k,x] of Object.entries(c.architecture)){
  ok(eq(na?.blob_refs?.[k],x),'manifest pin '+k);
  if(typeof na?.[k]==='string')ok(na[k]===x.path,'manifest path '+k);
 }
 const ckeys=[['contract','orchestration_contract'],['entrypoint','start_here'],['cycle_schema','cycle_schema'],['validator','cycle_validator'],['tests','cycle_tests'],['schema_tests','cycle_schema_tests']];
 for(const [k,v] of ckeys)
  ok(o[k]===c.architecture[v].path&&o[k+'_blob_sha']===c.architecture[v].blob_sha,'orchestration pointer '+k);
 ok(eq(m.runtime.current_m3_02_preparation?.dossier,c.plan.dossier)&&eq(m.runtime.current_m3_02_preparation?.sidecar,c.plan.sidecar),'preparation pointers');
 ok(m.runtime.current_m3_02_preparation?.first_cause_realized===false&&m.runtime.current_m3_02_preparation?.scene_started===false,'manifest incident precommitted');
 const ds=j(root,c.plan.dossier.path),sc=j(root,c.plan.sidecar.path),er=j(root,c.scene_frame.entry_review_ref.path),decision=j(root,c.scene_frame.spotlight_decision_ref.path);
 ok(ds.preparation_id===c.plan.preparation_id&&sc.preparation_id===c.plan.preparation_id&&eq(sc.dossier_ref,c.plan.dossier),'dossier/sidecar mismatch');
 ok(eq(ds.source_checkpoint.cycle,c.previous_cycle)&&eq(sc.source_checkpoint.cycle,c.previous_cycle),'preparation source cycle');
 ok(eq(ds.source_checkpoint.manifest,c.scene_frame.source_manifest_ref)&&eq(sc.source_checkpoint.manifest,c.scene_frame.source_manifest_ref),'preparation manifest');
 for(const k of keys)ok(eq(ds.source_checkpoint.state_refs[k],c.refs[k])&&eq(sc.source_checkpoint.state_refs[k],c.refs[k]),'carried state '+k);
 ok(ds.first_incident?.status==='PLANNED_CONDITIONAL_NOT_OCCURRED'&&ds.first_incident.actual_cause_present===false,'fictional realized incident');
 ok(ds.first_incident.scene_ready===true&&ds.first_scene_review.scene_ready===true&&ds.first_scene_review.narrator_permission===true,'dossier not ready');
 ok(ds.causal_guards.no_elapsed_time===true&&ds.causal_guards.no_pc_action===true&&ds.causal_guards.no_new_event===true,'dossier fabricated action');
 ok(ds.temporal_framing?.mode==='PROSPECTIVE_ELLIPSIS_SPOTLIGHT'&&ds.temporal_framing.event_state?.includes('UNPLAYED'),'invalid scene framing');
 ok(sc.scene_queue?.status==='NOT_STARTED'&&sc.scene_queue.entry_realized===false&&sc.scene_queue.scene_ready===true&&sc.scene_queue.narrator_permission===true,'sidecar false framing');
 ok(sc.causal_entry?.event_realized===false&&sc.causal_entry?.player_must_unload===false&&sc.causal_entry?.routine_ellipsis_allowed===true,'sidecar forced plot');
 ok(er.decision==='PATH_A_SCENE_FRAME_READY_CANDIDATE'&&er.realized_incident===false&&eq(er.source_cycle,c.previous_cycle),'review false cause');
 ok(decision.document_id==='PLAYER_DECISION_CHR001_SIGNIFICANT_SCENE_SPOTLIGHT_V001_PLAYER_SAFE','missing player direction');
 ok(ds.mechanics.xp_total===675&&ds.mechanics.xp_spent===270&&ds.mechanics.xp_credit_available===0&&ds.mechanics.willpower.available===4,'resource mismatch');
 const d04=j(root,c.architecture.d04_plot_admissions.path);
 ok(d04.admissions?.some(x=>x.plot_id===ds.first_incident.plot_admission&&x.decision==='ADMITTED_FOR_PROSPECTIVE_AUTHORIAL_PREPARATION'),'not admitted by D04');
 const d09=j(root,c.architecture.d09.path);
 ok(d09.operational_gate?.scene_ready===true&&d09.operational_gate?.narrator_permission===true&&d09.target_route?.status==='PENDING_UNCHANGED','D09 incorrect');
 const git=a=>execFileSync('git',['-C',root,...a],{encoding:'utf8'}).trim();
 ok(git(['rev-parse','HEAD^'])===c.source_head_sha,'candidate commit must descend directly from expected master');
 ok(git(['rev-parse','HEAD:'+cycle(40)])===hash(read(root,cycle(40))),'cycle tree mismatch');
 ok(git(['rev-parse','HEAD:'+c.manifest_path])===c.manifest_ref.blob_sha,'manifest tree mismatch');
 return {ok:true,cycle:c.cycle_id,status:c.status,predecessor_links:links,source_refs:Object.keys(c.architecture).length,carried_state_refs:6,mechanical_source_refs:mechanics.length,scenes_played:0,scene_ready:true,narrator_permission:true,release_on_explicit_narrator_prompt:true};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){
 try{const i=process.argv.indexOf('--root');console.log(JSON.stringify(validateLatestV14(path.resolve(i<0?process.cwd():process.argv[i+1]))));}
 catch(e){console.error(String(e));process.exitCode=1;}
}
