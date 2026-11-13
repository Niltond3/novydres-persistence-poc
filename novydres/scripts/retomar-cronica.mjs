// D05 candidate reader of CHR-001 C45 by exact snapshot and subject, not a runtime activation.
import {execFileSync} from 'node:child_process';
import {buildCatalog,checkCatalog,readSelected} from './catalogo-assuntos.mjs';
import {verifyD04State} from './verificar-estado-d04.mjs';
import {verifyMechanics} from './verificar-mecanica-c45.mjs';
import {verifyHistoryBatches} from './verificar-lotes-historicos-d04.mjs';
const err=code=>{const e=new Error(code);e.code=code;throw e;};
const obj=(root,catalog,id,path,sha,role)=>JSON.parse(readSelected(root,catalog,id,{
 snapshot_sha:sha,role,selected_paths:[path]
}).files[0].text);
export function readC45Candidate({root=process.cwd(),snapshot_sha,role=null,confirmed_write=null,actor_id=null,history_batch=null}={}){
 if(!/^[a-f0-9]{40}$/.test(snapshot_sha||''))err('SNAPSHOT_REQUIRED');
 const head=execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim();
 if(head!==snapshot_sha)err('HEAD_DIFFERENT');
 if(role===null||role===undefined)err('ROLE_NOT_AUTHORIZED');
 if(!['AUDITOR','DRAMATURGO','NARRADOR'].includes(role))err('DISCLOSURE_DENIED');
 if(confirmed_write && (confirmed_write.status!=='CONFIRMED'||confirmed_write.snapshot_sha!==head||confirmed_write.readback!==true))err('PENDING_PERSISTENCE');
 checkCatalog(root);
 const c=buildCatalog(root);
 const s=obj(root,c,'chr001-state-checkpoint','novydres/cronicas/CHR-001/estado/recuperacao-c45.json',head,role);
 const t=obj(root,c,'chr001-open-threads-versions','novydres/cronicas/CHR-001/tramas/abertas/atual-c45.json',head,role);
 const last=obj(root,c,'chr001-episode-m302','novydres/cronicas/CHR-001/episodios/m302/fatos-c45.json',head,role);
 const story=obj(root,c,'chr001-runtime-story-architecture','novydres/cronicas/CHR-001/documentos/proveniencia-arquitetura/autoridade-c45.json',head,role);
 const mechanics=obj(root,c,'chr001-table-config','novydres/cronicas/CHR-001/configuracao/mecanica-c45.json',head,role);
 const hist=obj(root,c,'chr001-historic-history-index','novydres/cronicas/CHR-001/historico/history-index/lotes-c45.json',head,role);
 const checked=verifyD04State(),checkedMechanics=verifyMechanics(),checkedHistory=verifyHistoryBatches();
 if(!checked.ok||!checkedMechanics.ok||!checkedHistory.ok||s.operational!==false||s.cursor.last_event_id!==t.last_event_id||t.threads.length!==44)err('C45_RECOVERY_NOT_VERIFIED');
 if(last.last_event_id!==s.cursor.last_event_id || last.scene?.status!=='CLOSED'||last.scene?.last_event_id!==s.cursor.last_event_id||last.scene_starts_created!==0 || last.generated_transcript!==false)err('C45_SCENE_FACT_DRIFT');
 if(mechanics.application?.target_future_disciplines_unavailable_before_embrace!==true||mechanics.authority?.no_runtime_activation!==true||
    mechanics.current?.resources?.xp_spent!==s.resources.xp_spent)err('C45_MECHANICS_UNAPPROVED');
 if(story.c45_authority?.candidate_runtime_activation!==false||story.c45_authority?.last_confirmed_event_id!==s.cursor.last_event_id||story.boundaries?.gm_hidden_player_disclosure!==false||story.boundaries?.preparation_is_not_played_event!==true)err('C45_STORY_AUTHORITY_NOT_RECONCILED');
 if(s.cursor.status!=='READY_FOR_NARRATOR'||s.cursor.next_role!=='NARRADOR'||s.cursor.next_scene!=='C02'||
    last.scene?.next_scene_requires!=='DRAMATURGO'||story.c45_authority?.source_narrator_permission!==true||
    story.c45_authority?.source_narrator_prompt_required!==true)err('C45_HANDOFF_PRECEDENCE_DRIFT');
 const actorSubjects=c.subjects.filter(x=>x.id.startsWith('chr001-knowledge-npc-'));
 if(actorSubjects.length!==38)err('C45_ACTOR_SCOPE_INCOMPLETE');
 if(hist.last_event_id!==s.cursor.last_event_id||
    hist.index_coverage!=='PARTIAL_SPARSE_NEEDS_COMPLETE_HISTORY_AUDIT'||
    hist.source_rows?.length!==27)err('C45_HISTORY_SOURCE_UNRECONCILED');
 let selectedHistory=null;
 if(history_batch!==null){
   if(!Number.isInteger(history_batch)||history_batch<1||history_batch>27)err('HISTORY_BATCH_NOT_FOUND');
   selectedHistory=hist.source_rows[history_batch-1];
   if(selectedHistory.ordinal!==history_batch||selectedHistory.not_automatic_fact_authority!==true)
     err('C45_HISTORY_SOURCE_UNRECONCILED');
 }
 let actor=null;
 if(actor_id!==null){
  if(!/^[a-z][a-z0-9-]*$/.test(actor_id))err('NOT_FOUND');
  const id='chr001-knowledge-'+actor_id;
  const target=actorSubjects.find(x=>x.id===id);
  if(!target)err('NOT_FOUND');
  actor=obj(root,c,id,target.path+'/conhecimento.json',head,role);
  if(actor.actor_id!==actor_id||!Array.isArray(actor.records)||actor.no_player_disclosure!==true)err('ACTOR_SCOPE_INVALID');
 }
 return {status:'CANDIDATE_NON_OPERATIONAL',snapshot_sha:head,source_commit:s.source_commit,
  cursor:s.cursor,resources:s.resources,last_scene:last.scene,actor_subjects:actorSubjects.length,open_threads:t.threads.length,
  handoff:{historical_close_gate:last.scene.next_scene_requires,current_cycle_status:s.cursor.status,
   next_role:s.cursor.next_role,player_narrator_prompt_required:story.c45_authority.source_narrator_prompt_required,
   candidate_runtime_activation:false},
  actor,history_batch:selectedHistory,historical_index_coverage:'PARTIAL_SOURCE_BACKED_27_BATCHES',story_authority:{activation:'SOURCE_V004_V018_BASE_V019_PROSPECTIVE',candidate_runtime_activation:false},
  local_mechanics:{source:'DEC-CR-019_TARGET_V2_PROVISIONAL_ONLY',grapple_bonus_dice:1,future_powers_active:false},write_authorized:false,next:'E02_SPECIFIC_APPROVAL_REQUIRED'};
}
if(process.argv[1]?.endsWith('/retomar-cronica.mjs'))
 console.log(JSON.stringify(readC45Candidate({snapshot_sha:execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim(),role:'AUDITOR'})));
