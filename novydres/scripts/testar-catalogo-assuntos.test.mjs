// ADR-001 C02 V03/V09 functional risk tests against current candidate Git commit.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {buildCatalog,catalogBytes,checkCatalog,resolveSubject,readSelected} from './catalogo-assuntos.mjs';

const root=process.cwd(), p='novydres/cronicas/CHR-001/', global='novydres/personagens/npc-samir-haddad/';
const snap=execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim();
const read=p=>JSON.parse(readFileSync(p,'utf8'));
const override=(path,delta)=>{
  const obj=read(path);delta(obj);return buildCatalog(root,{overrides:{[path]:obj}});
};
const expectCode=(fn,code)=>assert.throws(fn,e=>e.code===code,'must reject with '+code);

test('V09 bytes are deterministic and equal the committed generated file',()=>{
 const a=catalogBytes(buildCatalog(root)),b=catalogBytes(buildCatalog(root));
 assert.equal(a,b);assert.equal(a,readFileSync('novydres/catalogo.json','utf8'));
 assert.equal(checkCatalog(root).ok,true);
});
test('V03 candidate subjects have exact single owners, files, derived reverse links',()=>{
 const c=buildCatalog(root);
 assert.equal(c.subjects.length,79);
 assert.deepEqual(c.subjects.map(s=>s.id).filter(id=>!id.startsWith('world-')&&!id.startsWith('rule-')&&!id.startsWith('district-')&&!id.startsWith('poi-')&&!id.startsWith('org-')&&!id.startsWith('pc-')&&!['npc-iskander-yasupov','npc-madame-zoya'].includes(id)),[
  'chr001-npc-samir-haddad','chr001-state-checkpoint','chr001-table-config',
  'npc-samir-haddad','plot-contato-condicional-samir','story-m301-c01']);
 assert.equal(new Set(c.subjects.flatMap(s=>s.files.map(f=>f.path))).size,316);
 assert.ok(c.inverse_dependencies['plot-contato-condicional-samir'].includes('story-m301-c01'));
 assert.equal(c.deferred.length,0);
 assert.ok(c.subjects.some(s=>s.id==='pc-bartholomeu-krauser'));
 assert.ok(c.inverse_dependencies['pc-bartholomeu-krauser'].includes('npc-samir-haddad'));
});
test('V03 resolves exact metadata for player-known global NPC in pinned snapshot',()=>{
 const c=buildCatalog(root), cache=new Map();
 const out=resolveSubject(c,'npc-samir-haddad',{snapshot_sha:snap,role:'PLAYER',cache});
 assert.equal(out.owner_path,global.slice(0,-1));
 assert.equal(out.snapshot_sha,snap);
 assert.ok(out.files.some(f=>f.path===global+'perfil.json'));
 assert.equal(cache.size,1);
 const p2=resolveSubject(c,'npc-samir-haddad',{snapshot_sha:snap,role:'PLAYER',cache});
 assert.deepEqual(p2,out);p2.files[0].path='poison';
 assert.notEqual(resolveSubject(c,'npc-samir-haddad',{snapshot_sha:snap,role:'PLAYER',cache}).files[0].path,'poison');
});
test('V03 selective read uses actual git show at the pinned commit, unmodified bytes',()=>{
 const c=buildCatalog(root);
 const path=global+'perfil.json';
 const got=readSelected(root,c,'npc-samir-haddad',{snapshot_sha:snap,role:'PLAYER',selected_paths:[path]});
 const ref=execFileSync('git',['show',snap+':'+path],{encoding:'utf8'});
 assert.equal(got.files[0].text,ref);
 assert.equal(got.files[0].blob_sha,c.subjects.find(s=>s.id==='npc-samir-haddad').files.find(f=>f.path===path).blob_sha);
});
test('V03 rejects fuzzy missing IDs and legacy path labels without lookup fallback',()=>{
 const c=buildCatalog(root);
 for(const id of ['npc-samir','NPC Samir Haddad','novydres/chronicles/CHR-001/LIVE_v038.json'])
   expectCode(()=>resolveSubject(c,id,{snapshot_sha:snap,role:'AUDITOR'}),'NOT_FOUND');
});
test('V09 content hash invalidates on payload bytes even when subject metadata stays fixed',()=>{
 const base=buildCatalog(root),path=global+'perfil.json';
 const altered=override(path,o=>{o.aliases.push('TEST_ONLY_NEW_ALIAS');});
 assert.notEqual(base.content_index_sha,altered.content_index_sha);
 assert.notEqual(catalogBytes(base),catalogBytes(altered));
});
test('V02 duplicate subject ID cannot silently shadow another owner',()=>{
 const path=p+'tramas/contato-condicional-samir/assunto.json';
 expectCode(()=>override(path,o=>o.subject_id='chr001-npc-samir-haddad'),'SUBJECT_ID_COLLISION');
});
test('V09 index metadata must match the authoritative subject document',()=>{
 const path=global+'index.md', text=readFileSync(path,'utf8').replace('visibility: PLAYER_SAFE','visibility: GM_HIDDEN');
 expectCode(()=>buildCatalog(root,{overrides:{[path]:text}}),'INDEX_METADATA_MISMATCH');
});
test('V03 missing subject dependency is blocking, not deferred',()=>{
 const path=p+'tramas/contato-condicional-samir/assunto.json';
 expectCode(()=>override(path,o=>o.related_subject_ids.push('unmigrated-no-owner')),'DEPENDENCY_NOT_FOUND');
});
test('V03 scoped C41 external relation cannot exempt an arbitrary new target',()=>{
 const path=p+'elenco/npc-samir-haddad/relacoes.json';
 expectCode(()=>override(path,o=>o.relations[0].to_subject_id='invented-other-character'),'RELATION_TARGET_NOT_FOUND');
});
test('V04 restricted local actor knowledge is denied before selective retrieval',()=>{
 const c=buildCatalog(root);
 expectCode(()=>resolveSubject(c,'chr001-npc-samir-haddad',{snapshot_sha:snap,role:'PLAYER'}),'DISCLOSURE_DENIED');
 expectCode(()=>readSelected(root,c,'chr001-npc-samir-haddad',{snapshot_sha:snap,role:'PLAYER',
  selected_paths:[p+'elenco/npc-samir-haddad/conhecimento.json']}),'DISCLOSURE_DENIED');
});
test('V04 omitted actor role fails closed instead of defaulting to AUDITOR',()=>{
 const c=buildCatalog(root);
 expectCode(()=>resolveSubject(c,'chr001-table-config',{snapshot_sha:snap}),'ROLE_NOT_AUTHORIZED');
 expectCode(()=>readSelected(root,c,'chr001-table-config',{snapshot_sha:snap}),'ROLE_NOT_AUTHORIZED');
});
test('V04 unknown roles cannot bypass disclosure control',()=>{
 expectCode(()=>resolveSubject(buildCatalog(root),'chr001-state-checkpoint',{snapshot_sha:snap,role:'UNAUTHORIZED'}),'ROLE_NOT_AUTHORIZED');
});
test('V09 stale or forged catalog never reads data from a different Git snapshot',()=>{
 const c=buildCatalog(root),other='a0430cf15b0c0715e9572954dbf320c97374bfa8';
 expectCode(()=>readSelected(root,c,'npc-samir-haddad',{snapshot_sha:other,role:'AUDITOR'}),'SNAPSHOT_CATALOG_NOT_FOUND');
 const forged=structuredClone(c);forged.content_index_sha='0'.repeat(40);
 expectCode(()=>readSelected(root,forged,'npc-samir-haddad',{snapshot_sha:snap,role:'AUDITOR'}),'SNAPSHOT_CATALOG_MISMATCH');
});
test('V03 selected paths must be declared by that exact subject, no legacy or traversal',()=>{
 const c=buildCatalog(root);
 for(const path of ['novydres/.AGENT.md','novydres/chronicles/CHR-001/LIVE_v038.json','../old']) {
   expectCode(()=>readSelected(root,c,'npc-samir-haddad',{snapshot_sha:snap,role:'AUDITOR',selected_paths:[path]}),'UNDECLARED_PATH');
 }
});
test('V04 poisoned PLAYER cache cannot return restricted metadata or text',()=>{
 const c=buildCatalog(root), id='chr001-npc-samir-haddad';
 const privateMeta=resolveSubject(c,id,{snapshot_sha:snap,role:'AUDITOR'});
 const key=[snap,id,privateMeta.kind,c.content_index_sha,'PLAYER'].join('|');
 const injected=new Map([[key,privateMeta]]);
 expectCode(()=>resolveSubject(c,id,{snapshot_sha:snap,role:'PLAYER',cache:injected}),
  'DISCLOSURE_DENIED');
 expectCode(()=>readSelected(root,c,id,{snapshot_sha:snap,role:'PLAYER',cache:injected,
  selected_paths:[p+'elenco/npc-samir-haddad/conhecimento.json']}),'DISCLOSURE_DENIED');
});
test('V09 externally supplied cache cannot change authorized owner/file list',()=>{
 const c=buildCatalog(root), id='npc-samir-haddad';
 const known=resolveSubject(c,id,{snapshot_sha:snap,role:'PLAYER'});
 const key=[snap,id,known.kind,c.content_index_sha,'PLAYER'].join('|');
 const tampered=structuredClone(known);
 tampered.files=[{path:'novydres/cronicas/CHR-001/elenco/npc-samir-haddad/conhecimento.json',
   blob_sha:'0'.repeat(40)}];
 const injected=new Map([[key,tampered]]);
 expectCode(()=>resolveSubject(c,id,{snapshot_sha:snap,role:'PLAYER',cache:injected}),'CACHE_INTEGRITY');
 expectCode(()=>readSelected(root,c,id,{snapshot_sha:snap,role:'PLAYER',cache:injected,
  selected_paths:[tampered.files[0].path]}),'CACHE_INTEGRITY');
});
test('V04 PLAYER cannot enumerate restricted dependencies or internal provenance via a public subject',()=>{
 const c=buildCatalog(root),id='npc-samir-haddad',manifest=global+'assunto.json';
 const auditor=resolveSubject(c,id,{snapshot_sha:snap,role:'AUDITOR'});
 assert.ok(auditor.dependencies.includes('chr001-npc-samir-haddad'));
 assert.ok(auditor.files.some(f=>f.path===manifest));
 assert.ok(auditor.source_ids.length>0);
 const player=resolveSubject(c,id,{snapshot_sha:snap,role:'PLAYER'});
 assert.ok(!player.dependencies.includes('chr001-npc-samir-haddad'));
 assert.ok(player.dependencies.every(x=>c.subjects.find(s=>s.id===x)?.visibility==='PLAYER_SAFE'));
 assert.ok(!player.files.some(f=>f.path===manifest));
 assert.deepEqual(player.source_ids,[]);
 expectCode(()=>readSelected(root,c,id,{snapshot_sha:snap,role:'PLAYER',
   selected_paths:[manifest]}),'UNDECLARED_PATH');
 assert.equal(readSelected(root,c,id,{snapshot_sha:snap,role:'PLAYER',
   selected_paths:[global+'perfil.json']}).files.length,1);
});
test('V09 cache is snapshot keyed (never borrows entry from new commit)',()=>{
 const c=buildCatalog(root),cache=new Map();
 resolveSubject(c,'npc-samir-haddad',{snapshot_sha:snap,role:'AUDITOR',cache});
 resolveSubject(c,'npc-samir-haddad',{snapshot_sha:'a'.repeat(40),role:'AUDITOR',cache});
 assert.equal(cache.size,2);
});
test('D03 private subject portfolios expose exact copied source only to authorized roles',()=>{
 const c=buildCatalog(root), ids=['world-atlas-novydres','world-history-novydres','world-politics-novydres',
 'world-lineage-urban-gangrel','world-npc-power-scale','npc-iskander-yasupov','npc-madame-zoya',
 'rule-creation-novydres','rule-experience-novydres'];
 for(const id of ids){
  expectCode(()=>resolveSubject(c,id,{snapshot_sha:snap,role:'PLAYER'}),'DISCLOSURE_DENIED');
  const result=resolveSubject(c,id,{snapshot_sha:snap,role:'AUDITOR'});
  const source=result.files.find(f=>/\/fonte-\d+\.source\./.test(f.path));
  assert.ok(source,'missing literal source '+id);
  const read=readSelected(root,c,id,{snapshot_sha:snap,role:'AUDITOR',selected_paths:[source.path]});
  assert.equal(read.files.length,1);assert.equal(read.files[0].blob_sha,source.blob_sha);
 }
});
