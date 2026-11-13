import test from 'node:test';
import assert from 'node:assert/strict';
import {CandidateGitTransaction,fingerprint} from './transacao-git.mjs';
const env=process.env, token=env.GITHUB_TOKEN,repo=env.GITHUB_REPOSITORY;
const floor=env.GITHUB_SHA,runId=env.GITHUB_RUN_ID,attempt=env.GITHUB_RUN_ATTEMPT||'1';
if(!token||!repo||!runId||!/^[a-f0-9]{40}$/.test(floor||''))throw Error('REAL_GITHUB_ACTIONS_ENV_REQUIRED');
const branch='test/adr001-c03-'+runId+'-'+attempt;
const client=new CandidateGitTransaction({repo,token,branch,floor_sha:floor});
const changes=n=>[
 {path:'tmp/adr001-c03/scene.txt',content:'TEST_ONLY '+n+'\nNo game scene or player action.\n'},
 {path:'tmp/adr001-c03/state.json',content:JSON.stringify({test_only:true,resources:{xp:10,fv:4},marker:n},null,2)+'\n'}
];
const reject=(promise,code)=>assert.rejects(promise,e=>e.code===code,'expected '+code);
test('V05/V10 real remote atomicity, idempotence, stale, lost ack and concurrency',async()=>{
 const result={status:'PENDING',run_id:runId,source_head:floor,branch};
 let created=false;
 try{
  await client.api('POST','/git/refs',{ref:'refs/heads/'+branch,sha:floor});created=true;
  assert.equal(await client.head(),floor);
  const input=changes('first');
  assert.equal(fingerprint(input),fingerprint([...input].reverse()));
  assert.throws(()=>new CandidateGitTransaction({repo,token,branch:'master',floor_sha:floor}),e=>e.code==='PROTECTED_REF');
  await reject(client.transact({expected_head:floor,tx_id:'tx-c03-denied',changes:input,authority:'BAD'}),'AUTHORITY_DENIED');
  await reject(client.transact({expected_head:floor,tx_id:'tx-c03-invalid-path',
   changes:[{path:'novydres/cronicas/CHR-001/estado/atual.json',content:'{}'},input[0]]}),'UNAUTHORIZED_PATH');
  assert.equal(await client.head(),floor);
  const unpub=await client.transact({expected_head:floor,tx_id:'tx-c03-orphan',
   changes:changes('object-only'),stop_before_ref:true});
  assert.equal(unpub.status,'COMMIT_OBJECT_CREATED_UNPUBLISHED');
  assert.equal(await client.head(),floor);
  const first=await client.transact({expected_head:floor,tx_id:'tx-c03-first',changes:input});
  assert.equal(first.status,'CONFIRMED');assert.equal(first.verified.parent_sha,floor);
  assert.equal(first.verified.blobs.length,2);
  const duplicate=await client.transact({expected_head:floor,tx_id:'tx-c03-first',changes:input});
  assert.equal(duplicate.status,'NO_OP_VERIFIED');assert.equal(await client.head(),first.head);
  await reject(client.transact({expected_head:first.head,tx_id:'tx-c03-first',changes:changes('conflicting')}),'STOP_CONFLICT_SAME_ID');
  await reject(client.verify(first.head,floor,changes('tampered')),'READBACK_BLOB_MISMATCH');
  assert.equal(await client.head(),first.head);
  const lost=changes('suppressed-ack');
  let suppressed;
  await assert.rejects(client.transact({expected_head:first.head,tx_id:'tx-c03-lost',changes:lost,
   simulate_ack_loss:true}),e=>{
     suppressed=e;return e.code==='CLIENT_SUPPRESSED_ACK_AFTER_REMOTE_COMMIT'&&/^[a-f0-9]{40}$/.test(e.commit_sha||'');
   });
  const afterLost=await client.waitForPublished(suppressed.commit_sha,{previous:first.head});
  assert.notEqual(afterLost,first.head);
  const recovered=await client.transact({expected_head:first.head,tx_id:'tx-c03-lost',changes:lost});
  assert.equal(recovered.status,'NO_OP_VERIFIED');assert.equal(recovered.head,afterLost);
  await reject(client.transact({expected_head:first.head,tx_id:'tx-c03-stale',changes:changes('stale')}),'STALE_HEAD_PRECHECK');
  const runs=await Promise.allSettled(['writer-a','writer-b'].map(n=>
   client.transact({expected_head:afterLost,tx_id:'tx-c03-'+n,changes:changes(n)})));
  const wins=runs.map((x,i)=>x.status==='fulfilled'?i:-1).filter(x=>x!==-1);
  assert.equal(wins.length,1,'remote write must have one winner');
  const loser=runs[1-wins[0]];assert.equal(loser.status,'rejected');
  assert.ok(['STALE_HEAD_PRECHECK','STOP_CONFLICT_STALE_REMOTE'].includes(loser.reason.code));
  const head=await client.head();assert.equal(head,runs[wins[0]].value.head);
  const final=await client.verify(head,afterLost,changes(wins[0]?'writer-b':'writer-a'));
  assert.equal(final.commit_sha,head);
  Object.assign(result,{status:'PASS_REAL_GITHUB_DISPOSABLE',first:{commit_sha:first.head,parent:floor,blobs:first.verified.blobs},
   duplicate:duplicate.status,conflict:'STOP_CONFLICT_SAME_ID',injected_bad_readback:'READBACK_BLOB_MISMATCH',
   object_unpublished:unpub.status,ack_suppressed_after_remote_success:true,
   recovered:recovered.status,stale:'STALE_HEAD_PRECHECK',
   concurrent:{winner:head,loser:loser.reason.code},master_or_campaign_changed:false});
  console.log(JSON.stringify(result));
 }finally{
  if(created){
   await client.api('DELETE','/git/refs/heads/'+branch);
   await assert.rejects(client.head(),e=>e.status===404);
   console.log(JSON.stringify({test_ref:branch,cleanup:'CONFIRMED'}));
  }
 }
});

test('bounded eventual-consistency ref readback never confirms stale or divergent HEAD',async()=>{
 const c=Object.create(CandidateGitTransaction.prototype);
 const old='a'.repeat(40),next='b'.repeat(40),other='c'.repeat(40);
 let seq=0;c.head=async()=>++seq<3?old:next;
 assert.equal(await c.waitForPublished(next,{previous:old,attempts:4,delayMs:0}),next);
 c.head=async()=>old;
 await assert.rejects(c.waitForPublished(next,{previous:old,attempts:3,delayMs:0}),e=>e.code==='PENDING_PERSISTENCE_READBACK');
 c.head=async()=>other;
 await assert.rejects(c.waitForPublished(next,{previous:old,attempts:3,delayMs:0}),e=>e.code==='STOP_CONFLICT_REF_MOVED');
});
