// D03 gate proof is candidate-only: semantic equivalence by exact literal source + owned projections.
import {readFileSync} from 'node:fs';
import {validateCandidates} from './validar-assuntos.mjs';
import {checkCatalog,buildCatalog} from './catalogo-assuntos.mjs';
import {verifyD03} from './verificar-migracao-d03.mjs';
import {verifyD03Segments} from './verificar-fragmentos-d03.mjs';
import {validateD03DistributedSegments} from './verificar-segmentos-distribuidos-d03.mjs';
import {validateAtlasConcepts} from './verificar-conceitos-d03.mjs';
import {verifyWorldLinks} from './verificar-vinculos-d03.mjs';
import {verifyGlobalRelationships} from './verificar-relacoes-globais-d03.mjs';
import {verifyD03PC} from './verificar-identidade-pc-d03.mjs';
import {verifyD03RuleModules} from './verificar-modulos-d03.mjs';
const load=p=>JSON.parse(readFileSync(p,'utf8'));
const fail=code=>{let e=new Error(code);e.code=code;throw e;};
export function checkD03Gate({worldAuthorityOverride=null,npcAuditOverride=null,catalogOverride=null}={}){
 const inv=load('novydres/sistema/arquitetura/fase-d/inventario-origens.json');
 const source=inv.source_files.filter(x=>x.d01_origin_route?.handoff_phase==='D03');
 if(source.length!==64||new Set(source.map(x=>x.source_path)).size!==64)
   fail('D03_GATE_INVENTORY_COVERAGE');
 const custody=verifyD03(),refs=verifyWorldLinks(),segments=verifyD03Segments(),
  ownership=validateD03DistributedSegments(),places=validateAtlasConcepts(),
  relations=verifyGlobalRelationships(),pc=verifyD03PC(),rules=verifyD03RuleModules(),structure=validateCandidates(),
  catalog= catalogOverride||buildCatalog();
 if(!custody.ok||custody.identical_blobs!==64||!segments.ok||segments.documents!==64||
   ownership.locators!==1707||rules.modules!==20||rules.source_documents!==32||rules.d05_consumer_handoffs!==6||places.concepts!==41||places.exact_source_sections!==82||
   relations.directed_edges!==5||pc.local_state_promoted!==false||!structure.ok||
   !checkCatalog().ok)fail('D03_GATE_EQUIVALENCE');
 if(catalog.subjects.length!==79||
   new Set(catalog.subjects.map(s=>s.id)).size!==79||
   catalog.subjects.some(s=>!s.files?.length||s.status==='ACTIVE'))
   fail('D03_GATE_OWNER');
 const ids=new Set(catalog.subjects.map(s=>s.id));
 for(const s of catalog.subjects)for(const dep of s.dependencies||[])
   if(!ids.has(dep))fail('D03_GATE_DANGLING_ACTIVE_SUBJECT');
 if(catalog.deferred?.length!==0)fail('D03_GATE_DANGLING_ACTIVE_SUBJECT');
 if(refs.links!==84||refs.owner_resolved!==20||refs.deferred!==64)
   fail('D03_GATE_SOURCE_REFERENCE_AUDIT');
 const links=load('novydres/sistema/arquitetura/fase-d/vinculos-literais-d03.json');
 const unresolved=links.links.filter(x=>x.target_subject_id===null);
 if(unresolved.length!==64||
   unresolved.some(x=>x.semantic_relation_confirmed!==false||x.visibility!=='SYSTEM_AUDIT'))
   fail('D03_GATE_UNRESOLVED_OPERATIONAL_LINK');
 const wm=worldAuthorityOverride||load('novydres/fontes/originais/migration/WORLD_AUTHORITY_MATRIX_V1.json');
 const npc=npcAuditOverride||load('novydres/world/organizations/npc-sources/MADAME_ZOYA_V09_VARIANT_AUDIT_VERIFIED_V2.json');
 if(wm.status!=='SOURCE_COLLISION_UNRESOLVED'||wm.chapter_count!==6||
   wm.chapters.some(x=>x.promotion_verdict_directly_audited!==false)||
   npc.independent_editorial_verdict!=='PENDING_DO_NOT_PROMOTE'||npc.authority!=='NO_PROMOTION_OR_SELECTION')
   fail('D03_GATE_EDITORIAL_PROMOTION');
 const xp=load('novydres/sistema/regras/experiencia/escopos.json');
 if(xp.source_records.length!==8||xp.source_records.some(x=>
   x.semantic_owner_current!=='UNASSIGNED_UNTIL_APPLICABLE_PHASE'))
   fail('D03_GATE_XP_GLOBAL_LOCAL');
 const profiles=['npc-iskander-yasupov','npc-madame-zoya'].map(id=>load('novydres/personagens/'+id+'/perfil.json'));
 if(profiles.some(p=>p.epistemic_status!=='UNKNOWN'||p.editorial_selection!=='NO_VARIANT_SELECTED'||
   p.local_knowledge_transferred!==false||p.local_relations_transferred!==false))
   fail('D03_GATE_KNOWLEDGE_LEAK');
 return {
   status:'D03_SOURCE_INFORMATION_AND_OWNED_PROJECTION_VERIFIED_NONOPERATIONAL',
   source_origins:64,literal_equivalence_sha:64,source_locators:1707,
   candidate_subjects:79,rule_module_subjects:20,rule_source_claims_owned:32,geographic_semantic_topics:41,organization_topics:2,
   global_character_profiles:4,source_npc_relations:5,
   graph_active_dangling_refs:0,source_publication_refs_deferred:64,
   editorial_conflicts_retained:['CONFLICT-001','CONFLICT-002','CONFLICT-003B'],
   epistemic_promotion:false,local_xp_claim:false,
   release_dependency:'D04_D05_D06_D07_MUST_COMPLETE_BEFORE_D_PASS'
 };
}
