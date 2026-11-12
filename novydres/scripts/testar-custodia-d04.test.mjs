import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyD04Custody} from './verificar-custodia-d04.mjs';
const p='novydres/cronicas/CHR-001/episodios/m203/registro.json';
const get=()=>JSON.parse(readFileSync(p,'utf8'));
test('D04 all 438 local sources have unique subject custodian and exact source Git blob',()=>{
 const x=verifyD04Custody();
 assert.deepEqual([x.originals,x.exact_bytes_copied,x.subject_owners],[438,438,31]);
 assert.match(x.gate,/NOT_SEMANTIC_STATE_PASS/);
});
test('D04 refuses raw file alteration or provenance substitution',()=>{
 const x=get();x.source_records[0].original_git_blob_sha='0'.repeat(40);
 assert.throws(()=>verifyD04Custody({overrideSubject:x.subject_id,overrideRecord:x}),{code:'D04_WRONG_SOURCE_OWNER'});
});
test('D04 refuses local source assigned as different owner',()=>{
 const x=get();x.source_records[0].local_owner='chr001-invented-owner';
 assert.throws(()=>verifyD04Custody({overrideSubject:x.subject_id,overrideRecord:x}),{code:'D04_WRONG_SOURCE_OWNER'});
});
test('D04 refuses missing historical source disguised as complete',()=>{
 const x=get();x.source_records.pop();
 assert.throws(()=>verifyD04Custody({overrideSubject:x.subject_id,overrideRecord:x}),{code:'D04_MISSING_RECORD'});
});
test('D04 refuses implicit activation through source metadata',()=>{
 const x=get();x.operational_ownership='ACTIVE';
 assert.throws(()=>verifyD04Custody({overrideSubject:x.subject_id,overrideRecord:x}),{code:'D04_UNAUTHORIZED_OWNER_OR_PROMOTION'});
});
