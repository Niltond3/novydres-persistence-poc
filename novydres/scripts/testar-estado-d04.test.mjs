import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyD04State} from './verificar-estado-d04.mjs';
const base=JSON.parse(readFileSync('novydres/cronicas/CHR-001/estado/recuperacao-c45.json','utf8'));
const edited=fn=>{const c=structuredClone(base);fn(c);return ()=>verifyD04State({override:c});};
test('D04 C45 readback verifies immutable master pins and stays non-operational',()=>{
 const r=verifyD04State();
 assert.equal(r.ok,true);
 assert.equal(r.gate,'D04_C45_SNAPSHOT_VERIFIED_NOT_FULL_D04_PASS');
 assert.equal(r.actor_knowledge_records,47);
 assert.equal(r.open_threads,44);
});
test('D04 refuses stale C41/cursor swap and wrong C45 blob',()=>{
 assert.throws(edited(x=>x.cursor.next_scene='C01'),{code:'D04_C45_CURSOR_DRIFT'});
 assert.throws(edited(x=>x.source_refs.cycle.sha='0'.repeat(40)),{code:'D04_SOURCE_DRIFT'});
});
test('D04 rejects resource rewriting, disclosure and editor promotion',()=>{
 assert.throws(edited(x=>x.resources.xp_spent++),{code:'D04_RESOURCE_DRIFT'});
 assert.throws(edited(x=>x.visibility='PLAYER_SAFE'),{code:'D04_UNAUTHORIZED_PROMOTION'});
 assert.throws(edited(x=>x.provenance_policy.editorial_promotions=true),{code:'D04_UNPROVEN_THREAD_OR_PROMOTION'});
});
