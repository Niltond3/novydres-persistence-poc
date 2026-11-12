import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {assessTemporalTransition, validateTemporalTransition} from './TEMPORAL_TRANSITION_VALIDATOR_V1.mjs';
const root=new URL('../../chronicles/CHR-001/',import.meta.url);
const read=p=>JSON.parse(readFileSync(new URL(p,root),'utf8'));
const packet=read('preparations/M3.02_TEMPORAL_TRANSITION_V2_PLAYER_SAFE.json');
const live=read('LIVE_v038.json'),threads=read('knowledge/OPEN_THREADS_V23.json');
const audit=p=>assessTemporalTransition(p,live,threads),copy=()=>structuredClone(packet);
test('all 44 source threads and all salient IDs are reconciled with exact pins',()=>{
 const r=validateTemporalTransition(process.cwd(),'novydres/chronicles/CHR-001/preparations/M3.02_TEMPORAL_TRANSITION_V2_PLAYER_SAFE.json');
 assert.equal(r.ready,true);assert.equal(r.package_status,'READY');
 assert.equal(r.source_thread_count,44);assert.equal(r.disposition_count,44);
 assert(r.salient_ids.includes('m301-c04-unopened-box'));
});
test('bounded interval and no forced action or FV spend',()=>{
 assert.equal(packet.interval.min_nights,1);assert.equal(packet.interval.max_nights,1);
 assert.equal(packet.prelude.distinct_test_count,0);
 assert.deepEqual(packet.prelude.required_player_decisions,[]);
 assert.equal(packet.no_story_delta,true);
});
test('box stays unopened, last location is historical and not teleported',()=>{
 const x=packet.contexts.material_custody;
 assert.equal(x.current_frame_status,'CARRIED_WITH_SOURCE');
 assert.equal(x.pc_choice_status,'NOT_REQUIRED');
 assert.match(x.last_confirmed_location,/NÃO localização confirmada/);
 assert.match(packet.opening.pending_carryovers,/não estão comprovados/);
});
test('Mary was not told by invented offscreen conversation',()=>{
 assert.equal(packet.contexts.family_knowledge.contact_claimed,false);
 assert.equal(packet.contexts.family_knowledge.mary_box_knowledge,'UNKNOWN');
});
test('workshop has shared access but no financial reward',()=>{
 assert.equal(packet.contexts.workshop.established_open,true);
 assert.equal(packet.contexts.workshop.shared_access,true);
 assert.equal(packet.contexts.workshop.revenue_delta_claimed,false);
});
test('obstacle has material, principal, lateral and reachable choices',()=>{
 for(const k of ['obstacle_type','position','main_entrance_effect','lateral_access_effect','movement_options','ownership_status'])
  assert(packet.scene_affordances[k].length>35);
 assert.match(packet.scene_affordances.main_entrance_effect,/acessíveis/);
 assert.match(packet.scene_affordances.lateral_access_effect,/pedestres/);
});
test('guard rejects missing historical box thread',()=>{
 const x=copy();x.thread_dispositions=x.thread_dispositions.filter(t=>t.id!=='m301-c04-unopened-box');
 assert(audit(x).issues.includes('MISSING_THREAD:m301-c04-unopened-box'));
});
test('guard rejects time, fabricated family knowledge, unsupported revenues',()=>{
 const x=copy();x.interval.max_nights=null;
 x.contexts.family_knowledge.contact_claimed=true;x.contexts.workshop.revenue_delta_claimed=true;
 const q=audit(x).issues;
 for(const e of ['INTERVAL_UNBOUNDED','UNSOURCED_FAMILY_CONTACT','UNSOURCED_REVENUE_DELTA'])assert(q.includes(e));
});
test('guard refuses premature removal of physical options',()=>{
 const x=copy();x.scene_affordances.obstacle_type='UNSPECIFIED';
 assert(audit(x).issues.includes('GEOMETRY_UNSPECIFIED:obstacle_type'));
});
test('guard preserves observed chat opening without creating G28',()=>{
 const x=copy();x.chat_opening_status='NOT_PRESENT';
 assert(audit(x).issues.includes('STORY_DELTA_OR_CHAT_ERASURE'));
 assert.equal(packet.chat_opening_status,'PLAYER_VISIBLE_OPENING_PAUSED_NOT_G28_PERSISTED');
});
test('no false acceptance of unresolved indispensable PC decision',()=>{
 const x=copy();x.prelude.required_player_decisions=['invented indispensable action'];
 x.prelude.all_essential_decisions_resolved=false;
 assert(audit(x).issues.includes('PLAYER_CHOICE_PENDING'));
});
