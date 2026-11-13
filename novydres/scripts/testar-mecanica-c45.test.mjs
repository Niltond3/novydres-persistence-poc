import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyMechanics} from './verificar-mecanica-c45.mjs';
const file='novydres/cronicas/CHR-001/configuracao/mecanica-c45.json';
const clone=()=>JSON.parse(readFileSync(file,'utf8'));
test('C45 provisional mechanic is source-backed and not a bought target',()=>{
 const x=verifyMechanics();assert.equal(x.ok,true);
 assert.equal(x.local_bonus_dice,1);assert.equal(x.auto_xp_awards,0);
 assert.equal(x.future_powers_active,false);
});
test('No silent specialization, future discipline or XP from a temporary target',()=>{
 const a=clone();a.application.grapple_provisional_bonus_dice=2;
 assert.throws(()=>verifyMechanics({override:a}),{code:'D04_MECHANICS_UNAUTHORIZED_RULE'});
 const b=clone();b.application.target_future_disciplines_unavailable_before_embrace=false;
 assert.throws(()=>verifyMechanics({override:b}),{code:'D04_MECHANICS_UNAUTHORIZED_RULE'});
 const c=clone();c.source_distinctions.allocated_actual.skills.Briga=5;
 assert.throws(()=>verifyMechanics({override:c}),{code:'D04_MECHANICS_ACTUAL_VS_PROVISIONAL_DRIFT'});
 const d=clone();d.current.resources.xp_spent++;
 assert.throws(()=>verifyMechanics({override:d}),{code:'D04_MECHANICS_RESOURCE_MISMATCH'});
});
