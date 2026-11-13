import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyD05} from './verificar-consumidores-d05.mjs';
const l=()=>JSON.parse(readFileSync('novydres/sistema/arquitetura/fase-d/execucao-d05.json','utf8'));
test('D05 covers all 399 with actual source bytes and does not certify 121 live successors',()=>{
 const x=verifyD05();
 assert.equal(x.exact_blobs_inert,285);
 assert.equal(x.historical_git_only,114);
 assert.equal(x.active_source_successions_unproven,121);
 assert.equal(x.cycle_direct_functional_review_pending,48);
 assert.equal(x.manifest_only_not_proven_inactive,73);
 assert.equal(x.gate,'D05_CUSTODY_PASS_BEHAVIORAL_GATE_PENDING');
});
test('D05 rejects fabricated source SHA and disappearance from inventory',()=>{
 const x=l();x.source_records[0].original_git_blob_sha='0'.repeat(40);
 assert.throws(()=>verifyD05({ledgerOverride:x}),{code:'D05_ORIGIN_SHA_OR_OWNER_DRIFT'});
 const y=l();y.source_records.pop();
 assert.throws(()=>verifyD05({ledgerOverride:y}),{code:'D05_COVERAGE'});
});

test('D05 refuses mislabeled manifest-only refs as live cycle pins',()=>{
 const x=l();
 x.source_records.find(r=>r.reference_kind==='M63_MANIFEST_ONLY_NOT_PROVEN_INACTIVE').reference_kind='C45_CYCLE_DIRECT';
 assert.throws(()=>verifyD05({ledgerOverride:x}),{code:'D05_REFERENCE_PROVENANCE_DRIFT'});
});
