// ADR-001 D01: read-only verifier of a fixed master/candidate source inventory.
// All per-path metadata remains SYSTEM_AUDIT; CLI prints only aggregated counters.
// Does not migrate, approve canon, activate runtime, or write Git objects.
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const INVENTORY='novydres/sistema/arquitetura/fase-d/inventario-origens.json';
const SHA=/^[a-f0-9]{40}$/;
const fail=code=>{const error=new Error(code);error.code=code;throw error;};
const need=(valid,code)=>{if(!valid)fail(code);};
const git=(root,args)=>execFileSync('git',args,{cwd:root,encoding:'utf8',maxBuffer:32*1024*1024,stdio:['ignore','pipe','ignore']}).trim();
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
export function classifyD01CandidateOnly(p) {
 let kind,disposition;
 if(p.startsWith('.github/workflows/')){
  kind=p==='.github/workflows/novydres-orchestration.yml'?'LEGACY_WORKFLOW_CANDIDATE_ONLY':'ADR_TEST_WORKFLOW';
  disposition='REWRITE_OR_REMOVE_AFTER_DEPENDENCY_REVIEW';
 }else if(['novydres/AGENTS.md','novydres/CONTEXT.md','novydres/catalogo.json'].includes(p)){
  kind='PROPOSED_ENTRY_OR_DERIVED_CATALOG';disposition='REBUILD_AFTER_FULL_D_MIGRATION';
 }else if(p.startsWith('novydres/cronicas/')||p.startsWith('novydres/personagens/')){
  kind='C41_SCOPE_SUBJECT_PROTOTYPE';disposition='RECONCILE_C45_AUTHORITY_FIELDS_BEFORE_E';
 }else if(p.startsWith('novydres/scripts/')){
  kind=p.endsWith('.test.mjs')||p.split('/').at(-1).startsWith('testar-')?'CANDIDATE_REGRESSION_TEST':'CANDIDATE_DEVELOPMENT_TOOL';
  disposition='REVIEW_FINAL_RUNTIME_DEPENDENCIES_AND_ANTI_LEGACY';
 }else if(p.startsWith('novydres/sistema/arquitetura/')){
  kind='ADR_DESIGN_AND_TEST_EVIDENCE';disposition='REVIEW_STORAGE_LOCATION_NOT_ACTIVE_RUNTIME';
 }else if(p==='novydres/sistema/narrativa/contrato.md'){
  kind='CANDIDATE_NARRATIVE_CONTRACT';disposition='POLICY_SUCCESSION_AND_APPROVAL_PENDING';
 }else{kind='UNCLASSIFIED_CANDIDATE_ARTIFACT';disposition='BLOCKED_PENDING_OWNER_REVIEW';}
 return {kind,disposition,operational_authority:'NOT_GRANTED'};
}
export function listPinnedTree(root,commit) {
 need(SHA.test(commit||''),'D01_COMMIT_PIN_INVALID');
 const content=execFileSync('git',['ls-tree','-r','-z','--full-tree',commit],
  {cwd:root,encoding:'utf8',maxBuffer:32*1024*1024,stdio:['ignore','pipe','ignore']});
 return content.split('\0').filter(Boolean).map(line=>{
  const found=/^(\d{6}) (blob|commit|tree) ([a-f0-9]{40})\t(.+)$/.exec(line);
  need(!!found,'D01_TREE_MALFORMED');
  need(found[2]==='blob','D01_UNSUPPORTED_TREE_ENTRY');
  return {path:found[4],sha:found[3],mode:found[1]};
 });
}
export function collectPins(obj,into=[]) {
 if(!obj||typeof obj!=='object')return into;
 if(typeof obj.path==='string'&&SHA.test(obj.blob_sha||''))
  into.push({path:obj.path,blob_sha:obj.blob_sha});
 for(const value of Object.values(obj))if(value&&typeof value==='object')collectPins(value,into);
 return into;
}
export function describePinnedContent(path,content) {
 need(typeof content==='string','D01_C45_CONTENT_NOT_READ');
 const ext=path.split('.').at(-1).toLowerCase();
 const format=({json:'JSON',md:'MARKDOWN',txt:'TEXT',py:'PYTHON',mjs:'JAVASCRIPT',js:'JAVASCRIPT',yml:'YAML',yaml:'YAML'})[ext]||'UNKNOWN';
 let top_level_keys=[],declared_source_metadata={},heading_count=0;
 if(format==='JSON'){
  const value=JSON.parse(content);
  need(value&&typeof value==='object'&&!Array.isArray(value),'D01_C45_INVALID_SOURCE_JSON');
  top_level_keys=Object.keys(value);
  for(const field of ['classification','visibility','status','schema','schema_id','spoiler_class','scope','phase'])
   if(typeof value[field]==='string'&&value[field].length<=180)
    declared_source_metadata[field]=value[field];
 }else if(format==='MARKDOWN')heading_count=(content.match(/^#{1,6} /gm)||[]).length;
 return {format,utf16_code_units:content.length,top_level_keys,declared_source_metadata,
  heading_count,classification_in_filename:/(?:GM_HIDDEN|PLAYER_SAFE|SYSTEM_AUDIT)/.exec(path)?.[0]||'UNDECLARED'};
}
export function deriveC45Precedence(index,{cycle,sourceContents,candidateState,candidateStateSha}){
 need(candidateState?.not_operational===true,'D01_C41_CANDIDATE_ACTIVATION_NOT_DENIED');
 const current=kind=>{
  const p=cycle.refs?.[kind]?.path;
  need(typeof p==='string'&&sourceContents.has(p),'D01_C45_SOURCE_POINTER_MISSING');
  const value=JSON.parse(sourceContents.get(p));
  need(value&&typeof value==='object'&&!Array.isArray(value),'D01_C45_SOURCE_POINTER_INVALID');
  return value;
 };
 const live=current('live'),hist=current('history_index'),know=current('knowledge'),threads=current('threads');
 const state=candidateState;
 return {
  status:'C45_CURRENT_C41_CANDIDATE_NOT_RECONCILED',
  inspection:'EXACT_GITHUB_BLOB_READBACK_STRUCTURAL_PRIORITY_NOT_FACTUAL_EQUIVALENCE',
  current_master_commit:index.source_snapshot.commit_sha,
  source_cycle_id:cycle.cycle_id,
  source_cycle_sha:index.authority_reference.cycle.blob_sha,
  source_manifest_path:cycle.manifest_ref.path,
  source_manifest_sha:cycle.manifest_ref.blob_sha,
  candidate_state:{
   path:'novydres/cronicas/CHR-001/estado/atual.json',
   sha:candidateStateSha,
   current_runtime:false,
   declared_not_operational:state.not_operational,
   source_cycle_id:state.cycle.id,
   source_cycle_path:state.cycle.path,
   source_cycle_sha:state.cycle.sha,
   source_manifest_ref:state.manifest_ref,
   original_source_commit:state.source_commit,
   source_live:state.source_live
  },
  current_direct_references:Object.fromEntries(Object.entries(cycle.refs).map(([name,x])=>[name,{path:x.path,blob_sha:x.blob_sha}])),
  live_internal_references:{
   history_index_ref:live.history_index_ref,
   knowledge_current_ref:live.knowledge_current_ref,
   open_threads_current_ref:live.open_threads_current_ref
  },
  historical_index_references:{
   knowledge_index_ref:hist.knowledge_index_ref,
   open_threads_ref:hist.open_threads_ref,
   index_coverage:hist.index_coverage,
   technical_ledger_status:hist.technical_ledger_status
  },
  situated_data_counters:{
   npc_knowledge_record_count:Array.isArray(know.records)?know.records.length:null,
   open_threads_count:Array.isArray(threads.threads)?threads.threads.length:null,
   knowledge_status:know.status,
   open_threads_status:threads.status
  },
  reference_evaluation:{
   cycle_live_matches_internal_history:cycle.refs.history_index.path===live.history_index_ref,
   cycle_live_matches_internal_knowledge:cycle.refs.knowledge.path===live.knowledge_current_ref,
   cycle_live_matches_internal_threads:cycle.refs.threads.path===live.open_threads_current_ref,
   current_history_matches_cycle_knowledge:hist.knowledge_index_ref===cycle.refs.knowledge.path,
   current_history_matches_cycle_threads:hist.open_threads_ref===cycle.refs.threads.path,
   candidate_state_uses_current_cycle:state.cycle.id===cycle.cycle_id,
   candidate_state_uses_current_manifest:state.manifest_ref.blob_sha===cycle.manifest_ref.blob_sha
  },
  rules:{
   source_selection:'EXACT_C45_CYCLE_PIN_FIRST',
   old_live_pointer_usage:'HISTORIC_REFERENCE_ONLY_UNLESS_RECONCILED',
   runtime_activation:'PROHIBITED',
   editorial_content_equivalence:'NOT_PROVEN',
   local_knowledge_and_secret_access:'PENDING_EPISTEMIC_REVIEW',
   historical_index_completeness:'PARTIAL_NOT_FULL_REPLAY'
  }
 };
}
export function verifyD01(index,{masterTree,candidateTree,external,media,cycle,sourceContents,candidateState,workflowContents}){
 need(index?.artifact_type==='ADR001_D01_SNAPSHOT_SOURCE_INVENTORY'&&
  index.classification==='SYSTEM_AUDIT_NOT_PLAYER_REPORT'&&
  index.status==='D01_SOURCE_INDEX_COMPLETE_EDITORIAL_MAPPING_PENDING'&&
  index.operational_activation===false&&index.cutover_authorized===false,'D01_AUTHORITY_INVALID');
 const m=index.source_snapshot,d=index.candidate_snapshot;
 need(SHA.test(m?.commit_sha||'')&&SHA.test(m?.tree_sha||'')&&
  SHA.test(d?.commit_sha||'')&&SHA.test(d?.tree_sha||''),'D01_SNAPSHOT_MISSING');
 const source=new Map(),other=new Map();
 for(const row of masterTree){
  need(!source.has(row.path),'D01_DUPLICATE_SOURCE_PATH');
  source.set(row.path,row);
 }
 for(const row of candidateTree){
  need(!other.has(row.path),'D01_DUPLICATE_CANDIDATE_PATH');
  other.set(row.path,row);
 }
 need(m.blobs===masterTree.length&&d.blobs===candidateTree.length,'D01_DENOMINATOR_DRIFT');
 need(Array.isArray(index.source_files)&&index.source_files.length===masterTree.length,'D01_SOURCE_INCOMPLETE');
 const seen=new Set(),counts={same:0,different:0,missing:0};
 for(const row of index.source_files){
  need(!seen.has(row.source_path),'D01_SOURCE_DUPLICATE');seen.add(row.source_path);
  const actual=source.get(row.source_path);
  need(!!actual,'D01_SOURCE_NOT_IN_TREE');
  need(actual.sha===row.source_blob_sha&&actual.mode===row.git_mode,'D01_SOURCE_SHA_MISMATCH');
  need(typeof row.source_family==='string'&&row.source_family.length>0&&
    typeof row.owner_route_candidate==='string'&&row.owner_route_candidate.length>0&&
    typeof row.target_root_candidate==='string'&&row.target_root_candidate.length>0&&
    row.authority_status==='NOT_AUDITED_BY_PATH_INDEX'&&
    row.editorial_equivalence==='PENDING_FIELD_REVIEW','D01_PREMATURE_AUTHORITY');
  const isBinaryEqual=row.candidate_relation==='SAME_PATH_SAME_BLOB';
  need(isBinaryEqual?
   row.binary_ownership_review==='GIT_BLOB_IDENTICAL_OWNER_AND_FIELD_AUTHORITY_NOT_PROVEN':
   !Object.hasOwn(row,'binary_ownership_review'),'D01_SHARED_BLOB_FALSE_AUTHORITY');
  const samePath=other.get(row.source_path);
  const relation=samePath?(samePath.sha===actual.sha?'SAME_PATH_SAME_BLOB':'SAME_PATH_DIFFERENT_BLOB'):'NO_SAME_PATH_IN_CANDIDATE';
  need(row.candidate_relation===relation&&row.candidate_same_path_blob_sha===(samePath?.sha||null),'D01_CANDIDATE_COMPARISON_DRIFT');
  counts[!samePath?'missing':samePath.sha===actual.sha?'same':'different']++;
 }
 need(Array.isArray(index.candidate_only_files),'D01_CANDIDATE_ONLY_ABSENT');
 const only=candidateTree.filter(x=>!source.has(x.path));
 const o=new Map();
 for(const row of index.candidate_only_files){
  need(!o.has(row.path),'D01_CANDIDATE_ONLY_DUPLICATE');o.set(row.path,row);
 }
 need(o.size===only.length,'D01_CANDIDATE_ONLY_INCOMPLETE');
 for(const row of only){
  const recorded=o.get(row.path);
  need(recorded?.blob_sha===row.sha&&recorded?.git_mode===row.mode,'D01_CANDIDATE_ONLY_SHA_MISMATCH');
  const expectedReview=classifyD01CandidateOnly(row.path);
  need(expectedReview.kind!=='UNCLASSIFIED_CANDIDATE_ARTIFACT'&&
   equal(recorded.candidate_review,expectedReview),'D01_CANDIDATE_ONLY_CLASSIFICATION_DRIFT');
 }
 const wf=index.workflow_divergence;
 need(wf?.path==='.github/workflows/novydres-marco-closure-v2.yml'&&
  wf.source_blob_sha===source.get(wf.path)?.sha&&
  wf.candidate_blob_sha===other.get(wf.path)?.sha&&
  wf.source_blob_sha!==wf.candidate_blob_sha&&
  wf.source_behavior==='V2_VALIDATOR_CONDITIONAL_ON_LATEST_CYCLE_SCHEMA'&&
  wf.candidate_behavior==='V2_VALIDATOR_UNCONDITIONAL'&&
  wf.conflict_class==='BLOCKING_FOR_FINAL_CUTOVER_IF_CANDIDATE_WORKFLOW_RETAINED'&&
  wf.final_authority==='NOT_RECONCILED'&&wf.operational_master_modified===false&&
  wf.resolution==='PRESERVE_MASTER_OPERATIONAL_WORKFLOW_UNMODIFIED;REWRITE_OR_REMOVE_LEGACY_WORKFLOW_BEFORE_E',
  'D01_WORKFLOW_CONFLICT_NOT_TRACKED');
 need(typeof workflowContents?.master==='string'&&typeof workflowContents?.candidate==='string'&&
  workflowContents.master.includes('Determine applicability of historical V2 gate')&&
  workflowContents.master.includes("if: steps.applicability.outputs.applicable == 'true'")&&
  !workflowContents.candidate.includes('Determine applicability of historical V2 gate')&&
  workflowContents.candidate.includes('ORCHESTRATION_VALIDATOR_V2.mjs --root .')&&
  workflowContents.master.includes('ORCHESTRATION_VALIDATOR_V2.mjs --root .'),
  'D01_WORKFLOW_BEHAVIOR_WITNESS_DRIFT');
 const shared=index.shared_blob_identity_review;
 need(shared?.count===counts.same&&shared?.editorial_equivalence==='NOT_PROVEN'&&
  shared.current_authority==='NO_AUTOMATIC_PROMOTION_FROM_BINARY_EQUALITY'&&
  shared.dependency_mapping==='PENDING'&&shared.final_destination==='PENDING_RECONCILIATION',
  'D01_SHARED_REVIEW_FALSE_CLOSURE');
 const er=index.controlled_external_registry;
 need(er?.discovery_status===external.discovery_status&&Array.isArray(er.items)&&
   er.items.length===external.items.length,'D01_EXTERNAL_INCOMPLETE');
 need(source.get(er.path)?.sha===er.blob_sha,'D01_EXTERNAL_REGISTRY_UNPINNED');
 for(let i=0;i<external.items.length;i++){
  const expected=external.items[i],actual=er.items[i];
  need(actual?.ordinal===i+1&&actual.source_id===expected.id&&
   actual.reported_scope===(expected.scope||null)&&
   actual.reported_governance_status===(expected.governance_status||null)&&
   actual.reported_migration_state===(expected.migration_state||null)&&
   actual.archived_target===(expected.target||null)&&
   actual.archived_target_sha===(expected.target?(source.get(expected.target)?.sha||null):null)&&
   actual.source_byte_equivalence==='NOT_REVALIDATED_D01'&&
   actual.git_archive_pin_status===(!actual.archived_target?
    'NO_ARCHIVED_TARGET_REPORTED':actual.archived_target_sha?
    'ARCHIVE_PATH_GIT_SHA_PINNED_EXTERNAL_BYTES_UNVERIFIED':
    'ARCHIVED_TARGET_NOT_IN_PINNED_GIT_TREE'),'D01_EXTERNAL_MAPPING_DRIFT');
 }
 const mr=index.visual_registry;
 need(source.get(mr?.path)?.sha===mr.blob_sha&&Array.isArray(mr.entries)&&
   mr.entries.length===media.entries.length,'D01_MEDIA_INCOMPLETE');
 for(let i=0;i<media.entries.length;i++){
  const expected=media.entries[i],actual=mr.entries[i];
  need(actual?.ordinal===i+1&&actual.library_id===(expected.library_id||null)&&
   actual.raw_original_migrated_reported===(expected.raw_original_migrated===true)&&
   actual.drive_sha256_verified_reported===(expected.drive_sha256_verified===true)&&
   actual.drive_id_present===!!expected.drive_file_id&&
   actual.drive_url_present===!!expected.drive_url&&
   actual.external_original_bytes_verified_in_D01===false,'D01_MEDIA_MAPPING_DRIFT');
 }
 const anchor=index.authority_reference;
 need(anchor?.operative_cycle===cycle.cycle_id&&
  anchor.source_commit_ref_from_cycle===cycle.source_head_sha&&
  anchor.cycle?.blob_sha===source.get(anchor.cycle.path)?.sha&&
  anchor.manifest?.path===cycle.manifest_ref.path&&
  anchor.manifest.blob_sha===cycle.manifest_ref.blob_sha&&
  source.get(anchor.manifest.path)?.sha===anchor.manifest.blob_sha&&
  anchor.previous_cycle?.path===cycle.previous_cycle.path&&
  anchor.previous_cycle.blob_sha===cycle.previous_cycle.blob_sha,'D01_CYCLE_MISMATCH');
 const pins=collectPins(cycle);
 need(equal(pins,anchor.pinned_references),'D01_PINS_CHANGED');
 for(const pin of pins)need(source.get(pin.path)?.sha===pin.blob_sha,'D01_PIN_BLOB_MISSING');
 const cyclePinKeys=new Map();
 for(const p of pins){
  const prior=cyclePinKeys.get(p.path);
  need(prior===undefined||prior===p.blob_sha,'D01_CYCLE_PIN_CONFLICT');
  cyclePinKeys.set(p.path,p.blob_sha);
 }
 const pinRelations={missing:0,same:0,different:0},pinRows=new Set();
 for(const row of index.source_files){
  if(cyclePinKeys.has(row.source_path)){
   pinRows.add(row.source_path);
   need(row.pinned_by_operational_cycle==='PINNED_C45_SOURCE','D01_CURRENT_PIN_UNTRACKED');
   const relation=row.candidate_relation==='NO_SAME_PATH_IN_CANDIDATE'?'SOURCE_NOT_IN_CANDIDATE':
    row.candidate_relation==='SAME_PATH_SAME_BLOB'?'SOURCE_SAME_BLOB':'SAME_PATH_DIFFERENT_CONTENT';
   need(row.current_cycle_candidate_reconciliation===relation,'D01_CURRENT_PIN_MISCLASSIFIED');
   pinRelations[relation==='SOURCE_NOT_IN_CANDIDATE'?'missing':
    relation==='SOURCE_SAME_BLOB'?'same':'different']++;
  }else need(!Object.hasOwn(row,'pinned_by_operational_cycle')&&
   !Object.hasOwn(row,'current_cycle_candidate_reconciliation'),'D01_FALSE_CURRENT_PIN');
 }
 need(pinRows.size===cyclePinKeys.size,'D01_CURRENT_PIN_INCOMPLETE');
 const pinnedMissing=index.source_files.filter(row=>row.current_cycle_candidate_reconciliation==='SOURCE_NOT_IN_CANDIDATE');
 need(sourceContents instanceof Map,'D01_C45_CONTENT_COLLECTION_MISSING');
 let structurallyInspected=0;
 const targetPattern=/^novydres\/(?:cronicas\/CHR-001(?:\/.*)?|sistema\/narrativa(?:\/.*)?|personagens(?:\/.*)?|scripts(?:\/.*)?)$/;
 for(const row of index.source_files){
  const info=row.c45_content_reconciliation;
  if(row.current_cycle_candidate_reconciliation==='SOURCE_NOT_IN_CANDIDATE'){
   need(info?.inspection_status==='STRUCTURAL_SOURCE_READBACK_NOT_SEMANTIC_APPROVAL',
    'D01_C45_INSPECTION_MISSING');
   need(info.derived_authority==='UNVERIFIED_SOURCE_DECLARATION'&&
    info.editorial_review==='PENDING'&&info.epistemic_and_visibility_review==='PENDING'&&
    info.target_materialized_in_candidate===false&&
    info.content_equivalence_to_target==='NOT_PROVEN','D01_C45_FALSE_APPROVAL');
   need(typeof info.proposed_owner==='string'&&info.proposed_owner.length>0&&
    typeof info.transformation_proposal==='string'&&info.transformation_proposal.length>0,
    'D01_C45_ROUTING_INCOMPLETE');
   need(typeof info.proposed_target_root==='string'&&
    info.proposed_target_root.split('|').every(x=>targetPattern.test(x)),
    'D01_C45_LEGACY_OR_UNSAFE_DESTINATION');
   if(row.source_path.includes('/knowledge/OPEN_THREADS_'))
    need(info.proposed_target_root==='novydres/cronicas/CHR-001/fios',
     'D01_C45_THREADS_OWNER_DRIFT');
   if(row.source_path.includes('/knowledge/NPC_KNOWLEDGE_'))
    need(info.proposed_target_root==='novydres/cronicas/CHR-001/elenco',
     'D01_C45_KNOWLEDGE_OWNER_DRIFT');
   if(row.source_path.includes('/D07_STORY_TRUTH_PACKAGE_'))
    need(info.proposed_target_root==='novydres/cronicas/CHR-001/tramas',
     'D01_C45_GM_TRUTH_OWNER_DRIFT');
   const original=sourceContents.get(row.source_path);
   need(typeof original==='string','D01_C45_CONTENT_NOT_READ');
   need(equal(info.source_content_structure,describePinnedContent(row.source_path,original)),
    'D01_C45_CONTENT_METADATA_DRIFT');
   structurallyInspected++;
  }else need(info===undefined,'D01_C45_NONMISSING_SPOOFED_INSPECTION');
 }
 need(structurallyInspected===pinnedMissing.length,'D01_C45_INSPECTION_COVERAGE_DRIFT');
 const noncurrentMissing=index.source_files.filter(row=>row.candidate_relation==='NO_SAME_PATH_IN_CANDIDATE'&&!row.pinned_by_operational_cycle);
 let otherStructurallyInspected=0;
 for(const row of index.source_files){
  const info=row.noncurrent_missing_inspection;
  const eligible=row.candidate_relation==='NO_SAME_PATH_IN_CANDIDATE'&&!row.pinned_by_operational_cycle;
  if(eligible){
   need(info?.inspection_status==='STRUCTURAL_SOURCE_READBACK_NOT_SEMANTIC_APPROVAL'&&
    info.cycle_pin_relation==='NOT_DIRECTLY_PINNED_BY_C45_OTHER_DEPENDENCIES_UNCHECKED'&&
    info.proposed_target_root===row.target_root_candidate&&
    info.owner_final==='NOT_DETERMINED'&&
    info.history_or_current==='NOT_DETERMINED_BY_PIN_ABSENCE'&&
    info.authority_review==='PENDING'&&
    info.epistemic_and_visibility_review==='PENDING'&&
    info.content_equivalence_to_target==='NOT_PROVEN'&&
    info.safe_to_remove_from_final_head==='NOT_PROVEN',
    'D01_NONCURRENT_FALSE_AUTHORITY');
   const original=sourceContents.get(row.source_path);
   need(typeof original==='string','D01_NONCURRENT_CONTENT_NOT_READ');
   need(equal(info.source_content_structure,describePinnedContent(row.source_path,original)),
    'D01_NONCURRENT_CONTENT_METADATA_DRIFT');
   otherStructurallyInspected++;
  }else need(info===undefined,'D01_NONCURRENT_SPOOFED_INSPECTION');
 }
 need(sourceContents.size===pinnedMissing.length+noncurrentMissing.length&&
  otherStructurallyInspected===noncurrentMissing.length,
  'D01_NONCURRENT_COVERAGE_DRIFT');

 const candidateStatePath='novydres/cronicas/CHR-001/estado/atual.json';
 const candidateStateSha=other.get(candidateStatePath)?.sha;
 need(SHA.test(candidateStateSha||''),'D01_C41_STATE_CANDIDATE_MISSING');
 need(candidateState&&typeof candidateState==='object','D01_C41_STATE_SOURCE_NOT_READ');
 const expectedCrosswalk=deriveC45Precedence(index,{cycle,sourceContents,candidateState,candidateStateSha});
 need(equal(index.c45_candidate_state_precedence_crosswalk,expectedCrosswalk),
  'D01_C45_PRECEDENCE_CROSSWALK_DRIFT');
 const evaluation=expectedCrosswalk.reference_evaluation;
 need(evaluation.current_history_matches_cycle_knowledge===true&&
  evaluation.current_history_matches_cycle_threads===true,'D01_C45_HISTORY_CHAIN_DRIFT');
 need(evaluation.cycle_live_matches_internal_history===false&&
  evaluation.cycle_live_matches_internal_knowledge===false&&
  evaluation.cycle_live_matches_internal_threads===false&&
  evaluation.candidate_state_uses_current_cycle===false&&
  evaluation.candidate_state_uses_current_manifest===false,
  'D01_C45_EXPECTED_HISTORY_DIFFERENCE_CHANGED');
 const summary=index.denominators;
 need(summary?.cycle_unique_pinned_paths===pinRows.size&&
  summary.cycle_pinned_paths_missing_in_candidate===pinRelations.missing&&
  summary.cycle_pinned_paths_same_blob===pinRelations.same&&
  summary.cycle_pinned_paths_changed===pinRelations.different,'D01_PIN_SUMMARY_MISMATCH');
 need(summary?.c45_missing_pin_content_inspections===structurallyInspected&&
  summary.c45_missing_pin_routing_proposals===structurallyInspected,
  'D01_C45_INSPECTION_DENOMINATOR_DRIFT');
 need(summary?.noncurrent_missing_structurally_inspected===otherStructurallyInspected&&
  summary.master_missing_structurally_inspected===otherStructurallyInspected+structurallyInspected,
  'D01_ALL_MISSING_SOURCE_DENOMINATOR_DRIFT');
 need(summary?.c45_source_priority_mismatches===Object.values(evaluation).filter(x=>x===false).length,
  'D01_C45_PRIORITY_DENOMINATOR_DRIFT');
 need(summary?.master_blobs===masterTree.length&&summary.candidate_blobs===candidateTree.length&&
  summary.same_path_equal_blob===counts.same&&summary.same_path_changed_blob===counts.different&&
  summary.master_without_candidate_same_path===counts.missing&&summary.candidate_only===only.length&&
  summary.external_records===external.items.length&&summary.media_records===media.entries.length&&
  summary.media_originals_pending===media.entries.filter(x=>x.raw_original_migrated!==true).length&&
  summary.media_sha_unverified===media.entries.filter(x=>x.drive_sha256_verified!==true).length&&
  summary.cycle_pinned_refs===pins.length,'D01_SUMMARY_MISMATCH');
 need(Array.isArray(index.gate_requirements_pending)&&index.gate_requirements_pending.length>0,
  'D01_FALSE_GATE_CLOSURE');
 return {gate:'D01_STRUCTURE_VERIFIED_EDITORIAL_PENDING',source_blobs:source.size,candidate_blobs:other.size,
  same_path_same_blob:counts.same,same_path_changed_blob:counts.different,
  source_without_candidate_path:counts.missing,candidate_only:only.length,
  external_items:external.items.length,media_items:media.entries.length,cycle_pins:pins.length,
  cycle_unique_pinned_paths:pinRows.size,cycle_pins_missing_candidate:pinRelations.missing,
  cycle_pins_same_candidate:pinRelations.same,
  c45_missing_source_content_structurally_inspected:structurallyInspected,
  noncurrent_missing_structurally_inspected:otherStructurallyInspected,
  all_master_only_sources_inspected:structurallyInspected+otherStructurallyInspected,
  candidate_checkpoint:expectedCrosswalk.candidate_state.source_cycle_id,
  current_checkpoint:expectedCrosswalk.source_cycle_id,
  state_precedence_mismatches:summary.c45_source_priority_mismatches,
  editorial_approval:'NOT_PROVEN',runtime_activation:false};
}
export function readAndVerifyD01(root=process.cwd()){
 const index=JSON.parse(readFileSync(resolve(root,INVENTORY),'utf8'));
 const sha=(commit)=>git(root,['rev-parse',commit+'^{tree}']);
 need(sha(index.source_snapshot.commit_sha)===index.source_snapshot.tree_sha,'D01_MASTER_TREE_MISMATCH');
 need(sha(index.candidate_snapshot.commit_sha)===index.candidate_snapshot.tree_sha,'D01_CANDIDATE_TREE_MISMATCH');
 const masterTree=listPinnedTree(root,index.source_snapshot.commit_sha);
 const candidateTree=listPinnedTree(root,index.candidate_snapshot.commit_sha);
 const read=path=>JSON.parse(git(root,['show',index.source_snapshot.commit_sha+':'+path]));
 const sourceContents=new Map(index.source_files.filter(row=>
  row.candidate_relation==='NO_SAME_PATH_IN_CANDIDATE').map(row=>[
   row.source_path,execFileSync('git',['show',index.source_snapshot.commit_sha+':'+row.source_path],
    {cwd:root,encoding:'utf8',maxBuffer:32*1024*1024,stdio:['ignore','pipe','ignore']})]));
 return verifyD01(index,{masterTree,candidateTree,
  external:read(index.controlled_external_registry.path),
  media:read(index.visual_registry.path),
  cycle:read(index.authority_reference.cycle.path),sourceContents,
  candidateState:JSON.parse(git(root,['show',index.candidate_snapshot.commit_sha+
   ':novydres/cronicas/CHR-001/estado/atual.json'])),
  workflowContents:{
   master:git(root,['show',index.source_snapshot.commit_sha+':.github/workflows/novydres-marco-closure-v2.yml']),
   candidate:git(root,['show',index.candidate_snapshot.commit_sha+':.github/workflows/novydres-marco-closure-v2.yml'])
  }});
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))
 console.log(JSON.stringify(readAndVerifyD01()));
