import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {assessSceneEntry,validateCausalTransition,validateLatestV13} from './ORCHESTRATION_VALIDATOR_V13.mjs';
const p='../../chronicles/CHR-001/orchestration/';
const old=JSON.parse(readFileSync(new URL(p+'CYCLE_V0038.json',import.meta.url)));
const base=JSON.parse(readFileSync(new URL(p+'CYCLE_V0039.json',import.meta.url)));
const cp=()=>JSON.parse(JSON.stringify(base));
const deny=(mut,pattern)=>{let c=cp();mut(c);assert.throws(()=>validateCausalTransition(c,old),pattern)};
test('C38 to C39 intentionally requests player intention; no scene grant',()=>assert.equal(validateCausalTransition(cp(),old).ok,true));
test('no event invented',()=>deny(c=>c.checkpoint.last_event_id='invented',/checkpoint/));
test('no action or arbitrary relocation',()=>deny(c=>c.causal_handoff.pc_action_assumed=true,/pc_action_assumed/));
test('no imaginary travel or clock jump',()=>deny(c=>c.causal_handoff.elapsed_time_or_travel=true,/elapsed_time_or_travel/));
test('no NPC appearance absent legitimate cause',()=>deny(c=>c.causal_handoff.npc_presence_assumed=true,/npc_presence_assumed/));
test('no NPC knowledge jump',()=>deny(c=>c.causal_handoff.npc_knowledge_changed=true,/npc_knowledge_changed/));
test('no fictional incident realization',()=>deny(c=>c.causal_handoff.future_incident_realized=true,/false causal entry/));
test('no forced PC selection',()=>deny(c=>c.pending_player_decision='RETURN_TO_WORKSHOP',/intention step/));
test('no intention treated as event',()=>deny(c=>c.causal_handoff.intention_executed=true,/intention_executed/));
test('no automatic intention registered',()=>deny(c=>c.causal_handoff.intention_received=true,/intention_received/));
test('no scene readiness on plan alone',()=>deny(c=>c.operational_gates.scene_ready=true,/premature gate/));
test('no narrator permission on plan alone',()=>deny(c=>c.operational_gates.narrator_permission=true,/premature gate/));
test('no mechanical preflight false-positive',()=>deny(c=>c.operational_gates.mechanical_scene_ready=true,/premature gate/));
test('no thread change',()=>deny(c=>c.refs.threads.blob_sha='f'.repeat(40),/state threads/));
test('no XP/FV change',()=>deny(c=>c.operational_gates.mechanical_sources.xp_envelope.blob_sha='f'.repeat(40),/mechanics xp_envelope/));
test('no lost independent authorial source',()=>deny(c=>c.architecture.d04_plot_admissions.blob_sha='f'.repeat(40),/old authority/));
test('no claim of world entry just because incident planned',()=>{
 const a={prepared_cause:true,authorial_admission:true,actor_capacity_backed:true,real_choices:true,
 immediate_world_condition:false,independent_npc_initiative_backed:false,spatio_temporal_reach_backed:false};
 assert.equal(assessSceneEntry(a),'INTENTION_PENDING');
});
test('legitimate future incident need not already be persisted before eligible scene',()=>{
 const a={prepared_cause:true,authorial_admission:true,actor_capacity_backed:true,real_choices:true,
 immediate_world_condition:false,independent_npc_initiative_backed:true,spatio_temporal_reach_backed:true,
 future_incident_realized:false,mandatory_pc_action:false,fictitious_travel:false,fictitious_time:false,unearned_npc_knowledge:false};
 assert.equal(assessSceneEntry(a),'SCENE_ENTRY_ELIGIBLE_SEPARATE_GRANT');
});
test('no forced action even with independent world cause',()=>{
 const a={prepared_cause:true,authorial_admission:true,actor_capacity_backed:true,real_choices:true,
 immediate_world_condition:true,spatio_temporal_reach_backed:true,mandatory_pc_action:true};
 assert.equal(assessSceneEntry(a),'INTENTION_PENDING');
});
test('no invented NPC knowledge even with available world entry',()=>{
 const a={prepared_cause:true,authorial_admission:true,actor_capacity_backed:true,real_choices:true,
 immediate_world_condition:true,spatio_temporal_reach_backed:true,unearned_npc_knowledge:true};
 assert.equal(assessSceneEntry(a),'INTENTION_PENDING');
});
test('full source, predecessor chain, manifest, and Git tree verification',()=>assert.equal(validateLatestV13(process.cwd()).ok,true));
