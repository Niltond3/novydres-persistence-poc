import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {validateActivation} from './VALIDATOR_V2.mjs';
import {evaluate,calculate} from './EVALUATOR_V1.mjs';
const root=path.resolve(new URL('../../../../',import.meta.url).pathname);
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const b='novydres/chronicles/CHR-001/npc-disposition/';
test('C15-01 sidecar preserves cycle LIVE and verifies blob SHAs',()=>{
 const v=validateActivation(root);assert.equal(v.ok,true);assert.equal(v.scene,'C15');assert.equal(v.npc_count,4);
});
test('C15-02 only administrative activation, no retroactive mood or relationship delta',()=>{
 const a=read(b+'STATE_V002.json'),s=read(b+'STATE_V001.json');
 assert.equal(a.status,'ACTIVE');
 assert.equal(a.activation_event_id,'CHR001-ADMIN-C15-20261106-001');
 assert.deepEqual(a.checkpoint,s.checkpoint);assert.deepEqual(a.actors,s.actors);
 for(const actor of Object.values(a.actors))assert.equal(actor.mood_window,null);
});
test('C15-03 a +3 bond is not automatic assent or mechanical bonus',()=>{
 const s=read(b+'STATE_V002.json');
 const r=evaluate(s,{npc_id:'npc-mary-krauser',interlocutor_id:'pc-bartholomeu-krauser',period_key:'C15-UNSET'});
 assert.equal(r.score,3);assert.equal(r.requires_mood,true);
 assert.ok(r.boundaries.length>0);assert.equal(r.mechanical_bonus,0);
 assert.equal(calculate({mood:-2,baseline:3}).score,1);
});
