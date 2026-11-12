import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {validateD03DistributedSegments} from './verificar-segmentos-distribuidos-d03.mjs';
const path='novydres/sistema/regras/experiencia/segmentos.json';
const load=()=>JSON.parse(readFileSync(path,'utf8'));
test('D03: 64 source documents and 1707 locators map to unique subject owners',()=>{
 const result=validateD03DistributedSegments();
 assert.deepEqual([result.source_documents,result.locators,result.unique_owners],[64,1707,9]);
});
test('D03: cannot duplicate source document in owner index',()=>{
 const x=load();x.document_refs.push({...x.document_refs[0]});x.source_document_count++;
 assert.throws(()=>validateD03DistributedSegments({overrides:{[path]:x}}),{code:'D03_SEGMENT_DUPLICATE_OWNER'});
});
test('D03: cannot promote source document ownership to operational truth',()=>{
 const x=load();x.editorial_promotion=true;
 assert.throws(()=>validateD03DistributedSegments({overrides:{[path]:x}}),{code:'D03_SEGMENT_OWNER_OR_AUTHORITY'});
});
test('D03: cannot silently replace a source locator',()=>{
 const x=load();x.document_refs[0].source_sections_or_fields[0].line_start=999;
 assert.throws(()=>validateD03DistributedSegments({overrides:{[path]:x}}),{code:'D03_SEGMENT_MISMATCH'});
});
