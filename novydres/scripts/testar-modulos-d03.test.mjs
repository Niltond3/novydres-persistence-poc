import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyD03RuleModules} from './verificar-modulos-d03.mjs';
const path='novydres/sistema/regras/criacao-de-personagens/integration/conteudo.json';
const doc=()=>JSON.parse(readFileSync(path,'utf8'));
test('D03 32 creation/rule docs have one of 20 module owners; 6 executable consumers deferred D05',()=>{
 const r=verifyD03RuleModules();
 assert.deepEqual([r.modules,r.source_documents,r.d05_consumer_handoffs],[20,32,6]);
 assert.ok(r.source_field_or_section_locators>300);
});
test('D03 cannot elevate a source doc to active system rule via module pointer',()=>{
 const x=doc();x.current_system_rule_active=true;
 assert.throws(()=>verifyD03RuleModules({overrides:{[path]:x}}),{code:'D03_RULE_MODULE_AUTHORITY'});
});
test('D03 rejects loss of source semantic owner',()=>{
 const x=doc();x.source_records[0].semantic_owner='other-owner';
 assert.throws(()=>verifyD03RuleModules({overrides:{[path]:x}}),{code:'D03_RULE_MODULE_OWNER_OR_SOURCE'});
});
test('D03 rejects source locator truncation',()=>{
 const x=doc();x.source_records[0].section_or_field_locators=[];
 assert.throws(()=>verifyD03RuleModules({overrides:{[path]:x}}),{code:'D03_RULE_MODULE_FRAGMENT_MISMATCH'});
});
