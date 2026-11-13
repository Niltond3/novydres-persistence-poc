import test from 'node:test';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {readC45Candidate} from './retomar-cronica.mjs';
const sha=execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim();
test('D05 read C45 without promoting historical C41',()=>{
 const x=readC45Candidate({snapshot_sha:sha,role:'AUDITOR'});
 assert.equal(x.cursor.last_event_id,'CHR001-M302-C01-05-20261111-001');
 assert.equal(x.actor_subjects,38);
 assert.equal(x.story_authority.candidate_runtime_activation,false);
 assert.equal(x.local_mechanics.grapple_bonus_dice,1);
 assert.equal(x.local_mechanics.future_powers_active,false);
 assert.equal(x.open_threads,44);
 assert.equal(x.resources.xp_spent,270);
 assert.equal(x.status,'CANDIDATE_NON_OPERATIONAL');
});
test('D05 read situated NPC knowledge without collapsing actor lines',()=>{
 const x=readC45Candidate({snapshot_sha:sha,role:'AUDITOR',actor_id:'npc-pavel-heating-supervisor'});
 assert.equal(x.actor.actor_id,'npc-pavel-heating-supervisor');
 assert.equal(x.actor.records.length,5);
 assert.ok(x.actor.records.every(y=>y.record.entity==='npc-pavel-heating-supervisor'));
});
test('D05 fail closed on disclosure, wrong actor and unconfirmed writing',()=>{
 assert.throws(()=>readC45Candidate({snapshot_sha:sha,role:'PLAYER'}),{code:'DISCLOSURE_DENIED'});
 assert.throws(()=>readC45Candidate({snapshot_sha:sha,actor_id:'npc-no-one'}),{code:'NOT_FOUND'});
 assert.throws(()=>readC45Candidate({snapshot_sha:'0'.repeat(40),role:'AUDITOR'}),{code:'HEAD_DIFFERENT'});
 assert.throws(()=>readC45Candidate({snapshot_sha:sha,role:'AUDITOR',confirmed_write:{status:'PENDING',snapshot_sha:sha,readback:false}}),{code:'PENDING_PERSISTENCE'});
});

test('C45 scene facts retain explicit unknowns and no invented future event',()=>{
 const x=readC45Candidate({snapshot_sha:sha});
 assert.equal(x.last_scene.scene_id,'CHR001-M302-C01_A_PASSAGEM');
 assert.equal(x.last_scene.status,'CLOSED');
 assert.equal(x.last_scene.confirmed.length,4);
 assert.equal(x.last_scene.unknown.length,4);
 assert.equal(x.cursor.next_scene,'C02');
 assert.equal(x.handoff.historical_close_gate,'DRAMATURGO');
 assert.equal(x.handoff.current_cycle_status,'READY_FOR_NARRATOR');
 assert.equal(x.handoff.next_role,'NARRADOR');
 assert.equal(x.handoff.player_narrator_prompt_required,true);
 assert.equal(x.handoff.candidate_runtime_activation,false);
});

test('C45 historical range lookup is exact and access-scoped, no fabricated ledger',()=>{
 const x=readC45Candidate({snapshot_sha:sha,role:'AUDITOR',history_batch:1});
 assert.equal(x.history_batch.ordinal,1);
 assert.equal(x.history_batch.representation,'ORIGINAL_DIARY_NOT_AUDITED_LEDGER');
 assert.equal(x.historical_index_coverage,'PARTIAL_SOURCE_BACKED_27_BATCHES');
 assert.throws(()=>readC45Candidate({snapshot_sha:sha,history_batch:28}),{code:'HISTORY_BATCH_NOT_FOUND'});
});

test('D05 C45 reader requires an explicit authorized role',()=>{
 assert.throws(()=>readC45Candidate({snapshot_sha:sha}),{code:'ROLE_NOT_AUTHORIZED'});
 assert.throws(()=>readC45Candidate({snapshot_sha:sha,role:null}),{code:'ROLE_NOT_AUTHORIZED'});
});
