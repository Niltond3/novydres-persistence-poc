import test from 'node:test';
import assert from 'node:assert/strict';
import {evaluate,calculate,startMoodWindow} from './EVALUATOR_V2.mjs';
const mk=(baseline=0)=>({chronicle_id:'CHR-001',status:'ACTIVE',actors:{A:{profile:{personal_goal:'Proteger seu emprego',negative_expression:'corta conversa',positive_expression:'pode escutar',boundaries:[{rule:'Não liberar trabalho inseguro'}]},relationships:{PC:{baseline,pressures:[]}},mood_window:null}}});
const args={npc_id:'A',interlocutor_id:'PC',period_key:'late-70s-day-1'};
const withMood=(st,value)=>{st.actors.A.mood_window=startMoodWindow(null,{period_key:args.period_key,period_anchor_event_id:'EVENT-001',method:'CONTEXT',value,source_event_id:'EVENT-001'});return st;};
test('v3-01 unprofiled NPC is unknown, not automatically pleasant zero',()=>{
 const out=evaluate({chronicle_id:'CHR-001',status:'ACTIVE',actors:{}},args);
 assert.equal(out.profile_missing,true);assert.equal(out.score,null);assert.equal(out.expression,null);assert.equal(out.mechanical_bonus,0);
});
test('v3-02 unrolled mood blocks expression even with friendly +3 bond',()=>{
 const out=evaluate(mk(3),args);assert.equal(out.requires_mood,true);assert.equal(out.expression_mode,'PENDING_MOOD');assert.equal(out.expression,null);
});
test('v3-03 neutral score 0 chooses neither POSITIVE nor NEGATIVE',()=>{
 const out=evaluate(withMood(mk(),0),args);assert.equal(out.score,0);assert.equal(out.expression_mode,'NEUTRAL_ROLE_DRIVEN');assert.equal(out.expression,null);
});
test('v3-04 -1 and +1 remain role-driven neutral',()=>{
 for(const val of [-1,1]){const out=evaluate(withMood(mk(),val),args);assert.equal(out.expression_mode,'NEUTRAL_ROLE_DRIVEN');assert.equal(out.expression,null);}
});
test('v3-05 negative and positive expressions require actual signed band',()=>{
 const a=evaluate(withMood(mk(),-2),args),b=evaluate(withMood(mk(),2),args);
 assert.equal(a.expression_mode,'NEGATIVE');assert.equal(a.expression,'corta conversa');
 assert.equal(b.expression_mode,'POSITIVE');assert.equal(b.expression,'pode escutar');
});
test('v3-06 positive relationship is not authorization to violate job rules',()=>{
 const out=evaluate(withMood(mk(3),0),args);assert.equal(out.score,3);
 assert.equal(out.decision_not_determined,true);assert.deepEqual(out.boundaries,['Não liberar trabalho inseguro']);assert.equal(out.mechanical_bonus,0);
});
test('v3-07 two d3 relationship formula unchanged',()=>{
 assert.equal(calculate({mood:-2,baseline:3}).score,1);
 assert.equal(calculate({mood:2,baseline:-3}).score,-1);
});
test('v3-08 invalid scope blocks',()=>assert.throws(()=>evaluate({chronicle_id:'OTHER',status:'ACTIVE',actors:{}},args)));
