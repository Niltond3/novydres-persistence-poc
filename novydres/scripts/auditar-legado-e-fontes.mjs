// ADR-001 C06 — whole-tree V08/V11/V12 audit, candidate-only until E.
// Every HEAD entry is inventoried. Historical provenance and test negatives may
// remain evidence; no legacy executable fallback may pass ZERO_LEGACY_FINAL.
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const LEGACY_ROOT=/^(?:novydres\/(?:chronicles|runtime|world|governance|systems|migration|assets\/drive-links)\/|poc\/)/;
const VERSIONED_ROOT=/^novydres\/(?:MANIFEST(?:_V\d+)?\.json|\.AGENT(?:_V\d+)?\.md|\.CONTEXTG(?:_V\d+)?\.md)$/;
const ACTIONABLE=/\b(?:from\s+['"]|import\s*\(|require\s*\(|readFileSync\s*\(|fetch_file\s*\(|open\s*\(|run:\s*|node\s+|python\s+|execFileSync\s*\(|git\s+(?:show|rev-parse)\b|fallback\b|alias\b|redirect\b|symlink\b)/i;
const OLD_LITERAL=/novydres\/(?:chronicles|runtime|world|governance|systems|migration|assets\/drive-links)\//i;
const RELATIVE_OLD=/(?:\.\.\/)+(?:chronicles|runtime|world|governance|systems|migration)\//i;
const PUBLIC_ENTRY=new Set(['novydres/AGENTS.md','novydres/CONTEXT.md','novydres/catalogo.json']);
const PRIVATELABEL=/(?:GM_HIDDEN|__GM_HIDDEN)/;
const mediaPath='novydres/migration/VISUAL_ASSET_REGISTRY_V2.json';
const finalMediaPath='novydres/fontes/registro.json'; // D02 must migrate the real register; no legacy fallback.
const MAX_GIT_BUFFER=64*1024*1024; // Explicit upper bound; Node execFileSync defaults to only 1 MiB.
const fail=(code,detail='')=>{const e=new Error(code+(detail?': '+detail:''));e.code=code;throw e;};
const order=(a,b)=>a<b?-1:a>b?1:0;

function lsTree(root,commit) {
 const raw=execFileSync('git',['ls-tree','-r','-z','--full-tree',commit],
  {cwd:root,encoding:'utf8',stdio:['ignore','pipe','ignore'],maxBuffer:MAX_GIT_BUFFER});
 return raw.split('\0').filter(Boolean).map(line=>{
  const m=/^(\d{6}) (blob|commit|tree) ([a-f0-9]{40})\t(.+)$/.exec(line);
  if(!m)fail('MALFORMED_GIT_TREE');
  return {mode:m[1],type:m[2],blob_sha:m[3],path:m[4]};
 });
}
const isText=path=>/\.(?:json|jsonl|md|txt|mjs|js|jsx|ts|tsx|cjs|yml|yaml|py|sh|toml|xml|html|css)$/i.test(path)||
 path==='README.md'||path==='AGENTS.md'||path==='CONTEXT.md';
const isCode=path=>/\.(?:mjs|cjs|js|jsx|ts|tsx|py|sh|yml|yaml)$/i.test(path);
const legacyRoot=path=>LEGACY_ROOT.test(path)||VERSIONED_ROOT.test(path);
export function auditTree({files,contents={},mode='CANDIDATE',mediaRegistry=null}={}) {
 if(!['CANDIDATE','ZERO_LEGACY_FINAL'].includes(mode))fail('INVALID_MODE');
 if(!Array.isArray(files)||!files.length)fail('EMPTY_INVENTORY');
 if(new Set(files.map(x=>x.path)).size!==files.length)fail('DUPLICATE_TREE_PATH');
 const all=files.slice().sort((a,b)=>order(a.path,b.path));
 const issues=[],warnings=[];
 const counters={blobs:0,text_files:0,binary_files:0,legacy_paths:0,symlinks:0,
  candidate_code_consumers:0,textual_legacy_mentions:0,unverified_media:0,media_pending:0,public_secret_marker_paths:0};
 const classified=[];
 for(const file of all) {
  const path=file.path;
  if(file.type!=='blob')fail('NON_BLOB_TREE_ENTRY',path);
  counters.blobs++;
  const legacy=legacyRoot(path);
  const symlink=file.mode==='120000';
  if(symlink){counters.symlinks++;issues.push({code:'SYMLINK_FORBIDDEN',path});}
  if(legacy){counters.legacy_paths++;if(mode==='ZERO_LEGACY_FINAL')
    issues.push({code:'LEGACY_PATH_IN_FINAL',path});}
  if(isText(path))counters.text_files++;else counters.binary_files++;
  const value=contents[path];
  if(typeof value==='string'){
   if(PUBLIC_ENTRY.has(path) && /(?:_GM_HIDDEN\.(?:json|md|txt)|GM_HIDDEN_[A-Z0-9_]+\.json)/i.test(value)){
    counters.public_secret_marker_paths++;issues.push({code:'HIDDEN_SOURCE_IN_PUBLIC_ENTRY',path});
   }
   if(OLD_LITERAL.test(value))counters.textual_legacy_mentions++;
   if(isCode(path) && (OLD_LITERAL.test(value)||RELATIVE_OLD.test(value))) {
    const live=value.split('\n').some(line=>(OLD_LITERAL.test(line)||RELATIVE_OLD.test(line))&&ACTIONABLE.test(line)&&
      !(/^\s*(?:\/\/|#|\/\*|\*|\-)\s/.test(line))&&
      !(path.endsWith('.test.mjs') && /\baudit\(\[/.test(line)));
    if(live){
      counters.candidate_code_consumers++;
      if(mode==='ZERO_LEGACY_FINAL'||path.startsWith('novydres/scripts/'))issues.push({code:'LEGACY_CODE_CONSUMER',path});
      else warnings.push({code:'LEGACY_CODE_CONSUMER_PRECUTOVER',path});
    }
   }
  }
  classified.push({path,kind:symlink?'SYMLINK':legacy?'LEGACY_ORIGINAL':
   isText(path)?'TEXT_OR_CONFIG':'BINARY_OR_OTHER',blob_sha:file.blob_sha});
 }
 for(const required of PUBLIC_ENTRY)if(!classified.some(x=>x.path===required))
  issues.push({code:'BOOTSTRAP_MISSING',path:required});
 const catalog=contents['novydres/catalogo.json'];
 if(typeof catalog==='string'){
  let parsed;
  try{parsed=JSON.parse(catalog);}catch{issues.push({code:'CATALOG_INVALID',path:'novydres/catalogo.json'});}
  if(parsed){
   for(const s of parsed.subjects||[]){
    if(!s.id||!all.some(f=>f.path===s.path+'/index.md'))
      issues.push({code:'CATALOG_OWNER_NOT_RESOLVED',path:'novydres/catalogo.json'});
    if(s.visibility!=='PLAYER_SAFE'&&(s.source_ids||[]).length)
      issues.push({code:'CATALOG_PRIVATE_SOURCE_IDS_EXPOSED',path:'novydres/catalogo.json'});
    if(s.files?.some(f=>!all.some(t=>t.path===f.path&&t.blob_sha===f.blob_sha)))
      issues.push({code:'CATALOG_PIN_NOT_IN_TREE',path:'novydres/catalogo.json'});
   }
  }
 }
 if(mediaRegistry!==null){
  const entries=mediaRegistry.entries;
  if(!Array.isArray(entries))issues.push({code:'MEDIA_REGISTRY_INVALID',path:mediaPath});
  else for(const item of entries){
   if(item.media_storage!=='GOOGLE_DRIVE' && item.raw_original_migrated_destination!=='GOOGLE_DRIVE')
    warnings.push({code:'MEDIA_LOCATION_UNCONFIRMED',path:mediaPath});
   if(item.drive_sha256_verified!==true)counters.unverified_media++;
   if(item.raw_original_migrated!==true)counters.media_pending++;
   if(item.raw_original_migrated===true && (!item.drive_file_id||!item.drive_url))
     issues.push({code:'MEDIA_LINK_UNVERIFIED',path:mediaPath});
  }
  if(mediaRegistry.policy!=='DRIVE_BINARY_GITHUB_LINK_ONLY')
   issues.push({code:'MEDIA_POLICY_MISMATCH',path:mediaPath});
 }
 if(mode==='ZERO_LEGACY_FINAL'&&mediaRegistry===null)
   issues.push({code:'MEDIA_REGISTRY_REQUIRED_IN_FINAL',path:finalMediaPath});
 const legal=issues.length===0;
 const gate=mode==='ZERO_LEGACY_FINAL'?
   (legal&&counters.legacy_paths===0&&counters.symlinks===0&&counters.media_pending===0?
   'ZERO_LEGACY_STRUCTURAL_PASS_WITH_EXTERNAL_REVIEW':'ZERO_LEGACY_BLOCKED'):
   (legal?'C06_CANDIDATE_AUDIT_EXECUTED_WITH_LEGACY_PENDING':'C06_AUDIT_FAILED');
 return {schema_version:'1.0',mode,gate,counters,
  issues,warning_counts:Object.fromEntries([...new Set(warnings.map(x=>x.code))]
   .sort().map(k=>[k,warnings.filter(x=>x.code===k).length])),
  legacy_path_sample:classified.filter(x=>x.kind==='LEGACY_ORIGINAL').slice(0,5)
    .map(x=>({kind:x.kind,path:x.path})),
  inventory_coverage:{scanned:classified.length,missing:0},
  media_integrity:'EXTERNAL_ORIGINAL_BYTES_NOT_FETCHED_NO_SHA_INVENTED',
  semantic_review:'REQUIRED_SEPARATELY_V08_V11_V12_NOT_AST_COMPLETE'};
}
export function auditRepository(root=process.cwd(),{mode='CANDIDATE',expected_head=null}={}) {
 // V08/V12: read the Git object graph, NEVER the mutable checkout. A dirty,
 // substituted or symlink-backed working-tree file must not hide an old route
 // or a secret still committed in HEAD.
 const git=(...args)=>execFileSync('git',args,
  {cwd:root,encoding:'utf8',stdio:['ignore','pipe','ignore'],maxBuffer:MAX_GIT_BUFFER}).trim();
 const head=git('rev-parse','HEAD');
 if(!/^[a-f0-9]{40}$/.test(head))fail('HEAD_NOT_RESOLVED');
 if(expected_head!==null&&expected_head!==head)fail('HEAD_DIFFERENT');
 const files=lsTree(root,head);
 const contents={};
 for(const f of files){
  if(!isText(f.path))continue;
  let bytes;
  try {
    bytes=execFileSync('git',['cat-file','blob',f.blob_sha],
      {cwd:root,stdio:['ignore','pipe','ignore'],maxBuffer:MAX_GIT_BUFFER});
  } catch(error) {
    if(error?.code==='ENOBUFS')fail('GIT_BLOB_AUDIT_LIMIT',f.path);
    fail('GIT_BLOB_UNAVAILABLE',f.path);
  }
  const actual=createHash('sha1').update('blob '+bytes.length+'\0').update(bytes).digest('hex');
  if(actual!==f.blob_sha)fail('GIT_BLOB_INTEGRITY',f.path);
  contents[f.path]=bytes.toString('utf8');
 }
 // The old media register itself is a legacy path. Once D02 removes that
 // subtree, the final audit must use the migrated, HEAD-pinned source. Missing
 // final evidence is BLOCKED, never a successful empty media inventory.
 const registryPath=mode==='ZERO_LEGACY_FINAL'?finalMediaPath:mediaPath;
 let registry=null;
 if(typeof contents[registryPath]==='string') {
   try {registry=JSON.parse(contents[registryPath]);}
   catch {fail('MEDIA_REGISTRY_INVALID',registryPath);}
 } else if(mode!=='ZERO_LEGACY_FINAL') fail('MEDIA_REGISTRY_INVALID',registryPath);
 if(git('rev-parse','HEAD')!==head)fail('HEAD_DIFFERENT');
 const result=auditTree({files,contents,mediaRegistry:registry,mode});
 return {...result,audited_commit:head,source:'PINNED_GIT_TREE_BLOBS_NOT_WORKTREE'};
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const mode=process.argv.includes('--final')?'ZERO_LEGACY_FINAL':'CANDIDATE';
 const audit=auditRepository(process.cwd(),{mode});
 console.log(JSON.stringify(audit));
 if((mode==='CANDIDATE' && audit.gate!=='C06_CANDIDATE_AUDIT_EXECUTED_WITH_LEGACY_PENDING') ||
    (mode==='ZERO_LEGACY_FINAL' && audit.gate.startsWith('ZERO_LEGACY_BLOCKED')))process.exitCode=1;
}
