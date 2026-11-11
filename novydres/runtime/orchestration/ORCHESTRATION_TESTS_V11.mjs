import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { validateEpisodeClosureTransition, verifyHistory } from './ORCHESTRATION_VALIDATOR_V11.mjs';

const ref=(path,blob_sha='a'.repeat(40))=>({path,blob_sha});
const state={live:ref('live'),history_index:ref('history'),episode:ref('episode'),character:ref('character'),knowledge:ref('knowledge'),threads:ref('threads')};
const mech={rules_provenance:ref('r'),target_sheet:ref('t'),adjudication_gate:ref('a'),motor_manual:ref('m'),xp_policy:ref('xp'),xp_audit:ref('xa'),act_resolution_schema:ref('as'),xp_envelope:ref('xe'),settlement_record:ref('sr')};
const gates={architecture_active:true,d07_active:true,story_preparation_ready:false,mechanical_scene_ready:false,scene_ready:false,narrator_permission:false,mechanical_matrix_ref:ref('matrix'),mechanical_sources:mech};
const checkpoint={last_event_id:'CHR001-M301-C05-22-20261109-001',last_closed_scene:'C05',next_scene:'C06',next_scene_status:'NOT_STARTED',pending_persistence:false,mortal:true,embrace_occurred:false};
const prev={sequence:36,cycle_id:'CHR001-CYCLE-0036',provocation_id:'M3.01',transition:'CLOSURE_RECOMMENDED',status:'PROVOCATION_CLOSURE_PENDING',pending_player_decision:'CLOSE_M3_01_AS_ALTERNATE_OR_CONTINUE',checkpoint,refs:state,operational_gates:gates,activation:{authorization:ref('auth'),d07_activation:ref('act'),truth_package:ref('truth'),architecture_contract:ref('old-contract')}};
const make=()=>({sequence:37,cycle_id:'CHR001-CYCLE-0037',provocation_id:'M3.01',transition:'EPISODIC_CLOSURE_APPROVED',status:'PROVOCATION_EPISODE_CLOSED',next_role:'NONE',previous_cycle:{path:'novydres/chronicles/CHR-001/orchestration/CYCLE_V0036.json',blob_sha:'b'.repeat(40)},checkpoint:{...checkpoint},refs:structuredClone(state),operational_gates:structuredClone(gates),activation:structuredClone(prev.activation),plan:{validity:'STALE',reviewed_against_event_id:checkpoint.last_event_id},review:{decision:'EPISODE_CLOSED',against_last_event_id:checkpoint.last_event_id},pending_player_decision:null,blocking:{code:null,reason:null},guards:{no_story_delta_in_prep:true,no_xp_fv_delta_in_prep:true,g28_scene_only:true,frozen_unchanged:true,no_public_spoilers:true},episode_closure:{closure_id:'CHR001-M301-EPISODIC-CLOSE-C05-22',scope:'M3.01_EPISODE_ONLY',decision:'CLOSE_M3_01_EPISODIC_ALTERNATE',decision_ref:ref('decision'),source_cycle_ref:{...ref('novydres/chronicles/CHR-001/orchestration/CYCLE_V0036.json','b'.repeat(40))},preserved_threads_ref:structuredClone(state.threads),creation_route_disposition:'UNCHANGED_PENDING',scene_authorized:false,narrator_authorized:false,state_delta:false},architecture:{player_episode_closure_decision:ref('novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_M301_EPISODIC_CLOSURE_V001_PLAYER_SAFE.json')}});

test('accepts episodic closure with unchanged state and route disposition',()=>assert.equal(validateEpisodeClosureTransition(make(),prev).ok,true));
test('rejects changed last event',()=>{const c=make();c.checkpoint.last_event_id='invented';assert.throws(()=>validateEpisodeClosureTransition(c,prev),/checkpoint\/event/);});
test('rejects a changed persistent thread pin',()=>{const c=make();c.refs.threads.blob_sha='c'.repeat(40);assert.throws(()=>validateEpisodeClosureTransition(c,prev),/state ref/);});
test('rejects scene readiness',()=>{const c=make();c.operational_gates.scene_ready=true;assert.throws(()=>validateEpisodeClosureTransition(c,prev),/opened gate scene_ready/);});
test('rejects Narrator permission',()=>{const c=make();c.operational_gates.narrator_permission=true;assert.throws(()=>validateEpisodeClosureTransition(c,prev),/opened gate narrator_permission/);});
test('rejects route disposition change',()=>{const c=make();c.episode_closure.creation_route_disposition='ALTERNATE';assert.throws(()=>validateEpisodeClosureTransition(c,prev),/changed route/);});
test('rejects a fictional state delta',()=>{const c=make();c.episode_closure.state_delta=true;assert.throws(()=>validateEpisodeClosureTransition(c,prev),/state/);});
test('rejects M3.02/C06 activation',()=>{const c=make();c.checkpoint.next_scene_status='STARTED';assert.throws(()=>validateEpisodeClosureTransition(c,prev),/checkpoint\/event/);});
test('rejects missing player decision pin',()=>{const c=make();c.architecture.player_episode_closure_decision.path='wrong.json';assert.throws(()=>validateEpisodeClosureTransition(c,prev),/decision pin/);});
test('rejects changed mechanical evidence',()=>{const c=make();c.operational_gates.mechanical_sources.xp_policy.blob_sha='f'.repeat(40);assert.throws(()=>validateEpisodeClosureTransition(c,prev),/mechanical source refs/);});
test('verifies predecessor links from the immediate previous cycle',()=>{
 const root=mkdtempSync(join(tmpdir(),'novydres-history-'));
 try{
  const dir=join(root,'novydres/chronicles/CHR-001/orchestration'); mkdirSync(dir,{recursive:true});
  const path='novydres/chronicles/CHR-001/orchestration/CYCLE_V0001.json';
  const first=Buffer.from(JSON.stringify({sequence:1,cycle_id:'CHR001-CYCLE-0001',previous_cycle:null}));
  writeFileSync(join(dir,'CYCLE_V0001.json'),first);
  const blob_sha=createHash('sha1').update(Buffer.from(`blob ${first.length}\0`)).update(first).digest('hex');
  const current={sequence:2,cycle_id:'CHR001-CYCLE-0002',previous_cycle:{path,blob_sha}};
  assert.equal(verifyHistory(root,current),2);
  current.previous_cycle.blob_sha='0'.repeat(40);
  assert.throws(()=>verifyHistory(root,current),/predecessor link mismatch/);
 }finally{rmSync(root,{recursive:true,force:true});}
});
