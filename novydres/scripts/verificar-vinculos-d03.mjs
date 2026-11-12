import {readFileSync} from 'node:fs';
const r=p=>JSON.parse(readFileSync(p,'utf8'));
const fail=code=>{let e=new Error(code);e.code=code;throw e;};
export function verifyWorldLinks(root=process.cwd(),override=null){
 const base='novydres/sistema/arquitetura/fase-d/';
 const report=override||r(base+'vinculos-literais-d03.json'),inv=r(base+'inventario-origens.json'),cat=r('novydres/catalogo.json');
 const sources=new Map(inv.source_files.filter(x=>x.d01_origin_route?.handoff_phase==='D03'&&x.source_path.startsWith('novydres/world/')).map(x=>[x.source_path,x]));
 if(sources.size!==18||report.links?.length!==84||report.classification!=='SYSTEM_AUDIT'||report.not_operational!==true||
    report.role!=='LITERAL_LINK_INDEX_NOT_SEMANTIC_RELATION_GRAPH'||report.semantic_claims_promoted!==0)fail('D03_LINK_SCOPE_INVALID');
 const seen=new Set(),reportedSources=new Set();let resolved=0,deferred=0;
 for(const link of report.links){
  const origin=sources.get(link.source_path);
  if(!origin||origin.source_blob_sha!==link.source_sha)fail('D03_LINK_SOURCE_SHA');
  const key=[link.source_sha,link.location?.line,link.target_literal,link.link_type].join('|');
  if(seen.has(key))fail('D03_LINK_DUPLICATE');seen.add(key);reportedSources.add(link.source_path);
  if(link.semantic_relation_confirmed!==false||link.epistemic_status!=='UNKNOWN'||link.visibility!=='SYSTEM_AUDIT')
    fail('D03_LINK_TRUTH_OR_DISCLOSURE_PROMOTION');
  const subject=cat.subjects.find(x=>x.id===link.owner_subject_id);
  if(!subject)fail('D03_LINK_SOURCE_OWNER');
  const ledger=r(subject.path+'/registro.json'),copy=ledger.source_records.find(x=>x.source_path===link.source_path);
  if(!copy||copy.source_blob_sha!==origin.source_blob_sha)fail('D03_LINK_SOURCE_OWNER');
  const line=readFileSync(copy.target_path,'utf8').split(/\r?\n/)[link.location.line-1];
  if(typeof line!=='string'||!line.includes(link.target_literal))fail('D03_LINK_LINE_NOT_FOUND');
  if(link.resolution==='DOCUMENT_OWNER_RESOLVED_VARIANTS_UNSELECTED'){
    const target=cat.subjects.find(x=>x.id===link.target_subject_id);
    if(!target||!Array.isArray(link.target_options)||!link.target_options.length)fail('D03_LINK_INVALID_TARGET');
    for(const item of link.target_options){
      const o=sources.get(item.source_path);
      if(!o||o.source_blob_sha!==item.source_sha||!target.path.startsWith('novydres/'))
        fail('D03_LINK_INVALID_TARGET');
    }
    resolved++;
  }else if(['DEFERRED_SEMANTIC_TARGET_NO_ACTIVE_REFERENCE','REFERENCED_HISTORICAL_VARIANT_NOT_EXACTLY_PRESENT'].includes(link.resolution)&&link.target_subject_id===null){
    deferred++;
  }else fail('D03_LINK_SILENT_RESOLUTION');
 }
 return {ok:true,links:seen.size,origin_documents:reportedSources.size,owner_resolved:resolved,deferred,semantic_relations_verified:false};
}
