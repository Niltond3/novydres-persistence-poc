// CHR-001 — EVALUATOR V2. V1 mood math retained; neutral ≠ friendliness.
// COW prospective; no action, V5 dice bonus, relationship change or fact generation.
import {clamp,twoD3Mood,secureTwoD3,startMoodWindow,addPressure,resolvePressure,updateBaseline,calculate} from './EVALUATOR_V1.mjs';
export {clamp,twoD3Mood,secureTwoD3,startMoodWindow,addPressure,resolvePressure,updateBaseline,calculate};
const fail = msg=>{throw new Error('NPC_DISPOSITION_V2_BLOCK: '+msg);};
export function evaluate(state,{npc_id,interlocutor_id,period_key}) {
  if(state?.chronicle_id!=='CHR-001'||state?.status!=='ACTIVE') fail('state scope or activation');
  if(![npc_id,interlocutor_id,period_key].every(x=>typeof x==='string'&&x.trim())) fail('identity and diegetic period required');
  const a=state.actors?.[npc_id];
  const common={npc_id,interlocutor_id,period_key,mechanical_bonus:0,decision_not_determined:true,
    preflight:['NPC_GOAL','AUTHORITY','COST_OF_CONSENT','BOUNDARIES','KNOWLEDGE','MOOD','RELATIONSHIP']};
  if(!a)return {...common,profile_missing:true,requires_profile:true,requires_mood:true,score:null,band:'UNPROFILED_UNKNOWN',
    expression:null,expression_mode:'ROLE_CONTEXT_REQUIRED',boundaries:[],personal_goal:null,no_default_courtesy:true};
  const rel=a.relationships?.[interlocutor_id]??null,win=a.mood_window?.period_key===period_key?a.mood_window:null;
  // A missing window is not silently equivalent to a chosen neutral mood.
  const provisional=calculate({mood:win?.value??0,baseline:rel?.baseline??0,pressures:rel?.pressures??[]});
  const mode=!win?'PENDING_MOOD':provisional.score<=-2?'NEGATIVE':provisional.score>=2?'POSITIVE':'NEUTRAL_ROLE_DRIVEN';
  const expression=mode==='NEGATIVE'?a.profile?.negative_expression??null:mode==='POSITIVE'?a.profile?.positive_expression??null:
    mode==='NEUTRAL_ROLE_DRIVEN'?a.profile?.neutral_expression??null:null;
  return {...common,...provisional,profile_missing:false,requires_profile:false,relationship_unrecorded:!rel,requires_mood:!win,
    score_confirmed:!!win,mood_window_method:win?.method??'NOT_RESOLVED',expression_mode:mode,expression,
    personal_goal:a.profile?.personal_goal??null,boundaries:(a.profile?.boundaries??[]).map(b=>b.rule),
    disposition_is_not_compliance:true,no_default_courtesy:true,no_assumption_npc_is_happy:true};
}
