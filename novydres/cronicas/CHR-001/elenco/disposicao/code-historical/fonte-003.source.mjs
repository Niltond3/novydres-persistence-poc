// CHR-001 regression suite. Node >=18: node --test <path>.
import test from 'node:test';
import assert from 'node:assert/strict';
import {twoD3Mood,secureTwoD3,startMoodWindow,calculate,addPressure,resolvePressure,updateBaseline,evaluate} from './EVALUATOR_V1.mjs';
import {validateState} from './VALIDATOR_V1.mjs';
import path from 'node:path';
import fs from 'node:fs';
import os from 'node:os';
const evt='CHR001-M204-C14-24-20261105-001';
const pressure=(id,delta,source_event_id)=>({id,delta,reason:'Impacto realmente narrado',source_event_id});
const rel=()=>({baseline:3,source_event_id:evt,pressures:[]});
test('T01: d3-d3 yields triangular -2..2 distribution',()=>{
 const counts=new Map();
 for(let a=1;a<=3;a++)for(let b=1;b<=3;b++){const v=twoD3Mood(a,b);counts.set(v,(counts.get(v)||0)+1);}
 assert.deepEqual([...counts.entries()].sort((a,b)=>a[0]-b[0]),[[-2,1],[-1,2],[0,3],[1,2],[2,1]]);
});
test('T02: Mary -2 +3 = +1',()=>assert.equal(calculate({mood:-2,baseline:3}).score,1));
test('T03: pressures -2 then -1 produce -1 then -2',()=>{
 let r=addPressure(rel(),pressure('wait',-2,'E-WAIT'));
 assert.equal(calculate({mood:-2,baseline:r.baseline,pressures:r.pressures}).score,-1);
 r=addPressure(r,pressure('reserve',-1,'E-RESERVE'));
 assert.equal(calculate({mood:-2,baseline:r.baseline,pressures:r.pressures}).score,-2);
});
test('T04: same mood but stranger baseline 0 = -2; distinct relationships',()=>assert.equal(calculate({mood:-2,baseline:0}).score,-2));
test('T05: clipping does not exceed -5..+5',()=>{
 assert.equal(calculate({mood:2,baseline:3,pressures:[pressure('a',2,'Ea')]}).score,5);
 assert.equal(calculate({mood:-2,baseline:-3,pressures:[pressure('b',-2,'Eb')]}).score,-5);
});
test('T06: duplicate pressure event/id rejected',()=>{
 const r=addPressure(rel(),pressure('a',-1,'SOURCE1'));
 assert.throws(()=>addPressure(r,pressure('b',-1,'SOURCE1')),/NPC_DISPOSITION_BLOCK/);
 assert.throws(()=>addPressure(r,pressure('a',-1,'SOURCE2')),/NPC_DISPOSITION_BLOCK/);
});
test('T07: pressure overflow requires review',()=>{
 let r=rel();
 for(let i=0;i<3;i++)r=addPressure(r,pressure('p'+i,-1,'E'+i));
 assert.throws(()=>addPressure(r,pressure('p3',-1,'E3')),/review required/);
});
test('T08: cannot silently clear pressure; requires event',()=>{
 const r=addPressure(rel(),pressure('x',-1,'E1'));
 assert.throws(()=>resolvePressure(r,'x',''),/real source event/);
 assert.equal(resolvePressure(r,'x','E2').pressures.length,0);
 assert.equal(r.pressures.length,1);
});
test('T09: baseline moves only with evidence',()=>{
 assert.throws(()=>updateBaseline(rel(),-2,''),/source event/);
 assert.equal(updateBaseline(rel(),-1,'E3').baseline,-1);
});
test('T10: same window reused, no reroll across chats',()=>{
 const w=startMoodWindow(null,{period_key:'period@C14',period_anchor_event_id:evt,method:'TWO_D3_RECORDED',dice:[1,3],rng_provenance:'MOCK_TEST'});
 const w2=startMoodWindow(w,{period_key:'period@C14',period_anchor_event_id:evt,method:'TWO_D3_RECORDED',dice:[3,1],rng_provenance:'MOCK_TEST'});
 assert.equal(w2.value,-2);
 assert.notEqual(w,w2);
});
test('T11: without verifiable RNG neutral fallback contains no fictional cause',()=>{
 const w=startMoodWindow(null,{period_key:'new',period_anchor_event_id:evt});
 assert.equal(w.value,0);assert.equal(w.method,'NEUTRAL_FALLBACK');assert.equal(w.source_event_id,null);
 assert.throws(()=>startMoodWindow(null,{period_key:'new',period_anchor_event_id:evt,method:'CONTEXT',value:-2}),/source event/);
});
test('T12: dice mismatch and absent provenance rejected',()=>{
 assert.throws(()=>startMoodWindow(null,{period_key:'new',period_anchor_event_id:evt,method:'TWO_D3_RECORDED',dice:[1,3]}),/RNG origin/);
 assert.throws(()=>startMoodWindow(null,{period_key:'new',period_anchor_event_id:evt,method:'TWO_D3_RECORDED',dice:[1,3],value:2,rng_provenance:'MOCK_TEST'}),/mismatch/);
});
test('T13: strong resistance/high receptivity never overrides boundaries or grants dice',()=>{
 const actor={profile:{negative_expression:'calma e firme',positive_expression:'afeto sem ceder',boundaries:[{rule:'não usar reservas',source_event_id:evt}]},
 relationships:{'pc-bartholomeu-krauser':rel()},mood_window:{period_key:'t',value:2}};
 const st={chronicle_id:'CHR-001',status:'ACTIVE',actors:{'npc-mary-krauser':actor}};
 const x=evaluate(st,{npc_id:'npc-mary-krauser',interlocutor_id:'pc-bartholomeu-krauser',period_key:'t'});
 assert.equal(x.score,5);assert.deepEqual(x.boundaries,['não usar reservas']);assert.equal(x.mechanical_bonus,0);
 assert.throws(()=>evaluate({...st,status:'STAGED'},{npc_id:'npc-mary-krauser',interlocutor_id:'pc-bartholomeu-krauser',period_key:'t'}),/not activated/);
});
test('T14: missing NPC/profile and stale period never fabricate a mood',()=>{
 const st={chronicle_id:'CHR-001',status:'ACTIVE',actors:{'npc-mary-krauser':{profile:{negative_expression:'x',positive_expression:'y',boundaries:[]},relationships:{},mood_window:{period_key:'old',value:-2}}}};
 const e=evaluate(st,{npc_id:'npc-mary-krauser',interlocutor_id:'npc-someone',period_key:'new'});
 assert.equal(e.score,0);assert.equal(e.requires_mood,true);assert.equal(e.relationship_unrecorded,true);
 assert.equal(evaluate(st,{npc_id:'npc-new',interlocutor_id:'pc-bartholomeu-krauser',period_key:'new'}).requires_profile,true);
});
test('T15: secure RNG returns valid d3 faces, no fabricated fixed output',()=>{
 const r=secureTwoD3();assert.equal(r.value,r.dice[0]-r.dice[1]);assert.equal(r.rng_provenance,'NODE_CRYPTO_RANDOMINT');
});
test('T16: real STAGED snapshot validates without altering cycle',()=>{
 const root=path.resolve(new URL('../../../../',import.meta.url).pathname);
 // import.meta URL at .../novydres/chronicles/CHR-001/npc-disposition/, four parents => repo root
 const p='novydres/chronicles/CHR-001/npc-disposition/STATE_V001.json';
 assert.equal(validateState(root,p).status,'STAGED');
});
