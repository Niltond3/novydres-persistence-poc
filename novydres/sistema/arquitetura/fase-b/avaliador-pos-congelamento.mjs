// ADR-001 B03 — post-freeze deterministic scorer. NOT a semantic or editorial reviewer.
// Read answer and gabarito only after answer commits are frozen by SHA in GitHub.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read = path => JSON.parse(readFileSync(new URL(path,import.meta.url),'utf8'));
const fixtures=read('./fixtures-consultas.json').questions;
const audit=read('./resultado-testes.json');
const first=audit.b03_new_web_round_2026_11_12;
assert.equal(first.status,'RAW_FROZEN_UNSCORED','raw must be frozen before scoring');
assert.equal(first.cases.length,6);
assert.equal(first.targeted_retest.status,'FROZEN_BEFORE_REEVALUATION');
const candidates={
  story:read('../../../cronicas/CHR-001/historias/m301-c01/historia.json'),
  state:read('../../../cronicas/CHR-001/estado/atual.json'),
  npc:read('../../../personagens/npc-samir-haddad/perfil.json'),
  local:read('../../../cronicas/CHR-001/elenco/npc-samir-haddad/conhecimento.json')
};
const by=new Map(fixtures.map(x=>[x.id,x]));
const retest=new Map(first.targeted_retest.cases.map(x=>[x.id,x]));
const status=[];
for(const x of first.cases) {
  const q=by.get(x.id);
  assert.ok(q?.request,'original request must exist');
  assert.equal(x.source.path,q.evidence_source_path,x.id+' source path');
  assert.equal(x.source.sha,q.evidence_source_sha,x.id+' source blob');
  assert.equal(x.source_commit,q.snapshot.source_commit,x.id+' pinned snapshot');
  assert.ok(x.locator?.length>0 && x.read_operation?.length>0);
  let complete=false;
  if(x.id==='B-Q01') complete=/UNKNOWN/.test(x.answer);
  if(x.id==='B-Q11') complete=typeof x.answer==='object' &&
    x.answer.legacy_actor_id===candidates.npc.historical_actor_id &&
    x.answer.candidate_global_subject_id===candidates.npc.subject_id;
  if(x.id==='B-Q21') complete=candidates.story.event_text_markers.length===8 &&
    /8 entradas/.test(x.answer) && q.expected_from_source===8;
  if(x.id==='B-Q26') complete=typeof x.answer==='object' &&
    x.answer.last_closed_scene===candidates.state.checkpoint.last_closed_scene &&
    x.answer.next_scene_status===candidates.state.checkpoint.next_scene_status;
  if(x.id==='B-Q29') complete=['xp_total','xp_spent','xp_remaining','xp_credit_available'].every(k=>
    x.answer[k]===candidates.state.resources[k]) &&
    JSON.stringify(Object.values(x.answer))===JSON.stringify(q.expected_from_source);
  if(x.id==='B-Q30') complete=typeof x.answer==='object' &&
    ['willpower_provisional_max','willpower_superficial_damage','willpower_aggravated_damage','willpower_available'].every(k=>
      x.answer[k]===candidates.state.resources[k]);
  status.push({id:x.id,initial:complete?'PASS_SCOPED':'INCOMPLETE_OR_NOT_VERIFIED',effective:complete?'PASS_SCOPED':'PENDING'});
}
for(const x of status.filter(x=>x.effective==='PENDING')) {
  const ret=retest.get(x.id)?.answer;
  assert.ok(ret,'targeted retest required for '+x.id);
  if(x.id==='B-Q11') assert.deepEqual(
    [ret.legacy_actor_id,ret.candidate_global_subject_id,ret.candidate_local_subject_id],
    [candidates.npc.historical_actor_id,candidates.npc.subject_id,candidates.local.subject_id]);
  else if(x.id==='B-Q26') assert.deepEqual(
    [ret.last_closed_scene,ret.next_scene,ret.next_scene_status],
    [candidates.state.checkpoint.last_closed_scene,candidates.state.checkpoint.next_scene,candidates.state.checkpoint.next_scene_status]);
  else if(x.id==='B-Q30') {
    for(const field of ['willpower_provisional_max','willpower_superficial_damage','willpower_aggravated_damage','willpower_available'])
      assert.equal(ret[field],candidates.state.resources[field]);
  } else throw new Error('unexpected retest '+x.id);
  x.effective='PASS_SCOPED_POST_RETEST';
}
assert.equal(status.filter(x=>x.effective.startsWith('PASS')).length,6);
assert.equal(status.filter(x=>x.initial!=='PASS_SCOPED').length,3);
const scenes=audit.narrative_exercises_2026_11_12;
assert.equal(scenes.exercises.length,8);
assert.ok(scenes.exercises.every(e=>e.classification==='TEST_ONLY_NOT_CAMPAIGN'));
assert.equal(scenes.targeted_followup.id,'N-06-RESULT');
console.log(JSON.stringify({status:'PASS_DETERMINISTIC_POST_FREEZE_ONLY',
  comparison:'RAW_FIRST_ROUND_SEPARATE_FROM_TARGETED_RETEST',
  first_round_complete:3,first_round_incomplete:status.filter(x=>x.initial!=='PASS_SCOPED').map(x=>x.id),
  targeted_retests_verified:3,effective_verified:6,critical_resource_cases:['B-Q29','B-Q30'],
  candidate_bytes_read:'ACTUAL_CHECKOUT_JSON',source_pins_compared_to_fixtures:true,
  historical_web_retroapproved:false,independent_semantic_review:'NOT_PERFORMED',
  narrative_fiction_scenarios:scenes.exercises.length,
  narrative_contextual_editorial_review:'NOT_PERFORMED_BY_THIS_SCORER'}));
