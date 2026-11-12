#!/usr/bin/env node
// CHR-001 / ORCHESTRATION V3. Safe raw blob verification and closure administrative validator promotion.
// Legacy CYCLE_V0019/V0020 fail V1 administrative-pending validation; NOT erased.
// Validate HEAD-snapshot on checkout, blobs and live; never authorize Narrador on closure.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import process from 'node:process';
const DIR='novydres/chronicles/CHR-001/orchestration';
const RX=/^CYCLE_V(\d{4})\.json$/;
const HEX=/^[a-f0-9]{40}$/;
const fail=m=>{throw Error('ORCHESTRATION_V3_BLOCK: '+m)};
const check=(v,m)=>{if(!v)fail(m)};
const read=(root,p)=>{check(typeof p==='string'&&!p.includes('..')&&!p.includes('\\')&&!path.isAbsolute(p),'invalid path');const q=path.resolve(root,p);check(q.startsWith(path.resolve(root)+path.sep),'outside root');return fs.readFileSync(q)};
const json=(root,p)=>JSON.parse(read(root,p).toString('utf8'));
const sha=bytes=>crypto.createHash('sha1').update(Buffer.from('blob '+bytes.length+'\0')).update(bytes).digest('hex');
const verify=(root,r,label)=>{check(r&&HEX.test(r.blob_sha),'missing blob '+label);check(sha(read(root,r.path))===r.blob_sha,'blob mismatch '+label);return r.path.endsWith('.json')?json(root,r.path):null;};
export function validateTransitionV3(c,prev,live,prevLive,closure,manifest) {
  check(c?.sequence===prev?.sequence+1,'sequence');
  check(c.source_head_sha&&HEX.test(c.source_head_sha),'source head');
  check(c.previous_cycle&&prev.cycle_id===`CHR001-CYCLE-${String(prev.sequence).padStart(4,'0')}`,'predecessor');
  check(c.checkpoint?.last_event_id===live.last_confirmed_event_id,'LIVE and cycle event mismatch');
  check(c.checkpoint?.pending_persistence===false,'pending persistence');
  check(c.checkpoint?.next_scene_status==='NOT_STARTED','scene initiated without authority');
  check(c.checkpoint?.mortal===true&&c.checkpoint?.embrace_occurred===false,'unexpected Embrace in closure flow');
  if(c.transition==='MARCO_CLOSED'){
    check(prev.status==='PROVOCATION_CLOSURE_PENDING'&&prev.next_role==='NONE','closure requires pending provocation');
    check(c.status==='READY_FOR_DRAMATURGO'&&c.next_role==='DRAMATURGO','closing must handoff only to Dramaturgo');
    check(c.review?.decision==='NOT_REVIEWED'&&c.plan?.validity==='STALE','M3 preparation cannot be pre-validated');
    check(c.plan.dossier.path===prev.plan.dossier.path&&c.plan.dossier.blob_sha===prev.plan.dossier.blob_sha,'M3 dossier prematurely created');
    check(c.provocation_id===prev.provocation_id&&c.provocation_id==='M2.04','new provocation identifier created');
    check(c.checkpoint.last_event_id===prev.checkpoint.last_event_id&&live.last_confirmed_event_id===prevLive.last_confirmed_event_id,'invented narrative event');
    check(c.checkpoint.last_closed_scene==='C17'&&c.checkpoint.next_scene==='C18','M2 scene checkpoint changed');
    for(const k of ['episode','knowledge','threads'])check(c.refs[k].path===prev.refs[k].path&&c.refs[k].blob_sha===prev.refs[k].blob_sha,'historical source mutation '+k);
    check(closure?.status==='OFFICIALLY_CLOSED_BY_EXPLICIT_PLAYER_REQUEST'&&closure.scope?.M2==='CLOSED'&&closure.scope?.M2_04?.startsWith('CLOSED'),'closure source');
    check(closure.scope.M3==='NOT_STARTED'&&closure.future_scope.initial_provocation==='NOT_CREATED','M3 pre-generation');
    check(c.closure?.marco_closed==='M2'&&c.closure?.next_marco==='M3'&&c.closure?.initial_provocation_status==='NOT_CREATED','closure cycle marker');
    check(live.stage.M2==='CLOSED'&&live.stage.M2_04.startsWith('CLOSED')&&live.stage.M3==='NOT_STARTED'&&live.stage.M3_to_M5==='NOT_STARTED','LIVE closure markers');
    check(live.stage.embrace_occurred===false&&live.stage.main_chronicle_2010_started===false,'premature main chronicle');
    check(JSON.stringify(live.character.resources)===JSON.stringify(prevLive.character.resources),'XP/FV were altered during closure');
    check(JSON.stringify(live.character.allocated_attributes)===JSON.stringify(prevLive.character.allocated_attributes)&&JSON.stringify(live.character.allocated_skills)===JSON.stringify(prevLive.character.allocated_skills),'purchase sheet changed');
    check(live.character.roll_pool_basis_during_guided_creation===prevLive.character.roll_pool_basis_during_guided_creation,'target provisional rolls changed');
    check(c.blocking?.code==='M3_INITIAL_PROVOCATION_NOT_PREPARED'&&c.plan.reviewed_against_event_id===null,'no M3 dossier gate');
    check(manifest.runtime?.orchestration?.current_cycle===`${DIR}/CYCLE_V${String(c.sequence).padStart(4,'0')}.json`,'manifest cycle');
    check(manifest.runtime.orchestration.next_role==='DRAMATURGO'&&manifest.runtime.orchestration.next_scene_executable===false,'manifest allows scene');
    check(manifest.runtime?.civic_cultural_naming_lens_current?.path==='novydres/chronicles/CHR-001/world/CIVIC_CULTURAL_NAMING_LENS_V1.md','naming lens missing');
    return {ok:true,kind:'MARCO_CLOSED',marco:'M2',next_marco:'M3',initial_provocation:'NOT_CREATED',next_role:'DRAMATURGO'};
  }

  if(c.transition==='ADMIN_VALIDATOR_REVALIDATED'){
    check(prev.transition==='MARCO_CLOSED'&&prev.status==='READY_FOR_DRAMATURGO','admin revalidation requires approved M2 closure');
    check(c.status==='READY_FOR_DRAMATURGO'&&c.next_role==='DRAMATURGO','admin revalidation cannot release Narrador');
    check(c.review?.decision==='NOT_REVIEWED'&&c.plan?.validity==='STALE','M3 preplanning state altered');
    check(c.provocation_id==='M2.04'&&c.provocation_id===prev.provocation_id,'M3 first provocation generated without Dramaturgo');
    check(c.checkpoint.last_event_id===prev.checkpoint.last_event_id&&live.last_confirmed_event_id===prevLive.last_confirmed_event_id,'invented event on validator repair');
    check(c.checkpoint.last_closed_scene===prev.checkpoint.last_closed_scene&&c.checkpoint.next_scene===prev.checkpoint.next_scene,'closed M2 scene changed');
    check(c.closure?.path===prev.closure?.path&&c.closure?.blob_sha===prev.closure?.blob_sha,'changed Marco closure source');
    for(const k of ['live','history_index','episode','character','knowledge','threads'])
      check(c.refs[k].path===prev.refs[k].path&&c.refs[k].blob_sha===prev.refs[k].blob_sha,'changed stable source '+k);
    check(c.plan.dossier.path===prev.plan.dossier.path&&c.plan.dossier.blob_sha===prev.plan.dossier.blob_sha,'M3 dossier prematurely created');
    check(JSON.stringify(live.character.resources)===JSON.stringify(prevLive.character.resources),'XP/FV changed');
    check(live.stage.M2==='CLOSED'&&live.stage.M2_04.startsWith('CLOSED')&&live.stage.M3==='NOT_STARTED'&&live.stage.M3_to_M5==='NOT_STARTED','not actually M2 closed or M3 already started');
    check(live.stage.embrace_occurred===false,'premature Abraço');
    check(closure?.status==='OFFICIALLY_CLOSED_BY_EXPLICIT_PLAYER_REQUEST'&&closure.scope?.M2==='CLOSED'&&closure.scope.M3==='NOT_STARTED','Marco closure source no longer valid');
    check(c.closure.initial_provocation_status==='NOT_CREATED','M3 provocation unexpectedly created');
    check(c.blocking?.code==='M3_INITIAL_PROVOCATION_NOT_PREPARED','M3 planning gate removed');
    check(manifest.runtime?.orchestration?.current_cycle===`${DIR}/CYCLE_V${String(c.sequence).padStart(4,'0')}.json`,'manifest cycle mismatch');
    check(manifest.runtime.orchestration.next_role==='DRAMATURGO'&&manifest.runtime.orchestration.next_scene_executable===false,'manifest narrator accidentally released');
    check(manifest.runtime.orchestration.validator==='novydres/runtime/orchestration/ORCHESTRATION_VALIDATOR_V3.mjs','V3 validator not promoted');
    check(manifest.runtime?.civic_cultural_naming_lens_current?.path==='novydres/chronicles/CHR-001/world/CIVIC_CULTURAL_NAMING_LENS_V1.md','culture lens lost');
    return {ok:true,kind:'ADMIN_VALIDATOR_REVALIDATED',marco:'M2',next_marco:'M3',initial_provocation:'NOT_CREATED',next_role:'DRAMATURGO'};
  }
  if(['PLAN_REVISED','PLAN_REVALIDATED'].includes(c.transition)&&['MARCO_CLOSED','ADMIN_VALIDATOR_REVALIDATED'].includes(prev.transition)){
    check(c.status==='READY_FOR_NARRATOR'&&c.next_role==='NARRADOR','only valid future publication can release narrator');
    check(/^M3\.\d{2}$/.test(c.provocation_id),'not M3 first provocation');
    check(c.plan.validity==='REVISED'&&c.plan.dossier.blob_sha!==prev.plan.dossier.blob_sha,'fresh M3 dossier required');
    check(c.plan.reviewed_against_event_id===c.checkpoint.last_event_id&&c.review.against_last_event_id===c.checkpoint.last_event_id,'M3 plan review missing');
    check(c.checkpoint.last_event_id===prev.checkpoint.last_event_id,'M3 preparation generated story event');
    check(c.checkpoint.last_closed_scene==='C00'&&c.checkpoint.next_scene==='C01','M3 scene namespace must reset');
    for(const k of ['live','history_index','episode','character','knowledge','threads'])check(c.refs[k].blob_sha===prev.refs[k].blob_sha&&c.refs[k].path===prev.refs[k].path,'M3 preparation silently changed state '+k);
    check(c.blocking?.code===null&&c.blocking?.reason===null,'blocked narrator');
    return {ok:true,kind:'M3_FIRST_PLAN_PUBLISHED',next_role:'NARRADOR'};
  }
  fail('unsupported transition; do not bypass by old validator');
}
export function validateLatestV3(root=process.cwd()) {
  const list=fs.readdirSync(path.join(root,DIR)).map(x=>RX.exec(x)).filter(Boolean).map(x=>Number(x[1])).sort((a,b)=>a-b);
  check(list.length&&list[0]===1&&list.every((x,i)=>i===0||x===list[i-1]+1),'cycle sequence gap');
  const n=list.at(-1),name=x=>`${DIR}/CYCLE_V${String(x).padStart(4,'0')}.json`;
  const c=json(root,name(n)),prev=json(root,name(n-1));
  check(c.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V3','latest does not use V2 schema');
  check(c.previous_cycle?.path===name(n-1),'previous path');
  check(c.cycle_id===`CHR001-CYCLE-${String(n).padStart(4,'0')}`,'cycle id');
  verify(root,c.previous_cycle,'cycle predecessor');
  check(fs.existsSync(path.resolve(root,c.manifest_path)),'manifest missing');
  const manifest=json(root,c.manifest_path);
  for(const k of ['live','history_index','episode','character','knowledge','threads'])verify(root,c.refs[k],k);
  verify(root,c.plan.dossier,'dossier');
  if(c.plan.sidecar)verify(root,c.plan.sidecar,'sidecar');
  const live=json(root,c.refs.live.path),prevLive=json(root,prev.refs.live.path);
  let closure=null;
  if(['MARCO_CLOSED','ADMIN_VALIDATOR_REVALIDATED'].includes(c.transition)){
    check(c.closure&&c.closure.path==='novydres/chronicles/CHR-001/admin/M2_FORMAL_MARCO_CLOSURE_V1.json','closure ref');
    closure=verify(root,c.closure,'closure');
  }
  const r=validateTransitionV3(c,prev,live,prevLive,closure,manifest);
  return {...r,cycle_id:c.cycle_id,last_event_id:c.checkpoint.last_event_id};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){
  try{const i=process.argv.indexOf('--root');const root=path.resolve(i<0?process.cwd():process.argv[i+1]);console.log(JSON.stringify(validateLatestV3(root)));}
  catch(e){console.error(String(e));process.exitCode=1;}
}
