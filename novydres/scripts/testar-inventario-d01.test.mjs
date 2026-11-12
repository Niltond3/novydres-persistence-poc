// D01 regressions work against committed immutable Git trees, no write or scene.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {verifyD01,listPinnedTree,readAndVerifyD01,summarizeD01ObservedRefs} from './verificar-inventario-d01.mjs';
const root=process.cwd();
const index=JSON.parse(readFileSync('novydres/sistema/arquitetura/fase-d/inventario-origens.json','utf8'));
const pinned=index.source_snapshot.commit_sha;
const read=p=>JSON.parse(execFileSync('git',['show',pinned+':'+p],{encoding:'utf8',maxBuffer:32*1024*1024}));
const readFromCandidateState=()=>JSON.parse(execFileSync('git',['show',index.candidate_snapshot.commit_sha+':novydres/cronicas/CHR-001/estado/atual.json'],{encoding:'utf8',maxBuffer:32*1024*1024}));
const data={masterTree:listPinnedTree(root,pinned),
 candidateTree:listPinnedTree(root,index.candidate_snapshot.commit_sha),
 external:read(index.controlled_external_registry.path),
 media:read(index.visual_registry.path),
 cycle:read(index.authority_reference.cycle.path),
 candidateState:readFromCandidateState(),
 workflowContents:{
  master:execFileSync('git',['show',pinned+':.github/workflows/novydres-marco-closure-v2.yml'],{encoding:'utf8',maxBuffer:32*1024*1024}),
  candidate:execFileSync('git',['show',index.candidate_snapshot.commit_sha+':.github/workflows/novydres-marco-closure-v2.yml'],{encoding:'utf8',maxBuffer:32*1024*1024})
 },
 sourceContents:new Map(index.source_files.filter(row=>
  row.candidate_relation==='NO_SAME_PATH_IN_CANDIDATE'||
  row.priority_shared_content_review).map(row=>[
  row.source_path,execFileSync('git',['show',pinned+':'+row.source_path],
  {encoding:'utf8',maxBuffer:32*1024*1024})]))};
const clone=()=>structuredClone(index);
const reject=(mutate,code)=>{const x=clone();mutate(x);assert.throws(()=>verifyD01(x,data),e=>e.code===code);};
test('D01 whole-tree fixed baseline, 1029/923 blobs and no editorial PASS',()=>{
 const r=readAndVerifyD01(root);
 assert.equal(r.gate,'D01_STRUCTURE_VERIFIED_EDITORIAL_PENDING');
 assert.equal(r.source_blobs,1029);assert.equal(r.candidate_blobs,923);
 assert.equal(r.external_items,193);assert.equal(r.media_items,19);
 assert.equal(r.cycle_pins,77);assert.equal(r.runtime_activation,false);
 assert.equal(r.c45_missing_source_content_structurally_inspected,53);
 assert.equal(r.noncurrent_missing_structurally_inspected,136);
 assert.equal(r.all_master_only_sources_inspected,189);
 assert.equal(r.editorial_approval,'NOT_PROVEN');
});
test('D01 missing original path fails, not a reduced denominator',()=>{
 reject(x=>x.source_files.pop(),'D01_SOURCE_INCOMPLETE');
});
test('D01 source path duplicate fails',()=>{
 reject(x=>x.source_files[1]=structuredClone(x.source_files[0]),'D01_SOURCE_DUPLICATE');
});
test('D01 source blob substitution fails, even with identical filename',()=>{
 reject(x=>x.source_files[0].source_blob_sha='0'.repeat(40),'D01_SOURCE_SHA_MISMATCH');
});
test('D01 cannot relabel unreviewed editorial authority as approved',()=>{
 reject(x=>x.source_files[0].authority_status='APPROVED','D01_PREMATURE_AUTHORITY');
});
test('D01 cannot hide missing master path from candidate or invent match',()=>{
 const i=index.source_files.findIndex(x=>x.candidate_relation==='NO_SAME_PATH_IN_CANDIDATE');
 assert.ok(i>=0);
 reject(x=>x.source_files[i].candidate_relation='SAME_PATH_SAME_BLOB','D01_CANDIDATE_COMPARISON_DRIFT');
});
test('D01 candidate-only inventory cannot omit a source',()=>{
 reject(x=>x.candidate_only_files.shift(),'D01_CANDIDATE_ONLY_INCOMPLETE');
});
test('D01 registry external ID cannot be exchanged without provenance',()=>{
 reject(x=>x.controlled_external_registry.items[0].source_id='TEST_INVALID','D01_EXTERNAL_MAPPING_DRIFT');
});
test('D01 media pending flag cannot be reported verified by convenience',()=>{
 reject(x=>x.visual_registry.entries[0].drive_sha256_verified_reported=true,'D01_MEDIA_MAPPING_DRIFT');
});
test('D01 cannot silently detach the active operational cycle and source pins',()=>{
 reject(x=>x.authority_reference.pinned_references[0].blob_sha='0'.repeat(40),'D01_PINS_CHANGED');
});
test('D01 C45 active pins uniquely reconciled and missing candidate paths cannot be silently marked present',()=>{
 const observed=verifyD01(index,data);
 assert.equal(observed.cycle_pins,77);
 assert.equal(observed.cycle_unique_pinned_paths,73);
 assert.equal(observed.cycle_pins_missing_candidate,53);
 assert.equal(observed.cycle_pins_same_candidate,20);
 const i=index.source_files.findIndex(x=>x.current_cycle_candidate_reconciliation==='SOURCE_NOT_IN_CANDIDATE');
 assert.ok(i>=0);
 reject(x=>x.source_files[i].current_cycle_candidate_reconciliation='SOURCE_SAME_BLOB',
  'D01_CURRENT_PIN_MISCLASSIFIED');
 reject(x=>delete x.source_files[i].pinned_by_operational_cycle,'D01_CURRENT_PIN_UNTRACKED');
});
test('D01 no false success when gate pending list disappears',()=>{
 reject(x=>x.gate_requirements_pending=[],'D01_FALSE_GATE_CLOSURE');
});

test('D01 all 53 absent operational pins require immutable content evidence',()=>{
 const p=index.source_files.find(x=>x.c45_content_reconciliation)?.source_path;
 assert.ok(p);
 reject(x=>delete x.source_files.find(row=>row.source_path===p).c45_content_reconciliation,
  'D01_C45_INSPECTION_MISSING');
});
test('D01 content keys/status cannot drift from the exact master blob',()=>{
 const p=index.source_files.find(x=>x.c45_content_reconciliation?.source_content_structure.format==='JSON')?.source_path;
 assert.ok(p);
 reject(x=>x.source_files.find(row=>row.source_path===p).c45_content_reconciliation.source_content_structure.top_level_keys.push('FAKE_KEY'),
  'D01_C45_CONTENT_METADATA_DRIFT');
});
test('D01 cannot declare editorial equivalence or destination materialized',()=>{
 const p=index.source_files.find(x=>x.c45_content_reconciliation)?.source_path;
 assert.ok(p);
 reject(x=>x.source_files.find(row=>row.source_path===p).c45_content_reconciliation.editorial_review='APPROVED',
  'D01_C45_FALSE_APPROVAL');
 reject(x=>x.source_files.find(row=>row.source_path===p).c45_content_reconciliation.target_materialized_in_candidate=true,
  'D01_C45_FALSE_APPROVAL');
});
test('D01 forbids routing a new pinned source back into legacy paths',()=>{
 const p=index.source_files.find(x=>x.c45_content_reconciliation)?.source_path;
 assert.ok(p);
 reject(x=>x.source_files.find(row=>row.source_path===p).c45_content_reconciliation.proposed_target_root='novydres/runtime',
  'D01_C45_LEGACY_OR_UNSAFE_DESTINATION');
});
test('D01 distinguishes open plot threads from NPC knowledge owner',()=>{
 const p=index.source_files.find(x=>x.c45_content_reconciliation&&x.source_path.includes('/knowledge/OPEN_THREADS_'))?.source_path;
 assert.ok(p);
 reject(x=>x.source_files.find(row=>row.source_path===p).c45_content_reconciliation.proposed_target_root='novydres/cronicas/CHR-001/elenco',
  'D01_C45_THREADS_OWNER_DRIFT');
});
test('D01 cannot fabricate source readback by deleting content',()=>{
 const p=index.source_files.find(x=>x.c45_content_reconciliation)?.source_path;
 assert.ok(p);
 const bad=new Map(data.sourceContents);
 bad.delete(p);
 assert.throws(()=>verifyD01(index,{...data,sourceContents:bad}),e=>e.code==='D01_C45_CONTENT_NOT_READ');
});

test('D01 keeps local NPC knowledge separate from the open-plot-threads owner',()=>{
 const p=index.source_files.find(x=>x.c45_content_reconciliation&&x.source_path.includes('/knowledge/NPC_KNOWLEDGE_'))?.source_path;
 assert.ok(p);
 reject(x=>x.source_files.find(row=>row.source_path===p).c45_content_reconciliation.proposed_target_root='novydres/cronicas/CHR-001/fios',
  'D01_C45_KNOWLEDGE_OWNER_DRIFT');
});
test('D01 restricted story truth cannot be routed into public chronicle state',()=>{
 const p=index.source_files.find(x=>x.c45_content_reconciliation&&x.source_path.includes('/D07_STORY_TRUTH_PACKAGE_'))?.source_path;
 assert.ok(p);
 reject(x=>x.source_files.find(row=>row.source_path===p).c45_content_reconciliation.proposed_target_root='novydres/cronicas/CHR-001/estado',
  'D01_C45_GM_TRUTH_OWNER_DRIFT');
});

test('D01 active C45 cycle has precedence over archived C41 candidate state',()=>{
 const observed=verifyD01(index,data);
 assert.equal(observed.candidate_checkpoint,'CHR001-CYCLE-0041');
 assert.equal(observed.current_checkpoint,'CHR001-CYCLE-0045');
 assert.equal(observed.state_precedence_mismatches,5);
 assert.equal(observed.editorial_approval,'NOT_PROVEN');
});
test('D01 old LIVE refs cannot silently supersede C45 pinned knowledge and threads',()=>{
 const x=index.c45_candidate_state_precedence_crosswalk.reference_evaluation;
 assert.equal(x.cycle_live_matches_internal_knowledge,false);
 assert.equal(x.cycle_live_matches_internal_threads,false);
 assert.equal(x.current_history_matches_cycle_knowledge,true);
 assert.equal(x.current_history_matches_cycle_threads,true);
 reject(y=>y.c45_candidate_state_precedence_crosswalk.rules.source_selection='LIVE_INTERNAL_POINTER_FIRST',
   'D01_C45_PRECEDENCE_CROSSWALK_DRIFT');
});
test('D01 current knowledge/thread coverage counters cannot be invented',()=>{
 reject(y=>y.c45_candidate_state_precedence_crosswalk.situated_data_counters.open_threads_count+=1,
  'D01_C45_PRECEDENCE_CROSSWALK_DRIFT');
 reject(y=>y.c45_candidate_state_precedence_crosswalk.situated_data_counters.npc_knowledge_record_count-=1,
  'D01_C45_PRECEDENCE_CROSSWALK_DRIFT');
});
test('D01 C41 candidate state cannot be passed off as operational',()=>{
 reject(y=>y.c45_candidate_state_precedence_crosswalk.candidate_state.current_runtime=true,
  'D01_C45_PRECEDENCE_CROSSWALK_DRIFT');
 const state=structuredClone(data.candidateState);state.not_operational=false;
 assert.throws(()=>verifyD01(index,{...data,candidateState:state}),
  e=>e.code==='D01_C41_CANDIDATE_ACTIVATION_NOT_DENIED');
});
test('D01 no downgrade of current history partial coverage to full',()=>{
 reject(y=>y.c45_candidate_state_precedence_crosswalk.historical_index_references.index_coverage='COMPLETE',
  'D01_C45_PRECEDENCE_CROSSWALK_DRIFT');
});

test('D01 all 136 sources missing from candidate but not directly pinned by C45 have content evidence',()=>{
 const p=index.source_files.find(x=>x.noncurrent_missing_inspection)?.source_path;
 assert.ok(p);
 reject(x=>delete x.source_files.find(row=>row.source_path===p).noncurrent_missing_inspection,
  'D01_NONCURRENT_FALSE_AUTHORITY');
});
test('D01 nonpinned cannot be promoted to unused or safe to delete',()=>{
 const p=index.source_files.find(x=>x.noncurrent_missing_inspection)?.source_path;
 assert.ok(p);
 reject(x=>x.source_files.find(row=>row.source_path===p).noncurrent_missing_inspection.safe_to_remove_from_final_head=true,
  'D01_NONCURRENT_FALSE_AUTHORITY');
});
test('D01 nonpinned source keys cannot change and still pass immutable source check',()=>{
 const p=index.source_files.find(x=>x.noncurrent_missing_inspection?.source_content_structure.format==='JSON')?.source_path;
 assert.ok(p);
 reject(x=>x.source_files.find(row=>row.source_path===p).noncurrent_missing_inspection.source_content_structure.top_level_keys.push('FAKE'),
  'D01_NONCURRENT_CONTENT_METADATA_DRIFT');
});
test('D01 nonpinned source content absent is fail-closed',()=>{
 const p=index.source_files.find(x=>x.noncurrent_missing_inspection)?.source_path;
 assert.ok(p);
 const sourceContents=new Map(data.sourceContents);
 sourceContents.delete(p);
 assert.throws(()=>verifyD01(index,{...data,sourceContents}),
  e=>e.code==='D01_NONCURRENT_CONTENT_NOT_READ');
});

test('D01 shared unchanged SHA is not proof of authority or destination',()=>{
 const p=index.source_files.find(x=>x.binary_ownership_review)?.source_path;
 assert.ok(p);
 reject(x=>x.source_files.find(r=>r.source_path===p).binary_ownership_review='APPROVED',
  'D01_SHARED_BLOB_FALSE_AUTHORITY');
 reject(x=>x.shared_blob_identity_review.editorial_equivalence='PROVEN',
  'D01_SHARED_REVIEW_FALSE_CLOSURE');
});
test('D01 candidate-only type and cutover disposition cannot be silently promoted',()=>{
 const p=index.candidate_only_files.find(x=>x.candidate_review)?.path;
 assert.ok(p);
 reject(x=>x.candidate_only_files.find(r=>r.path===p).candidate_review.operational_authority='ACTIVE',
  'D01_CANDIDATE_ONLY_CLASSIFICATION_DRIFT');
});
test('D01 divergent historical workflow cannot be approved without resolution',()=>{
 reject(x=>x.workflow_divergence.final_authority='APPROVED',
  'D01_WORKFLOW_CONFLICT_NOT_TRACKED');
 const witness={...data.workflowContents,candidate:data.workflowContents.master};
 assert.throws(()=>verifyD01(index,{...data,workflowContents:witness}),
  e=>e.code==='D01_WORKFLOW_BEHAVIOR_WITNESS_DRIFT');
});
test('D01 external Git archived path does not prove original external bytes',()=>{
 reject(x=>x.controlled_external_registry.items[0].git_archive_pin_status='EXTERNAL_BYTES_VERIFIED',
  'D01_EXTERNAL_MAPPING_DRIFT');
});

test('D01 governance and shared C45 pins have immutable structural content evidence',()=>{
 const r=verifyD01(index,data);
 assert.equal(r.shared_priority_content_inspected,47);
 const p=index.source_files.find(x=>x.priority_shared_content_review)?.source_path;
 assert.ok(p);
 reject(x=>delete x.source_files.find(y=>y.source_path===p).priority_shared_content_review,
  'D01_PRIORITY_SHARED_FALSE_APPROVAL');
});
test('D01 shared priority content metadata cannot be invented',()=>{
 const p=index.source_files.find(x=>x.priority_shared_content_review)?.source_path;
 assert.ok(p);
 reject(x=>x.source_files.find(y=>y.source_path===p).priority_shared_content_review.source_content_structure.utf16_code_units+=3,
  'D01_PRIORITY_SHARED_SOURCE_CONTENT_DRIFT');
});
test('D01 priority original bytes must exist and cannot be called approved',()=>{
 const p=index.source_files.find(x=>x.priority_shared_content_review)?.source_path;
 const bad=new Map(data.sourceContents);bad.delete(p);
 assert.throws(()=>verifyD01(index,{...data,sourceContents:bad}),e=>e.code==='D01_PRIORITY_SHARED_READBACK_MISSING');
 reject(x=>x.priority_shared_content_summary.source_authority='APPROVED',
  'D01_PRIORITY_SHARED_FALSE_AUTHORITY');
});

test('D01 C45 versus C41 pinned checkpoint fields expose drift without disclosure',()=>{
 const o=verifyD01(index,data);
 assert.deepEqual(o.field_value_comparison,
  {checkpoint_match:6,checkpoint_drift:3,resources_match:8,resources_drift:0});
 assert.equal(index.c45_field_value_reconciliation.matching_values_are_approval,false);
});
test('D01 cannot disguise narrative checkpoint drift as field match',()=>{
 const candidate=index.c45_field_value_reconciliation.checkpoint.fields.find(x=>x.value_relation==='DRIFT_CURRENT_C45_PRECEDES_C41');
 assert.ok(candidate);
 reject(x=>x.c45_field_value_reconciliation.checkpoint.fields.find(y=>y.source_field===candidate.source_field).value_relation='SAME_VALUE_NOT_AUTHORITY_PROOF',
  'D01_C45_FIELD_VALUE_CROSSWALK_DRIFT');
});
test('D01 matching resources do not grant runtime authority',()=>{
 reject(x=>x.c45_field_value_reconciliation.matching_values_are_approval=true,
  'D01_C45_FIELD_VALUE_CROSSWALK_DRIFT');
 const altered=structuredClone(data.candidateState);
 altered.resources.xp_spent+=1;
 assert.throws(()=>verifyD01(index,{...data,candidateState:altered}),
  e=>e.code==='D01_C45_FIELD_VALUE_CROSSWALK_DRIFT');
});
test('D01 current pinned LIVE bytes cannot be omitted to fake comparisons',()=>{
 const p=data.cycle.refs.live.path;
 const omitted=new Map(data.sourceContents);
 omitted.delete(p);
 assert.throws(()=>verifyD01(index,{...data,sourceContents:omitted}),
  e=>e.code==='D01_C45_CONTENT_NOT_READ');
});
test('D01 C41 checkpoint cannot be promoted by rewriting historical comparison',()=>{
 const altered=structuredClone(data.candidateState);
 altered.checkpoint.next_scene=data.cycle.checkpoint.next_scene;
 assert.throws(()=>verifyD01(index,{...data,candidateState:altered}),
  e=>e.code==='D01_C45_FIELD_VALUE_CROSSWALK_DRIFT');
});

test('D01 manifest runtime referenced objects are classified by path and pin without promoting usage',()=>{
 const observed=verifyD01(index,data);
 assert.deepEqual(observed.manifest_runtime_references,
  {occurrences:303,distinct_missing_candidate:90,missing_without_direct_pin:38});
 assert.equal(index.c45_manifest_runtime_references.no_operational_activation,true);
});
test('D01 must not erase a manifest non-direct reference absent in the candidate',()=>{
 const entry=index.c45_manifest_runtime_references.items.find(x=>
  x.relation==='SOURCE_FILE_ABSENT_FROM_CANDIDATE'&&!x.directly_pinned_by_c45);
 assert.ok(entry);
 reject(x=>x.c45_manifest_runtime_references.items.find(y=>y.field===entry.field).relation='SOURCE_CANDIDATE_IDENTICAL_BLOB',
  'D01_MANIFEST_RUNTIME_REFERENCE_DRIFT');
});
test('D01 manifest directory prefix is not an absent file blob',()=>{
 const row=index.c45_manifest_runtime_references.items.find(x=>x.relation==='SOURCE_DIRECTORY_PREFIX_EXISTS');
 assert.ok(row);
 reject(x=>x.c45_manifest_runtime_references.items.find(y=>y.field===row.field).relation='SOURCE_REFERENCE_NOT_IN_MASTER',
  'D01_MANIFEST_RUNTIME_REFERENCE_DRIFT');
});
test('D01 no automatic activation from an arbitrary referenced manifest string',()=>{
 reject(x=>x.c45_manifest_runtime_references.items[0].authority='CURRENT_OPERATIONAL_DEPENDENCY_VERIFIED',
  'D01_MANIFEST_RUNTIME_REFERENCE_DRIFT');
 reject(x=>x.c45_manifest_runtime_references.full_field_owner_review='APPROVED',
  'D01_MANIFEST_RUNTIME_REFERENCE_DRIFT');
});

test('D01 all 1029 origins have provenance-linked owner and destination proposals',()=>{
 const r=verifyD01(index,data);
 assert.equal(r.origin_routes_mapped,1029);
 assert.equal(r.origin_routes_field_scope_split,463);
 assert.equal(index.d01_origin_mapping_coverage.content_field_ownership_approved,false);
});
test('D01 mixed owner split must not be silently reduced to a file copy',()=>{
 const source=index.source_files.find(x=>x.d01_origin_route.owner_routing==='FIELD_SCOPE_SPLIT_REQUIRED');
 assert.ok(source);
 reject(x=>x.source_files.find(y=>y.source_path===source.source_path).d01_origin_route.owner_roots_proposed.pop(),
  'D01_ORIGIN_MAPPING_FIELD_DRIFT');
});
test('D01 executable validators are routed to scripts instead of narrative facts',()=>{
 const source=index.source_files.find(x=>x.d01_origin_route.information_kind==='EXECUTABLE_VALIDATOR');
 assert.ok(source);
 assert.equal(source.d01_origin_route.owner_roots_proposed[0],'novydres/scripts/validadores');
 reject(x=>x.source_files.find(y=>y.source_path===source.source_path).d01_origin_route.owner_roots_proposed[0]='novydres/cronicas/CHR-001',
  'D01_ORIGIN_MAPPING_FIELD_DRIFT');
});
test('D01 source name cannot falsely grant PLAYER_SAFE to unreviewed content',()=>{
 const source=index.source_files.find(x=>x.d01_origin_route.disclosure_status==='RESTRICTED_UNTIL_CLASSIFIED');
 assert.ok(source);
 reject(x=>x.source_files.find(y=>y.source_path===source.source_path).d01_origin_route.disclosure_status='PLAYER_SAFE',
  'D01_ORIGIN_MAPPING_FIELD_DRIFT');
});
test('D01 no source omitted or field-level editorial authority accidentally approved',()=>{
 reject(x=>x.d01_origin_mapping_coverage.mapped_source_paths-=1,'D01_ORIGIN_MAPPING_COVERAGE_DRIFT');
 reject(x=>x.d01_origin_mapping_coverage.content_field_ownership_approved=true,
  'D01_ORIGIN_MAPPING_COVERAGE_DRIFT');
});

test('D01 safe scan token parsing is a textual hint, never authority or absence proof',()=>{
 const sha=index.source_snapshot.commit_sha;
 const sample=index.source_files.find(x=>x.candidate_relation==='NO_SAME_PATH_IN_CANDIDATE');
 assert.ok(sample);
 const text=sha+':'+sample.source_path+':1:'+sample.source_path+'\\n';
 const result=summarizeD01ObservedRefs(index,text.replace('\\n','\n'));
 assert.equal(result.missing_candidate_sources_with_textual_refs,1);
 assert.equal(result.no_current_usage_proof,true);
 assert.equal(result.no_dynamic_import_or_external_dependency_proof,true);
});
test('D01 static scan rejects malformed output instead of claiming coverage',()=>{
 assert.throws(()=>summarizeD01ObservedRefs(index,'not-git-grep-output'),
  e=>e.code==='D01_STATIC_GREP_OUTPUT_MALFORMED');
});
