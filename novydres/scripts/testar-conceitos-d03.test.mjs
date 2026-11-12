import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {validateAtlasConcepts} from './verificar-conceitos-d03.mjs';
const file='novydres/cenario/lugares/poi-01/conteudo.json';
const get=()=>JSON.parse(readFileSync(file,'utf8'));
test('D03: 41 distinct source-grounded places preserve both Atlas variants',()=>{
 const v=validateAtlasConcepts();
 assert.deepEqual([v.concepts,v.districts,v.places,v.exact_source_sections],[41,9,32,82]);
 assert.equal(v.editorial_selection,false);
});
test('D03: a source section cannot become an unapproved confirmed fact',()=>{
 const x=get();x.epistemic_status='CONFIRMED';
 assert.throws(()=>validateAtlasConcepts({overrides:{[file]:x}}),{code:'D03_ATLAS_AUTHORITY_PROMOTION'});
});
test('D03: cannot drop a competing historical Atlas variant',()=>{
 const x=get();x.source_variants.pop();
 assert.throws(()=>validateAtlasConcepts({overrides:{[file]:x}}),{code:'D03_ATLAS_VARIANT_LOSS'});
});
test('D03: source section mismatch cannot be masked by a correct source SHA',()=>{
 const x=get();x.source_variants[0].text+='invented';
 assert.throws(()=>validateAtlasConcepts({overrides:{[file]:x}}),{code:'D03_ATLAS_LITERAL_MISMATCH'});
});
