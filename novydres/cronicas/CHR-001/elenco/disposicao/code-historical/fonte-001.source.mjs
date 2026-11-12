// CHR-001, somente local. Node >=18, stdlib. Funções puras; nenhum fato é inventado.
import {randomInt} from 'node:crypto';
const fail=(message)=>{throw new Error('NPC_DISPOSITION_BLOCK: '+message);};
const asInt=(x,min,max,label)=>{if(!Number.isInteger(x)||x<min||x>max)fail(label+' outside '+min+'..'+max);return x;};
export const clamp=(value,min,max)=>Math.min(max,Math.max(min,value));
export function twoD3Mood(a,b){asInt(a,1,3,'first d3');asInt(b,1,3,'second d3');return a-b;}
export function secureTwoD3(){
  const dice=[randomInt(1,4),randomInt(1,4)];
  return {dice,value:twoD3Mood(...dice),rng_provenance:'NODE_CRYPTO_RANDOMINT'};
}
export function startMoodWindow(previous,{period_key,period_anchor_event_id,method='NEUTRAL_FALLBACK',dice=null,value=null,source_event_id=null,rng_provenance=null}){
  if(typeof period_key!=='string'||!period_key.trim()||typeof period_anchor_event_id!=='string'||!period_anchor_event_id.trim())fail('window requires grounded period and event');
  if(previous?.period_key===period_key)return structuredClone(previous); // mesmo período: não rerrolar
  let result=0;
  if(method==='TWO_D3_RECORDED'){
    if(!Array.isArray(dice)||dice.length!==2||!rng_provenance||!rng_provenance.trim())fail('recorded dice require RNG origin');
    result=twoD3Mood(...dice);
    if(value!==null&&value!==result)fail('dice/value mismatch');
    if(source_event_id!==null)fail('dice alone cannot claim diegetic causal event');
  }else if(method==='CONTEXT'){
    result=asInt(value,-2,2,'context mood');
    if(!source_event_id||!source_event_id.trim())fail('context mood requires source event');
    if(dice!==null||rng_provenance!==null)fail('context mood cannot claim dice');
  }else if(method==='NEUTRAL_FALLBACK'){
    if(dice!==null||value!==null||source_event_id!==null||rng_provenance!==null)fail('neutral fallback carries no invented evidence');
  }else fail('invalid mood method');
  return {period_key,period_anchor_event_id,value:result,method,dice:method==='TWO_D3_RECORDED'?[...dice]:null,source_event_id,rng_provenance};
}
export function addPressure(relationship,pressure){
  if(!relationship||!Array.isArray(relationship.pressures))fail('missing relationship');
  const {id,delta,reason,source_event_id}=pressure||{};
  asInt(delta,-2,2,'pressure delta');
  if(delta===0||![id,reason,source_event_id].every(v=>typeof v==='string'&&v.trim()))fail('pressure requires nonzero delta, id, reason and event source');
  if(relationship.pressures.some(p=>p.id===id||p.source_event_id===source_event_id))fail('duplicate pressure source/id');
  if(relationship.pressures.length>=3)fail('too many active pressures; review required');
  return {...relationship,pressures:[...relationship.pressures,structuredClone(pressure)]};
}
export function resolvePressure(relationship,id,resolution_event_id){
  if(!resolution_event_id||!resolution_event_id.trim())fail('resolution requires real source event');
  const next=relationship.pressures.filter(p=>p.id!==id);
  if(next.length===relationship.pressures.length)fail('pressure missing');
  return {...relationship,pressures:next}; // resolução no evento G28; não apagar história
}
export function updateBaseline(relationship,next,source_event_id){
  asInt(next,-3,3,'baseline');
  if(!source_event_id||!source_event_id.trim())fail('baseline change requires source event');
  return {...relationship,baseline:next,source_event_id};
}
export function calculate({mood,baseline,pressures=[]}){
  asInt(mood,-2,2,'mood');asInt(baseline,-3,3,'baseline');
  if(!Array.isArray(pressures)||pressures.length>3)fail('invalid pressure list');
  const seenIds=new Set(),seenEvents=new Set();
  let delta=0;
  for(const p of pressures){
    asInt(p.delta,-2,2,'pressure delta');
    if(p.delta===0||!p.id||!p.source_event_id||seenIds.has(p.id)||seenEvents.has(p.source_event_id))fail('invalid or duplicate pressure');
    seenIds.add(p.id);seenEvents.add(p.source_event_id);delta+=p.delta;
  }
  const relation=clamp(baseline+delta,-3,3),score=mood+relation;
  return {mood,baseline,pressure_total:delta,relation,score,band:score<=-4?'STRONGLY_RESISTANT':score<=-2?'LOW_RECEPTIVITY':score<=1?'MODERATE':score<=3?'RECEPTIVE':'HIGHLY_RECEPTIVE'};
}
export function evaluate(state,{npc_id,interlocutor_id,period_key}){
  if(state?.chronicle_id!=='CHR-001'||state?.status!=='ACTIVE')fail('module not activated');
  if(!npc_id||!interlocutor_id||!period_key)fail('interaction identity and period required');
  const actor=state.actors[npc_id];
  if(!actor)return {npc_id,interlocutor_id,profile_missing:true,score:0,requires_profile:true,requires_mood:true,mechanical_bonus:0};
  const rel=actor.relationships[interlocutor_id];
  const activeMood=actor.mood_window?.period_key===period_key?actor.mood_window:null;
  const r=calculate({mood:activeMood?.value??0,baseline:rel?.baseline??0,pressures:rel?.pressures??[]});
  return {...r,npc_id,interlocutor_id,profile_missing:false,requires_mood:!activeMood,relationship_unrecorded:!rel,
    expression:r.score<=-2?actor.profile.negative_expression:actor.profile.positive_expression,
    boundaries:actor.profile.boundaries.map(b=>b.rule),mechanical_bonus:0};
}
