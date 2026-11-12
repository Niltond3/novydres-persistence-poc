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
export function verifyD01(index,{masterTree,candidateTree,external,media,cycle}){
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
 for(const row of only)need(o.get(row.path)?.blob_sha===row.sha&&
   o.get(row.path)?.git_mode===row.mode,'D01_CANDIDATE_ONLY_SHA_MISMATCH');
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
   actual.source_byte_equivalence==='NOT_REVALIDATED_D01','D01_EXTERNAL_MAPPING_DRIFT');
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
 const summary=index.denominators;
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
 return verifyD01(index,{masterTree,candidateTree,
  external:read(index.controlled_external_registry.path),
  media:read(index.visual_registry.path),
  cycle:read(index.authority_reference.cycle.path)});
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))
 console.log(JSON.stringify(readAndVerifyD01()));
