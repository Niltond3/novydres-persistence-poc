// D04 targeted semantic parity: compare all C45 actor-local knowledge and open threads with pinned original facts.
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {isDeepStrictEqual} from 'node:util';

const M='c9fcfc0c558cd17d58ec8c8272da3ed70182ff37';
const KNOW='novydres/chronicles/CHR-001/knowledge/NPC_KNOWLEDGE_PROVENANCE_V22.json';
const THREAD='novydres/chronicles/CHR-001/knowledge/OPEN_THREADS_V24.json';
const DEST='novydres/cronicas/CHR-001/tramas/abertas/atual-c45.json';
const fail=code=>{const e=new Error(code);e.code=code;throw e;};
const read=p=>JSON.parse(readFileSync(p,'utf8'));
const git=(...args)=>execFileSync('git',args,{encoding:'utf8',stdio:['ignore','pipe','ignore'],maxBuffer:16*1024*1024}).trim();
const source=p=>JSON.parse(git('show',M+':'+p));
function pinned(ref,p,sha){
 return ref?.id===p && ref?.sha===sha && ref?.source_commit===M &&
        git('rev-parse',M+':'+p)===sha;
}
export function verifyC45KnowledgeThreads({actorOverrides=null,threadsOverride=null}={}){
 const cat=read('novydres/catalogo.json');
 const actors=cat.subjects.filter(s=>s.id.startsWith('chr001-knowledge-npc-'));
 const orig=source(KNOW),trOrig=source(THREAD);
 if(actors.length!==38 || orig.last_event_id!=='CHR001-M302-C01-05-20261111-001'||
    !Array.isArray(orig.records)||orig.records.length!==47||
    !Array.isArray(trOrig.threads)||trOrig.threads.length!==44)
    fail('D04_ORIGINAL_SEMANTIC_BOUNDARY_DRIFT');
 const pinnedKnowledge=git('rev-parse',M+':'+KNOW);
 const pinnedThreads=git('rev-parse',M+':'+THREAD);
 if(pinnedKnowledge!=='a5da61e00c5e29a4941d5697b2010743313f9007'||
    pinnedThreads!=='05ce76898d2757c1e270e9c3b1282712df123d13')
    fail('D04_ORIGINAL_SOURCE_NOT_PINNED');
 const seen=new Set(),byActor=new Map();
 for(const s of actors){
   if(s.visibility!=='SYSTEM_AUDIT'||!s.path.startsWith('novydres/cronicas/CHR-001/conhecimento/atores/'))
     fail('D04_KNOWLEDGE_OWNER_OR_VISIBILITY');
   const a=actorOverrides?.[s.id]??read(s.path+'/conhecimento.json');
   if(a.subject_id!==s.id||s.id!=='chr001-knowledge-'+a.actor_id||
      a.status!=='CANDIDATE_C45_NOT_ACTIVE'||
      a.source_last_event_id!==orig.last_event_id||a.source_record_count!==47||
      a.no_global_fact_promotion!==true||a.no_cross_actor_inference!==true||
      a.no_player_disclosure!==true||
      a.source_refs?.length!==1||!pinned(a.source_refs[0],KNOW,pinnedKnowledge)||
      !Array.isArray(a.records))
     fail('D04_KNOWLEDGE_SCOPE_OR_DISCLOSURE');
   if(byActor.has(a.actor_id))fail('D04_DUPLICATE_ACTOR_OWNER');
   byActor.set(a.actor_id,a.records.length);
   for(const item of a.records){
     const i=item?.source_row_index,original=orig.records[i];
     if(!Number.isInteger(i)||i<0||i>=47||seen.has(i)||original?.entity!==a.actor_id||
        !isDeepStrictEqual(item.record,original))
       fail('D04_KNOWLEDGE_SEMANTIC_DIFFERENCE');
     for(const k of ['confirmed','claims','suspected','unknown'])
       if(!Array.isArray(item.record[k]))fail('D04_KNOWLEDGE_EPISTEMIC_DRIFT');
     seen.add(i);
   }
 }
 if(seen.size!==47||orig.records.some(x=>!byActor.has(x.entity)))
   fail('D04_KNOWLEDGE_UNMAPPED_SOURCE_ROW');
 const threads=threadsOverride??read(DEST);
 if(threads.subject_id!=='chr001-open-threads-versions'||
    threads.status!=='CANDIDATE_C45_HISTORICAL_PARTIAL'||
    threads.visibility!=='SYSTEM_AUDIT'||
    threads.source_refs?.length!==1||
    !pinned(threads.source_refs[0],THREAD,pinnedThreads)||
    threads.last_event_id!==trOrig.last_event_id||
    threads.source_count!==44||
    threads.no_future_outcome_inferred!==true||
    threads.no_player_disclosure!==true||threads.no_new_events!==true||
    !isDeepStrictEqual(threads.threads,trOrig.threads))
    fail('D04_OPEN_THREADS_SEMANTIC_DIFFERENCE');
 return {ok:true,source_commit:M,actors:actors.length,knowledge_rows:seen.size,
  open_threads:threads.threads.length,epistemic_buckets_exact:true,
  evidence_and_unknowns_preserved:true,gate:'D04_C45_ACTOR_AND_THREADS_SEMANTIC_PARITY_NOT_FULL_D04_PASS'};
}
if(process.argv[1]?.endsWith('/verificar-semantica-c45.mjs'))
 console.log(JSON.stringify(verifyC45KnowledgeThreads()));
