import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {assessTemporalTransition,salientIds,validateTemporalTransition} from './TEMPORAL_TRANSITION_VALIDATOR_V1.mjs';
const root=new URL('../../chronicles/CHR-001/preparations/',import.meta.url);
const load=p=>JSON.parse(readFileSync(new URL(p,root),'utf8'));
const packet=load('M3.02_TEMPORAL_TRANSITION_V1_PLAYER_SAFE.json');
const live=load('../LIVE_v038.json');
const threads=load('../knowledge/OPEN_THREADS_V23.json');
const copy=()=>structuredClone(packet);
const audit=p=>assessTemporalTransition(p,live,threads);
test('source-grounded inventory includes all 44 open threads, especially the unopened Y.B. box',()=>{
 const r=audit(copy());assert.equal(r.source_thread_count,44);assert.equal(r.disposition_count,44);
 assert(r.salient_ids.includes('m301-c04-unopened-box'));
});
test('intentionally blocked M3.02 transition is not falsely READY',()=>{
 const r=audit(copy());assert.equal(r.ready,false);
 for(const code of ['INTERVAL_UNBOUNDED','MATERIAL_CUSTODY_UNRESOLVED','PLAYER_CHOICE_PENDING','OPENING_INCOMPLETE','GEOMETRY_UNSPECIFIED:obstacle_type'])assert(r.issues.includes(code));
});
test('remove unopened box -> gate rejects silent omission',()=>{
 const x=copy();x.thread_dispositions=x.thread_dispositions.filter(t=>t.id!=='m301-c04-unopened-box');
 assert(audit(x).issues.includes('MISSING_THREAD:m301-c04-unopened-box'));
});
test('remove family/business/recent salient entry -> gate rejects omission',()=>{
 const x=copy();const id=x.salient_bridges.find(t=>t.id==='m204-mary-bart-trust')?.id;
 assert(id);x.salient_bridges=x.salient_bridges.filter(t=>t.id!==id);
 assert(audit(x).issues.includes('MISSING_SALIENT:'+id));
});
test('never treat Mary as already told about box without evidence',()=>{
 const x=copy();x.contexts.family_knowledge.contact_claimed=true;
 assert(audit(x).issues.includes('UNSOURCED_FAMILY_CONTACT'));
});
test('fabricated business gain fails regardless of unspecified duration',()=>{
 const x=copy();x.contexts.workshop.revenue_delta_claimed=true;
 assert(audit(x).issues.includes('UNSOURCED_REVENUE_DELTA'));
});
test('bounded time and geometry alone cannot bypass undecided player choice',()=>{
 const x=copy();x.interval.min_nights=1;x.interval.max_nights=2;
 for(const k of Object.keys(x.scene_affordances))x.scene_affordances[k]='Source-grounded playable description';
 x.opening={interval_and_life:'Narrative bridge with sourced established routine.',pending_carryovers:'Y.B. box pending, relationships still bounded by knowledge.',physical_stakes:'Main and lateral access consequences concretely stated.',ready:true};
 const e=audit(x).issues;assert(e.includes('PLAYER_CHOICE_PENDING'));assert(e.includes('MATERIAL_CUSTODY_UNRESOLVED'));
});
test('complete hypothetical fixture passes, never writes a story event',()=>{
 const x=copy();x.status='READY';x.interval.min_nights=1;x.interval.max_nights=2;
 x.contexts.material_custody.current_frame_status='CARRIED_WITH_SOURCE';x.contexts.material_custody.pc_choice_status='NOT_REQUIRED';
 x.prelude.required_player_decisions=[];x.prelude.all_essential_decisions_resolved=true;
 for(const k of Object.keys(x.scene_affordances))x.scene_affordances[k]='Causally grounded physical description for player action';
 x.opening={interval_and_life:'One or two nights; normal workshop operation continued.',pending_carryovers:'Y.B. box is preserved in custody with no examination claimed.',physical_stakes:'Both vehicle and pedestrian paths described with safe alternatives.',ready:true};
 assert.deepEqual(audit(x).issues,[]);assert.equal(x.no_story_delta,true);
});
test('contiguous scenes require no ellipsis or arbitrary prelude',()=>{
 const x=copy();x.mode='CONTINUITY';x.interval.min_nights=0;x.interval.max_nights=0;
 assert(!audit(x).issues.includes('FALSE_ELAPSE_IN_CONTINUITY'));
});
test('validate source pins and explicit REVIEW_REQUIRED in candidate checkout',()=>{
 const r=validateTemporalTransition(process.cwd(),'novydres/chronicles/CHR-001/preparations/M3.02_TEMPORAL_TRANSITION_V1_PLAYER_SAFE.json');
 assert.equal(r.package_status,'REVIEW_REQUIRED');assert.equal(r.ready,false);
});
