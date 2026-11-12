import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyWorldLinks} from './verificar-vinculos-d03.mjs';
const doc=()=>JSON.parse(readFileSync('novydres/sistema/arquitetura/fase-d/vinculos-literais-d03.json','utf8'));
test('D03 all 84 world reference occurrences are pinned, scoped and nonpromoted',()=>{
 const x=verifyWorldLinks();assert.equal(x.ok,true);assert.equal(x.links,84);assert.equal(x.owner_resolved,11);assert.equal(x.deferred,73);
});
test('D03 prevents source citation being silently transformed into semantic relationship',()=>{
 const d=doc();d.links[0].semantic_relation_confirmed=true;
 assert.throws(()=>verifyWorldLinks(process.cwd(),d),{code:'D03_LINK_TRUTH_OR_DISCLOSURE_PROMOTION'});
});
test('D03 refuses unresolved source citation assigned fabricated target',()=>{
 const d=doc();const x=d.links.find(x=>x.target_subject_id===null);x.target_subject_id='npc-not-in-repository';
 assert.throws(()=>verifyWorldLinks(process.cwd(),d),{code:'D03_LINK_SILENT_RESOLUTION'});
});
test('D03 rejects changed source citation anchor',()=>{
 const d=doc();d.links[0].location.line=999999;
 assert.throws(()=>verifyWorldLinks(process.cwd(),d),{code:'D03_LINK_LINE_NOT_FOUND'});
});
