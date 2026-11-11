#!/usr/bin/env node
// NOVYDRES CHR-001 V16: administrative activation of material-temporal gate, no play-state mutation.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {validateC41} from './ORCHESTRATION_VALIDATOR_V15.mjs';
import {validateTemporalTransition} from '../scene-execution/TEMPORAL_TRANSITION_VALIDATOR_V1.mjs';

const fail=m=>{throw Error('CHR001_V16_BLOCK:'+m)},ok=(v,m)=>{if(!v)fail(m)};
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const hash=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const file=(root,p)=>{ok(typeof p==='string'&&p.startsWith('novydres/')&&!p.split(/[\/\\]/).includes('..'),'unsafe path '+p);return fs.readFileSync(path.resolve(root,p))};
const j=(root,p)=>JSON.parse(file(root,p).toString('utf8'));
const pin=(root,x,name)=>{ok(x?.path&&/^[a-f0-9]{40}$/.test(x.blob_sha),name+' malformed');ok(hash(file(root,x.path))===x.blob_sha,name+' content mismatch '+x.path)};
const cycle=n=>'novydres/chronicles/CHR-001/orchestration/CYCLE_V'+String(n).padStart(4,'0')+'.json';
const newArch=['temporal_transition_gate_contract','temporal_transition_schema','temporal_transition_validator','temporal_transition_tests','temporal_transition_schema_tests','temporal_transition_packet'];
const changed=['start_here','orchestration_contract','cycle_schema','cycle_validator','cycle_tests','cycle_schema_tests','role_dramaturgo','role_narrador','handoff_to_narrador','pacing_policy'];
export function validateC42(c,prev){
 ok(c?.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V16'&&c.cycle_id==='CHR001-CYCLE-0042'&&c.sequence===42,'wrong cycle');
 ok(prev?.sequence===41&&prev.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V15','wrong predecessor');
 ok(c.transition==='TEMPORAL_GATE_ACTIVATED_REVIEW_REQUIRED'&&c.status==='TEMPORAL_RECONCILIATION_REQUIRED'&&c.next_role==='DRAMATURGO','false readiness');
 ok(c.source_head_sha==='c26c0fbf15fff6c817182c06e6208e302b954f3a','wrong initial HEAD');
 ok(c.previous_cycle?.path===cycle(41)&&c.previous_cycle.blob_sha==='06398ed7cbc19e315fb7d59b08cc807b3e36c88d','wrong prior pin');
 ok(c.manifest_path==='novydres/MANIFEST_V57.json'&&eq(c.manifest_ref?.path,c.manifest_path),'manifest path');
 for(const k of ['checkpoint','refs','plan','scene_frame','activation','guards','operational_gates','blocking','pending_player_decision'])ok(eq(c[k],prev[k]),'protected historical field changed '+k);
 ok(eq({...c.temporal_governance,pacing_ref:prev.temporal_governance.pacing_ref},prev.temporal_governance),'temporal source changed beyond prospective pacing successor');
 ok(eq(c.temporal_governance.pacing_ref,c.architecture.pacing_policy),'new pacing ref is not active');
 ok(c.review?.decision==='TEMPORAL_GATE_ACTIVATED_REVIEW_REQUIRED'&&c.review.against_last_event_id===c.checkpoint.last_event_id,'review mismatch');
 ok(Object.keys(c.architecture||{}).length===Object.keys(prev.architecture).length+newArch.length,'architecture size');
 for(const [k,v] of Object.entries(prev.architecture))if(!changed.includes(k))ok(eq(c.architecture[k],v),'changed non-successor arch '+k);
 for(const k of [...changed,...newArch])ok(c.architecture[k]?.path&&/^[a-f0-9]{40}$/.test(c.architecture[k].blob_sha),'missing revision '+k);
 const t=c.transition_readiness;
 ok(t?.status==='REVIEW_REQUIRED'&&t?.effective_narrator_permission===false,'permission not blocked');
 ok(t?.chat_opening_observed===true&&t?.g28_scene_event_recorded===false&&t?.no_story_delta===true,'chat fact erased or made event');
 ok(eq(t?.source_cycle_ref,c.previous_cycle),'transition source cycle');
 ok(t?.source_manifest_ref?.path===prev.manifest_path&&t.source_manifest_ref.blob_sha===prev.manifest_ref.blob_sha,'transition source manifest');
 ok(eq(t?.packet_ref,c.architecture.temporal_transition_packet),'packet pin missing');
 return {ok:true,status:c.status,active_permission:false};
}
export function validateLatestV16(root){
 const dir=path.resolve(root,'novydres/chronicles/CHR-001/orchestration');
 const ns=fs.readdirSync(dir).map(x=>/^CYCLE_V(\d{4})\.json$/.exec(x)).filter(Boolean).map(x=>Number(x[1]));
 ok(ns.length===42&&Math.max(...ns)===42,'unexpected cycle count');
 const c=j(root,cycle(42)),prior=j(root,cycle(41)),p40=j(root,cycle(40));
 validateC41(prior,p40);validateC42(c,prior);
 for(let n=42;n>=2;n--){const v=j(root,cycle(n));ok(v.previous_cycle.path===cycle(n-1),'broken predecessor link '+n);pin(root,v.previous_cycle,'cycle predecessor '+n)}
 pin(root,c.manifest_ref,'manifest');
 for(const [k,v] of Object.entries(c.refs))pin(root,v,'source '+k);
 for(const [k,v] of Object.entries(c.architecture))pin(root,v,'architecture '+k);
 for(const [k,v] of Object.entries(c.activation))pin(root,v,'activation '+k);
 for(const [k,v] of Object.entries(c.operational_gates.mechanical_sources))pin(root,v,'mechanical '+k);
 pin(root,c.operational_gates.mechanical_matrix_ref,'mechanical matrix');
 pin(root,c.plan.dossier,'original dossier');pin(root,c.plan.sidecar,'original sidecar');
 pin(root,c.transition_readiness.packet_ref,'transition packet');
 const report=validateTemporalTransition(root,c.transition_readiness.packet_ref.path);
 ok(report.package_status==='REVIEW_REQUIRED'&&!report.ready,'old review inaccurately marked ready');
 for(const code of ['INTERVAL_UNBOUNDED','MATERIAL_CUSTODY_UNRESOLVED','PLAYER_CHOICE_PENDING','GEOMETRY_UNSPECIFIED:obstacle_type','OPENING_INCOMPLETE'])
  ok(report.issues.includes(code),'required blocker not detected '+code);
 const m=j(root,c.manifest_path),o=m.runtime?.orchestration,na=m.runtime?.narrative_architecture;
 ok(o?.current_cycle===cycle(42)&&o?.status===c.status&&o?.next_role===c.next_role&&o?.next_scene_executable===false,'manifest failed gating');
 ok(m.runtime?.last_confirmed_narrative_event===c.checkpoint.last_event_id,'narrative event changed');
 ok(m.runtime.temporal_transition?.status==='REVIEW_REQUIRED'&&m.runtime.temporal_transition?.effective_narrator_permission===false,'manifest temporal gate');
 for(const [k,v] of Object.entries(c.architecture))ok(eq(na?.blob_refs?.[k],v),'manifest lacks architecture '+k);
 const pointers=[['contract','orchestration_contract'],['entrypoint','start_here'],['cycle_schema','cycle_schema'],['validator','cycle_validator'],['tests','cycle_tests'],['schema_tests','cycle_schema_tests']];
 for(const [name,key] of pointers)ok(o[name]===c.architecture[key].path&&o[name+'_blob_sha']===c.architecture[key].blob_sha,'manifest pointer '+name);
 const git=args=>execFileSync('git',['-C',root,...args],{encoding:'utf8'}).trim();
 ok(git(['rev-parse','HEAD:'+cycle(42)])===hash(file(root,cycle(42))),'cycle not checked into HEAD');
 ok(git(['rev-parse','HEAD:'+c.manifest_path])===c.manifest_ref.blob_sha,'manifest not checked into HEAD');
 ok(git(['merge-base','--is-ancestor',c.source_head_sha,'HEAD'])==='', 'source commit not ancestor');
 return {ok:true,cycle:c.cycle_id,status:c.status,source_threads:report.source_thread_count,salient:report.salient_ids.length,issues:report.issues,protected_state_refs:6,predecessor_links:41,ready_for_narrator:false,no_played_event:true};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){
 try{const i=process.argv.indexOf('--root');console.log(JSON.stringify(validateLatestV16(path.resolve(i<0?process.cwd():process.argv[i+1]))));}
 catch(e){console.error(String(e));process.exitCode=1}
}
