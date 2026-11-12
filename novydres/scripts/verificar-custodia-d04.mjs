// D04 integrity: every source gets exact byte-preserved local-subject custody; no fake replay ledger.
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const get=p=>JSON.parse(readFileSync(p,'utf8'));
const err=code=>{const e=new Error(code);e.code=code;throw e;};
const digest=bytes=>createHash('sha1').update('blob '+bytes.length+'\0').update(bytes).digest('hex');
export function verifyD04Custody({overrideSubject=null,overrideRecord=null}={}){
 const inv=get('novydres/sistema/arquitetura/fase-d/inventario-origens.json');
 const expected=inv.source_files.filter(x=>x.d01_origin_route?.handoff_phase==='D04');
 const original=new Map(expected.map(x=>[x.source_path,x]));
 if(expected.length!==438||original.size!==438)err('D04_SOURCE_COUNT');
 const cat=get('novydres/catalogo.json');
 const subjects=cat.subjects.filter(s=>s.id.startsWith('chr001-')&&
 !['chr001-npc-samir-haddad','chr001-state-checkpoint','chr001-table-config'].includes(s.id));
 if(subjects.length!==31||new Set(subjects.map(s=>s.path)).size!==31)err('D04_OWNER_COUNT');
 const seen=new Set();let copied=0,historicalAbsent=0;
 for(const s of subjects){
  const meta=get(s.path+'/assunto.json'),path=s.path+'/registro.json';
  const reg=overrideSubject===s.id?overrideRecord:get(path);
  if(meta.subject_id!==s.id||meta.owner_scope!==s.owner||
   meta.status!=='CANDIDATE'||meta.visibility!=='SYSTEM_AUDIT'||
   reg.subject_id!==s.id||reg.local_chronicle_id!=='CHR-001'||
   reg.status!=='CANDIDATE_NOT_OPERATIONAL'||reg.not_played_event_creation!==true||
   reg.no_editorial_or_epistemic_promotion!==true||reg.operational_ownership!=='NOT_ACTIVATED')
   err('D04_UNAUTHORIZED_OWNER_OR_PROMOTION');
  if(reg.source_count!==reg.source_records?.length||!reg.source_count)err('D04_MISSING_RECORD');
  for(const row of reg.source_records){
   const src=original.get(row.source_path);
   if(!src||seen.has(row.source_path)||row.original_git_blob_sha!==src.source_blob_sha||
    row.source_snapshot_commit!==inv.source_snapshot.commit_sha||
    row.semantic_group!==s.id||row.local_owner!==s.id||
    row.source_kind!=='EXACT_ORIGINAL_BYTES'||row.epistemic_status!=='SOURCE_LITERAL_UNEVALUATED'||
    row.current_state_authority!=='NOT_INFERRED_FROM_FILENAME'||row.visibility!=='SYSTEM_AUDIT'||
    row.source_legacy_route_custody_only!==true)err('D04_WRONG_SOURCE_OWNER');
   seen.add(row.source_path);
   if(!row.target_path.startsWith(s.path+'/fonte-'))err('D04_WRONG_TARGET');
   const bytes=readFileSync(row.target_path);
   if(digest(bytes)!==src.source_blob_sha)err('D04_CONTENT_MISMATCH');
   const f=s.files.find(f=>f.path===row.target_path);
   if(!f||f.blob_sha!==src.source_blob_sha)err('D04_CATALOG_MISMATCH');
   if(!meta.source_refs.some(r=>r.id===src.source_path&&r.sha===src.source_blob_sha&&
       r.source_commit===inv.source_snapshot.commit_sha))err('D04_PROVENANCE_MISSING');
   const git=execFileSync('git',['rev-parse',inv.source_snapshot.commit_sha+':'+src.source_path],{
       encoding:'utf8',stdio:['ignore','pipe','ignore']}).trim();
   if(git!==src.source_blob_sha)err('D04_ORIGINAL_SNAPSHOT_DRIFT');
   copied++;
   if(!s.files.find(f=>f.path===src.source_path))historicalAbsent++;
  }
 }
 if(seen.size!==438||copied!==438)err('D04_INCOMPLETE_COVERAGE');
 return {ok:true,originals:438,exact_bytes_copied:438,subject_owners:31,
   source_paths_obsolete_as_current:historicalAbsent,gate:'D04_SOURCE_CUSTODY_NOT_SEMANTIC_STATE_PASS'};
}
