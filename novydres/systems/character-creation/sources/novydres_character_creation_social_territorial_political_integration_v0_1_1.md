---
document_id: novydres_character_creation_social_territorial_political_integration
version: 0.1.1
status: candidate_for_senior_editor_revalidation
date: 2026-08-13
workstream: character_creation_novydres_architecture
execution_node: C
scope: social_territorial_political_integration_for_pc_and_npc_creation
owns:
  - CHAR-CREATE-Q-030
  - CHAR-CREATE-Q-031
  - CHAR-CREATE-Q-032
  - CHAR-CREATE-Q-033
  - CHAR-CREATE-Q-034
  - CHAR-CREATE-Q-035
  - CHAR-CREATE-Q-036
  - CHAR-CREATE-Q-037
  - CHAR-CREATE-Q-038
  - CHAR-CREATE-Q-039
  - CHAR-CREATE-Q-040
  - CHAR-CREATE-Q-041
  - CHAR-CREATE-Q-042
decisions:
  - CHAR-C-001
  - CHAR-C-002
  - CHAR-C-003
  - CHAR-C-004
  - CHAR-C-005
  - CHAR-C-006
  - CHAR-C-007
  - CHAR-C-008
  - CHAR-C-009
  - CHAR-C-010
  - CHAR-C-011
  - CHAR-C-012
  - CHAR-C-013
  - CHAR-C-014
  - CHAR-C-015
  - CHAR-C-016
  - CHAR-C-017
  - CHAR-C-018
  - CHAR-C-019
  - CHAR-C-020
depends_on:
  - novydres_master_senior_editor_prompt_v1_2.md
  - novydres_prompt_reuse_contract_v0_1.md
  - skill_caveman_v1_0.md
  - skill_grill_me_v1_1.md
  - novydres_editorial_governance_v1_0.md
  - novydres_character_creation_novydres_architecture_audit_v0_1_3.md
  - novydres_character_creation_architecture_decision_inventory_v0_1_2.md
  - novydres_character_creation_core_v5_baseline_v0_1.md
  - novydres_character_creation_specialist_a_decisions_v0_1.md
  - novydres_character_creation_power_envelope_v0_1_1.md
  - novydres_character_creation_specialist_b_decisions_v0_1_1.md
  - novydres_npc_power_scale_citywide_v0_1_1.md
  - novydres_npc_power_scale_citywide_decisions_v0_1.md
  - 03_atlas_de_novydres_v0_2_2.md
  - 04_faccoes_politica_conflitos_v0_2.md
  - 05_concilio_leis_status_prestacoes_v0_2_2.md
  - 06_fe_heresia_e_ordem_v0_2_1.md
  - 07_personagens/iskander_yasupov_v0_9.md
  - 07_personagens/madame_zoya_v0_9.md
companion_decision_log: novydres_character_creation_specialist_c_decisions_v0_1_1.md
supersedes: novydres_character_creation_social_territorial_political_integration_v0_1.md
patch_scope: downstream_ownership_leakage_and_decision_provenance_auditability_only
no_substantive_rule_change: true
decision_authority: CHAR-C-001_through_CHAR-C-020_preserved
final_verdict: READY_FOR_SENIOR_EDITOR_REVALIDATION
---

# Character Creation — Social, Territorial & Political Integration

## A. Function and authority

This document closes Specialist C for the `character_creation_novydres_architecture` workstream.

Its purpose is to define the creation-time interfaces through which a PC or NPC is situated in Novydres as a social, territorial and political being without redesigning the upstream authorities that already own those subjects.

This document does **not** redefine:

- V5 core legality, Background catalogues, Attribute/Skill/Discipline construction or their final numeric allocation;
- Power Envelope, Generation, Blood Potency, Discipline Depth/Breadth, Mechanical Load or Rarity Debt;
- Chapter 03 territorial canon;
- Chapter 04 factions and political structures;
- Chapter 05 Recognition, Status, offices, positional authority or Prestações;
- Chapter 06 institutions and religious structures;
- the complete Bairrismo mechanic;
- the complete Marco Territorial mechanic;
- Dignitas authority and catalogue;
- the detailed prompt/provocation system for Guided Creation;
- the detailed published sequence for Quick Creation;
- XP awards or advancement economics.

Where an upstream authority exists, Character Creation consumes it through a creation interface rather than duplicating it.

### A.1 Corrective ownership rule

This v0.1.1 patch does not change any Specialist-C social, territorial or political rule.

For governance purposes, every statement in this artifact must be read in one of three authority classes:

1. **C-OWNED FINAL** — a current Specialist-C invariant or state semantic;
2. **USER-APPROVED DOWNSTREAM DESIGN DIRECTION — OWNER RATIFICATION REQUIRED** — a project direction already approved by the user that the proper downstream owner must consume, evaluate and ratify inside its scope;
3. **DERIVED/EDITORIAL** — explanation, audit scaffolding or non-normative production guidance.

`APPROVED DIRECTION ≠ FINAL DOWNSTREAM IMPLEMENTATION`.

`OWNER RATIFICATION ≠ PERMISSION TO IGNORE USER-APPROVED DIRECTION`.

If a downstream owner finds an incompatibility, it must not silently override the direction. It must return the conflict to the Senior Editor and cite the originating `CHAR-C-*` decision.

## B. TTRPG design invariant

Novydres Character Creation is a **tabletop RPG procedure**.

Exactly two creation modes exist:

1. **Rápido**;
2. **Guiado**.

Both apply to PCs and NPCs and must terminate in a complete, playable character state.

The final supplement must not require software, an engine, a parser, executable frontmatter, automated state tracking or any other runtime infrastructure.

Editorial matrices, taxonomies, flags, ledgers, validation tables and state labels in this document are production and audit tools only. They may inform how rules are written, but they are not mandatory player-facing forms unless a later publication-design node deliberately converts a small part of them into concise tabletop instructions.

The design target is:

`complete sheet + coherent history + V5 Relationship Map + playable current placement in Novydres`

for both modes.

The difference between Rápido and Guiado is the **path**, not the required completeness of the result.

## C. Common creation-state invariants

1. Social, territorial and political power never automatically grants personal supernatural power.
2. Age does not automatically grant Rootedness, Status, office, Dignitas, Prestações, Marco Territorial, Backgrounds or assets.
3. Residence is not feeding right, domain, ownership, jurisdiction or supernatural attachment.
4. Affiliation is not Status, office, Influence, ownership or authority.
5. Office is not a purchase entitlement and does not manufacture Attributes, Skills, Disciplines or Personal Status.
6. Narrative importance does not create a mechanical trait for free.
7. Historical truth does not imply that a state remains active in 2010.
8. Rápido and Guiado use the same legal and social ontology.
9. NPC depth may be abbreviated downstream, but NPCs do not use a third creation ontology.
10. Published procedures should expose only the information needed to make and use the character at the table.

## D. Rootedness

### D.1 States

The creation-time Rootedness sequence is:

`Forasteiro → Residente → Enraizado → Histórico`

These are qualitative states, not dots and not a numeric progression.

Rootedness is independent from:

- chronological age;
- Generation;
- Blood Potency;
- Clan;
- Personal Status;
- office;
- Marco Territorial;
- Bairrismo;
- Presence State.

No universal fixed-year threshold determines a state.

### D.2 Creation procedure

Rootedness is resolved through three conceptual moments:

1. intended/premise state;
2. qualitative trajectory evidence;
3. final validated state.

Rápido may summarize the trajectory in a compact history.

Guiado may demonstrate it through the pre-chronicle storyline.

Both terminate in the same current-state vocabulary.

### D.3 Political meaning

Rootedness can support the provenance or plausibility of trust, familiarity, legitimacy and local reputation, but it grants none of them mechanically.

A newcomer can possess valid political legitimacy through appointment, patronage, Recognition or another competent authority.

A Histórico character can be politically marginal, proscribed, hated or oppositional.

Rootedness is evidence and context; it is not a Status economy.

## E. Bairrismo at creation

### E.1 Nature

Bairrismo is real, supernatural, extremely subtle, progressive and ultimately inevitable through prolonged lived exposure to Novydres.

It is not inherently beneficial.

Its expression includes emotional and territorial dependence and a real aggravatable compulsion under its own mechanic/authority.

Ordinary residents and Cainites do not normally perceive or name Bairrismo as a measurable condition.

Published language must avoid presenting local society as if characters routinely say that one person is “more affected by Bairrismo” than another.

### E.2 Creation-time progression

For creation architecture only, the following internal progression may be used:

`não consolidado → manifestação emergente → consolidado`

These are editorial interface states, not player-facing dots or levels.

No universal timer exists.

Acquisition depends on actual exposure, permanence, trajectory and belonging.

Local origin or local Embrace does not instantly grant consolidation.

However, `Enraizado + real belonging` makes consolidated Bairrismo the ordinary expected result. Lack of consolidation in a clearly rooted character should therefore have an explanation.

The belonging milestone may be mundane and organic. Consolidation must not require extraordinary heroism, centuries of residence, Status or office.

`Histórico` does not create a second Bairrismo layer.

### E.3 Quick and Guided

Rápido may select the current Bairrismo state from a coherent summarized trajectory.

Guiado may show emergence and consolidation during the storyline.

Neither mode receives additional power merely for using a more elaborate narrative route.

## F. Marco Territorial

### F.1 Timing

Marco Territorial is resolved during final territorial/moral consolidation, after the trajectory establishes eligibility.

In Guiado, the storyline may discover **which place** becomes the Marco.

In Rápido, the place may be defined directly from summarized history.

Narrative discovery cannot bypass eligibility.

### F.2 Relationship to Bairrismo and Touchstones

Marco Territorial is an adapted urban/place Touchstone interface already authorized upstream.

It is distinct from ordinary mortal Touchstones and does not automatically replace them.

It is special/additional where applicable.

Marco does not create or automatically intensify Bairrismo.

Valid final states include Enraizado/Historical characters with or without Marco and former newcomers who acquire a Marco only after genuine rooting.

A still-unrooted newcomer cannot select a Marco merely because the player likes a location.

## G. Territorial placement

Character Creation must provide enough current territorial placement to situate the character immediately in Novydres.

The following concepts must remain distinct:

- current raion/placement;
- residence/refuge;
- feeding territory;
- political or legal domain;
- shared/coterie domain;
- faction/institutional territory;
- Marco Territorial.

Safety formula:

`living there ≠ hunting there ≠ ruling there ≠ owning there ≠ being supernaturally attached to there`

Raion placement is ordinarily supplied or bounded by the chronicle premise and Play Guidance.

Rápido needs a clear present territorial state.

Guiado may additionally explore historical movement, but prior presence never manufactures present territorial rights.

## H. Affiliation and institutional links

Creation uses a modular model of political, sectarian, factional, institutional, Clan and juridical links.

This is an **internal design model**, not a mandatory player checklist.

A character is not required to fill every affiliation category.

Only materially relevant links created by premise or trajectory need to survive into the final character state.

Current and historical links must remain distinct.

Former membership does not imply current rights, access, Status or authority.

Affiliation remains separate from:

- Personal Status;
- Positional Status;
- office;
- Influence;
- Backgrounds;
- legal authority;
- territorial ownership.

## I. Personal Status at creation

Personal Status may exist at creation when two validations are satisfied:

1. the Status is mechanically/legalistically permitted under the common V5 model and Chapter 05;
2. recognized social provenance explains why the Status is real in Novydres in 2010.

History explains Status; it does not manufacture free Status.

Rápido can begin with premise-justified Status.

Guiado may show the trajectory that produces Recognition or reputation, but the final trait must still be valid under Chapter 05.

External reputation brought by a newcomer does not automatically become formal Novydres court Status.

Reputação Paralela remains a separate political sphere where applicable.

## J. Offices and Positional Status at creation

A PC or NPC may begin holding an office only as an **authorized political state** from the chronicle premise and existing political authority.

An initial office requires:

1. a real office recognized by upstream authority;
2. juridical/political eligibility where required;
3. valid provenance through appointment, election, Recognition, succession or another authorized route;
4. compatibility with the chronicle premise;
5. Office Functional Fit;
6. correct Positional Status treatment without free Personal Status.

Rápido may receive an office as an authorized part of the premise.

Guiado may explain how the character reached the office but cannot manufacture institutional authority merely because a storyline event is dramatic.

Multiple offices are permitted only where upstream rules permit them.

Positional Status does not stack: the existing Chapter 05 rule remains authoritative.

A character without Recognition cannot exercise a Concílio office when Chapter 05 prohibits it.

## K. Dignitas at creation

Dignitas may exist in the initial state of a Ventrue when valid trajectory and Ventrue authority sustain the recognition.

Dignitas is:

- not mandatory;
- not granted merely for being Ventrue;
- not derived automatically from Status;
- not derived automatically from office;
- not derived automatically from supernatural power.

Character Creation records only the interface needed to make the starting state coherent: recognition, provenance, current state and governing authority.

The complete Dignitas mechanic remains in its Ventrue authority.

Rápido can begin with pre-existing validated Dignitas.

Guiado may explain acquisition or loss, but cannot create unrecognized Dignitas for free.

## L. Prestações at creation

A character may begin:

- with no Prestações;
- owing one or more Prestações;
- holding one or more Prestações owed by others;
- with obligations in both directions across different relationships.

Every initial Prestação requires:

- identifiable parties;
- direction of obligation;
- degree where applicable;
- provenance;
- current validity;
- registration/testimony when Chapter 05 requires it.

Historical obligations that were paid, cancelled, replaced, extinguished or no longer valid do not automatically survive as current assets.

Prestações do not automatically grant or consume Status, Mawla, Allies, Influence, Resources or another Background.

Juramentos Imortais remain a separate authority.

## M. Narrative relationships and mechanical representation

Relationships exist first as fictionally real relationships.

A relationship may be:

1. narrative only;
2. narrative plus a legally allocated mechanical representation;
3. one relationship participating in multiple independent systems.

Example: the same NPC may be a Mawla, creditor of a Prestação and political sponsor, provided each layer has its own valid authority and acquisition.

No one-to-one conversion is mandatory.

A relationship becomes the concrete identity of a mechanical option only when:

1. a legal mechanical option exists;
2. the character possesses the required allocation;
3. the relationship is coherent with that option;
4. the link is explicitly established in ordinary tabletop terms.

Reputation adjectives do not determine a trait by themselves.

A respected character may have formal Status, Reputação Paralela, Influence or only narrative reputation depending on actual authority.

The same applies to enemies, patrons, debts, allies and institutional relationships.

## N. Complete-sheet invariant and numeric allocation deferment

Specialist C does not set XP or the final distribution tables for Attributes, Skills, Disciplines, Advantages/Flaws or other sheet values.

However, Character Creation as a whole **must** eventually define concrete sheet values and how they are distributed.

Both modes must produce a complete character sheet.

C owns the invariant that both modes must end in a complete legal sheet, coherent history and V5 Relationship Map, and that narrative does not replace mechanical allocation.

**USER-APPROVED DOWNSTREAM DESIGN DIRECTION — OWNER RATIFICATION REQUIRED:** the Rápido route should reach that endpoint through a direct/accelerated construction path, while the Guiado route should use played pre-chronicle history as part of its construction path. Exact allocation order, sequencing and conversion procedures remain owned by G/H and final integration by K.

Ratifying owners: **G, H, K**.

If those owners discover a conflict, they must escalate it to the Senior Editor rather than silently overriding `CHAR-C-011`.

## O. Office Functional Fit

Office Functional Fit is a qualitative design validation between what an office actually requires and the character’s combination of:

- personal capability;
- institutional capability;
- delegation;
- relationships;
- dependencies;
- vulnerabilities.

No universal Attribute, Skill, Discipline or Power Envelope floor exists for an office.

An office holder may function through radically different combinations of personal and institutional capacity.

The following table is an **internal editorial guardrail** for designing and auditing characters and storylines. It is not a mandatory published character-creation form.

| Office requirement | Personal capacity | Institutional capacity | Delegation | Dependency | Vulnerability | Internal result |
|---|---|---|---|---|---|---|
| functional need | how the character solves it directly | what the office/institution supplies | who performs it for them | what/person they rely on | how the arrangement can fail | FIT / GAP / CONDITIONAL |

A useful internal test is to remove formal office authority and ask whether the character remains coherent as a person. They need not remain equally powerful.

C owns only the Functional Fit invariant and the rule that the editorial table is not a mandatory player form.

**USER-APPROVED DOWNSTREAM DESIGN DIRECTION — OWNER RATIFICATION REQUIRED:** Rápido may use concise validation gateways for office choices, and Guiado may integrate Functional Fit through played-history situations rather than exposing this internal table directly.

Ratifying owners: **G** for Quick procedure; **H** and **D1/D2** where Guided/played-history procedure is involved; **K** for final publication/integration exposure.

Exact gateway behavior, prompt embedding, ordering and player-facing wording are not finalized by C.

## P. Exceptional social, political, institutional and territorial assets

Specialist C does not create a second rarity scale.

When a materially extraordinary asset needs evaluation, C supplies B’s Asset Portfolio/Rarity Debt with a causal profile using these qualitative dimensions:

- **source** — how it was obtained;
- **control** — ownership, command, access, influence, custody, temporary use or mere association;
- **maintenance** — what keeps it functioning;
- **dependency** — people/institutions/resources it relies on;
- **exposure** — political, social, Masquerade or hostile visibility created by it;
- **reach** — practical geographical/social extent;
- **vulnerability** — how it can be reduced, blocked or lost.

These dimensions are editorial audit tools, not a player worksheet.

C describes the asset’s structure; B judges exceptionalism under the Power Envelope.

Access through office does not automatically become personal property. Institutional assets may disappear when office, patronage, legitimacy or institutional access is lost.

## Q. Rootedness × political legitimacy

Rootedness can make local trust or political claims more plausible but never produces formal legitimacy automatically.

Formal legitimacy remains owned by the system that recognizes it:

- Status → Chapter 05;
- office → political authority;
- Dignitas → Ventrue authority;
- Prestações → relational/Chapter 05 authority;
- Influence/Background → common mechanical allocation;
- Reputação Paralela → its own political sphere.

C owns the invariant that improbable combinations remain legal when independently authorized but require coherent provenance.

**USER-APPROVED DOWNSTREAM DESIGN DIRECTION — OWNER RATIFICATION REQUIRED:** the Quick route may express that need through concise explanatory gateways for combinations such as `newcomer + high office + no visible source of authority`.

Ratifying owners: **G** for Quick procedure and **K** for final integration/exposure. C does not finalize gateway mechanics or placement.

## R. Internal guardrails and player-facing gateways

### R.1 C-owned approved invariant

C owns the following now-normative invariant:

- internal validation taxonomy must not automatically become player-facing bureaucracy;
- downstream procedures must preserve C's social/territorial legality and final-state requirements;
- Rápido and Guiado must terminate in the same legal/social ontology;
- later procedures may consume C guardrails without exposing C's full editorial taxonomy as a mandatory form.

C does **not** own exact Quick gateway behavior, exact Guided prompt embedding, UI/exposure, procedure ordering or mandatory player-facing checks.

### R.2 User-approved downstream direction

**USER-APPROVED DOWNSTREAM DESIGN DIRECTION — OWNER RATIFICATION REQUIRED**

The already-approved direction is:

- Rápido may use brief, contextual, natural-language gateways when compressed creation needs additional provenance validation;
- Guiado may absorb equivalent guardrails into ordinary-language played-history prompts, choices and consequences;
- neither route should expose editorial fields such as `dependency`, `source`, `Functional Fit state` or comparable production metadata as a universal player checklist.

This direction is approved project memory. It is not a mere suggestion and must not be silently ignored.

### R.3 Required downstream ratification

- **G** — owns exact Quick gateway implementation, count, timing, ordering and wording;
- **H** — owns exact Guided integration;
- **D1/D2** — own played-history prompt/event mechanics where those guardrails are implemented through history;
- **K** — owns final publication/integration exposure and contradiction validation.

### R.4 Escalation rule

If G, H, D1/D2 or K discovers that the approved direction cannot be implemented without violating a stronger authority, the owner must:

1. preserve the C-owned invariant;
2. identify the exact incompatibility;
3. cite `CHAR-C-015`;
4. return the conflict to the Senior Editor.

The owner may refine implementation inside its scope but may not silently discard the approved direction.

## S. Guided storyline: initial scope and mutability

### S.1 C-owned approved invariant

C owns the semantics of the social/territorial states, not the event machinery used to produce them.

The following are normative now:

- social and territorial states may genuinely change across a character's pre-chronicle history;
- history may establish, transform, weaken, lose or restore states where the governing authority permits;
- a historically true state is not automatically a currently active state;
- finalization must validate the 2010 endpoint under each state's own authority;
- fictionally unresolved conditions such as a contested claim may remain uncertain, but the final sheet cannot remain mechanically undefined.

Therefore:

`historically true ≠ currently active`

and:

`narratively earned ≠ mechanically free`

A historically held office may have been lost. A historical affiliation may be former. A Prestação may have been paid. A patron may have become an enemy. A relationship may matter only to biography.

### S.2 User-approved downstream direction

**USER-APPROVED DOWNSTREAM DESIGN DIRECTION — OWNER RATIFICATION REQUIRED**

The user-approved direction preserved from `CHAR-C-016` is that the Guiado route should:

- begin with explicit player/Narrator inputs sufficient to delimit the scope of the character before played-history prompts begin;
- allow those inputs to be broad or highly constrained;
- organize future prompts/provocations into smaller, bounded sets or scopes rather than one unlimited pool;
- use manual tabletop eligibility instructions so impossible, repeated or premise-incompatible prompts are not used;
- treat initial premise plus already-established fictional facts as constraints on later prompt eligibility;
- adapt *Thousand Year Old Vampire* as concise structural inspiration rather than reproduce an endless solo chronicle.

Examples of possible initial constraints include an open character, a Methuselah older than Gilgamesh, a Thin-Blood Embraced moments ago, an unknown Sire, unknown Embrace circumstances, a predetermined office, a newcomer premise or a chronicle rule that characters do not know how they were Embraced.

These examples preserve design intent only. C does not define the final prompt catalogue, event pools, branching, sequencing or filtering procedure.

### S.3 Required downstream ratification

- **D1** — Played History Core: base event/prompt unit, agency/randomization fundamentals and core eligibility machinery;
- **D2** — Played History Finalization/Integration: final prompt taxonomy, late transitions and integration after E/F;
- **H** — Guided Creation: complete Guided assembly and user-facing Guided procedure;
- **F** — historical eligibility/revelation constraints where protected chronology or knowledge states restrict what prompts may establish.

### S.4 Escalation rule

If D1, D2, H or F finds a conflict between this approved direction and its governing authorities, it must not silently replace the direction.

It must cite `CHAR-C-016`, identify the conflict and return it to the Senior Editor.

## T. Minimum final social/territorial state

Every completed PC or NPC must contain enough social/territorial state to exist immediately in Novydres.

The conceptual minimum is:

- current Rootedness;
- current Bairrismo/exposure state, even if not consolidated;
- sufficient current territorial placement;
- minimum political/social position, including valid states such as unaligned or peripheral;
- enough materially relevant relationships for a functional V5 Relationship Map.

The following remain conditional rather than universally mandatory:

- Marco Territorial;
- domain;
- specific faction/institution affiliation;
- Personal Status;
- office;
- Dignitas;
- Prestações;
- patron;
- enemy;
- structured reputation;
- exceptional assets.

This is an ontological completeness requirement. It does not require the published character sheet to expose C’s internal fields.

## U. V5 Relationship Map

The “mapa de relacionamentos” in this architecture means the **Relationship Map of Vampire: The Masquerade V5 used at the tabletop**.

It is not an executable graph, database, dependency DAG or engine.

### U.1 C-owned approved invariant

C owns the requirement that the character-creation endpoint contain a coherent **current social relationship state** that can be represented on the V5 Relationship Map.

C also owns these semantics:

- materially relevant present-day relationships must be representable;
- the same person may participate in multiple simultaneous relationship roles without becoming several duplicate people;
- a narrative relationship does not automatically create a mechanical trait;
- historical relationships without current material relevance need not occupy the active 2010 Relationship Map;
- removing a defunct relationship from the active 2010 map does not erase its history.

C does not own the exact construction/update procedure by mode.

### U.2 User-approved downstream direction

**USER-APPROVED DOWNSTREAM DESIGN DIRECTION — OWNER RATIFICATION REQUIRED**

The approved direction is:

- the Rápido route should construct the initial V5 Relationship Map directly from the completed character state, history and relevant relationships;
- the Guiado route should be able to build and alter the V5 Relationship Map progressively as materially relevant relationships emerge;
- Guided finalization should consolidate the active map around relationships that still matter at the start of the chronicle.

This remains a manual TTRPG direction, not a software algorithm.

### U.3 Required downstream ratification

- **G** — exact Quick Relationship Map construction procedure;
- **H** — exact Guided construction/update procedure;
- **E** — temporal persistence, transformation, loss and survival of relationships across long histories;
- **K** — final integration and publication consistency.

### U.4 Escalation rule

If G, H, E or K finds an incompatibility, it must cite `CHAR-C-019` and return the conflict to the Senior Editor rather than silently overriding the approved direction.

## V. Social-state matrix

The following matrix is an internal consolidation aid.

| State | May be absent? | May be historical only? | Historically mutable under C semantics? | Current authority | Automatic mechanical grant? |
|---|---:|---:|---:|---|---:|
| Rootedness | no, final current state required | yes, trajectory may contain prior states | yes | Power Scale + C | no |
| Bairrismo exposure/consolidation | no, current condition required | yes | yes | project Bairrismo authority + C interface | no |
| Marco Territorial | yes | yes | yes | upstream Marco/Bairrismo authority + C timing | no |
| current raion/placement | no | yes | yes | Atlas/Play Guidance + C interface | no |
| feeding/domain rights | yes | yes | yes | upstream territorial/legal authority | no |
| affiliation | yes | yes | yes | Chapters 04–06 | no |
| Personal Status | yes | yes | yes | Chapter 05 | no |
| office | yes | yes | yes | Chapter 05 / competent political authority | no personal power |
| Positional Status | conditional on office | yes | yes | Chapter 05 | only as already defined by office |
| Dignitas | yes | yes | yes | Ventrue authority | no |
| Prestações | yes | yes | yes | Chapter 05 | no |
| patron/enemy/reputation relation | yes individually | yes | yes | fiction + applicable mechanics | no |
| exceptional asset | yes | yes | yes | A/B + source authority | no |
| Relationship Map relation | minimum relevant network required | yes | yes | V5 Relationship Map procedure | no |

## W. Relationship mapping matrix

This matrix is editorial guidance for mapping fiction to existing mechanics. It is not a mandatory published table.

| Fictional relationship | Possible mechanical/interface representation | Automatic? | Notes |
|---|---|---:|---|
| mentor/patron | Mawla, Ally, Contact, narrative only | no | allocation must be independently legal |
| rival/enemy | Enemy/Adversary where legal, narrative only | no | rivalry alone does not create dots |
| political sponsor | Status provenance, Mawla, Influence, narrative | no | layers remain separate |
| creditor/debtor | Prestação, ordinary debt, institutional duty | no | Prestação requires Chapter 05 validity |
| institutional superior | affiliation, office dependency, Mawla, narrative | no | affiliation does not grant authority automatically |
| territorial ally | Ally/Contact, shared domain relation, narrative | no | residence does not imply domain |
| reputation source | Personal Status, Reputação Paralela, narrative reputation | no | adjective alone does not select mechanic |
| Sire | V5 relationship, lineage/generation authority, Mawla if separately allocated | no | Sire existence does not automatically create Mawla |
| Touchstone | V5 Touchstone | conditional | use common V5 legality; Marco remains separate/special |
| Marco Territorial | adapted place Touchstone interface | conditional | requires eligibility; does not replace all ordinary Touchstones |

## X. Downstream interfaces

### X.1 C → D1/D2 — Played History state-transition interface

C supplies:

- Rootedness, Bairrismo/Marco, affiliation, Status, office, Dignitas, Prestações and relationship state semantics;
- historical/current distinction;
- state-transition legality constraints;
- the invariant that history may create causal facts but cannot manufacture illegal mechanics or authority;
- `CHAR-C-016` as a **USER-APPROVED DOWNSTREAM DESIGN DIRECTION — OWNER RATIFICATION REQUIRED** concerning initial inputs, bounded prompt scopes and manual eligibility.

D1/D2 decide event units, prompt pools/taxonomy, filtering/eligibility machinery, branching, sequencing and final played-history implementation.

They must not silently ignore `CHAR-C-016`; incompatibility requires Senior Editor escalation.

### X.2 C → E — Relationship / temporal-persistence interface

C supplies:

- present-day relationship destinations that must be representable;
- distinction between historical truth and current active relationship/state;
- permission for historical relationships without current material relevance to leave the active 2010 V5 Relationship Map without being erased from history;
- Rootedness/territorial-state semantics independent of age entitlement;
- `CHAR-C-019` as a downstream direction where temporal persistence affects final-map relevance.

E decides temporal relationship persistence, transformation, loss, mortal lifespan effects, descendants, memory/identity continuity and long-horizon change architecture.

### X.3 C → F — History / revelation constraint interface

C supplies local state semantics and the approved `CHAR-C-016` direction that played-history scope must respect premise and established facts.

F owns canon chronology, Historical Reach, protected truths, knowledge states and revelation eligibility. F may constrain what historical prompts are eligible but may not silently erase the approved direction; conflict returns to the Senior Editor.

### X.4 C → G — Quick Creation

C supplies:

- required final social/territorial states and distinctions;
- legality/provenance constraints for Status, offices, territorial rights, relationships and exceptional assets;
- requirement for complete playable endpoint and V5 Relationship Map;
- `CHAR-C-015` and `CHAR-C-019` Quick-specific clauses as **USER-APPROVED DOWNSTREAM DESIGN DIRECTION — OWNER RATIFICATION REQUIRED**.

G owns the **Quick procedure**: exact sequence, shortcuts, gateway mechanics, timing, count, wording and Relationship Map construction procedure.

C does not finalize those implementation details.

### X.5 C → H — Guided Creation

C supplies:

- required final social/territorial state;
- historical/current state semantics;
- complete-character endpoint requirements;
- `CHAR-C-015`, `CHAR-C-016` and `CHAR-C-019` Guided-specific clauses as **USER-APPROVED DOWNSTREAM DESIGN DIRECTION — OWNER RATIFICATION REQUIRED**.

H owns the **Guided procedure**: exact assembly, prompt integration, user-facing sequencing, completion logic and Relationship Map update procedure, consuming D1/D2/E/F as required by the DAG.

C does not finalize those implementation details.

### X.6 C → I — NPC application and depth

C supplies the same social/territorial ontology for PCs and NPCs.

I decides NPC application/depth profiles, abbreviation policy and role-dependent completeness over the two existing modes. I does not create a third mode.

### X.7 C → J2 — Coterie creation integration

C supplies individual social/territorial states and relationship distinctions relevant to coterie integration.

J2 decides coterie creation architecture, shared Domain/history/patrons/enemies/advantages/flaws/relationships and group territorial/political placement.

### X.8 C → K — Final integration / publication

K must verify:

- exactly two modes: Rápido and Guiado;
- both terminate in complete playable characters;
- C-owned invariants survive downstream implementation;
- no implementation silently contradicts `CHAR-C-015`, `CHAR-C-016` or `CHAR-C-019`;
- approved downstream directions are either ratified/refined by their proper owners or escalated with an explicit conflict;
- `APPROVED DIRECTION ≠ FINAL DOWNSTREAM IMPLEMENTATION`;
- `OWNER RATIFICATION ≠ PERMISSION TO IGNORE USER-APPROVED DIRECTION`;
- the V5 Relationship Map remains a tabletop artifact, not a runtime engine;
- internal editorial taxonomies are not automatically published as mandatory bookkeeping;
- no third NPC/social/history ontology is introduced.

K owns final integration, terminology/schema normalization, contradiction detection and publication-level validation; it does not retroactively grant C implementation authority over G/H/D/E.

## X.9 Corrective governance validation

Ownership-sensitive active text was audited after the patch.

No final-authority claim remains that assigns to C:

- exact Quick gateway implementation;
- exact Guided prompt implementation;
- Played History prompt pools/filtering/branch sequencing;
- Relationship Map construction/update procedure.

Approved direction references remain only with explicit owner-ratification status.

Comparable but non-equivalent wording was noted in `CHAR-C-004`, `CHAR-C-008`, `CHAR-C-011`, `CHAR-C-012` and `CHAR-C-014`. Those decisions already function as C state/interface constraints or explicit deferments; their material meanings were not changed by this patch.

## Y. Question closure matrix — CHAR-CREATE-Q-030–042

| Question | Closure | Authority / decision |
|---|---|---|
| `CHAR-CREATE-Q-030` | RESOLVED BY CHAR-C DECISION | `CHAR-C-001`; Rootedness qualitative creation classification |
| `CHAR-CREATE-Q-031` | RESOLVED BY CHAR-C DECISION | `CHAR-C-002`; local/locally formed Bairrismo starting treatment |
| `CHAR-CREATE-Q-032` | RESOLVED BY CHAR-C DECISION | `CHAR-C-003`; newcomer Bairrismo acquisition interface |
| `CHAR-CREATE-Q-033` | RESOLVED BY CHAR-C DECISION | `CHAR-C-004`; Marco Territorial selection timing |
| `CHAR-CREATE-Q-034` | RESOLVED BY EXISTING PROJECT AUTHORITY | Marco as special/additional place Touchstone interface; not ordinary Touchstone replacement |
| `CHAR-CREATE-Q-035` | RESOLVED BY CHAR-C DECISION | `CHAR-C-005`; raion/current placement without domain conflation |
| `CHAR-CREATE-Q-036` | RESOLVED BY CHAR-C DECISION | `CHAR-C-006`; modular affiliation timing/interface |
| `CHAR-CREATE-Q-037` | RESOLVED BY CHAR-C DECISION | `CHAR-C-007`; Personal Status at creation |
| `CHAR-CREATE-Q-038` | RESOLVED BY CHAR-C DECISION | `CHAR-C-008`; office and Positional Status at creation |
| `CHAR-CREATE-Q-039` | RESOLVED BY CHAR-C DECISION | `CHAR-C-009`; Dignitas at creation |
| `CHAR-CREATE-Q-040` | RESOLVED BY CHAR-C DECISION | `CHAR-C-010`; Prestações at creation |
| `CHAR-CREATE-Q-041` | RESOLVED BY CHAR-C DECISION | `CHAR-C-011`; narrative/mechanical relationship mapping |
| `CHAR-CREATE-Q-042` | RESOLVED BY CHAR-C DECISION | `CHAR-C-012`; Office Functional Fit |

All C-owned inventory questions are closed.

## Z. Iskander/Zoya calibration

Iskander Yasupov and Madame Zoya are **non-normative stress-test profiles**.

They are used to ask whether the architecture can represent socially and politically complex characters without:

- converting their exceptional states into ordinary baselines;
- reopening already approved profiles automatically;
- writing ad hoc exceptions merely to fit them;
- confusing institutional reach with personal supernatural power.

For either profile, a mismatch must first be classified as one of:

1. architecture defect;
2. valid exceptional/outlier state;
3. missing provenance detail;
4. actual conflict with upstream authority.

Only category 4 is a retroactive reopening trigger by itself.

The forward-looking test is:

> Could Rápido or Guiado, using the final common architecture, produce a structurally equivalent character without bespoke rules?

Exact reverse engineering of every existing sheet value is not required at C.

## AA. Retro triggers

Specialist C identifies the following retro triggers for Senior Editor handling:

1. a later node changes the upstream definition of Rootedness or couples it mechanically to age/power;
2. the Bairrismo/Marco authority later contradicts C’s creation-time assumptions;
3. Chapter 05 changes Recognition, Status, office or Prestações in a way that invalidates C interfaces;
4. Ventrue/Dignitas authority changes the separation between Dignitas and court Status;
5. final Quick/Guided design requires a third social ontology or third NPC creation mode;
6. final mechanical allocation proves unable to produce a complete sheet in one or both modes;
7. final V5 Relationship Map guidance conflicts with the current common output contract;
8. Iskander/Zoya stress testing reveals an actual upstream contradiction rather than mere exceptionalism;
9. publication design attempts to expose internal editorial matrices as mandatory player-facing bookkeeping.

These are triggers for revalidation, not automatic reopening verdicts.

## AB. Explicit deferments — not blockers

The following remain downstream by design:

- exact Quick creation sequence and gateway mechanics — **G**, with K integration;
- exact Guided prompt/provocation catalogue and user-facing procedure — **H**, consuming D1/D2/E/F;
- exact prompt scopes, event pools, eligibility rules, branching and sequencing — **D1/D2/H**, with F constraints where applicable;
- exact Relationship Map construction/update procedure — **G/H**, with temporal persistence owned by **E** and final integration by **K**;
- exact concrete sheet-value allocation and distribution;
- XP/advancement rules;
- exact published names for internal states where not already canonical;
- final sheet layout;
- final Relationship Map presentation/examples;
- complete Bairrismo mechanic;
- complete Marco mechanic;
- complete Dignitas catalogue;
- NPC depth-profile presentation.

Where `CHAR-C-015`, `CHAR-C-016` or `CHAR-C-019` supplies an approved downstream direction, deferment transfers implementation authority but does **not** permit the owner to ignore the direction. Owner incompatibility must be escalated to the Senior Editor.

## AC. Blockers

**None identified.**

No unresolved Specialist C decision remains necessary before downstream design.

## AD. Final verdict

**READY FOR SENIOR EDITOR REVALIDATION**

Specialist C preserves closure of `CHAR-CREATE-Q-030–042` and supplies a stable social, territorial and political creation interface for PCs and NPCs.

The architecture preserves upstream authority, TTRPG usability, Quick/Guided parity, full-character completion, V5 Relationship Map integration, causal exceptionalism and the separation between fictionally earned history and mechanically legal final state.