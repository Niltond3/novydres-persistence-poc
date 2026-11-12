// C05 contextual evidence is reused, not regenerated or marked "new blind review".
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {examineFictionalFrame,correlateFrozenBReview} from './revisar-conducao-candidata.mjs';
import {buildCatalog,resolveSubject,readSelected} from './catalogo-assuntos.mjs';
const read=path=>readFileSync(path,'utf8'),json=path=>JSON.parse(read(path));
const head=execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim();
const confPath='novydres/cronicas/CHR-001/configuracao/';
const base='novydres/sistema/arquitetura/fase-b/';
const result=json(base+'resultado-testes.json');
const gate=json(base+'gate-e-readback.json');
const exercises=result.narrative_exercises_2026_11_12;
const review=gate.b05_independent_session_contextual_review_2026_11_12;
const expectCode=(fn,code)=>assert.throws(fn,e=>e.code===code,'expected '+code);
test('IMP-01/02 C05 routes the contract through CONTEXT without a fourth bootstrap',()=>{
 const context=read('novydres/CONTEXT.md');
 const contract='novydres/sistema/narrativa/contrato.md';
 assert.ok(context.includes(contract));
 assert.ok(context.includes('chr001-table-config'));
 const text=read(contract);
 assert.ok(text.includes('Não operacional.'));
 assert.ok(text.includes('E02'));
 assert.ok(text.includes('N-06-RESULT'));
 assert.ok(text.includes('C05'));
});
test('IMP-04/08/15 local CHR-001 configuration has independent owner and is catalogued without changing C41',()=>{
 const c=buildCatalog();
 const meta=c.subjects.find(s=>s.id==='chr001-table-config');
 assert.ok(meta);assert.equal(meta.path,confPath.slice(0,-1));
 assert.equal(meta.visibility,'SYSTEM_AUDIT');
 assert.deepEqual(meta.dependencies,['chr001-state-checkpoint']);
 assert.equal(c.subjects.length,110);
 const pinned=resolveSubject(c,'chr001-table-config',{snapshot_sha:head,role:'AUDITOR'});
 assert.ok(pinned.files.some(f=>f.path===confPath+'configuracao.json'));
 const actual=JSON.parse(readSelected(process.cwd(),c,'chr001-table-config',{snapshot_sha:head,
   role:'AUDITOR',selected_paths:[confPath+'configuracao.json']}).files[0].text);
 assert.equal(actual.not_operational,true);
 assert.equal(actual.no_campaign_events_created,true);
 assert.equal(actual.mechanics.current_sheet_not_certified,true);
 assert.equal(actual.mechanics.local_exceptions,'MUST_RESOLVE_FROM_PINNED_OPERATIONAL_AUTHORITIES');
});
test('IMP-05..11 already frozen B fictional outputs and contextual review reused without blind PASS claim',()=>{
 const r=correlateFrozenBReview(exercises.exercises,exercises.targeted_followup,review);
 assert.equal(r.status,'HISTORICAL_CONTEXTUAL_REVIEW_REUSED');
 assert.equal(r.case_count,8);
 assert.equal(r.blind_review,false);
 assert.equal(r.runtime_certified,false);
 assert.equal(exercises.status,'EXECUTED_FICTIONAL_OUTPUTS_AWAITING_INDEPENDENT_CONTEXT_REVIEW');
 assert.equal(exercises.exercises.find(x=>x.id==='N-06').risk,'DRAMA_PLAYED_WITH_CAUSAL_CONSEQUENCES');
 assert.ok(review.narrative.find(x=>x.id==='N-06').result.startsWith('INITIAL_INSUFFICIENT'));
});
test('contextual review is distinct from syntax checks and cannot be generated from case count',()=>{
 const corrupted={...review,narrative:review.narrative.filter(x=>x.id!=='N-06')};
 expectCode(()=>correlateFrozenBReview(exercises.exercises,exercises.targeted_followup,corrupted),
   'CONTEXTUAL_REVIEW_NOT_FOUND');
 const falsified={...review,narrative:review.narrative.map(x=>x.id==='N-06'?
   {...x,result:'PASS_CONTEXTUAL_TEST_ONLY'}:x)};
 expectCode(()=>correlateFrozenBReview(exercises.exercises,exercises.targeted_followup,falsified),
   'N06_HISTORICAL_FAILURE_ERASED');
});
test('risk functions can be checked on synthetic frames without narrative quota',()=>{
 const cases=[
 {npc:{objective:'keep permit',friendly:true,opposes:true,automatic_compliance_from_courtesy:false}},
 {social:{won:true,concession_delivered:true,automatic_friendship:false}},
 {pending_intention:{exists:true,lost_without_cause:false}},
 {ellipsis:{substantial:false,performed:true}},
 {ellipsis:{substantial:true,performed:false,priorities_known:false}},
 {family:{harm_mandated_for_horror:false,invulnerable:false}},
 {mystery:{material_clue:true,truth_pinned_ref:'TEST_ONLY:locked_truth'}},
 {correction:{material:true,consent_required:true,consent_granted:true}},
 {output_delivered:true,transaction:{confirmed:true}},
 {mechanics:{awarded_xp_without_source:false,rerolled_after_recovery:false}}
 ];
 for(const frame of cases)assert.equal(
  examineFictionalFrame({test_only:true,...frame}).status,'REVIEW_READY_NOT_LITERARY_CERTIFIED');
});
test('negative: player agency, NPC autonomy, numeric mood, social concessions',()=>{
 const bad=[
 ['NOT_AN_ISOLATED_FIXTURE',{test_only:false}],
 ['CAMPAIGN_SOURCE_MIXED',{uses_actual_campaign_event:true}],
 ['PLAYER_AGENCY_OVERRIDE',{narrator_chose_pc_action:true}],
 ['NUMERIC_MOOD_QUOTA_REINTRODUCED',{npc:{disposition_quota_required:true}}],
 ['NPC_AUTONOMY_LOST',{npc:{automatic_compliance_from_courtesy:true}}],
 ['EARNED_CONCESSION_REMOVED',{social:{won:true,concession_delivered:false}}],
 ['SOCIAL_SUCCESS_OVERGENERALIZED',{social:{won:true,concession_delivered:true,automatic_friendship:true}}]
 ];
 for(const [code,frame] of bad)expectCode(()=>examineFictionalFrame({test_only:true,...frame}),code);
});
test('negative: ellipsis, material choice, pending intention, mystery retcon',()=>{
 const bad=[
 ['INTENTION_DROPPED',{pending_intention:{exists:true,lost_without_cause:true}}],
 ['PRIORITIES_BEFORE_LEAP_REQUIRED',{ellipsis:{substantial:true,performed:true,priorities_known:false}}],
 ['MATERIAL_CHOICE_CONSUMED_OFFSCREEN',{ellipsis:{consumes_material_choice:true}}],
 ['MYSTERY_TRUTH_NOT_FIXED',{mystery:{material_clue:true}}],
 ['MYSTERY_RETCON',{mystery:{material_clue:true,truth_pinned_ref:'locked',truth_changed_to_match_clue:true}}]
 ];
 for(const [code,frame] of bad)expectCode(()=>examineFictionalFrame({test_only:true,...frame}),code);
});
test('negative: XP, no reroll, family no mandatory harm, no material retcon, publication-before-delivery',()=>{
 const bad=[
 ['INVENTED_XP',{mechanics:{awarded_xp_without_source:true}}],
 ['REROLL_ON_RECOVERY',{mechanics:{rerolled_after_recovery:true}}],
 ['FAMILY_OUTCOME_MANDATED',{family:{harm_mandated_for_horror:true}}],
 ['FAMILY_OUTCOME_MANDATED',{family:{invulnerable:true}}],
 ['MATERIAL_RETCON_UNAPPROVED',{correction:{material:true,consent_required:true,consent_granted:false}}],
 ['NARRATED_WITHOUT_CONFIRMED_PERSISTENCE',{output_delivered:true,transaction:{confirmed:false}}],
 ['OLD_CADENCE_REINTRODUCED',{legacy_per_scene_manifest_required:true}]
 ];
 for(const [code,frame] of bad)expectCode(()=>examineFictionalFrame({test_only:true,...frame}),code);
});
test('semantic false statement can pass syntax: external contextual review is needed',()=>{
 const fake={test_only:true,npc:{friendly:true,opposes:true,automatic_compliance_from_courtesy:false},
  report:'TEST_ONLY: synthetic false inference, unchecked by script'};
 assert.equal(examineFictionalFrame(fake).status,'REVIEW_READY_NOT_LITERARY_CERTIFIED');
});
