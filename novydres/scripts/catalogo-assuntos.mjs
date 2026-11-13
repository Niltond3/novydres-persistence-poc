// ADR-001: derived catalog and snapshot-pinned selective retrieval.
// Effective authority is master plus E03_PASS; no secondary bootstrap or legacy fallback.
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { dirname, join, relative, resolve, sep, posix } from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

export const CATALOG_PATH = 'novydres/catalogo.json';
const SUBJECT_ROOTS = ['novydres/cenario', 'novydres/personagens', 'novydres/cronicas', 'novydres/sistema/regras'];
const SHA = /^[a-f0-9]{40}$/;
const ID = /^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/;
const norm = s => s.normalize('NFC').toLowerCase();
const canon = o => JSON.stringify(o, null, 2) + '\n';
const blobSha = bytes => createHash('sha1').update('blob ' + bytes.length + '\0').update(bytes).digest('hex');
const fail = (code, detail = '') => { const err = new Error(code + (detail ? ': ' + detail : '')); err.code=code; throw err; };

function paths(dir, found = []) {
  if (!existsSync(dir)) return found;
  for (const ent of readdirSync(dir, {withFileTypes:true})) {
    const abs=join(dir,ent.name);
    if(ent.isSymbolicLink()) fail('SYMLINK_NOT_ALLOWED', abs);
    if(ent.isDirectory()) paths(abs,found);
    else if(ent.name==='assunto.json') found.push(abs);
  }
  return found;
}
function frontmatter(src) {
  const m=/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(src);
  if(!m) fail('INDEX_FRONTMATTER_MISSING');
  const fields={};
  for(const line of m[1].split(/\r?\n/)) {
    const sepIndex=line.indexOf(':');
    if(sepIndex<1) continue;
    const name=line.slice(0,sepIndex).trim();
    const value=line.slice(sepIndex+1).trim();
    if(Object.hasOwn(fields,name)) fail('INDEX_DUPLICATE_KEY',name);
    fields[name]=value;
  }
  return fields;
}

export function buildCatalog(root=process.cwd(), {overrides={}}={}) {
  // Override is used only for isolated mutation tests; never alters repository files.
  const read = p => {
    const o=Object.hasOwn(overrides,p)?overrides[p]:readFileSync(resolve(root,p));
    return Buffer.isBuffer(o)?o:Buffer.from(typeof o==='string'?o:canon(o),'utf8');
  };
  const all=SUBJECT_ROOTS.flatMap(prefix=>paths(resolve(root,prefix))).sort();
  if(!all.length) fail('NO_CANDIDATE_SUBJECTS');
  const subjects=[], inputs=[], idMap=new Map(), relationRecords=[];
  for(const abs of all) {
    const dir=dirname(abs), path=relative(root,dir).split(sep).join('/');
    const main=posix.join(path,'assunto.json');
    const obj=JSON.parse(read(main).toString('utf8'));
    if(!ID.test(obj.subject_id || '')) fail('INVALID_SUBJECT_ID',main);
    if(!obj.owner_scope || !(path===obj.owner_scope || path.startsWith(obj.owner_scope+'/'))) fail('OWNER_MISMATCH',main);
    // CANDIDATE is the migrated manifest's historical metadata, not a runtime gate.
    if(obj.status!=='CANDIDATE') fail('MIGRATION_STATUS_DRIFT',main);
    if(idMap.has(norm(obj.subject_id))) fail('SUBJECT_ID_COLLISION',obj.subject_id);
    const files=readdirSync(dir,{withFileTypes:true})
      .filter(x=>{if(x.isSymbolicLink())fail('SYMLINK_NOT_ALLOWED',x.name);return x.isFile();})
      .map(x=>x.name).sort();
    if(!files.includes('index.md')) fail('INDEX_MISSING',path);
    const front=frontmatter(read(posix.join(path,'index.md')).toString('utf8'));
    for(const [key,value] of Object.entries({subject_id:obj.subject_id,kind:obj.kind,
      owner_scope:obj.owner_scope,status:obj.status,visibility:obj.visibility})) {
      if(front[key]!==value) fail('INDEX_METADATA_MISMATCH',path+': '+key);
    }
    const located=files.map(name=>{
      const p=posix.join(path,name), buf=read(p);
      // Literal archived source JSON is verified by its pinned Git blob, not interpreted as subject claims.
      if(name.endsWith('.json') && !name.endsWith('.source.json')) {
        const doc=JSON.parse(buf.toString('utf8'));
        if(doc.subject_id!==obj.subject_id) fail('SUBJECT_OWNER_MISMATCH',p);
        if(name==='relacoes.json') relationRecords.push({path:p,doc});
      }
      const sha=blobSha(buf);
      inputs.push({path:p,blob_sha:sha});
      return {path:p,blob_sha:sha};
    });
    const dependencies=(obj.related_subject_ids||[]).slice().sort();
    if(new Set(dependencies.map(norm)).size!==dependencies.length)fail('DUPLICATE_DEPENDENCY',main);
    const sourceIds=(obj.source_refs||[]).map(x=>x.id);
    if(sourceIds.some(x=>typeof x!=='string'||!x))fail('SOURCE_ID_INVALID',main);
    const subject={id:obj.subject_id,kind:obj.kind,owner:obj.owner_scope,path,
      visibility:obj.visibility,dependencies,
      // No hidden source names in public-facing metadata. The source file remains
      // available to an authorized agent after an explicit scoped read.
      source_ids:obj.visibility==='PLAYER_SAFE'?[...new Set(sourceIds)].sort():[],
      files:located};
    idMap.set(norm(obj.subject_id),subject);subjects.push(subject);
  }
  subjects.sort((a,b)=>a.id<b.id?-1:a.id>b.id?1:0);
  for(const s of subjects) for(const dependency of s.dependencies)
    if(!idMap.has(norm(dependency))) fail('DEPENDENCY_NOT_FOUND',s.id+' -> '+dependency);
  const backlinks=new Map(subjects.map(s=>[s.id,new Set()]));
  for(const s of subjects) for(const d of s.dependencies)
    backlinks.get(idMap.get(norm(d)).id).add(s.id);
  const deferred=[];
  for(const {path,doc} of relationRecords) {
    if(!Array.isArray(doc.relations)) fail('RELATIONS_INVALID',path);
    for(const rel of doc.relations) {
      if(rel.inverse_is_derived!==true) fail('INVERSE_NOT_DERIVED',path);
      if(!idMap.has(norm(rel.from_subject_id || ''))) fail('RELATION_FROM_NOT_FOUND',path);
      if(idMap.has(norm(rel.to_subject_id || ''))) backlinks.get(idMap.get(norm(rel.to_subject_id)).id).add(rel.from_subject_id);
      else if(doc.external_target_id_not_migrated_in_phase_b===true && rel.to_subject_id==='pc-bartholomeu-krauser')
        deferred.push({from:rel.from_subject_id,to:rel.to_subject_id,reason:'EXTERNAL_NOT_MIGRATED_C41'});
      else fail('RELATION_TARGET_NOT_FOUND',path);
    }
  }
  inputs.sort((a,b)=>a.path<b.path?-1:a.path>b.path?1:0);
  // Git blob SHA of sorted input path/blob manifest, not SHA of enclosing commit or
  // catalog file: edits invalidate this hash without introducing a circular hash.
  const content_index_sha=blobSha(Buffer.from(canon(inputs),'utf8'));
  deferred.sort((a,b)=>a.from<b.from?-1:a.from>b.from?1:a.to<b.to?-1:a.to>b.to?1:0);
  return {schema_version:'1.0',kind:'DERIVED_SUBJECT_CATALOG',status:'OPERATIONAL_AFTER_E03_PASS',
    content_index_sha,subjects,
    inverse_dependencies:Object.fromEntries([...backlinks].sort(([a],[b])=>a<b?-1:a>b?1:0)
      .map(([id,inbound])=>[id,[...inbound].sort()])),deferred};
}

export function catalogBytes(catalog) { return canon(catalog); }
export function checkCatalog(root=process.cwd()) {
  const expected=catalogBytes(buildCatalog(root));
  const actual=readFileSync(resolve(root,CATALOG_PATH),'utf8');
  if(actual!==expected) fail('CATALOG_GENERATION_DRIFT');
  return {ok:true,bytes:Buffer.byteLength(expected),entries:JSON.parse(actual).subjects.length,
    content_index_sha:JSON.parse(actual).content_index_sha};
}

// Only metadata (not full text) is cached; each snapshot is independent.
export function resolveSubject(catalog, subjectId, {snapshot_sha,role=null,cache=new Map()}={}) {
  if(!SHA.test(snapshot_sha||'')) fail('SNAPSHOT_REQUIRED');
  if(!ID.test(subjectId||'')) fail('NOT_FOUND',String(subjectId));
  if(!['PLAYER','AUDITOR','DRAMATURGO','NARRADOR'].includes(role)) fail('ROLE_NOT_AUTHORIZED');
  const id=norm(subjectId);
  const matches=catalog.subjects.filter(s=>norm(s.id)===id);
  if(matches.length!==1 || matches[0].id!==subjectId) fail(matches.length>1?'AMBIGUOUS_ID':'NOT_FOUND',subjectId);
  const s=matches[0];
  // Validate role/scope BEFORE consulting the optional caller-supplied cache.
  // A poisoned cache entry must never override an authoritative subject ACL,
  // owner or blob pointer, even when the snapshot/key happens to be correct.
  const canRead=role!=='PLAYER'||s.visibility==='PLAYER_SAFE'||s.visibility==='PC_KNOWN';
  if(!canRead) fail('DISCLOSURE_DENIED',s.id);
  // The subject may be PLAYER_SAFE while its technical owner manifest points to
  // restricted local scopes. Do not export private relationship names, provenance
  // locators or the raw owner manifest through a PLAYER lookup.
  const player=role==='PLAYER';
  const playerVisible=id=>{
    const linked=catalog.subjects.find(x=>x.id===id);
    return linked && ['PLAYER_SAFE','PC_KNOWN'].includes(linked.visibility);
  };
  const resolved={snapshot_sha,subject_id:s.id,kind:s.kind,owner_path:s.path,
    files:s.files.filter(x=>!player||!x.path.endsWith('/assunto.json')).map(x=>({...x})),
    source_ids:player?[]:s.source_ids.slice(),visibility:s.visibility,
    dependencies:player?s.dependencies.filter(playerVisible):s.dependencies.slice()};
  const key=snapshot_sha+'|'+s.id+'|'+s.kind+'|'+catalog.content_index_sha+'|'+role;
  if(cache.has(key)) {
    if(JSON.stringify(cache.get(key))!==JSON.stringify(resolved)) fail('CACHE_INTEGRITY',s.id);
    return structuredClone(resolved);
  }
  cache.set(key,structuredClone(resolved));
  return resolved;
}

export function readSelected(root,catalog,subjectId,{snapshot_sha,role=null,
  selected_paths=[],cache}={}) {
  if(!SHA.test(snapshot_sha||'')) fail('SNAPSHOT_REQUIRED');
  const record=resolveSubject(catalog,subjectId,{snapshot_sha,role,cache});
  // Check that the catalog itself belongs to this exact Git snapshot; do not
  // silently rebuild from checkout or search historic/legacy locations.
  let pinned;
  try {
    pinned=execFileSync('git',['show',snapshot_sha+':'+CATALOG_PATH],{cwd:root,encoding:'utf8',stdio:['ignore','pipe','ignore']});
  } catch { fail('SNAPSHOT_CATALOG_NOT_FOUND'); }
  if(pinned!==catalogBytes(catalog)) fail('SNAPSHOT_CATALOG_MISMATCH');
  const refs=new Map(record.files.map(f=>[f.path,f.blob_sha]));
  const pathsToRead=selected_paths.length?selected_paths:[posix.join(record.owner_path,'index.md')];
  if(new Set(pathsToRead).size!==pathsToRead.length)fail('DUPLICATE_SELECTION');
  const out=[];
  for(const path of pathsToRead) {
    if(!refs.has(path)) fail('UNDECLARED_PATH',path);
    let bytes;
    try {bytes=execFileSync('git',['show',snapshot_sha+':'+path],{cwd:root,stdio:['ignore','pipe','ignore']});}
    catch {fail('SNAPSHOT_FILE_NOT_FOUND',path);}
    if(blobSha(bytes)!==refs.get(path)) fail('HASH_MISMATCH',path);
    out.push({path,blob_sha:refs.get(path),text:bytes.toString('utf8')});
  }
  return {snapshot_sha,subject_id:subjectId,files:out};
}

if(process.argv[1] && resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  const arg=process.argv[2]||'--check';
  if(arg==='--check') console.log(JSON.stringify(checkCatalog()));
  else if(arg==='--print') process.stdout.write(catalogBytes(buildCatalog()));
  else fail('UNSUPPORTED_MODE',arg);
}
