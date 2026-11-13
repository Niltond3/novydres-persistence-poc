#!/usr/bin/env node
// CHR-001 local semantic validator. Node >=18, stdlib, sem mutações.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import process from 'node:process';
const BASE='novydres/chronicles/CHR-001/npc-disposition/';
const fail=(why)=>{throw Error('NPC_DISPOSITION_INVALID: '+why);};
const check=(v,why)=>{if(!v)fail(why);};
const HEX=/^[0-9a-f]{40}$/;
const REF=/^(pc|npc)-[a-z0-9-]+$/;
export const gitBlobSha=bytes=>{const b=Buffer.isBuffer(bytes)?bytes:Buffer.from(bytes,'utf8');return crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');};
function safe(root,repoPath){
 check(typeof repoPath==='string'&&!repoPath.includes('..')&&!repoPath.includes('\\')&&!path.isAbsolute(repoPath),'unsafe path');
 const target=path.resolve(root,repoPath);check(target.startsWith(path.resolve(root)+path.sep),'path outside root');return target;
}
const load=(root,p)=>fs.readFileSync(safe(root,p));
const json=(root,p)=>JSON.parse(load(root,p).toString('utf8'));
const str=(s)=>typeof s==='string'&&s.trim().length>0;
const integer=(v,min,max)=>Number.isInteger(v)&&v>=min&&v<=max;
const exact=(obj,keys,label)=>{check(obj&&typeof obj==='object'&&!Array.isArray(obj),label+' not object');check(Object.keys(obj).sort().join('|')===keys.slice().sort().join('|'),label+' unexpected/missing keys');};
export function discoverLatestState(root){
 const names=fs.readdirSync(safe(root,BASE.slice(0,-1))).map(n=>/^STATE_V(\d{3})\.json$/.exec(n)).filter(Boolean).map(m=>+m[1]).sort((a,b)=>a-b);
 check(names.length&&names[0]===1,'state sequence start missing');
 for(let i=1;i<names.length;i++)check(names[i]===names[i-1]+1,'state sequence gap');
 return BASE+'STATE_V'+String(names.at(-1)).padStart(3,'0')+'.json';
}
export function validateState(root,statePath,{livePath=null}={}){
 check(new RegExp('^'+BASE+'STATE_V[0-9]{3}\\.json$').test(statePath),'invalid state path');
 const s=json(root,statePath);
 exact(s,['schema_id','chronicle_id','status','checkpoint','previous_version','activation_event_id','actors'],'state');
 check(s.schema_id==='CHR001_NPC_DISPOSITION_STATE_V1'&&s.chronicle_id==='CHR-001','wrong scope/schema');
 check(['STAGED','ACTIVE'].includes(s.status),'wrong status');
 exact(s.checkpoint,['source_head_sha','cycle_path','cycle_blob_sha','last_event_id'],'checkpoint');
 check(HEX.test(s.checkpoint.source_head_sha)&&HEX.test(s.checkpoint.cycle_blob_sha)&&str(s.checkpoint.last_event_id),'missing checkpoint SHA/event');
 check(/^novydres\/chronicles\/CHR-001\/orchestration\/CYCLE_V[0-9]{4}\.json$/.test(s.checkpoint.cycle_path),'invalid anchor cycle');
 check(gitBlobSha(load(root,s.checkpoint.cycle_path))===s.checkpoint.cycle_blob_sha,'anchor cycle blob mismatch');
 const cycle=json(root,s.checkpoint.cycle_path);
 check(cycle.checkpoint?.last_event_id===s.checkpoint.last_event_id,'anchor event mismatch');
 if(s.previous_version!==null){
   check(/^novydres\/chronicles\/CHR-001\/npc-disposition\/STATE_V[0-9]{3}\.json$/.test(s.previous_version),'bad predecessor path');
   check(s.previous_version!==statePath,'self-predecessor');
   const prior=json(root,s.previous_version);
   check(prior.chronicle_id==='CHR-001'&&prior.schema_id===s.schema_id,'predecessor scope mismatch');
 }
 for(const [id,a]of Object.entries(s.actors)){
  check(/^npc-[a-z0-9-]+$/.test(id),'bad npc ID');
  exact(a,['profile','relationships','mood_window'],'actor '+id);
  exact(a.profile,['personal_goal','negative_expression','positive_expression','boundaries'],'profile '+id);
  for(const k of ['personal_goal','negative_expression','positive_expression'])check(str(a.profile[k]),'blank profile '+k);
  check(Array.isArray(a.profile.boundaries),'bad boundaries');
  for(const b of a.profile.boundaries){exact(b,['rule','source_event_id'],'boundary');check(str(b.rule)&&str(b.source_event_id),'boundary without evidence');}
  for(const [partner,rel]of Object.entries(a.relationships)){
   check(REF.test(partner),'bad interlocutor');
   exact(rel,['baseline','source_event_id','pressures'],'relationship');
   check(integer(rel.baseline,-3,3)&&str(rel.source_event_id),'bad baseline/evidence');
   check(Array.isArray(rel.pressures)&&rel.pressures.length<=3,'pressure overflow');
   const ids=new Set(),sources=new Set();
   for(const pr of rel.pressures){
     exact(pr,['id','delta','reason','source_event_id'],'pressure');
     check(str(pr.id)&&str(pr.reason)&&str(pr.source_event_id)&&integer(pr.delta,-2,2)&&pr.delta!==0,'invalid pressure');
     check(!ids.has(pr.id)&&!sources.has(pr.source_event_id),'duplicate pressure');ids.add(pr.id);sources.add(pr.source_event_id);
   }
  }
  if(a.mood_window!==null){
   const w=a.mood_window;exact(w,['period_key','period_anchor_event_id','value','method','dice','source_event_id','rng_provenance'],'mood');
   check(str(w.period_key)&&str(w.period_anchor_event_id)&&integer(w.value,-2,2),'bad mood/window');
   if(w.method==='TWO_D3_RECORDED'){check(Array.isArray(w.dice)&&w.dice.length===2&&w.dice.every(n=>integer(n,1,3))&&w.value===w.dice[0]-w.dice[1]&&str(w.rng_provenance)&&w.source_event_id===null,'dice mismatch');}
   else if(w.method==='CONTEXT'){check(w.dice===null&&w.rng_provenance===null&&str(w.source_event_id),'context source missing');}
   else if(w.method==='NEUTRAL_FALLBACK'){check(w.dice===null&&w.value===0&&w.source_event_id===null&&w.rng_provenance===null,'false neutral provenance');}
   else fail('unknown mood method');
  }
 }
 if(s.status==='STAGED')check(s.activation_event_id===null,'staged cannot imply activation');
 if(s.status==='ACTIVE'){
   check(str(s.activation_event_id),'active needs real activation marker');
   check(str(livePath),'active validator requires LIVE path');
   const live=json(root,livePath);
   const ref=live.npc_disposition_state_ref;
   check(ref?.path===statePath&&HEX.test(ref.blob_sha)&&ref.blob_sha===gitBlobSha(load(root,statePath)),'LIVE does not point to active social state SHA');
 }
 return {ok:true,status:s.status,actors:Object.keys(s.actors).length,path:statePath};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){
 try{
  const arg=k=>{let i=process.argv.indexOf(k);return i<0?null:process.argv[i+1];};
  const root=path.resolve(arg('--root')||process.cwd());
  console.log(JSON.stringify(validateState(root,arg('--state')||discoverLatestState(root),{livePath:arg('--live')})));
 }catch(err){console.error(String(err));process.exitCode=1;}
}
