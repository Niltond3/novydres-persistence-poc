// NOVYDRES CHR-001 / structural regressions. Run:
// node --test novydres/runtime/orchestration/ORCHESTRATION_TESTS_V1.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {gitBlobSha,validateCycle,discoverLatest} from './ORCHESTRATION_VALIDATOR_V1.mjs';
const DIR='novydres/chronicles/CHR-001/orchestration';
function put(root,p,content) {
  const dest=path.join(root,p);
  fs.mkdirSync(path.dirname(dest),{recursive:true});
  const text=typeof content==='string'?content:JSON.stringify(content,null,2)+'\n';
  fs.writeFileSync(dest,text,'utf8');
  return {path:p,blob_sha:gitBlobSha(text)};
}
function sample(t){
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'novydres-cycle-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const refs={};
  const files={
    live:{last_confirmed_event_id:'E09',stage:{embrace_occurred:false}},
    history_index:{last_event_id:'E09'},
    episode:'C09 closed E09',
    character:'XP 170; FV 1/6',
    knowledge:'knowledge',
    threads:'open threads'
  };
  for(const [name,value] of Object.entries(files))refs[name]=put(root,'novydres/chronicles/CHR-001/'+name+'.json',value);
  const dossier=put(root,'novydres/chronicles/CHR-001/preparations/M2.04_DOSSIER_V1.json',{status:'OLD'});
  put(root,'novydres/MANIFEST_V30.json',{orchestration:true});
  const c={
    schema_id:'NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V1',
    cycle_id:'CHR001-CYCLE-0001',sequence:1,chronicle_id:'CHR-001',provocation_id:'M2.04',
    manifest_path:'novydres/MANIFEST_V30.json',source_head_sha:'a'.repeat(40),previous_cycle:null,
    transition:'BOOTSTRAP',status:'READY_FOR_DRAMATURGO',next_role:'DRAMATURGO',
    checkpoint:{last_event_id:'E09',last_closed_scene:'C09',next_scene:'C10',next_scene_status:'NOT_STARTED',
      pending_persistence:false,mortal:true,embrace_occurred:false},
    refs,plan:{preparation_id:'PREP-1',dossier,sidecar:null,validity:'STALE',reviewed_against_event_id:null},
    review:{decision:'NOT_REVIEWED',against_last_event_id:null,public_rationale:null},
    blocking:{code:'STALE_PLAN_REVIEW',reason:'C09 changed the plan'},
    guards:{no_story_delta_in_prep:true,no_xp_fv_delta_in_prep:true,g28_scene_only:true,
      frozen_unchanged:true,no_public_spoilers:true}
  };
  const p=DIR+'/CYCLE_V0001.json';
  const ref=put(root,p,c);
  return {root,c,p,ref};
}
function next(f,transition='PLAN_REVALIDATED'){
  const c=structuredClone(f.c);
  c.sequence=2;c.cycle_id='CHR001-CYCLE-0002';
  c.previous_cycle=f.ref;c.transition=transition;c.status='READY_FOR_NARRATOR';c.next_role='NARRADOR';
  c.plan.validity=transition==='PLAN_REVISED'?'REVISED':'VALIDATED';
  c.plan.reviewed_against_event_id='E09';
  c.review={decision:transition==='PLAN_REVISED'?'REVISED':'REVALIDATED',
    against_last_event_id:'E09',
    public_rationale:'Reavaliada a provocação inteira: escolhas, ritmo, atos e horizonte de 2010.'};
  c.blocking={code:null,reason:null};
  if(transition==='PLAN_REVISED'){
    c.plan.preparation_id='PREP-2';
    c.plan.dossier=put(f.root,'novydres/chronicles/CHR-001/preparations/M2.04_DOSSIER_V2.json',{status:'PROSPECTIVE_ONLY'});
  }
  const p=DIR+'/CYCLE_V0002.json';
  put(f.root,p,c);
  return {c,p};
}
test('T01 / bootstrap READY_FOR_DRAMATURGO is valid; C10 cannot start',t=>{
 const f=sample(t);assert.equal(validateCycle(f.root,f.p).role,'DRAMATURGO');
 assert.equal(discoverLatest(f.root),f.p);
});
test('T02 / reviewer can validate unchanged plan, no dossier rewrite',t=>{
 const f=sample(t),n=next(f);assert.equal(validateCycle(f.root,n.p).role,'NARRADOR');
 assert.equal(n.c.plan.dossier.blob_sha,f.c.plan.dossier.blob_sha);
});
test('T03 / revised plan changes only dossier and permits narrator',t=>{
 const f=sample(t),n=next(f,'PLAN_REVISED');
 assert.equal(validateCycle(f.root,n.p).role,'NARRADOR');
});
test('T04 / narrator cannot run on stale plan without fresh review',t=>{
 const f=sample(t),n=next(f);n.c.plan.reviewed_against_event_id='E08';
 put(f.root,n.p,n.c);assert.throws(()=>validateCycle(f.root,n.p),/ORCHESTRATION_BLOCK/);
});
test('T05 / no fabricated XP or FV by Dramaturgo',t=>{
 const f=sample(t),n=next(f);
 n.c.refs.character=put(f.root,'novydres/chronicles/CHR-001/character_new.json','XP 999');
 put(f.root,n.p,n.c);assert.throws(()=>validateCycle(f.root,n.p),/Dramaturgo changed narrative source/);
});
test('T06 / G26 buffer blocks transfer',t=>{
 const f=sample(t);f.c.checkpoint.pending_persistence=true;
 put(f.root,f.p,f.c);assert.throws(()=>validateCycle(f.root,f.p),/PENDING_PERSISTENCE/);
});
test('T07 / tampered LIVE blob SHA blocks handoff',t=>{
 const f=sample(t);put(f.root,f.c.refs.live.path,{last_confirmed_event_id:'E10',stage:{embrace_occurred:false}});
 assert.throws(()=>validateCycle(f.root,f.p),/SHA mismatch/);
});
test('T08 / improper previous-cycle SHA blocks',t=>{
 const f=sample(t),n=next(f);n.c.previous_cycle.blob_sha='0'.repeat(40);
 put(f.root,n.p,n.c);assert.throws(()=>validateCycle(f.root,n.p),/SHA mismatch/);
});
test('T09 / skip a cycle number blocks discovery',t=>{
 const f=sample(t);put(f.root,DIR+'/CYCLE_V0003.json',f.c);
 assert.throws(()=>discoverLatest(f.root),/missing cycle/);
});
test('T10 / valid scene commit returns to Dramaturgo exactly once',t=>{
 const f=sample(t),n=next(f);
 const s=structuredClone(n.c);
 s.sequence=3;s.cycle_id='CHR001-CYCLE-0003';
 s.previous_cycle=put(f.root,n.p,n.c);
 s.transition='SCENE_COMMITTED';s.status='READY_FOR_DRAMATURGO';s.next_role='DRAMATURGO';
 s.checkpoint.last_event_id='E10';s.checkpoint.last_closed_scene='C10';s.checkpoint.next_scene='C11';
 s.refs.episode=put(f.root,'novydres/chronicles/CHR-001/episode_new.json','C10 closed E10');
 s.refs.live=put(f.root,'novydres/chronicles/CHR-001/live_new.json',{last_confirmed_event_id:'E10',stage:{embrace_occurred:false}});
 s.plan.validity='STALE';s.plan.reviewed_against_event_id=null;
 s.review={decision:'NOT_REVIEWED',against_last_event_id:null,public_rationale:null};
 s.blocking={code:'NEEDS_DRAMATURGO_REVIEW',reason:'C10 completed'};
 const p=DIR+'/CYCLE_V0003.json';put(f.root,p,s);
 assert.equal(validateCycle(f.root,p).role,'DRAMATURGO');
});
test('T11 / scene commit without new event is blocked',t=>{
 const f=sample(t),n=next(f);
 const s=structuredClone(n.c);s.sequence=3;s.cycle_id='CHR001-CYCLE-0003';
 s.previous_cycle=put(f.root,n.p,n.c);
 s.transition='SCENE_COMMITTED';s.status='READY_FOR_DRAMATURGO';s.next_role='DRAMATURGO';
 s.plan.validity='STALE';s.review={decision:'NOT_REVIEWED',against_last_event_id:null,public_rationale:null};
 s.blocking={code:'NEEDS_DRAMATURGO_REVIEW',reason:'C10 completed'};
 const p=DIR+'/CYCLE_V0003.json';put(f.root,p,s);
 assert.throws(()=>validateCycle(f.root,p),/wrong scene closed|scene lacks new event/);
});
test('T12 / narrator cannot revise dossier during G28',t=>{
 const f=sample(t),n=next(f);
 const s=structuredClone(n.c);s.sequence=3;s.cycle_id='CHR001-CYCLE-0003';
 s.previous_cycle=put(f.root,n.p,n.c);
 s.transition='SCENE_COMMITTED';s.status='READY_FOR_DRAMATURGO';s.next_role='DRAMATURGO';
 s.checkpoint.last_event_id='E10';s.checkpoint.last_closed_scene='C10';s.checkpoint.next_scene='C11';
 s.refs.episode=put(f.root,'novydres/chronicles/CHR-001/episode_new.json','C10 closed E10');
 s.refs.live=put(f.root,'novydres/chronicles/CHR-001/live_new.json',{last_confirmed_event_id:'E10',stage:{embrace_occurred:false}});
 s.plan.validity='STALE';s.plan.dossier=put(f.root,'novydres/chronicles/CHR-001/preparations/rogue.json','roteiro adulterado');
 s.review={decision:'NOT_REVIEWED',against_last_event_id:null,public_rationale:null};
 s.blocking={code:'NEEDS_DRAMATURGO_REVIEW',reason:'C10 completed'};
 const p=DIR+'/CYCLE_V0003.json';put(f.root,p,s);
 assert.throws(()=>validateCycle(f.root,p),/Narrador altered a planned dossier/);
});
