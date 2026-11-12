import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyD03} from './verificar-migracao-d03.mjs';
const read=p=>JSON.parse(readFileSync(p,'utf8'));
const id='world-atlas-novydres';
const dir='novydres/cenario/atlas-novydres';
test('D03 verifies 64 exact source blobs, 9 owners, provenance and no editorial promotion',()=>{
 const r=verifyD03();assert.equal(r.ok,true);assert.equal(r.originals,64);
 assert.equal(r.identical_blobs,64);assert.equal(r.subject_portfolios,9);
 assert.match(r.gate,/SEMANTIC_EQUIVALENCE_PENDING/);
});
test('D03 rejects false authority promotion',()=>{
 const x=read(dir+'/registro.json');x.editorial_promotion=true;
 assert.throws(()=>verifyD03(process.cwd(),{ledgerOverrides:{[id]:x}}),{code:'D03_UNAUTHORIZED_PROMOTION'});
});
test('D03 rejects truncated portfolio',()=>{
 const x=read(dir+'/registro.json');x.source_records.pop();
 assert.throws(()=>verifyD03(process.cwd(),{ledgerOverrides:{[id]:x}}),{code:'D03_INCOMPLETE_COVERAGE'});
});
test('D03 rejects destination digest substitution',()=>{
 const x=read(dir+'/registro.json');x.source_records[0].source_blob_sha='0'.repeat(40);
 assert.throws(()=>verifyD03(process.cwd(),{ledgerOverrides:{[id]:x}}),{code:'D03_AUTHORITY_OR_SHA_MISMATCH'});
});
