---
document_id: novydres_character_creation_d1_played_history_core
version: 0.1
status: candidate_for_senior_editor_revalidation
date: 2026-08-15
workstream: character_creation_novydres_architecture
execution_node: D1
scope: played_history_core
owns:
  - CHAR-CREATE-Q-043
  - CHAR-CREATE-Q-044
  - CHAR-CREATE-Q-045
  - CHAR-CREATE-Q-046
  - CHAR-CREATE-Q-047
  - CHAR-CREATE-Q-050
  - CHAR-CREATE-Q-053
  - CHAR-CREATE-Q-055
  - CHAR-CREATE-Q-057
  - CHAR-CREATE-Q-058
companion_decision_log: novydres_character_creation_d1_played_history_core_decisions_v0_1.md
final_verdict: READY_FOR_SENIOR_EDITOR_REVALIDATION
---

# D1 — Played History Core

## A. Scope and authority

This artifact defines the stable core engine of the Guided Played History system for Novydres character creation.

Played History is a component of the `Guiado` creation mode. It is not a third creation mode.

Exactly two creation modes remain authoritative:

1. `Rápido`;
2. `Guiado`.

Both remain subject to the common legality model and the same authorized Power Envelope.

D1 resolves only:

- `CHAR-CREATE-Q-043`;
- `CHAR-CREATE-Q-044`;
- `CHAR-CREATE-Q-045`;
- `CHAR-CREATE-Q-046`;
- `CHAR-CREATE-Q-047`;
- `CHAR-CREATE-Q-050`;
- `CHAR-CREATE-Q-053`;
- `CHAR-CREATE-Q-055`;
- `CHAR-CREATE-Q-057`;
- `CHAR-CREATE-Q-058`.

D1 does not close D2-, E-, F-, H-, J2-, G-, I- or K-owned questions.

## B. Upstream contracts

### B.1 Specialist A

Specialist A remains legality authority.

Played History may:

- establish fictional causes;
- establish historical facts;
- establish acquisition opportunities;
- explain how legal traits entered the character trajectory;
- produce provisional historical allocations for later consolidation.

Played History may not independently legalize:

- unsupported options;
- invalid Clan/Discipline combinations;
- illegal traits;
- extra mechanical allocations;
- unsupported starting states.

### B.2 Specialist B

Specialist B remains authority for:

- Generation;
- Blood Potency;
- Discipline Depth;
- Discipline Breadth;
- Power Density;
- Mechanical Load;
- Rarity Debt;
- Exceptional Start;
- Declared Outlier;
- the authorized Power Envelope.

Core invariant:

> Played History is not an XP generator.

More Episodes never imply more raw power.

### B.3 Specialist C

D1 consumes C's social, territorial and political state interfaces without redefining them.

Played History may establish or transform fictional circumstances around:

- Rootedness;
- Bairrismo;
- territorial placement;
- Marco Territorial eligibility/state;
- affiliation;
- office;
- Status provenance;
- Dignitas context;
- Prestações;
- patrons;
- enemies;
- reputation;
- obligations.

Their legality and exact meaning remain with C and the applicable upstream rule-home.

### B.4 J1

D1 preserves:

- coterie state may exist during character creation;
- Domain is not mandatory for every coterie;
- member contribution to shared traits must not be double-counted as a free historical reward;
- shared coterie mechanics are not the same as the Power Scale Collective Power Profile;
- no mandatory canonical shared lifepath was established.

D1 does not design J2.

## C. Played History design principles

The Played History engine follows these principles:

1. history is played selectively, not exhaustively;
2. relevance, not elapsed time, determines where narrative zoom is applied;
3. the engine must be finite;
4. age expands possible historical span but does not grant power or require proportional event count;
5. the player's initial concept is an intention, not a guarantee of final trajectory;
6. protected premises cannot be contradicted gratuitously;
7. the engine may become deliberately disruptive and may frustrate initial ambitions;
8. disruption must be causal, not arbitrary;
9. mechanical state may be expressed provisionally during history but remains bounded by the Power Envelope;
10. consequences may persist across later construction;
11. mature content limits constrain eligibility without eliminating dramatic consequence;
12. final implementation must remain usable as a tabletop procedure rather than requiring a software runtime.

## D. Atomic history unit

### D.1 Episode of History

The smallest played-history unit is the:

`Episódio de História`

Conceptual structure:

`ESTADO DE ENTRADA → PROVOCAÇÃO → DECISÃO/INTERPRETAÇÃO → CONSEQUÊNCIA → ESTADO DE SAÍDA`

An Episode is not necessarily a scene.

It may cover:

- a single moment;
- a night;
- a short chain of events;
- a prolonged crisis;
- a meaningful stretch of months or years.

Its scale is defined by historical relevance rather than elapsed duration.

### D.2 Qualification threshold

An Episode must resolve a historically meaningful question.

It is not enough for something merely interesting to have happened.

A candidate Episode must materially help explain, reveal, establish, transform or complicate the trajectory.

A practical test is:

> If this Episode were removed, would a materially relevant explanation, decision, consequence or state needed to understand the character's trajectory be lost?

If not, it is probably biographical texture rather than a full Episode.

### D.3 Driver versus arbiter

The engine may both guide and arbitrate character history, but at different levels:

- the Marco guides the construction problem being investigated;
- the Provocation introduces pressure;
- the Episode resolves the concrete historical impact;
- accumulated state limits and feeds later possibilities.

The engine may meaningfully redirect the character, but not through causally unrooted rupture.

## E. Unit input/output contract

Every Episode must resolve at minimum:

1. a temporal position or historically meaningful placement;
2. a relevant situation;
3. the character's response, decision or interpretation;
4. a determined result.

Every Episode must also produce at least one material output:

- state change;
- new causal fact;
- relevant confirmation/revelation about the trajectory;
- pending consequence.

An Episode does not need to:

- change every state surface;
- alter the final character sheet;
- award a trait;
- grant XP;
- create a permanent relationship;
- resolve all consequences it generates.

## F. Chronological advancement

### F.1 Flexible temporal advancement

Played History uses a continuous chronology with variable temporal jumps.

Structure:

`EPISÓDIO → SALTO TEMPORAL → NOVA POSIÇÃO TEMPORAL → PRÓXIMO EPISÓDIO`

The jump may span:

- hours;
- months;
- years;
- decades;
- centuries.

The jump itself is not:

- a reward;
- a cost;
- an Episode;
- an XP event.

It only repositions the trajectory.

### F.2 Independent variables

Historical density and elapsed time are independent.

A single week may contain several Episodes.

A century may contain none.

### F.3 Retrospective insertion

The main chronology remains authoritative, but Marcos may open controlled retrospective windows.

A retrospective Episode may be inserted into an earlier still-open interval to:

- explain;
- reveal;
- add cause;
- recontextualize.

It may not:

- contradict closed facts;
- silently invalidate later causality;
- violate protected premises;
- violate canon.

A navigation result that moves "backward" within a Marco does not automatically mean chronological time travel. D2 may later connect specific navigation results to retrospective insertion under this contract.

## G. Age-scaling model

Played History scales by:

`SIGNIFICANT COVERAGE`

not by fixed years-per-Episode.

Coverage is informed by:

1. temporal span;
2. historical complexity;
3. complexity of the desired initial/final state;
4. chronicle premise.

Age expands the possible historical space but does not determine Episode count.

Power Envelope complexity may increase causal explanation needs, but the Power Envelope is not an Episode counter.

The target is:

> sufficient historical coverage, not historical completeness.

## H. Quiet-period abstraction

### H.1 Interval of Continuity

A period in which nothing merits full play is represented as an:

`Intervalo de Continuidade`

Structure:

`ESTADO APÓS EPISÓDIO → INTERVALO DE CONTINUIDADE → ESTADO ANTES DO PRÓXIMO EPISÓDIO`

An Interval:

- advances time;
- does not create a Provocation;
- does not require a dramatic decision;
- does not generate XP;
- does not fabricate an event.

Its function is to test which states remain valid across elapsed time.

It may flag:

`CONTINUA / TERMINA / MUDA / EXIGE RESOLUÇÃO DOWNSTREAM`

D1 does not define how relationships, memories, identities, resources or other persistent objects survive such intervals.

Torpor remains D2-owned under `Q-048`.

## I. State eligibility prerequisites

### I.1 Marcos de Fechamento

Played History organizes Provocations inside higher-order construction units called:

`Marcos`

A Marco is not necessarily a chronological era.

It is a:

`CONTRATO DE CONSTRUÇÃO`

defined by a functional construction target.

Each Marco establishes:

- what must be understood or established;
- which state surfaces may be investigated;
- which structural coverage elements are required;
- which Provocations are compatible with the scope;
- what gaps still prevent closure.

### I.2 Functional construction target

Each Marco has an:

`Alvo Funcional de Construção`

This is the condition the history/character must reach so later creation can operate on it.

The Marco specifies the kind of construction problem that must be solved.

It does not preselect the exact traits or answers the character will end with.

### I.3 Eligibility contract

A candidate Provocation is evaluated against:

1. current Marco and its scope;
2. protected premises;
3. current chronological/supernatural state;
4. relevant social/territorial state;
5. already-established trajectory facts;
6. prior incidence history of that Provocation;
7. unresolved causal debts;
8. content-calibration limits;
9. constraints supplied by A/B/C/E/F as applicable.

Baseline result:

- `ELEGIBLE`;
- `INELIGIBLE`;
- `ELIGIBLE WITH REQUIRED VALIDATION`.

D1 does not define the final selection/randomization algorithm.

### I.4 Coverage before closure

A Marco cannot close merely because player and Storyteller are tired of it.

Before closure, every structural coverage element required by that Marco must have been visited at least once through an appropriate Episode/Provocation.

This does not mean:

- every possible prompt in the pool;
- every optional variant;
- every recurrence tier;
- every mutually exclusive branch.

It means that each minimum construction surface needed to reach the Marco's functional target has received at least one valid treatment.

## J. Player/Storyteller agency model

### J.1 Protected premise plus constrained discovery

The system uses:

`PREMISSA PROTEGIDA + DESCOBERTA CONSTRANGIDA`

The player has primary authority over:

- intended concept;
- protected premises established at the start;
- subjective interpretation;
- decisions made by the character;
- internal reactions;
- personal biographical details not fixed elsewhere.

The engine may:

- introduce unexpected Provocations;
- pressure existing elements;
- introduce opportunity, cost, accident and disruption;
- revisit previous elements from new angles;
- frustrate the character's initial aspirations;
- produce trajectory change.

The Storyteller has authority over:

- external world;
- NPC action;
- Novydres canon;
- protected chronology;
- external consequences;
- ambiguity resolution;
- mechanical validation under the correct authority.

### J.2 Personal horror from creation

The player may define who the character wanted to become.

Played History may determine that the final character became someone different.

This is intentional.

The engine should construct personal horror by allowing:

- aspirations to fail;
- strengths to generate costs;
- relationships to become liabilities;
- success to produce exposure;
- protective beliefs to become traps;
- earlier gains to become sources of later catastrophe.

However:

> disruption must arise from causality already present or plausibly introduced into the current state.

## K. Mechanical-consequence interface

### K.1 Provisional allocation inside the envelope

A constructive Episode may:

- justify;
- reveal;
- provisionally allocate;

part of the already-authorized mechanical budget.

Example conceptual relationship:

`authorized budget → historical cause → provisional expression`

The Episode is not awarding new power.

It is discovering where already-authorized character capacity came from.

### K.2 Later revision

A later Episode may:

- challenge;
- disable;
- destroy;
- transform;
- invalidate the current fictional basis;

of an earlier provisional expression.

The affected mechanical allocation then enters:

`trajectory review`

Potential final treatments may include, where allowed by the proper authority:

- actual loss;
- redistribution;
- conversion;
- temporary unavailability;
- replacement;
- transformation into another legal consequence.

D1 does not decide the final treatment.

### K.3 Invariant

> Episodes may undo earlier construction; they may not freely create or destroy the authorized Power Envelope.

### K.4 Mechanical categories exposed to the engine

An Episode may be classified conceptually as:

- purely historical fact;
- narrative consequence;
- justification for an already-authorized trait;
- acquisition opportunity;
- provisional allocation inside the envelope;
- attempted change requiring a B gateway.

## L. Content-calibration interface

Content limits become part of eligibility.

Possible constraints include:

- excluded subjects;
- fade-to-black or low-detail subjects;
- intensity ceilings;
- personal-horror sources that must not be used;
- subjects removed from eligibility during play.

A Provocation incompatible with those limits is not eligible in that form.

The engine must seek another valid way to perform the same construction/disruption function where possible.

Core invariant:

> Refusing a content theme creates no mechanical debt and does not make the character less complete.

D1 does not define the final veto/reroll/substitution procedure. That remains D2-owned under `Q-054`.

## M. Collaborative execution model

Played History uses:

`AUTORIA ASSIMÉTRICA COLABORATIVA`

### Player

Controls primarily:

- intention;
- choice;
- internal reaction;
- subjective interpretation;
- non-protected personal biography.

### Storyteller

Controls primarily:

- external world;
- NPCs;
- canon;
- protected chronology;
- external consequences;
- plausibility;
- legal/mechanical validation.

### Engine

Functions as pressure architecture.

It may:

- introduce questions;
- determine when a previously constructed element is challenged again;
- require constructive/disruptive/critical treatment where applicable;
- prevent the biography from remaining entirely under authorial control.

It does not decide the character's interiority.

It does not replace the Storyteller as narrator.

### Other players

May contribute when shared history or coterie state makes this useful.

Their participation:

- is not mandatory;
- does not grant authority over another character's interiority;
- does not establish a mandatory shared lifepath procedure.

J2 remains responsible for coterie integration.

## N. Core state model

D1 requires the engine to be capable of representing the following conceptual state groups.

This is an internal editorial/system model, not a mandatory player-facing schema.

### N.1 Chronological state

- current historical position;
- positioned Episodes;
- open intervals;
- closed facts protected from contradiction;
- retrospective insertion windows.

### N.2 Character premise

- initial concept;
- protected premises;
- initial aspirations;
- content calibration.

### N.3 Supernatural state

Only the state needed for eligibility, under the correct upstream authority.

Examples may include:

- mortal;
- Embraced;
- other legally resolved supernatural facts.

### N.4 Social/territorial state

References C-owned state as needed.

D1 does not redefine it.

### N.5 Relationship references

The engine may know that a relevant relationship exists or changed.

D1 does not define:

- final relationship ontology;
- persistence;
- death handling;
- descendant replacement;
- Touchstone validity.

### N.6 Provisional mechanical state

- authorized Power Envelope;
- portions currently provisionally expressed;
- causal justification;
- acquisition opportunities;
- gateway-needed changes.

### N.7 Pending consequences

Unresolved consequences may persist as:

`DÍVIDA CAUSAL`

They may:

- alter future eligibility;
- provide cause for later disruption;
- restrict possibilities;
- recur;
- worsen;
- resolve;
- become irrelevant only with sufficient cause.

They do not need immediate resolution.

They may not simply be forgotten for convenience.

### N.8 Eligibility state

- current Marco;
- active scope;
- prior Provocation incidence;
- exhausted Provocations;
- satisfied/unsatisfied conditions;
- content constraints.

### N.9 Coverage state

- structural coverage already visited;
- remaining meaningful gaps;
- whether the Marco is eligible for closure.

## O. Reincidence architecture

A Provocation may support an:

`ARCO DE REINCIDÊNCIA`

Its repeated incidence should change dramatic function rather than merely increase intensity.

Conceptual sequence:

### Initial incidence — construction

Establishes how an element:

- arose;
- was learned;
- was acquired;
- became part of the character.

### Later incidence — contestation

Shows when the same element:

- created cost;
- failed;
- generated exposure;
- caused dependency;
- worsened another problem.

### Critical incidence — rupture or transformation

May:

- destroy;
- transform;
- break;
- radically recontextualize;
- impose severe cost;
- redefine how the character relates to that element.

D1 does not require every Provocation to have exactly three incidences.

Final incidence counts and navigation behavior remain downstream.

When a Provocation has exhausted all materially distinct functions defined for it, it ceases to be eligible for generating a new Episode in that trajectory.

## P. Marco closure

A Marco becomes eligible for closure only after its required structural coverage has been visited at least once.

Player and Storyteller then apply a three-axis sufficiency test.

### P.1 Coverage

The Marco's functional target has been materially explored.

### P.2 Coherence

The result has no unresolved contradiction with:

- protected premises;
- established state;
- canon;
- Power Envelope;
- applicable social/territorial authority.

### P.3 Consequence

The Marco produced material that genuinely informs the trajectory.

This may include:

- state;
- causality;
- relationship;
- vulnerability;
- changed aspiration;
- pending consequence;
- provisional mechanical expression;
- materially important character understanding.

Closure does not require exhausting the full pool.

## Q. Marco consolidation package

When a Marco closes it produces a:

`PACOTE DE CONSOLIDAÇÃO DO MARCO`

Containing, where applicable:

- historical synthesis;
- chronological coverage;
- consolidated causal facts;
- changes in concept or aspiration;
- relevant relationship state;
- relevant social/territorial state;
- provisional mechanical expressions;
- pending consequences;
- unresolved owner-specific demands;
- references needed for future eligibility.

`Consolidated` means:

> current historical truth.

It does not mean:

> immune to later transformation.

Later Marcos may pressure, reinterpret, transform or destroy earlier established elements if causal and legally valid.

## R. D1 → E interface

E receives demands to decide persistence for:

- relationship changes;
- historical supporting figures;
- identities;
- resources;
- memories;
- capabilities/skill-like narrative constructs;
- consequences crossing long intervals;
- states requiring replacement logic.

D1 provides:

- Episode outputs;
- Interval of Continuity state checks;
- retrospective insertion demands;
- pending causal debts;
- Marco consolidation packages.

D1 does not decide:

- memory subsystem;
- memory capacity;
- forgetting;
- final relationship ontology;
- mortal relationship death handling;
- descendants as replacements;
- current Touchstone validity;
- identity replacement rules;
- resource persistence;
- final narrative terminology.

## S. D1 → F interface

F receives:

- flexible chronological advancement model;
- continuous chronology;
- controlled retrospective insertion;
- chronology fields required by Episodes;
- canon-sensitive input points;
- state eligibility concept;
- surfaces that may require Revelation filtering.

F must later decide:

- eligible canonical historical events;
- protected chronology access;
- Historical Reach;
- revelation-safe exposure;
- chronology-safe event families.

## T. D1 → D2 interface

### Frozen by D1

D2 may rely on:

- Episode of History as atomic unit;
- Episode minimum output contract;
- flexible temporal advancement;
- Significant Coverage scaling;
- Interval of Continuity;
- Marco as Construction Contract;
- Functional Construction Target;
- eligibility by Marco + state + premise + incidence + causal debt;
- controlled retrospective insertion;
- protected premise + constrained discovery;
- causal disruption;
- provisional mechanical allocation inside B envelope;
- content limits as eligibility constraints;
- asymmetric collaborative authorship;
- conceptual state model;
- recurrence arcs;
- three-axis Marco sufficiency;
- Marco consolidation package;
- pending consequence as causal debt.

### Still open for D2

D2 retains ownership of:

- `Q-048` torpor compression;
- `Q-049` final prompt-family taxonomy;
- `Q-051` final branching architecture;
- `Q-052` randomization method;
- `Q-054` reroll/veto/override policy;
- `Q-056` final negative-outcome/loss categories;
- `Q-059` final prompt-engine data dependencies and transitions.

### User-approved D2 design direction — not D1-final

A proposed navigation method uses two differently colored d10s.

Conceptual example:

- one die indicates forward movement within the current Marco;
- the other indicates backward movement;
- net displacement determines navigation.

A result such as `4 forward / 8 backward` could imply a net movement of four positions backward.

D1 records this only as a user-approved downstream direction for D2/Q-052.

D1 does not finalize:

- the exact formula;
- indexing;
- wraparound;
- edge behavior;
- exhausted-prompt handling;
- whether backward movement triggers retrospective chronology;
- reroll behavior.

## U. D1 → H interface

H receives:

### Required Played History inputs

- initial character concept;
- protected premises;
- authorized Power Envelope;
- applicable legality state;
- content calibration;
- relevant initial social/territorial state;
- starting chronological position;
- any already-known coterie/shared state where applicable.

### Terminal Played History outputs

- Marco consolidation packages;
- historical chronology;
- causal facts;
- provisional/finalizable mechanical history;
- unresolved consequence set;
- relationship references;
- social/territorial history inputs;
- downstream owner demands.

H must later decide:

- exact start-to-finish Guided workflow;
- placement relative to standard V5 creation steps;
- final presentation;
- Quick→Guided upgrade handling.

## V. Specialist-C downstream direction dispositions

### CHAR-C-015

Disposition:

`RATIFIED WITH D1 SCOPE LIMIT`

D1 ratifies that Guided creation may embed C legality/validation guardrails inside natural-language Played History rather than expose C's internal editorial taxonomy.

D1 does not ratify or define:

- final player-facing UI;
- Quick behavior;
- final H/K presentation.

### CHAR-C-016

Disposition:

`RATIFIED WITH D1 SCOPE LIMIT`

D1 ratifies:

- explicit initial premises;
- bounded Marco scopes;
- state-based eligibility;
- prevention of impossible/repeated/incompatible Provocations;
- historical mutability followed by endpoint consolidation.

D1 does not define:

- final prompt families;
- F-owned chronology safety;
- D2-owned branching/randomization;
- H-owned workflow presentation.

### CHAR-C-019

Disposition:

`DEFERRED TO CORRECT OWNER`

D1 supports the need for progressive historical relationship change and provides relationship-reference outputs.

However, the exact construction, temporal persistence and final consolidation of the V5 Relationship Map remain principally E/G/H/K-owned according to the approved split.

D1 does not create a graph engine or runtime representation.
## W. Question closure matrix

| Question ID | Authoritative question | D1 disposition |
|---|---|---|
| `CHAR-CREATE-Q-043` | Smallest played-history unit | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-044` | Unit minimum outputs | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-045` | Chronological advancement model | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-046` | Age-scaling model for event count/density | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-047` | Quiet-period abstraction | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-050` | Prompt sequencing prerequisites | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-053` | Player-choice versus constrained-random balance | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-055` | Mechanical-consequence budget interface | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-057` | Safety/content calibration layer | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-058` | Collaborative versus solo execution mode | `RESOLVED BY CHAR-D1 DECISION` |

Exactly ten D1-owned questions are accounted for.

## X. Validation matrix

| Validation item | Result |
|---|---|
| Exactly 10 D1-owned question IDs accounted for | PASS |
| No D2-owned question closed | PASS |
| No E-owned question closed | PASS |
| No F-owned question closed | PASS |
| No J2/G/H/I/K question closed | PASS |
| A/B/C/J1 authority unchanged | PASS |
| No XP-per-Episode engine | PASS |
| No age=power formula | PASS |
| No fixed simulation-per-year requirement | PASS |
| No final prompt taxonomy | PASS |
| No final branching architecture | PASS |
| No final randomizer | PASS |
| No memory subsystem designed | PASS |
| Exactly two creation modes remain | PASS |
| Played History remains component of Guided | PASS |
| Collaborative tabletop compatibility | PASS |
| Original design, not TYOV transcription | PASS |

## Y. Potential retroactive triggers

`NONE CONFIRMED`

No actual contradiction with A, B, C or J1 was identified.

## Z. Blockers

`NONE`

## AA. Readiness verdict

`READY FOR SENIOR EDITOR REVALIDATION`