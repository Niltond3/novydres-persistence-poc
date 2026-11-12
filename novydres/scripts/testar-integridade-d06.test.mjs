import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyD06} from './verificar-integridade-d06.mjs';
const current=()=>JSON.parse(readFileSync('novydres/sistema/arquitetura/fase-d/execucao-d05.json','utf8'));
test('D06 audited complete origin routing never claims editorial PASS from source copies',()=>{
 const x=verifyD06();assert.equal(x.originals,1029);assert.equal(x.source_exact_custody,915);
 assert.equal(x.active_successions_requiring_contextual_semantic_review,121);
 assert.equal(x.gate,'D06_NOT_YET_PASS');
});
test('D06 rejects removed originals and fabricated origin approval',()=>{
 const x=current();x.source_records.pop();
 assert.throws(()=>verifyD06({ledgerOverride:x}),{code:'SOURCE_COVERAGE_COUNT'});
 const y=current();y.source_records[0].original_git_blob_sha='0'.repeat(40);
 assert.throws(()=>verifyD06({ledgerOverride:y}),{code:'D05_RETIREMENT_WRONG_PIN'});
});
