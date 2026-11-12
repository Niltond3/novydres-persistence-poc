# NOVYDRES / CHR-001 — ORCHESTRATION CONTRACT V7

Status: successor to `ORCHESTRATION_CONTRACT_V6.md`. V7 becomes operational only when the numerically latest valid cycle and its current manifest pin the exact V7 contract, V9 cycle schema, V9 validator, both V9 test suites, V6 dossier schema, V5 sidecar schema, and V6 entrypoint listed below. A filename or version label alone does not establish authority. This contract does not amend canon, prior events, player decisions, character resources, or approved narrative outcomes.

Entrypoint: `novydres/runtime/orchestration/START_HERE_V6.md`. The current manifest entrypoint and cycle `architecture.start_here` pin must identify that exact path and its Git blob.

Bootstrap authority is deliberately two-stage. The repository's required legacy `.AGENT.md` and `.CONTEXTG.md` are discovery-only entry files: use them only to locate this repository and the CHR-001 orchestration directory. Their embedded Drive links, historical checkpoint, role instructions, and old campaign state are not current authority. Locate and validate the numerically latest cycle, its complete predecessor/blob chain, and the exact manifest it pins. Then read and verify only the cycle-and-manifest-pinned `novydres/.AGENT_V4.md` and `novydres/.CONTEXTG_V3.md` as the active operational entry and context gateway. A missing, stale, or mismatched pin for either file blocks work; do not combine their instructions with the legacy checkpoint.

## Authority, pins, and disclosure

Resolve the latest cycle by numeric sequence. Validate its schema, exact Git blob pins, predecessor chain, and pinned manifest before trusting its role or status. The cycle and manifest must agree on every operational gate, pending decision, next-scene cursor, test path/blob, and current architecture blob reference. The manifest must pin these exact files:

| Key | Required path |
|---|---|
| `orchestration_contract` | `novydres/runtime/orchestration/ORCHESTRATION_CONTRACT_V7.md` |
| `cycle_schema` | `novydres/runtime/orchestration/CYCLE_SCHEMA_V9.json` |
| `cycle_validator` | `novydres/runtime/orchestration/ORCHESTRATION_VALIDATOR_V9.mjs` |
| `cycle_tests` | `novydres/runtime/orchestration/ORCHESTRATION_TESTS_V9.mjs` |
| `cycle_schema_tests` | `novydres/runtime/orchestration/ORCHESTRATION_SCHEMA_TESTS_V9.py` |
| `preparation_dossier_schema` | `novydres/runtime/provocation-prep/PROVOCATION_DOSSIER_SCHEMA_V6.json` |
| `preparation_sidecar_schema` | `novydres/runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V5.json` |
| `start_here` | `novydres/runtime/orchestration/START_HERE_V6.md` |
| `agent_entry` | `novydres/.AGENT_V4.md` |
| `context_gateway` | `novydres/.CONTEXTG_V3.md` |
| `player_authorization` | `novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_AGENT_ACCESS_V004.json` |
| `d07_activation_record` | `novydres/runtime/narrative-architecture/program/deliverables/D07_ACTIVATION_V004_PLAYER_SAFE.json` |

The manifest's corresponding `runtime.narrative_architecture.blob_refs` entries, including `agent_entry`, `context_gateway`, `player_authorization`, and `d07_activation_record`, must match the cycle path and blob SHA exactly. `runtime.operational_entry_current` and `runtime.context_gateway_current` must independently match the exact V4/V3 paths and blobs. Its `runtime.orchestration` fields `contract`/`contract_blob_sha`, `cycle_schema`/`cycle_schema_blob_sha`, `validator`/`validator_blob_sha`, `tests`/`tests_blob_sha`, `schema_tests`/`schema_tests_blob_sha`, and `entrypoint`/`entrypoint_blob_sha` must also match those exact pins. The cycle `activation.authorization` ref must pin decision V004; the activation record's `authorization_ref` must match that exact blob. The cycle `activation.d07_activation` ref and manifest `runtime.d07_activation_current` ref must pin the exact V004 activation record. The V9 validator rejects missing or stale authorization/activation blob refs and stale version paths even when the manifest and cycle agree with each other.

Creating or validating `D07_ACTIVATION_V004_PLAYER_SAFE.json` alone does not activate D07 at runtime. `D07_ACTIVE` is established only when a valid, PASS-gated cycle and its current manifest pin the same V004 blob and the record confirms its runtime activation fields and V004 authorization reference.

Load the live state, history index, episode, character, NPC knowledge, open threads, D04–D12 architecture, D07, D08, preparation, and mechanical evidence only from verified pins. Authorized agents may read hidden project material for their work; public text must remain player-safe. The prompt checker rejects a long exact phrase copied from pinned D06–D08 sources. This is a literal-overlap screen and does not replace a player-safe review for paraphrase or implication.

## Transitions and open-plot routing

Every transition is a separate copy-on-write update to `master`, guarded by the expected old SHA and followed by readback. The cycle is the operational cursor.

- `OPERATIONAL_ACTIVATED → READY_FOR_DRAMATURGO` confirms architecture and D07 activation. It preserves the current provocation, event, scene cursor, and source state; the plan remains stale and all scene and narrator gates stay false.
- `PLAN_REVISED` or `PLAN_REVALIDATED → READY_FOR_NARRATOR` is allowed only after a valid Dramaturgo review against the exact latest real event and every readiness gate passes.
- `CLOSURE_RECOMMENDED → PROVOCATION_CLOSURE_PENDING` is a routing recommendation to the player. It does **not** close M3.01, record a player choice, start C06, or authorize the Narrator. M3.01 remains `OPEN`; C06 remains `NOT_STARTED`; the last event and all state/resource/knowledge cursors remain unchanged. The pending decision offers keeping the route open and quiet, continuing only after an admitted and available cause, or requesting alternate closure explicitly. No default closure is permitted; inaction preserves the open quiet route.
- `SCENE_COMMITTED → READY_FOR_DRAMATURGO` requires actual play, G28 persistence, and verified readback.
- `BLOCKED → BLOCKED_CONFLICT` records a specific source, authority, or technical failure.

Every transition preserves `provocation_id`. Preparation, simulation, review, and validation do not create events, outcomes, state changes, XP/FV changes, NPC knowledge changes, or elapsed time. The plan can remain open without an actionable scene when no cause is admitted and available; do not manufacture a cause, contact, arrival, location, or invitation to fill a scene slot.

## Independent gates and preparation provenance

The V004 record must identify `D07_RUNTIME_TRUTH_PACKAGE` activation, report `runtime_activation.d07_active=true`, and pin the exact D07 truth package and V004 authorization. This proves D07 runtime activation only; it does not imply scene readiness or Narrator permission. Record `ARCHITECTURE_ACTIVE`, `D07_ACTIVE`, `STORY_PREPARATION_READY`, `MECHANICAL_SCENE_READY`, `SCENE_READY`, and `NARRATOR_PERMISSION` independently in the cycle and manifest. The legacy `next_scene_executable` mirrors only `SCENE_READY`. Mechanical scene readiness is distinct from future Embrace eligibility and final 2010 sheet certification.

A non-stale dossier and sidecar must pin the exact immediate predecessor cycle and its manifest blob, source head, last real event, scene cursor, mortality/Embrace state, and all six operational source refs: LIVE, history index, episode, character state, NPC knowledge, and open threads. Their `source_refs` must include those exact path/blob pairs. The source manifest must resolve the same predecessor and agree on event, role, status, and scene cursor. The sidecar must pin the exact dossier blob. Preparation schemas are verified by the cycle's fixed V6/V5 schema refs at runtime.

A closure-routing preparation must explicitly leave M3.01 open and state that no event, scene, time, resource, or NPC-knowledge delta was created. It must retain the available quiet/open choice and keep scene readiness, narrator permission, cause, actors, entry conditions, stakes, and prepared-scene list false/empty where no cause exists. A pending player choice is not evidence that the player has chosen.

## Narrator handoff

Only a valid `READY_FOR_NARRATOR` cycle permits a handoff, and the player must still send the final prompt to start a scene. For that status the pinned D12 candidate must contain a nonempty public narrator prompt. For activation, Dramaturgo review, closure routing, or blocked status, a missing prompt is valid because narration is not ready and no Narrator handoff is authorized. A closure recommendation never auto-closes M3.01; absent a recorded player choice, the route stays open and quiet. The prompt must contain no hidden truth or unrevealed narrative content; the Narrator loads authorized material directly from verified repository sources.

G28 closes an actually played scene only. A declined or unavailable opportunity is not repeated without a distinct real cause. Do not start C06 during Dramaturgo preparation.

## Discovery and validation

`START_HERE_V6.md` is the discovery entrypoint after the required legacy bootstrap. The cycle and manifest pin the exact files listed above. Run `node --test novydres/runtime/orchestration/ORCHESTRATION_TESTS_V9.mjs` and `python3 novydres/runtime/orchestration/ORCHESTRATION_SCHEMA_TESTS_V9.py <repo-root>` against the same checkout whose blobs are pinned. Synthetic transition fixtures are tests only, never events or operational cycles. These checks do not replace narrative sufficiency review, mechanical adjudication, player decision, promotion, or readback.
