#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
const fail=m=>{throw Error('CHR001_V13_BLOCK: '+m)};
const ok=(v,m)=>{if(!v)fail(m)};
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const hash=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\\0'.replace('\\0','\0'))).update(b).digest('hex');
const read=(root,p)=>{ok(typeof p==='string'&&p.length>0&&!path.isAbsolute(p)&&!p.split(/[\\/]/).includes('..'),'unsafe path '+p);const f=path.resolve(root,p);ok(f.startsWith(path.resolve(root)+path.sep),'path escape '+p);return fs.readFileSync(f)};
const json=(root,p)=>JSON.parse(read(root,p).toString('utf8'));
const pin=(root,x,what)=>{ok(x?.path&&/^[a-f0-9]{40}$/.test(x.blob_sha),what+' malformed pin');ok(hash(read(root,x.path))===x.blob_sha,what+' SHA mismatch '+x.path)};
const cycle=n=>'novydres/chronicles/CHR-001/orchestration/CYCLE_V'+String(n).padStart(4,'0')+'.json';
const six=['live','history_index','episode','character','knowledge','threads'];
const mechanics=['rules_provenance','target_sheet','adjudication_gate','motor_manual','xp_policy','xp_audit','act_resolution_schema','xp_envelope','settlement_record'];
const replacements=['start_here','orchestration_contract','cycle_schema','cycle_validator','cycle_tests','cycle_schema_tests'];
export function assessSceneEntry(a){
  ok(a && typeof a==='object','entry assessment missing');
  const prepared=a.prepared_cause===true&&a.authorial_admission===true&&a.actor_capacity_backed===true&&a.real_choices===true;
  const entry=(a.immediate_world_condition===true||a.independent_npc_initiative_backed===true)&&a.spatio_temporal_reach_backed===true;
  const noCompulsion=a.mandatory_pc_action!==true&&a.fictitious_travel!==true&&a.fictitious_time!==true&&a.unearned_npc_knowledge!==true;
  // The future incident is deliberately not an entry prerequisite.
  return prepared&&entry&&noCompulsion?'SCENE_ENTRY_ELIGIBLE_SEPARATE_GRANT':'INTENTION_PENDING';
}
export function validateCausalTransition(c,prev){
  ok(c?.sequence===39&&c.cycle_id==='CHR001-CYCLE-0039'&&c.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V13','C39 identity');
  ok(c.provocation_id==='M3.02'&&c.transition==='CAUSAL_ENTRY_INTENTION_REQUESTED'&&c.status==='INTENTION_PENDING'&&c.next_role==='PLAYER_INTENTION','wrong transition or role');
  ok(prev?.sequence===38&&prev?.status==='READY_FOR_DRAMATURGO'&&prev?.transition==='NEXT_PROVOCATION_ADMIN_OPENED','C38 provenance');
  ok(c.previous_cycle.path===cycle(38),'predecessor path');
  ok(c.source_head_sha==='44b5c2348ccd3bb2ea5edaaa918f2f55b197321b','wrong source head');
  ok(eq(c.checkpoint,prev.checkpoint)&&c.checkpoint.last_event_id==='CHR001-M301-C05-22-20261109-001'&&c.checkpoint.next_scene_status==='NOT_STARTED'&&c.checkpoint.mortal===true&&c.checkpoint.embrace_occurred===false,'event/checkpoint changed');
  for(const k of six)ok(eq(c.refs?.[k],prev.refs?.[k]),'changed state '+k);
  for(const k of mechanics)ok(eq(c.operational_gates?.mechanical_sources?.[k],prev.operational_gates?.mechanical_sources?.[k]),'changed mechanics '+k);
  ok(eq(c.operational_gates?.mechanical_matrix_ref,prev.operational_gates?.mechanical_matrix_ref),'changed mechanics matrix');
  ok(c.operational_gates?.architecture_active===true&&c.operational_gates?.d07_active===true,'architecture deactivated');
  for(const k of ['story_preparation_ready','mechanical_scene_ready','scene_ready','narrator_permission'])ok(c.operational_gates?.[k]===false,'premature gate '+k);
  ok(c.pending_player_decision==='NEXT_INTENTION_FROM_C05_22','missing player intention step');
  ok(!('administrative_opening' in c)&&!('episode_closure' in c),'replayed old transition');
  ok(eq(c.plan,prev.plan)&&c.plan.validity==='REVISED'&&c.plan.reviewed_against_event_id===c.checkpoint.last_event_id,'plan changed/fabricated');
  ok(c.review?.decision==='INTENTION_REQUIRED'&&c.review.against_last_event_id===c.checkpoint.last_event_id,'review mismatch');
  ok(c.blocking?.code===null&&c.blocking.reason===null,'spurious governance blocker');
  ok(c.guards?.no_story_delta_in_prep===true&&c.guards?.no_xp_fv_delta_in_prep===true&&c.guards?.frozen_unchanged===true&&c.guards?.no_public_spoilers===true,'lost guard');
  ok(eq(c.activation,prev.activation),'activation changed');
  for(const [k,p] of Object.entries(prev.architecture))if(!replacements.includes(k))ok(eq(c.architecture[k],p),'replaced old authority '+k);
  ok(c.architecture.causal_entry_review?.path==='novydres/chronicles/CHR-001/preparations/M3.02_ENTRY_REVIEW_V1_PLAYER_SAFE.json','review path');
  ok(Object.keys(c.architecture).length===Object.keys(prev.architecture).length+1,'unexpected architecture');
  const h=c.causal_handoff;
  ok(h?.path==='B_INTENTION_FIRST'&&eq(h.source_admin_cycle_ref,c.previous_cycle)&&h.source_manifest_ref.path===prev.manifest_path&&eq(h.entry_review_ref,c.architecture.causal_entry_review),'handoff source pins');
  ok(h.prepared_cause_available===true&&h.entry_condition_available===false&&h.future_incident_realized===false,'false causal entry');
  for(const k of ['intention_received','intention_executed','pc_action_assumed','elapsed_time_or_travel','npc_presence_assumed','npc_knowledge_changed','story_state_changed','mechanics_changed','open_threads_changed','scene_started','narrator_granted'])ok(h[k]===false,'fabricated causal state '+k);
  ok(h.future_reassessment_required===true&&h.question?.includes('o que ele pretende fazer em seguida?'),'invalid intention step');
  return {ok:true,cycle_id:c.cycle_id,path:'B',status:c.status,scene_ready:false,narrator_permission:false};
}
export function validateLatestV13(root){
  const dir=path.resolve(root,'novydres/chronicles/CHR-001/orchestration');
  const ns=fs.readdirSync(dir).map(x=>/^CYCLE_V(\d{4})\.json$/.exec(x)).filter(Boolean).map(x=>+x[1]);
  ok(Math.max(...ns)===39,'highest cycle not C39');
  const c=json(root,cycle(39)),prev=json(root,cycle(38));
  validateCausalTransition(c,prev);
  let chain=0;
  for(let n=39;n>=2;n--){const x=json(root,cycle(n));ok(x.previous_cycle?.path===cycle(n-1),'chain path C'+n);pin(root,x.previous_cycle,'predecessor C'+n);chain++}
  pin(root,c.manifest_ref,'manifest');
  for(const [k,x] of Object.entries(c.refs))pin(root,x,'state '+k);
  for(const [k,x] of Object.entries(c.architecture))pin(root,x,'architecture '+k);
  for(const [k,x] of Object.entries(c.activation))pin(root,x,'activation '+k);
  for(const [k,x] of Object.entries(c.operational_gates.mechanical_sources))pin(root,x,'mechanics '+k);
  pin(root,c.operational_gates.mechanical_matrix_ref,'mechanical matrix');
  pin(root,c.plan.dossier,'dossier');pin(root,c.plan.sidecar,'sidecar');
  pin(root,c.causal_handoff.source_manifest_ref,'M53');pin(root,c.causal_handoff.entry_review_ref,'entry review');
  const m=json(root,c.manifest_path),o=m.runtime?.orchestration,na=m.runtime?.narrative_architecture;
  ok(c.manifest_path===c.manifest_ref.path&&m.branch==='master','manifest identity');
  ok(o?.current_cycle===cycle(39)&&o.status===c.status&&o.next_role===c.next_role,'orchestration pointer');
  ok(o.next_scene==='C01'&&o.next_scene_status==='NOT_STARTED'&&o.next_scene_executable===false,'scene cursor');
  for(const k of ['architecture_active','d07_active','story_preparation_ready','mechanical_scene_ready','scene_ready','narrator_permission'])ok(o.operational_gates?.[k]===c.operational_gates[k],'manifest gate '+k);
  ok(m.runtime.last_confirmed_narrative_event===c.checkpoint.last_event_id&&m.runtime.marco_M3_status==='M3.02_INTENTION_PENDING_C01_NOT_STARTED','narrative state mismatch');
  for(const [k,x] of Object.entries(c.architecture)){
    ok(eq(na?.blob_refs?.[k],x),'manifest pin '+k);
    if(k in na && typeof na[k]==='string')ok(na[k]===x.path,'manifest path '+k);
  }
  for(const [key,blob] of [['contract','orchestration_contract'],['cycle_schema','cycle_schema'],['validator','cycle_validator'],['tests','cycle_tests'],['schema_tests','cycle_schema_tests'],['entrypoint','start_here']]){
    ok(o[key]===c.architecture[blob].path&&o[(key==='entrypoint'?'entrypoint':key)+'_blob_sha']===c.architecture[blob].blob_sha,'manifest orchestration pin '+key);
  }
  ok(m.runtime.current_m3_02_preparation?.dossier?.blob_sha===c.plan.dossier.blob_sha&&m.runtime.current_m3_02_preparation?.sidecar?.blob_sha===c.plan.sidecar.blob_sha,'dossier pins');
  ok(m.runtime.current_m3_02_preparation?.first_cause_realized===false,'fabricated future incident');
  const rev=json(root,c.causal_handoff.entry_review_ref.path),ds=json(root,c.plan.dossier.path),sc=json(root,c.plan.sidecar.path);
  ok(eq(rev.source_cycle,c.previous_cycle)&&rev.status==='INTENTION_FIRST_RECOMMENDED'&&rev.path_assessment?.B?.selected===true,'entry review wrong');
  ok(rev.guards?.scene_ready===false&&rev.guards?.narrator_permission===false,'review fictitious grant');
  ok(ds.first_incident?.status==='PLANNED_CONDITIONAL_NOT_OCCURRED'&&ds.first_incident.actual_cause_present===false&&ds.first_incident.scene_ready===false,'dossier incident fake');
  ok(ds.first_scene_review.scene_ready===false&&ds.first_scene_review.narrator_permission===false,'dossier false opening');
  ok(sc.scene_queue?.status==='NOT_STARTED'&&sc.scene_queue?.entry_realized===false&&sc.no_new_event===true,'sidecar false opening');
  ok(ds.mechanics.xp_total===675&&ds.mechanics.xp_spent===270&&ds.mechanics.xp_credit_available===0&&ds.mechanics.willpower.available===4,'mechanical mismatch');
  const git=args=>execFileSync('git',['-C',root,...args],{encoding:'utf8'}).trim();
  ok(git(['rev-parse','HEAD^'])===c.source_head_sha,'candidate first parent must be C38 commit');
  ok(git(['rev-parse','HEAD:'+cycle(39)])===hash(read(root,cycle(39))),'cycle tree readback');
  ok(git(['rev-parse','HEAD:'+c.manifest_path])===c.manifest_ref.blob_sha,'manifest tree readback');
  return {ok:true,cycle_id:c.cycle_id,predecessor_links:chain,authority_pins:Object.keys(c.architecture).length,scene_ready:false,narrator_permission:false,protagonist_action:false,remote_checkout:true};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){
try{const idx=process.argv.indexOf('--root');console.log(JSON.stringify(validateLatestV13(path.resolve(idx<0?process.cwd():process.argv[idx+1]))))}catch(e){console.error(String(e));process.exitCode=1}
}
