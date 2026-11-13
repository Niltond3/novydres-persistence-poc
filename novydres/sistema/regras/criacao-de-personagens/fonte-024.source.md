---
document_id: novydres_character_creation_novydres_architecture_audit
version: 0.1.4
status: candidate_for_senior_editor_revalidation
date: 2026-08-21
scope: character_creation_novydres_architecture_audit_RETRO_Q092_propagation
supersedes: novydres_character_creation_novydres_architecture_audit_v0_1_3.md
corrective_scope: RETRO-Q092_scope_boundary_handoff_and_execution_surface_registration_only
substantive_decision_surface_changes: Q092_active_meaning_reclassified_without_inventory_expansion
target_gap: character_creation_novydres_architecture
target_milestone: character_creation_architecture_pre_design_audit
generation_gate: mandatory
npc_generation_status: blocked
companion_inventory: novydres_character_creation_architecture_decision_inventory_v0_1_3.md
final_verdict: READY_FOR_SENIOR_EDITOR_REVALIDATION
---

# Novydres Character Creation Architecture — Pre-Design Audit v0.1.3

## A. Executive assessment

**Workstream size:** exceptional / project-level.  
**Complexity:** very high.  
**Recommended state:** `MULTI-SUBAGENT DECOMPOSITION REQUIRED`.

The target is one common character model consumed by exactly two character-creation modes — **Quick/Rápido** and **Guided/Guiado** — and by supporting architecture for played history, coteries, NPC application/depth profiles, and future Chapter-07 generation/revalidation. Both creation modes may create PCs or NPCs; NPC is a use/depth/application dimension, not a third creation procedure.

Primary upstream authorities:

- `novydres_npc_power_scale_citywide_v0_1_1.md`;
- `novydres_npc_power_scale_citywide_decisions_v0_1.md`;
- `novydres_standalone_rules_contract_v0_1.md`;
- `novydres_play_guidance_contract_v0_1.md`;
- `novydres_revelation_architecture_contract_v0_1.md`;
- `05_concilio_leis_status_prestacoes_v0_2_2.md`;
- current Chapter-07 revalidation and patched Iskander/Zoya profiles;
- `novydres_editorial_map_v0_9_4.json`;
- current chronology, Atlas, factions, institutions and local-mechanics sources.

Primary risks:

1. parallel PC/NPC creation architectures emerging instead of one common model and two shared modes;
2. age becoming hidden XP through lifepath accumulation;
3. Guided Creation becoming mechanically stronger than Quick Creation;
4. played history becoming a competing canon/truth source;
5. local social/territorial rules being duplicated or silently redesigned;
6. official V5 coverage being reduced to one book;
7. old NPC profile conventions being mistaken for final creation law;
8. coterie creation becoming detached from the common model;
9. the output schema being fixed too early by one specialist;
10. mega-grill failure through unrelated decisions in one chain.

No architectural ambiguity currently blocks decomposition. **No auditor-level grill is required.**

### A.1 Documentary startup note

`novydres_prompt_reuse_contract_v0_1.md` was located in the current documentary authority chain and is part of the governing authority set for this audit. No successor was identified for this corrective patch. The audit uses it by documentary pointer and does not reproduce its contents.

No final character rule is approved by this audit.

### A.2 RETRO-CHAR-A-001 propagation

Specialist A subsequently closed `CHAR-A-011`: Novydres has exactly two character-creation modes, `Rápido` and `Guiado`, and both may create PCs or NPCs. `CHAR-A-012` further fixes `QUICK ⊆ GUIDED ⊆ COMMON MODEL`.

This v0.1.2 propagates that approved authority without reopening any `CHAR-CREATE-Q-*` surface:

- G owns Quick/Rápido;
- H owns Guided/Guiado;
- I owns NPC application/depth profiles over G/H;
- I is downstream of both G and H;
- no NPC-only creation engine, ontology or legality layer exists.

### A.3 RETRO-Q092 propagation

The approved 2026-08-21 scope retcon separates **Quick Character Creation** from a distinct **Quick Coterie Creation** DEU. This is a procedure-surface separation, not a third character-creation mode and not a new coterie ontology.

`CHAR-CREATE-Q-092` remains historically preserved under G, with active meaning narrowed to the Quick Character ↔ Quick Coterie boundary/handoff. J2 remains the coterie architecture authority. No new `CHAR-CREATE-Q-*` ID is created.

The separate Quick Coterie DEU is registered as an execution/publication surface consuming J2 + the G character endpoint + C + Play Guidance, and later K. It is **not added as a new specialist DAG node in this patch**. If the Senior Editor later requires a first-class node, that requires explicit registration and a fresh cycle check.

## B. Existing authority inventory

### B.1 Standalone character-creation contract

Already decided:

- Novydres is an operational standalone product.
- Exactly two compatible character-creation modes are mandatory: **Guided/Guiado Creation** and **Quick/Rápido Creation**.
- Both modes may create PCs or NPCs.
- Quick Creation is an accelerated interface over the same mechanical architecture.
- NPC depth/application is not a third creation mode.
- Creation owns procedure/order/preconditions/derived values; catalogues retain authority over individual options.
- Supported creation must cover the V5 fields needed for a complete playable character.
- Official source admission is broad but versioned; new official material does not enter silently.
- Official options, selected homebrew, supersession and errata require explicit provenance/normalization.

Not decided: exact allocation, exact source inventory, detailed step sequence, fast-mode shortcuts, Guided internals.

### B.2 Play Guidance interface

Already decided:

- Play Guidance precedes mechanical creation and produces positioning inputs.
- Inputs may include local/newcomer/mixed insertion, raion/territory, political posture, faction/institution ties, obligations and coterie identity.
- Both creation routes must consume compatible inputs and return completed characters/coterie.
- Played creation inspired structurally by *Thousand Year Old Vampire* is preserved as future specialist work.
- Play Guidance does not own character mechanics or hidden truths.

### B.3 Power Scale integration contract

Shared PC/NPC invariants already decided:

1. Generation, age and Blood Potency are distinct.
2. Time creates opportunity, not automatic dots.
3. Exceptional mechanics require acquisition and trajectory.
4. Resources require origin, maintenance and vulnerability.
5. Institutional authority is not personal mechanical strength.
6. Rootedness/Bairrismo are not functions of age or BP.
7. Historical depth does not grant omniscience.
8. Weaknesses do not purchase exceptional power.
9. Relevant power needs a legible operational identity plus dependency/constraint.
10. Sheet mechanics should emerge from trajectory, not receive biography retroactively written to justify arbitrary numbers.

NPC-only citywide controls remain NPC/setting-side: demographic pyramid, rarity distribution, exception register/density, saturation, clan/raion population asymmetry, presence-state accounting and NPC-generation gates.

Relevant future NPCs require a **pre-sheet Power Envelope** and a **post-sheet audit**. Different resolution depths are allowed.

### B.4 Bairrismo and Marco Territorial

Already decided:

- Bairrismo exists as Novydres project canon.
- Its approved implementation uses V5-compatible Conviction/Touchstone/Humanity spaces.
- It is not a numeric Power Scale trait.
- Rootedness predicts exposure; age, Generation and BP do not set intensity.
- A territorial Conviction may anchor to city, raion, institution, community or place.
- Locally formed vampires may begin with a territorial Conviction.
- Outsiders normally move through rootedness milestones before consolidated Bairrismo.
- Marco Territorial is a preferred, not mandatory, Touchstone-like anchor.
- Marco Territorial does not create or automatically intensify Bairrismo.

Character Creation must operationalize these rules, not redesign them.

### B.5 Status, offices, Dignitas and Prestações

Current authority establishes:

- Status/Recognition and court offices remain local political systems;
- positional Status does not automatically imply personal mechanical power;
- accumulated offices do not accumulate positional Status; higher positional Status prevails, with equivalent offices allowing choice of exercised Status;
- Prestações remain recognized social obligations with four grades and contextual, non-mathematical equivalence;
- Dignitas Ventrue is outside Chapter 05 and belongs to future Ventrue material.

Character Creation may define selection/application interfaces. If it changes Chapter-05 caps, Recognition acquisition or creation-time Status incompatibly, that becomes a controlled retroactive trigger.

### B.6 Revelation architecture

Already decided:

- reader access and truth state are distinct internal layers;
- objective resolution has one truth home when resolved;
- player-facing material cannot certify hidden truth;
- rumors remain epistemic forms, not truth labels;
- minimal functional restatement is allowed; competing authority is forbidden;
- progressive revelation may move through increasingly privileged information without exposing internal truth labels;
- Dramatis Personae remains authoritative for NPC presentation/statistics/local information layers;
- Character Creation must not become a new truth home for setting secrets.

### B.7 Chapter-07 architecture

Already retained:

- main, secondary and legendary profile classes;
- simplified dependent/stat-block treatment where justified;
- completion is multidimensional: editorial, narrative, mechanical, revelation-safety, production/layout;
- Iskander and Zoya are current v0.9 profiles with specific mechanical work still pending;
- broad new NPC generation remains blocked by this character-creation gate.

### B.8 Coteries

J1 canonical research and J2 coterie architecture have since closed their approved scope. J2 is the sole coterie architecture authority for Domain reconciliation, group-owned traits/liabilities, shared-history integration, relationship density, Collective Power Profile audit, and final group-output surfaces.

RETRO-Q092 does not reopen J2. It only separates the **Quick Coterie Creation DEU** from **Quick Character Creation** and preserves G as owner of the character-side handoff. Formal juridical formation in Novydres points to Chapter 05 → `Leges Coterium`; this audit creates no new coterie law.
## C. Unresolved decision inventory

The companion artifact `novydres_character_creation_architecture_decision_inventory_v0_1_2.md` records **134** unresolved question IDs.

Material clusters:

- canonical V5 creation baseline and source admission;
- PC/NPC power envelopes;
- local social/territorial/political integration;
- played-history unit, prompt engine, scaling, agency and loss;
- memory/relationship/temporal persistence;
- chronology/revelation integration;
- Quick Creation;
- Guided Creation integration;
- NPC creation application/depth profiles;
- coterie creation;
- final ontology/schema/integration validation.

No row is an approved rule.

## D. Dependency graph

### D.1 Corrected specialist DAG

```text
A  Core V5 Baseline
├──> B  Character Power Envelope
├──> C  Social/Territorial/Political Integration
└──> J1 Coterie Canonical Baseline (research preflight; no question ownership)

B + C + J1
└──> D1 Played History Core

A + C + D1
└──> E  Memory/Relationships/Temporal Persistence

C + D1 + E
└──> F  History/Chronology/Revelation Integration

B + C + D1 + E + F
└──> D2 Played History Finalization / Integration

A + C + D2 + E
└──> J2 Coterie Creation Architecture

A + B + C + J2
└──> G  Quick Creation

A + B + C + D2 + E + F + G + J2
└──> H  Guided Creation Mode / Integration

A + B + C + D2 + E + F + G + H + J2
└──> I  NPC Creation Application & Depth Profiles

G + H + I + J2 + D2
└──> K  Final Integration & Validation
```

D1 and D2 are two execution phases under one broader Played History specialist domain. J1 is research-only; J2 is the sole coterie decision owner.

**RETRO-Q092 DAG note:** topology is unchanged. The Quick Coterie DEU is a downstream execution/publication surface under J2 authority and G-boundary consumption, not a new specialist node. Therefore no edge or cycle change is introduced by this patch.

### D.2 Parallelization

Safe parallel research:

- A canonical V5 inventory;
- C documentary extraction of local rules;
- J1 canonical coterie-source baseline after A establishes admission/provenance method;
- D1 copyright-safe TYOV design-principle research once B/C boundaries are available;
- F chronology/revelation source mapping may begin as documentary research before E closes, but F material decisions close only after E.

Unsafe parallel decision work:

- B before A establishes the V5 legality/source baseline;
- E/F before D1 supplies the played-history core state model they consume;
- D2 before both E and F close;
- J2 shared-history decisions before D2;
- G before J2 where the Quick Character ↔ coterie boundary/handoff requires J2 authority;
- H before D2/E/F/G/J2 interfaces close;
- I final application/depth contract before both Quick and Guided mode outputs are available;
- K before all terminal specialist outputs are approved.

### D.3 DAG validity

Machine-level validation of the corrected execution nodes reports:

- self-dependencies: **0**;
- direct cycles: **0**;
- indirect cycles: **0**.

The correction also removes three additional pre-existing execution cycles exposed by full validation: B↔I, G↔I and G↔H. Their question text is unchanged; only ownership/dependency metadata was corrected.
## E. V5 research requirements

The audit confirms that the V5 Core is necessary but insufficient as the only source. Current official Player's Guide material explicitly revisits character/coterie creation, consolidates clans absent from the Core, expands Discipline/ritual/alchemy/Oblivion options and adds coterie systems and additional Predator Types.

| Research surface | Classification | Audit requirement |
|---|---|---|
| Core character-creation procedure | `CORE V5 BASELINE REQUIRED` | Recover exact canonical sequence, allocations, derived values and legality. |
| Attributes | `CORE V5 BASELINE REQUIRED` | Exact baseline required. |
| Skills | `CORE V5 BASELINE REQUIRED` | Exact baseline required. |
| Specialties | `OFFICIAL EXPANSION REVIEW REQUIRED` | Core legality + admitted-source additions. |
| Disciplines / Powers | `OFFICIAL EXPANSION REVIEW REQUIRED` | Core + admitted later powers; creation must not duplicate catalogue text. |
| Advantages | `OFFICIAL EXPANSION REVIEW REQUIRED` | Consolidated admitted-source inventory required. |
| Backgrounds | `OFFICIAL EXPANSION REVIEW REQUIRED` | Consolidated admitted-source inventory required. |
| Merits | `OFFICIAL EXPANSION REVIEW REQUIRED` | Consolidated admitted-source inventory required. |
| Flaws | `OFFICIAL EXPANSION REVIEW REQUIRED` | Consolidated admitted-source inventory required. |
| Convictions | `NOVYDRES LOCAL INTEGRATION REQUIRED` | Core baseline plus Bairrismo interface. |
| Touchstones | `NOVYDRES LOCAL INTEGRATION REQUIRED` | Core baseline plus Marco/long-history persistence. |
| Humanity | `NOVYDRES LOCAL INTEGRATION REQUIRED` | Core baseline plus local/historical interaction. |
| Predator Types | `OFFICIAL EXPANSION REVIEW REQUIRED` | Core + later official types + selected homebrew/local review. |
| Generation | `NOVYDRES LOCAL INTEGRATION REQUIRED` | Canonical legality plus Power Scale invariants. |
| Blood Potency | `NOVYDRES LOCAL INTEGRATION REQUIRED` | Canonical bounds/trajectory plus Power Scale. |
| Coteries | `OFFICIAL EXPANSION REVIEW REQUIRED` | Core + Player's Guide + any other admitted group options. |
| Clan-specific creation effects | `OFFICIAL EXPANSION REVIEW REQUIRED` | All supported clans; normalize later official presentations. |
| Loresheet interactions | `OFFICIAL EXPANSION REVIEW REQUIRED` | Admission + creation timing + Revelation interface. |
| Status / Dignitas | `NOVYDRES LOCAL INTEGRATION REQUIRED` | Local authority, not generic V5 baseline. |
| Standalone source-admission policy | `ALREADY RESOLVED` | Broad versioned admission with `ADMITTED/SUPERSEDED/PARTIAL/EXCLUDED`. |
| Bairrismo / Marco baseline | `ALREADY RESOLVED` | Procedure integration remains open; substantive local rule does not. |
| Non-supported splats/options | `OUT OF SCOPE` | Unless later explicitly admitted. |

### E.1 Canonical research discipline

Future V5 specialist must:

- use official/current primary sources;
- record source/version/provenance;
- distinguish errata/supersession;
- avoid assuming Player's Guide exhausts every option in every admitted book;
- output an admission/dependency inventory, not a copied rules corpus;
- hand full operational rule text to its proper standalone catalogue/rules authority, not to creation procedure by duplication.

## F. Thousand Year Old Vampire adaptation requirements

Audit-only external research supports these abstract inspiration points:

- solo roleplaying/journaling orientation;
- long chronological sweep;
- memory and loss as central themes;
- prompt-driven play;
- simple resource tracking;
- semi-random progression through prompts;
- optional group play.

Mandatory adaptation surfaces:

1. prompt-driven biography without copied prompts;
2. event consequences feeding later state;
3. chronological compression;
4. relationship entry/change/loss;
5. acquisition/loss without unlimited mechanical growth;
6. memory/forgetting as an explicit later choice, not automatic transplant;
7. solo-native procedure converted for collaborative tabletop use;
8. scaling for young, ancilla, elder and legendary histories;
9. random discovery balanced against player agency;
10. V5 legality and Novydres canon constraints;
11. conversion from temporary lifepath state into the shared character model.

### F.1 Copyright-safe research rule for future specialist

- research *Thousand Year Old Vampire* as inspiration only;
- identify abstract mechanisms in research notes;
- cite research sources internally where appropriate;
- do not reproduce prompts, tables or large rule passages;
- do not recreate its navigation/prose as a near-identical substitute;
- create original Novydres/V5 mechanics and prompt families;
- distinguish inspiration from implementation.
## G. PC/NPC common-core analysis

The common core is a design target to validate, not a completed schema.

Shared foundations must include at least:

- identity and category/clan legality;
- Generation/BP legality;
- core mechanical fields;
- moral architecture;
- relationship/asset provenance;
- Novydres social/territorial placement when applicable;
- trajectory/acquisition causality;
- common terminology;
- common output ownership.

Legitimate differences may exist in depth, number of resolved fields, amount of history, publication exposure, citywide rarity audit, protected-envelope handling and degree of mechanical completeness.

NPC-specific population controls must not be imposed automatically on PCs. PC/NPC differences should be application/depth/governance differences over the same two modes, not a second ontology or a third NPC-only mode.

## H. Quick/Guided mode analysis

Binding: **exactly two creation modes exist: Quick/Rápido and Guided/Guiado**. Both may create PCs or NPCs and must remain compatible with the same common model.

Later design must close:

- minimum common fields;
- common legality checks;
- Quick shortcuts;
- Guided-only historical state;
- Quick → Guided upgrade;
- whether history discovers or contextualizes mechanics;
- parity preventing Guided from becoming systematically stronger;
- how both consume Play Guidance positioning;
- how both return compatible character/coterie state.

No allocation method is chosen here.

## I. Played-history architecture problem map

Independent surfaces:

- event unit;
- chronological progression;
- age/event-density scaling;
- quiet-period compression;
- torpor compression;
- prompt taxonomy;
- stateful branching;
- randomization;
- agency/reroll/veto;
- mechanical consequence ceilings;
- negative/loss architecture;
- relationship mutation;
- memory/forgetting;
- present-day asset validity;
- present-day Touchstone validity;
- identity/Mask replacement;
- canon-event eligibility;
- protected-truth handling;
- Beckoning exposure;
- Historical Peak versus current profile;
- collaborative execution;
- safety/content control;
- final conversion to canonical output.

This is too large for one undifferentiated grill.

## J. Coterie integration analysis

Coterie creation deserves a dedicated specialist because it touches official V5 group mechanics, shared Domain, local territory, political positioning, collective resources, shared history, relationship graph and Power Scale collective audit.

It should not be invisibly absorbed into Guided PC creation: Quick must also interoperate with it, and official group options require their own provenance review.

## K. Power Scale integration

Non-negotiable interfaces:

- `Generation ≠ age ≠ BP`;
- no retrospective XP;
- trajectory/acquisition for exceptional mechanics;
- vector-based power, not one score;
- office/institutional power separate from personal mechanics;
- resources/assets require source and dependencies;
- relevant NPCs use pre-sheet Power Envelope + post-sheet audit;
- `Unknown stays Unknown`;
- protected legendary envelopes remain bounded;
- NPC demographic/rarity controls remain setting-side;
- Character Creation cannot silently alter Power Scale.

Conflict protocol:

`POWER SCALE INTERFACE CONFLICT`

Stop that rule and return it to Senior Editor. Do not patch Power Scale inside Character Creation.

## L. Bairrismo/Marco integration

Creation needs application rules, not a Bairrismo redesign.

Later work must distinguish locally formed Cainite, long-term resident, newcomer, chronicle-start arrival, NPC rootedness, current territorial Conviction, possible Marco Territorial, loss/re-anchoring history, present Touchstones, and history-generated belonging milestones.

No new numeric Bairrismo trait is presumed.

## M. Revelation integration

Played creation is a high-risk revelation surface.

Mandatory guardrails:

- creation events may establish character experience without certifying protected setting truth;
- objective secrets remain in their truth homes;
- player-facing history may encode belief, rumor, partial knowledge or witnessed surface facts;
- Storyteller-only interventions may reference protected material without copying the answer into player outputs;
- Historical Reach does not equal objective knowledge;
- titles, tables, navigation and prompt eligibility must not leak secret resolutions;
- generated biography must not silently override Chapters 02–06 canon.

## N. Mechanical-envelope risks

1. age converted to free XP;
2. event count converted to mechanical advantage;
3. lost traits used as currency for stronger traits;
4. rare Discipline access justified by generic history;
5. BP derived directly from years undead;
6. office converted to Discipline/BP/Attribute floor;
7. lineage converted to mastery;
8. Guided mode yielding more dots than Quick;
9. legendary mystery used to justify unlimited stats;
10. temporary/historical assets retained as current Background dots;
11. lifepath `Resource`/`Skill` terminology colliding with V5 traits;
12. coterie complementarity erasing meaningful gaps.

## O. History/canon integration risks

- impossible participation dates;
- false omniscience;
- accidental objective resolution of rumors;
- protected secrets copied into character history;
- multiple incompatible versions of city events;
- ancient NPCs receiving every historical affiliation;
- characters retaining every mortal relationship indefinitely;
- assets surviving centuries without maintenance explanation;
- present-day Touchstones being dead historical contacts;
- Beckoning/Torpor used as arbitrary shortcuts;
- generated history changing raion/clan/institution canon.
## P. Output-schema ownership

Final schema is not established here.

| Output family | Primary future owner | Sources consumed |
|---|---|---|
| Creation procedure/order | Character Creation architecture | Standalone + Play Guidance |
| Core V5 mechanical legality | Standalone rules/catalogues | Official V5 |
| Generation/BP envelope | Character Power Envelope | V5 + Power Scale |
| Attributes/Skills/Specialties | Core V5 creation + catalogues | V5 |
| Disciplines/Powers | Authoritative rules catalogue | V5/admitted sources; creation only selects |
| Advantages/Backgrounds/Merits/Flaws | Authoritative catalogues | V5/admitted sources |
| Bairrismo/Marco | Existing local authority | Creation only applies |
| Status/Prestações/offices | Chapter 05 | Creation only interfaces |
| Dignitas | Future Ventrue authority | Creation only interfaces |
| Faction/raion/institution facts | Chapters 03–06 | Creation consumes |
| Played-history temporary state | D + E | Converts into final output |
| Hidden setting truths | Revelation-designated truth homes | Creation references, never owns |
| NPC presentation | Chapter 07 | NPC application/depth contract feeds it |
| Coterie group state | J + Play Guidance interface | V5 + local territory/politics |
| Final common schema | K | All approved specialist outputs |

## Q. Retroactive dependency candidates

No chapter is reopened by this audit.

| Interface | Classification | Possible trigger | Current contradiction? |
|---|---|---|---|
| Chapter 01 | consumption / future implementation | material onboarding responsibility proven missing | No |
| Chapter 02 | consumption + candidate dependency | guided history needs new authoritative chronology distinction or detects conflict | No |
| Chapter 03 | consumption | territorial creation requires semantic geography/domain change, not reference | No |
| Chapter 04 | consumption | mandatory affiliation contradicts faction authority | No |
| Chapter 05 | **candidate retroactive trigger** | changes Status cap, Recognition, creation-time Status, office authority or legal operation | No |
| Chapter 06 | consumption + candidate dependency | creation-time institution/faith rule contradicts current authority | No |
| Play Guidance | future implementation dependency | exact positioning/output fields synchronize after creation closes | No; explicitly deferred |
| Standalone Rules | direct implementation dependency | detailed procedure/source inventory must instantiate contract promises | No |
| Revelation Architecture | consumption | only a genuinely missing global revelation case | No |
| Format Contract | consumption / later production | stable workflow proves need for new production/DEU behavior | No |
| Editorial Map | mandatory living-memory update after approval | approved decomposition/final architecture changes gates/dependencies/pointers | Not content contradiction |
| Chapter 07 | mandatory downstream revalidation | after architecture closes, mechanics and depth modes become applicable | No |

## R. Proposed subagent decomposition

Smallest coherent decomposition remains **11 specialist domains**, including final integration. D and J now expose explicit execution phases so the topology is acyclic; no new substantive specialist domain was created.

| ID | Specialist / execution phase | Exact scope | Size | Rough decision range |
|---|---|---|---|---|
| A | Core V5 Creation Baseline & Admission Interface | V5 core + admitted-source character-building baseline; procedure/catalogue interface; no local redesign. | large | 18–25 |
| B | Character Power Envelope | Generation, age, BP, older-PC/NPC envelopes, Discipline/mechanical-load interface with Power Scale. | large | 18–28 |
| C | Social, Territorial & Political Integration | Bairrismo, Marco Territorial, raion/domain, faction, Status, Dignitas, Prestações, offices and institutions at creation. | large | 20–30 |
| D1 | Played History Core | Core event unit, time/scaling architecture, base state, agency/randomization fundamentals, mechanical-envelope interface and safety baseline. | large | 12–20 |
| E | Memory, Relationships & Temporal Persistence | Memory model, relationship graph, mortal lifespan, descendants, identity/Mask continuity, terminology and lasting consequences. | large | 20–30 |
| F | History, Chronology & Revelation Integration | Canon-event participation, Historical Reach, protected truths, knowledge states and Beckoning/history interfaces. | large | 15–25 |
| D2 | Played History Finalization / Integration | Canon-aware/memory-aware branching, final prompt taxonomy, late state transitions and finalized engine integration after E/F. | medium | 8–15 |
| J1 | Coterie Canonical Baseline | Canonical research/input baseline only; no project-decision ownership. | small | research preflight |
| J2 | Coterie Creation Architecture | Authority for shared Domain/history/patron/enemy/advantages/flaws/relationships and territorial/political group placement; consumed by separate Quick Coterie surface. | large | 15–25 |
| G | Quick Character Creation | Fast individual-character route derived from the common model; owns Q-092 character-side coterie boundary/handoff only; does not create coterie. | medium | 10–18 |
| H | Guided Creation Mode / Integration | Guided assembly of the common model for PCs or NPCs, including finalized played history where applicable, local integration, coterie interface, fairness and completion. | large | 15–25 |
| I | NPC Creation Application & Depth Profiles | Main, secondary, legendary, dependent, recurring-official and minor NPC application/depth profiles over Quick/Guided; same common model. | large | 15–25 |
| K | Final Integration & Validation | Contradiction detection, terminology normalization, common schema and all final validation passes. | medium | 10–18 |

### R.1 Why not fewer?

- A+B would mix canonical provenance with local balance and exceed a coherent grill.
- D remains one specialist domain but requires D1/D2 execution phases because E/F legitimately consume its core and its finalization legitimately consumes E/F.
- F inside D would make canon/revelation a side concern of prompt design.
- G+H would weaken independent validation of the fast route.
- I remains separate from H to prevent PC-first assumptions, but I is an NPC application/depth specialist over Quick/Guided, not a third mode designer.
- J remains one specialist domain; J1 is research-only and J2 owns all decisions, preventing the former J→J ambiguity.
- K must remain dedicated; producing agents should not be sole judges of integration.

### R.2 Ownership matrix

| Phase | Owns | Explicitly does not own | Expected artifact class | Stop condition |
|---|---|---|---|---|
| A | Canonical creation baseline, admission/provenance, selection interfaces | Power Scale changes; full catalogue prose | V5 baseline/research inventory + decisions if grilled | supported fields have source/provenance and procedure boundaries |
| B | Starting/advanced envelopes and Power Scale legality interface | population canon; final history engine | power-envelope architecture + decisions | legal envelopes and validation hooks closed |
| C | Local social/territorial/political application | redesign of Bairrismo/Marco/Chapter 05 | local integration architecture + decisions | every local input has timing/ownership without upstream change |
| D1 | Played-history core unit, time/scaling, base event state, agency/randomization fundamentals, envelope interface | memory persistence final model; canon-safe final branching; final prompt taxonomy | played-history core phase + decisions | E/F can consume a stable core without needing D2 |
| E | Memory, relationships, identity and temporal persistence | canon history selection; core V5 allocation | temporal-persistence architecture + decisions | long-horizon state terminates in valid present-day outputs |
| F | Canon chronology, Historical Reach and Revelation integration | new secrets; chronology rewrite | history/revelation integration + decisions | history can interact with canon without truth leakage |
| D2 | Final played-history branching/state/prompt integration requiring E/F | reopening D1 fundamentals; changing E/F decisions | played-history finalization phase + decisions | finalized engine consumes E/F without cycles |
| J1 | Official coterie source/admission research | project coterie rules or creation decisions | canonical baseline research note/input | J2 has an explicit sourced baseline |
| J2 | Coterie construction and group outputs; authority consumed by Quick Coterie surface | individual allocation; faction rewrites; J1 provenance decisions | coterie architecture + decisions | V5/local-compatible group output feeds separate Quick Coterie/Guided/Play Guidance surfaces |
| G | Quick Character Creation + Q-092 character-side coterie handoff | coterie construction; new ontology; extra budget; final NPC reuse decision | quick-character architecture + decisions | fast individual path yields common-schema legal output and a clean coterie handoff |
| H | Guided Creation assembly over the common model for PCs or NPCs, including Quick→Guided upgrade interface | NPC citywide controls; catalogue duplication; NPC depth taxonomy | guided-mode architecture + decisions | finite, fair common-schema output |
| I | NPC application/depth profiles, required completeness by NPC role, choice of Quick versus Guided by profile, two-pass audit, revalidation protocol | third NPC creation procedure; NPC-only legality; separate NPC ontology; new Power Scale; NPC-only Played History engine | NPC application/depth contract + decisions | all Chapter-07 classes consume governed Quick/Guided paths over the common model |
| K | Integration, terminology, schema and validation | new feature invention outside approved inputs | final integrated architecture + validation | one model passes all closure tests |

### R.3 Grill ceiling

Recommended default: **15–30 materially related decisions** per specialist grill.

D is explicitly split for execution: D1 carries 10 inventory surfaces and D2 carries 7. Neither phase requires a mega-grill. E remains 15 surfaces; F remains 12. J1 carries no project decision; J2 carries 9 surfaces.
## S. Proposed execution order

### Phase 0 — Senior Editor decomposition approval

Approve scope, 11 specialist-domain boundary, D1/D2 and J1/J2 phase topology, ownership, DAG, artifact classes and grill-size policy. No specialist execution before this gate.

### Phase 1 — Baselines

1. A — Core V5 Creation Baseline.
2. B — Character Power Envelope after A legality baseline.
3. C — Social/Territorial/Political Integration; documentary extraction may start alongside A.
4. J1 — Coterie Canonical Baseline research after A establishes source-admission method. No project decisions.

### Phase 2 — Played-history core

5. D1 — Played History Core after B/C and J1 inputs needed by collaborative execution.

### Phase 3 — Persistence and canon integration

6. E — Memory/Relationships/Temporal Persistence after D1.
7. F — History/Chronology/Revelation Integration after D1 and E.

Documentary chronology/revelation research may start earlier, but F decisions close only after E.

### Phase 4 — Played-history finalization and coterie

8. D2 — Played History Finalization / Integration after E and F.
9. J2 — Coterie Creation Architecture after D2 for shared-history questions and after E for relationship persistence.

### Phase 5 — Creation modes and NPC application

10. G — Quick Character Creation after A/B/C/J2 interfaces needed by its output and Q-092 boundary/handoff. The separate Quick Coterie DEU is not embedded in this step.
11. H — Guided Creation Mode / Integration after D2/E/F/G/J2.
12. I — NPC Creation Application & Depth Profiles after G and H, with the upstream B/C/D2/E/F/J2 outputs required by NPC depth/application decisions. I does not execute in parallel with H because it must consume both finalized creation modes.

### Phase 6 — Integration

13. K — Final Integration & Validation after G/H/I/J2/D2 terminal outputs.

Return to Main Senior Editor. Do not automatically resume NPC generation.
## T. Integration strategy

K must ingest approved specialist artifacts only. Terminal inputs are D2, J2, G, H and I plus the upstream approved A/B/C/E/F artifacts they consume. D1 and J1 remain traceable upstream phase inputs, not alternate final authorities.

Mandatory passes:

1. authority;
2. ontology;
3. V5 legality;
4. Power Scale;
5. local Bairrismo/Marco/Status/Dignitas/Prestações;
6. history/Historical Reach/current-vs-peak;
7. revelation;
8. Quick/Guided parity;
9. NPC application/depth, including confirmation that I consumes Quick/Guided rather than defining a third mode;
10. standalone operation;
11. publication ownership/no duplication;
12. retroactive dependency classification.

## U. Closure criteria for entire milestone

Milestone closes only when Senior Editor verifies:

- one common character ontology exists;
- exactly two creation modes exist: Quick/Rápido and Guided/Guiado;
- Quick and Guided are compatible;
- PC and NPC construction share that ontology and both consume those same two modes;
- NPC application/depth profiles do not create a third workflow;
- supported V5 creation fields have source/procedure;
- admitted official source coverage is explicit/versioned;
- Generation/age/BP/Disciplines obey Power Scale;
- age never becomes retrospective XP;
- played history scales finitely from young to ancient;
- history consequences cannot exceed approved mechanical envelopes;
- memory/relationships/temporal persistence produce valid 2010 outputs;
- Bairrismo/Marco application is clear without redesign;
- Status/Dignitas/Prestações/offices use non-competing interfaces;
- Coterie creation is integrated;
- protected truth remains protected;
- canon history cannot be overwritten silently;
- NPC depth profiles and two-pass audit are defined;
- existing-profile revalidation queue is actionable;
- retroactive dependencies are classified and only actual triggers reopen;
- final artifacts are standalone-operational;
- K reports no unresolved blocking contradiction.

### U.1 NPC-generation release condition

NPC generation resumes only after:

1. blocking specialist decisions close;
2. K integration passes;
3. Main Senior Editor approves final architecture;
4. required living-memory/editorial-map updates are applied;
5. Chapter-07 targeted revalidation prerequisites are recorded.

## U.1 RETRO-Q092 validation

- character-creation modes: **2** (`Rápido`, `Guiado`);
- Quick Character Creation creates coterie: **NO**;
- separate Quick Coterie surface registered: **YES**;
- J2 coterie authority preserved: **YES**;
- Q-092 lineage preserved: **YES**;
- inventory IDs: **134**;
- new question IDs: **0**;
- DAG nodes added: **0**;
- DAG edges changed: **0**;
- cycle status: unchanged from v0.1.3; **0 direct / 0 indirect / 0 self-cycles**.

## V. Senior Editor decisions required before delegation

- [ ] Approve/amend the 11 specialist-domain split.
- [ ] Approve A as V5 baseline/provenance owner and B as power-envelope owner.
- [ ] Approve C as local-interface owner without upstream redesign power.
- [ ] Approve D as one Played History domain executed as D1 → E → F → D2, with no duplicate question ownership.
- [ ] Approve J as one Coterie domain executed as J1 research preflight → J2 decision architecture; J1 owns no `CHAR-CREATE-Q-*`.
- [ ] Keep G/H as the only two creation-mode owners over one common model.
- [ ] Approve `Q-093` under I and `Q-094` under H as topology corrections only.
- [ ] Keep I as NPC application/depth-profile specialist, not a third-mode or parallel-system designer.
- [ ] Require I to consume both finalized G and H outputs before closing NPC application/depth decisions.
- [ ] Keep K mandatory and downstream of all terminal outputs.
- [ ] Approve 15–30 related decisions as normal grill ceiling.
- [ ] Approve corrected DAG/order with 0 direct, self or indirect cycles.
- [ ] Accept `CHAR-CREATE-Q-*` as questions-only memory; count remains 134.
- [ ] Do not authorize Chapter 01–06 reopening from this audit.
- [ ] Keep Chapter-07 generation blocked.
# Existing-profile future revalidation queue

## Tier 1 — targeted after architecture closure

### Iskander Yasupov

Review later:

- Generation 8 / BP 4 envelope;
- Discipline Depth/Breadth/Power Density and unresolved power dependencies;
- Bairrismo/rootedness application;
- Beckoning exposure/trajectory;
- office Functional Fit versus personal mechanics.

Do not regenerate from zero by default.

### Madame Zoya

Review later:

- Generation 11 / BP 2 envelope;
- Discipline/ritual breadth and unresolved ritual dependencies;
- Bairrismo/rootedness application;
- multi-office Functional Fit while preserving non-cumulative positional Status;
- existing Revelation protections.

### Vasya Ivanoff

Review later:

- protected-envelope treatment;
- historical/Beckoning trajectory;
- Presence State and Shadow/Legacy distinction.

## Tier 2 — complete when generated under the new contract

Principal/main queue: Kuthulun, Bispo Konstantin, Wilhelmina Harker, Dom Sebastião de Avis, Miriam Abramovich, Fatima al-Faqadi, Zara/Zarina, Sergei Orlov, Khalil Al-Rashid.

Secondary/dependent queue: Mikhail Vasiliev, Mariya Vasilieva, Leah ben Avraham when independent treatment is operationally required, plus future recurring officials/dependents.

Legendary/protected queue: Gilgamesh, Levi, Baba Yaga, Durga Syn. Bound scale without inferring protected mechanics.

# External research note

Audit-only checks performed 2026-08-11:

- Renegade Game Studios — *Vampire: The Masquerade 5th Edition Core Rulebook* current product page.
- Renegade Game Studios — *Vampire: The Masquerade 5th Edition Player's Guide* current product page and official update.
- Tim Hutchings — *Thousand Year Old Vampire* official itch.io/product descriptions.

These checks support the research inventory only. They do not insert copied V5 or TYOV rules into Novydres.

# Final verdict

`READY FOR MULTI-SUBAGENT DECOMPOSITION REVIEW`