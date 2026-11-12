import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  EXPECTED_RUNTIME_PATHS,
  EXPECTED_D07_ACTIVATION_PATH,
  EXPECTED_AUTHORIZATION_PATH,
  EXPECTED_BOOTSTRAP_PATHS,
  containsHiddenPhrase,
  validateActivationTransition,
  validateClosureRecommendationTransition,
  validateDramaturgoTransition,
  validateExpectedArtifactPins,
  validateD07RuntimeActivation,
  validateNarratorPrompt,
  validateOpenQuietHandoff,
  validatePreparationCheckpoint,
  validatePreparationSourceCheckpoint,
  validateBlockedTransition,
  validateSceneCommittedTransition,
  validateLatestV10,
  validateV9ToV10ClosureMigration
} from './ORCHESTRATION_VALIDATOR_V10.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const hash = digit => digit.repeat(40);
const cycleId = n => `CHR001-CYCLE-${String(n).padStart(4, '0')}`;
const guards = { no_story_delta_in_prep: true, no_xp_fv_delta_in_prep: true, g28_scene_only: true, frozen_unchanged: true, no_public_spoilers: true };
const checkpoint = () => ({ last_event_id: 'CHR001-M301-C05-22-20261109-001', last_closed_scene: 'C05', next_scene: 'C06', next_scene_status: 'NOT_STARTED', pending_persistence: false, mortal: true, embrace_occurred: false });
const refs = () => Object.fromEntries(['live', 'history_index', 'episode', 'character', 'knowledge', 'threads'].map((key, i) => [key, { path: `source/${key}.json`, blob_sha: hash(String(i + 1)) }]));
const architecture = () => {
  const out = Object.fromEntries(Object.entries(EXPECTED_RUNTIME_PATHS).map(([key, p], i) => [key, { path: p, blob_sha: hash(String((i % 9) + 1)) }]));
  for (const [i, key] of ['d04_plot_admissions','d05_approval_queue','d06','d07','d08','d09','d10_schema_registry','d10_role_adapters','d10_validator','d10_results','d11_cases','d11_results','d11_review','d12_candidate','d12_mechanical_source_refs','d12_validator','d12_results','promotion_inventory','agent_entry','context_gateway','player_authorization'].entries()) out[key] = { path: `architecture/${key}`, blob_sha: hash(String((i % 9) + 1)) };
  out.agent_entry.path = EXPECTED_BOOTSTRAP_PATHS.agent_entry;
  out.context_gateway.path = EXPECTED_BOOTSTRAP_PATHS.context_gateway;
  return out;
};
const mechanicalSources = () => Object.fromEntries(['rules_provenance','target_sheet','adjudication_gate','motor_manual','xp_policy','xp_audit','act_resolution_schema','xp_envelope','settlement_record'].map((key, i) => [key, { path: `rules/${key}.json`, blob_sha: hash(String((i % 9) + 1)) }]));

function activationPair() {
  const cp = checkpoint();
  const prev = { sequence: 34, cycle_id: cycleId(34), provocation_id: 'M3.01', status: 'READY_FOR_DRAMATURGO', transition: 'SOURCE_RECONCILED', checkpoint: cp };
  const c = {
    sequence: 35, cycle_id: cycleId(35), provocation_id: 'M3.01', status: 'READY_FOR_DRAMATURGO', next_role: 'DRAMATURGO', transition: 'OPERATIONAL_ACTIVATED', checkpoint: structuredClone(cp),
    pending_player_decision: null, plan: { validity: 'STALE' }, review: { decision: 'NOT_REVIEWED', against_last_event_id: cp.last_event_id },
    operational_gates: { architecture_active: true, d07_active: true, story_preparation_ready: false, mechanical_scene_ready: false, scene_ready: false, narrator_permission: false }, guards: structuredClone(guards)
  };
  return { c, prev };
}

function reviewPair() {
  const cp = checkpoint(), cycleRefs = refs(), arch = architecture(), ms = mechanicalSources();
  const prev = { sequence: 35, cycle_id: cycleId(35), provocation_id: 'M3.01', transition: 'OPERATIONAL_ACTIVATED', status: 'READY_FOR_DRAMATURGO', next_role: 'DRAMATURGO', checkpoint: cp, refs: cycleRefs, architecture: arch,
    operational_gates: { architecture_active: true, d07_active: true, story_preparation_ready: false, mechanical_scene_ready: false, scene_ready: false, narrator_permission: false, mechanical_matrix_ref: { path: 'rules/matrix.md', blob_sha: hash('a') }, mechanical_sources: ms } };
  const c = structuredClone(prev);
  Object.assign(c, { sequence: 36, cycle_id: cycleId(36), transition: 'PLAN_REVISED', status: 'READY_FOR_NARRATOR', next_role: 'NARRADOR', previous_cycle: { path: 'cycle35.json', blob_sha: hash('b') },
    plan: { validity: 'REVISED', reviewed_against_event_id: cp.last_event_id }, review: { decision: 'REVISED', against_last_event_id: cp.last_event_id }, pending_player_decision: null, guards: structuredClone(guards) });
  Object.assign(c.operational_gates, { story_preparation_ready: true, mechanical_scene_ready: true, scene_ready: true, narrator_permission: true });
  return { c, prev };
}

function openQuietHandoff() {
  return {
    provocation_status: 'OPEN', status: 'HANDOFF_PENDING_PLAYER_DECISION', scene_ready: false, SCENE_READY: false, NARRATOR_PERMISSION: false,
    source_checkpoint: { provocation_status: 'OPEN' },
    closure_routing: { recommendation: 'PROVOCATION_CLOSURE_PENDING', effect: 'ROUTING_ONLY', player_decision_required: true, provocation_closed: false, event_created: false },
    handoff: { player_decision_pending: true, cause: null, actors: [], entry_condition: null, stakes: null, prepared_scenes: [], acts: [], next_decision: {
      cause_status: 'NO_C06_CAUSE_ADMITTED_OR_AVAILABLE', default_if_no_action: 'KEEP_OPEN_QUIET', decision_recorded: false,
      choices: [
        { choice_id: 'KEEP_OPEN_QUIET' },
        { choice_id: 'CONTINUE_AFTER_ADMISSION' },
        { choice_id: 'REQUEST_ALTERNATE_CLOSURE' }
      ]
    } },
    governance: { no_story_event_created: true, no_time_advanced: true, no_npc_knowledge_delta: true, no_player_spoilers: true }
  };
}

function preparationSourceFixture() {
  const cycleRefs = refs(), cp0 = checkpoint();
  const sourceCycle = { schema_id: 'NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V9', sequence: 35, cycle_id: cycleId(35), provocation_id: 'M3.01', transition: 'OPERATIONAL_ACTIVATED', status: 'READY_FOR_DRAMATURGO', next_role: 'DRAMATURGO', source_head_sha: hash('c'), manifest_path: 'novydres/MANIFEST_V49.json', manifest_ref: { path: 'novydres/MANIFEST_V49.json', blob_sha: hash('d') }, refs: cycleRefs, checkpoint: cp0 };
  const cyclePath = 'novydres/chronicles/CHR-001/orchestration/CYCLE_V0035.json';
  const sourceManifest = { runtime: {
    orchestration: { current_cycle: cyclePath, status: 'READY_FOR_DRAMATURGO', next_role: 'DRAMATURGO', next_scene: 'C06', next_scene_status: 'NOT_STARTED' },
    last_confirmed_narrative_event: cp0.last_event_id, live_current: cycleRefs.live.path, history_index_current: cycleRefs.history_index.path, episode_current: cycleRefs.episode.path,
    character_state_current: cycleRefs.character.path, knowledge_current: cycleRefs.knowledge.path, open_threads_current: cycleRefs.threads.path
  } };
  const cp = { base_commit_sha: sourceCycle.source_head_sha, cycle_path: cyclePath, cycle_blob_sha: hash('e'), manifest_path: sourceCycle.manifest_path, manifest_blob_sha: sourceCycle.manifest_ref.blob_sha,
    live_path: cycleRefs.live.path, live_blob_sha: cycleRefs.live.blob_sha, history_index_path: cycleRefs.history_index.path, history_index_blob_sha: cycleRefs.history_index.blob_sha,
    episode_path: cycleRefs.episode.path, episode_blob_sha: cycleRefs.episode.blob_sha, state_path: cycleRefs.character.path, state_blob_sha: cycleRefs.character.blob_sha,
    knowledge_path: cycleRefs.knowledge.path, knowledge_blob_sha: cycleRefs.knowledge.blob_sha, open_threads_path: cycleRefs.threads.path, open_threads_blob_sha: cycleRefs.threads.blob_sha,
    last_confirmed_event_id: cp0.last_event_id, last_closed_scene: cp0.last_closed_scene, next_scene: cp0.next_scene, next_scene_status: cp0.next_scene_status,
    protagonist_mortal: cp0.mortal, embrace_occurred: cp0.embrace_occurred };
  const c = { sequence: 36, provocation_id: 'M3.01', previous_cycle: { path: cyclePath, blob_sha: hash('e') }, checkpoint: cp0 };
  return { cp, sourceCycle, sourceManifest, c, preparation: { source_refs: Object.values(cycleRefs) } };
}

test('V10 activation transition preserves C05-22, M3.01 identity, and false scene gates', () => {
  const { c, prev } = activationPair();
  assert.equal(validateActivationTransition(c, prev).ok, true);
  const wrongProvocation = activationPair(); wrongProvocation.c.provocation_id = 'M3.02';
  assert.throws(() => validateActivationTransition(wrongProvocation.c, wrongProvocation.prev), /activation sequence\/provocation mismatch/);
  const falseGate = activationPair(); falseGate.c.operational_gates.scene_ready = true;
  assert.throws(() => validateActivationTransition(falseGate.c, falseGate.prev), /activation crossed scene gates/);
});

test('D07 runtime activation is explicit and does not grant scene readiness or Narrator permission', () => {
  const activationRef = { path: EXPECTED_D07_ACTIVATION_PATH, blob_sha: hash('a') };
  const truthRef = { path: 'architecture/D07_V018.md', blob_sha: hash('b') };
  const authorizationRef = { path: EXPECTED_AUTHORIZATION_PATH, blob_sha: hash('c') };
  const record = { document_id: 'D07_ACTIVATION_V004_PLAYER_SAFE', version: 'V004', status: 'ACTIVE', activation_kind: 'D07_RUNTIME_TRUTH_PACKAGE', runtime_activation: { d07_active: true }, authorization_ref: structuredClone(authorizationRef), truth_package_ref: structuredClone(truthRef) };
  assert.equal(validateD07RuntimeActivation(record, activationRef, truthRef, authorizationRef).d07_active, true);
  const { c, prev } = activationPair();
  assert.equal(c.operational_gates.d07_active, true);
  assert.equal(c.operational_gates.scene_ready, false);
  assert.equal(c.operational_gates.narrator_permission, false);
  assert.equal(validateActivationTransition(c, prev).ok, true);
  const agentAccessOnly = structuredClone(record); agentAccessOnly.runtime_activation = undefined;
  assert.throws(() => validateD07RuntimeActivation(agentAccessOnly, activationRef, truthRef, authorizationRef), /D07 runtime activation record mismatch/);
  const wrongPackage = structuredClone(record); wrongPackage.truth_package_ref.blob_sha = hash('d');
  assert.throws(() => validateD07RuntimeActivation(wrongPackage, activationRef, truthRef, authorizationRef), /D07 activation truth package mismatch/);
  const wrongAuthorization = structuredClone(record); wrongAuthorization.authorization_ref.blob_sha = hash('e');
  assert.throws(() => validateD07RuntimeActivation(wrongAuthorization, activationRef, truthRef, authorizationRef), /D07 activation authorization blob mismatch/);
  const staleAuthorization = { path: 'novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_AGENT_ACCESS_V003.json', blob_sha: hash('c') };
  assert.throws(() => validateD07RuntimeActivation(record, activationRef, truthRef, staleAuthorization), /fixed V004 decision/);
});

test('V10 Dramaturgo transition accepts only exact checkpoint and all readiness gates', () => {
  const { c, prev } = reviewPair();
  assert.equal(validateDramaturgoTransition(c, prev).ok, true);
  const falseReady = structuredClone(c); falseReady.operational_gates.scene_ready = false;
  assert.throws(() => validateDramaturgoTransition(falseReady, prev), /gate not passed: scene_ready/);
  const changedEvent = structuredClone(c); changedEvent.checkpoint.last_event_id = 'invented-event';
  assert.throws(() => validateDramaturgoTransition(changedEvent, prev), /changed real event or scene cursor/);
  const pending = structuredClone(c); pending.pending_player_decision = 'CLOSE_M3_01_AS_ALTERNATE_OR_CONTINUE';
  assert.throws(() => validateDramaturgoTransition(pending, prev), /cannot carry a pending player decision/);
});

test('V10 closure recommendation routes only and cannot close, record a choice, or start a scene', () => {
  const { c, prev } = reviewPair();
  Object.assign(c, { transition: 'CLOSURE_RECOMMENDED', status: 'PROVOCATION_CLOSURE_PENDING', next_role: 'NONE',
    plan: { validity: 'REVISED', reviewed_against_event_id: c.checkpoint.last_event_id },
    review: { decision: 'CLOSURE_RECOMMENDED', against_last_event_id: c.checkpoint.last_event_id, public_rationale: 'Encaminha escolha sem fechar a provocação ou iniciar cena.' },
    pending_player_decision: 'CLOSE_M3_01_AS_ALTERNATE_OR_CONTINUE', blocking: { code: 'PLAYER_DECISION_REQUIRED', reason: 'A decisão expressa permanece com o jogador.' } });
  Object.assign(c.operational_gates, { story_preparation_ready: false, mechanical_scene_ready: false, scene_ready: false, narrator_permission: false });
  assert.equal(validateClosureRecommendationTransition(c, prev).ok, true);
  const sceneReady = structuredClone(c); sceneReady.operational_gates.scene_ready = true;
  assert.throws(() => validateClosureRecommendationTransition(sceneReady, prev), /closure crossed a scene gate/);
  const changedProvocation = structuredClone(c); changedProvocation.provocation_id = 'M3.02';
  assert.throws(() => validateClosureRecommendationTransition(changedProvocation, prev), /closure sequence\/provocation/);
  const changedEvent = structuredClone(c); changedEvent.checkpoint.last_event_id = 'invented-event';
  assert.throws(() => validateClosureRecommendationTransition(changedEvent, prev), /changed the real checkpoint/);
});

test('V10 BLOCKED transition is event-anchored and preserves the source checkpoint without readiness', () => {
  const { prev: source } = reviewPair();
  const c = structuredClone(source);
  Object.assign(c, { sequence: 36, cycle_id: cycleId(36), transition: 'BLOCKED', status: 'BLOCKED_CONFLICT', next_role: 'NONE',
    plan: { validity: 'STALE' }, review: { decision: 'BLOCKED', against_last_event_id: source.checkpoint.last_event_id,
      public_rationale: 'Validação sintética bloqueada por uma referência de teste incompatível.' },
    pending_player_decision: null,
    blocking: { code: 'SYNTHETIC_VALIDATION_BLOCK', reason: 'Caso sintético: dependência de validação ausente.' },
    guards: structuredClone(guards) });
  Object.assign(c.operational_gates, { story_preparation_ready: false, mechanical_scene_ready: false, scene_ready: false, narrator_permission: false });
  assert.equal(validateBlockedTransition(c, source).ok, true);

  const readinessLeak = structuredClone(c); readinessLeak.operational_gates.scene_ready = true;
  assert.throws(() => validateBlockedTransition(readinessLeak, source), /blocked cycle changed checkpoint\/source refs|blocked cycle leaked a scene permission/);
  const changedCursor = structuredClone(c); changedCursor.checkpoint.last_event_id = 'SYNTHETIC_UNCONFIRMED_EVENT';
  assert.throws(() => validateBlockedTransition(changedCursor, source), /blocked cycle changed checkpoint\/source refs/);
  const falseRole = structuredClone(c); falseRole.next_role = 'NARRADOR';
  assert.throws(() => validateBlockedTransition(falseRole, source), /blocked transition status\/role/);
});

test('V10 SCENE_COMMITTED synthetic transition requires consistent persisted evidence; fixture is in-memory only', () => {
  const { c: prev } = reviewPair();
  prev.plan.dossier = { path: 'synthetic/M3.01_DOSSIER_V10.json', blob_sha: hash('1') };
  prev.plan.sidecar = { path: 'synthetic/M3.01_SIDECAR_V10.json', blob_sha: hash('2') };
  const eventId = 'SYNTHETIC-ONLY-EVENT-C06-001';
  const c = structuredClone(prev);
  c.sequence = prev.sequence + 1;
  c.cycle_id = cycleId(c.sequence);
  c.transition = 'SCENE_COMMITTED';
  c.status = 'READY_FOR_DRAMATURGO';
  c.next_role = 'DRAMATURGO';
  c.checkpoint = { ...structuredClone(prev.checkpoint), last_event_id: eventId, last_closed_scene: 'C06', next_scene: 'C07', next_scene_status: 'NOT_STARTED', pending_persistence: false };
  c.refs.episode.blob_sha = hash('e');
  c.refs.live.path = 'synthetic/live_after_c06.json';
  c.refs.live.blob_sha = hash('f');
  c.plan = { ...structuredClone(prev.plan), validity: 'STALE' };
  c.review = { decision: 'NOT_REVIEWED', against_last_event_id: eventId };
  c.pending_player_decision = null;
  c.operational_gates = { architecture_active: true, d07_active: true, story_preparation_ready: false, mechanical_scene_ready: false, scene_ready: false, narrator_permission: false };
  c.guards = structuredClone(guards);
  const live = { character: { mortal: true }, stage: { embrace_occurred: false }, simulation_only: false, last_confirmed_event_id: eventId,
    scene: { status: 'CLOSED', last_event_id: eventId, source_ref: { path: c.refs.episode.path }, scene_id: 'SYNTHETIC-C06' }, recent_event_ids: [eventId] };
  const episodeText = `Synthetic test fixture only: ${eventId}`;
  assert.equal(validateSceneCommittedTransition(c, prev, { live, episodeText }).ok, true);

  const unpersistedEvent = structuredClone(c); unpersistedEvent.refs.episode.blob_sha = prev.refs.episode.blob_sha;
  assert.throws(() => validateSceneCommittedTransition(unpersistedEvent, prev, { live, episodeText }), /scene commit did not persist changed episode and LIVE/);
  const staleLive = structuredClone(live); staleLive.last_confirmed_event_id = prev.checkpoint.last_event_id;
  assert.throws(() => validateSceneCommittedTransition(c, prev, { live: staleLive, episodeText }), /scene commit is not confirmed by persisted LIVE/);
  const prematureReview = structuredClone(c); prematureReview.plan.dossier.blob_sha = hash('3');
  assert.throws(() => validateSceneCommittedTransition(prematureReview, prev, { live, episodeText }), /Narrator changed Dramaturgo preparation/);
  const nextSceneReady = structuredClone(c); nextSceneReady.operational_gates.scene_ready = true;
  assert.throws(() => validateSceneCommittedTransition(nextSceneReady, prev, { live, episodeText }), /scene commit retained readiness gate/);
});

test('V10 fixed artifact paths and manifest path/blob pins reject stale or drifted pointers', () => {
  const arch = Object.fromEntries(Object.entries(EXPECTED_RUNTIME_PATHS).map(([key, p], i) => [key, { path: p, blob_sha: hash(String(i + 1)) }]));
  for (const [i, [key, p]] of Object.entries(EXPECTED_BOOTSTRAP_PATHS).entries()) arch[key] = { path: p, blob_sha: hash(String(i + 6)) };
  const blobRefs = structuredClone(arch);
  const orchestration = {
    contract: arch.orchestration_contract.path, contract_blob_sha: arch.orchestration_contract.blob_sha,
    cycle_schema: arch.cycle_schema.path, cycle_schema_blob_sha: arch.cycle_schema.blob_sha,
    validator: arch.cycle_validator.path, validator_blob_sha: arch.cycle_validator.blob_sha,
    tests: arch.cycle_tests.path, tests_blob_sha: arch.cycle_tests.blob_sha,
    schema_tests: arch.cycle_schema_tests.path, schema_tests_blob_sha: arch.cycle_schema_tests.blob_sha,
    entrypoint: arch.start_here.path, entrypoint_blob_sha: arch.start_here.blob_sha
  };
  const activation = { path: EXPECTED_D07_ACTIVATION_PATH, blob_sha: hash('a') };
  blobRefs.d07_activation_record = structuredClone(activation);
  const authorization = { path: EXPECTED_AUTHORIZATION_PATH, blob_sha: hash('b') };
  const c = { architecture: arch, activation: { d07_activation: activation, authorization } }, manifest = { runtime: { orchestration, narrative_architecture: { blob_refs: blobRefs }, d07_activation_current: structuredClone(activation), operational_entry_current: structuredClone(arch.agent_entry), context_gateway_current: structuredClone(arch.context_gateway) } };
  assert.equal(validateExpectedArtifactPins(c, manifest).ok, true);
  for (const [key, p] of Object.entries(EXPECTED_RUNTIME_PATHS)) {
    const badCycle = structuredClone(c); badCycle.architecture[key].path = 'novydres/runtime/obsolete.json';
    assert.throws(() => validateExpectedArtifactPins(badCycle, manifest), new RegExp(`cycle fixed artifact pin mismatch: ${key}`));
    const badManifest = structuredClone(manifest); badManifest.runtime.narrative_architecture.blob_refs[key].blob_sha = hash('f');
    assert.throws(() => validateExpectedArtifactPins(c, badManifest), new RegExp(`manifest fixed artifact blob pin mismatch: ${key}`));
  }
  for (const [key, p] of Object.entries(EXPECTED_BOOTSTRAP_PATHS)) {
    const badCycle = structuredClone(c); badCycle.architecture[key].path = 'novydres/.AGENT.md';
    assert.throws(() => validateExpectedArtifactPins(badCycle, manifest), new RegExp(`cycle fixed bootstrap pin mismatch: ${key}`));
    const badManifest = structuredClone(manifest); badManifest.runtime.narrative_architecture.blob_refs[key].path = 'novydres/.CONTEXTG.md';
    assert.throws(() => validateExpectedArtifactPins(c, badManifest), new RegExp(`manifest fixed bootstrap blob pin mismatch: ${key}`));
    const badCurrent = structuredClone(manifest);
    const activeKey = key === 'agent_entry' ? 'operational_entry_current' : 'context_gateway_current';
    badCurrent.runtime[activeKey].blob_sha = hash('f');
    assert.throws(() => validateExpectedArtifactPins(c, badCurrent), new RegExp(`manifest current bootstrap pointer mismatch: ${key}`));
  }
  const wrongTestSHA = structuredClone(manifest); wrongTestSHA.runtime.orchestration.tests_blob_sha = hash('f');
  assert.throws(() => validateExpectedArtifactPins(c, wrongTestSHA), /manifest active artifact path\/blob mismatch: cycle_tests/);
  const wrongActivation = structuredClone(c); wrongActivation.activation.d07_activation.path = 'novydres/runtime/narrative-architecture/program/deliverables/D07_ACTIVATION_V002_PLAYER_SAFE.json';
  assert.throws(() => validateExpectedArtifactPins(wrongActivation, manifest), /cycle fixed D07 activation pin mismatch/);
  const wrongAuthorization = structuredClone(c); wrongAuthorization.activation.authorization.path = 'novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_AGENT_ACCESS_V003.json';
  assert.throws(() => validateExpectedArtifactPins(wrongAuthorization, manifest), /cycle fixed V004 authorization pin mismatch/);
  const staleManifestActivation = structuredClone(manifest); staleManifestActivation.runtime.d07_activation_current.blob_sha = hash('f');
  assert.throws(() => validateExpectedArtifactPins(c, staleManifestActivation), /manifest D07 activation path\/blob mismatch/);
  const missingActivationBlobRef = structuredClone(manifest); delete missingActivationBlobRef.runtime.narrative_architecture.blob_refs.d07_activation_record;
  assert.throws(() => validateExpectedArtifactPins(c, missingActivationBlobRef), /manifest fixed D07 activation blob pin mismatch/);
  const staleActivationBlobRef = structuredClone(manifest); staleActivationBlobRef.runtime.narrative_architecture.blob_refs.d07_activation_record.blob_sha = hash('f');
  assert.throws(() => validateExpectedArtifactPins(c, staleActivationBlobRef), /manifest fixed D07 activation blob pin mismatch/);
  const missingNarrativeBlobRefs = structuredClone(manifest); delete missingNarrativeBlobRefs.runtime.narrative_architecture.blob_refs;
  assert.throws(() => validateExpectedArtifactPins(c, missingNarrativeBlobRefs), /manifest missing V10 operational blob refs/);
});

test('V10 preparation checkpoint pins all six operational sources, including individual knowledge and open threads', () => {
  const f = preparationSourceFixture();
  assert.equal(validatePreparationSourceCheckpoint(f.cp, f.sourceCycle, f.sourceManifest, f.c, 'dossier', f.preparation).ok, true);
  for (const [field, bad, message] of [
    ['knowledge_blob_sha', hash('f'), /knowledge checkpoint pin mismatch/],
    ['open_threads_path', 'source/wrong-threads.json', /threads checkpoint pin mismatch/]
  ]) {
    const changed = structuredClone(f.cp); changed[field] = bad;
    assert.throws(() => validatePreparationSourceCheckpoint(changed, f.sourceCycle, f.sourceManifest, f.c, 'dossier', f.preparation), message);
  }
  const missingNpc = structuredClone(f.preparation); missingNpc.source_refs = missingNpc.source_refs.filter(x => x.path !== f.sourceCycle.refs.knowledge.path);
  assert.throws(() => validatePreparationSourceCheckpoint(f.cp, f.sourceCycle, f.sourceManifest, f.c, 'sidecar', missingNpc), /does not pin source cycle ref: knowledge/);
  const missingThreads = structuredClone(f.preparation); missingThreads.source_refs = missingThreads.source_refs.filter(x => x.path !== f.sourceCycle.refs.threads.path);
  assert.throws(() => validatePreparationSourceCheckpoint(f.cp, f.sourceCycle, f.sourceManifest, f.c, 'sidecar', missingThreads), /does not pin source cycle ref: threads/);
});

test('preparation next-scene must match the exact cycle cursor', () => {
  const c = { checkpoint: { next_scene: 'C06' } };
  assert.equal(validatePreparationCheckpoint({ next_scene: 'C06' }, c, 'dossier').ok, true);
  assert.throws(() => validatePreparationCheckpoint({ next_scene: 'C07' }, c, 'dossier'), /next_scene differs/);
});

test('closure handoff preserves open quiet, no recorded choice, and no fictional scene data', () => {
  const doc = openQuietHandoff();
  assert.equal(validateOpenQuietHandoff(doc, 'dossier').ok, true);
  for (const [mutate, message] of [
    d => { d.provocation_status = 'CLOSED'; }, /incorrectly closes/,
    d => { d.handoff.next_decision.decision_recorded = true; }, /records a player choice/,
    d => { d.handoff.next_decision.default_if_no_action = 'CLOSE'; }, /open-quiet default/,
    d => { d.handoff.stakes = 'invented'; }, /unprepared scene or decision/,
    d => { d.scene_ready = true; }, /leaked scene readiness/,
    d => { d.handoff.next_decision.choices = d.handoff.next_decision.choices.slice(1); }, /three distinct player routes/
  ].reduce((pairs, item, i, all) => { if (i % 2 === 0) pairs.push([item, all[i + 1]]); return pairs; }, [])) {
    const changed = structuredClone(doc); mutate(changed);
    assert.throws(() => validateOpenQuietHandoff(changed, 'dossier'), message);
  }
});

test('narrator prompt is mandatory only when ready and never repeats an exact hidden phrase', () => {
  const hidden = 'SYNTHETIC_SECRET_SENTINEL internal phrase exists solely in test fixture';
  assert.equal(validateNarratorPrompt({ narrator_prompt: null }, 'PROVOCATION_CLOSURE_PENDING', 'NONE', [hidden]).prompt_present, false);
  assert.equal(validateNarratorPrompt({ narrator_prompt: null }, 'READY_FOR_DRAMATURGO', 'DRAMATURGO', [hidden]).prompt_present, false);
  assert.throws(() => validateNarratorPrompt({ narrator_prompt: null }, 'READY_FOR_NARRATOR', 'NARRADOR', [hidden]), /requires a nonempty public narrator prompt/);
  assert.throws(() => validateNarratorPrompt({ narrator_prompt: 'SYNTHETIC_SECRET_SENTINEL internal phrase exists solely in test fixture' }, 'READY_FOR_NARRATOR', 'NARRADOR', [hidden]), /repeats a hidden-source phrase/);
  assert.equal(validateNarratorPrompt({ narrator_prompt: 'Narrate from verified sources after receiving the player handoff.' }, 'READY_FOR_NARRATOR', 'NARRADOR', [hidden]).prompt_present, true);
  assert.equal(containsHiddenPhrase('Use verified repository sources and wait for the player.', hidden), false);
});


test('V9 to V10 migration advances runtime pins only and keeps closure pending', () => {
  const cycleDir = path.join(root, 'novydres/chronicles/CHR-001/orchestration');
  const previous = JSON.parse(fs.readFileSync(path.join(cycleDir, 'CYCLE_V0035.json'), 'utf8'));
  const current = JSON.parse(fs.readFileSync(path.join(cycleDir, 'CYCLE_V0036.json'), 'utf8'));
  const result = validateV9ToV10ClosureMigration(current, previous);
  assert.equal(result.ok, true);
  assert.equal(current.status, 'PROVOCATION_CLOSURE_PENDING');
  assert.equal(current.next_role, 'NONE');
  assert.equal(current.operational_gates.scene_ready, false);
  assert.equal(current.operational_gates.narrator_permission, false);

  const narrativeDrift = structuredClone(current);
  narrativeDrift.architecture.d07.blob_sha = hash('f');
  assert.throws(() => validateV9ToV10ClosureMigration(narrativeDrift, previous), /changed non-runtime architecture pin: d07/);
  const activationDrift = structuredClone(current);
  activationDrift.activation.architecture_contract.blob_sha = hash('e');
  assert.throws(() => validateV9ToV10ClosureMigration(activationDrift, previous), /rewrote historical activation evidence: architecture_contract/);
  const readinessLeak = structuredClone(current);
  readinessLeak.operational_gates.scene_ready = true;
  assert.throws(() => validateV9ToV10ClosureMigration(readinessLeak, previous), /closure crossed a scene gate/);
});

const hasV10Cycle = (() => {
  const dir = path.join(root, 'novydres/chronicles/CHR-001/orchestration');
  return fs.readdirSync(dir).some(name => /^CYCLE_V\d+\.json$/.test(name) && JSON.parse(fs.readFileSync(path.join(dir, name), 'utf8')).schema_id === 'NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V10');
})();
test('current V10 candidate validates through source pins and predecessor chain', { skip: !hasV10Cycle }, () => {
  assert.equal(validateLatestV10(root).ok, true);
});
