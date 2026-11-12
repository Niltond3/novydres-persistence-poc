// ADR-001 C04 — scoped recovery of an existing candidate state, never runtime.
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {readFileSync} from 'node:fs';
import {buildCatalog,checkCatalog,readSelected} from './catalogo-assuntos.mjs';
import {validateShape} from './validar-assuntos.mjs';

const STATE='novydres/cronicas/CHR-001/estado/atual.json';
const STORY='novydres/cronicas/CHR-001/historias/m301-c01/historia.json';
const PLOT='novydres/cronicas/CHR-001/tramas/contato-condicional-samir/trama.json';
const KNOWLEDGE='novydres/cronicas/CHR-001/elenco/npc-samir-haddad/conhecimento.json';
const SHA=/^[a-f0-9]{40}$/;
const STATUS='CANDIDATE_HISTORICAL_ONLY';
const error=(code,detail='')=>{const err=new Error(code+(detail?': '+detail:''));err.code=code;throw err;};
const blobSha=buffer=>createHash('sha1').update('blob '+buffer.length+'\0').update(buffer).digest('hex');
const git=(root,args,encoding='utf8')=>execFileSync('git',args,{cwd:root,encoding,stdio:['ignore','pipe','ignore']});
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const expectedResourceKeys=['xp_total','xp_spent','xp_remaining','xp_credit_available',
  'willpower_provisional_max','willpower_superficial_damage',
  'willpower_aggravated_damage','willpower_available'];

function pinnedFile(root,commit,path,sha) {
  if(!SHA.test(commit||'')||!/^[a-f0-9]{40}$/.test(sha||''))error('SOURCE_PIN_MISSING');
  if(!path||path.startsWith('/')||path.split('/').includes('..')||path.includes('\\'))error('SOURCE_PATH_INVALID');
  let bytes;
  try{bytes=git(root,['show',commit+':'+path],null);}
  catch{error('SOURCE_NOT_FOUND',path);}
  if(blobSha(bytes)!==sha)error('SOURCE_HASH_MISMATCH',path);
  return bytes;
}
const loadFromCandidate=(root,catalog,id,path,snapshot)=>JSON.parse(readSelected(root,catalog,id,{
  snapshot_sha:snapshot,role:'AUDITOR',selected_paths:[path]
}).files[0].text);
const need=(condition,code)=>{if(!condition)error(code);};

/**
 * Return a small, reference-only snapshot for an authorized migration review.
 * Does not narrate, manufacture pending intention, read master HEAD as truth,
 * or rebuild state by replay of hypothetical events.
 */
export function inspectCandidateResume(root=process.cwd(),{
  snapshot_sha,
  expected_head=snapshot_sha,
  mode='HISTORICAL_C41',
  overrides={},
  confirmed_write=null
}={}) {
  if(!SHA.test(snapshot_sha||'')||!SHA.test(expected_head||''))error('SNAPSHOT_REQUIRED');
  const checkout=git(root,['rev-parse','HEAD']).trim();
  if(checkout!==snapshot_sha||checkout!==expected_head)error('HEAD_DIFFERENT');
  if(mode!=='HISTORICAL_C41')error('CANDIDATE_NOT_OPERATIONAL');
  checkCatalog(root);
  const catalog=buildCatalog(root);
  const read=(id,path)=>Object.hasOwn(overrides,path)?structuredClone(overrides[path]):
    loadFromCandidate(root,catalog,id,path,snapshot_sha);
  const state=read('chr001-state-checkpoint',STATE);
  const story=read('story-m301-c01',STORY);
  const plot=read('plot-contato-condicional-samir',PLOT);
  const knowledge=read('chr001-npc-samir-haddad',KNOWLEDGE);

  const schema=JSON.parse(readFileSync(resolve(root,
    'novydres/sistema/arquitetura/fase-a/schemas/checkpoint-candidate.schema.json'),'utf8'));
  if(validateShape(state,schema).length)error('CHECKPOINT_SCHEMA');
  need(state.subject_id==='chr001-state-checkpoint'&&state.not_operational===true,'CANDIDATE_NOT_OPERATIONAL');
  need(SHA.test(state.source_commit||''),'SOURCE_PIN_MISSING');
  if(confirmed_write&&confirmed_write.status!=='CONFIRMED')error('PENDING_PERSISTENCE');
  if(confirmed_write&&
      (confirmed_write.snapshot_sha!==snapshot_sha||confirmed_write.readback!==true))
      error('PENDING_PERSISTENCE');
  need(state.cycle?.path&&state.cycle?.sha&&state.source_live?.path&&state.source_live?.sha,'SOURCE_PIN_MISSING');
  const cycle=JSON.parse(pinnedFile(root,state.source_commit,state.cycle.path,state.cycle.sha));
  const live=JSON.parse(pinnedFile(root,state.source_commit,state.source_live.path,state.source_live.sha));
  const primary=story.primary_literal;
  need(primary?.source_commit===state.source_commit,'HISTORICAL_SOURCE_MIX');
  const sourceText=pinnedFile(root,primary.source_commit,primary.path,primary.sha).toString('utf8');
  need(story.subject_id==='story-m301-c01'&&story.scene_closed===true,'STORY_SCOPE_MISMATCH');
  need(knowledge.subject_id==='chr001-npc-samir-haddad'&&knowledge.claims_are_not_world_facts===true,
    'EPISTEMIC_CONFLICT');
  need(Array.isArray(knowledge.unknown)&&knowledge.unknown.length>0 &&
       Array.isArray(knowledge.claims)&&Array.isArray(knowledge.confirmed),'EPISTEMIC_CONFLICT');
  need(plot.subject_id==='plot-contato-condicional-samir'&&
       plot.future_contact_realized===false&&plot.pc_obligation_created===false,
       'FUTURE_EVENT_INVENTED');
  need(story.pc_action_boundaries?.no_future_call_confirmed===true&&
       story.pc_action_boundaries?.handshake_reply_unconfirmed===true,'PLAYER_AGENCY_VIOLATION');
  need(story.technical_ledger_proven===false,'TECHNICAL_LEDGER_INVENTED');
  need(story.event_text_markers?.length===8&&
       new Set(story.event_text_markers.map(x=>x.event_marker)).size===8,'LITERAL_MARKER_MISMATCH');
  need(story.event_text_markers.every(x=>x.scene_marker&&sourceText.includes(x.scene_marker)),
       'LITERAL_MARKER_MISMATCH');

  const rc=state.resources,rl=live.character?.resources;
  need(rc&&rl&&expectedResourceKeys.every(k=>Number.isInteger(rc[k])&&rc[k]>=0),
       'RESOURCE_INVALID');
  need(rc.xp_total-rc.xp_spent===rc.xp_remaining,'RESOURCE_MISMATCH');
  need(rc.willpower_provisional_max-rc.willpower_superficial_damage-
    rc.willpower_aggravated_damage===rc.willpower_available,'RESOURCE_MISMATCH');
  need(rc.xp_credit_available===0,'UNPROVEN_SPENDABLE_CREDIT');
  need(expectedResourceKeys.every(k=>rc[k]===rl[k]),'HISTORICAL_RESOURCE_DRIFT');
  need(eq(state.workshop,live.character?.current_mortal_workshop),'MATERIAL_EFFECT_DRIFT');

  const c=state.checkpoint,source=cycle.checkpoint;
  need(state.cycle.id===cycle.cycle_id&&cycle.provocation_id===c.provocation,
       'CYCLE_MISMATCH');
  need(c.status===cycle.status&&c.next_role===cycle.next_role,'CYCLE_MISMATCH');
  for(const field of ['last_event_id','last_closed_scene','next_scene','next_scene_status',
    'mortal','embrace_occurred'])
    need(c[field]===source[field],'CURSOR_DRIFT');
  need(c.scene_started===false&&cycle.scene_frame?.scene_started===false,'SCENE_ALREADY_STARTED');
  need(source.pending_persistence===false,'PENDING_PERSISTENCE');
  need(c.mortal===true&&c.embrace_occurred===false,'FUTURE_STATE_INVENTED');
  need(c.next_scene_status==='NOT_STARTED'&&cycle.pending_player_decision===null,
       'PLAYER_INTENT_INVENTED');
  need(state.cursor_resolution==='VALIDATED_C41_OVER_HISTORICAL_LIVE_FIELD_NO_REWRITE'&&
       state.historical_live_cursor!==c.provocation,'HISTORICAL_CURSOR_UNDECLARED');
  need(state.no_technical_replay===true,'REPLAY_REQUIREMENT_REINTRODUCED');
  need(state.manifest_ref?.path===cycle.manifest_ref?.path&&
    state.manifest_ref?.blob_sha===cycle.manifest_ref?.blob_sha,'MANIFEST_PIN_MISMATCH');

  // Resolve source pin, not current master. Source excerpt supports a historical
  // locator but cannot establish semantic facts without contextual review.
  return {status:STATUS,snapshot_sha,source_commit:state.source_commit,
    state_subject_id:state.subject_id,checkpoint:{
      provocation:c.provocation,last_closed_scene:c.last_closed_scene,
      next_scene:c.next_scene,next_scene_status:c.next_scene_status,
      scene_started:c.scene_started,player_decision_pending:false,
      last_event_id:c.last_event_id,mortal:c.mortal,embrace_occurred:c.embrace_occurred
    },resources:{...rc},last_material_effect_source_event:state.workshop.source_event_id,
    known_actor_subject_id:knowledge.subject_id,
    actor_knowledge_scope:knowledge.scope,actor_claims_status:'NPC_CLAIM_NOT_WORLD_FACT',
    historical_literal:{path:primary.path,source_commit:primary.source_commit,blob_sha:primary.sha,
      marker_count:story.event_text_markers.length},
    source_pins:[{path:state.cycle.path,sha:state.cycle.sha},
      {path:state.source_live.path,sha:state.source_live.sha}],
    unresolved:{external_relations:'DEFERRED_C41',civil_date:'UNKNOWN',
      next_contact:'UNKNOWN',historical_cursor_drift:'DECLARED_C41_NOT_C45'},
    publication:{state:'NOT_OPERATIONAL',authority:'CANDIDATE_ONLY'},
    next_action:'MIGRATION_REVIEW_ONLY_NO_SCENE'};
}
export function continuationDecision({expected_head,actual_head,commit_sha,
  verified_blobs=false,transaction_status='PENDING_PERSISTENCE',evidence=null}={}) {
  if(!SHA.test(expected_head||'')||!SHA.test(actual_head||''))return 'RECOVERY_FAILED';
  if(expected_head!==actual_head)return 'HEAD_DIFFERENT';
  if(transaction_status==='CONFIRMED'&&commit_sha===actual_head&&verified_blobs===true&&
    evidence?.commit_sha===actual_head&&evidence?.readback===true)return 'SNAPSHOT_SYNCED';
  if(transaction_status==='STOP_CONFLICT')return 'STOP_CONFLICT';
  return 'PENDING_PERSISTENCE';
}
if(process.argv[1]&&resolve(process.argv[1])===resolve(new URL(import.meta.url).pathname)) {
  const out=inspectCandidateResume(process.cwd(),{snapshot_sha:git(process.cwd(),['rev-parse','HEAD']).trim()});
  console.log(JSON.stringify({status:out.status,snapshot_sha:out.snapshot_sha,
    source_commit:out.source_commit,subject_id:out.state_subject_id,
    scope:out.next_action,resources_verified:true,literal_marker_count:out.historical_literal.marker_count}));
}
