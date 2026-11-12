// ADR-001 D02: candidate-only provenance, source custody and media contract verifier.
// It does not decide editorial authority, prove external bytes or grant cutover.
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
const need=(ok,code)=>{if(!ok){let e=new Error(code);e.code=code;throw e;}};
const by=(v,k)=>new Map(v.map(x=>[x[k],x]));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
export function verifyD02Model({inventory,governance,sources,external,visual}) {
 need(inventory.d01_scope_gate?.decision==='D01_PASS_SCOPED_ORIGIN_INVENTORY_ONLY','D02_INPUT_D01_GATE');
 need(governance.classification==='SYSTEM_AUDIT'&&sources.classification==='SYSTEM_AUDIT','D02_DISCLOSURE');
 need(governance.status==='CANDIDATE_NOT_OPERATIONAL_D02_OPEN'&&
  sources.status==='CANDIDATE_D02_PARTIAL_NOT_OPERATIONAL'&&sources.gate==='D02_NOT_EVALUATED_AS_PASS','D02_FALSE_GATE');
 need(governance.frozen_sources_modified===false&&
  governance.source_snapshot.sha===inventory.source_snapshot.commit_sha&&
  sources.original_snapshot_sha===inventory.source_snapshot.commit_sha,'D02_AUTHORITY_DRIFT');
 need(sources.policy==='DRIVE_BINARY_GITHUB_LINK_ONLY','D02_MEDIA_POLICY');
 const originals=inventory.source_files.filter(x=>x.d01_origin_route?.handoff_phase==='D02');
 const gov=originals.filter(x=>x.source_family==='EDITORIAL_GOVERNANCE');
 need(originals.length===128&&gov.length===27&&sources.origin_custody.length===128&&
  governance.source_documents.length===27,'D02_ORIGIN_DENOMINATOR');
 const sourceMap=by(originals,'source_path'),custody=by(sources.origin_custody,'original_path');
 const governanceMap=by(governance.source_documents,'source_path');
 need(custody.size===128&&governanceMap.size===27,'D02_DUPLICATE_ORIGIN');
 for(const x of originals){
  const y=custody.get(x.source_path);
  need(y&&y.original_blob_sha===x.source_blob_sha&&y.source_family===x.source_family&&
    y.original_preserved_in_git===true&&y.authority==='PRESERVED_SOURCE_NOT_PROMOTED'&&
    y.visibility==='SYSTEM_AUDIT_UNTIL_REVIEW','D02_ORIGIN_CUSTODY');
  const newTarget=x.source_family==='EDITORIAL_GOVERNANCE'?
   'novydres/sistema/governanca/originais/'+x.source_path.replace(/^novydres\/governance\//,''):
   'novydres/fontes/originais/'+x.source_path.replace(/^novydres\//,'');
  need(y.candidate_destination===newTarget&&
   y.transformation_evidence==='EXACT_ORIGINAL_GIT_BLOB_SHA_REHOME_PRESERVE_SOURCE','D02_TARGET_OWNER');
  const split=x.d01_origin_route.owner_routing==='FIELD_SCOPE_SPLIT_REQUIRED';
  need(y.field_split===split&&(!split||y.cross_domain_content_handoff==='D03_D04_D05_SEMANTIC_REVIEW_REQUIRED'),'D02_FIELD_OWNER_HANDOFF');
 }
 for(const x of gov){
  const y=governanceMap.get(x.source_path);
  need(y&&y.source_sha===x.source_blob_sha&&y.candidate_original_blob_sha===x.source_blob_sha&&
    y.copy==='GIT_BLOB_EXACT_UNMODIFIED'&&
    y.operational_authority==='NOT_GRANTED_BY_CANDIDATE','D02_GOVERNANCE_CUSTODY');
 }
 const partitions=sources.field_partition_audit;
 need(partitions&&partitions.d01_total_handed_over_other_phases===463&&
  partitions.d02_flagged_for_split===96&&
  partitions.d02_historical_source_custody_classified===96&&
  partitions.d02_domain_fields_promoted===0&&
  partitions.d02_unapproved_authority_claims===0&&
  partitions.unmapped_external_link_cases===28&&
  partitions.residual==='DOMAIN_SEMANTIC_FIELDS_NOT_MIGRATED_OR_AUTHORIZED_UNDER_D02','D02_PARTITION_AUDIT');
 let splitCount=0;
 for(const row of sources.origin_custody.filter(x=>x.field_split)) {
  splitCount++;
  const fields=row.field_owner_custody;
  need(fields&&fields.original_document_sha_owner==='novydres/fontes/originais'&&
   fields.identity_provenance_reference_owner==='novydres/fontes/registro.json'&&
   fields.technical_audit_assertion_owner==='novydres/sistema/arquitetura'&&
   fields.domain_semantics_in_original==='SOURCE_ONLY_NOT_CURRENT_AUTHORITY'&&
   fields.no_field_fact_promoted_d02===true&&
   fields.owner_collision_resolution.startsWith('ORIGINAL_BLOB_REHOMED_ONCE'),'D02_FIELD_CONCURRENT_OWNER');
 }
 need(splitCount===96,'D02_SPLIT_DENOMINATOR');
  const externalMap=by(external.items,'id'),mapped=by(sources.external_sources,'id');
 need(external.items.length===193&&mapped.size===193&&mapped.size===externalMap.size,'D02_EXTERNAL_DENOMINATOR');
 for(const [id,e] of externalMap){
  const m=mapped.get(id),pin=inventory.controlled_external_registry.items.find(x=>x.source_id===id);
  need(m&&pin&&m.title===e.title&&m.source_revision===(e.source_revision||null)&&
    m.archived_source_path===(pin.archived_target||null)&&
    m.archived_git_blob_sha===(pin.archived_target_sha||null)&&
    m.drive_current_revision_verified_d02===false&&m.git_archive_blob_is_external_integrity_proof===false&&
    m.rights_verified_d02===false,'D02_EXTERNAL_PROVENANCE');
 }
 const audit=sources.external_metadata_audit;
 need(audit&&audit.total===193&&audit.google_drive_ids_found===109&&
  audit.google_drive_ids_unavailable===0&&audit.library_ids_not_drive===68&&
  audit.file_ids_not_drive===16&&audit.drive_title_matches_historical===109&&
  audit.drive_mime_differences===16&&audit.drive_name_differences===0&&
  audit.source_bytes_verified_now===0&&audit.source_revision_readback_verified_now===0&&
  audit.permissions_and_rights_verified_now===0,'D02_METADATA_DENOMINATOR');
 let drive=0,library=0,file=0,mimeDiff=0;
 for(const source of sources.external_sources) {
  const isLib=source.id.startsWith('libfile_'),isFile=source.id.startsWith('file_');
  const expected=isLib?'LIBRARY_REFERENCE':isFile?'FILE_REFERENCE':'GOOGLE_DRIVE_FILE_ID';
  need(source.identifier_namespace===expected&&source.d02_metadata_observation&&
   source.drive_current_revision_verified_d02===false,'D02_ID_NAMESPACE');
  const obs=source.d02_metadata_observation;
  if(isLib||isFile) {
   isLib?library++:file++;
   need(obs.status==='NOT_DRIVE_ID_NOT_QUERIED_AS_PROVIDER_ORIGINAL'&&
    obs.rights_and_original_bytes_unverified===true,'D02_INVENTED_DRIVE_ACCESS');
  } else {
   drive++;
   need(obs.source==='GOOGLE_DRIVE_GET_FILE_METADATA_2026_11_12'&&
    obs.status==='METADATA_FOUND'&&obs.title_matches_historical===true&&
    obs.checksum_or_permissions_not_proven===true,'D02_DRIVE_METADATA');
   if(obs.mime_matches_historical===false)mimeDiff++;
   else need(obs.mime_matches_historical===true,'D02_DRIVE_MIME_UNCLASSIFIED');
  }
 }
 need(drive===109&&library===68&&file===16&&mimeDiff===16,'D02_METADATA_CLASSIFICATION');
 const mediaBy=by(sources.entries,'library_id');
 need(visual.entries.length===19&&mediaBy.size===19,'D02_MEDIA_DENOMINATOR');
 let linked=0,pending=0;
 for(const e of visual.entries){
  const m=mediaBy.get(e.library_id);
  need(m&&m.name===e.name&&m.reported_status===e.reported_status&&
    m.drive_file_id===e.drive_file_id&&m.drive_url===e.drive_url&&
    m.raw_original_migrated===e.raw_original_migrated,'D02_MEDIA_PROVENANCE');
  if(e.raw_original_migrated){
   need(m.drive_sha256_verified===true&&/^[a-f0-9]{64}$/.test(m.drive_sha256||'')&&
    m.d02_observation.drive_sha256_computed===true&&
    m.d02_observation.drive_raw_original_bytes_read===true&&
    m.d02_observation.destination_sha256===m.drive_sha256&&
    m.d02_observation.drive_byte_length_matches_registry===true&&
    m.d02_observation.source_sha256_computed_d02===false,'D02_MEDIA_DIGEST_INVALID');
  }else{
   need(m.drive_sha256_verified!==true&&m.d02_observation.drive_sha256_computed===false,'D02_PENDING_MEDIA_DIGEST');
  }
  if(e.raw_original_migrated) {
   linked++;need(!!m.drive_file_id&&m.d02_observation.name_mime_size_match===true,'D02_MEDIA_LINK');
  }else{
   pending++;need(m.d02_observation.matching_original_found===false&&
    m.d02_observation.library_original_bytes_accessible==='RAW_FILE_MATERIALIZATION_NOT_AUTHORIZED'&&
    m.d02_observation.library_metadata_exact_id_found===true&&
    m.d02_observation.source_integrity_verified===false&&
    m.d02_observation.destination_original_uploaded_d02===false,'D02_PENDING_MEDIA');
  }
 }
 need(linked===14&&pending===5&&sources.media_integrity.unlocated_originals===5&&
  sources.media_integrity.source_or_destination_sha256_verified_now===14&&
  sources.media_integrity.destination_sha256_verified_now===14&&
  sources.media_integrity.source_original_sha256_computed_now===0&&
  sources.media_integrity.source_destination_equivalence_unverified===13,'D02_FALSE_MEDIA_INTEGRITY');
 const crypto=sources.media_crypto_audit;
 need(crypto&&crypto.destination_originals_downloaded===14&&crypto.destination_sha256_computed===14&&
  crypto.destination_length_matched===14&&crypto.source_raw_bytes_directly_hashed_in_d02===0&&
  crypto.source_previous_digest_matches===1&&crypto.source_equivalence_unproven===13&&
  crypto.drive_originals_unresolved===5&&crypto.source_and_destination_fully_equivalent_for_all_19===false,'D02_CRYPTO_COVERAGE');
 const matched=sources.entries.filter(e=>e.drive_sha256_verified===true&&
  typeof e.source_sha256==='string'&&e.source_sha256===e.drive_sha256);
 need(matched.length===1&&matched[0].name==='MasterMap.png'&&
  visual.storage_summary.mastermap_source_sha256_verified===1,'D02_CRYPTO_SOURCE_CLAIM');
  const recovery=sources.media_source_recovery;
 need(recovery&&recovery.pending_originals===5&&recovery.exact_library_metadata_found===5&&
  recovery.source_bytes_materialized===0&&recovery.source_bytes_sha256_computed===0&&
  recovery.google_drive_exact_name_search_matches===0&&recovery.drive_new_uploads===0&&
  recovery.gate_impact==='D02_EXTERNAL_MEDIA_COMPLETION_NOT_PROVEN','D02_FALSE_MEDIA_RECOVERY');
  const known=new Set(governance.conflicts.map(x=>x.id));
 need(['CONFLICT-001','CONFLICT-002','CONFLICT-003B'].every(x=>known.has(x))&&
  governance.conflicts.find(x=>x.id==='CONFLICT-003B').status==='TEXT_DIFFERENCES_VERIFIED_EDITORIAL_VERDICT_OPEN',
 'D02_EDITORIAL_CONFLICT_SUPPRESSED');
 return {gate:'D02_PROVENANCE_CUSTODY_VALID_EDITORIAL_AND_EXTERNAL_OPEN',origins:128,governance:27,external:193,
  media:19,linked,pending,split:originals.filter(x=>x.d01_origin_route.owner_routing==='FIELD_SCOPE_SPLIT_REQUIRED').length};
}
const cmd=(...a)=>execFileSync('git',a,{encoding:'utf8',maxBuffer:64*1024*1024}).trim();
export function verifyD02Git(root=process.cwd()) {
 const read=p=>JSON.parse(readFileSync(p,'utf8'));
 const inventory=read('novydres/sistema/arquitetura/fase-d/inventario-origens.json');
 const governance=read('novydres/sistema/governanca/registro.json');
 const sources=read('novydres/fontes/registro.json');
 const external=JSON.parse(cmd('show',inventory.source_snapshot.commit_sha+':novydres/migration/INVENTORY.json'));
 const visual=JSON.parse(cmd('show',inventory.source_snapshot.commit_sha+':novydres/migration/VISUAL_ASSET_REGISTRY_V2.json'));
 const outcome=verifyD02Model({inventory,governance,sources,external,visual});
 const gitBlob=(p)=>cmd('rev-parse','HEAD:'+p);
 for(const g of governance.source_documents){
  need(gitBlob(g.candidate_original_path)===g.source_sha,'D02_GOVERNANCE_BYTES_CHANGED');
  need(gitBlob(g.source_path)===g.source_sha,'D02_ORIGINAL_REMOVED_EARLY');
 }
 for(const p of ['novydres/sistema/governanca/registro.json','novydres/fontes/registro.json'])
  need(/^[a-f0-9]{40}$/.test(gitBlob(p)),'D02_REGISTRY_NOT_PINNED');
 need(sources.origin_custody.every(x=>gitBlob(x.candidate_destination)===x.original_blob_sha),
  'D02_REHOMED_SOURCE_MISMATCH');
 need(sources.origin_custody.every(x=>gitBlob(x.original_path)===x.original_blob_sha),
  'D02_SOURCE_BYTES_CHANGED');
 const editorial=JSON.parse(cmd('show',inventory.source_snapshot.commit_sha+':novydres/governance/sources/novydres_editorial_map_v0_9_4.json'));
 need(editorial.schema_version==='0.9.3','D02_CONFLICT_002_NOT_PRESERVED');
 return {...outcome,readback:'ALL_D02_ORIGIN_AND_27_GOVERNANCE_BLOBS_MATCH_HEAD',
  external_bytes:'NOT_VERIFIED',cutover:false};
}
if(import.meta.url===new URL('file://'+process.argv[1]).href) {
 try{console.log(JSON.stringify(verifyD02Git()));}
 catch(e){console.error(e.code||e.message);process.exitCode=1;}
}
