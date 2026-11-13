import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyStoryAuthority} from './verificar-autoridade-c45.mjs';
const p='novydres/cronicas/CHR-001/documentos/proveniencia-arquitetura/autoridade-c45.json';
const src=()=>JSON.parse(readFileSync(p,'utf8'));
test('D04 distinguishes active V018 authorization from C45 prospective V019 successor',()=>{
 const a=verifyStoryAuthority();assert.equal(a.ok,true);assert.equal(a.source_pins,6);
 assert.equal(a.candidate_runtime_activation,false);assert.equal(a.gm_disclosure,false);
});
test('D04 rejects unpinned story-source substitution and runtime promotion',()=>{
 const a=src();a.source_refs.find(x=>x.id.endsWith('V019_GM_HIDDEN.md')).sha='0'.repeat(40);
 assert.throws(()=>verifyStoryAuthority({override:a}),{code:'D04_STORY_BLOB_DRIFT'});
 const b=src();b.c45_authority.candidate_runtime_activation=true;
 assert.throws(()=>verifyStoryAuthority({override:b}),{code:'D04_STORY_UNAUTHORIZED_PROMOTION'});
 const c=src();c.boundaries.gm_hidden_player_disclosure=true;
 assert.throws(()=>verifyStoryAuthority({override:c}),{code:'D04_STORY_UNAUTHORIZED_PROMOTION'});
});
