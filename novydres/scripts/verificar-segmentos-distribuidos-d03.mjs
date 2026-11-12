// D03: every existing document field/section locator has one owner-local projection.
import {readFileSync} from 'node:fs';
const p='novydres/sistema/arquitetura/fase-d/';
const get=p=>JSON.parse(readFileSync(p,'utf8'));
const fail=code=>{let e=new Error(code);e.code=code;throw e;};
export function validateD03DistributedSegments({overrides={}}={}){
 const source=get(p+'fragmentos-d03.json'),catalog=get('novydres/catalogo.json');
 const ids=new Set(['world-atlas-novydres','world-history-novydres','world-politics-novydres',
  'world-lineage-urban-gangrel','npc-iskander-yasupov','npc-madame-zoya',
  'world-npc-power-scale','rule-creation-novydres','rule-experience-novydres']);
 const collected=new Map();let locators=0;
 for(const s of catalog.subjects.filter(s=>ids.has(s.id))){
  const path=s.path+'/segmentos.json';
  const record=overrides[path]||get(path);
  if(record.subject_id!==s.id||record.not_operational!==true||
     record.editorial_promotion!==false||record.epistemic_promotion!==false||
     record.source_document_count!==record.document_refs?.length)
     fail('D03_SEGMENT_OWNER_OR_AUTHORITY');
  for(const d of record.document_refs){
    if(collected.has(d.source_path))fail('D03_SEGMENT_DUPLICATE_OWNER');
    collected.set(d.source_path,{owner:s.id,data:d});
    locators+=d.source_sections_or_fields?.length||0;
  }
 }
 if(collected.size!==64||locators!==1707)fail('D03_SEGMENT_INCOMPLETE');
 for(const d of source.documents){
   const entry=collected.get(d.source_path);
   if(!entry||entry.owner!==d.owner_subject_id||
      entry.data.source_blob_sha!==d.source_blob_sha||
      entry.data.epistemic_status!==d.epistemic_status||
      entry.data.visibility!==d.visibility||
      JSON.stringify(entry.data.conflicts)!==JSON.stringify(d.conflicts)||
      JSON.stringify(entry.data.source_sections_or_fields)!==JSON.stringify(d.sections_or_fields))
     fail('D03_SEGMENT_MISMATCH');
 }
 return {ok:true,source_documents:collected.size,locators,unique_owners:ids.size};
}
