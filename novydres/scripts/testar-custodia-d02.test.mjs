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
 fails(d=>d.sources.entries[0].drive_sha256_verified=true,'D02_MEDIA_PROVENANCE');
});
test('D02 must retain unresolved editorial authority',()=>{
 fails(d=>d.governance.conflicts.find(x=>x.id==='CONFLICT-003B').status='RESOLVED','D02_EDITORIAL_CONFLICT_SUPPRESSED');
});
test('D02 cannot copy-source without exact SHA',()=>{
 fails(d=>d.governance.source_documents[0].candidate_original_blob_sha='0'.repeat(40),'D02_GOVERNANCE_CUSTODY');
});
