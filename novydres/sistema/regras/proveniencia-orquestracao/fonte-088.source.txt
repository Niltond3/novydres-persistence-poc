#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {validateSceneFrameGrant} from './ORCHESTRATION_VALIDATOR_V14.mjs';

const fail=m=>{throw new Error('CHR001_V15_BLOCK: '+m)};
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
const stateKeys=['live','history_index','episode','character','knowledge','threads'];
const mechanicalKeys=['rules_provenance','target_sheet','adjudication_gate','motor_manual','xp_policy','xp_audit','act_resolution_schema','xp_envelope','settlement_record'];
const changedArch=['start_here','orchestration_contract','cycle_schema','cycle_validator','cycle_tests','cycle_schema_tests'];
const addedArch=['role_dramaturgo','role_narrador','handoff_to_narrador','pacing_policy','ellipsis_prelude_protocol','player_living_ellipsis_decision','temporal_review'];

export function assessTemporalMode({mode='CONTINUITY',meaningful_continuity=false,erases_player_choice=false,world_cause_valid=true,required_distinct_tests=0,prelude_mechanics_valid=true,unearned_benefit=false,pretend_event_recorded=false}={}){
 if(!['CONTINUITY','ABSTRACTION','MONTAGE','ELLIPSIS'].includes(mode))return 'BLOCK_INVALID_MODE';
 if(!Number.isInteger(required_distinct_tests)||required_distinct_tests<0)return 'BLOCK_INVALID_TEST_COUNT';
 if(unearned_benefit||pretend_event_recorded)return 'BLOCK_FALSE_DELTA';
 if(mode==='CONTINUITY')return required_distinct_tests===0?'CONTINUE_DIRECTLY':'BLOCK_PRELUDE_NOT_APPLICABLE';
 if(mode==='ELLIPSIS'&&meaningful_continuity)return 'RETURN_TO_CONTINUITY';
 if(erases_player_choice&&mode==='ELLIPSIS')return 'PLAYER_DECISION_PRELUDE_OR_CONTINUITY';
 if(required_distinct_tests>2)return 'FULL_SCENE_REQUIRED';
 if(required_distinct_tests>0&&!prelude_mechanics_valid)return 'MECHANICAL_PREFLIGHT_REQUIRED';
 if(!world_cause_valid&&mode==='ELLIPSIS')return 'BLOCK_UNSUPPORTED_WORLD_ADVANCEMENT';
 return mode==='ELLIPSIS'?'ELLIPSIS_WITH_CAUSAL_WORLD_ADVANCEMENT':'ABSTRACT_OR_MONTAGE';
}
export function validateC41(c,prev){
 ok(c?.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V15'&&c.cycle_id==='CHR001-CYCLE-0041'&&c.sequence===41,'cycle identity');
 ok(prev?.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V14'&&prev.sequence===40,'source cycle version');
 ok(c.transition==='TEMPORAL_GOVERNANCE_REFINED'&&c.status==='READY_FOR_NARRATOR'&&c.next_role==='NARRADOR'&&c.provocation_id==='M3.02','role/status/transition');
 ok(c.source_head_sha==='1af5e5549120be66115bc8c8c4c61d0ea3d7a3f2','source master mismatch');
 ok(c.previous_cycle?.path===cycle(40),'previous cycle');
 ok(c.manifest_path==='novydres/MANIFEST_V56.json'&&c.manifest_ref?.path===c.manifest_path,'manifest');
 ok(eq(c.checkpoint,prev.checkpoint),'played checkpoint mutated');
 ok(c.checkpoint.last_event_id==='CHR001-M301-C05-22-20261109-001'&&c.checkpoint.next_scene==='C01'&&c.checkpoint.next_scene_status==='NOT_STARTED'&&c.checkpoint.mortal===true&&c.checkpoint.embrace_occurred===false,'last event/Embrace/scene');
 for(const k of stateKeys)ok(eq(c.refs?.[k],prev.refs?.[k]),'historical state changed '+k);
 for(const k of mechanicalKeys)ok(eq(c.operational_gates?.mechanical_sources?.[k],prev.operational_gates?.mechanical_sources?.[k]),'mechanical provenance changed '+k);
 ok(eq(c.operational_gates?.mechanical_matrix_ref,prev.operational_gates?.mechanical_matrix_ref),'mechanical matrix changed');
 ok(eq(c.plan,prev.plan),'M3.02 preparation changed silently');
 ok(eq(c.scene_frame,prev.scene_frame),'already authorized scene frame changed');
 ok(eq(c.activation,prev.activation),'activation changed');
 ok(eq(c.guards,prev.guards),'historical guards changed');
 ok(eq(c.blocking,prev.blocking),'blocking changed');
 ok(eq(c.operational_gates,prev.operational_gates),'scene/mechanical gate changed');
 ok(c.pending_player_decision===null&&prev.pending_player_decision===null,'invented player choice');
 ok(c.review?.decision==='TEMPORAL_GOVERNANCE_REFINED'&&c.review.against_last_event_id===c.checkpoint.last_event_id,'review origin');
 ok(Object.keys(c.architecture).length===Object.keys(prev.architecture).length+addedArch.length,'unexpected architecture width');
 for(const [k,v] of Object.entries(prev.architecture))
  if(!changedArch.includes(k))ok(eq(c.architecture?.[k],v),'immutable authority ref changed '+k);
 for(const k of [...changedArch,...addedArch])ok(c.architecture?.[k]?.path&&/^[a-f0-9]{40}$/.test(c.architecture[k].blob_sha),'missing new authority '+k);
 const t=c.temporal_governance;
 ok(t?.temporal_selection==='SITUATIONAL_CONTINUITY_FIRST_WHEN_MEANINGFUL','temporal mode decision');
 ok(eq(t.possible_modes,['CONTINUITY','ABSTRACTION','MONTAGE','ELLIPSIS']),'possible temporal modes');
 for(const k of ['ellipse_per_scene_required','ellipse_per_act_required','ellipse_per_provocation_required','prelude_mandatory','prelude_results_recorded','past_scene_changed','new_event_recorded','elapsed_time_recorded','pc_action_assumed','npc_knowledge_changed','xp_fv_changed','scene_started'])
  ok(t?.[k]===false,'false or obligatory time progression '+k);
 for(const k of ['continuity_if_meaningful','ellipsis_requires_dramaturgical_reason','world_advances_causally_during_ellipse','prepared_scene_time_remains_prospective','narrator_grant_requires_player_handoff'])
  ok(t?.[k]===true,'temporal right missing '+k);
 ok(t?.prelude_distinct_tests_max===2&&t?.prelude_tests_planned_now===0,'unsupported prelude counts');
 ok(eq(t.source_cycle_ref,c.previous_cycle),'temporal source cycle mismatch');
 ok(eq(t.decision_ref,c.architecture.player_living_ellipsis_decision),'temporal decision mismatch');
 ok(eq(t.pacing_ref,c.architecture.pacing_policy),'pacing mismatch');
 ok(eq(t.prelude_protocol_ref,c.architecture.ellipsis_prelude_protocol),'prelude mismatch');
 ok(eq(t.temporal_review_ref,c.architecture.temporal_review),'temporal plan mismatch');
 return {ok:true,status:c.status,scene_started:false,scene_ready:true,elapsed_time_recorded:false,prelude_tests_planned_now:0};
}
export function validateLatestV15(root){
 const dir=path.resolve(root,'novydres/chronicles/CHR-001/orchestration');
 const ns=fs.readdirSync(dir).map(n=>/^CYCLE_V(\d{4})\.json$/.exec(n)).filter(Boolean).map(x=>+x[1]);
 ok(Math.max(...ns)===41,'latest cycle is not C41');
 const c=j(root,cycle(41)),prev=j(root,cycle(40)),before=j(root,cycle(39));
 validateSceneFrameGrant(prev,before);
 validateC41(c,prev);
 for(let n=41;n>=2;n--){
  const obj=j(root,cycle(n));
  ok(obj.previous_cycle.path===cycle(n-1),'history chain path '+n);
  pin(root,obj.previous_cycle,'history predecessor '+n);
 }
 pin(root,c.manifest_ref,'manifest');
 for(const [k,v] of Object.entries(c.refs))pin(root,v,'state '+k);
 for(const [k,v] of Object.entries(c.architecture))pin(root,v,'architecture '+k);
 for(const [k,v] of Object.entries(c.activation))pin(root,v,'activation '+k);
 pin(root,c.operational_gates.mechanical_matrix_ref,'mechanical matrix');
 for(const [k,v] of Object.entries(c.operational_gates.mechanical_sources))pin(root,v,'mechanical '+k);
 pin(root,c.plan.dossier,'dossier');pin(root,c.plan.sidecar,'sidecar');
 for(const k of ['source_manifest_ref','source_cycle_ref','decision_ref','pacing_ref','prelude_protocol_ref','temporal_review_ref'])pin(root,c.temporal_governance[k],'temporal '+k);
 const m=j(root,c.manifest_path),o=m.runtime?.orchestration,na=m.runtime?.narrative_architecture;
 ok(m.branch==='master'&&o?.current_cycle===cycle(41)&&o?.status===c.status&&o?.next_role===c.next_role,'manifest cursor');
 ok(o?.next_scene==='C01'&&o?.next_scene_status==='NOT_STARTED'&&o?.next_scene_executable===true,'scene launch state');
 ok(m.runtime.last_confirmed_narrative_event===c.checkpoint.last_event_id,'event mismatch');
 for(const [k,ref] of Object.entries(c.architecture)){
  ok(eq(na?.blob_refs?.[k],ref),'manifest architecture pin '+k);
  if(typeof na[k]==='string')ok(na[k]===ref.path,'manifest architecture path '+k);
 }
 const ptr=[['contract','orchestration_contract'],['entrypoint','start_here'],['cycle_schema','cycle_schema'],['validator','cycle_validator'],['tests','cycle_tests'],['schema_tests','cycle_schema_tests']];
 for(const [p,k] of ptr)ok(o[p]===c.architecture[k].path&&o[p+'_blob_sha']===c.architecture[k].blob_sha,'orchestration pointer '+p);
 for(const [p,k] of [['role_dramaturgo','role_dramaturgo'],['role_narrador','role_narrador'],['handoff_to_narrador','handoff_to_narrador']])
  ok(o[p]===c.architecture[k].path,'role adapter '+p);
 ok(o?.temporal_policy==='SITUATIONAL_LIVING_ELLIPSE_NONMANDATORY'&&o?.prelude_distinct_test_max===2,'orchestration temporal policy');
 ok(eq(m.runtime.current_m3_02_preparation?.dossier,c.plan.dossier)&&eq(m.runtime.current_m3_02_preparation?.sidecar,c.plan.sidecar),'current dossier changed');
 ok(m.runtime.current_m3_02_preparation.scene_started===false&&m.runtime.current_m3_02_preparation.first_cause_realized===false,'preplayed incident');
 ok(eq(m.runtime.temporal_governance?.policy_ref,c.architecture.pacing_policy)&&eq(m.runtime.temporal_governance?.decision_ref,c.architecture.player_living_ellipsis_decision),'manifest temporal references');
 ok(m.runtime.temporal_governance.ellipse_mandatory===false&&m.runtime.temporal_governance.prelude_mandatory===false,'manifest forces ellipse');
 ok(m.runtime.temporal_governance.scene_started===false&&m.runtime.temporal_governance.elapsed_time_recorded===false,'manifest fictitious time');
 const review=j(root,c.temporal_governance.temporal_review_ref.path);
 ok(review.source_last_event_id===c.checkpoint.last_event_id&&review.no_played_event===true&&review.no_precommitted_time_delta===true,'review invented event');
 ok(review.prelude?.test_specs?.length===0&&review.prelude?.max_distinct_tests===2&&review.no_automatic_ellipse_next_scene===true,'temporal review prelude/count');
 ok(review.temporal_mode==='ELLIPSIS_PROSPECTIVE_FOR_THIS_FRAME_NOT_GLOBAL_POLICY'&&review.prior_important_choice_erased===false,'frame governance');
 const decision=j(root,c.temporal_governance.decision_ref.path);
 ok(decision.id==='PLAYER_DECISION_CHR001_LIVING_ELLIPSES_V001_PLAYER_SAFE','wrong player directive');
 const ds=j(root,c.plan.dossier.path);
 ok(ds.first_incident.actual_cause_present===false&&ds.mechanics.xp_credit_available===0&&ds.mechanics.willpower.available===4,'event or resources precommitted');
 const git=args=>execFileSync('git',['-C',root,...args],{encoding:'utf8'}).trim();
 ok(git(['rev-parse','HEAD^'])===c.source_head_sha,'commit parent does not match original master');
 ok(git(['rev-parse','HEAD:'+cycle(41)])===hash(read(root,cycle(41))),'cycle tree SHA mismatch');
 ok(git(['rev-parse','HEAD:'+c.manifest_path])===c.manifest_ref.blob_sha,'manifest tree SHA mismatch');
 return {ok:true,cycle:c.cycle_id,status:c.status,predecessor_links:40,protected_state_refs:6,mechanical_refs:9,temporal_modes:4,ellipsis_mandatory:false,prelude_tests_planned:0,prelude_test_max:2,scene_started:false,ready_for_narrator:true};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){
 try{const i=process.argv.indexOf('--root');console.log(JSON.stringify(validateLatestV15(path.resolve(i<0?process.cwd():process.argv[i+1]))));}
 catch(e){console.error(String(e));process.exitCode=1;}
}
