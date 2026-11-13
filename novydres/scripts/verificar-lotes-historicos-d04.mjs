// ADR-001 D04: reconstitute only documented HISTORY_INDEX_v039 batch ownership, not lost events.
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const M='c9fcfc0c558cd17d58ec8c8272da3ed70182ff37';
const base='novydres/cronicas/CHR-001/historico/history-index/lotes-c45.json';
const origins=[
 'novydres/cronicas/CHR-001/personagem/state-versions/registro.json',
 'novydres/cronicas/CHR-001/episodios/m203/registro.json',
 'novydres/cronicas/CHR-001/episodios/m204/registro.json',
 'novydres/cronicas/CHR-001/episodios/m301/registro.json',
 'novydres/cronicas/CHR-001/episodios/m302/registro.json'
];
const fail=x=>{const e=new Error(x);e.code=x;throw e;};
const get=x=>JSON.parse(readFileSync(x,'utf8'));
const git=(...a)=>execFileSync('git',a,{encoding:'utf8',maxBuffer:64*1024*1024,stdio:['ignore','pipe','ignore']}).trim();
const blob=bytes=>createHash('sha1').update('blob '+bytes.length+'\0').update(bytes).digest('hex');
export function verifyHistoryBatches({override=null}={}){
 const data=override||get(base),ref='novydres/chronicles/CHR-001/HISTORY_INDEX_v039.json';
 if(data.subject_id!=='chr001-historic-history-index'||data.status!=='CANDIDATE_PARTIAL_HISTORICAL_INDEX_NO_RUNTIME'||
   data.visibility!=='SYSTEM_AUDIT'||data.source_refs?.length!==1||
   data.source_refs[0].id!==ref||data.source_refs[0].source_commit!==M||
   data.source_refs[0].sha!=='a8cc5a2860e8bc5e7acbf5a48b3f98614c7469a0'||
   git('rev-parse',M+':'+ref)!==data.source_refs[0].sha)
   fail('D04_HISTORY_AUTHORITY_PIN');
 const historic=JSON.parse(git('show',M+':'+ref));
 if(data.last_event_id!==historic.last_event_id||data.index_coverage!==historic.index_coverage||
   data.history_retrieval_status!==historic.history_retrieval_status||
   data.technical_ledger_status!==historic.technical_ledger_status||
   data.historical_unindexed_relationships!==historic.historical_unindexed_relationships||
   data.no_universal_ledger!==true||data.no_false_verbatim_transcripts!==true||
   data.no_new_historical_events!==true||data.no_claim_of_complete_history_index!==true||
   data.not_player_disclosable!==true)fail('D04_HISTORY_SEMANTIC_OVERCLAIM');
 const registers=new Map();
 for(const path of origins)for(const record of get(path).source_records){
   if(registers.has(record.source_path))fail('D04_HISTORY_MULTI_OWNER');
   registers.set(record.source_path,record);
 }
 const rows=data.source_rows||[];
 if(rows.length!==27||historic.history_batches.length!==27||data.total_batches!==27||
    new Set(rows.map(x=>x.original_path)).size!==26||data.unique_source_files!==26)
    fail('D04_HISTORY_BATCH_COUNT');
 for(let i=0;i<rows.length;i++){
   const row=rows[i],source=historic.history_batches[i],reg=registers.get(source.path);
   if(!reg||row.ordinal!==i+1||row.episode_range!==source.episode_range||
      row.original_path!==source.path||row.original_sha!==reg.original_git_blob_sha||
      row.original_source_commit!==M||row.candidate_path!==reg.target_path||
      row.candidate_sha!==reg.original_git_blob_sha||
      row.destination_subject_id!==reg.semantic_group||row.provenance!==source.provenance||
      row.event_count!==(source.event_count??null)||
      row.last_event_id!==(source.last_event_id??source.event_id??null)||
      row.roll_audit_path!==(source.roll_audit??source.roll_transcript??null)||
      row.mechanical_annotation!==(source.mechanics??null)||
      row.technical_ledger_committed!==(source.technical_ledger_committed??null)||
      row.not_automatic_fact_authority!==true)
      fail('D04_HISTORY_BATCH_SOURCE_MISMATCH');
   const classification=source.provenance.includes('ORIGINAL_DRIVE')?'ORIGINAL_DIARY_NOT_AUDITED_LEDGER':
     source.provenance.includes('SUMMARY')?'SOURCE_SUMMARY_NOT_VERBATIM_TRANSCRIPT':
     'SOURCE_RECORD_NO_NEW_EVENT_PROVEN';
   if(row.representation!==classification||row.technical_ledger_committed===true)
     fail('D04_HISTORY_FALSE_TRANSCRIPT_OR_LEDGER');
   if(git('rev-parse',M+':'+row.original_path)!==row.original_sha||
      git('rev-parse','HEAD:'+row.candidate_path)!==row.candidate_sha||
      blob(readFileSync(row.candidate_path))!==row.original_sha)
      fail('D04_HISTORY_SOURCE_CONTENT_DRIFT');
 }
 return {ok:true,gate:'D04_27_BATCH_SOURCE_SEMANTICS_VERIFIED_INDEX_COVERAGE_PARTIAL',
  source_commit:M,batches:27,unique_original_files:26,
  original_index_coverage:historic.index_coverage,
  no_ledger_reconstruction:true,no_transcripts_invented:true};
}
if(process.argv[1]?.endsWith('/verificar-lotes-historicos-d04.mjs'))
 console.log(JSON.stringify(verifyHistoryBatches()));
