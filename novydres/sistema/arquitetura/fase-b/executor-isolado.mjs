// ADR-001 B04 — synthetic, non-operational regression harness. No network or CHR-001 edits.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const load = name => JSON.parse(readFileSync(new URL(name, import.meta.url), 'utf8'));
const negatives = load('./fixtures-negativos.json').cases;
const journeys = load('./fixtures-mutacoes.json').cases;
const clone = x => structuredClone(x);
const stable = x => JSON.stringify(x);
const baseline = {
  actor_id: 'artificial-npc-001', aliases: ['Test Alias'],
  confirmed: ['synthetic observed fact'],
  claims: [{ text:'synthetic unverified claim', epistemic:'NPC_CLAIM', known_by:['artificial-npc-001'] }],
  unknown: ['synthetic unknown'], future_contact:false, pc_obligation:false,
  technical_ledger_proven:false, last_event_id:'synthetic-event-001',
  resources:{ xp:10, fv:4 }, scene_started:false, source_sha:'a'.repeat(40)
};
const guards = [
  ['identity',x=>x.actor_id===baseline.actor_id],
  ['aliases',x=>stable(x.aliases)===stable(baseline.aliases)],
  ['claim-promotion',x=>stable(x.claims)===stable(baseline.claims)],
  ['unknown-suppression',x=>stable(x.unknown)===stable(baseline.unknown)],
  ['future-contact',x=>x.future_contact===baseline.future_contact],
  ['invent-pc-obligation',x=>x.pc_obligation===baseline.pc_obligation],
  ['forge-technical-ledger',x=>x.technical_ledger_proven===baseline.technical_ledger_proven],
  ['event-id-corruption',x=>x.last_event_id===baseline.last_event_id],
  ['xp-resource-change',x=>x.resources.xp===baseline.resources.xp],
  ['fv-resource-change',x=>x.resources.fv===baseline.resources.fv],
  ['unauthorized-scene-start',x=>x.scene_started===baseline.scene_started],
  ['source-hash-change',x=>x.source_sha===baseline.source_sha]
];
const mutations = {
  'identity':x=>x.actor_id='fake-id',
  'aliases':x=>x.aliases=[],
  'claim-promotion':x=>x.claims[0].epistemic='CONFIRMED',
  'unknown-suppression':x=>x.unknown=[],
  'future-contact':x=>x.future_contact=true,
  'invent-pc-obligation':x=>x.pc_obligation=true,
  'forge-technical-ledger':x=>x.technical_ledger_proven=true,
  'event-id-corruption':x=>x.last_event_id='fake',
  'xp-resource-change':x=>x.resources.xp=999,
  'fv-resource-change':x=>x.resources.fv=999,
  'unauthorized-scene-start':x=>x.scene_started=true,
  'source-hash-change':x=>x.source_sha='0'.repeat(40)
};
function validateSubject(x) {
  for (const [id, check] of guards) if(!check(x)) throw new Error('REJECT_'+id);
  return 'ACCEPT';
}
assert.equal(validateSubject(clone(baseline)), 'ACCEPT');
const negativeResults=[];
for (const tc of negatives) {
  assert.equal(tc.expected, 'REJECT');
  assert.ok(Object.hasOwn(mutations,tc.mutation), 'missing payload for '+tc.id);
  const sample=clone(baseline);mutations[tc.mutation](sample);
  let observed='ACCEPT'; try { validateSubject(sample); } catch { observed='REJECT'; }
  assert.equal(observed,tc.expected,tc.id);negativeResults.push({id:tc.id,observed});
}
function transact(store, tx) {
  if(tx.branch!=='test/adr001-local-isolation') throw new Error('branch_not_test');
  if(tx.frozen_file || tx.owner_duplicate || tx.activate_candidate_route || tx.synthetic_event_roll) throw new Error('scope');
  if(tx.visibility && !['PLAYER_SAFE','SYSTEM_AUDIT'].includes(tx.visibility)) throw new Error('visibility');
  if(tx.dangling_ref || tx.non_fast_forward) throw new Error('invalid_ref');
  const prev=store.transactions[tx.id];
  if(prev!==undefined) { if(prev!==tx.payload) throw new Error('conflicting_transaction_id'); return 'NO_OP'; }
  if(tx.expected_sha!==store.head) throw new Error('stale_sha');
  store.transactions[tx.id]=tx.payload;store.head='artificial-head-'+Object.keys(store.transactions).length;
  return 'COMMITTED';
}
const seed=()=>({head:'artificial-head-1',transactions:{'tx-seed':'value-one'}});
const normal={branch:'test/adr001-local-isolation',id:'tx-new',payload:'value-two',expected_sha:'artificial-head-1'};
assert.equal(transact(seed(),normal),'COMMITTED');
const journeyCases={
 'B-M01':{...normal,id:'tx-seed',payload:'value-one'},
 'B-M02':{...normal,id:'tx-seed',payload:'other-value'},
 'B-M03':{...normal,expected_sha:'obsolete-head'},
 'B-M04':{...normal,non_fast_forward:true},
 'B-M05':{...normal,branch:'master'},
 'B-M06':{...normal,dangling_ref:true},
 'B-M07':{...normal,owner_duplicate:true},
 'B-M08':{...normal,frozen_file:true},
 'B-M09':{...normal,visibility:'INVALID'},
 'B-M10':{...normal,activate_candidate_route:true},
 'B-M11':{...normal,synthetic_event_roll:true},
 'B-M12':{...normal,expected_sha:'obsolete-head'}
};
const journeyResults=[];
for(const tc of journeys){
  const tx=journeyCases[tc.id];assert.ok(tx,'missing executable journey '+tc.id);
  const s=seed(),before=stable(s);let observed;
  try { observed=transact(s,tx); } catch { observed='BLOCK'; }
  assert.equal(observed,tc.expected,tc.id);
  if(observed==='BLOCK'||observed==='NO_OP')assert.equal(stable(s),before,'state changed on '+tc.id);
  journeyResults.push({id:tc.id,observed});
}
assert.equal(negativeResults.length,12);
assert.equal(journeyResults.length,12);

// DEC-25/B04 additional evidence guards (artificial payloads only).
function evidenceGate(e) {
  if(e.source_authority!=='SUBJECT_OWNER') throw new Error('invalid_authority');
  if(!e.source_path || !e.source_locator) throw new Error('insufficient_source');
  if(e.knowledge_subject!==e.actor_id) throw new Error('improper_npc_knowledge');
  if(e.audience==='PLAYER' && ['GM_HIDDEN','SECRET','HIDDEN'].includes(e.visibility)) throw new Error('restricted_disclosure');
  if(e.source_sha!==e.pinned_source_sha) throw new Error('source_mismatch');
  if(e.checkpoint_sha!==e.remote_head_sha) throw new Error('checkpoint_drift');
  if(e.completion_claimed && (!e.proof_commit || !e.proof_blob)) throw new Error('unproven_completion');
  return 'ALLOW';
}
const goodEvidence={
  source_authority:'SUBJECT_OWNER',source_path:'artificial/path.json',source_locator:'/fact/0',
  actor_id:'synthetic-npc',knowledge_subject:'synthetic-npc',
  audience:'PLAYER',visibility:'PLAYER_SAFE',
  source_sha:'b'.repeat(40),pinned_source_sha:'b'.repeat(40),
  checkpoint_sha:'c'.repeat(40),remote_head_sha:'c'.repeat(40),
  completion_claimed:true,proof_commit:'c'.repeat(40),proof_blob:'b'.repeat(40)
};
assert.equal(evidenceGate(clone(goodEvidence)),'ALLOW');
const extraCases=[
  ['WRONG_AUTHORITY',x=>x.source_authority='OTHER_OWNER'],
  ['INSUFFICIENT_SOURCE',x=>x.source_locator=null],
  ['IMPROPER_NPC_KNOWLEDGE',x=>x.knowledge_subject='different-npc'],
  ['FORBIDDEN_DISCLOSURE',x=>x.visibility='GM_HIDDEN'],
  ['WRONG_SOURCE_SHA',x=>x.source_sha='0'.repeat(40)],
  ['CHECKPOINT_HEAD_DRIFT',x=>x.checkpoint_sha='0'.repeat(40)],
  ['UNPROVEN_COMPLETION',x=>x.proof_blob=null]
];
const extraResults=[];
for(const [id,alter] of extraCases){const x=clone(goodEvidence);alter(x);
  let outcome='ALLOW';try{evidenceGate(x)}catch{outcome='REJECT'}
  assert.equal(outcome,'REJECT',id);extraResults.push({id,outcome});
}
// Synthetic lost-ack recovery: discard first return, read persisted state, retry with same ID/payload.
// This is NOT an injected network failure and does NOT prove remote transaction idempotency.
const afterLostAck=seed(),recoveryTx={...normal};
transact(afterLostAck,recoveryTx);
assert.equal(afterLostAck.transactions[recoveryTx.id],recoveryTx.payload);
const recoveryHead=afterLostAck.head;
assert.equal(transact(afterLostAck,recoveryTx),'NO_OP');
assert.equal(afterLostAck.head,recoveryHead);

console.log(JSON.stringify({status:'PASS_SYNTHETIC_LOCAL_REFERENCE_IMPLEMENTATION',negative_total:12,negative_rejected:negativeResults.length,journey_total:12,journey_expected:journeyResults.length,remote_cas_test:'NOT_TESTED_BY_THIS_SCRIPT',extra_guard_total:extraResults.length,synthetic_lost_ack_recovery:'PASS_LOCAL_ONLY',independent_semantic_review:'NOT_EXECUTED',factual_canonicity:'NOT_EVALUATED'}));


// B04 real integration: this mode runs exclusively on a disposable GitHub ref via Actions.
// Local synthetic assertions above remain historical regression checks, not remote proof.
if (process.env.ADR001_REMOTE_PROOF === '1') {
  const { createHash } = await import('node:crypto');
  const { spawnSync } = await import('node:child_process');
  const token = process.env.GITHUB_TOKEN;
  const repo = process.env.GITHUB_REPOSITORY;
  const base = process.env.GITHUB_SHA;
  const branch = 'test/adr001-b04-ci-' + process.env.GITHUB_RUN_ID + '-' + process.env.GITHUB_RUN_ATTEMPT;
  assert.ok(token && repo && base && process.env.GITHUB_RUN_ID, 'CI token, repository, HEAD and run required');
  assert.ok(branch.startsWith('test/adr001-b04-ci-'));
  const sourcePath = 'novydres/sistema/arquitetura/fase-b/artificial-b04-source.txt';
  const ownerPath = 'novydres/sistema/arquitetura/fase-b/artificial-b04-transactions.json';
  const sourceText = 'TEST_ONLY; NOT_CAMPAIGN\nEvidence: the artificial custodian holds the blue key.\n';
  const sha256 = value => createHash('sha256').update(value).digest('hex');
  let disposableCreated = false, sourceBlob, sourceCommit, cleaned = false;
  const timings = [];
  async function api(method, endpoint, body) {
    const url = 'https://api.github.com/repos/' + repo + endpoint;
    const t0 = performance.now();
    const res = await fetch(url, { method, headers: {
      Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      'User-Agent': 'novydres-adr001-b04-isolated'
    }, body: body === undefined ? undefined : JSON.stringify(body) });
    const content = await res.text();
    timings.push({ operation: method + ' ' + endpoint.split('?')[0].split('/').slice(0,4).join('/'), milliseconds: Math.round(performance.now()-t0), http: res.status });
    let obj; try { obj = JSON.parse(content); } catch { obj = { message: content.slice(0,160) }; }
    if (!res.ok) { const error = new Error('GITHUB_HTTP_' + res.status + ': ' + String(obj.message).slice(0,250)); error.status = res.status; error.response = obj; throw error; }
    return obj;
  }
  const refEndpoint = '/git/refs/heads/' + branch;
  const getHead = async () => (await api('GET','/git/ref/heads/' + branch)).object.sha;
  const getCommit = sha => api('GET','/git/commits/' + sha);
  async function readPath(path) {
    try {
      const x=await api('GET','/contents/'+path+'?ref='+encodeURIComponent(branch));
      return { content: Buffer.from(x.content.replace(/\s/g,''), 'base64').toString('utf8'), blob_sha:x.sha };
    } catch(e) { if(e.status===404) return null; throw e; }
  }
  async function makeCommit(parent, changes, message) {
    const parentObject = await getCommit(parent);
    const tree = await api('POST','/git/trees',{base_tree:parentObject.tree.sha,
      tree:changes.map(x=>({path:x.path,mode:'100644',type:'blob',content:x.content}))});
    const commit = await api('POST','/git/commits',{message:'TEST_ONLY B04 '+message,tree:tree.sha,parents:[parent]});
    return {sha:commit.sha,parent,tree_sha:tree.sha};
  }
  const push = candidate => api('PATCH',refEndpoint,{sha:candidate.sha,force:false});
  async function verify(candidate, txId, fingerprint) {
    assert.equal(await getHead(),candidate.sha,'promoted HEAD');
    const obj=await getCommit(candidate.sha);
    assert.equal(obj.parents[0].sha,candidate.parent,'parent');
    assert.equal(obj.tree.sha,candidate.tree_sha,'tree');
    const stored=await readPath(ownerPath);
    assert.ok(stored,'owner exists in remote ref');
    assert.equal(JSON.parse(stored.content).transactions[txId],fingerprint,'tx persisted');
    return {head:candidate.sha,owner_blob:stored.blob_sha,parent:candidate.parent};
  }
  async function transact(expected, txId, payload, evidence, ackMode='normal') {
    const existing=await readPath(ownerPath);
    const saved=existing?JSON.parse(existing.content):{test_only:true,transactions:{}};
    const fingerprint=sha256(JSON.stringify(payload));
    if(Object.hasOwn(saved.transactions,txId)) {
      if(saved.transactions[txId]!==fingerprint) throw new Error('STOP_CONFLICT_SAME_TX_DIFFERENT_PAYLOAD');
      const head=await getHead(), commit=await getCommit(head), verified=await readPath(ownerPath);
      assert.ok(commit.tree.sha && verified && JSON.parse(verified.content).transactions[txId]===fingerprint,'remote idempotent readback');
      return {status:'NO_OP_VERIFIED',head,owner_blob:verified.blob_sha};
    }
    await validateEvidence(evidence);
    const observed=await getHead();
    if(observed!==expected) throw new Error('STALE_HEAD_PRECHECK_REMOTE_' + observed);
    saved.transactions[txId]=fingerprint;
    const candidate=await makeCommit(expected,[{path:ownerPath,content:JSON.stringify(saved,null,2)+'\n'}],txId);
    await push(candidate);
    if(ackMode==='discard_after_remote_success') throw new Error('CLIENT_SUPPRESSED_ACK_AFTER_REAL_REMOTE_WRITE');
    const verified=await verify(candidate,txId,fingerprint);
    return {status:'CONFIRMED',...verified};
  }
  async function validateEvidence(e) {
    if(e.role!=='SYSTEM_TEST') throw new Error('AUTHORITY_DENIED');
    if(e.audience==='PLAYER' && e.visibility!=='PLAYER_SAFE') throw new Error('DISCLOSURE_DENIED');
    if(e.actor!=='artificial-custodian') throw new Error('ACTOR_KNOWLEDGE_UNSUPPORTED');
    if(e.decision!=='ARTIFICIAL_DECISION_CURRENT') throw new Error('OBSOLETE_DECISION');
    const real=await readPath(e.source_path);
    if(!real) throw new Error('SOURCE_NOT_FOUND');
    if(e.source_path!==sourcePath) throw new Error('WRONG_SOURCE_PATH');
    if(real.blob_sha!==e.source_blob_sha) throw new Error('SOURCE_BLOB_MISMATCH');
    if(!real.content.includes(e.source_excerpt)) throw new Error('SOURCE_IRRELEVANT_TO_QUOTE');
    if(e.checkpoint!==await getHead()) throw new Error('CHECKPOINT_DIVERGED');
    if(e.conclusion==='PASS') {
      const claimed=e.external_proof;
      if(!claimed?.commit_sha || !claimed?.owner_blob_sha || claimed.commit_sha!==await getHead()) throw new Error('CONCLUSION_WITHOUT_PROOF');
      const proofCommit=await getCommit(claimed.commit_sha);
      const proofOwner=await readPath(ownerPath);
      if(!proofCommit.tree.sha || !proofOwner || proofOwner.blob_sha!==claimed.owner_blob_sha) throw new Error('CONCLUSION_WITHOUT_PROOF');
    }
  }
  try {
    await api('POST','/git/refs',{ref:'refs/heads/'+branch,sha:base});
    disposableCreated=true;
    sourceCommit=await makeCommit(base,[{path:sourcePath,content:sourceText}], 'seed-artificial-source');
    await push(sourceCommit);
    const savedSource=await readPath(sourcePath);
    assert.equal(savedSource.content,sourceText);
    sourceBlob=savedSource.blob_sha;
    const evidence=()=>({role:'SYSTEM_TEST',audience:'PLAYER',visibility:'PLAYER_SAFE',
      actor:'artificial-custodian',decision:'ARTIFICIAL_DECISION_CURRENT',
      source_path:sourcePath,source_blob_sha:sourceBlob,
      source_excerpt:'Evidence: the artificial custodian holds the blue key.',
      checkpoint:null,conclusion:'PENDING',external_proof:null});
    const e1={...evidence(),checkpoint:await getHead()};
    const t1=await transact(e1.checkpoint,'tx-artificial-01',{effect:'artificial-one'},e1);
    const firstHead=await getHead();
    const duplicate=await transact(e1.checkpoint,'tx-artificial-01',{effect:'artificial-one'},e1);
    assert.equal(duplicate.status,'NO_OP_VERIFIED');
    assert.equal(await getHead(),firstHead);
    await assert.rejects(transact(firstHead,'tx-artificial-01',{effect:'conflicting'},e1),/STOP_CONFLICT/);
    assert.equal(await getHead(),firstHead);
    const staleEvidence={...evidence(),checkpoint:firstHead};
    await validateEvidence({...staleEvidence,conclusion:'PASS',external_proof:{commit_sha:firstHead,owner_blob_sha:(await readPath(ownerPath)).blob_sha}});
    const wrongs=[
      ['SOURCE_NOT_FOUND',{source_path:sourcePath+'-missing'}],
      ['SOURCE_IRRELEVANT_TO_QUOTE',{source_excerpt:'the artificial custodian owns the red tower'}],
      ['OBSOLETE_DECISION',{decision:'ARTIFICIAL_DECISION_OBSOLETE'}],
      ['CHECKPOINT_DIVERGED',{checkpoint:base}],
      ['CONCLUSION_WITHOUT_PROOF',{conclusion:'PASS'}],
      ['CONCLUSION_BAD_PROOF',{conclusion:'PASS',external_proof:{commit_sha:base,owner_blob_sha:'0'.repeat(40)}}],
      ['ACTOR_KNOWLEDGE_UNSUPPORTED',{actor:'different-actor'}],
      ['DISCLOSURE_DENIED',{visibility:'GM_HIDDEN'}],
      ['AUTHORITY_DENIED',{role:'UNAUTHORIZED'}],
      ['SOURCE_BLOB_MISMATCH',{source_blob_sha:'0'.repeat(40)}]
    ];
    const rejected=[];
    for(const [label,delta] of wrongs) {
      const before=await getHead();
      await assert.rejects(validateEvidence({...staleEvidence,...delta}),new RegExp(label==='CONCLUSION_BAD_PROOF'?'CONCLUSION_WITHOUT_PROOF':label));
      assert.equal(await getHead(),before,'guard rejection must not mutate ref: '+label);
      rejected.push(label);
    }
    // A real remote commit is published; the client deliberately discards its ack.
    // This models an unknown outcome, not an injected network outage.
    const lost={...evidence(),checkpoint:await getHead()};
    await assert.rejects(transact(lost.checkpoint,'tx-artificial-lost-ack',
      {effect:'one-time-remote'},lost,'discard_after_remote_success'),/CLIENT_SUPPRESSED_ACK/);
    const recoveredHead=await getHead();
    const recovered=await transact(lost.checkpoint,'tx-artificial-lost-ack',
      {effect:'one-time-remote'},lost);
    assert.equal(recovered.status,'NO_OP_VERIFIED');
    assert.equal(await getHead(),recoveredHead,'no duplicate commit after unknown outcome');
    // Two sibling commits share the same real parent: exactly one may advance the ref.
    const raceBase=await getHead();
    const old=JSON.parse((await readPath(ownerPath)).content);
    const candidates=await Promise.all(['writer-a','writer-b'].map(async label => {
      const obj=structuredClone(old);obj.transactions['tx-'+label]=sha256(JSON.stringify({effect:label}));
      return makeCommit(raceBase,[{path:ownerPath,content:JSON.stringify(obj,null,2)+'\n'}],label);
    }));
    const attempts=await Promise.allSettled(candidates.map(c=>push(c)));
    const winners=attempts.map((a,i)=>a.status==='fulfilled'?i:-1).filter(i=>i>=0);
    assert.equal(winners.length,1,'exactly one remote fast-forward writer');
    const loser=1-winners[0], winning=candidates[winners[0]];
    const raceHead=await getHead();
    assert.equal(raceHead,winning.sha);
    const rejection=attempts[loser].reason;
    assert.equal(rejection.status,422,'loser rejected by GitHub REST HTTP 422');
    const staleProof=String(rejection.response?.message||'');
    assert.ok(staleProof.length>0,'retain native rejection message; generic 422 is not an exact SHA-lease diagnostic');
    const racedStored=JSON.parse((await readPath(ownerPath)).content);
    assert.ok(Object.hasOwn(racedStored.transactions,'tx-'+['writer-a','writer-b'][winners[0]]));
    assert.ok(!Object.hasOwn(racedStored.transactions,'tx-'+['writer-a','writer-b'][loser]));
    await assert.rejects(transact(raceBase,'tx-stale-late',{effect:'obsolete'},
      {...evidence(),checkpoint:raceBase}),/CHECKPOINT_DIVERGED/);
    assert.equal(await getHead(),raceHead);
    // Explicit stale-expected-SHA push: exercise Git transport's lease diagnostic,
    // not just the generic REST HTTP 422 response. This is ONLY a disposable test ref.
    const leaseArgs=['push','--force-with-lease=refs/heads/'+branch+':'+raceBase,'origin',base+':refs/heads/'+branch];
    const leaseProbe=spawnSync('git',leaseArgs,{encoding:'utf8',timeout:20000});
    const leaseOutput=(leaseProbe.stdout||'')+'\n'+(leaseProbe.stderr||'');
    assert.notEqual(leaseProbe.status,0,'obsolete expected SHA push must fail');
    assert.match(leaseOutput,/stale info/i,'explicit stale lease transport diagnostic');
    assert.equal(await getHead(),raceHead,'real remote ref unchanged after explicit stale lease');
    console.log(JSON.stringify({status:'PASS_REAL_GITHUB_DISPOSABLE_REF',
      run_id:process.env.GITHUB_RUN_ID,head_under_test:base,sandbox_ref:branch,
      seed_commit:sourceCommit.sha,source_blob_sha:sourceBlob,
      first_transaction:t1,duplicate_tx:duplicate.status,conflict_tx:'STOP_CONFLICT',
      rejected_guards:rejected,client_suppressed_ack_recovery:recovered.status,
      acknowledgement_failure_mode:'CLIENT_SUPPRESSED_AFTER_REAL_REMOTE_WRITE_NOT_NETWORK_INJECTION',
      concurrent_writers:'ONE_WINNER_REMOTE_422_GENERIC_REJECTION',
      winner_commit:winning.sha,loser_commit:candidates[loser].sha,
      native_rejection_http:rejection.status,native_rejection_message:staleProof,
      native_stale_lease_diagnostic:'NOT_PROVEN_BY_GENERIC_422',
      explicit_git_lease_result:'REJECTED_STALE_INFO',explicit_git_lease_exit:leaseProbe.status,
      explicit_git_lease_message:leaseOutput.slice(0,450),
      stale_precheck:'REMOTE_CHECKPOINT_VALIDATOR_BLOCK',remote_head_readback:raceHead,
      requests_sample:timings.length,latency_p95:'NOT_REPORTED_SMALL_NONCOMPARABLE_SAMPLE',
      timings_ms:timings.filter(x=>x.http>=400 || x.operation.startsWith('PATCH')),
      content_scope:'ARTIFICIAL_ONLY_NO_CAMPAIGN_WRITES'}));
  } finally {
    if(disposableCreated) {
      try { await api('DELETE','/git/refs/heads/'+branch); cleaned=true; }
      catch(e) { console.error('DISPOSABLE_REF_CLEANUP_FAILED '+e.message); }
    }
    console.log(JSON.stringify({disposable_ref:branch,cleanup:cleaned?'CONFIRMED':'NOT_CONFIRMED'}));
  }
}
