import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { validateCandidates, validateShape } from './validar-assuntos.mjs';

const prefix='novydres/cronicas/CHR-001/';
const global='novydres/personagens/npc-samir-haddad/assunto.json';
const plot=prefix+'tramas/contato-condicional-samir/assunto.json';
const local=prefix+'elenco/npc-samir-haddad/';
const state=prefix+'estado/atual.json';
const obj=p=>JSON.parse(readFileSync(p, 'utf8'));
const mutation=(path, change)=>{const copy=obj(path); change(copy); return validateCandidates(process.cwd(),{overrides:{[path]:copy}});};
const has=(r,code)=>r.errors.some(x=>x.code===code);
test('V01–V04: historical C41 subjects plus isolated table config, intact sources and deferred external target',()=>{
 const r=validateCandidates();
 assert.equal(r.ok,true,JSON.stringify(r.errors));
 assert.equal(r.subjects,15); // Six historical subjects plus nine D03 source portfolios
 assert.ok(r.checked>=10);
 assert.ok(r.deferred.some(x=>x.target==='pc-bartholomeu-krauser'));
});
test('V01 schema rejects missing type/status',()=>{
 const r=mutation(global,o=>{delete o.kind;});
 assert.ok(has(r,'V01_SCHEMA'));
});
test('V02 rejects casefold identity collision',()=>{
 const r=mutation(plot,o=>o.subject_id='npc-samir-haddad');
 assert.ok(has(r,'V02_COLLISION'));
});
test('V02 rejects ambiguous mixed-case ID',()=>{
 const r=mutation(global,o=>o.subject_id='NPC-Samir-Haddad');
 assert.ok(has(r,'V02_ID'));
});
test('V03 rejects missing source',()=>{
 const r=mutation(global,o=>o.source_refs[0].id='missing/provenance.json');
 assert.ok(has(r,'V03_SOURCE_MISSING'));
});
test('V03 rejects historical blob SHA substitution',()=>{
 const r=mutation(global,o=>o.source_refs[0].sha='0'.repeat(40));
 assert.ok(has(r,'V03_SOURCE_SHA'));
});
test('V03 rejects unresolved cross-subject IDs',()=>{
 const r=mutation(plot,o=>o.related_subject_ids.push('unregistered-target'));
 assert.ok(has(r,'V03_SUBJECT_REF'));
});
test('V04 rejects incorrect owner and silent activation',()=>{
 assert.ok(has(mutation(global,o=>o.owner_scope='novydres/cronicas'), 'V04_OWNER'));
 assert.ok(has(mutation(global,o=>o.status='ACTIVE'), 'V04_PROMOTION'));
});
test('V04 rejects knowledge claim promoted to fact',()=>{
 const path=local+'conhecimento.json';
 assert.ok(has(mutation(path,o=>o.claims_are_not_world_facts=false),'V04_CLAIM_PROMOTION'));
});
test('V04 rejects foreign relation owner',()=>{
 const path=local+'relacoes.json';
 assert.ok(has(mutation(path,o=>o.relations[0].owner_subject_id='other-owner'),'V04_RELATION_OWNER'));
});
test('V03 rejects unregistered target when explicit Phase B deferment is absent',()=>{
 const path=local+'relacoes.json';
 assert.ok(has(mutation(path,o=>o.external_target_id_not_migrated_in_phase_b=false),'V03_TARGET_NOT_FOUND'));
});
test('V04 rejects invented resource balances and future Embrace',()=>{
 assert.ok(has(mutation(state,o=>o.resources.xp_remaining+=1),'V04_RESOURCES'));
 assert.ok(has(mutation(state,o=>o.checkpoint.embrace_occurred=true),'V04_STATE'));
});
test('V01 optional record schema preserves DEC-23/24: no universal event ledger or roll faces',()=>{
 const schema=obj('novydres/sistema/arquitetura/fase-a/schemas/record-candidate.schema.json');
 const minimal={schema_version:'1.0',record_id:'correction-001',record_kind:'CORRECTION',owner_subject_id:'story-m301-c01',scope:'CHR-001',visibility:'SYSTEM_AUDIT',payload:{note:'explicit correction pending source review'}};
 assert.deepEqual(validateShape(minimal,schema),[]);
 assert.ok(validateShape({...minimal,record_kind:'ROLL_FACES'},schema).length>0);
});
