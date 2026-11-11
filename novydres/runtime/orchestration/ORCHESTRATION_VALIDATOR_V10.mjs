#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { validateLatestV9 } from './ORCHESTRATION_VALIDATOR_V9.mjs';

const fail = m => { throw new Error(`ORCHESTRATION_V10_BLOCK: ${m}`); };
const check = (v, m) => { if (!v) fail(m); };
const read = (root, p) => {
  check(typeof p === 'string' && !p.includes('..') && !path.isAbsolute(p), 'invalid relative path');
  const q = path.resolve(root, p);
  check(q.startsWith(path.resolve(root) + path.sep), 'path escapes repository');
  return fs.readFileSync(q);
};
const json = (root, p) => JSON.parse(read(root, p).toString('utf8'));
const blob = b => crypto.createHash('sha1').update(Buffer.from(`blob ${b.length}\0`)).update(b).digest('hex');
const verify = (root, ref, label) => check(ref && blob(read(root, ref.path)) === ref.blob_sha, `blob mismatch: ${label}`);
const noDeltaGuards = c => {
  for (const k of ['no_story_delta_in_prep', 'no_xp_fv_delta_in_prep', 'g28_scene_only', 'frozen_unchanged', 'no_public_spoilers']) {
    check(c.guards?.[k] === true, `guard not preserved: ${k}`);
  }
};
const cyclePath = n => `novydres/chronicles/CHR-001/orchestration/CYCLE_V${String(n).padStart(4, '0')}.json`;
const REFS = ['live', 'history_index', 'episode', 'character', 'knowledge', 'threads'];
const MECHANICAL_SOURCES = ['rules_provenance', 'target_sheet', 'adjudication_gate', 'motor_manual', 'xp_policy', 'xp_audit', 'act_resolution_schema', 'xp_envelope', 'settlement_record'];
const SOURCE_INDEX_IDS = {
  rules_provenance: 'guided_creation_mechanical_provenance',
  target_sheet: 'approved_target_sheet',
  adjudication_gate: 'mechanical_adjudication_gate',
  motor_manual: 'v5_mechanical_rules_text',
  xp_policy: 'xp_credit_policy',
  xp_audit: 'xp_credit_audit_contract',
  act_resolution_schema: 'act_resolution_schema_only',
  xp_envelope: 'current_xp_envelope',
  settlement_record: 'current_settled_xp_transaction_record'
};
const cycleId = n => `CHR001-CYCLE-${String(n).padStart(4, '0')}`;
const READINESS_GATES = ['architecture_active', 'd07_active', 'story_preparation_ready', 'mechanical_scene_ready', 'scene_ready', 'narrator_permission'];
export const EXPECTED_RUNTIME_PATHS = Object.freeze({
  orchestration_contract: 'novydres/runtime/orchestration/ORCHESTRATION_CONTRACT_V8.md',
  cycle_schema: 'novydres/runtime/orchestration/CYCLE_SCHEMA_V10.json',
  cycle_validator: 'novydres/runtime/orchestration/ORCHESTRATION_VALIDATOR_V10.mjs',
  cycle_tests: 'novydres/runtime/orchestration/ORCHESTRATION_TESTS_V10.mjs',
  cycle_schema_tests: 'novydres/runtime/orchestration/ORCHESTRATION_SCHEMA_TESTS_V10.py',
  preparation_dossier_schema: 'novydres/runtime/provocation-prep/PROVOCATION_DOSSIER_SCHEMA_V6.json',
  preparation_sidecar_schema: 'novydres/runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V6.json',
  start_here: 'novydres/runtime/orchestration/START_HERE_V7.md'
});
export const EXPECTED_D07_ACTIVATION_PATH = 'novydres/runtime/narrative-architecture/program/deliverables/D07_ACTIVATION_V004_PLAYER_SAFE.json';
export const EXPECTED_AUTHORIZATION_PATH = 'novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_AGENT_ACCESS_V004.json';
export const EXPECTED_BOOTSTRAP_PATHS = Object.freeze({
  agent_entry: 'novydres/.AGENT_V4.md',
  context_gateway: 'novydres/.CONTEXTG_V3.md'
});
const EXPECTED_MANIFEST_FIELDS = Object.freeze({
  orchestration_contract: ['contract', 'contract_blob_sha'],
  cycle_schema: ['cycle_schema', 'cycle_schema_blob_sha'],
  cycle_validator: ['validator', 'validator_blob_sha'],
  cycle_tests: ['tests', 'tests_blob_sha'],
  cycle_schema_tests: ['schema_tests', 'schema_tests_blob_sha'],
  start_here: ['entrypoint', 'entrypoint_blob_sha']
});
const sameCursor = (a, b) => ['last_event_id', 'last_closed_scene', 'next_scene', 'next_scene_status', 'pending_persistence', 'mortal', 'embrace_occurred'].every(k => a.checkpoint[k] === b.checkpoint[k]);
const sameRefs = (a, b) => REFS.every(k => a.refs?.[k]?.path === b.refs?.[k]?.path && a.refs?.[k]?.blob_sha === b.refs?.[k]?.blob_sha);
const sameMechanicalSources = (a, b) => a.operational_gates?.mechanical_matrix_ref?.path === b.operational_gates?.mechanical_matrix_ref?.path && a.operational_gates?.mechanical_matrix_ref?.blob_sha === b.operational_gates?.mechanical_matrix_ref?.blob_sha && MECHANICAL_SOURCES.every(k => a.operational_gates?.mechanical_sources?.[k]?.path === b.operational_gates?.mechanical_sources?.[k]?.path && a.operational_gates?.mechanical_sources?.[k]?.blob_sha === b.operational_gates?.mechanical_sources?.[k]?.blob_sha);
const sameArchitecture = (a, b) => {
  const left = a.architecture ?? {}, right = b.architecture ?? {};
  return Object.keys(left).length === Object.keys(right).length && Object.entries(left).every(([k, r]) => right[k]?.path === r.path && right[k]?.blob_sha === r.blob_sha);
};

const pythonSchemaCheck = `import json,sys
from jsonschema import Draft202012Validator
item=json.load(sys.stdin)
schema=item['schema']; document=item['document']
Draft202012Validator.check_schema(schema)
errors=list(Draft202012Validator(schema).iter_errors(document))
if errors:
 e=errors[0]
 print('/'.join(str(x) for x in e.absolute_path)+': '+e.message)
 sys.exit(1)
`;

export function validateDocumentAgainstSchema(root, schemaRef, document, label = 'document') {
  verify(root, schemaRef, `${label} schema`);
  const schema = json(root, schemaRef.path);
  const result = spawnSync('python3', ['-c', pythonSchemaCheck], {
    input: JSON.stringify({ schema, document }), encoding: 'utf8', maxBuffer: 4 * 1024 * 1024
  });
  check(!result.error && result.status === 0, `${label} schema validation failed: ${(result.stderr || result.stdout || result.error?.message || 'unknown error').trim()}`);
  return { ok: true, schema_path: schemaRef.path, schema_blob_sha: schemaRef.blob_sha };
}

const disclosureWords = value => (value.toLocaleLowerCase('pt-BR').match(/[\p{L}\p{N}]+/gu) || []);
export function containsHiddenPhrase(publicText, hiddenText, minWords = 8) {
  const hidden = disclosureWords(hiddenText), publicWords = disclosureWords(publicText);
  if (hidden.length < minWords || publicWords.length < minWords) return false;
  const phrases = new Set();
  for (let i = 0; i <= hidden.length - minWords; i++) phrases.add(hidden.slice(i, i + minWords).join(' '));
  for (let i = 0; i <= publicWords.length - minWords; i++) if (phrases.has(publicWords.slice(i, i + minWords).join(' '))) return true;
  return false;
}

export function validatePreparationCheckpoint(cp, c, label = 'preparation') {
  check(cp?.next_scene === c.checkpoint.next_scene, `${label} next_scene differs from cycle checkpoint`);
  return { ok: true };
}

export function validatePreparationSourceCheckpoint(cp, sourceCycle, sourceManifest, c, label = 'preparation', preparation) {
  check(cp?.cycle_path === c.previous_cycle?.path && cp?.cycle_blob_sha === c.previous_cycle?.blob_sha, `${label} source cycle differs from immediate predecessor`);
  check(['NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V9', 'NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V10'].includes(sourceCycle?.schema_id) && sourceCycle.sequence + 1 === c.sequence && sourceCycle.cycle_id === cycleId(sourceCycle.sequence), `${label} source cycle identity/schema mismatch`);
  check(['OPERATIONAL_ACTIVATED', 'SCENE_COMMITTED'].includes(sourceCycle.transition) && sourceCycle.status === 'READY_FOR_DRAMATURGO', `${label} source cycle is not a valid Dramaturgo checkpoint`);
  check(sourceCycle.provocation_id === c.provocation_id, `${label} source cycle provocation mismatch`);
  check(cp?.base_commit_sha === sourceCycle.source_head_sha, `${label} source head mismatch`);
  check(cp?.manifest_path === sourceCycle.manifest_path && cp?.manifest_path === sourceCycle.manifest_ref?.path && cp?.manifest_blob_sha === sourceCycle.manifest_ref?.blob_sha, `${label} source manifest pin mismatch`);
  const mappings = [
    ['live', 'live_path', 'live_blob_sha'],
    ['history_index', 'history_index_path', 'history_index_blob_sha'],
    ['episode', 'episode_path', 'episode_blob_sha'],
    ['character', 'state_path', 'state_blob_sha'],
    ['knowledge', 'knowledge_path', 'knowledge_blob_sha'],
    ['threads', 'open_threads_path', 'open_threads_blob_sha']
  ];
  for (const [sourceKey, pathKey, shaKey] of mappings) {
    check(cp?.[pathKey] === sourceCycle.refs?.[sourceKey]?.path && cp?.[shaKey] === sourceCycle.refs?.[sourceKey]?.blob_sha, `${label} ${sourceKey} checkpoint pin mismatch`);
  }
  check(Array.isArray(preparation?.source_refs), `${label} source refs missing`);
  for (const sourceKey of REFS) {
    const expected = sourceCycle.refs?.[sourceKey];
    check(expected?.path && expected?.blob_sha, `${label} source cycle ref missing: ${sourceKey}`);
    const pinned = preparation.source_refs.find(ref => ref?.path === expected.path && ref?.blob_sha === expected.blob_sha);
    check(Boolean(pinned), `${label} does not pin source cycle ref: ${sourceKey}`);
  }
  const sourceCheckpoint = sourceCycle.checkpoint;
  check((cp?.last_confirmed_event_id ?? cp?.last_event_id) === sourceCheckpoint?.last_event_id, `${label} source event mismatch`);
  check(cp?.last_closed_scene === sourceCheckpoint?.last_closed_scene && cp?.next_scene === sourceCheckpoint?.next_scene && cp?.next_scene_status === sourceCheckpoint?.next_scene_status, `${label} source scene cursor mismatch`);
  check(cp?.protagonist_mortal === sourceCheckpoint?.mortal && cp?.embrace_occurred === sourceCheckpoint?.embrace_occurred, `${label} source mortality/Embrace mismatch`);
  check(sourceManifest?.runtime?.orchestration?.current_cycle === cp.cycle_path && sourceManifest.runtime.orchestration.status === sourceCycle.status && sourceManifest.runtime.orchestration.next_role === sourceCycle.next_role, `${label} source manifest cursor/status mismatch`);
  check(sourceManifest.runtime.last_confirmed_narrative_event === sourceCheckpoint.last_event_id, `${label} source manifest event mismatch`);
  for (const [manifestKey, sourceKey] of [['live_current', 'live'], ['history_index_current', 'history_index'], ['episode_current', 'episode'], ['character_state_current', 'character'], ['knowledge_current', 'knowledge'], ['open_threads_current', 'threads']]) {
    check(sourceManifest.runtime[manifestKey] === sourceCycle.refs?.[sourceKey]?.path, `${label} source manifest ${manifestKey} mismatch`);
  }
  check(sourceManifest.runtime.orchestration.next_scene === sourceCheckpoint.next_scene && sourceManifest.runtime.orchestration.next_scene_status === sourceCheckpoint.next_scene_status, `${label} source manifest scene cursor mismatch`);
  return { ok: true, source_cycle_id: sourceCycle.cycle_id, source_manifest_path: cp.manifest_path };
}

export function validateNarratorPrompt(candidate, status, nextRole, hiddenTexts = []) {
  const prompt = candidate?.narrator_prompt;
  const narratorReady = status === 'READY_FOR_NARRATOR' && nextRole === 'NARRADOR';
  if (prompt === null || prompt === undefined) {
    check(!narratorReady, 'READY_FOR_NARRATOR requires a nonempty public narrator prompt');
    return { ok: true, prompt_present: false };
  }
  check(typeof prompt === 'string', 'public narrator prompt must be text or null');
  check(!narratorReady || prompt.trim().length > 0, 'READY_FOR_NARRATOR requires a nonempty public narrator prompt');
  for (const hiddenText of hiddenTexts) {
    check(!containsHiddenPhrase(prompt, hiddenText), 'public narrator prompt repeats a hidden-source phrase');
  }
  return { ok: true, prompt_present: prompt.trim().length > 0 };
}

export function validatePublicPromptDisclosure(root, c) {
  const candidate = json(root, c.architecture.d12_candidate.path);
  const hiddenTexts = ['d06', 'd07', 'd08'].map(key => read(root, c.architecture[key].path).toString('utf8'));
  return validateNarratorPrompt(candidate, c.status, c.next_role, hiddenTexts);
}

export function validateExpectedArtifactPins(c, manifest) {
  const orchestration = manifest?.runtime?.orchestration;
  const blobRefs = manifest?.runtime?.narrative_architecture?.blob_refs;
  check(orchestration && blobRefs, 'manifest missing V10 operational blob refs');
  for (const [key, expectedPath] of Object.entries(EXPECTED_RUNTIME_PATHS)) {
    const ref = c.architecture?.[key];
    check(ref?.path === expectedPath && /^[0-9a-f]{40}$/.test(ref?.blob_sha ?? ''), `cycle fixed artifact pin mismatch: ${key}`);
    const manifestRef = blobRefs[key];
    check(manifestRef?.path === expectedPath && manifestRef?.blob_sha === ref.blob_sha, `manifest fixed artifact blob pin mismatch: ${key}`);
    const fields = EXPECTED_MANIFEST_FIELDS[key];
    if (fields) check(orchestration[fields[0]] === expectedPath && orchestration[fields[1]] === ref.blob_sha, `manifest active artifact path/blob mismatch: ${key}`);
  }
  for (const [key, expectedPath] of Object.entries(EXPECTED_BOOTSTRAP_PATHS)) {
    const ref = c.architecture?.[key];
    check(ref?.path === expectedPath && /^[0-9a-f]{40}$/.test(ref?.blob_sha ?? ''), `cycle fixed bootstrap pin mismatch: ${key}`);
    const manifestRef = blobRefs[key];
    check(manifestRef?.path === expectedPath && manifestRef?.blob_sha === ref.blob_sha, `manifest fixed bootstrap blob pin mismatch: ${key}`);
    const currentRef = key === 'agent_entry' ? manifest.runtime?.operational_entry_current : manifest.runtime?.context_gateway_current;
    check(currentRef?.path === expectedPath && currentRef?.blob_sha === ref.blob_sha, `manifest current bootstrap pointer mismatch: ${key}`);
  }
  const activation = c.activation?.d07_activation;
  check(activation?.path === EXPECTED_D07_ACTIVATION_PATH && /^[0-9a-f]{40}$/.test(activation?.blob_sha ?? ''), 'cycle fixed D07 activation pin mismatch');
  check(c.activation?.authorization?.path === EXPECTED_AUTHORIZATION_PATH && /^[0-9a-f]{40}$/.test(c.activation?.authorization?.blob_sha ?? ''), 'cycle fixed V004 authorization pin mismatch');
  const activationManifestRef = blobRefs.d07_activation_record;
  check(activationManifestRef?.path === EXPECTED_D07_ACTIVATION_PATH && activationManifestRef?.blob_sha === activation.blob_sha, 'manifest fixed D07 activation blob pin mismatch');
  check(manifest.runtime.d07_activation_current?.path === EXPECTED_D07_ACTIVATION_PATH && manifest.runtime.d07_activation_current?.blob_sha === activation.blob_sha, 'manifest D07 activation path/blob mismatch');
  return { ok: true, pinned_artifacts: [...Object.keys(EXPECTED_RUNTIME_PATHS), ...Object.keys(EXPECTED_BOOTSTRAP_PATHS), 'd07_activation_record'] };
}

export function validateD07RuntimeActivation(record, activationRef, truthPackageRef, authorizationRef) {
  check(activationRef?.path === EXPECTED_D07_ACTIVATION_PATH && /^[0-9a-f]{40}$/.test(activationRef?.blob_sha ?? ''), 'D07 activation record path/blob is not the fixed V004 pin');
  check(record?.document_id === 'D07_ACTIVATION_V004_PLAYER_SAFE' && record.version === 'V004', 'D07 activation record identity/version mismatch');
  check(record?.status === 'ACTIVE' && record.activation_kind === 'D07_RUNTIME_TRUTH_PACKAGE' && record.runtime_activation?.d07_active === true, 'D07 runtime activation record mismatch');
  check(authorizationRef?.path === EXPECTED_AUTHORIZATION_PATH && /^[0-9a-f]{40}$/.test(authorizationRef?.blob_sha ?? ''), 'D07 activation authorization pin is not the fixed V004 decision');
  check(record.authorization_ref?.path === authorizationRef.path && record.authorization_ref?.blob_sha === authorizationRef.blob_sha, 'D07 activation authorization blob mismatch');
  check(record.truth_package_ref?.path === truthPackageRef?.path && record.truth_package_ref?.blob_sha === truthPackageRef?.blob_sha, 'D07 activation truth package mismatch');
  return { ok: true, d07_active: true };
}

export function validateOpenQuietHandoff(doc, label = 'preparation') {
  check(doc.provocation_status === 'OPEN' && doc.source_checkpoint?.provocation_status === 'OPEN', `${label} closure routing incorrectly closes M3.01`);
  check(doc.status === 'HANDOFF_PENDING_PLAYER_DECISION' && doc.scene_ready === false && doc.SCENE_READY === false && doc.NARRATOR_PERMISSION === false, `${label} closure handoff leaked scene readiness`);
  check(doc.closure_routing?.recommendation === 'PROVOCATION_CLOSURE_PENDING' && doc.closure_routing?.effect === 'ROUTING_ONLY' && doc.closure_routing?.player_decision_required === true && doc.closure_routing?.provocation_closed === false && doc.closure_routing?.event_created === false, `${label} closure routing mismatch`);
  check(doc.handoff?.player_decision_pending === true && doc.handoff?.cause === null && doc.handoff?.actors?.length === 0 && doc.handoff?.entry_condition === null && doc.handoff?.stakes === null && doc.handoff?.prepared_scenes?.length === 0 && doc.handoff?.acts?.length === 0, `${label} introduced an unprepared scene or decision`);
  const decision = doc.handoff?.next_decision;
  check(decision?.cause_status === 'NO_C06_CAUSE_ADMITTED_OR_AVAILABLE' && decision?.default_if_no_action === 'KEEP_OPEN_QUIET' && decision?.decision_recorded === false, `${label} changed the open-quiet default or records a player choice`);
  const choices = Array.isArray(decision?.choices) ? decision.choices.map(x => x?.choice_id).sort() : [];
  check(JSON.stringify(choices) === JSON.stringify(['CONTINUE_AFTER_ADMISSION', 'KEEP_OPEN_QUIET', 'REQUEST_ALTERNATE_CLOSURE']), `${label} does not preserve the three distinct player routes`);
  check(doc.governance?.no_story_event_created === true && doc.governance?.no_time_advanced === true && doc.governance?.no_npc_knowledge_delta === true && doc.governance?.no_player_spoilers === true, `${label} governance guard mismatch`);
  return { ok: true, provocation_status: 'OPEN', choice_recorded: false, scene_ready: false };
}

export function validateActivationTransition(c, prev) {
  check(c.transition === 'OPERATIONAL_ACTIVATED', 'activation transition name');
  check(c.status === 'READY_FOR_DRAMATURGO' && c.next_role === 'DRAMATURGO', 'activation role/status');
  check(c.sequence === prev.sequence + 1 && c.cycle_id === cycleId(c.sequence) && c.provocation_id === prev.provocation_id, 'activation sequence/provocation mismatch');
  check(prev.status === 'READY_FOR_DRAMATURGO' && prev.transition === 'SOURCE_RECONCILED', 'activation must follow reconciled source cycle');
  check(sameCursor(c, prev), 'activation changed scene/event cursor or checkpoint');
  check(sameRefs(c, prev), 'activation changed narrative source refs');
  check(c.pending_player_decision === null, 'activation carries a pending player decision');
  check(c.plan.validity === 'STALE' && c.review.decision === 'NOT_REVIEWED' && c.review.against_last_event_id === c.checkpoint.last_event_id, 'activation cannot claim Dramaturgo review');
  check(c.operational_gates.architecture_active === true && c.operational_gates.d07_active === true, 'architecture/D07 not active');
  check(c.operational_gates.story_preparation_ready === false && c.operational_gates.mechanical_scene_ready === false && c.operational_gates.scene_ready === false && c.operational_gates.narrator_permission === false, 'activation crossed scene gates');
  noDeltaGuards(c);
  return { ok: true, transition: c.transition, cycle_id: c.cycle_id };
}

export function validateDramaturgoTransition(c, prev) {
  check(['PLAN_REVISED', 'PLAN_REVALIDATED'].includes(c.transition), 'Dramaturgo transition name');
  check(c.status === 'READY_FOR_NARRATOR' && c.next_role === 'NARRADOR', 'Narrator status/role');
  check(['OPERATIONAL_ACTIVATED', 'SCENE_COMMITTED'].includes(prev.transition) && prev.status === 'READY_FOR_DRAMATURGO' && prev.sequence + 1 === c.sequence, 'Dramaturgo review must follow activation or a persisted scene');
  check(c.sequence === prev.sequence + 1 && c.cycle_id === cycleId(c.sequence) && c.provocation_id === prev.provocation_id, 'Dramaturgo cycle identity/provocation mismatch');
  check(sameCursor(c, prev), 'review changed real event or scene cursor');
  check(sameRefs(c, prev) && sameMechanicalSources(c, prev) && sameArchitecture(c, prev), 'Dramaturgo review changed source state, architecture, or mechanical pins');
  check(c.plan.validity === (c.transition === 'PLAN_REVISED' ? 'REVISED' : 'VALIDATED'), 'plan validity disagrees with transition');
  check(c.review.decision === (c.transition === 'PLAN_REVISED' ? 'REVISED' : 'REVALIDATED') && c.review.against_last_event_id === c.checkpoint.last_event_id, 'review does not match latest event');
  for (const k of ['architecture_active', 'd07_active', 'story_preparation_ready', 'mechanical_scene_ready', 'scene_ready', 'narrator_permission']) check(c.operational_gates[k] === true, `gate not passed: ${k}`);
  check(c.checkpoint.pending_persistence === false, 'review changed persistence');
  check(c.pending_player_decision === null, 'Narrator-ready cycle cannot carry a pending player decision');
  noDeltaGuards(c);
  return { ok: true, transition: c.transition, cycle_id: c.cycle_id, reviewed_event_id: c.review.against_last_event_id };
}

export function validateClosureRecommendationTransition(c, prev) {
  check(c.transition === 'CLOSURE_RECOMMENDED', 'closure transition name');
  check(c.status === 'PROVOCATION_CLOSURE_PENDING' && c.next_role === 'NONE', 'closure status/role');
  check(['OPERATIONAL_ACTIVATED', 'SCENE_COMMITTED'].includes(prev.transition) && prev.status === 'READY_FOR_DRAMATURGO' && prev.sequence + 1 === c.sequence, 'closure review must follow activation or a persisted scene');
  check(c.sequence === prev.sequence + 1 && c.cycle_id === cycleId(c.sequence) && c.provocation_id === prev.provocation_id, 'closure sequence/provocation');
  check(sameCursor(c, prev) && sameRefs(c, prev) && sameMechanicalSources(c, prev) && sameArchitecture(c, prev), 'closure changed the real checkpoint or its source pins');
  check(c.checkpoint.pending_persistence === false, 'closure changed persistence');
  check(['REVISED', 'VALIDATED'].includes(c.plan.validity) && c.plan.reviewed_against_event_id === c.checkpoint.last_event_id, 'closure plan does not pin reviewed checkpoint');
  check(c.review.decision === 'CLOSURE_RECOMMENDED' && c.review.against_last_event_id === c.checkpoint.last_event_id && typeof c.review.public_rationale === 'string' && c.review.public_rationale.length >= 20, 'closure recommendation lacks checkpointed rationale');
  check(c.pending_player_decision === 'CLOSE_M3_01_AS_ALTERNATE_OR_CONTINUE', 'closure must name the pending player decision');
  check(c.blocking?.code === 'PLAYER_DECISION_REQUIRED' && typeof c.blocking.reason === 'string' && c.blocking.reason.length >= 20, 'closure must identify required player decision');
  check(c.operational_gates.architecture_active === true && c.operational_gates.d07_active === true, 'architecture/D07 not active for closure');
  check(c.operational_gates.story_preparation_ready === false && c.operational_gates.mechanical_scene_ready === false && c.operational_gates.scene_ready === false && c.operational_gates.narrator_permission === false, 'closure crossed a scene gate');
  noDeltaGuards(c);
  return { ok: true, transition: c.transition, cycle_id: c.cycle_id, reviewed_event_id: c.review.against_last_event_id, pending_player_decision: c.pending_player_decision };
}

export function validateSceneCommittedTransition(c, prev, { live, episodeText } = {}) {
  check(c.transition === 'SCENE_COMMITTED' && c.status === 'READY_FOR_DRAMATURGO' && c.next_role === 'DRAMATURGO', 'scene commit must return control to Dramaturgo');
  check(prev.status === 'READY_FOR_NARRATOR' && ['PLAN_REVISED', 'PLAN_REVALIDATED'].includes(prev.transition), 'scene committed without Narrator-ready predecessor');
  check(c.sequence === prev.sequence + 1 && c.cycle_id === cycleId(c.sequence) && c.provocation_id === prev.provocation_id, 'scene commit cycle identity/provocation mismatch');
  check(c.checkpoint.pending_persistence === false && c.checkpoint.next_scene_status === 'NOT_STARTED', 'scene commit has pending persistence or starts another scene');
  check(c.checkpoint.last_closed_scene === prev.checkpoint.next_scene && Number(c.checkpoint.next_scene.slice(1)) === Number(c.checkpoint.last_closed_scene.slice(1)) + 1, 'scene commit has wrong closed/next scene cursor');
  check(c.checkpoint.last_event_id !== prev.checkpoint.last_event_id, 'scene commit lacks a new real event');
  check(c.refs.episode.blob_sha !== prev.refs.episode.blob_sha && c.refs.live.blob_sha !== prev.refs.live.blob_sha, 'scene commit did not persist changed episode and LIVE');
  check(c.refs.live.path !== prev.refs.live.path, 'scene commit reused LIVE source');
  check(c.plan.dossier.blob_sha === prev.plan.dossier.blob_sha && c.plan.sidecar.blob_sha === prev.plan.sidecar.blob_sha, 'Narrator changed Dramaturgo preparation');
  check(c.plan.validity === 'STALE' && c.review.decision === 'NOT_REVIEWED' && c.review.against_last_event_id === c.checkpoint.last_event_id, 'scene commit preempted Dramaturgo review');
  check(live?.character?.mortal === c.checkpoint.mortal && live?.stage?.embrace_occurred === c.checkpoint.embrace_occurred, 'scene commit mortality/Embrace does not match LIVE');
  check(live && live.simulation_only === false && live.last_confirmed_event_id === c.checkpoint.last_event_id && live.scene?.status === 'CLOSED' && live.scene?.last_event_id === c.checkpoint.last_event_id, 'scene commit is not confirmed by persisted LIVE');
  check(live.scene.source_ref?.path === c.refs.episode.path && live.scene.scene_id?.includes(c.checkpoint.last_closed_scene), 'LIVE scene does not identify the committed episode and scene');
  check(typeof episodeText === 'string' && episodeText.includes(c.checkpoint.last_event_id), 'scene event is absent from persisted episode');
  check(Array.isArray(live.recent_event_ids) && live.recent_event_ids.includes(c.checkpoint.last_event_id), 'LIVE recent-event index omits committed event');
  for (const k of ['architecture_active', 'd07_active']) check(c.operational_gates[k] === true, `gate not active after scene: ${k}`);
  for (const k of ['story_preparation_ready', 'mechanical_scene_ready', 'scene_ready', 'narrator_permission']) check(c.operational_gates[k] === false, `scene commit retained readiness gate: ${k}`);
  check(c.pending_player_decision === null, 'scene commit carries a pending player decision');
  noDeltaGuards(c);
  return { ok: true, transition: c.transition, cycle_id: c.cycle_id, event_id: c.checkpoint.last_event_id };
}

export function validateBlockedTransition(c, prev) {
  check(c.transition === 'BLOCKED' && c.status === 'BLOCKED_CONFLICT' && c.next_role === 'NONE', 'blocked transition status/role');
  check(c.sequence === prev.sequence + 1 && c.cycle_id === cycleId(c.sequence) && c.provocation_id === prev.provocation_id, 'blocked cycle identity/provocation mismatch');
  check(sameCursor(c, prev) && sameRefs(c, prev) && sameMechanicalSources(c, prev) && sameArchitecture(c, prev), 'blocked cycle changed checkpoint/source refs');
  check(c.review.decision === 'BLOCKED' && c.review.against_last_event_id === c.checkpoint.last_event_id && typeof c.review.public_rationale === 'string' && c.review.public_rationale.length >= 20, 'blocked cycle lacks event-anchored reason');
  check(typeof c.blocking?.code === 'string' && c.blocking.code.length > 0 && typeof c.blocking.reason === 'string' && c.blocking.reason.length >= 20, 'blocked cycle lacks specific blocker');
  check(c.operational_gates.scene_ready === false && c.operational_gates.narrator_permission === false && c.pending_player_decision === null, 'blocked cycle leaked a scene permission/decision');
  check(c.blocking.code && c.blocking.reason && c.operational_gates.scene_ready === false && c.operational_gates.narrator_permission === false, 'blocked cycle lacks blocker or leaks readiness');
  noDeltaGuards(c);
  return { ok: true, transition: c.transition, cycle_id: c.cycle_id, blocker: c.blocking.code };
}

export function validateManifestReadiness(manifest, c) {
  const orchestration = manifest.runtime.orchestration;
  check(orchestration.next_scene_executable === c.operational_gates.scene_ready, 'manifest SCENE_READY mismatch');
  for (const k of READINESS_GATES) {
    check(orchestration.operational_gates?.[k] === c.operational_gates[k], `manifest readiness mismatch: ${k}`);
  }
  check(orchestration.pending_player_decision === c.pending_player_decision, 'manifest pending_player_decision mismatch');
  check(orchestration.next_scene === c.checkpoint.next_scene && orchestration.next_scene_status === c.checkpoint.next_scene_status, 'manifest next-scene checkpoint mismatch');
  check(orchestration.tests === c.architecture.cycle_tests.path && orchestration.tests_blob_sha === c.architecture.cycle_tests.blob_sha, 'manifest active orchestration tests path/blob mismatch');
  check(orchestration.schema_tests === c.architecture.cycle_schema_tests.path && orchestration.schema_tests_blob_sha === c.architecture.cycle_schema_tests.blob_sha, 'manifest active schema tests path/blob mismatch');
  return { ok: true };
}

function verifyCyclePins(root, c, cpath) {
  check(c.schema_id === 'NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V10', 'cycle schema id');
  check(c.cycle_id === cycleId(c.sequence), 'cycle id/sequence mismatch');
  check(c.manifest_ref.path === c.manifest_path, 'manifest path/ref mismatch');
  verify(root, c.manifest_ref, 'manifest');
  for (const [k, r] of Object.entries(c.refs)) verify(root, r, k);
  for (const [k, r] of Object.entries(c.architecture)) verify(root, r, `architecture.${k}`);
  check(c.architecture.cycle_schema.path === 'novydres/runtime/orchestration/CYCLE_SCHEMA_V10.json', 'active cycle schema path');
  validateDocumentAgainstSchema(root, c.architecture.cycle_schema, c, 'cycle');
  verify(root, c.plan.dossier, 'dossier');
  verify(root, c.plan.sidecar, 'sidecar');
  for (const [k, r] of Object.entries(c.activation)) verify(root, r, `activation.${k}`);
  verify(root, c.operational_gates.mechanical_matrix_ref, 'mechanical matrix');
  verify(root, c.architecture.d12_mechanical_source_refs, 'mechanical source index');
  for (const k of MECHANICAL_SOURCES) verify(root, c.operational_gates.mechanical_sources[k], `mechanical_sources.${k}`);
  const manifest = json(root, c.manifest_path), live = json(root, c.refs.live.path);
  validateExpectedArtifactPins(c, manifest);
  check(manifest.branch === 'master', 'manifest branch');
  check(manifest.runtime.last_confirmed_narrative_event === c.checkpoint.last_event_id, 'manifest last event mismatch');
  check(manifest.runtime.live_current === c.refs.live.path && manifest.runtime.history_index_current === c.refs.history_index.path && manifest.runtime.episode_current === c.refs.episode.path && manifest.runtime.character_state_current === c.refs.character.path && manifest.runtime.knowledge_current === c.refs.knowledge.path && manifest.runtime.open_threads_current === c.refs.threads.path, 'manifest source pointers mismatch');
  check(manifest.runtime.orchestration.current_cycle === cpath && manifest.runtime.orchestration.next_role === c.next_role, 'manifest cycle/role mismatch');
  check(manifest.runtime.orchestration.status === c.status, 'manifest operational status mismatch');
  check(manifest.runtime.orchestration.contract === c.architecture.orchestration_contract.path && manifest.runtime.orchestration.contract_blob_sha === c.architecture.orchestration_contract.blob_sha && manifest.runtime.orchestration.cycle_schema === EXPECTED_RUNTIME_PATHS.cycle_schema && manifest.runtime.orchestration.validator === EXPECTED_RUNTIME_PATHS.cycle_validator, 'manifest active contract pointers mismatch');
  check(manifest.runtime.orchestration.entrypoint === EXPECTED_RUNTIME_PATHS.start_here, 'manifest start-here pointer mismatch');
  check(manifest.runtime.narrative_architecture?.d04_plot_admissions === c.architecture.d04_plot_admissions.path && manifest.runtime.narrative_architecture?.d05_approval_queue === c.architecture.d05_approval_queue.path && manifest.runtime.narrative_architecture?.d06 === c.architecture.d06.path && manifest.runtime.narrative_architecture?.d07 === c.architecture.d07.path && manifest.runtime.narrative_architecture?.d08 === c.architecture.d08.path && manifest.runtime.narrative_architecture?.d09 === c.architecture.d09.path, 'manifest current D04-D09 pointers mismatch');
  check(manifest.runtime.narrative_architecture?.d10_schema_registry === c.architecture.d10_schema_registry.path && manifest.runtime.narrative_architecture?.d10_role_adapters === c.architecture.d10_role_adapters.path && manifest.runtime.narrative_architecture?.d10_validator === c.architecture.d10_validator.path && manifest.runtime.narrative_architecture?.d10_results === c.architecture.d10_results.path, 'manifest current D10 pointers mismatch');
  check(manifest.runtime.narrative_architecture?.d11_cases === c.architecture.d11_cases.path && manifest.runtime.narrative_architecture?.d11_results === c.architecture.d11_results.path && manifest.runtime.narrative_architecture?.d11_review === c.architecture.d11_review.path, 'manifest current D11 pointers mismatch');
  check(manifest.runtime.narrative_architecture?.promotion_inventory === c.architecture.promotion_inventory.path, 'manifest promotion inventory pointer mismatch');
  for (const [k, r] of Object.entries(c.architecture)) {
    const current = manifest.runtime.narrative_architecture?.blob_refs?.[k];
    check(current?.path === r.path && current?.blob_sha === r.blob_sha, `manifest architecture pin mismatch: ${k}`);
  }
  check(c.architecture.player_authorization.path === c.activation.authorization.path && c.architecture.d07.path === c.activation.truth_package.path, 'cycle architecture refs disagree with activation refs');
  check(/^novydres\/runtime\/orchestration\/ORCHESTRATION_CONTRACT_V[0-9]+\.md$/.test(c.activation.architecture_contract?.path ?? ''), 'activation contract archive reference is invalid');
  validateManifestReadiness(manifest, c);
  const prep = manifest.runtime.current_m3_01_preparation;
  check(prep?.preparation_id === c.plan.preparation_id && prep.dossier?.path === c.plan.dossier.path && prep.dossier?.blob_sha === c.plan.dossier.blob_sha && prep.sidecar?.path === c.plan.sidecar.path && prep.sidecar?.blob_sha === c.plan.sidecar.blob_sha, 'manifest current M3.01 preparation path/blob mismatch');
  check(prep.reviewed_against_event_id === c.plan.reviewed_against_event_id || c.plan.reviewed_against_event_id === null && prep.reviewed_against_event_id === null, 'manifest preparation review cursor mismatch');
  check(prep.story_preparation_ready === c.operational_gates.story_preparation_ready && prep.scene_ready === c.operational_gates.scene_ready && prep.narrator_permission === c.operational_gates.narrator_permission, 'manifest preparation gate mismatch');
  check(manifest.runtime.mechanical_gate_matrix_current === c.operational_gates.mechanical_matrix_ref.path && manifest.runtime.mechanical_gate_matrix_blob_sha === c.operational_gates.mechanical_matrix_ref.blob_sha, 'manifest mechanical matrix pin mismatch');
  const xp = c.operational_gates.mechanical_sources.xp_envelope, settlement = c.operational_gates.mechanical_sources.settlement_record;
  check(manifest.runtime.xp_policy_envelope_current === xp.path && manifest.runtime.xp_economy.envelope_ref === xp.path && manifest.runtime.xp_economy.envelope_blob_sha === xp.blob_sha, 'manifest XP envelope path/blob mismatch');
  check(manifest.runtime.xp_economy.settlement_record_ref === settlement.path && manifest.runtime.xp_economy.settlement_record_blob_sha === settlement.blob_sha, 'manifest XP settlement path/blob mismatch');
  check(live.last_confirmed_event_id === c.checkpoint.last_event_id && live.scene?.status === 'CLOSED' && live.scene?.last_event_id === c.checkpoint.last_event_id, 'LIVE/cycle mismatch');
  check(new RegExp(`(?:^|[-_])${c.checkpoint.last_closed_scene}(?:[-_]|$)`).test(live.scene.scene_id), 'LIVE scene cursor mismatch');
  check(live.character?.mortal === c.checkpoint.mortal && live.stage?.embrace_occurred === c.checkpoint.embrace_occurred, 'LIVE mortality/Embrace mismatch');
  const envelope = json(root, xp.path), settlementRecord = json(root, settlement.path);
  for (const k of ['xp_total', 'xp_spent', 'xp_remaining', 'xp_credit_available']) check(live.character.resources[k] === envelope.current[k] && live.character.resources[k] === settlementRecord.final[{xp_total:'cap',xp_spent:'spent',xp_remaining:'remaining',xp_credit_available:'available'}[k]], `LIVE/envelope/settlement ${k} mismatch`);
  const sourceIndex = json(root, c.architecture.d12_mechanical_source_refs.path);
  const indexedSources = Object.fromEntries(sourceIndex.source_refs.map(x => [x.id, x]));
  for (const k of MECHANICAL_SOURCES) {
    const source = indexedSources[SOURCE_INDEX_IDS[k]], cycleSource = c.operational_gates.mechanical_sources[k];
    check(source?.path === cycleSource.path && source?.blob_sha === cycleSource.blob_sha, `D12 mechanical source index mismatch: ${k}`);
  }
  check(sourceIndex.state_checkpoint.last_event_id === c.checkpoint.last_event_id && sourceIndex.state_checkpoint.last_closed_scene === c.checkpoint.last_closed_scene && sourceIndex.state_checkpoint.next_scene === `${c.checkpoint.next_scene} NOT_STARTED`, 'D12 mechanical source index checkpoint mismatch');
  check(manifest.runtime.operational_entry_current?.path === c.architecture.agent_entry.path && manifest.runtime.operational_entry_current?.blob_sha === c.architecture.agent_entry.blob_sha && manifest.runtime.context_gateway_current?.path === c.architecture.context_gateway.path && manifest.runtime.context_gateway_current?.blob_sha === c.architecture.context_gateway.blob_sha, 'manifest operational entry/context gateway pins mismatch');
  const activationRecord = json(root, c.activation.d07_activation.path);
  validateD07RuntimeActivation(activationRecord, c.activation.d07_activation, c.activation.truth_package, c.activation.authorization);
  check(manifest.runtime.d07_activation_current?.path === c.activation.d07_activation.path && manifest.runtime.d07_activation_current?.blob_sha === c.activation.d07_activation.blob_sha, 'manifest D07 activation pin mismatch');
  validatePreparation(root, c);
  validatePublicPromptDisclosure(root, c);
  return { manifest, live };
}

function validatePreparation(root, c) {
  if (c.plan.validity === 'STALE') return;
  const dossier = json(root, c.plan.dossier.path), sidecar = json(root, c.plan.sidecar.path);
  validateDocumentAgainstSchema(root, c.architecture.preparation_dossier_schema, dossier, 'dossier');
  validateDocumentAgainstSchema(root, c.architecture.preparation_sidecar_schema, sidecar, 'sidecar');
  const sourceCycleBytes = read(root, c.previous_cycle.path);
  check(blob(sourceCycleBytes) === c.previous_cycle.blob_sha, 'preparation immediate predecessor blob mismatch');
  const sourceCycle = JSON.parse(sourceCycleBytes.toString('utf8'));
  const dossierCheckpoint = dossier.source_checkpoint, sidecarCheckpoint = sidecar.source_checkpoint;
  check(dossierCheckpoint?.cycle_path === sidecarCheckpoint?.cycle_path && dossierCheckpoint?.cycle_blob_sha === sidecarCheckpoint?.cycle_blob_sha, 'dossier/sidecar source cycle pins disagree');
  check(dossierCheckpoint?.manifest_path === sidecarCheckpoint?.manifest_path && dossierCheckpoint?.manifest_blob_sha === sidecarCheckpoint?.manifest_blob_sha, 'dossier/sidecar source manifest pins disagree');
  verify(root, { path: dossierCheckpoint.manifest_path, blob_sha: dossierCheckpoint.manifest_blob_sha }, 'preparation source manifest');
  const sourceManifest = json(root, dossierCheckpoint.manifest_path);
  validatePreparationSourceCheckpoint(dossierCheckpoint, sourceCycle, sourceManifest, c, 'dossier', dossier);
  validatePreparationSourceCheckpoint(sidecarCheckpoint, sourceCycle, sourceManifest, c, 'sidecar', sidecar);
  check(dossier.preparation_id === c.plan.preparation_id && sidecar.preparation_id === c.plan.preparation_id, 'preparation id mismatch');
  for (const [label, doc] of [['dossier', dossier], ['sidecar', sidecar]]) {
    check(Array.isArray(doc.source_refs), `${label} source refs missing`);
    for (const ref of doc.source_refs) verify(root, ref, `${label} source ${ref.path}`);
    const cp = doc.source_checkpoint;
    check(cp?.last_event_id === c.checkpoint.last_event_id || cp?.last_confirmed_event_id === c.checkpoint.last_event_id, `${label} is not anchored to the real event`);
    check(cp?.last_closed_scene === c.checkpoint.last_closed_scene && cp?.next_scene_status === c.checkpoint.next_scene_status, `${label} scene cursor mismatch`);
    validatePreparationCheckpoint(cp, c, label);
    check(cp?.protagonist_mortal === c.checkpoint.mortal && cp?.embrace_occurred === c.checkpoint.embrace_occurred, `${label} mortality/Embrace mismatch`);
    for (const k of ['d04_plot_admissions', 'd06', 'd07', 'd08', 'd09']) {
      const ref = doc.source_refs.find(x => x.path === c.architecture[k].path);
      check(ref?.blob_sha === c.architecture[k].blob_sha, `${label} does not pin current architecture: ${k}`);
    }
  }
  const dref = sidecar.source_checkpoint.dossier_path === c.plan.dossier.path && sidecar.source_checkpoint.dossier_blob_sha === c.plan.dossier.blob_sha;
  check(dref, 'sidecar does not pin the exact dossier blob');
  check(dossier.review_basis?.reviewed_against_event_id === c.plan.reviewed_against_event_id && sidecar.source_checkpoint.last_event_id === c.plan.reviewed_against_event_id, 'preparation review event mismatch');
  if (c.status === 'PROVOCATION_CLOSURE_PENDING') {
    for (const [label, doc] of [['dossier', dossier], ['sidecar', sidecar]]) {
      validateOpenQuietHandoff(doc, label);
    }
    check(dossier.story_preparation_ready === false && sidecar.story_preparation_ready === false, 'closure handoff claims story preparation readiness');
  } else if (c.status === 'READY_FOR_NARRATOR') {
    for (const [label, doc] of [['dossier', dossier], ['sidecar', sidecar]]) {
      check(doc.story_preparation_ready === true && doc.scene_ready === true && doc.SCENE_READY === true && doc.NARRATOR_PERMISSION === true, `${label} does not independently attest scene readiness`);
      check(Array.isArray(doc.handoff?.prepared_scenes) && doc.handoff.prepared_scenes.length > 0, `${label} has no prepared scene`);
    }
  }
}

const V9_TO_V10_RUNTIME_MIGRATION = Object.freeze({
  orchestration_contract: 'novydres/runtime/orchestration/ORCHESTRATION_CONTRACT_V8.md',
  cycle_schema: 'novydres/runtime/orchestration/CYCLE_SCHEMA_V10.json',
  cycle_validator: 'novydres/runtime/orchestration/ORCHESTRATION_VALIDATOR_V10.mjs',
  cycle_tests: 'novydres/runtime/orchestration/ORCHESTRATION_TESTS_V10.mjs',
  cycle_schema_tests: 'novydres/runtime/orchestration/ORCHESTRATION_SCHEMA_TESTS_V10.py',
  preparation_sidecar_schema: 'novydres/runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V6.json',
  start_here: 'novydres/runtime/orchestration/START_HERE_V7.md'
});

export function validateV9ToV10ClosureMigration(c, prev) {
  check(prev?.schema_id === 'NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V9' && c?.schema_id === 'NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V10', 'migration must advance exactly V9 to V10');
  const allowed = new Set(Object.keys(V9_TO_V10_RUNTIME_MIGRATION));
  const previousKeys = Object.keys(prev.architecture ?? {}).sort(), currentKeys = Object.keys(c.architecture ?? {}).sort();
  check(JSON.stringify(previousKeys) === JSON.stringify(currentKeys), 'migration changed the architecture key set');
  for (const key of previousKeys) {
    const before = prev.architecture[key], after = c.architecture[key];
    if (allowed.has(key)) {
      check(after?.path === V9_TO_V10_RUNTIME_MIGRATION[key] && /^[0-9a-f]{40}$/.test(after?.blob_sha ?? ''), `migration runtime pin mismatch: ${key}`);
    } else {
      check(after?.path === before?.path && after?.blob_sha === before?.blob_sha, `migration changed non-runtime architecture pin: ${key}`);
    }
  }
  const activationKeys = Object.keys(prev.activation ?? {}).sort();
  check(JSON.stringify(activationKeys) === JSON.stringify(Object.keys(c.activation ?? {}).sort()), 'migration changed the activation evidence key set');
  for (const key of activationKeys) {
    check(c.activation[key]?.path === prev.activation[key]?.path && c.activation[key]?.blob_sha === prev.activation[key]?.blob_sha, `migration rewrote historical activation evidence: ${key}`);
  }
  const closureCandidate = { ...c, architecture: prev.architecture };
  const result = validateClosureRecommendationTransition(closureCandidate, prev);
  return { ...result, migration: 'V9_TO_V10_RUNTIME_CONTRACT_ONLY', updated_runtime_pins: [...allowed] };
}

function validateTransition(root, c, prev) {
  if (c.transition === 'OPERATIONAL_ACTIVATED') return validateActivationTransition(c, prev);
  if (['PLAN_REVISED', 'PLAN_REVALIDATED'].includes(c.transition)) return validateDramaturgoTransition(c, prev);
  if (c.transition === 'CLOSURE_RECOMMENDED') {
    if (prev.schema_id === 'NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V9') return validateV9ToV10ClosureMigration(c, prev);
    return validateClosureRecommendationTransition(c, prev);
  }
  if (c.transition === 'BLOCKED') return validateBlockedTransition(c, prev);
  if (c.transition === 'SCENE_COMMITTED') {
    const live = json(root, c.refs.live.path), episodeText = read(root, c.refs.episode.path).toString('utf8');
    return validateSceneCommittedTransition(c, prev, { live, episodeText });
  }
  fail('unsupported V10 transition');
}

function validateV10Predecessor(root, c, prev, ppath) {
  check(c.previous_cycle?.path === ppath && blob(read(root, ppath)) === c.previous_cycle.blob_sha, 'previous cycle path/blob');
  if (prev.schema_id === 'NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V10') {
    const pprevPath = cyclePath(prev.sequence - 1), pprev = json(root, pprevPath);
    verifyCyclePins(root, prev, ppath);
    validateV10Predecessor(root, prev, pprev, pprevPath);
    validateTransition(root, prev, pprev);
  } else if (prev.schema_id === 'NOVYDRES_CHR001_ORCHESTRATION_CYCLE_V9') {
    validateCommittedV9Baseline(root, c.source_head_sha, prev, c.previous_cycle.blob_sha);
  } else fail('unsupported predecessor schema');
}

function validatePublishedCommitPins(root, c, cpath, commit) {
  const pins = [
    { path: cpath, blob_sha: blob(read(root, cpath)), label: 'current cycle' },
    { ...c.manifest_ref, label: 'manifest' },
    ...Object.entries(c.refs).map(([key, ref]) => ({ ...ref, label: `state.${key}` })),
    ...Object.entries(c.architecture).map(([key, ref]) => ({ ...ref, label: `architecture.${key}` })),
    ...Object.entries(c.activation).map(([key, ref]) => ({ ...ref, label: `activation.${key}` })),
    { ...c.plan.dossier, label: 'preparation.dossier' },
    { ...c.plan.sidecar, label: 'preparation.sidecar' },
    { ...c.operational_gates.mechanical_matrix_ref, label: 'mechanical matrix' },
    { ...c.architecture.d12_mechanical_source_refs, label: 'mechanical source index' },
    ...Object.entries(c.operational_gates.mechanical_sources).map(([key, ref]) => ({ ...ref, label: `mechanical.${key}` }))
  ];
  const seen = new Set();
  for (const pin of pins) {
    const key = `${pin.path}:${pin.blob_sha}`;
    if (seen.has(key)) continue;
    seen.add(key);
    const treeBlob = execGit(root, ['rev-parse', `${commit}:${pin.path}`]);
    check(treeBlob === pin.blob_sha, `published commit does not contain exact ${pin.label} pin: ${pin.path}`);
  }
  return { ok: true, commit, checked_blob_pins: seen.size };
}

function validateCommittedV9Baseline(root, sourceHead, expectedCycle, expectedBlob) {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'novydres-v9-baseline-'));
  try {
    const sourceRepo = execGit(root, ['rev-parse', '--show-toplevel']);
    const clone = spawnSync('git', ['clone', '--quiet', '--shared', '--no-checkout', sourceRepo, temp], { encoding: 'utf8', maxBuffer: 4 * 1024 * 1024 });
    check(!clone.error && clone.status === 0, `could not create detached V9 baseline checkout: ${(clone.stderr || clone.error?.message || '').trim()}`);
    execGit(temp, ['checkout', '--quiet', '--detach', sourceHead]);
    const committedCycleBytes = read(temp, cyclePath(expectedCycle.sequence));
    check(blob(committedCycleBytes) === expectedBlob, 'detached V9 baseline cycle blob does not match predecessor');
    const result = validateLatestV9(temp);
    check(result.ok && result.cycle_id === expectedCycle.cycle_id && result.status === 'READY_FOR_DRAMATURGO' && result.transition === 'OPERATIONAL_ACTIVATED', 'committed V9 baseline is not the expected activated Dramaturgo checkpoint');
  } finally {
    fs.rmSync(temp, { recursive: true, force: true });
  }
}

export function validateLatestV10(root = process.cwd()) {
  const dir = path.resolve(root, 'novydres/chronicles/CHR-001/orchestration');
  const versions = fs.readdirSync(dir).map(n => /^CYCLE_V(\d{4})\.json$/.exec(n)).filter(Boolean).map(m => Number(m[1])).sort((a, b) => b - a);
  check(versions.length > 0, 'no cycle files');
  const n = versions[0], cpath = cyclePath(n), c = json(root, cpath);
  const ppath = cyclePath(n - 1), prev = json(root, ppath);
  check(c.previous_cycle?.path === ppath, 'previous cycle path');
  const head = execGit(root, ['rev-parse', 'HEAD']), parentHead = execGit(root, ['rev-parse', 'HEAD^']);
  check(c.source_head_sha === head || c.source_head_sha === parentHead, 'source_head is neither current precommit HEAD nor verified first parent');
  const publication = c.source_head_sha === parentHead ? validatePublishedCommitPins(root, c, cpath, head) : null;
  verifyCyclePins(root, c, cpath);
  validateV10Predecessor(root, c, prev, ppath);
  const transition = validateTransition(root, c, prev);
  return { ok: true, cycle_id: c.cycle_id, transition: c.transition, status: c.status, next_role: c.next_role, last_event_id: c.checkpoint.last_event_id, gates: c.operational_gates, transition_validation: transition, publication };
}

function execGit(root, args) {
  const p = spawnSync('git', ['-C', root, ...args], { encoding: 'utf8' });
  if (p.status !== 0) fail(`git ${args.join(' ')} failed`);
  return p.stdout.trim();
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname)) {
  try { const i = process.argv.indexOf('--root'); console.log(JSON.stringify(validateLatestV10(path.resolve(i < 0 ? process.cwd() : process.argv[i + 1])))); }
  catch (e) { console.error(String(e)); process.exitCode = 1; }
}
