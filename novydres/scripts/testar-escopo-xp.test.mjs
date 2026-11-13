import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {verifyXP} from './verificar-escopo-xp.mjs';
const read=p=>JSON.parse(readFileSync(p,'utf8'));
const local=()=>read('novydres/cronicas/CHR-001/estado/xp-autoridade-c45.json');
const common=()=>read('novydres/sistema/regras/experiencia/principios-credito.json');
test('XP current 675/270/405/0 retains historical 170 and no credit promotion',()=>{
 const v=verifyXP();assert.equal(v.ok,true);assert.equal(v.records,8);
 assert.deepEqual(v.current,{xp_total:675,xp_spent:270,xp_remaining:405,xp_credit_available:0});
});
test('XP fail-closed on invented credit, stale balance or mistaken global 675',()=>{
 const x=local();x.current.xp_spent=170;
 assert.throws(()=>verifyXP({localOverride:x}),{code:'D04_XP_STATE_DRIFT'});
 const y=local();y.local_credit_rule.once_per_distinct_act=false;
 assert.throws(()=>verifyXP({localOverride:y}),{code:'D04_XP_UNAUTHORIZED_CREDIT'});
 const z=common();z.scope_disclaimer='ALL V5 MUST HAVE CAP 675';
 assert.throws(()=>verifyXP({globalOverride:z}),{code:'D03_GLOBAL_LOCAL_XP_PROMOTION'});
});
