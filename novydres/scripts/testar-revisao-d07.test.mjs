import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {reviewD07} from './revisar-independente-d07.mjs';
const root='novydres/cronicas/CHR-001/';
test('D07 independently checks 47 records across 38 actors and 44 threads',()=>{
 const x=reviewD07();
 assert.equal(x.actor_rows_exact,47);
 assert.equal(x.actor_scopes,38);
 assert.equal(x.gate,'D07_NOT_YET_PASS');
});
test('D07 independently rejects fabrication in an actor history',()=>{
 const a=JSON.parse(readFileSync(root+'conhecimento/atores/npc-mary-krauser/conhecimento.json','utf8'));
 a.records[0].record.confirmed.push('FABRICATED');
 assert.throws(()=>reviewD07({actorOverride:{id:a.subject_id,doc:a}}),{code:'D07_ACTOR_STATEMENT_DRIFT'});
});
test('D07 rejects a changed unresolved thread as equivalent',()=>{
 const t=JSON.parse(readFileSync(root+'tramas/abertas/atual-c45.json','utf8'));
 t.threads.pop();
 assert.throws(()=>reviewD07({threadOverride:t}),{code:'D07_THREADS_SEMANTIC_REWRITE'});
});
