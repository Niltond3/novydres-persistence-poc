// D01 regressions work against committed immutable Git trees, no write or scene.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {verifyD01,listPinnedTree,readAndVerifyD01} from './verificar-inventario-d01.mjs';
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
 sourceContents:new Map(index.source_files.filter(row=>
  row.current_cycle_candidate_reconciliation==='SOURCE_NOT_IN_CANDIDATE').map(row=>[
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
