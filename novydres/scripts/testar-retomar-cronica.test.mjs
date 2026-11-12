import test from 'node:test';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {readC45Candidate} from './retomar-cronica.mjs';
const sha=execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim();
test('D05 read C45 without promoting historical C41',()=>{
 const x=readC45Candidate({snapshot_sha:sha});
 assert.equal(x.cursor.last_event_id,'CHR001-M302-C01-05-20261111-001');
 assert.equal(x.actor_subjects,38);
 assert.equal(x.open_threads,44);
 assert.equal(x.resources.xp_spent,270);
 assert.equal(x.status,'CANDIDATE_NON_OPERATIONAL');
});
test('D05 read situated NPC knowledge without collapsing actor lines',()=>{
 const x=readC45Candidate({snapshot_sha:sha,actor_id:'npc-pavel-heating-supervisor'});
 assert.equal(x.actor.actor_id,'npc-pavel-heating-supervisor');
 assert.equal(x.actor.records.length,5);
 assert.ok(x.actor.records.every(y=>y.record.entity==='npc-pavel-heating-supervisor'));
});
test('D05 fail closed on disclosure, wrong actor and unconfirmed writing',()=>{
 assert.throws(()=>readC45Candidate({snapshot_sha:sha,role:'PLAYER'}),{code:'DISCLOSURE_DENIED'});
 assert.throws(()=>readC45Candidate({snapshot_sha:sha,actor_id:'npc-no-one'}),{code:'NOT_FOUND'});
 assert.throws(()=>readC45Candidate({snapshot_sha:'0'.repeat(40)}),{code:'HEAD_DIFFERENT'});
 assert.throws(()=>readC45Candidate({snapshot_sha:sha,confirmed_write:{status:'PENDING',snapshot_sha:sha,readback:false}}),{code:'PENDING_PERSISTENCE'});
});
