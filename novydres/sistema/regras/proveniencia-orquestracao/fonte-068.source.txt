import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {validateSceneFrameGrant,validateLatestV14,assessSpotlightFrame} from './ORCHESTRATION_VALIDATOR_V14.mjs';
const directory=new URL('../../chronicles/CHR-001/orchestration/',import.meta.url);
const c=JSON.parse(readFileSync(new URL('CYCLE_V0040.json',directory)));
const prev=JSON.parse(readFileSync(new URL('CYCLE_V0039.json',directory)));
const clone=()=>JSON.parse(JSON.stringify(c));
const reject=(mut,pattern)=>{const d=clone();mut(d);assert.throws(()=>validateSceneFrameGrant(d,prev),pattern)};
test('C39 to C40 authorizes significant scene WITHOUT starting it',()=>assert.equal(validateSceneFrameGrant(clone(),prev).ok,true));
test('no new event manufactured',()=>reject(x=>x.checkpoint.last_event_id='invented',/checkpoint/));
test('no fabricated PC travel',()=>reject(x=>x.scene_frame.pc_travel_assumed=true,/pc_travel_assumed/));
test('no consequential PC act presumed',()=>reject(x=>x.scene_frame.consequential_pc_action_assumed=true,/consequential_pc_action_assumed/));
test('no invented elapsed time in prep',()=>reject(x=>x.scene_frame.elapsed_time_persisted=true,/elapsed_time_persisted/));
test('no NPC contact presumed as previous fact',()=>reject(x=>x.scene_frame.npc_contact_already_recorded=true,/npc_contact_already_recorded/));
test('no future incident falsely realized',()=>reject(x=>x.scene_frame.future_incident_realized=true,/future_incident_realized/));
test('no NPC knowledge changed',()=>reject(x=>x.scene_frame.npc_knowledge_changed=true,/npc_knowledge_changed/));
test('no changed open threads',()=>reject(x=>x.refs.threads.blob_sha='f'.repeat(40),/state changed threads/));
test('no mechanical source mutation',()=>reject(x=>x.operational_gates.mechanical_sources.xp_envelope.blob_sha='f'.repeat(40),/mechanical source changed xp_envelope/));
test('no fictitious Embrace',()=>reject(x=>x.checkpoint.embrace_occurred=true,/checkpoint changed/));
test('no immediate scene marked started',()=>reject(x=>x.scene_frame.scene_started=true,/scene_started/));
test('reject premature narrative grant without preparation',()=>reject(x=>x.operational_gates.story_preparation_ready=false,/scene gate/));
test('reject mechanical gate omission',()=>reject(x=>x.operational_gates.mechanical_scene_ready=false,/scene gate/));
test('reject missing narrator permission',()=>reject(x=>x.operational_gates.narrator_permission=false,/scene gate/));
test('reject unadmitted world authority swap',()=>reject(x=>x.architecture.d04_plot_admissions.blob_sha='f'.repeat(40),/old authority/));
test('reject omitted player direction',()=>reject(x=>x.architecture.player_spotlight_direction=null,/missing user decision/));
test('reject return to mandatory intent gate',()=>reject(x=>x.pending_player_decision='NEXT_INTENTION_FROM_C05_22',/unjustified/));
test('reject false player agency approval',()=>reject(x=>x.scene_frame.meaningful_choice_available=false,/meaningful_choice_available/));
test('legitimate future scene does NOT require future incident already recorded',()=>{
 const f={last_checkpoint_reconciled:true,admitted_plot:true,prepared_actor_agency:true,spatial_reach:true,meaningful_stakes:true,real_choices:true,routine_ellipsis_allowed:true,incident_already_realized:false};
 assert.equal(assessSpotlightFrame(f),'ELIGIBLE_FOR_SEPARATE_NARRATOR_GRANT');
});
test('unimportant daily steps can be elided without asking for every drive',()=>{
 const f={last_checkpoint_reconciled:true,admitted_plot:true,prepared_actor_agency:true,spatial_reach:true,meaningful_stakes:true,real_choices:true,routine_ellipsis_allowed:true,offscreen_consequential_pc_action:false};
 assert.equal(assessSpotlightFrame(f),'ELIGIBLE_FOR_SEPARATE_NARRATOR_GRANT');
});
test('do not elide a pending consequential player choice',()=>{
 const f={last_checkpoint_reconciled:true,admitted_plot:true,prepared_actor_agency:true,spatial_reach:true,meaningful_stakes:true,real_choices:true,routine_ellipsis_allowed:true,important_pending_player_choice:true};
 assert.equal(assessSpotlightFrame(f),'PENDING_PLAYER_CHOICE');
});
test('no imaginary benefits in ellipsis',()=>{
 const f={last_checkpoint_reconciled:true,admitted_plot:true,prepared_actor_agency:true,spatial_reach:true,meaningful_stakes:true,real_choices:true,routine_ellipsis_allowed:true,fictitious_xp_fv:true};
 assert.equal(assessSpotlightFrame(f),'BLOCKED_AGENCY_OR_CHRONOLOGY');
});
test('no unsupported NPC placement for spectacle',()=>{
 const f={last_checkpoint_reconciled:true,admitted_plot:true,prepared_actor_agency:true,spatial_reach:false,meaningful_stakes:true,real_choices:true,routine_ellipsis_allowed:true};
 assert.equal(assessSpotlightFrame(f),'BLOCKED_INSUFFICIENT_PREPARATION');
});
test('exact pins, full historical chain, Git tree and manifest',()=>assert.equal(validateLatestV14(process.cwd()).ok,true));
