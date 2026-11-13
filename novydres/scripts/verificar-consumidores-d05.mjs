// ADR-001 D05: whole-inventory consumer retirement and historical source readback.
// Passing byte custody never certifies behavioral equivalence or cutover.
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const fail=code=>{const e=new Error(code);e.code=code;throw e;};
const read=p=>JSON.parse(readFileSync(p,'utf8'));
const git=paths=>new Map(execFileSync('git',['ls-tree','-r','--full-tree',paths],{
 encoding:'utf8',maxBuffer:64*1024*1024,stdio:['ignore','pipe','ignore']
}).trim().split('\n').filter(Boolean).map(row=>{
 const m=/^\d+ blob ([a-f0-9]{40})\t(.+)$/.exec(row);
 if(!m)fail('D05_TREE_INVALID');
 return [m[2],m[1]];
}));
const digest=bytes=>createHash('sha1').update('blob '+bytes.length+'\0').update(bytes).digest('hex');
const groups=[
 ['chr001-runtime-story-architecture','novydres/cronicas/CHR-001/documentos/proveniencia-arquitetura',97],
 ['rule-runtime-orchestration-sources','novydres/sistema/regras/proveniencia-orquestracao',112],
 ['rule-runtime-preparation-sources','novydres/sistema/regras/proveniencia-preparacao',40],
 ['rule-runtime-scene-execution-sources','novydres/sistema/regras/proveniencia-execucao',28],
 ['rule-runtime-root-contract-sources','novydres/sistema/regras/proveniencia-runtime',8]
];
export function verifyD05({ledgerOverride=null,custodyOverride=null}={}){
 const ledger=ledgerOverride||read('novydres/sistema/arquitetura/fase-d/execucao-d05.json');
 const inv=read('novydres/sistema/arquitetura/fase-d/inventario-origens.json');
 const cat=read('novydres/catalogo.json'),original=git(inv.source_snapshot.commit_sha);
 const now=git(execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8',stdio:['ignore','pipe','ignore']}).trim());
 const originals=inv.source_files.filter(x=>x.d01_origin_route?.handoff_phase==='D05');
 if(originals.length!==399||ledger.source_count!==399||ledger.source_records?.length!==399)fail('D05_COVERAGE');
 const byOriginal=new Map(originals.map(x=>[x.source_path,x]));
 if(byOriginal.size!==399)fail('D05_DUPLICATE_ORIGIN');
 const records=new Map();
 for(const r of ledger.source_records){
   const o=byOriginal.get(r.origin);
   if(!o||records.has(r.origin)||r.original_git_blob_sha!==o.source_blob_sha||
      r.source_snapshot!==inv.source_snapshot.commit_sha||
      original.get(r.origin)!==r.original_git_blob_sha)fail('D05_ORIGIN_SHA_OR_OWNER_DRIFT');
   records.set(r.origin,r);
 }
 let exact=0;const archived=new Set();
 for(const [id,root,count] of groups){
   const entry=cat.subjects.find(x=>x.id===id);
   if(!entry||entry.visibility!=='SYSTEM_AUDIT'||entry.path!==root)fail('D05_CUSTODY_OWNER_DRIFT');
   const manifest=custodyOverride?.id===id?custodyOverride.doc:read(root+'/registro.json');
   if(manifest.subject_id!==id||manifest.status!=='CANDIDATE_HISTORICAL_SOURCE_CUSTODY_ONLY'||
      manifest.no_operational_promotion!==true||manifest.no_automatic_editorial_selection!==true||
      manifest.no_player_disclosure!==true||manifest.source_count!==count||manifest.source_records?.length!==count)
      fail('D05_CUSTODY_PROMOTION_OR_GAP');
   for(const row of manifest.source_records){
     const r=records.get(row.source_path),f=entry.files.find(x=>x.path===row.target_path);
     if(!r||r.retirement_method!=='EXACT_INERT_SOURCE_BLOB_REHOMED'||
        row.original_git_blob_sha!==r.original_git_blob_sha||
        row.source_commit!==inv.source_snapshot.commit_sha||row.source_owner!==id||
        row.source_kind!=='EXACT_GIT_BLOB_INERT'||row.epistemic_status!=='UNREVIEWED_SOURCE_NOT_ACTIVE_FACT'||
        !row.target_path.startsWith(root+'/fonte-')||archived.has(row.source_path)||
        !f||f.blob_sha!==row.original_git_blob_sha||now.get(row.target_path)!==row.original_git_blob_sha)
       fail('D05_CUSTODY_SOURCE_MISMATCH');
     const bytes=readFileSync(row.target_path);
     if(digest(bytes)!==row.original_git_blob_sha)fail('D05_CUSTODY_SOURCE_BYTES');
     archived.add(row.source_path);exact++;
   }
 }
 if(exact!==285||records.size!==399)fail('D05_INCOMPLETE_SOURCE_RETENTION');
 const historical=ledger.source_records.filter(x=>x.retirement_method==='HISTORIC_GIT_ORIGINAL_RETAINED');
 if(historical.length!==114||historical.some(r=>archived.has(r.origin)||original.get(r.origin)!==r.original_git_blob_sha))
   fail('D05_HISTORICAL_SOURCE_GAP');
 const active=ledger.source_records.filter(x=>x.active_original_reference===true);
 if(active.length!==121||active.some(x=>!x.proposed_successor||x.semantic_equivalence!=='NOT_YET_PROVEN'))
   fail('D05_OPERATIONAL_SUCCESSION_UNPROVEN');
 for(const x of ledger.source_records){
   const successor=x.proposed_successor;
   if(successor==='HISTORICAL_GIT_TREE_ONLY')continue;
   const target=cat.subjects.find(s=>s.id===successor);
   if(!target&&!now.has(successor))fail('D05_SUCCESSOR_TARGET_MISSING');
   if(target&&target.visibility!=='SYSTEM_AUDIT'&&x.origin.startsWith('novydres/runtime/'))
     fail('D05_SECRET_SOURCE_PROMOTION');
 }
 return {source_commit:inv.source_snapshot.commit_sha,exact_blobs_inert:exact,
  historical_git_only:historical.length,source_origins_covered:records.size,
  active_source_successions_unproven:active.length,
  source_blobs_preserved:true,behavior_equivalence:'UNPROVEN_FOR_121_CURRENTLY_REFERENCED_SOURCES',
  gate:'D05_CUSTODY_PASS_BEHAVIORAL_GATE_PENDING'};
}
if(process.argv[1]?.endsWith('/verificar-consumidores-d05.mjs'))
 console.log(JSON.stringify(verifyD05()));
