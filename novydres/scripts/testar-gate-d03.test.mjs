import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {checkD03Gate} from './verificar-gate-d03.mjs';
const read=p=>JSON.parse(readFileSync(p,'utf8'));
test('D03 complete source equivalence and owner graph without semantic fact promotion',()=>{
 const result=checkD03Gate();
 assert.deepEqual([result.source_origins,result.source_locators,result.candidate_subjects],[64,1707,59]);
 assert.equal(result.graph_active_dangling_refs,0);
 assert.equal(result.source_publication_refs_deferred,64);
 assert.equal(result.epistemic_promotion,false);
});
test('D03 cannot silently treat later handoff reports as direct source-editor approvals',()=>{
 const world=read('novydres/fontes/originais/migration/WORLD_AUTHORITY_MATRIX_V1.json');
 world.chapters[0].promotion_verdict_directly_audited=true;
 assert.throws(()=>checkD03Gate({worldAuthorityOverride:world}),{code:'D03_GATE_EDITORIAL_PROMOTION'});
});
test('D03 cannot fabricate an active dependency in candidate catalog',()=>{
 const cat=read('novydres/catalogo.json');
 cat.subjects[0].dependencies.push('invented-subject-without-owner');
 assert.throws(()=>checkD03Gate({catalogOverride:cat}),{code:'D03_GATE_DANGLING_ACTIVE_SUBJECT'});
});
test('D03 cannot select an unresolved global NPC historical variant',()=>{
 const npc=read('novydres/world/organizations/npc-sources/MADAME_ZOYA_V09_VARIANT_AUDIT_VERIFIED_V2.json');
 npc.independent_editorial_verdict='APPROVED_BY_INFERENCE';
 assert.throws(()=>checkD03Gate({npcAuditOverride:npc}),{code:'D03_GATE_EDITORIAL_PROMOTION'});
});
