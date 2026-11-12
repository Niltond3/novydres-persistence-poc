import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyGlobalRelationships} from './verificar-relacoes-globais-d03.mjs';
const path='novydres/personagens/npc-iskander-yasupov/vinculos.json';
const copy=()=>JSON.parse(readFileSync(path,'utf8'));
test('D03 preserves five global source relations, with owner, direction and provenance',()=>{
 const x=verifyGlobalRelationships();
 assert.deepEqual([x.directed_edges,x.linked_to_existing_subjects,x.source_only_unknown_targets],[5,3,2]);
});
test('D03 rejects false global relation truth promotion',()=>{
 const x=copy();x.relations[0].epistemic_status='CONFIRMED';
 assert.throws(()=>verifyGlobalRelationships({overrides:{[path]:x}}),{code:'D03_GLOBAL_RELATION_OWNER'});
});
test('D03 rejects invented target subject',()=>{
 const x=copy();x.relations[0].to_subject_id='invented';
 assert.throws(()=>verifyGlobalRelationships({overrides:{[path]:x}}),{code:'D03_GLOBAL_RELATION_TARGET'});
});
test('D03 rejects lost variant provenance',()=>{
 const x=copy();x.relations[0].source_evidence=[];
 assert.throws(()=>verifyGlobalRelationships({overrides:{[path]:x}}),{code:'D03_GLOBAL_RELATION_SOURCE_LOSS'});
});
