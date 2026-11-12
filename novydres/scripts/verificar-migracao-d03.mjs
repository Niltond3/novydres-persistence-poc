// ADR-001 D03 — verify all source-to-subject custody mappings, without granting editorial authority.
import {readFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const sha=bytes=>createHash('sha1').update('blob '+bytes.length+'\0').update(bytes).digest('hex');
const fail=(code)=>{const e=new Error(code);e.code=code;throw e;};
const read=(root,p)=>JSON.parse(readFileSync(resolve(root,p),'utf8'));
export function verifyD03(root=process.cwd(),opts={}){
 const inv=opts.inventory||read(root,'novydres/sistema/arquitetura/fase-d/inventario-origens.json');
 const cat=opts.catalog||read(root,'novydres/catalogo.json');
 const expected=inv.source_files.filter(x=>x.d01_origin_route?.handoff_phase==='D03');
 if(expected.length!==64)fail('D03_INVENTORY_COUNT');
 const byPath=new Map(expected.map(x=>[x.source_path,x]));
 if(byPath.size!==64)fail('D03_DUPLICATE_SOURCE');
 const dirs=['novydres/cenario/','novydres/personagens/','novydres/sistema/regras/'];
 const ids=['world-atlas-novydres','world-history-novydres','world-politics-novydres',
  'world-lineage-urban-gangrel','npc-iskander-yasupov','npc-madame-zoya',
  'world-npc-power-scale','rule-creation-novydres','rule-experience-novydres'];
 const own=new Set(),seen=new Set(),records=[];
 for(const id of ids){
  const subject=cat.subjects.find(x=>x.id===id);
  if(!subject || !dirs.some(x=>subject.path.startsWith(x)))fail('D03_SUBJECT_NOT_INDEXED');
  if(own.has(subject.path))fail('D03_DUPLICATE_OWNER');own.add(subject.path);
  const meta=read(root,subject.path+'/assunto.json'),ledger=(opts.ledgerOverrides||{})[id]||read(root,subject.path+'/registro.json');
  if(meta.subject_id!==id||meta.status!=='CANDIDATE'||meta.visibility!=='SYSTEM_AUDIT'||
    meta.owner_scope!==subject.owner||ledger.subject_id!==id||
    ledger.not_operational!==true||ledger.editorial_promotion!==false||
    ledger.epistemic_promotion!==false)fail('D03_UNAUTHORIZED_PROMOTION');
  const rows=ledger.source_records||[];
  if(rows.length<1)fail('D03_EMPTY_OWNER');
  for(const row of rows){
   const original=byPath.get(row.source_path);
   if(!original||seen.has(row.source_path))fail('D03_SOURCE_UNMAPPED_OR_DUPLICATE');
   seen.add(row.source_path);
   if(row.source_blob_sha!==original.source_blob_sha||row.semantic_owner!==id||
     row.source_authority!=='UNCHANGED'||row.source_episteme!=='UNCHANGED_NOT_RECLASSIFIED'||
     row.field_semantics!=='PENDING_VERIFICATION'||row.exact_blob_copy!==true)
      fail('D03_AUTHORITY_OR_SHA_MISMATCH');
   if(!row.target_path.startsWith(subject.path+'/fonte-')||!existsSync(resolve(root,row.target_path)))
      fail('D03_DESTINATION_MISSING');
   const bytes=readFileSync(resolve(root,row.target_path));
   if(sha(bytes)!==row.source_blob_sha)fail('D03_DESTINATION_CONTENT_MISMATCH');
   const p=meta.source_refs.find(x=>x.id===row.source_path);
   if(!p||p.sha!==original.source_blob_sha||p.source_commit!==inv.source_snapshot.commit_sha)
     fail('D03_PROVENANCE_NOT_PINNED');
   const git=execFileSync('git',['rev-parse',inv.source_snapshot.commit_sha+':'+row.source_path],
     {cwd:root,encoding:'utf8',stdio:['ignore','pipe','ignore']}).trim();
   if(git!==original.source_blob_sha)fail('D03_ORIGINAL_MISMATCH');
   const catalogFile=subject.files.find(x=>x.path===row.target_path);
   if(!catalogFile||catalogFile.blob_sha!==original.source_blob_sha)fail('D03_CATALOG_SOURCE_MISMATCH');
   records.push({id,path:row.target_path,blob_sha:git});
  }
 }
 if(seen.size!==64)fail('D03_INCOMPLETE_COVERAGE');
 return {ok:true,phase:'D03',originals:expected.length,identical_blobs:records.length,
   subject_portfolios:ids.length,gate:'STRUCTURAL_CUSTODY_ONLY_SEMANTIC_EQUIVALENCE_PENDING'};
}
if(process.argv[1]===fileURLToPath(import.meta.url))console.log(JSON.stringify(verifyD03()));
