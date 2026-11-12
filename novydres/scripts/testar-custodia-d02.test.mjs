import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {verifyD02Git,verifyD02Model} from './verificar-custodia-d02.mjs';
const load=p=>JSON.parse(readFileSync(p,'utf8'));
const inventory=load('novydres/sistema/arquitetura/fase-d/inventario-origens.json');
const governance=load('novydres/sistema/governanca/registro.json');
const sources=load('novydres/fontes/registro.json');
const show=p=>JSON.parse(execFileSync('git',['show',inventory.source_snapshot.commit_sha+':'+p],{encoding:'utf8',maxBuffer:64*1024*1024}));
const external=show('novydres/migration/INVENTORY.json');
const visual=show('novydres/migration/VISUAL_ASSET_REGISTRY_V2.json');
const args=()=>structuredClone({inventory,governance,sources,external,visual});
const fails=(fn,code)=>{let d=args();fn(d);assert.throws(()=>verifyD02Model(d),e=>e.code===code);};
test('D02 full candidate HEAD preserves original governance blobs and references',()=>{
 let r=verifyD02Git();assert.equal(r.gate,'D02_PROVENANCE_CUSTODY_VALID_EDITORIAL_AND_EXTERNAL_OPEN');
 assert.equal(r.origins,128);assert.equal(r.governance,27);assert.equal(r.external,193);
 assert.equal(r.media,19);assert.equal(r.pending,5);assert.equal(r.split,96);
});
test('D02 gate cannot be promoted through metadata',()=>{
 fails(d=>d.sources.gate='D02_PASS','D02_FALSE_GATE');
});
test('D02 cannot pretend external Drive bytes or rights checked',()=>{
 fails(d=>d.sources.external_sources[0].rights_verified_d02=true,'D02_EXTERNAL_PROVENANCE');
});
test('D02 cannot drop a governance decision from the migrated register',()=>{
 fails(d=>d.governance.source_documents.pop(),'D02_ORIGIN_DENOMINATOR');
});
test('D02 cannot drop a source origin with a stable Git blob',()=>{
 fails(d=>d.sources.origin_custody.pop(),'D02_ORIGIN_DENOMINATOR');
});
test('D02 cannot reassign split fields invisibly',()=>{
 let x=d=>d.sources.origin_custody.find(y=>y.field_split);
 fails(d=>x(d).field_split=false,'D02_FIELD_OWNER_HANDOFF');
});
test('D02 may not invent a visual original link',()=>{
 fails(d=>{let x=d.sources.entries.find(x=>!x.raw_original_migrated);x.drive_file_id='invented';},'D02_MEDIA_PROVENANCE');
});
test('D02 may not inflate integrity to SHA verified',()=>{
 fails(d=>d.sources.entries[0].drive_sha256='0'.repeat(64),'D02_MEDIA_DIGEST_INVALID');
});
test('D02 must retain unresolved editorial authority',()=>{
 fails(d=>d.governance.conflicts.find(x=>x.id==='CONFLICT-003B').status='RESOLVED','D02_EDITORIAL_CONFLICT_SUPPRESSED');
});
test('D02 cannot copy-source without exact SHA',()=>{
 fails(d=>d.governance.source_documents[0].candidate_original_blob_sha='0'.repeat(40),'D02_GOVERNANCE_CUSTODY');
});
test('D02 Library source IDs are not treated as Drive file IDs',()=>{
 fails(d=>d.sources.external_sources.find(x=>x.identifier_namespace==='LIBRARY_REFERENCE').identifier_namespace='GOOGLE_DRIVE_FILE_ID','D02_ID_NAMESPACE');
});
test('D02 does not suppress an observed Drive MIME difference',()=>{
 fails(d=>d.sources.external_sources.find(x=>x.identifier_namespace==='GOOGLE_DRIVE_FILE_ID'&&x.d02_metadata_observation.mime_matches_historical===false).d02_metadata_observation.mime_matches_historical=true,'D02_METADATA_CLASSIFICATION');
});
test('D02 does not fabricate current Drive content integrity',()=>{
 fails(d=>d.sources.external_metadata_audit.source_bytes_verified_now=109,'D02_METADATA_DENOMINATOR');
});
test('D02 rejects pointing to old roots instead of rehomed exact source',()=>{
 fails(d=>d.sources.origin_custody[0].candidate_destination=d.sources.origin_custody[0].original_path,'D02_TARGET_OWNER');
});
test('D02 rejects provenance claiming transformation without proof',()=>{
 fails(d=>d.sources.origin_custody[0].transformation_evidence='UNKNOWN','D02_TARGET_OWNER');
});
test('D02 cannot claim Library original bytes were recovered without evidence',()=>{
 fails(d=>d.sources.media_source_recovery.source_bytes_materialized=5,'D02_FALSE_MEDIA_RECOVERY');
});
test('D02 cannot pretend pending originals were uploaded to Drive',()=>{
 fails(d=>d.sources.entries.find(x=>!x.raw_original_migrated).d02_observation.destination_original_uploaded_d02=true,'D02_PENDING_MEDIA');
});
test('D02 cannot erase a proven destination SHA-256',()=>{
 fails(d=>d.sources.entries.find(x=>x.raw_original_migrated).drive_sha256_verified=false,'D02_MEDIA_DIGEST_INVALID');
});
test('D02 may not extrapolate one historical source-hash match to all media',()=>{
 fails(d=>d.sources.media_crypto_audit.source_previous_digest_matches=14,'D02_CRYPTO_COVERAGE');
});
test('D02 cannot replace the true source digest without exposing the discrepancy',()=>{
 fails(d=>d.sources.entries.find(x=>x.name==='MasterMap.png').source_sha256='0'.repeat(64),'D02_CRYPTO_SOURCE_CLAIM');
});
test('D02 cannot conceal outstanding subject-field routing under artifact custody',()=>{
 fails(d=>d.sources.field_partition_audit.d02_domain_fields_promoted=96,'D02_PARTITION_AUDIT');
});
test('D02 cannot introduce a rival authoritative owner on a routed historical source',()=>{
 fails(d=>d.sources.origin_custody.find(x=>x.field_split).field_owner_custody.no_field_fact_promoted_d02=false,'D02_FIELD_CONCURRENT_OWNER');
});
