// D03: source-grounded spatial concepts, no silent editorial authority or truth promotion.
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const base='novydres/cenario/';
const fail=code=>{const e=new Error(code);e.code=code;throw e;};
const load=p=>JSON.parse(readFileSync(p,'utf8'));
const sha=b=>createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
export function validateAtlasConcepts({overrides={}}={}){
 const cat=load('novydres/catalogo.json');
 const topics=cat.subjects.filter(s=>s.id.startsWith('district-')||/^poi-\d\d$/.test(s.id));
 if(topics.length!==41||topics.filter(s=>s.id.startsWith('district-')).length!==9||
    topics.filter(s=>/^poi-\d\d$/.test(s.id)).length!==32)fail('D03_ATLAS_SUBJECT_COVERAGE');
 const seen=new Set(),sourceSet=new Set();let sections=0;
 for(const s of topics){
   if(seen.has(s.id)||s.kind!=='world-location'||s.visibility!=='SYSTEM_AUDIT'||
      !s.dependencies.includes('world-atlas-novydres'))fail('D03_ATLAS_OWNER');
   seen.add(s.id);
   const owner=load(s.path+'/assunto.json');
   const p=s.path+'/conteudo.json';
   const row=overrides[p]||load(p);
   if(owner.subject_id!==s.id||owner.status!=='CANDIDATE'||owner.owner_scope!==s.owner||
      row.subject_id!==s.id||row.editorial_authority!=='NOT_SELECTED'||
      row.epistemic_status!=='UNKNOWN'||row.visibility!=='SYSTEM_AUDIT'||
      row.status!=='CANDIDATE_NOT_OPERATIONAL'||
      row.atlas_document_owner!=='SOURCE_CUSTODY_NOT_COMPETING_FACT_OWNER')
      fail('D03_ATLAS_AUTHORITY_PROMOTION');
   if(row.source_variants?.length!==2)fail('D03_ATLAS_VARIANT_LOSS');
   const distinct=new Set();
   for(const v of row.source_variants){
     if(distinct.has(v.source_path)||v.source_status!=='candidate'||
        v.source_text_literal!==true||v.epistemic_promotion!==false||
        !Number.isInteger(v.start_line)||!Number.isInteger(v.end_line)||v.end_line<v.start_line)
        fail('D03_ATLAS_VARIANT_CORRUPT');
     distinct.add(v.source_path);sourceSet.add(v.source_path);
     const fileBytes=readFileSync(v.source_path);
     if(sha(fileBytes)!==v.source_blob_sha)fail('D03_ATLAS_SHA_MISMATCH');
     const lines=fileBytes.toString('utf8').split(/\r?\n/);
     if(v.end_line>lines.length)fail('D03_ATLAS_SECTION_RANGE');
     if(lines.slice(v.start_line-1,v.end_line).join('\n')!==v.text||
        !v.text.startsWith('### '+row.display_label_from_source))
        fail('D03_ATLAS_LITERAL_MISMATCH');
     if(!owner.source_refs.some(x=>x.id===v.source_path&&x.sha===v.source_blob_sha))
        fail('D03_ATLAS_PROVENANCE');
     sections++;
   }
 }
 if(sourceSet.size!==2||sections!==82)fail('D03_ATLAS_VARIANT_COVERAGE');
 return {ok:true,concepts:41,districts:9,places:32,exact_source_sections:82,
   operational_authority:false,editorial_selection:false};
}
