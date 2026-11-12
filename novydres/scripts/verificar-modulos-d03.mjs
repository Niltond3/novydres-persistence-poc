// D03 module-level field ownership of all creation/rule originals, without active rule promotion.
import {readFileSync} from 'node:fs';
const load=p=>JSON.parse(readFileSync(p,'utf8'));
const fail=code=>{let e=new Error(code);e.code=code;throw e;};
export function verifyD03RuleModules({overrides={}}={}){
 const inv=load('novydres/sistema/arquitetura/fase-d/inventario-origens.json');
 const fragments=load('novydres/sistema/arquitetura/fase-d/fragmentos-d03.json');
 const src=new Map(inv.source_files.filter(x=>x.d01_origin_route?.handoff_phase==='D03'&&
   x.source_path.startsWith('novydres/systems/')).map(x=>[x.source_path,x]));
 const cat=load('novydres/catalogo.json');
 const ids=cat.subjects.filter(s=>s.id.startsWith('rule-')&&
   !['rule-creation-novydres','rule-experience-novydres'].includes(s.id));
 if(src.size!==38||ids.length!==20)fail('D03_RULE_MODULE_COVERAGE');
 const ledger=load('novydres/sistema/regras/criacao-de-personagens/registro.json');
 const ledgerMap=new Map(ledger.source_records.map(r=>[r.source_path,r]));
 if(ledgerMap.size!==38)fail('D03_RULE_SOURCE_CUSTODY');
 const fragmentMap=new Map(fragments.documents.map(d=>[d.source_path,d]));
 const seen=new Set(),byId=new Map();let segments=0;
 for(const s of ids){
   const path=s.path+'/conteudo.json';
   const doc=overrides[path]||load(path);
   const meta=load(s.path+'/assunto.json');
   if(doc.subject_id!==s.id||doc.semantic_owner!==s.id||
      doc.source_custodian!=='rule-creation-novydres'||
      doc.status!=='CANDIDATE_NOT_OPERATIONAL'||doc.current_system_rule_active!==false||
      doc.editorial_approval_inferred!==false||meta.owner_scope!=='novydres/sistema/regras/criacao-de-personagens')
     fail('D03_RULE_MODULE_AUTHORITY');
   if(!doc.source_records?.length)fail('D03_RULE_MODULE_EMPTY');
   byId.set(s.id,doc);
   for(const item of doc.source_records){
     const original=src.get(item.source_path),parent=ledgerMap.get(item.source_path),frag=fragmentMap.get(item.source_path);
     if(seen.has(item.source_path)||!original||!parent||!frag||original.source_blob_sha!==item.source_sha||
        item.semantic_owner!==s.id||parent.semantic_owner!==s.id||
        parent.owner_handoff_phase!=='D03_RULE_MODULE')fail('D03_RULE_MODULE_OWNER_OR_SOURCE');
     if(!meta.source_refs.some(r=>r.id===item.source_path&&r.sha===item.source_sha)||
        JSON.stringify(item.section_or_field_locators)!==JSON.stringify(frag.sections_or_fields))
        fail('D03_RULE_MODULE_FRAGMENT_MISMATCH');
     if(item.source_episteme!=='SOURCE_LITERAL_NOT_RECLASSIFIED'||item.local_character_state_not_imported!==true)
        fail('D03_RULE_MODULE_TRUTH_PROMOTION');
     seen.add(item.source_path);segments+=item.section_or_field_locators.length;
   }
 }
 let deferred=0;
 for(const [path,item] of src){
   const parent=ledgerMap.get(path);
   if(!parent)fail('D03_RULE_SOURCE_CUSTODY');
   if(path.includes('/webfirst-legacy/')){
     if(parent.semantic_owner!==null||parent.owner_handoff_phase!=='D05_CONSUMER'||seen.has(path))
       fail('D03_RULE_CONSUMER_HANDBACK');
     deferred++;
   }else if(!seen.has(path))fail('D03_RULE_MODULE_UNMAPPED');
 }
 if(seen.size!==32||deferred!==6)fail('D03_RULE_MODULE_INCOMPLETE');
 return {ok:true,modules:ids.length,source_documents:seen.size,d05_consumer_handoffs:deferred,source_field_or_section_locators:segments,no_rule_activation:true};
}
