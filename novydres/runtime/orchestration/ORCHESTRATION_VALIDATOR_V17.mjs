#!/usr/bin/env node
// V17: deterministic prospective gate; verifies C43, 42 predecessor SHA links, 44 threads, no G28.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {validateC42} from './ORCHESTRATION_VALIDATOR_V16.mjs';
import {validateTemporalTransition} from '../scene-execution/TEMPORAL_TRANSITION_VALIDATOR_V1.mjs';
const ok=(v,m)=>{if(!v)throw Error('CHR001_V17_BLOCK:'+m)};
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const hash=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const file=(root,p)=>{ok(typeof p==='string'&&p.startsWith('novydres/')&&!p.split(/[\\/]/).includes('..'),'unsafe path');return fs.readFileSync(path.resolve(root,p));};
const j=(root,p)=>JSON.parse(file(root,p).toString('utf8'));
const pin=(root,x,k)=>{ok(x?.path&&/^[0-9a-f]{40}$/.test(x.blob_sha),k+' malformed');ok(hash(file(root,x.path))===x.blob_sha,k+' SHA mismatch '+x.path);};
const cycle=n=>'novydres/chronicles/CHR-001/orchestration/CYCLE_V'+String(n).padStart(4,'0')+'.json';
const successors=["start_here","orchestration_contract","handoff_to_narrador","cycle_schema","cycle_validator","cycle_tests","cycle_schema_tests","temporal_transition_packet","temporal_transition_tests","temporal_transition_schema_tests"];
export function validateC43(c,p){
 ok(c?.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V17'&&c.cycle_id==='CHR001-CYCLE-0043'&&c.sequence===43,'cycle identity');
 ok(p?.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V16'&&p.sequence===42,'predecessor identity');
 ok(c.transition==='TEMPORAL_RECONCILIATION_PASS'&&c.status==='READY_FOR_NARRATOR'&&c.next_role==='NARRADOR','readiness mismatch');
 ok(c.source_head_sha==='d14e1a90de81f0348f2fd07062427b0602de3eb0','source HEAD');
 ok(c.manifest_path==='novydres/MANIFEST_V58.json'&&c.manifest_ref.path===c.manifest_path,'manifest path');
 ok(c.previous_cycle.path===cycle(42)&&c.previous_cycle.blob_sha==='2f0fffffffffffffffffffffffffffffffffffffff'.replace('2f0fffffffffffffffffffffffffffffffffffffff','47e9334b4c1696b8334c63ba938da25cf4f8e644'),'predecessor SHA');
 for(const k of ['checkpoint','refs','plan','scene_frame','activation','guards','operational_gates','pending_player_decision','temporal_governance','blocking'])
  ok(eq(c[k],p[k]),'protected historical field changed '+k);
 ok(Object.keys(c.architecture).length===Object.keys(p.architecture).length,'architecture key drift');
 for(const [k,v] of Object.entries(p.architecture))if(!successors.includes(k))ok(eq(c.architecture[k],v),'unapproved architecture change '+k);
 for(const k of successors)ok(c.architecture[k]?.path&&/^[a-f0-9]{40}$/.test(c.architecture[k].blob_sha),'missing successor '+k);
 ok(c.review?.decision==='TEMPORAL_RECONCILIATION_PASS'&&c.review.against_last_event_id===c.checkpoint.last_event_id,'review mismatch');
 const t=c.transition_readiness;
 ok(t?.status==='READY'&&t.effective_narrator_permission===true,'temporal not READY');
 ok(t.chat_opening_observed===true&&t.g28_scene_event_recorded===false&&t.no_story_delta===true,'chat fact erased or G28 forged');
 ok(eq(t.source_cycle_ref,c.previous_cycle),'source cycle ref');
 ok(t.source_manifest_ref.path===p.manifest_path&&t.source_manifest_ref.blob_sha===p.manifest_ref.blob_sha,'source manifest ref');
 ok(eq(t.packet_ref,c.architecture.temporal_transition_packet),'packet mismatch');
 ok(t.packet_ref.path==='novydres/chronicles/CHR-001/preparations/M3.02_TEMPORAL_TRANSITION_V2_PLAYER_SAFE.json','wrong packet version');
 return {ok:true,active_permission:true};
}
export function validateLatestV17(root){
 const dir=path.resolve(root,'novydres/chronicles/CHR-001/orchestration');
 const ns=fs.readdirSync(dir).map(x=>/^CYCLE_V(\d{4})\.json$/.exec(x)).filter(Boolean).map(x=>Number(x[1]));
 ok(ns.length===43&&Math.max(...ns)===43,'unexpected cycle count');
 const c=j(root,cycle(43)),p=j(root,cycle(42)),p41=j(root,cycle(41));
 validateC42(p,p41);validateC43(c,p);
 for(let n=43;n>=2;n--){const x=j(root,cycle(n));ok(x.previous_cycle.path===cycle(n-1),'broken predecessor chain '+n);pin(root,x.previous_cycle,'cycle predecessor '+n);}
 pin(root,c.manifest_ref,'manifest');
 for(const [k,v] of Object.entries(c.refs))pin(root,v,'source '+k);
 for(const [k,v] of Object.entries(c.architecture))pin(root,v,'architecture '+k);
 for(const [k,v] of Object.entries(c.activation))pin(root,v,'activation '+k);
 for(const [k,v] of Object.entries(c.operational_gates.mechanical_sources))pin(root,v,'mechanical '+k);
 pin(root,c.operational_gates.mechanical_matrix_ref,'mechanical matrix');
 pin(root,c.plan.dossier,'original dossier');pin(root,c.plan.sidecar,'original sidecar');
 pin(root,c.transition_readiness.packet_ref,'transition packet');
 const q=validateTemporalTransition(root,c.transition_readiness.packet_ref.path);
 ok(q.package_status==='READY'&&q.ready&&q.issues.length===0,'temporal packet has issues: '+q.issues);
 ok(q.source_thread_count===44&&q.disposition_count===44,'44 source threads mismatch');
 const m=j(root,c.manifest_path),o=m.runtime?.orchestration,na=m.runtime?.narrative_architecture,t=m.runtime?.temporal_transition;
 ok(o?.current_cycle===cycle(43)&&o.status===c.status&&o.next_role==='NARRADOR'&&o.next_scene_executable===true,'manifest current cursor');
 ok(m.runtime.last_confirmed_narrative_event===c.checkpoint.last_event_id,'last event drift');
 ok(t?.status==='READY'&&t.effective_narrator_permission===true&&eq(t.packet_ref,c.architecture.temporal_transition_packet),'manifest temporal status');
 ok(t.chat_opening_observed===true&&t.chat_opening_g28_persisted===false&&t.no_new_scene_event===true,'manifest chat opening/G28');
 for(const [k,v] of Object.entries(c.architecture))ok(eq(na.blob_refs[k],v),'manifest missing pin '+k);
 for(const [field,key] of [['contract','orchestration_contract'],['entrypoint','start_here'],['cycle_schema','cycle_schema'],['validator','cycle_validator'],['tests','cycle_tests'],['schema_tests','cycle_schema_tests']])
 ok(o[field]===c.architecture[key].path&&o[field+'_blob_sha']===c.architecture[key].blob_sha,'manifest pointer '+field);
 const git=a=>execFileSync('git',['-C',root,...a],{encoding:'utf8'}).trim();
 ok(git(['rev-parse','HEAD:'+cycle(43)])===hash(file(root,cycle(43))),'cycle not at checkout HEAD');
 ok(git(['rev-parse','HEAD:'+c.manifest_path])===c.manifest_ref.blob_sha,'manifest not at checkout HEAD');
 ok(git(['merge-base','--is-ancestor',c.source_head_sha,'HEAD'])==='','source master HEAD not ancestor');
 return {ok:true,cycle:c.cycle_id,status:c.status,thread_dispositions:44,salient:q.salient_ids.length,protected_state_refs:6,predecessor_links:42,ready_for_narrator:true,no_played_event:true};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){
 try{const i=process.argv.indexOf('--root');console.log(JSON.stringify(validateLatestV17(path.resolve(i<0?process.cwd():process.argv[i+1]))));}
 catch(e){console.error(String(e));process.exitCode=1;}
}
