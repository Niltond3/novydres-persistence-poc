// D07 separate, fail-closed source/actor review. It does NOT certify narrative equivalence.
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {resolveSubject,buildCatalog} from './catalogo-assuntos.mjs';
const root='novydres/cronicas/CHR-001';
const source='c9fcfc0c558cd17d58ec8c8272da3ed70182ff37';
const err=c=>{const e=new Error(c);e.code=c;throw e;};
const git=(...a)=>execFileSync('git',a,{encoding:'utf8',maxBuffer:16*1024*1024}).trim();
const read=p=>JSON.parse(readFileSync(p,'utf8'));
const sourceJson=p=>JSON.parse(git('show',source+':'+p));
export function reviewD07({actorOverride=null,threadOverride=null,ledgerOverride=null,storyOverride=null,historyOverride=null}={}){
 const head=git('rev-parse','HEAD'),catalog=buildCatalog();
 const original=sourceJson('novydres/chronicles/CHR-001/knowledge/NPC_KNOWLEDGE_PROVENANCE_V22.json');
 const originalIndex=sourceJson('novydres/chronicles/CHR-001/HISTORY_INDEX_v039.json');
 const history=historyOverride||read(root+'/historico/history-index/lotes-c45.json');
 const batches=history.source_rows||[];
 if(history.subject_id!=='chr001-historic-history-index'||
    history.index_coverage!==originalIndex.index_coverage||
    history.last_event_id!==originalIndex.last_event_id||
    history.no_claim_of_complete_history_index!==true||
    batches.length!==originalIndex.history_batches.length||
    batches.length!==27||
    batches.some((r,i)=>r.ordinal!==i+1||
       r.original_path!==originalIndex.history_batches[i].path||
       r.episode_range!==originalIndex.history_batches[i].episode_range||
       r.provenance!==originalIndex.history_batches[i].provenance||
       r.candidate_sha!==r.original_sha||
       r.not_automatic_fact_authority!==true))
    err('D07_HISTORICAL_BATCH_MISMATCH');

 const authorial=storyOverride||read(root+'/documentos/proveniencia-arquitetura/autoridade-c45.json');
 const activation=sourceJson('novydres/runtime/narrative-architecture/program/deliverables/D07_ACTIVATION_V004_PLAYER_SAFE.json');
 const originalCycle=sourceJson('novydres/chronicles/CHR-001/orchestration/CYCLE_V0045.json');
 const A=authorial.source_refs||[];
 const get=(suffix)=>A.find(x=>x.id?.endsWith('/'+suffix));
 if(A.length!==6||authorial.subject_id!=='chr001-runtime-story-architecture'||
    authorial.visibility!=='SYSTEM_AUDIT'||
    authorial.c45_authority?.candidate_runtime_activation!==false||
    authorial.boundaries?.gm_hidden_player_disclosure!==false||
    authorial.boundaries?.V018_activation_record_not_silently_rewritten_to_V019!==true||
    activation.truth_package_ref?.blob_sha!=='537c4260c1d024cea144511596a9b54599b737b8'||
    originalCycle.activation.truth_package?.blob_sha!=='105e4fca581e10ce28d85133c40bd5237d68cfb4'||
    get('D07_STORY_TRUTH_PACKAGE_V018_GM_HIDDEN.md')?.sha!==activation.truth_package_ref.blob_sha||
    get('D07_STORY_TRUTH_PACKAGE_V019_GM_HIDDEN.md')?.sha!==originalCycle.activation.truth_package.blob_sha)
    err('D07_STORY_AUTHORITY_SOURCE_MISMATCH');

 const threads=sourceJson('novydres/chronicles/CHR-001/knowledge/OPEN_THREADS_V24.json');
 const xpEnv=sourceJson('novydres/runtime/xp/XP_ENVELOPE_V3.json');
 const xpLocal=read(root+'/estado/xp-autoridade-c45.json');
 const xpGlobal=read('novydres/sistema/regras/experiencia/principios-credito.json');
 if(xpEnv.current.xp_total!==675||xpEnv.current.xp_spent!==270||
    xpLocal.current.xp_total!==675||xpLocal.current.xp_spent!==270||
    xpLocal.current.xp_remaining!==405||xpLocal.current.xp_credit_available!==0||
    xpGlobal.local_owner_subject_id!=='chr001-state-checkpoint'||
    xpLocal.no_target_auto_purchase!==true||xpGlobal.operational_promotion!==false)
    err('D07_LOCAL_XP_SCOPE_OR_SOURCE_DRIFT');
 const live=sourceJson('novydres/chronicles/CHR-001/LIVE_v039.json');

 const originalMechanical=sourceJson('novydres/chronicles/CHR-001/character/MECHANICAL_GUIDED_CREATION_RULES_PROVENANCE_V3.json');
 const localMechanical=read(root+'/configuracao/mecanica-c45.json');
 if(localMechanical.subject_id!=='chr001-table-config'||
    localMechanical.authority?.no_runtime_activation!==true||
    JSON.stringify(localMechanical.source_distinctions)!==JSON.stringify(originalMechanical.distinctions)||
    localMechanical.application?.grapple_provisional_bonus_dice!==1||
    localMechanical.application?.target_dots_not_auto_purchased!==true||
    localMechanical.application?.target_future_disciplines_unavailable_before_embrace!==true||
    localMechanical.application?.historical_rolls_not_recomputed!==true)
    err('D07_PROVISIONAL_MECHANICS_AUTHORITY_DRIFT');

 const playedScene=read(root+'/episodios/m302/fatos-c45.json');
 if(playedScene.subject_id!=='chr001-episode-m302'||playedScene.visibility!=='SYSTEM_AUDIT'||
    playedScene.status!=='CANDIDATE_C45_FACT_PROJECTION_NOT_OPERATIONAL'||
    JSON.stringify(playedScene.scene)!==JSON.stringify(live.scene)||
    playedScene.last_event_id!==live.last_confirmed_event_id||playedScene.generated_transcript!==false)
    err('D07_SCENE_SEMANTIC_REWRITE');
 const out=threadOverride||read(root+'/tramas/abertas/atual-c45.json');
 const d05=ledgerOverride||read('novydres/sistema/arquitetura/fase-d/execucao-d05.json');
 const current=git('ls-tree','-r','--full-tree','HEAD').split('\n').filter(Boolean).map(x=>x.split('\t')[1]);
 if(current.some(p=>/^(?:novydres\/(?:runtime|chronicles|world|governance|systems|migration)\/|poc\/)/.test(p))||
    !['novydres/AGENTS.md','novydres/CONTEXT.md','novydres/catalogo.json'].every(p=>current.includes(p)))
    err('D07_OLD_ENTRY_OR_ROUTE');
 const recs=d05.source_records;
 if(recs?.length!==399||d05.source_count!==399||
    recs.filter(x=>x.retirement_method==='EXACT_INERT_SOURCE_BLOB_REHOMED').length!==285||
    recs.filter(x=>x.active_original_reference===true).length!==121||
    recs.some(x=>x.active_original_reference===true&&x.semantic_equivalence!=='NOT_YET_PROVEN'))
    err('D07_RUNTIME_SUCCESSION_NOT_PROVEN');

 if(out.subject_id!=='chr001-open-threads-versions'||out.visibility!=='SYSTEM_AUDIT'||
    JSON.stringify(out.threads)!==JSON.stringify(threads.threads)||out.last_event_id!==threads.last_event_id)
    err('D07_THREADS_SEMANTIC_REWRITE');
 const actorSubjects=catalog.subjects.filter(s=>s.id.startsWith('chr001-knowledge-npc-'));
 if(actorSubjects.length!==38)err('D07_ACTOR_COUNT');
 const covered=new Set();
 for(const s of actorSubjects){
   if(s.visibility!=='SYSTEM_AUDIT'||s.source_ids.length)err('D07_PRIVACY_METADATA');
   const a=actorOverride&&actorOverride.id===s.id?actorOverride.doc:read(s.path+'/conhecimento.json');
   if(a.subject_id!==s.id||a.actor_id!=='npc-'+s.id.slice('chr001-knowledge-npc-'.length)||
      a.no_player_disclosure!==true||a.no_global_fact_promotion!==true)err('D07_ACTOR_SCOPE');
   for(const item of a.records||[]){
     const i=item.source_row_index;
     if(covered.has(i)||!Number.isInteger(i)||i<0||i>=original.records.length||
       original.records[i].entity!==a.actor_id||
       JSON.stringify(original.records[i])!==JSON.stringify(item.record))err('D07_ACTOR_STATEMENT_DRIFT');
     covered.add(i);
   }
 }
 if(covered.size!==47)err('D07_ACTOR_SOURCE_GAP');
 const c=read(root+'/estado/recuperacao-c45.json');
 if(c.cursor.last_event_id!==out.last_event_id||c.cursor.mortal!==true||
    c.cursor.embrace_occurred!==false||c.resources.xp_total!==675||
    c.resources.xp_spent!==270||c.resources.xp_remaining!==405||
    c.resources.willpower_available!==4)err('D07_C45_STATE_DRIFT');
 if(!catalog.subjects.some(s=>s.id==='chr001-runtime-story-architecture')||
    catalog.subjects.filter(s=>s.id.startsWith('rule-runtime-')&&s.id.endsWith('-sources')).length!==4)
    err('D07_D05_CUSTODY_OWNER_GAP');
 for(const actor of actorSubjects.slice(0,2)) {
   try{resolveSubject(catalog,actor.id,{snapshot_sha:head,role:'PLAYER'});err('D07_DISCLOSURE_BROKEN');}
   catch(e){if(e.code!=='DISCLOSURE_DENIED')throw e;}
 }
 return {head,review:'D07_DISTINCT_SOURCE_COMPARISON_NOT_EXTERNAL_EDITORIAL_CERTIFICATION',
 actor_rows_exact:covered.size,actor_scopes:actorSubjects.length,open_threads_exact:44,scene_facts_exact:true,
 privacy:'DENY_PLAYER_FOR_SYSTEM_AUDIT',source_commit:source,
 runtime_semantic_review:'PENDING',active_runtime_successions_unproven:121,xp_field_owner_preserved:true,story_activation_source_preserved:true,provisional_mechanics_source_preserved:true,history_batches_source_preserved:27,
 gate:'D07_NOT_YET_PASS'};
}
if(process.argv[1]?.endsWith('/revisar-independente-d07.mjs')){
 const x=reviewD07();console.log(JSON.stringify(x));
 if(process.argv.includes('--require-pass')&&x.gate!=='D07_PASS')process.exitCode=1;
}
