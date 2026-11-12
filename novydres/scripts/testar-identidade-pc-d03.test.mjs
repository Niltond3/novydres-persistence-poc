import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyD03PC} from './verificar-identidade-pc-d03.mjs';
const p='novydres/personagens/pc-bartholomeu-krauser/perfil.json';
test('D03 approved PC name is global, but campaign state remains local and nonpromoted',()=>{
 const r=verifyD03PC();assert.equal(r.ok,true);assert.equal(r.local_state_promoted,false);
 assert.equal(r.deferred_reference_resolved,true);
});
test('D03 cannot turn approved TARGET attributes into purchased global traits',()=>{
 const v=JSON.parse(readFileSync(p,'utf8'));v.character_sheet_or_xp_copied=true;
 assert.throws(()=>verifyD03PC({profileOverride:v}),{code:'D03_PC_IDENTITY_AUTHORITY'});
});
test('D03 cannot replace the approved identity spelling by inference',()=>{
 const v=JSON.parse(readFileSync(p,'utf8'));v.identity_name.value='invented';
 assert.throws(()=>verifyD03PC({profileOverride:v}),{code:'D03_PC_IDENTITY_AUTHORITY'});
});
