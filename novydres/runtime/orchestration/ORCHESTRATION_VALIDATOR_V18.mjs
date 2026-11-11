#!/usr/bin/env node
// V18: G28 closure to Dramaturgo; no C02 narration authorized.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {validateC43} from './ORCHESTRATION_VALIDATOR_V17.mjs';
const ok=(v,m)=>{if(!v)throw Error('CHR001_V18_BLOCK:'+m)};
const b=(root,p)=>{ok(p?.startsWith('novydres/')&&!p.includes('..'),'unsafe path');return fs.readFileSync(path.resolve(root,p))};
const j=(root,p)=>JSON.parse(b(root,p).toString('utf8'));
const hash=x=>crypto.createHash('sha1').update(Buffer.from('blob '+x.length+'\0')).update(x).digest('hex');
const pin=(root,x,m)=>{ok(x?.path&&/^[a-f0-9]{40}$/.test(x.blob_sha),m+' invalid');ok(hash(b(root,x.path))===x.blob_sha,m+' mismatched SHA '+x.path)};
const cycle=n=>'novydres/chronicles/CHR-001/orchestration/CYCLE_V'+String(n).padStart(4,'0')+'.json';
export function validateC44(c,p){
 ok(c.schema_id==='NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V18'&&c.cycle_id==='CHR001-CYCLE-0044'&&c.sequence===44,'cycle id');
 ok(p.cycle_id==='CHR001-CYCLE-0043'&&p.sequence===43,'predecessor id');
 ok(c.previous_cycle.path===cycle(43)&&c.previous_cycle.blob_sha==='cb7c44d5952a96e59322890a1c15185f50aa2ea3','predecessor');
 ok(c.source_head_sha==='27652bc35755086ebbbdfd9749cb521e3e76c517'&&c.provocation_id==='M3.02','source master');
 ok(c.manifest_path==='novydres/MANIFEST_V59.json'&&c.manifest_ref.path===c.manifest_path,'manifest');
 ok(c.transition==='SCENE_COMMITTED'&&c.status==='READY_FOR_DRAMATURGO'&&c.next_role==='DRAMATURGO','role transition');
 ok(c.checkpoint.last_event_id==='CHR001-M302-C01-05-20261111-001'&&c.checkpoint.last_closed_scene==='C01'&&c.checkpoint.next_scene==='C02'&&c.checkpoint.next_scene_status==='NOT_STARTED'&&!c.checkpoint.pending_persistence&&c.checkpoint.mortal&&!c.checkpoint.embrace_occurred,'checkpoint');
 ok(c.scene_commit?.g28_persisted===true&&c.scene_commit.event_id===c.checkpoint.last_event_id&&c.scene_commit.event_count===5&&c.scene_commit.no_dice&&c.scene_commit.no_xp_fv_delta&&c.scene_commit.player_disengaged,'g28');
 for(const k of ['story_preparation_ready','mechanical_scene_ready','scene_ready','narrator_permission'])ok(c.operational_gates[k]===false,'next scene gate '+k);
 ok(c.operational_gates.architecture_active===true&&c.operational_gates.d07_active===true,'architecture');
 ok(c.plan.validity==='STALE'&&c.review.decision==='SCENE_COMMITTED'&&c.pending_player_decision===null,'review');
 ok(c.architecture.player_immersion_comment?.path==='novydres/chronicles/CHR-001/feedback/PLAYER_COMMENT_M302_C01_IMMERSION_V1_PLAYER_SAFE.md'&&c.architecture.player_immersion_comment.blob_sha==='a4cc9e5886e71602a08239577cd75b39f32e7f65','player comment pin');
 ok(c.architecture.narrative_immersion_gate?.path==='novydres/runtime/scene-execution/NARRATIVE_IMMERSION_GATE_V1.md'&&c.architecture.narrative_immersion_gate.blob_sha==='cbea713c1e11bbcb01e6c3b3e1901684acb0b7a9','immersion gate pin');
 ok(c.architecture.reconciliation_only_handoff?.path==='novydres/chronicles/CHR-001/handoffs/M302_C01_RECONCILIATION_ONLY_V1_PLAYER_SAFE.md'&&c.architecture.reconciliation_only_handoff.blob_sha==='d7b3f9cef7e21e11d3b8f76662e3cb7072712e25','restricted handoff pin');
 return {ok:true};
}
export function validateLatestV18(root){
 const names=fs.readdirSync(path.resolve(root,'novydres/chronicles/CHR-001/orchestration')).map(f=>/^CYCLE_V(\d{4})\.json$/.exec(f)).filter(Boolean).map(x=>Number(x[1]));
 ok(names.length===44&&Math.max(...names)===44,'cycle count');
 const c=j(root,cycle(44)),p=j(root,cycle(43)),p42=j(root,cycle(42));
 validateC43(p,p42);validateC44(c,p);
 for(let n=44;n>=2;n--){const x=j(root,cycle(n));ok(x.previous_cycle.path===cycle(n-1),'chain route '+n);pin(root,x.previous_cycle,'chain '+n)}
 pin(root,c.manifest_ref,'manifest');for(const[k,v]of Object.entries(c.refs))pin(root,v,'source '+k);
 for(const[k,v]of Object.entries(c.architecture))pin(root,v,'architecture '+k);
 for(const[k,v]of Object.entries(c.activation))pin(root,v,'activation '+k);
 for(const[k,v]of Object.entries(c.operational_gates.mechanical_sources))pin(root,v,'mechanical '+k);
 pin(root,c.operational_gates.mechanical_matrix_ref,'matrix');pin(root,c.plan.dossier,'dossier');pin(root,c.plan.sidecar,'sidecar');pin(root,c.scene_commit.episode,'episode');
 const m=j(root,c.manifest_path),o=m.runtime.orchestration,l=j(root,c.refs.live.path),h=j(root,c.refs.history_index.path),kn=j(root,c.refs.knowledge.path),t=j(root,c.refs.threads.path);
 ok([m.runtime.last_confirmed_narrative_event,l.last_confirmed_event_id,h.last_event_id,kn.last_event_id,t.last_event_id].every(x=>x===c.checkpoint.last_event_id),'last event');
 ok(l.scene.status==='CLOSED'&&l.scene.last_event_id===c.checkpoint.last_event_id&&l.event_buffer_status==='M302_C01_CLOSED_G28','scene close');
 ok(t.threads.length===44,'threads missing');
 ok(l.character.resources.xp_total===675&&l.character.resources.xp_spent===270&&l.character.resources.xp_credit_available===0&&l.character.resources.willpower_available===4,'resources');
 ok(o.current_cycle===cycle(44)&&o.status===c.status&&o.next_role==='DRAMATURGO'&&o.next_scene_executable===false&&o.next_scene==='C02','manifest status');
 ok(m.runtime.temporal_transition.chat_opening_g28_persisted===true&&m.runtime.temporal_transition.effective_narrator_permission===false,'temporal status');
 const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 for(const[k,v]of Object.entries(c.architecture))ok(eq(m.runtime.narrative_architecture.blob_refs[k],v),'manifest arch '+k);
 for(const[field,key]of [['contract','orchestration_contract'],['entrypoint','start_here'],['cycle_schema','cycle_schema'],['validator','cycle_validator'],['tests','cycle_tests'],['schema_tests','cycle_schema_tests']])
 ok(o[field]===c.architecture[key].path&&o[field+'_blob_sha']===c.architecture[key].blob_sha,'manifest pointer '+field);
 const git=(args)=>execFileSync('git',['-C',root,...args],{encoding:'utf8'}).trim();
 ok(git(['rev-parse','HEAD:'+cycle(44)])===hash(b(root,cycle(44))),'cycle HEAD');
 ok(git(['rev-parse','HEAD:'+c.manifest_path])===c.manifest_ref.blob_sha,'manifest HEAD');
 execFileSync('git',['-C',root,'merge-base','--is-ancestor',c.source_head_sha,'HEAD']);
 return {ok:true,cycle:c.cycle_id,status:c.status,previous_links:43,source_refs:6,threads:44,g28:true,next_scene_not_started:true};
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname)){
try{console.log(JSON.stringify(validateLatestV18(process.cwd())))}catch(e){console.error(String(e));process.exitCode=1}
}
