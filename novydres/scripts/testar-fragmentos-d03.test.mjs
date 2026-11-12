import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyD03Segments} from './verificar-fragmentos-d03.mjs';
const src=()=>JSON.parse(readFileSync('novydres/sistema/arquitetura/fase-d/fragmentos-d03.json','utf8'));
test('D03 source section and JSON-field locators cover all 64 originals without promotion',()=>{
  const out=verifyD03Segments();assert.equal(out.ok,true);assert.equal(out.documents,64);assert.ok(out.locators>1500);
});
test('D03 rejects excerpt without stable line bounds',()=>{
  const x=src();const d=x.documents.find(d=>d.sections_or_fields.some(f=>f.kind==='MARKDOWN_SECTION'));
  d.sections_or_fields.find(f=>f.kind==='MARKDOWN_SECTION').line_end=999999;
  assert.throws(()=>verifyD03Segments(process.cwd(),x),{code:'D03_SEGMENT_INVALID_RANGE'});
});
test('D03 rejects claimed CONFIRMED for unreviewed document',()=>{
  const x=src();x.documents[0].epistemic_status='CONFIRMED';
  assert.throws(()=>verifyD03Segments(process.cwd(),x),{code:'D03_SEGMENT_TRUTH_PROMOTION'});
});
test('D03 rejects source SHA substitution',()=>{
  const x=src();x.documents[0].source_blob_sha='0'.repeat(40);
  assert.throws(()=>verifyD03Segments(process.cwd(),x),{code:'D03_SEGMENT_SOURCE_SHA'});
});
test('D03 rejects altered section label with exact source anchor',()=>{
 const x=src(),d=x.documents.find(d=>d.sections_or_fields.some(f=>f.kind==='MARKDOWN_SECTION'));
 d.sections_or_fields.find(f=>f.kind==='MARKDOWN_SECTION').label='INVALID-RENAMED-SECTION';
 assert.throws(()=>verifyD03Segments(process.cwd(),x),{code:'D03_SEGMENT_LABEL_MISMATCH'});
});
