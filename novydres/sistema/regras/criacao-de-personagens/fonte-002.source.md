---
document_id: novydres_character_creation_core_v5_baseline
version: 0.1
status: draft_for_senior_editor_review
date: 2026-08-12
workstream: character_creation_novydres_architecture
execution_node: A
scope: common_v5_legality_spine_and_admission_interface
depends_on:
  - novydres_character_creation_specialist_a_v5_baseline_research_v0_1.md
  - novydres_character_creation_novydres_architecture_audit_v0_1_1.md
  - novydres_character_creation_architecture_decision_inventory_v0_1_1.md
  - novydres_npc_power_scale_citywide_v0_1_1.md
  - novydres_revelation_architecture_contract_v0_1.md
supersedes: null
---

# Core V5 Character-Creation Baseline — Novydres

## 1. Function

This artifact defines the common legality spine consumed by every Novydres character-creation procedure.

It does not define a third NPC procedure.

There are exactly two creation modes:

1. `Rápido`
2. `Guiado`

Both may create:

- PCs;
- NPCs.

`PC/NPC` changes intended use, envelope inputs and presentation needs where another authority says so. It does not create another legality system.

## 2. Core invariant

All character creation resolves to one common character model.

Different procedures may:

- reorder independent decisions;
- preselect or group choices;
- use presets;
- suppress advanced combinations from the Quick interface;
- provide different levels of explanation.

They may not:

- create different mechanical laws;
- use different derived formulas;
- bypass canonical/local prerequisites;
- make an illegal option legal;
- redefine clan membership;
- invent starting Generation/Blood Potency values owned downstream.

Relationship:

`QUICK ⊆ GUIDED ⊆ COMMON LEGALITY MODEL`

Quick may have a smaller operational reach. Guided is the complete supported creation procedure.

## 3. Publication invariant

This artifact is an editorial rules contract.

The player-facing character-creation material must be compact.

Do not publish the internal state taxonomy as a visible checklist of:

- admission;
- implementation;
- mode support;
- acquisition context;
- eligibility;
- supersession;
- provenance.

Player-facing creation should present:

- the next decision;
- the legal options relevant to that decision;
- the immediate effects that must be applied;
- a concise internal pointer to the authoritative rule-home when detail is required.

No external-book dead end is permitted for a supported option.

## 4. Common character model

A completed character must resolve all applicable domains below.

### 4.1 Identity and concept

Required identity-level information may include concept, name, mortal/undead framing, Ambition/Desire and other presentation fields required by the final design.

A does not lock the final UX order.

### 4.2 Attributes

Use the current canonical V5 starting Attribute allocation.

Research baseline:
- 1 Attribute at 4;
- 3 at 3;
- 4 at 2;
- 1 at 1.

Publication transcription remains subject to current-Core page verification.

### 4.3 Skills

Preserve every canonically equivalent legal starting Skill-distribution profile.

Research baseline:
- Jack of All Trades;
- Balanced;
- Specialist.

No mode may create a new dot total merely for convenience.

Quick may choose a default/preset route. Guided may expose the full legal choice.

### 4.4 Specialties

Apply canonical starting Specialty rules.

The exact current-Core formula is a rule-home transcription item and must be page-verified before publication.

### 4.5 Vampire lineage / condition

The character must resolve exactly one applicable lineage/condition model, such as:

- membership in a supported Clan;
- Caitiff;
- Thin Blood;
- another future explicitly admitted canonical/local condition.

This is not a free mix-and-match layer.

### 4.6 `CLAN MEMBERSHIP` contract

`CLAN MEMBERSHIP` is a central normative domain concept.

When a character belongs to a Clan, a single active versioned clan profile resolves all mandatory clan components through internal rule-homes.

At minimum the profile must be capable of resolving:

- stable clan identity;
- current clan Discipline list;
- current Bane;
- current Compulsion;
- other mandatory clan-specific traits;
- provenance;
- explicit Novydres overrides, if any.

Rules elsewhere may consume `CLAN MEMBERSHIP`. They may not redefine it locally.

A clan profile is atomic for creation legality. A user cannot combine a Discipline list from one version with a superseded Bane or otherwise compose an unofficial hybrid.

### 4.7 Caitiff

Caitiff use their current canonical profile rather than a fabricated clan profile.

Rules:

- demographic rarity does not create automatic mechanical penalty;
- rarity does not require Storyteller permission by itself;
- canonical Caitiff Discipline/advancement/trait exceptions apply;
- exact numerical transcription remains a canonical rule-home verification task.

### 4.8 Thin Blood

Thin Blood uses its current canonical profile.

Rules:

- demographic rarity does not make the option illegal;
- no extra permission gate exists merely because it is rare;
- canonical Thin-Blood traits, merits/flaws, Discipline/Alchemy interface and Generation/Blood Potency interactions apply;
- A does not define Novydres local frequency or starting envelope.

### 4.9 Starting Disciplines and powers

A character resolves canonical starting Discipline ratings according to lineage/condition and other authorized inputs.

Discipline rating and power identity are distinct data.

A power can be selected only when all applicable requirements are satisfied.

The common layer validates:

- active Discipline rating;
- power level;
- prerequisites/amalgam or equivalent requirements;
- clan/condition rules;
- source admission;
- implementation readiness;
- acquisition context;
- mode support;
- character eligibility;
- supersession/override state.

A does not define Novydres power-depth/breadth envelopes.

### 4.10 Advantages, Backgrounds, Merits and Flaws

Use the canonical V5 starting economy as the baseline.

Research baseline for ordinary Kindred:
- 7 dots Advantages;
- 2 dots Flaws.

Exceptions are resolved by the active condition/profile or other rule-home.

Do not duplicate complete catalogs inside the creation chapter.

### 4.11 Predator Type

Predator Type is a required component whenever the canonical rule applies.

It may:

- grant or modify traits;
- add a Discipline dot/selection where its active rule says so;
- modify Humanity or Advantages/Flaws where applicable;
- add hunting identity and related effects.

Quick may package or preset Predator Type. It may not delete a canonically required Predator Type or its effects.

Canonical exceptions are modeled explicitly.

### 4.12 Convictions, Touchstones and Humanity

Use current canonical V5 rules.

Research baseline:
- personal Convictions are chosen within the canonical range;
- Touchstones are assigned as the active canonical rule requires;
- ordinary starting Humanity baseline is 7 before authorized modifiers.

Revelation rule:
mechanical association with a belief, Loresheet, faction or historical claim never certifies protected truth.

### 4.13 Loresheets

A Loresheet is a character option, not a truth certificate.

Selection requires the ordinary catalog gates plus Loresheet-specific prerequisites and acquisition rules.

Hard invariant:

`LORESHEET_SELECTED != LORE_CLAIM_VERIFIED`

Player-facing text remains governed by `novydres_revelation_architecture_contract_v0_1.md`.

### 4.14 Generation

`Generation` is a required final field.

A does not choose the Novydres starting Generation.

Its value is supplied by the downstream envelope/authority that owns starting-age/generation decisions.

While unresolved:

`UNRESOLVED — DOWNSTREAM INPUT REQUIRED`

The character cannot be mechanically finalized until the field is resolved.

### 4.15 Blood Potency

`Blood Potency` is a required final field.

A does not choose the Novydres starting Blood Potency.

Validation must preserve:

- Generation hard constraints;
- Power Scale trajectory invariants;
- any applicable Torpor/trajectory inputs owned elsewhere.

No rule may infer Blood Potency solely from age.

### 4.16 Derived and starting state

Derived values are calculated in the common rules layer, never independently by Quick and Guided.

Invariant:

`SAME INPUTS => SAME DERIVED STATE`

Research baseline includes:
- Health derived from Stamina;
- Willpower derived from Composure + Resolve;
- Humanity from canonical baseline plus authorized modifiers;
- Hunger as an explicit starting state;
- any other canonical derived values required by the final sheet.

Exact formula transcription must use verified current rule-homes.

## 5. Legality spine

The legality spine is a dependency/validation graph, not a rigid page order.

A downstream procedure may move a decision earlier or later only if all true dependencies remain valid.

### 5.1 Conceptual validation flow

1. establish character-use context (`PC` or `NPC`) without changing the creation law;
2. resolve creation procedure (`QUICK` or `GUIDED`);
3. establish required identity/concept inputs;
4. allocate Attributes;
5. allocate Skills and Specialties;
6. resolve lineage/condition;
7. resolve starting Disciplines and powers under that profile;
8. resolve Advantages/Flaws and Loresheets as applicable;
9. resolve Predator Type when canonically applicable and apply its effects;
10. resolve Convictions/Touchstones/Humanity inputs;
11. receive required downstream Generation/Blood Potency values;
12. calculate all derived/starting state centrally;
13. run final legality validation.

This numbered list is not a mandatory publication order. It is a dependency-oriented baseline.

## 6. Catalog and admission interface

### 6.1 Stable option identity

Every selectable rule option has one stable internal identity.

Multiple official sources may point to the same identity.

Republication does not create duplicate selectable entries.

### 6.2 Admission granularity

Use three levels:

1. source;
2. content family;
3. option-level exception.

Default classification occurs at family level where practical. Individual option entries are used for exceptions, conflicts, supersession and special eligibility.

### 6.3 Official admission presumption

Official V5 content relevant to character building is presumed eligible for admission review.

This is not automatic admission of an entire book.

Setting prose, antagonist material, chronicle procedure and character options are distinct families.

### 6.4 Admission states

Final admission states:

- `ADMITTED`
- `SUPERSEDED`
- `PARTIAL`
- `EXCLUDED`

`PARTIAL` is aggregative:

a parent scope is `PARTIAL` when its children contain different final states.

`PARTIAL` never means unfinished research or incomplete implementation.

### 6.5 Specialized procedures

Content admission and procedure admission are independent.

Official alternative/specialized creation procedures may be recorded as:

- `BASELINE`;
- `DOWNSTREAM CANDIDATE`;
- `EXCLUDED/SUPERSEDED`.

Examples:
- action-focused creation from *Gehenna War* is not automatically the common baseline;
- Ancilla creation from *In Memoriam* is input to the owner of older-character envelopes;
- Memoriam procedure belongs to its own downstream integration decision.

### 6.6 Supersession

Precedence:

1. official errata;
2. explicitly corrected/revised current text;
3. demonstrably substitutive later mechanical presentation;
4. original text when no revision exists.

Latest date alone never proves supersession.

Unresolved official conflict:
`CANONICAL REVIEW REQUIRED`

No silent guess.

### 6.7 Implementation gate

Admission and standalone readiness are separate.

An option can be:

`ADMITTED`
but
`IMPLEMENTATION PENDING`

Such an option belongs to Novydres' supported scope but is not selectable in a published standalone workflow until its internal rule-home is sufficient.

### 6.8 Mode support

Mode support is separate from legality.

Possible editorial values include:
- `GUIDED — SUPPORTED`
- `QUICK — SUPPORTED`
- `QUICK — NOT_SUPPORTED`

`NOT_SUPPORTED` means only that the procedure does not construct that option directly. It does not make the option illegal.

### 6.9 Acquisition context

Admission does not mean “available at initial creation”.

Each option can identify legal acquisition contexts, such as:
- initial creation;
- advancement;
- narrative acquisition;
- other rule-defined context.

Character creation offers an option only when initial acquisition is allowed.

### 6.10 Eligibility

Global admission and contextual eligibility are separate.

An admitted, implemented option may still be ineligible for a specific character due to prerequisites, clan/condition, rating, or another authorized constraint.

Contextual ineligibility never globally reclassifies the option.

### 6.11 Effective selectability

Editorial rule:

`SELECTABLE = ADMITTED + IMPLEMENTED + MODE_SUPPORTED + ACQUISITION_ALLOWED + ELIGIBLE`

This formula must remain internal/editorial.

The player sees a clean list of legal choices, not the validation machinery.

## 7. Homebrew interface

### 7.1 Admission gate

Homebrew begins as:
`HOMEBREW — CANDIDATE`

Admission requires the applicable review set, including:

- stable identity/version;
- explicit provenance;
- internal rule-home;
- V5 compatibility;
- conflict/duplication review;
- prerequisites;
- balance review owned by the appropriate specialist;
- local-rule interactions;
- explicit admission decision;
- Senior Editor approval.

Only then:
`HOMEBREW — ADMITTED`

### 7.2 Official replacement

A homebrew/local implementation may replace an official implementation only through explicit Novydres override.

Requirements:

- official option identified;
- reason recorded;
- local rule-home complete;
- provenance preserved;
- downstream impact recorded;
- versioned/reversible decision;
- Senior Editor approval.

No silent replacement.

## 8. Downstream interfaces

### 8.1 A → B

A exports:

- required `Generation` field;
- required `Blood Potency` field;
- canonical Generation↔BP constraint interface;
- ordinary/canonical character model;
- specialized-procedure research pointers, especially *In Memoriam*;
- prohibition on age automatically granting power.

B must return:
- legal starting Generation/BP envelopes;
- any age/era/envelope inputs needed by Quick/Guided;
- no redefinition of the common model.

### 8.2 A → C

A exports:

- global admission vs contextual eligibility distinction;
- common option identities;
- `CLAN MEMBERSHIP` contract;
- Loresheet/revelation boundary;
- no automatic rarity penalty.

C may add local/contextual eligibility conditions only within its authority. It must not rewrite canon/source provenance.

### 8.3 A → J1

A exports:

- hybrid source/family/option admission model;
- stable option identity;
- supersession semantics;
- implementation gate;
- acquisition-context field;
- mode-support field;
- eligibility interface;
- homebrew gate;
- official source research matrix.

J1/catalog work must not create a parallel admission doctrine.

## 9. Retroactive triggers and blockers

### `RETRO-CHAR-A-001 — TWO-MODE DAG REVALIDATION`

Reason:
the approved audit/DAG language still describes an independent NPC-mode specialist, while the new approved architecture has exactly two procedures, both usable for PCs and NPCs.

Required Senior Editor action:
revalidate the DAG/inventory and convert NPC-specific work into profile/envelope/usage responsibilities over Quick/Guided rather than a third creation mode.

### `BLOCK-CHAR-A-001 — PAGE-LEVEL CANONICAL TRANSCRIPTION`

Blocks:
final player-facing transcription of exact V5 numbers/wording for the bounded items listed in the Specialist A research artifact.

Does not block:
approval of the A architecture, admission interface or downstream contracts.

## 10. Verdict

`SPECIALIST A BASELINE COMPLETE — READY FOR SENIOR EDITOR REVIEW`

Conditions:

1. Senior Editor must adjudicate `RETRO-CHAR-A-001`.
2. Exact player-facing canonical transcription must clear `BLOCK-CHAR-A-001`.
3. A does not authorize Chapter 07 NPC generation by itself.
4. A does not reopen Power Scale decisions.