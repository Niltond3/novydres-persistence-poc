// D04: immutable C45 source readback, without promoting the C41 historical B fixture.
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
const P='novydres/cronicas/CHR-001/estado/recuperacao-c45.json';
const legacy='novydres/cronicas/CHR-001/estado/atual.json';
const fail=code=>{const e=new Error(code);e.code=code;throw e;};
const git=(...a)=>execFileSync('git',a,{encoding:'utf8',stdio:['ignore','pipe','ignore']}).trim();
const blob=s=>createHash('sha1').update('blob '+Buffer.byteLength(s)+'\0').update(s).digest('hex');
export function verifyD04State({override=null}={}){
 const c=override||JSON.parse(readFileSync(P,'utf8'));
 const b=JSON.parse(readFileSync(legacy,'utf8'));
 if(b.source_commit!=='c26c0fbf15fff6c817182c06e6208e302b954f3a'||b.cycle.id!=='CHR001-CYCLE-0041')fail('D04_HISTORICAL_C41_CORRUPTED');
 if(c.subject_id!=='chr001-state-checkpoint'||c.operational!==false||c.visibility!=='SYSTEM_AUDIT'||c.source_commit!=='c9fcfc0c558cd17d58ec8c8272da3ed70182ff37')fail('D04_UNAUTHORIZED_PROMOTION');
 const needed=['cycle','manifest','live','history','character','episode','knowledge','threads'];
 if(Object.keys(c.source_refs||{}).sort().join(',')!==needed.slice().sort().join(','))fail('D04_MISSING_PIN');
 const data={};
 for(const name of needed){
  const ref=c.source_refs[name];
  if(ref.source_commit!==c.source_commit||!/^[a-f0-9]{40}$/.test(ref.sha)||!ref.path.startsWith('novydres/')||ref.path.includes('..'))fail('D04_INVALID_PIN');
  if(git('rev-parse',c.source_commit+':'+ref.path)!==ref.sha)fail('D04_SOURCE_DRIFT');
  const body=execFileSync('git',['show',c.source_commit+':'+ref.path],{encoding:'utf8',stdio:['ignore','pipe','ignore']});
  if(blob(body)!==ref.sha)fail('D04_SOURCE_BYTES_DRIFT');
  data[name]=name==='character'||name==='episode'?body:JSON.parse(body);
 }
 const cy=data.cycle,li=data.live,ko=data.knowledge,th=data.threads,ev=c.cursor,r=c.resources;
 if(cy.cycle_id!=='CHR001-CYCLE-0045'||cy.manifest_ref.path!==c.source_refs.manifest.path||
   cy.manifest_ref.blob_sha!==c.source_refs.manifest.sha||
   cy.refs.character.blob_sha!==c.source_refs.character.sha||
   cy.refs.episode.blob_sha!==c.source_refs.episode.sha||
   cy.refs.live.blob_sha!==c.source_refs.live.sha||
   cy.refs.knowledge.blob_sha!==c.source_refs.knowledge.sha||
   cy.refs.threads.blob_sha!==c.source_refs.threads.sha)fail('D04_CYCLE_PIN_MISMATCH');
 if(ev.last_event_id!==cy.checkpoint.last_event_id||ev.last_event_id!==li.last_confirmed_event_id||
   ev.next_scene!==cy.checkpoint.next_scene||ev.next_scene_status!=='NOT_STARTED'||
   ev.last_closed_scene!==cy.checkpoint.last_closed_scene||ev.status!==cy.status||
   ev.next_role!==cy.next_role||ev.mortal!==true||ev.embrace_occurred!==false||
   ev.diegetic_year!==1970||ev.diegetic_civil_date!==null||ev.pending_persistence!==false||
   li.stage.M3_02!=='ACTIVE_C01_CLOSED'||!data.episode.includes(ev.last_event_id)||
   !data.character.includes(ev.last_event_id))fail('D04_C45_CURSOR_DRIFT');
 const live=li.character.resources;
 for(const [name,value] of Object.entries(r))if(!Number.isInteger(value)||value<0||live[name]!==value)fail('D04_RESOURCE_DRIFT');
 if(r.xp_total-r.xp_spent!==r.xp_remaining||r.willpower_provisional_max-r.willpower_superficial_damage-r.willpower_aggravated_damage!==r.willpower_available||r.xp_credit_available!==0)fail('D04_RESOURCE_DRIFT');
 if(!Array.isArray(ko.records)||ko.records.length!==c.knowledge.source_rows||
   !ko.records.every(x=>x.entity&&['confirmed','claims','suspected','unknown'].every(k=>Array.isArray(x[k])))||
   ko.last_event_id!==ev.last_event_id||ko.records.some(x=>x.confirmed.includes('AGENT_KNOWS_ALL')))
   fail('D04_KNOWLEDGE_SCOPE_DRIFT');
 if(!Array.isArray(th.threads)||th.threads.length!==c.open_threads.source_rows||
   th.last_event_id!==ev.last_event_id||c.knowledge.not_agent_to_player_disclosure!==true||
   c.provenance_policy.editorial_promotions!==false||c.provenance_policy.no_new_roll_or_technical_ledger!==true)
   fail('D04_UNPROVEN_THREAD_OR_PROMOTION');
 return {ok:true,gate:'D04_C45_SNAPSHOT_VERIFIED_NOT_FULL_D04_PASS',source_commit:c.source_commit,
  cursor:ev.last_event_id,actor_knowledge_records:ko.records.length,open_threads:th.threads.length};
}
if(process.argv[1]?.endsWith('verificar-estado-d04.mjs'))console.log(JSON.stringify(verifyD04State()));
