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
const data={masterTree:listPinnedTree(root,pinned),
 candidateTree:listPinnedTree(root,index.candidate_snapshot.commit_sha),
 external:read(index.controlled_external_registry.path),
 media:read(index.visual_registry.path),
 cycle:read(index.authority_reference.cycle.path)};
const clone=()=>structuredClone(index);
const reject=(mutate,code)=>{const x=clone();mutate(x);assert.throws(()=>verifyD01(x,data),e=>e.code===code);};
test('D01 whole-tree fixed baseline, 1029/923 blobs and no editorial PASS',()=>{
 const r=readAndVerifyD01(root);
 assert.equal(r.gate,'D01_STRUCTURE_VERIFIED_EDITORIAL_PENDING');
 assert.equal(r.source_blobs,1029);assert.equal(r.candidate_blobs,923);
 assert.equal(r.external_items,193);assert.equal(r.media_items,19);
 assert.equal(r.cycle_pins,77);assert.equal(r.runtime_activation,false);
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
test('D01 no false success when gate pending list disappears',()=>{
 reject(x=>x.gate_requirements_pending=[],'D01_FALSE_GATE_CLOSURE');
});
