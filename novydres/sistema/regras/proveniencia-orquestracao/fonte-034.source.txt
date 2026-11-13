# NOVYDRES / CHR-001 — ORCHESTRATION CONTRACT V10

Status: successor of V9 for a **new, strictly administrative** transition after the validated episodic closure of M3.01. Activated only by highest numerically valid CYCLE_V0038 and its exact MANIFEST_V53 pins. V9 and C37 remain immutable historical authority. Nothing here creates a played event, changes canonical history, determines a protagonist action, or permits narration.

## Preconditions
- Recheck master SHA, highest sequence C37 and its complete predecessor SHA chain; check exact C37/MANIFEST_V52 blob pins.
- Match six carried refs, last event `CHR001-M301-C05-22-20261109-001`, mortal/Embrace flags, OPEN_THREADS_V23 and mechanical resources. No C06 or M3.02 scene played.
- D04 V010 independently admits PLOT-GANGREL-ATTENTION. D06 V031 / D07 V018 / D08 V021 author separate M3.02; the old C06 reentry has no admitted cause, cannot be reused or renamed. New authored prospective preparation must be source-pinned and independently tested.
- The user's 2026-11-11 authorization permits prospective planning and next administrative opening only after mandatory validators actually execute successfully. It expressly excludes scene initiation.

## Single supported transition
`C37 PROVOCATION_EPISODE_CLOSED/NONE/M3.01` to `C38 NEXT_PROVOCATION_ADMIN_OPENED/READY_FOR_DRAMATURGO/M3.02`.
C38 retains exactly C37 last event, six state blobs, knowledge/thread state, mortality and mechanics; last closed scene refers to M3.01.C05, new scene cursor M3.02.C01 NOT_STARTED with pending persistence false. The C37 episodic closure remains historical and is not reopened. Set `next_role=DRAMATURGO` for new prospective review and `SCENE_READY=false`, `NARRATOR_PERMISSION=false`, `mechanical_scene_ready=false`. The D04 target and D09 guided-creation route remain PENDING.
- Planned source of conflict: independent, future, specific causal entry admitted by D04 and bounded by D07/D08. Initial situation must be **actually established during separately authorized play**; administrative opening alone cannot create its unloading, obstacle, contact, scene, travel, time or NPC knowledge.
- If source causality absent, M3.02 remains ADMIN_OPENED, C01 NOT_STARTED and no narration is permitted. Do not force an offer, encounter, delivery, player attendance or target outcome.
- XP and FV are not awarded, spent or refreshed by this transition. Future skill checks obey G25/G27 and applied rules; no fabricated RNG or unapproved power.

## Verification
The companion `CYCLE_SCHEMA_V12.json`, `ORCHESTRATION_VALIDATOR_V12.mjs`, `ORCHESTRATION_TESTS_V12.mjs`, `ORCHESTRATION_SCHEMA_TESTS_V12.py`, and the M3.02 V7 preparation schemas are successors dedicated to C37→C38. All must execute on the exact candidate checkout; GitHub remote CI is acceptable when its run and results are inspected. Passing syntactic/authorial checks is separate from scene readiness and from a protected master publication/readback.
Required:
```sh
node --test novydres/runtime/orchestration/ORCHESTRATION_TESTS_V12.mjs
python3 novydres/runtime/orchestration/ORCHESTRATION_SCHEMA_TESTS_V12.py .
node novydres/runtime/orchestration/ORCHESTRATION_VALIDATOR_V12.mjs --root .
```
No new scene authorization can use this V12 validator automatically. A later scene-opening transition needs separate actual causality and independently validated successor authority. Publishing C38 uses a single Git tree/commit and expected old master SHA, with readback.
