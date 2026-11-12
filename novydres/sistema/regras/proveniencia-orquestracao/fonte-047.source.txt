# NOVYDRES / CHR-001 — ORCHESTRATION CONTRACT V9

Status: successor to `ORCHESTRATION_CONTRACT_V8.md`. It becomes operational only when the numerically latest valid cycle and its current manifest pin the exact V9 contract, V11 cycle schema/validator/tests, V11 schema tests and V8 entrypoint. A version label alone does not establish authority. This contract does not amend canon, prior events, character resources, knowledge or played outcomes.

## Authority and bootstrap

Use `START_HERE_V8.md` after the required discovery-only `novydres/.AGENT.md` and `novydres/.CONTEXTG.md`. Resolve the highest numeric cycle, validate its schema, exact blob pins, predecessor chain and manifest before trusting its role or status. Then use only cycle-and-manifest-pinned `.AGENT_V4.md` and `.CONTEXTG_V3.md` as active operational authority. Missing or mismatched pins block work.

The active cycle and manifest must agree on all operational gates, pending decision, scene cursor, runtime paths and current architecture blobs. Preserve the V004 authorization and D07 activation record as exact historical/runtime evidence. D07 activation grants access to the truth package only; it does not grant scene readiness or Narrator permission.

## Fixed runtime paths

| Key | Required path |
|---|---|
| `orchestration_contract` | `novydres/runtime/orchestration/ORCHESTRATION_CONTRACT_V9.md` |
| `cycle_schema` | `novydres/runtime/orchestration/CYCLE_SCHEMA_V11.json` |
| `cycle_validator` | `novydres/runtime/orchestration/ORCHESTRATION_VALIDATOR_V11.mjs` |
| `cycle_tests` | `novydres/runtime/orchestration/ORCHESTRATION_TESTS_V11.mjs` |
| `cycle_schema_tests` | `novydres/runtime/orchestration/ORCHESTRATION_SCHEMA_TESTS_V11.py` |
| `preparation_dossier_schema` | `novydres/runtime/provocation-prep/PROVOCATION_DOSSIER_SCHEMA_V6.json` |
| `preparation_sidecar_schema` | `novydres/runtime/provocation-prep/PROVOCATION_LONGITUDINAL_SIDECAR_SCHEMA_V6.json` |
| `start_here` | `novydres/runtime/orchestration/START_HERE_V8.md` |

## Transition rules

- `OPERATIONAL_ACTIVATED → READY_FOR_DRAMATURGO` records architecture/D07 activation. It preserves the provocation, event, scene cursor and state; all scene and Narrator gates remain false.
- `PLAN_REVISED` or `PLAN_REVALIDATED → READY_FOR_NARRATOR` requires review against the exact latest real event and every independent readiness gate. A scene may start only after the player supplies the final handoff prompt.
- `CLOSURE_RECOMMENDED → PROVOCATION_CLOSURE_PENDING` is a recommendation only. It leaves M3.01 open, records a pending player decision, starts no scene and grants no Narrator authority.
- `EPISODIC_CLOSURE_APPROVED → PROVOCATION_EPISODE_CLOSED` is allowed only after an explicit player choice at a reconciled checkpoint. It must pin the decision receipt, preserve the immediate predecessor's event/cursor, six state refs, mechanical refs and activation evidence exactly, and preserve the persistent-thread ledger byte-for-byte. Set `next_role=NONE`, clear the pending decision, and keep preparation, mechanical scene, scene and Narrator gates false. The episode closure is not route-level `ALTERNATE` or `INCOMPLETE`, D04 target completion, graduation or `CHARACTER_READY`.
- `SCENE_COMMITTED → READY_FOR_DRAMATURGO` requires actual play, G28 persistence and verified readback.
- `BLOCKED → BLOCKED_CONFLICT` records a specific evidence-backed blocker and grants no scene authority.

The V11 validator in this release certifies the C36-to-C37 episodic-closure transition and verifies the immutable predecessor chain. A later transition requires its own validated contract/validator successor; this closed cycle grants no next role.

Every transition is copy-on-write and guarded by the expected prior commit. Review, preparation and validation create no events, outcomes, state/resource/knowledge deltas or elapsed time. Do not infer a cause, contact, arrival or NPC action to fill an empty scene slot.

## Episode boundary and carried threads

Closing an episode requires the local evidence for every story that actually started and the player's explicit choice at the reconciled boundary. It does not require resolving every world-spanning conflict. Preserve every open thread, relationship, consequence, knowledge state, uncertainty and disposition exactly as reconciled. An unstarted optional unit remains quiet/not started, not declined. Any later engagement needs a distinct authored/admitted unit, an actual cause, player choice, current state/knowledge reconciliation and separate Marco/cycle gates. Episode closure alone does not open M3.02 or authorize a scene or Narrator.

For M3.01, the approved C05-22 closure leaves C06 `NOT_STARTED`; D04 V010 still has no admitted C06 cause. The guided-creation route, its adaptation target, graduation and character readiness remain independently pending.

## Preparation and disclosure

A non-stale dossier/sidecar must pin its exact predecessor cycle and manifest, source head, last event, scene cursor, mortality/Embrace state and all six operational state refs. When the episode is closed, any earlier preparation is stale for scene execution; it cannot make a scene ready. Public output must not disclose hidden story material. A public Narrator prompt is valid only for `READY_FOR_NARRATOR` with its independent gates open.

## Validation

Against the same checkout whose blobs are pinned, run:

```sh
node --test novydres/runtime/orchestration/ORCHESTRATION_TESTS_V11.mjs
python3 novydres/runtime/orchestration/ORCHESTRATION_SCHEMA_TESTS_V11.py <repo-root>
node novydres/runtime/orchestration/ORCHESTRATION_VALIDATOR_V11.mjs --root <repo-root>
```

The V11 validator also verifies exact cycle/manifest/source blobs, transition semantics and the immutable predecessor chain. Synthetic test fixtures are never operational events. All checks remain separate from mechanical adjudication, publication approval and remote readback.
