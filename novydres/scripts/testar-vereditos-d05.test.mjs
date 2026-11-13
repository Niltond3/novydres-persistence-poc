import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyD05Verdicts} from './verificar-vereditos-d05.mjs';
const read=()=>JSON.parse(readFileSync('novydres/sistema/arquitetura/fase-d/execucao-d05.json','utf8'));
test('All 121 reference verdicts tracked; 2 approved policy replacements, 119 unproven, 0 equivalence',()=>{
 const r=verifyD05Verdicts();
 assert.equal(r.reference_rows,121);
 assert.equal(r.cycle_direct,48);
 assert.equal(r.manifest_only,73);
 assert.equal(r.policy_replacements,2);
 assert.equal(r.behavioral_blocked,119);
 assert.equal(r.equivalent_verified,0);
 assert.equal(r.gate,'D05_NOT_PASS_FUNCTIONAL_PROOF_PENDING');
});
test('Cannot silently claim an unreviewed successor equivalent',()=>{
 const x=read();x.source_records.find(r=>r.active_original_reference&&r.functional_review.verdict==='BLOCKED').functional_review.verdict='EQUIVALENT_VERIFIED';
 assert.throws(()=>verifyD05Verdicts({override:x}),{code:'D05_UNPROVEN_FUNCTION_FALSE_PASS'});
});
test('Cannot invent a third approved replacement',()=>{
 const x=read();x.source_records.find(r=>r.active_original_reference&&r.functional_review.verdict==='BLOCKED').functional_review.verdict='APPROVED_REPLACEMENT';
 assert.throws(()=>verifyD05Verdicts({override:x}),{code:'D05_UNPROVEN_FUNCTION_FALSE_PASS'});
});
test('Cannot falsify original SHA or the DEC-18 authorization',()=>{
 const x=read();x.source_records.find(r=>r.origin==='novydres/runtime/G26_NONBLOCKING_PERSISTENCE_V1.md').functional_review.decision='UNKNOWN';
 assert.throws(()=>verifyD05Verdicts({override:x}),{code:'D05_POLICY_REPLACEMENT_UNSUPPORTED'});
 const y=read();y.source_records.find(r=>r.origin==='novydres/runtime/G28_SCENE_END_BATCH_AND_DYNAMIC_CONFLICT_V1.md').functional_review.source_blob_sha='0'.repeat(40);
 assert.throws(()=>verifyD05Verdicts({override:y}),{code:'D05_VERDICT_MISSING_OR_UNTRUSTED'});
});
test('Cannot falsely declare D05 PASS or ignore manifest-only references',()=>{
 const x=read();x.functional_review_by_successor.is_d05_pass=true;
 assert.throws(()=>verifyD05Verdicts({override:x}),{code:'D05_FALSE_GATE_APPROVAL'});
 const y=read();y.source_records.find(r=>r.reference_kind==='M63_MANIFEST_ONLY_NOT_PROVEN_INACTIVE').active_original_reference=false;
 assert.throws(()=>verifyD05Verdicts({override:y}),{code:'D05_ACTIVE_REFERENCE_COVERAGE'});
});
