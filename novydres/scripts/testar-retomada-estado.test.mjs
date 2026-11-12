import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {inspectCandidateResume,continuationDecision} from './retomar-estado.mjs';

const head=execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim();
const base='novydres/cronicas/CHR-001/';
const state=base+'estado/atual.json',story=base+'historias/m301-c01/historia.json',
  plot=base+'tramas/contato-condicional-samir/trama.json',
  knowledge=base+'elenco/npc-samir-haddad/conhecimento.json';
const obj=path=>JSON.parse(readFileSync(path,'utf8'));
const changed=(path,fn)=>{
 const copy=obj(path);fn(copy);
 return inspectCandidateResume(process.cwd(),{snapshot_sha:head,overrides:{[path]:copy}});
};
const code=(fn,expected)=>assert.throws(fn,e=>e.code===expected,'expected '+expected);
test('V06/V07 scoped C41 recovery from real pinned historical text/cycle/live, not master C45',()=>{
 const recovered=inspectCandidateResume(process.cwd(),{snapshot_sha:head,expected_head:head});
 assert.equal(recovered.status,'CANDIDATE_HISTORICAL_ONLY');
 assert.equal(recovered.snapshot_sha,head);
 assert.equal(recovered.source_commit,'c26c0fbf15fff6c817182c06e6208e302b954f3a');
 assert.equal(recovered.checkpoint.scene_started,false);
 assert.equal(recovered.checkpoint.player_decision_pending,false);
 assert.equal(recovered.historical_literal.marker_count,8);
 assert.equal(recovered.unresolved.historical_cursor_drift,'DECLARED_C41_NOT_C45');
 assert.equal(recovered.next_action,'MIGRATION_REVIEW_ONLY_NO_SCENE');
 assert.equal(recovered.resources.xp_remaining,
   recovered.resources.xp_total-recovered.resources.xp_spent);
});
test('V07 deterministic recovery in a fresh invocation does not create scene, alter resources or reroll',()=>{
 const first=inspectCandidateResume(process.cwd(),{snapshot_sha:head});
 const second=inspectCandidateResume(process.cwd(),{snapshot_sha:head});
 assert.deepEqual(first,second);
 assert.equal(second.publication.state,'NOT_OPERATIONAL');
});
test('V07 stale checkout/expected HEAD does not mix branch snapshots',()=>{
 code(()=>inspectCandidateResume(process.cwd(),{snapshot_sha:head,
   expected_head:'0'.repeat(40)}),'HEAD_DIFFERENT');
});
test('V07 historical mirror cannot be silently promoted to runtime',()=>{
 code(()=>inspectCandidateResume(process.cwd(),{snapshot_sha:head,mode:'OPERATIONAL'}),'CANDIDATE_NOT_OPERATIONAL');
 code(()=>changed(state,o=>o.not_operational=false),'CANDIDATE_NOT_OPERATIONAL');
});
test('V06 algebra for XP and willpower rejects invented balances',()=>{
 code(()=>changed(state,o=>o.resources.xp_remaining++),'RESOURCE_MISMATCH');
 code(()=>changed(state,o=>o.resources.willpower_available++),'RESOURCE_MISMATCH');
 code(()=>changed(state,o=>o.resources.xp_credit_available=99),'UNPROVEN_SPENDABLE_CREDIT');
});
test('V06 arithmetically consistent but changed resource history still conflicts',()=>{
 code(()=>changed(state,o=>{o.resources.xp_total++;o.resources.xp_remaining++;}),
   'HISTORICAL_RESOURCE_DRIFT');
});
test('V06 source bytes and pins checked at original historical commit',()=>{
 code(()=>changed(state,o=>o.source_live.sha='0'.repeat(40)),'SOURCE_HASH_MISMATCH');
 code(()=>changed(state,o=>o.source_live.path='other/missing.json'),'SOURCE_NOT_FOUND');
 code(()=>changed(state,o=>o.source_commit='0'.repeat(40)),'SOURCE_NOT_FOUND');
});
test('V06 material consequence mismatch rejected rather than silently reconciled',()=>{
 code(()=>changed(state,o=>o.workshop.tow_vehicle_owned=true),'MATERIAL_EFFECT_DRIFT');
});
test('V07 cursor/cycle disagreement cannot invent a new scene or a new event',()=>{
 code(()=>changed(state,o=>o.checkpoint.next_scene='C99'),'CURSOR_DRIFT');
 code(()=>changed(state,o=>o.checkpoint.scene_started=true),'SCENE_ALREADY_STARTED');
 code(()=>changed(state,o=>o.checkpoint.last_event_id='fabricated-event'),'CURSOR_DRIFT');
});
test('V07 history must preserve pending intention as unknown, not invent player response',()=>{
 code(()=>changed(state,o=>o.checkpoint.next_scene_status='IN_PROGRESS'),'CURSOR_DRIFT');
 code(()=>changed(state,o=>o.checkpoint.embrace_occurred=true),'CURSOR_DRIFT');
});
test('V06 literal marker presence, source identity and historical transparency',()=>{
 code(()=>changed(story,o=>o.event_text_markers[0].scene_marker='FABRICATED_SCENE'),'LITERAL_MARKER_MISMATCH');
 code(()=>changed(story,o=>o.primary_literal.sha='0'.repeat(40)),'SOURCE_HASH_MISMATCH');
 code(()=>changed(story,o=>o.technical_ledger_proven=true),'TECHNICAL_LEDGER_INVENTED');
});
test('V07 npc claim/status stays scoped; future outcome not fabricated',()=>{
 code(()=>changed(knowledge,o=>o.claims_are_not_world_facts=false),'EPISTEMIC_CONFLICT');
 code(()=>changed(plot,o=>o.future_contact_realized=true),'FUTURE_EVENT_INVENTED');
 code(()=>changed(plot,o=>o.pc_obligation_created=true),'FUTURE_EVENT_INVENTED');
});
test('V07 unverified transaction or missing readback never delivers new fiction',()=>{
 code(()=>inspectCandidateResume(process.cwd(),{snapshot_sha:head,
   confirmed_write:{status:'REF_UPDATED_READBACK_PENDING',snapshot_sha:head,readback:false}}),
   'PENDING_PERSISTENCE');
 code(()=>inspectCandidateResume(process.cwd(),{snapshot_sha:head,
   confirmed_write:{status:'CONFIRMED',snapshot_sha:'a'.repeat(40),readback:true}}),
   'PENDING_PERSISTENCE');
});
test('V07 continuation verdict distinguishes stale, publication pending and verified',()=>{
 const good={expected_head:head,actual_head:head,commit_sha:head,verified_blobs:true,
   transaction_status:'CONFIRMED',evidence:{commit_sha:head,readback:true}};
 assert.equal(continuationDecision(good),'SNAPSHOT_SYNCED');
 assert.equal(continuationDecision({...good,verified_blobs:false}),'PENDING_PERSISTENCE');
 assert.equal(continuationDecision({...good,actual_head:'a'.repeat(40)}),'HEAD_DIFFERENT');
 assert.equal(continuationDecision({...good,evidence:{commit_sha:head,readback:false}}),'PENDING_PERSISTENCE');
 assert.equal(continuationDecision({...good,transaction_status:'STOP_CONFLICT'}),'STOP_CONFLICT');
});
test('V07 a present source is not automatically semantic proof',()=>{
 // Any well-formed but substantively false claim may pass purely structural
 // validation. That requires separate human/contextual review; report the limit.
 const output=changed(knowledge,o=>o.claims.push('UNVERIFIED_SYNTHETIC_CLAIM'));
 assert.equal(output.actor_claims_status,'NPC_CLAIM_NOT_WORLD_FACT');
 assert.equal(output.publication.authority,'CANDIDATE_ONLY');
});
