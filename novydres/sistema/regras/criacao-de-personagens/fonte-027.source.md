---
document_id: novydres_character_creation_specialist_a_decisions
version: 0.1
status: draft_for_senior_editor_review
date: 2026-08-12
workstream: character_creation_novydres_architecture
execution_node: A
depends_on:
  - novydres_character_creation_specialist_a_v5_baseline_research_v0_1.md
  - novydres_character_creation_core_v5_baseline_v0_1.md
supersedes: null
---

# Specialist A — Decision Ledger

## 1. Decision ledger

| Decision ID | Question IDs | Decision | Status |
|---|---|---|---|
| `CHAR-A-001` | Q-014, affects Q-015 | Hybrid admission granularity: source + content family + per-option exception | APPROVED IN GRILL |
| `CHAR-A-002` | Q-014 | Official V5 character-building content has presumption of eligibility for admission review; no automatic whole-book admission | APPROVED IN GRILL |
| `CHAR-A-003` | Q-001, Q-014 | Content admission and specialized-procedure admission are independent | APPROVED IN GRILL |
| `CHAR-A-004` | Q-015 | Supersession requires evidence of revision; latest date alone is insufficient | APPROVED IN GRILL |
| `CHAR-A-005` | Q-016 | Homebrew requires complete applicable editorial gate + final Senior Editor approval | APPROVED IN GRILL |
| `CHAR-A-006` | Q-016, Q-015 | Homebrew may override official only through explicit, versioned Novydres override with preserved provenance | APPROVED IN GRILL |
| `CHAR-A-007` | Q-014, Q-015 | `PARTIAL` is aggregative composition, never pending/incomplete status | APPROVED IN GRILL |
| `CHAR-A-008` | Q-006–008, Q-011, Q-013, Q-014 | Selectable published option requires admission + standalone implementation + all other gates | APPROVED IN GRILL |
| `CHAR-A-009` | Q-001 | Common creation spine is dependency/validation graph, not rigid Core page order | APPROVED IN GRILL |
| `CHAR-A-010` | Q-002, Q-003 | Preserve all canonically equivalent Attribute/Skill allocation alternatives in common legality model | APPROVED IN GRILL |
| `CHAR-A-011` | Q-001 / architecture correction | Exactly two creation modes: `Rápido` and `Guiado`; both create PCs and NPCs | USER ADDENDUM — APPROVED |
| `CHAR-A-012` | Q-001 | Quick may be an operational subset of Guided: `QUICK ⊆ GUIDED ⊆ COMMON MODEL` | APPROVED IN GRILL |
| `CHAR-A-013` | Q-001 | Mode compatibility is separate state; Quick non-support does not make an option illegal | APPROVED IN GRILL |
| `CHAR-A-014` | Q-006–008, Q-011–013 | Global admission and per-character eligibility are separate | APPROVED IN GRILL |
| `CHAR-A-015` | Q-012 | Caitiff/Thin-Blood rarity alone does not create ineligibility or permission gate | APPROVED IN GRILL |
| `CHAR-A-016` | Q-013 | Loresheet selection never certifies truth; Revelation Architecture remains authoritative | APPROVED IN GRILL |
| `CHAR-A-017` | Q-008 | Predator Type is basal when canonically applicable; Quick cannot erase required effects | APPROVED IN GRILL |
| `CHAR-A-018` | Q-010, Q-012 | Generation and Blood Potency are required final fields; A does not set Novydres values | APPROVED IN GRILL |
| `CHAR-A-019` | Q-010 | Derived traits/state are calculated centrally; modes do not own duplicate formulas | APPROVED IN GRILL |
| `CHAR-A-020` | Q-011, Q-005, Q-006 | Clan selection resolves one active versioned mechanical profile; no free cross-version mixing | APPROVED IN GRILL |
| `CHAR-A-021` | Q-011 | `CLAN MEMBERSHIP` is a central normative reusable mechanical contract | APPROVED IN GRILL |
| `CHAR-A-022` | Q-005–008, Q-013, Q-014 | Admission does not imply initial-creation availability; acquisition context is explicit | APPROVED IN GRILL |
| `CHAR-A-023` | Q-001, Q-005–008, Q-010, Q-011, Q-013 | Published creation is compact: instructions + internal rule-home pointers; editorial machinery stays hidden | APPROVED IN GRILL |

## 2. Closure matrix — Q-001..Q-016

| Question | Closure | Basis |
|---|---|---|
| `CHAR-CREATE-Q-001` canonical starting creation sequence | CLOSED ARCHITECTURALLY | `CHAR-A-003`, `009`, `011`, `012`, `013`, `023`; common dependency spine, exactly Quick/Guided |
| `Q-002` Attributes baseline | CLOSED WITH CANON POINTER DEBT | Preserve current canonical allocation; page verification required before transcription |
| `Q-003` Skills baseline | CLOSED WITH CANON POINTER DEBT | Preserve all canonical legal distribution profiles; page verification required |
| `Q-004` Specialties | CLOSED WITH CANON POINTER DEBT | Canonical starting Specialty rule; exact current text must be page-verified |
| `Q-005` starting Disciplines | CLOSED AT INTERFACE / CANON POINTER DEBT | Canonical starting allocation + centralized option validation; exact dot text page-verify |
| `Q-006` Discipline-power selection interface | CLOSED | stable option identity + prerequisites + admission + acquisition + eligibility + central validation |
| `Q-007` Advantages/Backgrounds/Merits/Flaws | CLOSED AT INTERFACE / CANON POINTER DEBT | canonical economy; family catalogs internal; exact totals/exceptions page-verify |
| `Q-008` Predator Types | CLOSED | required when canonically applicable; source admission broad; exceptions page-verify |
| `Q-009` Convictions/Touchstones/Humanity | CLOSED AT INTERFACE / CANON POINTER DEBT | canonical moral model retained; exact current wording page-verify |
| `Q-010` derived/starting state | CLOSED ARCHITECTURALLY | central calculation; Generation/BP required final fields; exact starting-state text page-verify |
| `Q-011` clan-specific effects | CLOSED | atomic versioned clan profile + normative `CLAN MEMBERSHIP` contract |
| `Q-012` Caitiff/Thin-Blood | CLOSED AT INTERFACE / CANON POINTER DEBT | canonical distinct profiles; rarity is not a gate; exact numeric exceptions page-verify |
| `Q-013` Loresheets | CLOSED | catalog option + acquisition/eligibility; never truth certification |
| `Q-014` official source-admission cut | CLOSED | broad curated official corpus; source/family/option hybrid; not Core+PG exclusivity |
| `Q-015` supersession/errata | CLOSED | semantic precedence; errata/revision evidence; stable identity; conflict review |
| `Q-016` homebrew admission | CLOSED | candidate→gate→Senior Editor approval; explicit overrides only |

## 3. Official source-admission matrix — decision form

This is the operative policy summary; detailed research remains in the Specialist A research artifact.

| Source class | Default treatment |
|---|---|
| Current Core | baseline authority; `ADMITTED` |
| Player's Guide | major consolidation/expansion; relevant character-building families admitted subject to option exceptions |
| Earlier official source whose option is reprinted later | preserve provenance; resolve one stable identity; do not duplicate |
| Official source with only some character-building material | source aggregate normally `PARTIAL`; admit relevant families, exclude/defer unrelated families |
| Specialized creation procedure | separate procedure classification; never imported solely because source content is admitted |
| Antagonist-only material | not selectable by default |
| Future official V5 character-building material | mandatory admission review; no corpus freeze |
| Homebrew/local | candidate until full applicable gate + Senior Editor approval |

## 4. A → B/C/J1 interface ledger

### A → B
Must consume:
- common character model;
- required Generation/BP fields;
- Generation/BP constraint interface;
- no age→power automatic inference;
- *In Memoriam* as canonical research input for older-character/Ancilla procedure questions.

B owns:
- local starting envelopes;
- local Generation/BP values by envelope;
- age/era power-envelope decisions.

### A → C
Must consume:
- admission vs eligibility separation;
- `CLAN MEMBERSHIP`;
- Caitiff/Thin-Blood rarity-not-gate invariant;
- Loresheet Revelation boundary.

C may add:
- local contextual eligibility where authorized.

C may not:
- reclassify official provenance;
- redefine clan membership;
- convert rarity into a penalty without an explicit approved rule.

### A → J1
Must consume:
- hybrid admission granularity;
- stable option identity;
- semantic supersession;
- implementation state;
- mode support;
- acquisition context;
- eligibility;
- homebrew lifecycle;
- official-source matrix.

J1 may refine catalog schema but may not create a parallel admission doctrine.

## 5. Retroactive triggers

### `RETRO-CHAR-A-001 — TWO-MODE DAG REVALIDATION`

**Cause:** `CHAR-A-011`.

**Detected contradiction:** the approved architecture audit/DAG still contains language assigning an independent NPC creation mode/specialist, while the newly approved model has exactly two modes, both valid for PCs and NPCs.

**Required Senior Editor action:** patch the architecture documents/DAG/inventory so that any NPC-specific specialist responsibility becomes an envelope/profile/usage layer over Quick/Guided rather than a third procedure.

**Do not silently patch from Specialist A.**

## 6. Blockers

### `BLOCK-CHAR-A-001 — PAGE-LEVEL CANONICAL TRANSCRIPTION`

Exact current licensed text/page verification is still required before final standalone publication for:

- Attribute allocation wording;
- Skill package wording;
- Specialty freebies;
- ordinary starting Discipline allocation;
- Caitiff exact starting/advancement exceptions;
- Thin-Blood exact merits/flaws/Alchemy interface;
- Advantages/Flaws exact baseline/exceptions;
- Predator-Type exceptions;
- Touchstone mapping language;
- starting Hunger;
- any Loresheet creation-limit wording.

This is a transcription/provenance blocker, not an architecture blocker.

## 7. Final Specialist A verdict

`A — COMPLETE FOR SENIOR EDITOR REVIEW`

- Q-001..Q-016: architecturally closed.
- No open user grill decisions remain.
- One retroactive architecture trigger is mandatory.
- One bounded canonical transcription blocker remains.
- Chapter 07 NPC generation remains gated by the wider character-creation architecture; Specialist A alone does not release it.