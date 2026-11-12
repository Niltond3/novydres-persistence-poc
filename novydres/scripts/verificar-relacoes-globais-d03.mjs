// D03 proof: source-asserted global relations remain directed, evidenced and non-operational.
import {readFileSync} from 'node:fs';
const read=p=>JSON.parse(readFileSync(p,'utf8'));
const error=code=>{let e=new Error(code);e.code=code;throw e;};
export function verifyGlobalRelationships({overrides={}}={}){
 const cat=read('novydres/catalogo.json'),targets=new Set(['org-concilio-cruz-espada','org-legiao-coroa-ferro']);
 let edges=0,resolved=0,sourceOnly=0;
 for(const id of ['npc-iskander-yasupov','npc-madame-zoya']){
  const s=cat.subjects.find(x=>x.id===id),p=s.path+'/vinculos.json';
  const doc=overrides[p]||read(p),profile=read(s.path+'/perfil.json');
  if(doc.subject_id!==id||doc.status!=='CANDIDATE_NOT_OPERATIONAL'||
     doc.no_local_knowledge_claim!==true||doc.no_chronicle_relation_claim!==true||
     doc.source_only_unknown_targets_not_promoted!==true||
     profile.epistemic_status!=='UNKNOWN'||profile.local_knowledge_transferred!==false)
     error('D03_GLOBAL_RELATION_PROMOTION');
  if(doc.source_variants_examined!==(id==='npc-madame-zoya'?3:1))error('D03_GLOBAL_VARIANT_COUNT');
  const relationIds=new Set();
  for(const r of doc.relations){
    if(r.owner_subject_id!==id||r.from_subject_id!==id||r.direction!=='FROM_GLOBAL_CHARACTER'||
       r.inverse_is_derived!==true||r.epistemic_status!=='UNKNOWN'||
       r.visibility!=='SYSTEM_AUDIT'||r.scope!=='GLOBAL_SOURCE_ONLY_NOT_CHRONICLE_LOCAL')
       error('D03_GLOBAL_RELATION_OWNER');
    if(relationIds.has(r.relation_id))error('D03_GLOBAL_RELATION_DUPLICATE');
    relationIds.add(r.relation_id);
    if(r.to_subject_id===null){if(!r.to_source_only_literal)error('D03_GLOBAL_RELATION_TARGET');sourceOnly++;}
    else {if(!targets.has(r.to_subject_id)||!cat.subjects.some(x=>x.id===r.to_subject_id)||!s.dependencies.includes(r.to_subject_id))
      error('D03_GLOBAL_RELATION_TARGET');resolved++;}
    if(r.source_evidence?.length!==doc.source_variants_examined)error('D03_GLOBAL_RELATION_SOURCE_LOSS');
    for(const ev of r.source_evidence){
      const ref=profile.source_refs.find(x=>x.id===ev.path&&x.sha===ev.sha);
      if(!ref)error('D03_GLOBAL_RELATION_SHA');
      const lines=readFileSync(ev.path,'utf8').split(/\r?\n/);
      const text=lines[ev.line-1]||'';
      if(!/^\s+- /.test(text))error('D03_GLOBAL_RELATION_LITERAL');
    }
    edges++;
  }
 }
 if(edges!==5||resolved!==3||sourceOnly!==2)error('D03_GLOBAL_RELATION_COUNT');
 return {ok:true,directed_edges:edges,linked_to_existing_subjects:resolved,source_only_unknown_targets:sourceOnly,epistemic_promotion:false};
}
