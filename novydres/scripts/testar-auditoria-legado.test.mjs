import test from 'node:test';
import assert from 'node:assert/strict';
import {auditRepository,auditTree} from './auditar-legado-e-fontes.mjs';
import {mkdtempSync,mkdirSync,writeFileSync,rmSync,symlinkSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join,dirname} from 'node:path';
import {execFileSync} from 'node:child_process';
const sha='a'.repeat(40);
const baseFiles=['novydres/AGENTS.md','novydres/CONTEXT.md','novydres/catalogo.json',
 'novydres/personagens/synthetic/index.md','novydres/personagens/synthetic/assunto.json']
 .map(path=>({path,type:'blob',mode:'100644',blob_sha:sha}));
const exampleSubject={id:'synthetic',kind:'character',path:'novydres/personagens/synthetic',
 visibility:'PLAYER_SAFE',source_ids:[],files:[]};
const baseCatalog=JSON.stringify({subjects:[exampleSubject]});
const media=()=>({policy:'DRIVE_BINARY_GITHUB_LINK_ONLY',entries:[]});
const audit=(extra=[],contents={},mode='CANDIDATE',registry=media())=>auditTree({
 files:[...baseFiles,...extra],contents:{'novydres/catalogo.json':baseCatalog,...contents},
 mode,mediaRegistry:registry});
const has=(r,code)=>r.issues.some(x=>x.code===code);

test('V08/V11/V12 actual HEAD entire file inventory; no false ZERO LEGADO in pre-cutover',()=>{
 const a=auditRepository();
 assert.equal(a.mode,'CANDIDATE');
 assert.equal(a.gate,'C06_CANDIDATE_AUDIT_EXECUTED_WITH_LEGACY_PENDING');
 assert.ok(a.inventory_coverage.scanned>850);
 assert.equal(a.inventory_coverage.missing,0);
 assert.ok(a.counters.legacy_paths>200,'pre-cutover old paths must be reported');
 assert.equal(a.counters.symlinks,0);
 assert.equal(a.counters.media_pending,5,'historical registry must be confirmed, not guessed');
 assert.equal(a.counters.unverified_media,19,'do not invent hashes');
 assert.equal(a.issues.length,0,JSON.stringify(a.issues.slice(0,3)));
});
test('V12 FINAL gate rejects entire actual pre-cutover HEAD, independently of C06 tool passing',()=>{
 const a=auditRepository(process.cwd(),{mode:'ZERO_LEGACY_FINAL'});
 assert.equal(a.gate,'ZERO_LEGACY_BLOCKED');
 assert.ok(a.issues.some(x=>x.code==='LEGACY_PATH_IN_FINAL'));
 assert.ok(a.inventory_coverage.scanned>850);
});
test('V12 synthetic clean tree distinguishes permitted provenance from active route',()=>{
 const path='novydres/personagens/synthetic/origem.json';
 const x=audit([{path,mode:'100644',type:'blob',blob_sha:sha}],
 {[path]:JSON.stringify({source_ref:{id:'novydres/chronicles/CHR-001/LIVE_v038.json',source_commit:sha,sha}})},
 'ZERO_LEGACY_FINAL');
 assert.equal(x.gate,'ZERO_LEGACY_STRUCTURAL_PASS_WITH_EXTERNAL_REVIEW');
 assert.equal(x.counters.textual_legacy_mentions,1);
});
test('V12 legacy physical paths may remain during design but cannot be hidden in final',()=>{
 const path='novydres/runtime/old-handler.js', entry={path,type:'blob',mode:'100644',blob_sha:sha};
 assert.equal(audit([entry]).gate,'C06_CANDIDATE_AUDIT_EXECUTED_WITH_LEGACY_PENDING');
 const r=audit([entry],{},'ZERO_LEGACY_FINAL');
 assert.equal(r.gate,'ZERO_LEGACY_BLOCKED');assert.ok(has(r,'LEGACY_PATH_IN_FINAL'));
});
test('V12 imports from an old runtime in NEW candidate scripts are blocked now',()=>{
 const path='novydres/scripts/bridge.js',entry={path,type:'blob',mode:'100644',blob_sha:sha};
 const r=audit([entry],{[path]:"import engine from 'novydres/runtime/legacy.js'\n"});
 assert.ok(has(r,'LEGACY_CODE_CONSUMER'));
 assert.equal(r.gate,'C06_AUDIT_FAILED');
});
test('V12 relative imports to legacy directories are also blocked',()=>{
 const path='novydres/scripts/bridge.js',entry={path,type:'blob',mode:'100644',blob_sha:sha};
 const r=audit([entry],{[path]:"const old = require('../runtime/legacy.js')"});
 assert.ok(has(r,'LEGACY_CODE_CONSUMER'));
});
test('V12 detects symlinks and aliases, no blanket skip for fixtures',()=>{
 const path='poc/synthetic-fixture-link',entry={path,type:'blob',mode:'120000',blob_sha:sha};
 const r=audit([entry]);assert.ok(has(r,'SYMLINK_FORBIDDEN'));
});
test('V08 public entry must not list hidden source filenames',()=>{
 const path='novydres/AGENTS.md';
 const r=audit([],{[path]:'open: novydres/plan_GM_HIDDEN.json'});
 assert.ok(has(r,'HIDDEN_SOURCE_IN_PUBLIC_ENTRY'));
});
test('V08 metadata index cannot expose private source IDs or mismatched file blobs',()=>{
 const privateCatalog=JSON.stringify({subjects:[{...exampleSubject,visibility:'SYSTEM_AUDIT',
 source_ids:['secret-ref'],files:[{path:'novydres/personagens/synthetic/index.md',blob_sha:'b'.repeat(40)}]}]});
 const r=audit([],{['novydres/catalogo.json']:privateCatalog});
 assert.ok(has(r,'CATALOG_PRIVATE_SOURCE_IDS_EXPOSED'));
 assert.ok(has(r,'CATALOG_PIN_NOT_IN_TREE'));
});
test('V11 media linked originals require exact link/ID and policy; missing stays pending',()=>{
 const asset={raw_original_migrated:true,drive_sha256_verified:false,drive_file_id:null,drive_url:null,
  media_storage:'GOOGLE_DRIVE_ORIGINAL_FILE'};
 const r=audit([],{},'CANDIDATE',{policy:'DRIVE_BINARY_GITHUB_LINK_ONLY',entries:[asset]});
 assert.ok(has(r,'MEDIA_LINK_UNVERIFIED'));
 assert.equal(r.counters.unverified_media,1);
});
test('V11 missing originals and unverified SHA are recorded, never synthesized',()=>{
 const asset={raw_original_migrated:false,drive_sha256_verified:false,drive_file_id:null,drive_url:null,
  media_storage:'PENDING_SOURCE_ORIGINAL'};
 const a=audit([],{},'CANDIDATE',{policy:'DRIVE_BINARY_GITHUB_LINK_ONLY',entries:[asset]});
 assert.equal(a.counters.media_pending,1);
 assert.equal(a.counters.unverified_media,1);
 const final=audit([],{},'ZERO_LEGACY_FINAL',{policy:'DRIVE_BINARY_GITHUB_LINK_ONLY',entries:[asset]});
 assert.equal(final.gate,'ZERO_LEGACY_BLOCKED');
});

test('V11/V12 final mode never passes without the migrated media registry',()=>{
 const incomplete=audit([],{},'ZERO_LEGACY_FINAL',null);
 assert.equal(incomplete.gate,'ZERO_LEGACY_BLOCKED');
 assert.ok(has(incomplete,'MEDIA_REGISTRY_REQUIRED_IN_FINAL'));
 // D02 supplies the pinned final registry; missing-registry is still tested on the synthetic negative.
 const actual=auditRepository(process.cwd(),{mode:'ZERO_LEGACY_FINAL'});
 assert.equal(actual.gate,'ZERO_LEGACY_BLOCKED');
 assert.ok(!has(actual,'MEDIA_REGISTRY_REQUIRED_IN_FINAL'));
 assert.equal(actual.counters.media_pending,5);
 assert.equal(actual.counters.unverified_media,19);
});
test('V08/V12 HEAD-pinned bytes cannot be masked by dirty checkout or false media JSON',()=>{
 const dir=mkdtempSync(join(tmpdir(),'novydres-c07-audit-'));
 const git=(...args)=>execFileSync('git',args,{cwd:dir,stdio:['ignore','pipe','ignore'],encoding:'utf8'}).trim();
 const put=(p,value)=>{const file=join(dir,p);mkdirSync(dirname(file),{recursive:true});writeFileSync(file,value);};
 const save=()=>{git('add','.');git('-c','user.name=NOVYDRES-test','-c','user.email=test@example.invalid',
   'commit','--quiet','-m','TEST_ONLY synthetic HEAD');return git('rev-parse','HEAD');};
 try{
  git('init','--quiet');
  put('novydres/AGENTS.md','Candidate agent text without secret locator\n');
  put('novydres/CONTEXT.md','Candidate context without legacy active links\n');
  put('novydres/catalogo.json','{"subjects":[]}\n');
  put('novydres/migration/VISUAL_ASSET_REGISTRY_V2.json',
    '{"policy":"DRIVE_BINARY_GITHUB_LINK_ONLY","entries":[]}\n');
  const goodHead=save();
  put('novydres/AGENTS.md','open novydres/internal_GM_HIDDEN.json\n');
  put('novydres/catalogo.json','{invalid json');
  put('novydres/migration/VISUAL_ASSET_REGISTRY_V2.json','{invalid json');
  const committed=auditRepository(dir,{expected_head:goodHead});
  assert.equal(committed.gate,'C06_CANDIDATE_AUDIT_EXECUTED_WITH_LEGACY_PENDING');
  assert.equal(committed.audited_commit,goodHead);
  assert.equal(committed.source,'PINNED_GIT_TREE_BLOBS_NOT_WORKTREE');
  assert.ok(!has(committed,'HIDDEN_SOURCE_IN_PUBLIC_ENTRY'));
  assert.equal(committed.inventory_coverage.scanned,4);
  assert.throws(()=>auditRepository(dir,{expected_head:'0'.repeat(40)}),
    error=>error.code==='HEAD_DIFFERENT');
  // Flip: a harmful committed entry cannot be excused by cleaning the working tree.
  put('novydres/catalogo.json','{"subjects":[]}\n');
  put('novydres/migration/VISUAL_ASSET_REGISTRY_V2.json',
    '{"policy":"DRIVE_BINARY_GITHUB_LINK_ONLY","entries":[]}\n');
  const badHead=save();
  put('novydres/AGENTS.md','Candidate agent text without secret locator\n');
  const bad=auditRepository(dir,{expected_head:badHead});
  assert.equal(bad.gate,'C06_AUDIT_FAILED');
  assert.ok(has(bad,'HIDDEN_SOURCE_IN_PUBLIC_ENTRY'));
  // Git symlink points at an unavailable target. Scanner audits the link blob;
  // it must not dereference a checkout symlink.
  symlinkSync('TEST_ONLY_nonexistent_target',join(dir,'novydres','suspicious.md'));
  const linkHead=save();
  const link=auditRepository(dir,{expected_head:linkHead});
  assert.ok(has(link,'SYMLINK_FORBIDDEN'));
 }finally{rmSync(dir,{recursive:true,force:true});}
});

test('V08 HEAD-pinned auditor accepts a valid >1MiB blob without skipping SHA verification',()=>{
 const dir=mkdtempSync(join(tmpdir(),'novydres-c06-large-'));
 const git=(...args)=>execFileSync('git',args,{cwd:dir,encoding:'utf8',stdio:['ignore','pipe','ignore']}).trim();
 const put=(p,value)=>{const file=join(dir,p);mkdirSync(dirname(file),{recursive:true});writeFileSync(file,value);};
 try{
  git('init','--quiet');
  put('novydres/AGENTS.md','Candidate only. No activation.\n');
  put('novydres/CONTEXT.md','Candidate only. No runtime use.\n');
  put('novydres/catalogo.json','{"subjects":[]}\n');
  put('novydres/migration/VISUAL_ASSET_REGISTRY_V2.json',
   '{"policy":"DRIVE_BINARY_GITHUB_LINK_ONLY","entries":[]}\n');
  const large=JSON.stringify({kind:'TEST_ONLY_LARGE_INVENTORY',payload:'x'.repeat(1_300_000)});
  assert.ok(Buffer.byteLength(large)>1024*1024);
  put('novydres/sistema/arquitetura/fase-d/inventario-origens.json',large);
  git('add','.');
  git('-c','user.name=NOVYDRES-test','-c','user.email=test@example.invalid',
   'commit','--quiet','-m','TEST_ONLY large Git blob audit');
  const sha=git('rev-parse','HEAD');
  const a=auditRepository(dir,{expected_head:sha});
  assert.equal(a.gate,'C06_CANDIDATE_AUDIT_EXECUTED_WITH_LEGACY_PENDING');
  assert.equal(a.inventory_coverage.scanned,5);
  assert.equal(a.inventory_coverage.missing,0);
  assert.equal(a.audited_commit,sha);
  assert.equal(a.issues.length,0);
 }finally{rmSync(dir,{recursive:true,force:true});}
});
