#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';

const fail = m => { throw Error('CHR001_V12_BLOCK: ' + m); };
const ok = (v,m) => { if(!v) fail(m); };
const hash = b => crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const read = (root,p) => {
 ok(typeof p === 'string' && p.length > 0 && !path.isAbsolute(p) && !p.split(/[\\/]/).includes('..'),'unsafe path '+p);
 const full=path.resolve(root,p);
 ok(full.startsWith(path.resolve(root)+path.sep),'path traversal '+p);
 return fs.readFileSync(full);
};
const json=(root,p)=>JSON.parse(read(root,p).toString('utf8'));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const pin=(root,r,name)=>{ok(r?.path && r?.blob_sha,name+' missing ref');const got=hash(read(root,r.path));ok(got===r.blob_sha,name+' blob SHA '+r.path);};
const pth=n=>'novydres/chronicles/CHR-001/orchestration/CYCLE_V'+String(n).padStart(4,'0')+'.json';
const stateKeys=['live','history_index','episode','character','knowledge','threads'];
const mechKeys=['rules_provenance','target_sheet','adjudication_gate','motor_manual','xp_policy','xp_audit','act_resolution_schema','xp_envelope','settlement_record'];

export function validateAdminTransition(c,prev){
 ok(c?.sequence===38 && c.cycle_id==='CHR001-CYCLE-0038' && c.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V12','C38 identity');
 ok(c.provocation_id==='M3.02' && c.transition==='NEXT_PROVOCATION_ADMIN_OPENED' && c.status==='READY_FOR_DRAMATURGO' && c.next_role==='DRAMATURGO','M3.02 admin transition/role');
 ok(prev?.sequence===37 && prev.provocation_id==='M3.01' && prev.transition==='EPISODIC_CLOSURE_APPROVED' && prev.status==='PROVOCATION_EPISODE_CLOSED' && prev.next_role==='NONE','source episode not closed C37');
 ok(c.previous_cycle?.path===pth(37) && c.previous_cycle.blob_sha?.length===40,'C37 predecessor ref');
 ok(c.checkpoint?.last_event_id===prev.checkpoint?.last_event_id && c.checkpoint.last_event_id==='CHR001-M301-C05-22-20261109-001','new or changed event');
 ok(c.checkpoint?.last_closed_scene===prev.checkpoint.last_closed_scene && c.checkpoint?.next_scene==='C01' && c.checkpoint?.next_scene_status==='NOT_STARTED' && c.checkpoint?.pending_persistence===false,'C01 cursor/event guard');
 ok(c.checkpoint.mortal===prev.checkpoint.mortal && c.checkpoint.mortal===true && c.checkpoint.embrace_occurred===prev.checkpoint.embrace_occurred && c.checkpoint.embrace_occurred===false,'mortal/Embrace state changed');
 for(const k of stateKeys)ok(eq(c.refs?.[k],prev.refs?.[k]),'changed '+k+' ref');
 for(const k of mechKeys)ok(eq(c.operational_gates?.mechanical_sources?.[k],prev.operational_gates?.mechanical_sources?.[k]),'changed mechanical '+k);
 ok(eq(c.operational_gates?.mechanical_matrix_ref,prev.operational_gates?.mechanical_matrix_ref),'mechanical matrix changed');
 ok(c.operational_gates?.architecture_active===true && c.operational_gates?.d07_active===true,'architecture activation lost');
 for(const k of ['story_preparation_ready','mechanical_scene_ready','scene_ready','narrator_permission'])ok(c.operational_gates?.[k]===false,'scene gate opened '+k);
 ok(c.pending_player_decision===null,'pending player decision invented');
 ok(c.plan?.preparation_id==='CHR001-PREP-M302-20261111-V1' && c.plan?.validity==='REVISED' && c.plan?.reviewed_against_event_id===prev.checkpoint.last_event_id,'wrong planning checkpoint');
 ok(c.review?.decision==='REVISED' && c.review?.against_last_event_id===prev.checkpoint.last_event_id,'review not reconciled');
 ok(c.blocking?.code===null,'unexpected admin blocker');
 ok(!('episode_closure' in c),'episode closure copied as current');
 const a=c.administrative_opening;
 ok(a?.scope==='M3.02_ADMIN_OPEN_ONLY' && a.old_episode_unchanged===true && a.guided_route_pending===true,'closure or route modified');
 for(const k of ['first_cause_realized','new_scene_started','elapsed_time','state_delta','npc_knowledge_delta','xp_fv_delta','scene_authorized','narrator_authorized'])ok(a[k]===false,'fictitious admin delta '+k);
 ok(a.planning_only===true && typeof a.first_scene_blocker==='string' && a.first_scene_blocker.length>20,'admin planning/first-scene guard');
 ok(eq(a.source_episode_cycle_ref,c.previous_cycle),'admin C37 origin changed');
 ok(a.decision_ref?.path===c.architecture?.player_next_provocation_authorization?.path && eq(a.decision_ref,c.architecture.player_next_provocation_authorization),'player authorization pin');
 ok(a.eligibility_ref?.path===c.architecture?.preparation_eligibility_audit?.path && eq(a.eligibility_ref,c.architecture.preparation_eligibility_audit),'eligibility pin');
 ok(c.guards?.no_story_delta_in_prep===true && c.guards?.no_xp_fv_delta_in_prep===true && c.guards?.frozen_unchanged===true && c.guards?.no_public_spoilers===true,'guard dropped');
 ok(c.activation?.d07_activation?.blob_sha===prev.activation?.d07_activation?.blob_sha && c.activation?.authorization?.blob_sha===prev.activation?.authorization?.blob_sha,'activation changed');
 return {ok:true,cycle_id:c.cycle_id,status:c.status,next_role:c.next_role,scene_ready:false,narrator_permission:false};
}

export function validateLatestV12(root){
 const dir=path.resolve(root,'novydres/chronicles/CHR-001/orchestration');
 const found=fs.readdirSync(dir).map(n=>/^CYCLE_V(\d{4})\.json$/.exec(n)).filter(Boolean).map(m=>+m[1]);
 const latest=Math.max(...found);
 ok(latest===38,'unexpected highest cycle '+latest);
 const c=json(root,pth(38)),prev=json(root,pth(37));
 validateAdminTransition(c,prev);
 let historyCount=0;
 for(let n=38;n>=2;n--){
  const current=json(root,pth(n)),pr=current.previous_cycle;
  ok(pr?.path===pth(n-1),'bad historical predecessor path C'+n);
  pin(root,pr,'predecessor C'+n);historyCount++;
 }
 pin(root,c.manifest_ref,'current manifest');
 for(const [k,r] of Object.entries(c.refs))pin(root,r,'state.'+k);
 for(const [k,r] of Object.entries(c.architecture))pin(root,r,'architecture.'+k);
 for(const [k,r] of Object.entries(c.activation))pin(root,r,'activation.'+k);
 for(const [k,r] of Object.entries(c.operational_gates.mechanical_sources))pin(root,r,'mechanical.'+k);
 pin(root,c.operational_gates.mechanical_matrix_ref,'mechanical.matrix');
 pin(root,c.plan.dossier,'plan.dossier');pin(root,c.plan.sidecar,'plan.sidecar');
 pin(root,c.administrative_opening.decision_ref,'authorization');pin(root,c.administrative_opening.eligibility_ref,'eligibility');
 pin(root,c.administrative_opening.source_manifest_ref,'M52');
 ok(c.administrative_opening.source_manifest_ref.path==='novydres/MANIFEST_V52.json','wrong M52 origin');
 const manifest=json(root,c.manifest_ref.path),or=manifest.runtime?.orchestration,na=manifest.runtime?.narrative_architecture;
 ok(c.manifest_path===c.manifest_ref.path && manifest.branch==='master','manifest path/branch');
 ok(or?.current_cycle===pth(38) && or?.status===c.status && or?.next_role===c.next_role,'operational pointer');
 ok(or.next_scene==='C01' && or.next_scene_status==='NOT_STARTED' && or.next_scene_executable===false,'manifest scene cursor');
 for(const k of ['architecture_active','d07_active','story_preparation_ready','mechanical_scene_ready','scene_ready','narrator_permission'])ok(or.operational_gates?.[k]===c.operational_gates[k],'manifest gate '+k);
 ok(manifest.runtime.last_confirmed_narrative_event===prev.checkpoint.last_event_id,'manifest fabricated event');
 ok(manifest.runtime.marco_M3_status==='M3.02_ADMIN_OPEN_C01_NOT_STARTED','manifest Marco status');
 const keys=['d04_plot_admissions','d05_approval_queue','d06','d07','d08','d09','d10_schema_registry','d10_role_adapters','d10_validator','d10_results','d11_cases','d11_results','d11_review','d12_candidate','d12_mechanical_source_refs','d12_validator','d12_results','promotion_inventory','start_here','agent_entry','context_gateway','player_authorization','orchestration_contract','cycle_schema','cycle_validator','cycle_tests','preparation_dossier_schema','preparation_sidecar_schema','cycle_schema_tests','player_episode_closure_decision','player_next_provocation_authorization','preparation_eligibility_audit'];
 for(const k of keys)ok(eq(na?.blob_refs?.[k],c.architecture?.[k]),'manifest architecture pin '+k);
 for(const k of ['start_here','agent_entry','context_gateway','player_authorization','orchestration_contract','cycle_schema','cycle_validator','cycle_tests','cycle_schema_tests','preparation_dossier_schema','preparation_sidecar_schema','player_next_provocation_authorization','preparation_eligibility_audit'])ok(na[k]===c.architecture[k].path,'manifest path '+k);
 ok(or.contract===c.architecture.orchestration_contract.path && or.contract_blob_sha===c.architecture.orchestration_contract.blob_sha,'contract mismatch');
 ok(or.cycle_schema===c.architecture.cycle_schema.path && or.cycle_schema_blob_sha===c.architecture.cycle_schema.blob_sha,'schema mismatch');
 ok(or.validator===c.architecture.cycle_validator.path && or.validator_blob_sha===c.architecture.cycle_validator.blob_sha,'validator mismatch');
 ok(or.tests===c.architecture.cycle_tests.path && or.tests_blob_sha===c.architecture.cycle_tests.blob_sha,'tests mismatch');
 ok(or.schema_tests===c.architecture.cycle_schema_tests.path && or.schema_tests_blob_sha===c.architecture.cycle_schema_tests.blob_sha,'schema test mismatch');
 const ds=json(root,c.plan.dossier.path),sc=json(root,c.plan.sidecar.path),el=json(root,c.administrative_opening.eligibility_ref.path),auth=json(root,c.administrative_opening.decision_ref.path),d04=json(root,c.architecture.d04_plot_admissions.path),d09=json(root,c.architecture.d09.path);
 ok(ds.preparation_id===c.plan.preparation_id && sc.preparation_id===c.plan.preparation_id,'dossier/sidecar identity');
 ok(eq(sc.dossier_ref,c.plan.dossier),'sidecar pin mismatch');
 ok(eq(ds.source_checkpoint.cycle,c.previous_cycle) && eq(sc.source_checkpoint.cycle,c.previous_cycle),'preparation source cycle');
 ok(eq(ds.source_checkpoint.manifest,c.administrative_opening.source_manifest_ref) && eq(sc.source_checkpoint.manifest,c.administrative_opening.source_manifest_ref),'preparation source manifest');
 for(const k of stateKeys)ok(eq(ds.source_checkpoint.state_refs[k],c.refs[k]) && eq(sc.source_checkpoint.state_refs[k],c.refs[k]),'preparation carried '+k);
 ok(ds.first_incident?.status==='PLANNED_CONDITIONAL_NOT_OCCURRED' && ds.first_incident?.actual_cause_present===false && ds.first_incident?.scene_ready===false,'fictional first incident');
 ok(ds.first_incident.story_id==='ST-GANGREL-ATTENTION' && ds.first_incident.plot_admission==='PLOT-GANGREL-ATTENTION','unadmitted incident');
 ok(d04.admissions?.some(a=>a.plot_id===ds.first_incident.plot_admission && a.decision==='ADMITTED_FOR_PROSPECTIVE_AUTHORIAL_PREPARATION'),'D04 admission missing');
 ok(ds.act_contracts?.length>=1 && ds.act_contracts.length<=5 && ds.act_contracts.every(a=>a.choices.length>=2 && a.closures.length>=2 && a.xp==='PLANNED_NOT_GRANTED'),'dramatic choices/acts not bounded');
 ok(ds.mechanics.xp_total===675 && ds.mechanics.xp_spent===270 && ds.mechanics.xp_credit_available===0 && ds.mechanics.willpower.available===4 && ds.mechanics.baseline==='MORTAL_ONLY','mechanical resources mismatch');
 ok(ds.first_scene_review.scene_ready===false && ds.first_scene_review.narrator_permission===false && ds.causal_guards.no_new_event===true,'premature first scene');
 ok(sc.scene_queue?.first==='M3.02.C01' && sc.scene_queue?.status==='NOT_STARTED' && sc.no_narration===true && sc.no_new_event===true,'sidecar first scene fake');
 ok(el.eligibility?.candidate==='M3.02' && el.eligibility?.cause_realized===false && el.eligibility?.initial_scene_ready===false,'eligibility false positive');
 ok(auth.authorization==='PLAYER_EXPLICIT_CURRENT_CHAT' && auth.not_allowed?.includes('Starting or narrating a scene'),'unauthorized scene/approval');
 ok(d09.checkpoint?.cycle==='CYCLE_V0038' && d09.target_route?.status==='PENDING_UNCHANGED' && d09.operational_gate?.scene_ready===false && d09.operational_gate?.narrator_permission===false,'D09 route prematurely closed');
 ok(manifest.runtime.current_m3_02_preparation?.dossier?.blob_sha===c.plan.dossier.blob_sha && manifest.runtime.current_m3_02_preparation?.sidecar?.blob_sha===c.plan.sidecar.blob_sha,'current preparation pointers');
 const git=(args)=>execFileSync('git',['-C',root,...args],{encoding:'utf8'}).trim();
 const head=git(['rev-parse','HEAD']),parent=git(['rev-parse','HEAD^']);
 ok(parent===c.source_head_sha,'source head lease must be candidate commit first parent');
 ok(git(['rev-parse',head+':'+pth(38)])===hash(read(root,pth(38))),'current C38 tree');
 ok(git(['rev-parse',head+':'+c.manifest_path])===c.manifest_ref.blob_sha,'current manifest tree');
 return {ok:true,cycle_id:c.cycle_id,status:c.status,next_role:c.next_role,history_links_verified:historyCount,architecture_refs_verified:Object.keys(c.architecture).length,carried_state_refs_verified:6,mechanical_sources_verified:mechKeys.length,preparation_acts:ds.act_contracts.length,scene_ready:false,narrator_permission:false,source_head:c.source_head_sha,published_tree_checked:true};
}
if(process.argv[1] && path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){
 try{const i=process.argv.indexOf('--root');const root=path.resolve(i<0?process.cwd():process.argv[i+1]);console.log(JSON.stringify(validateLatestV12(root)));}
 catch(e){console.error(String(e));process.exitCode=1;}
}
