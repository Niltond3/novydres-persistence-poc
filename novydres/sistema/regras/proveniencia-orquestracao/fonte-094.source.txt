import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import {validateLatestV19} from './ORCHESTRATION_VALIDATOR_V19.mjs';
const M='novydres/MANIFEST_V62.json';
const AUDIT='novydres/chronicles/CHR-001/audits/M3.02_POST_G28_CI_SCOPE_AUDIT_V1_PLAYER_SAFE.json';
const old='novydres/MANIFEST_V61.json';
function insist(v,msg){if(!v)throw Error('V20_SCOPE_BLOCK:'+msg)}
function read(root,p){return fs.readFileSync(path.join(root,p))}
function j(root,p){return JSON.parse(read(root,p).toString('utf8'))}
function sha(buf){return crypto.createHash('sha1').update(Buffer.from('blob '+buf.length+'\0')).update(buf).digest('hex')}
function pin(root,r){insist(r&&typeof r.path==='string'&&/^[a-f0-9]{40}$/.test(r.blob_sha),'malformed ref');insist(sha(read(root,r.path))===r.blob_sha,'pin mismatch '+r.path)}
export function validateScope(a,m){
insist(a.document_id==='CHR001_M302_POST_G28_CI_SCOPE_AUDIT_V1_PLAYER_SAFE','audit identity');
insist(a.historical_workflow.result==='FAIL'&&a.historical_workflow.evidence==='CHR001_V17_BLOCK:unexpected cycle count','must disclose historical false failure');
insist(a.historical_workflow.historical_v17_immutable&&a.historical_workflow.temporal_packet_v2_tests==='PASS_WITHIN_SAME_JOB','historical scope and V2 evidence');
insist(a.current_validators.v19_result==='PASS'&&a.current_validators.v18_result==='PASS'&&a.current_validators.v15_result==='PASS','observed candidate CI');
insist(a.current_validators.c44_predecessors==='43/43'&&a.current_validators.c44_exact_pins==='75/75'&&a.current_validators.g28_sources==='6/6'&&a.current_validators.threads_open===44,'G28 check evidence');
insist(a.promotion_status==='BLOCKED_UNTIL_FINAL_SHA_CI_AND_CAUSAL_GATES'&&a.c02_status==='NOT_STARTED'&&a.master_modified===false,'not promoted');
insist(a.no_canon_edit&&a.no_story_event&&a.no_xp_fv_change&&a.no_narrator_permission,'no narrative delta');
insist(m.status==='PROSPECTIVE_CANDIDATE_NOT_ACTIVE_PENDING_VALIDATION','manifest active forbidden');
insist(m.supersedes===old,'manifest supersession');
insist(m.runtime.orchestration.current_cycle==='novydres/chronicles/CHR-001/orchestration/CYCLE_V0044.json','C44 still current');
insist(m.runtime.orchestration.operational_gates.narrator_permission===false,'narrator forbidden');
insist(m.runtime.orchestration.next_scene_status==='NOT_STARTED','C02 not started');
insist(m.candidate_only.new_cycle_published===false&&m.candidate_only.player_safe_handoff_ready===false,'cannot publish handoff');
return true
}
export function validateLatestV20(root=process.cwd()){
const base=validateLatestV19(root),audit=j(root,AUDIT),manifest=j(root,M);
validateScope(audit,manifest);
insist(manifest.previous_manifest_sha===sha(read(root,old)),'previous manifest pin');
for(const item of Object.values(manifest.runtime.orchestration.post_g28_candidate_refs))pin(root,item);
for(const item of Object.values(manifest.runtime.current_m3_02_candidate_preparation))pin(root,item);
insist(manifest.runtime.orchestration.post_g28_candidate_refs.scope_audit.path===AUDIT,'scope audit ref');
return {...base,scope_audit:true,ci_exact_final_sha:'CHECK_BY_ACTIONS',handoff:false}
}
if(process.argv[1]&&path.resolve(process.argv[1])===path.resolve(new URL(import.meta.url).pathname))process.stdout.write(JSON.stringify(validateLatestV20())+'\n');
