import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {validateScope,validateLatestV20} from './ORCHESTRATION_VALIDATOR_V20.mjs';
const aud=JSON.parse(fs.readFileSync('novydres/chronicles/CHR-001/audits/M3.02_POST_G28_CI_SCOPE_AUDIT_V1_PLAYER_SAFE.json','utf8'));
const m=JSON.parse(fs.readFileSync('novydres/MANIFEST_V62.json','utf8'));
test('V20 checks final scope, G28 75 pins, 43 predecessors, 44 threads',()=>{const v=validateLatestV20();assert.equal(v.ok,true);assert.equal(v.c44_pins,75);assert.equal(v.predecessors,43);assert.equal(v.threads,44);assert.equal(v.handoff,false)});
function reject(name,mut){test('reject '+name,()=>{const a=structuredClone(aud),b=structuredClone(m);mut(a,b);assert.throws(()=>validateScope(a,b))})}
reject('pretending V17 passed',(a)=>a.historical_workflow.result='PASS');
reject('hiding V17 failure reason',(a)=>a.historical_workflow.evidence='NONE');
reject('claiming V17 is current',(a)=>a.historical_workflow.historical_v17_immutable=false);
reject('false predecessor count',(a)=>a.current_validators.c44_predecessors='42/42');
reject('missing G28 pin',(a)=>a.current_validators.c44_exact_pins='74/75');
reject('premature promotion',(a)=>a.promotion_status='PROMOTED');
reject('C02 started',(a)=>a.c02_status='STARTED');
reject('narrator enabled in manifest',(a,b)=>b.runtime.orchestration.operational_gates.narrator_permission=true);
reject('new active manifest',(a,b)=>b.status='GITHUB_ACTIVE_PRIMARY_FULL_MIGRATION_PENDING');
reject('new cycle claimed',(a,b)=>b.candidate_only.new_cycle_published=true);
reject('hiding frozen alteration',(a)=>a.no_canon_edit=false);
