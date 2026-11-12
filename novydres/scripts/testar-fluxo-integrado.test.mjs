// ADR-001 C07 — one candidate-only integrated flow, not an operational scene.
import test from 'node:test';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {performance} from 'node:perf_hooks';
import {readFileSync} from 'node:fs';
import {buildCatalog,catalogBytes,checkCatalog,resolveSubject,readSelected} from './catalogo-assuntos.mjs';
import {validateCandidates} from './validar-assuntos.mjs';
import {inspectCandidateResume,continuationDecision} from './retomar-estado.mjs';
import {CandidateGitTransaction,fingerprint} from './transacao-git.mjs';
import {auditRepository} from './auditar-legado-e-fontes.mjs';
import {examineFictionalFrame,correlateFrozenBReview} from './revisar-conducao-candidata.mjs';

const head=execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim();
const oldSource='c26c0fbf15fff6c817182c06e6208e302b954f3a';
const root=process.cwd();
const cfgId='chr001-table-config',stateId='chr001-state-checkpoint';
const load=p=>JSON.parse(readFileSync(p,'utf8'));
const b='novydres/sistema/arquitetura/fase-b/';
const err=(fn,expected)=>assert.throws(fn,e=>e.code===expected,'expected '+expected);
const quantile=(samples,p)=>{
 const sorted=[...samples].sort((a,b)=>a-b);
 return Math.round(sorted[Math.ceil(p*sorted.length)-1]*100)/100;
};
test('C07 integrated selective snapshot fixes one catalog+state+config at current candidate SHA',()=>{
 assert.equal(checkCatalog().ok,true);
 const c=buildCatalog();
 assert.equal(c.subjects.length,58);
 assert.equal(catalogBytes(c),readFileSync('novydres/catalogo.json','utf8'));
 const resolved=resolveSubject(c,cfgId,{snapshot_sha:head,role:'AUDITOR'});
 assert.equal(resolved.owner_path,'novydres/cronicas/CHR-001/configuracao');
 const filepath=resolved.files.find(f=>f.path.endsWith('/configuracao.json')).path;
 const cfg=JSON.parse(readSelected(root,c,cfgId,{snapshot_sha:head,role:'AUDITOR',
  selected_paths:[filepath]}).files[0].text);
 assert.equal(cfg.not_operational,true);
 assert.equal(cfg.state_subject_id,stateId);
 assert.equal(cfg.no_campaign_events_created,true);
 assert.equal(resolveSubject(c,stateId,{snapshot_sha:head,role:'AUDITOR'}).kind,'chronicle');
});
test('C07 integrated knowledge and private configuration cannot be disclosed to PLAYER by lookup',()=>{
 const c=buildCatalog();
 err(()=>resolveSubject(c,cfgId,{snapshot_sha:head,role:'PLAYER'}),'DISCLOSURE_DENIED');
 err(()=>resolveSubject(c,'chr001-npc-samir-haddad',{snapshot_sha:head,role:'PLAYER'}),'DISCLOSURE_DENIED');
 err(()=>resolveSubject(c,'chr001-unknown-fiction',{snapshot_sha:head,role:'AUDITOR'}),'NOT_FOUND');
});
test('C07 public subject resolution does not expose private relation or owner manifest',()=>{
 const c=buildCatalog();
 const player=resolveSubject(c,'npc-samir-haddad',{snapshot_sha:head,role:'PLAYER'});
 assert.ok(!player.dependencies.includes('chr001-npc-samir-haddad'));
 assert.deepEqual(player.source_ids,[]);
 assert.ok(player.files.every(f=>!f.path.endsWith('/assunto.json')));
 err(()=>readSelected(root,c,'npc-samir-haddad',{snapshot_sha:head,role:'PLAYER',
   selected_paths:['novydres/personagens/npc-samir-haddad/assunto.json']}),'UNDECLARED_PATH');
});
test('C07 state recovery C41 not C45, with NPC claim and unknowns preserved',()=>{
 const output=inspectCandidateResume(root,{snapshot_sha:head,expected_head:head});
 assert.equal(output.status,'CANDIDATE_HISTORICAL_ONLY');
 assert.equal(output.source_commit,oldSource);
 assert.equal(output.actor_claims_status,'NPC_CLAIM_NOT_WORLD_FACT');
 assert.equal(output.checkpoint.scene_started,false);
 assert.equal(output.unresolved.historical_cursor_drift,'DECLARED_C41_NOT_C45');
 assert.equal(output.publication.authority,'CANDIDATE_ONLY');
 const old=validateCandidates();
 assert.equal(old.errors.length,0,JSON.stringify(old.errors));
 assert.ok(old.deferred.some(x=>x.target==='pc-bartholomeu-krauser'));
});
test('C07 transaction recovery decides publication separately from player text',()=>{
 const prepared={expected_head:head,actual_head:head,commit_sha:head,
   verified_blobs:true,transaction_status:'CONFIRMED',evidence:{commit_sha:head,readback:true}};
 assert.equal(continuationDecision(prepared),'SNAPSHOT_SYNCED');
 assert.equal(continuationDecision({...prepared,verified_blobs:false}),'PENDING_PERSISTENCE');
 assert.equal(continuationDecision({...prepared,actual_head:'a'.repeat(40)}),'HEAD_DIFFERENT');
 err(()=>examineFictionalFrame({test_only:true,output_delivered:true,
   transaction:{confirmed:false}}),'NARRATED_WITHOUT_CONFIRMED_PERSISTENCE');
});
test('C07 Git tx only disposable refs, no master write, deterministic content fingerprint',()=>{
 const a=[
   {path:'tmp/adr001-c03/narrative.txt',content:'TEST_ONLY no game fiction'},
   {path:'tmp/adr001-c03/state.json',content:'{"test_only":true}'}
 ];
 assert.equal(fingerprint(a),fingerprint(a.slice().reverse()));
 err(()=>new CandidateGitTransaction({repo:'Niltond3/novydres-persistence-poc',
   token:'TEST_ONLY',branch:'master',floor_sha:head}),'PROTECTED_REF');
 const x=new CandidateGitTransaction({repo:'Niltond3/novydres-persistence-poc',
   token:'TEST_ONLY',branch:'test/adr001-c03-c07-integration',floor_sha:head});
 assert.equal(x.floor_sha,head);
 // No network write from this test; remote C03 proof retained in Actions run.
});
test('C07 reuse B frozen fictional outputs and separate contextual review, no blind certification',()=>{
 const original=load(b+'resultado-testes.json').narrative_exercises_2026_11_12;
 const prior=load(b+'gate-e-readback.json').b05_independent_session_contextual_review_2026_11_12;
 const verdict=correlateFrozenBReview(original.exercises,original.targeted_followup,prior);
 assert.equal(verdict.case_count,8);
 assert.equal(verdict.blind_review,false);
 assert.equal(verdict.runtime_certified,false);
 assert.equal(examineFictionalFrame({test_only:true,npc:{friendly:true,opposes:true,
    automatic_compliance_from_courtesy:false}}).status,'REVIEW_READY_NOT_LITERARY_CERTIFIED');
});
test('C07 whole-tree audit must explicitly block cutover for pre-cutover legacy HEAD',()=>{
 const a=auditRepository(root);
 const z=auditRepository(root,{mode:'ZERO_LEGACY_FINAL'});
 assert.equal(a.gate,'C06_CANDIDATE_AUDIT_EXECUTED_WITH_LEGACY_PENDING');
 assert.equal(z.gate,'ZERO_LEGACY_BLOCKED');
 assert.ok(a.counters.legacy_paths>0);
 assert.ok(a.counters.media_pending>0);
 assert.equal(a.inventory_coverage.missing,0);
});
test('C07 visibly incomplete semantic truth is not automatically a technical failure',()=>{
 const frames={test_only:true,reported_fact:'TEST_ONLY claim unsupported by source'};
 assert.equal(examineFictionalFrame(frames).status,'REVIEW_READY_NOT_LITERARY_CERTIFIED');
 // This deliberately shows an undetected semantic false positive; independent
 // contextual review is still required and the runtime is not certified.
});
test('C07 local deterministic path measurements are labelled not comparable to Web',()=>{
 const c=buildCatalog();
 const path=c.subjects.find(x=>x.id===stateId).files.find(x=>x.path.endsWith('/atual.json')).path;
 const samples=[];
 for(let n=0;n<5;n++){
   const start=performance.now();
   const result=readSelected(root,c,stateId,{snapshot_sha:head,role:'AUDITOR',selected_paths:[path]});
   assert.equal(result.files.length,1);
   samples.push(performance.now()-start);
 }
 const summary={kind:'C07_LOCAL_NODE22_CHECKOUT_NOT_WEB_LATENCY',commit:head,
   samples_ms:samples.map(x=>Math.round(x*100)/100),
   p50_ms:quantile(samples,0.50),p95_ms_nearest_rank:quantile(samples,0.95),
   read_selected_calls:5,git_show_commands:10,actual_http_wire_bytes:'NOT_OBSERVABLE',model_tokens:'NOT_OBSERVABLE',
   baseline_comparable:false};
 console.log(JSON.stringify(summary));
 assert.ok(summary.p95_ms_nearest_rank>=summary.p50_ms);
});
