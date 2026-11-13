---
document_id: novydres_character_creation_specialist_a_v5_baseline_research
version: 0.1
status: draft_for_senior_editor_review
date: 2026-08-12
workstream: character_creation_novydres_architecture
execution_node: A
specialist: core_v5_creation_baseline_and_admission_interface
question_scope:
  - CHAR-CREATE-Q-001
  - CHAR-CREATE-Q-002
  - CHAR-CREATE-Q-003
  - CHAR-CREATE-Q-004
  - CHAR-CREATE-Q-005
  - CHAR-CREATE-Q-006
  - CHAR-CREATE-Q-007
  - CHAR-CREATE-Q-008
  - CHAR-CREATE-Q-009
  - CHAR-CREATE-Q-010
  - CHAR-CREATE-Q-011
  - CHAR-CREATE-Q-012
  - CHAR-CREATE-Q-013
  - CHAR-CREATE-Q-014
  - CHAR-CREATE-Q-015
  - CHAR-CREATE-Q-016
depends_on:
  - novydres_master_senior_editor_prompt_v1_2.md
  - novydres_prompt_reuse_contract_v0_1.md
  - novydres_character_creation_novydres_architecture_audit_v0_1_1.md
  - novydres_character_creation_architecture_decision_inventory_v0_1_1.md
  - novydres_character_creation_architecture_dag_correction_patch_report_v0_1.md
  - novydres_npc_power_scale_citywide_v0_1_1.md
  - novydres_npc_power_scale_citywide_decisions_v0_1.md
  - novydres_revelation_architecture_contract_v0_1.md
supersedes: null
---

# Specialist A — V5 Baseline Research

## 1. Purpose

This artifact separates three kinds of authority before the Novydres character-creation baseline is written:

1. `CANONICAL V5` — rules or product facts attributable to the official V5 line.
2. `NOVYDRES ARCHITECTURE` — project decisions made during the Specialist A grill.
3. `SOURCE POINTER DEBT` — a canonical rule believed to be stable but still requiring page-level confirmation against the current licensed Core/Player's Guide text before publication-quality transcription.

This document is research memory. It is not the player-facing character-creation chapter.

## 2. Authority and source posture

### 2.1 Current Core

The current Renegade edition of the V5 Core Rulebook is the baseline rules authority for the common character model. Renegade states that the current 428-page Core contains all previous Core Rulebook errata and the errata from the V5 Companion.

Operational consequence:

- old Core wording does not outrank a corrected current Core;
- current errata/revised wording wins when supersession is evidenced;
- publication date alone is not sufficient to infer supersession.

### 2.2 Player's Guide

The official Player's Guide is a major consolidation and expansion point for player-character material. Official descriptions confirm profiles for all Kindred clans, including Banu Haqim, Hecata, Lasombra, Ministry, Ravnos, Salubri, Tzimisce, Caitiff and Thin Blood, plus Discipline powers, Blood Sorcery Rituals, Thin-Blood Alchemy, Oblivion/Ceremonies, coterie systems, and additional Predator Types.

Operational consequence:

- Core + Player's Guide are primary normalization anchors;
- Player's Guide is not an exclusivity boundary for all character-building content.

### 2.3 Official line remains distributed

Official publisher descriptions confirm additional character-building material outside Core/Player's Guide, including at minimum:

- *Cults of the Blood Gods*: Hecata play material, Oblivion/Ceremonies, Loresheets, Backgrounds, Predator Types.
- *Blood Sigils*: Blood Sorcery Rituals, Thin-Blood Alchemy formulae, systems for blood craft, Loresheets.
- *Blood-Stained Love*: Merits, Flaws, Discipline powers.
- *Gehenna War*: specialized action-focused character-creation procedure.
- *In Memoriam*: enriched Ancilla creation, expanded/consolidated Memoriam, Loresheets.
- *Tattered Façade*: Discipline Powers, Rituals, Ceremonies, Formulae, Loresheets, clan Archetypes; it also reuses the existing Predator-Type family.
- earlier setting/source books may contain clans, powers, Loresheets, Backgrounds, Merits, Flaws or other selectable content and therefore require family-level review rather than book-level assumption.

## 3. Canonical baseline — research findings

### 3.1 Creation is a dependency graph, not merely a page order

The V5 character is composed from interdependent domains: concept/identity, Attributes, Skills, Specialties, vampire lineage/condition, Disciplines, Advantages and Flaws, Predator Type when applicable, Humanity/Convictions/Touchstones, and derived/starting state.

Novydres may reorder independent decisions in its two procedures, but cannot alter dependencies without an explicit local rule.

### 3.2 Attributes

Canonical baseline commonly used by V5 creation:

- one Attribute at 4;
- three Attributes at 3;
- four Attributes at 2;
- one Attribute at 1.

`SOURCE POINTER DEBT`: confirm exact current-Core presentation/page and whether the current licensed text phrases this as direct assignment or starting-at-1 plus increases. The final numerical distribution must be page-verified before publication.

### 3.3 Skills

Canonical V5 offers multiple legal Skill-distribution profiles rather than a single mandatory profile. The commonly documented distributions are:

- Jack of All Trades: one Skill at 3, eight at 2, ten at 1;
- Balanced: three Skills at 3, five at 2, seven at 1;
- Specialist: one Skill at 4, three at 3, three at 2, three at 1.

Novydres decision: preserve all canonically equivalent legal distributions in the common legality model. Quick or Guided may present them differently.

`SOURCE POINTER DEBT`: page-verify labels and exact dot distributions in the current Core before final publication.

### 3.4 Specialties

V5 treats Specialties as part of the starting Skill model. The canonical creation procedure grants required/free Specialties tied to specific broad Skills and an additional chosen Specialty.

`SOURCE POINTER DEBT`: page-verify the exact free-Specialty formula and affected Skills before transcription. Do not publish from memory alone.

### 3.5 Starting Disciplines

For ordinary clan Kindred, V5 character creation establishes starting Discipline dots from the character's clan Disciplines, with power selection constrained by Discipline rating and any prerequisites.

Novydres interface rule:

- the common model stores Discipline ratings separately from selected powers;
- each power is a stable catalog identity;
- eligibility validates Discipline level, prerequisites, clan/condition interactions, source admission, acquisition context, and local overrides;
- A does not set Novydres discipline-depth envelopes.

`SOURCE POINTER DEBT`: page-verify the exact starting dot allocation for ordinary clan Kindred and exact Caitiff/Thin-Blood exceptions.

### 3.6 Advantages, Backgrounds, Merits, Flaws

V5 uses Advantages as the broad acquisition layer containing Backgrounds, Merits and related option families; Flaws impose negative traits/obligations. Loresheets interface through the Advantage economy according to their active rules.

The commonly documented ordinary baseline is seven dots of Advantages and two dots of Flaws.

`SOURCE POINTER DEBT`: page-verify ordinary baseline totals, exceptional profiles, and any current Player's Guide clarifications before publication.

### 3.7 Predator Type

Predator Type is a canonical character-building component for vampires to whom the rule applies. It packages hunting identity with mechanical effects and can modify other starting choices/states.

Novydres decision:

- Predator Type is part of the legality spine when canonically applicable;
- Quick may simplify/preset the choice but may not erase required effects;
- canonical exceptions remain exceptions, not a weakening of the general rule.

`SOURCE POINTER DEBT`: page-verify exact exceptions for characters too new or otherwise canonically outside the normal Predator-Type assumption.

### 3.8 Convictions, Touchstones, Humanity

Canonical V5 creation uses Chronicle Tenets at chronicle level and personal Convictions/Touchstones at character level. Commonly documented baseline:

- choose 1–3 Convictions;
- associate each Conviction with a Touchstone as required by the active rule;
- ordinary starting Humanity is 7 before applicable modifiers, including Predator Type effects.

Novydres decision:

- this moral architecture remains canonical baseline;
- local lore/revelation does not certify truth through mechanical selection.

`SOURCE POINTER DEBT`: page-verify current exact Touchstone mapping language and any exceptions.

### 3.9 Derived and starting state

Commonly documented V5 derived values include:

- Health = Stamina + 3;
- Willpower = Composure + Resolve;
- Humanity starts from the canonical baseline then applies authorized modifiers;
- Hunger is an explicit starting-state field.

Generation and Blood Potency are required final fields, but Specialist A does not define Novydres starting values.

`SOURCE POINTER DEBT`: page-verify starting Hunger and all final-state initialization instructions in the current Core.

### 3.10 Clan membership

The official line treats clan as a bloodline identity associated with shared powers and weaknesses. Novydres goes further architecturally by defining a central, versioned `CLAN MEMBERSHIP` mechanical contract.

The active clan profile must resolve, through internal rule-homes:

- clan identity;
- clan Discipline list;
- Bane;
- Compulsion;
- other mandatory clan-specific traits in the active official/local implementation;
- provenance and any explicit local override.

The profile is atomic for creation purposes: components are not freely mixed across versions.

### 3.11 Caitiff

Caitiff are a canonical playable condition/profile distinct from ordinary clan membership.

Novydres decisions:

- Caitiff rarity is demographic only unless a separate rule says otherwise;
- rarity alone does not create a permission gate;
- Caitiff use their canonical discipline/advancement/trait exceptions;
- Caitiff are not modeled as a fake clan solely for schema convenience.

`SOURCE POINTER DEBT`: page-verify current Caitiff starting Discipline allocation, costs, and exact mechanical exceptions.

### 3.12 Thin Blood

Thin Blood is a canonical playable condition/profile with distinct Generation/Blood Potency and Thin-Blood-specific mechanics.

Novydres decisions:

- rarity alone does not make Thin Blood illegal or Storyteller-permission-only;
- Thin Blood uses its own canonical profile and exception rules;
- A does not set local demographic frequency or local starting envelope.

`SOURCE POINTER DEBT`: page-verify current Thin-Blood merits/flaws balance, Discipline/Alchemy starting interface, and exact generation/BP text before transcription.

### 3.13 Loresheets

Loresheets are selectable character-building content when admitted, implemented, mode-supported, acquisition-valid and character-eligible.

Novydres Revelation invariant:

`LORESHEET SELECTED != LORE CLAIM VERIFIED`

A Loresheet can establish mechanical association, access, reputation, knowledge framing or another authorized benefit. It does not certify player-facing historical truth, resolve a rumor, or bypass protected revelation.

### 3.14 Source admission

Approved A policy:

- official V5 material relevant to character building has a presumption of eligibility for admission review;
- it is not automatically admitted merely because the book is official;
- classification is hybrid: source → content family → per-option exception;
- states `ADMITTED / SUPERSEDED / PARTIAL / EXCLUDED` describe final admission composition;
- `PARTIAL` is aggregative composition, never a synonym for pending work;
- pending research/implementation/conflict uses separate editorial state;
- source admission and specialized-procedure admission are independent.

### 3.15 Supersession and errata

Approved precedence:

1. applicable official errata;
2. current text explicitly corrected/revised;
3. later presentation demonstrably substitutive or mechanically revised;
4. original presentation when no revision is evidenced.

A later identical/near-identical republication remains another provenance pointer to the same stable option identity. It does not create a second selectable option.

Unresolvable official conflicts are marked for canonical review; no arbitrary latest-date rule.

### 3.16 Homebrew

Homebrew lifecycle:

`HOMEBREW — CANDIDATE`
→ provenance/version/rule-home/compatibility/conflict/prerequisite/balance/local-interaction review
→ explicit decision
→ Senior Editor approval
→ `HOMEBREW — ADMITTED`

Homebrew never masquerades as official.

An admitted local/homebrew implementation may override official material only by explicit, versioned, justified Senior Editor-approved Novydres override. Official provenance remains traceable.

## 4. Official source-admission research matrix

This matrix is editorial. It is not player-facing.

| Source | Confirmed character-building families | Content admission posture | Procedure posture | Audit note |
|---|---|---|---|---|
| Current V5 Core Rulebook | baseline creation; core clans; Attributes; Skills; Disciplines; Advantages/Flaws; Predator Type; Humanity/Convictions/Touchstones; derived state | `ADMITTED` baseline | `BASELINE` | Current printing states prior Core + Companion errata incorporated |
| V5 Player's Guide | all-clan profiles; Caitiff; Thin Blood; Discipline powers; Rituals; TBA; Oblivion/Ceremonies; Predator Types; coterie material | family-level `ADMITTED`, option exceptions allowed | baseline clarification/consolidation only where compatible | Major normalization anchor, not exclusive corpus |
| V5 Companion | Tzimisce/Ravnos/Salubri; powers; ghoul/mortal material | `PARTIAL` / provenance-sensitive | not an independent baseline | Resolve active identities against current Core/PG and evidence of revision |
| Camarilla | setting-linked character options where present | `PARTIAL` after family audit | no automatic procedure import | Admit only character-building families |
| Anarch | setting-linked character options where present | `PARTIAL` after family audit | no automatic procedure import | Admit only character-building families |
| Chicago by Night | Lasombra and character options where present | `PARTIAL` | no automatic procedure import | Later consolidated presentations may share stable identities |
| Cults of the Blood Gods | Hecata; Oblivion/Ceremonies; Loresheets; Backgrounds; Predator Types | `PARTIAL`, relevant families presumed eligible | cult/chronicle procedures not baseline | Family admission + option exceptions |
| Children of the Blood | Loresheets; Merits; Flaws; Backgrounds and related options | `PARTIAL` | no automatic procedure import | Option-level eligibility may be setting/cult specific |
| Chicago Folios | character options where present | `PARTIAL` after family audit | no automatic procedure import | Scenario/setting text is not character catalog by default |
| Let the Streets Run Red | character options where present | `PARTIAL` after family audit | no automatic procedure import | Same rule |
| Trails of Ash and Bone | character options where present | `PARTIAL` after family audit | no automatic procedure import | Same rule |
| Fall of London | chronicle-linked character material where present | `PARTIAL` after family audit | chronicle procedure not baseline | Chronicle-specific assumptions require eligibility review |
| Sabbat: The Black Hand | player-usable mechanical options where officially intended as such | `PARTIAL` after family audit | antagonist/sect procedure not baseline by default | Antagonist-only material is not presumed selectable |
| Second Inquisition | mostly antagonist/tools; any player-facing options require explicit family audit | `PARTIAL` / likely narrow | no baseline import | Do not convert antagonist resources into PC options automatically |
| Blood Sigils | Blood Sorcery Rituals; Thin-Blood Alchemy; Loresheets; related blood-craft options | relevant families `ADMITTED` subject to option exceptions | build-your-own systems are separate procedure/rule-home concern | Strong character-option source |
| Blood-Stained Love | Merits; Flaws; Discipline powers | relevant families `ADMITTED` subject to option exceptions | romance procedures not baseline | Character options and chronicle advice separated |
| Gehenna War | action-focused character creation; combat-related player material | family audit required | `DOWNSTREAM CANDIDATE`, not A baseline | Admission of source content does not import action-focused creation |
| In Memoriam | Ancilla creation; expanded Memoriam; Loresheets | Loresheets/content families eligible; exact option audit required | Ancilla creation → B input; Memoriam → historical/played-history input | A records, downstream owner decides integration |
| Tattered Façade | Discipline Powers; Rituals; Ceremonies; Formulae; Loresheets; clan Archetypes | relevant families presumed eligible; option audit required | horror/city procedures not baseline | Published after PG; date alone does not imply supersession |
| Future official V5 sources | any character-building family | `REVIEW REQUIRED` | independent procedure review | No automatic corpus freeze |

## 5. Editorial-state model

The following dimensions are internal/editorial only:

- `admission_state`
- `implementation_state`
- `mode_support`
- `acquisition_context`
- `eligibility`
- `supersession_state`
- `provenance`
- `rule_home`
- `stable_option_identity`

Player-facing prose must not expose this machinery as a mass of states.

Effective selectability is conceptually:

`SELECTABLE = ADMITTED AND IMPLEMENTED AND MODE_SUPPORTED AND ACQUISITION_ALLOWED AND ELIGIBLE`

This expression is an editorial validation rule, not publication prose.

## 6. Two-mode architectural correction

Specialist A records a material project correction produced by the grill:

- exactly two character-creation modes exist: `QUICK` and `GUIDED`;
- both create PCs and NPCs;
- `PC/NPC` is a use/type dimension, not a third creation mode;
- Quick may support a strict operational subset of the space reachable by Guided;
- both write the same common character model and obey the same legality spine.

This conflicts with audit/DAG language that still describes an independent NPC-mode specialist. Specialist A does not silently rewrite the approved DAG.

### Retroactive trigger

`RETRO-CHAR-A-001 — TWO-MODE DAG REVALIDATION`

Trigger:
Senior Editor review of Specialist A.

Required action:
revalidate every architecture/DAG/inventory reference that treats NPC creation as an independent third procedure. Preserve any useful NPC-specific envelope/usage specialist responsibility by converting it to a consumer/profile layer over Quick/Guided rather than a parallel creation system.

## 7. Research confidence

### High confidence / current official publisher evidence
- current Core incorporates prior Core + Companion errata;
- Player's Guide is a major character-building consolidation but not exhaustive;
- current line distributes options across Cults, Blood Sigils, Blood-Stained Love, Tattered Façade and others;
- Gehenna War contains specialized action-focused creation;
- In Memoriam contains enriched Ancilla creation and expanded Memoriam.

### High confidence / stable V5 baseline, but page verification required before verbatim publication
- Attribute distribution;
- Skill distribution packages;
- ordinary Advantages/Flaws totals;
- ordinary Humanity baseline;
- Health/Willpower formulae.

### Must be page-verified before standalone rule transcription
- exact Specialty freebies;
- exact ordinary starting Discipline allocation wording;
- exact Caitiff starting and advancement exceptions;
- exact Thin-Blood starting merits/flaws/Alchemy interface;
- exact Predator-Type exception wording;
- exact starting Hunger instruction;
- exact Loresheet creation constraints.

## 8. Research verdict

`RESEARCH SUFFICIENT FOR SPECIALIST-A ARCHITECTURE BASELINE`

with one bounded provenance debt:

`PAGE-LEVEL CANONICAL TRANSCRIPTION CHECK REQUIRED BEFORE FINAL PLAYER-FACING RULE-HOMES`

This debt does not reopen the A architecture decisions. It blocks only exact publication transcription of the enumerated canonical details.