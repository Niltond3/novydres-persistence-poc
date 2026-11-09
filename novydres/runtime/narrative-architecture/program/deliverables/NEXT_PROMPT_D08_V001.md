# NOVYDRES CHR-001 · DRAMATURGO — FASE D08

Continue the persisted D05→D12 program from `CHR001_D05-D12_RUN_STATE.json`; do not restart completed phases.

## Repository and branch
- Repository: `Niltond3/novydres-persistence-poc`
- Clone: `/home/nilton_neto/Documentos/Backup/Notas/Personal Stuffs/RPG stuffs/NOVYDRES/Repository`
- Documentary branch only: `design/chr001-narrative-program-d01`
- Read the live branch HEAD and `master` before work. Never edit `master`. If HEAD differs from D07 handoff, reconcile and revalidate.

## D07 advancement gate
- Before any D08 design work, verify `HANDOFF_D07_V001.json` and `AUDIT_D07_V001.json` have gate `PASS` or `PASS_WITH_UNKNOWN`, and verify the local run manifest records the output commit, parent, tree, each artifact blob SHA, exact content readback, and unchanged `master`.
- If the gate is pending/failed or any readback evidence is absent, do not begin D08. Resume D07 audit/remediation and publication verification first.

## Required inputs
Read current governance and D07 artifacts by exact published blob SHA from the D07 handoff/run manifest: `D07_PLOT_BIBLES_V001.json`, `D07_TRUTH_LOCKS_V001.json`, `D07_PLAYER_APPROVAL_QUEUE_V001.json`, `AUDIT_D07_V001.json`, and `HANDOFF_D07_V001.json`. Re-read current cycle/manifest before proposing any scene.

## D08 mandate
Design optional stories, provocations, internal acts, conditional scenes and beats, with entry/exit gates, stakes, knowledge limits, NPC autonomy, consequences, refusal, failure and verifiable local endings. A story must be escapable and end locally even if a cross-story plot remains open.

## Boundaries
- No new scene starts; do not narrate C06 or change cycle/event state.
- No writing future player choices or dialogue; no forced sequence or required plot.
- Do not reopen closed scenes or turn editorial backlog into events.
- PC01 remains conditional/editorial. Its report-authorship investigation is blocked unless effective GM-hidden segregation is verified or the player first approves an open variant. Do not invent answers, clues, culprits, motives or NPC knowledge.
- PC02–PC04 remain candidates only.
- Preserve D05 pointer conflict, D06 target choice, provenance errata, UNKNOWNs and every pending approval.
- No retcon, canon change, mechanics grant, operational promotion, scene readiness or Narrator permission.

## Deliverables and gate
Create only proposed, PLAYER_SAFE, versioned D08 artifacts in `deliverables/`. Include reproducible validation, negative/adversarial cases, independent review, audit and handoff. Record exact source paths and blob SHAs. Gate honestly; use `PASS_WITH_UNKNOWN` only where limitations are explicit and do not make a blocked mystery playable. Publish only after review, then verify commit, parent, tree, every blob and exact readback; record results in the local manifest.
