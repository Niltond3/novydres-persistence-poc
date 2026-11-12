// ADR-001 C03 — candidate Git transaction executor. Non-operational.
// Real remote proof is restricted to disposable test/adr001-c03-* refs and
// tmp/adr001-c03/* paths. No master, canon, runtime, scene or campaign writes.
import { createHash } from 'node:crypto';

const SHA=/^[a-f0-9]{40}$/;
const ID=/^tx-[a-z0-9][a-z0-9-]{1,63}$/;
const TEST_REF=/^test\/adr001-c03-[a-z0-9-]+$/;
const TEST_PATH=/^tmp\/adr001-c03\/[a-z0-9][a-z0-9-]*\.(?:json|txt)$/;
const fail=(code,detail='')=>{ const error=new Error(code+(detail?': '+detail:''));error.code=code;throw error; };
const sha256=s=>createHash('sha256').update(s).digest('hex');
const blobSHA=content=>{const b=Buffer.from(content,'utf8');return createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');};
const sortByPath=(a,b)=>a.path<b.path?-1:a.path>b.path?1:0;

function canonicalChanges(changes) {
  if(!Array.isArray(changes)||changes.length<2)fail('ATOMIC_TEXT_AND_STATE_REQUIRED');
  const c=changes.map(x=>({...x}));
  if(c.some(x=>!TEST_PATH.test(x.path||'')||typeof x.content!=='string'))fail('UNAUTHORIZED_PATH');
  if(new Set(c.map(x=>x.path)).size!==c.length)fail('DUPLICATE_PATH');
  if(!c.some(x=>x.path.endsWith('.txt'))||!c.some(x=>x.path.endsWith('.json')))fail('ATOMIC_TEXT_AND_STATE_REQUIRED');
  return c.sort(sortByPath);
}
export function fingerprint(changes) {
  return sha256(JSON.stringify(canonicalChanges(changes).map(x=>({path:x.path,blob_sha:blobSHA(x.content)}))));
}
function parseMarker(message) {
  const tx=/^ADR001-C03-TX-ID: (tx-[a-z0-9-]+)$/m.exec(message||'');
  const fingerprint=/^ADR001-C03-FINGERPRINT: ([a-f0-9]{64})$/m.exec(message||'');
  return tx&&fingerprint?{tx_id:tx[1],fingerprint:fingerprint[1]}:null;
}
export class CandidateGitTransaction {
  constructor({repo,token,branch,floor_sha}) {
    if(!/^[-\w]+\/[-\w.]+$/.test(repo||'')||!token)fail('API_CREDENTIALS_MISSING');
    if(!TEST_REF.test(branch||''))fail('PROTECTED_REF');
    if(!SHA.test(floor_sha||''))fail('SNAPSHOT_REQUIRED');
    this.repo=repo;this.token=token;this.branch=branch;this.floor_sha=floor_sha;
  }
  async api(method,path,body) {
    const reply=await fetch('https://api.github.com/repos/'+this.repo+path,{
      method,headers:{Accept:'application/vnd.github+json',Authorization:'Bearer '+this.token,
       'X-GitHub-Api-Version':'2022-11-28','Content-Type':'application/json'},
      body:body===undefined?undefined:JSON.stringify(body)});
    const value=await reply.json().catch(()=>({}));
    if(!reply.ok){const e=new Error('GITHUB_'+reply.status+': '+String(value.message||''));e.status=reply.status;throw e;}
    return value;
  }
  async head(){return (await this.api('GET','/git/ref/heads/'+this.branch)).object.sha;}
  async commit(sha){return this.api('GET','/git/commits/'+sha);}
  async getContent(path,sha) {
    const value=await this.api('GET','/contents/'+path+'?ref='+sha);
    if(value.type!=='file'||value.encoding!=='base64')fail('INVALID_REMOTE_FILE',path);
    return {content:Buffer.from(value.content.replace(/\s/g,''),'base64').toString('utf8'),blob_sha:value.sha};
  }
  // Bounded traversal: unknown history is a STOP, not proof of no duplicate.
  async historyFor(txId,head) {
    let cur=head;
    for(let depth=0;depth<200;depth++) {
      if(cur===this.floor_sha)return null;
      const c=await this.commit(cur), marker=parseMarker(c.message);
      if(marker?.tx_id===txId)return {sha:cur,marker,object:c};
      if(c.parents.length!==1)fail('HISTORY_NOT_LINEAR');
      cur=c.parents[0].sha;
    }
    fail('HISTORY_RECOVERY_INCOMPLETE');
  }
  async verify(sha,parent,changes) {
    const c=await this.commit(sha);
    if(c.parents.length!==1||c.parents[0].sha!==parent)fail('PARENT_MISMATCH');
    if(!SHA.test(c.tree.sha))fail('TREE_MISSING');
    const checked=[];
    for(const x of changes) {
      const remote=await this.getContent(x.path,sha),expected=blobSHA(x.content);
      if(remote.blob_sha!==expected||remote.content!==x.content)fail('READBACK_BLOB_MISMATCH',x.path);
      checked.push({path:x.path,blob_sha:remote.blob_sha});
    }
    return {commit_sha:sha,parent_sha:parent,tree_sha:c.tree.sha,blobs:checked};
  }
  async transact({expected_head,tx_id,changes,authority='TEST_ONLY',simulate_ack_loss=false,
    stop_before_ref=false}) {
    if(!SHA.test(expected_head||'')||!ID.test(tx_id||''))fail('TRANSACTION_INVALID');
    if(authority!=='TEST_ONLY')fail('AUTHORITY_DENIED');
    const canonical=canonicalChanges(changes),fp=fingerprint(canonical),current=await this.head();
    const prior=await this.historyFor(tx_id,current);
    if(prior) {
      if(prior.marker.fingerprint!==fp)fail('STOP_CONFLICT_SAME_ID');
      const original=await this.verify(prior.sha,prior.object.parents[0].sha,canonical);
      // If later commits touched the same fields, a retry must reconcile, not
      // falsely report a current state equivalent to this historical transaction.
      for(const x of canonical) {
        const now=await this.getContent(x.path,current);
        if(now.blob_sha!==blobSHA(x.content))fail('STOP_CONFLICT_EFFECT_CHANGED',x.path);
      }
      return {status:'NO_OP_VERIFIED',head:current,tx_id,original};
    }
    if(current!==expected_head)fail('STALE_HEAD_PRECHECK',current);
    const base=await this.commit(expected_head);
    const blobs=[];
    for(const x of canonical) {
      const returned=await this.api('POST','/git/blobs',{content:x.content,encoding:'utf-8'});
      if(returned.sha!==blobSHA(x.content))fail('CREATED_BLOB_MISMATCH',x.path);
      blobs.push({...x,sha:returned.sha});
    }
    const tree=await this.api('POST','/git/trees',{base_tree:base.tree.sha,tree:blobs.map(x=>({
      path:x.path,mode:'100644',type:'blob',sha:x.sha}))});
    const message='ADR-001 C03 isolated transaction (no campaign writes)\n\n'+
      'ADR001-C03-TX-ID: '+tx_id+'\nADR001-C03-FINGERPRINT: '+fp;
    const candidate=await this.api('POST','/git/commits',{message,tree:tree.sha,parents:[expected_head]});
    if(stop_before_ref) {
      if(await this.head()!==expected_head)fail('UNPUBLISHED_BRANCH_DRIFT');
      return {status:'COMMIT_OBJECT_CREATED_UNPUBLISHED',commit_sha:candidate.sha,head:expected_head};
    }
    try {await this.api('PATCH','/git/refs/heads/'+this.branch,{sha:candidate.sha,force:false});}
    catch(e) {
      if((await this.head())===candidate.sha)fail('PENDING_PERSISTENCE_ACK_UNKNOWN');
      if(e.status===422)fail('STOP_CONFLICT_STALE_REMOTE');
      fail('PENDING_PERSISTENCE_ACK_UNKNOWN');
    }
    if(simulate_ack_loss)fail('CLIENT_SUPPRESSED_ACK_AFTER_REMOTE_COMMIT');
    const currentAfter=await this.head();
    if(currentAfter!==candidate.sha)fail('PENDING_PERSISTENCE_READBACK',currentAfter);
    const verified=await this.verify(candidate.sha,expected_head,canonical);
    if(verified.tree_sha!==tree.sha)fail('TREE_MISMATCH');
    return {status:'CONFIRMED',tx_id,head:currentAfter,verified};
  }
}
