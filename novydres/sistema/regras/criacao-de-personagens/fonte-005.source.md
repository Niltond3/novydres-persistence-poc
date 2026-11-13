---
document_id: novydres_character_creation_d1_played_history_core_decisions
version: 0.1
status: candidate_for_senior_editor_revalidation
date: 2026-08-15
workstream: character_creation_novydres_architecture
execution_node: D1
scope: played_history_core_decision_ledger
companion_core_artifact: novydres_character_creation_d1_played_history_core_v0_1.md
decision_range:
  - CHAR-D1-001
  - CHAR-D1-019
final_verdict: READY_FOR_SENIOR_EDITOR_REVALIDATION
---

# D1 — Played History Core Decision Ledger

## 1. Decision ledger

| Decision ID | Q IDs | Upstream authority | Approved decision | Downstream consumers | Status |
|---|---|---|---|---|---|
| `CHAR-D1-001` | `Q-043` | A; B | Atomic unit is `Episódio de História`: `entrada → provocação → decisão/interpretação → consequência → saída`; Episode qualification criteria and driver/arbiter boundary refined by later D1 decisions | E; F; D2; H | APPROVED |
| `CHAR-D1-002` | `Q-044` | A; B; C | Every Episode resolves a significant historical question and outputs temporal position, relevant situation, character response and determined result plus at least one material output: state change, causal fact, relevant confirmation/revelation or pending consequence | E; F; D2; H | APPROVED |
| `CHAR-D1-003` | `Q-045` | B | Continuous chronology with flexible temporal jumps; jumps reposition the character and are neither events nor rewards; historical density and elapsed time are independent | E; F; D2; H | APPROVED |
| `CHAR-D1-004` | `Q-046` | B | Episode count/density scales by Significant Coverage: temporal span, historical complexity, initial/final-state complexity and chronicle premise; age expands space but does not determine count | E; F; D2; H | APPROVED |
| `CHAR-D1-005` | `Q-047` | B; E interface | Quiet periods are `Intervalos de Continuidade`, non-played time units that advance chronology and test persistence without fake events/XP; torpor remains D2-owned | E; F; D2; H | APPROVED |
| `CHAR-D1-006` | `Q-050`; supports `Q-043/044/053` | A; C | Marcos de Fechamento + eligibility by scope, state and incidence. Episodes occur inside Marcos; Provocation eligibility depends on current Marco, state, protected premises and incidence history; exhausted Provocations stop generating Episodes | E; F; D2; H | APPROVED |
| `CHAR-D1-007` | `Q-053` | A; B | Protected premise + constrained discovery. The engine may deliberately disrupt initial goals and help construct personal horror; aspirations may be frustrated, but protected premises are not contradicted gratuitously | D2; H | APPROVED |
| `CHAR-D1-008` | `Q-055` | B | Constructive Episodes may provisionally allocate/justify already-authorized mechanical capacity; later consequences may force trajectory review, but Episodes do not freely create/destroy the Power Envelope | E; D2; H | APPROVED |
| `CHAR-D1-009` | `Q-057` | Editorial governance | Content calibration is part of eligibility. Incompatible Provocations are ineligible in that form; an equivalent construction/disruption route should be used where possible. Refusal creates no mechanical debt | D2; H | APPROVED |
| `CHAR-D1-010` | `Q-058` | Play Guidance; J1 | Asymmetric collaborative authorship: player owns decisions/interiority; Storyteller owns external world/canon/validation; engine supplies pressure; other players may contribute without mandatory shared lifepath | J2; D2; H | APPROVED |
| `CHAR-D1-011` | `Q-043/044/046/050/053` | D1 architecture; C downstream direction | A Marco is a `Contrato de Construção`, not necessarily a chronological era. It has a verifiable construction objective and closes by sufficient coherent coverage rather than arbitrary event count | E; F; D2; H | APPROVED |
| `CHAR-D1-012` | `Q-044/050/053/055` | B; D1 architecture | Provocations may form an `Arco de Reincidência`: initial construction, later contestation, critical rupture/transformation. Repetition changes dramatic function rather than merely increasing intensity | E; D2; H | APPROVED |
| `CHAR-D1-013` | `Q-043/044/050/053` | D1 architecture; A/B/C constraints | Engine may materially redirect the character, but disruption must be causal, rooted in existing state, decisions, relationships, vulnerabilities, opportunities, pending consequences or external pressure | E; F; D2; H | APPROVED |
| `CHAR-D1-014` | `Q-044/045/046/050` | F boundary; D1 chronology | Main chronology + controlled retrospective insertions. Earlier Episodes may explain/recontextualize open historical intervals but cannot contradict closed facts or protected causality | E; F; D2; H | APPROVED |
| `CHAR-D1-015` | `Q-044/050/055` | A; B; C; E/F boundaries | Core State Model uses conceptual surfaces: chronology, premise, supernatural eligibility, C social/territorial state, relationship refs, provisional mechanical state, pending consequences, eligibility state and coverage state | E; F; D2; H | APPROVED |
| `CHAR-D1-016` | `Q-046/050/053` | D1 architecture | Marco closure uses three-axis sufficiency — Coverage, Coherence, Consequence — plus minimum structural coverage: every required construction surface must be visited at least once before closure | E; F; D2; H | APPROVED |
| `CHAR-D1-017` | `Q-044/050/055` | D1 architecture | Closing a Marco creates a `Pacote de Consolidação do Marco`; consolidated means current historical truth, not immunity from later pressure/transformation | E; F; D2; H | APPROVED |
| `CHAR-D1-018` | `Q-046/050/053/055` | D1 architecture | Every Marco has an `Alvo Funcional de Construção`: the condition the character/history must reach for later creation to operate; it defines the problem to solve, not the exact traits to receive | E; F; D2; H | APPROVED |
| `CHAR-D1-019` | `Q-044/050/055` | D1 architecture; E/D2 boundary | Unresolved consequences may persist as `Dívida Causal`, affecting future eligibility, disruption and constraints; they need not resolve immediately but cannot be forgotten for convenience | E; D2; H | APPROVED |

## 2. Decision details

### CHAR-D1-001 — Episode of History

Approved option: `OP3`.

The atomic unit is the `Episódio de História`.

It is large enough to change or reveal relevant state and small enough to chain repeatedly.

Conceptual form:

`state-in → Provocation → decision/interpretation → consequence → state-out`

An Episode is not necessarily a single scene and may cover variable duration.

User addendum preserved:

- examples must represent materially consequential historical play rather than weak illustrative incidents;
- downstream design must define qualification boundaries clearly;
- the engine's driver-versus-arbiter role is refined by `CHAR-D1-011` and `CHAR-D1-013`.

### CHAR-D1-002 — Significant resolution

Approved option: `OP3`.

Every Episode must resolve a relevant historical question.

Minimum resolved information:

- temporal position;
- relevant situation;
- character response;
- determined outcome.

At least one material output is required:

- state change;
- causal fact;
- relevant confirmation/revelation;
- pending consequence.

Mechanical change is not mandatory.

### CHAR-D1-003 — Flexible temporal advancement

Approved option: `OP3`.

Played History uses continuous chronology with variable jumps to the next historically relevant point.

Temporal jumps do not grant:

- XP;
- power;
- rewards;
- automatic events.

### CHAR-D1-004 — Significant Coverage scaling

Approved option: `OP3`.

History density is determined by the amount of trajectory that needs explanation rather than by age alone.

Primary factors:

- temporal span;
- historical complexity;
- complexity of the initial/final state;
- chronicle premise.

Age increases possible historical breadth without creating proportional Episode obligation.

### CHAR-D1-005 — Interval of Continuity

Approved option: `OP3`.

Quiet time uses a non-played `Intervalo de Continuidade`.

It asks what remains valid after elapsed time and can flag:

- continues;
- ends;
- changes;
- needs downstream resolution.

It does not define persistence.

Torpor remains deferred to D2.

### CHAR-D1-006 — Marcos + eligibility by scope/state/incidence

Approved option: revised `OP3`.

A Marco groups Provocations around a construction objective.

Eligibility depends on:

- active Marco;
- current state;
- protected premise;
- history already established;
- prior incidence of the Provocation.

Provocations may be exhausted.

D1 does not decide the final randomizer.

### CHAR-D1-007 — Protected premise + constrained discovery

Approved option: `OP3 + addendum`.

The player may define who the character intended to be.

The engine may guide the character toward who they actually became.

This deliberate disruption is part of personal horror from creation.

Protected premise is distinct from aspiration:

- protected premise cannot be contradicted gratuitously;
- aspiration may be frustrated, transformed or destroyed.

User-approved downstream direction recorded:

- navigation by two differently colored d10s is reserved for D2/Q-052;
- one die may encode forward motion and the other backward motion;
- exact implementation is not D1-final.

### CHAR-D1-008 — Provisional allocation inside Power Envelope

Approved option: `OP3`.

An Episode may establish historical cause for already-authorized mechanical expression.

Later Episodes may destroy the fictional condition supporting that expression.

This triggers review rather than creating an independent points economy.

`more Episodes ≠ more power`

### CHAR-D1-009 — Calibration as eligibility restriction

Approved option: `OP3`.

Content constraints make incompatible Provocations ineligible in their current form.

The engine should seek another way to fulfill the same dramatic/construction role.

Refusal of content:

- creates no mechanical debt;
- does not reduce completeness.

Final reroll/veto procedure remains D2-owned.

### CHAR-D1-010 — Asymmetric collaborative authorship

Approved option: `OP3`.

Player:

- character choices;
- interiority;
- subjective response;
- personal biography where not fixed.

Storyteller:

- external world;
- NPCs;
- canon;
- protected chronology;
- external consequences;
- validation.

Engine:

- pressure;
- prompts;
- recurrence;
- disruption.

Other players may contribute where shared history is relevant but no mandatory shared lifepath is established.

### CHAR-D1-011 — Marco as Construction Contract

Approved option: `OP3`.

A Marco is a higher-order construction unit defined by a verifiable objective.

It may be:

- conceptual;
- moral;
- relational;
- historical;
- territorial;
- monstrous;
- mixed.

It need not be a fixed chronological era.

### CHAR-D1-012 — Recurrence Arc

Approved option: `OP3`.

A Provocation may return with changing function:

1. construction;
2. contestation;
3. rupture/transformation.

D1 does not mandate exactly three incidences for every Provocation.

### CHAR-D1-013 — Causal, not arbitrary, direction

Approved option: `OP3`.

The engine may materially change the character's path, including against initial goals.

The change must be rooted in:

- existing state;
- prior decision;
- relationship;
- vulnerability;
- opportunity;
- pending consequence;
- external pressure;
- recurrence.

### CHAR-D1-014 — Main chronology + controlled retrospective insertion

Approved option: `OP3`.

A thematic Marco may investigate earlier periods without allowing unrestricted rewriting.

Retrospective insertion can add cause or recontextualize an open interval.

It cannot silently contradict closed facts.

### CHAR-D1-015 — Conceptual state surfaces

Approved option: `OP3`.

Core state groups:

1. chronology;
2. character premise;
3. supernatural eligibility state;
4. social/territorial references;
5. relationship references;
6. provisional mechanical state;
7. pending consequences;
8. eligibility state;
9. coverage state.

This is an editorial/system ontology only.

### CHAR-D1-016 — Three-axis sufficiency + minimum structural coverage

Approved option: `OP3 + addendum`.

Marco closure requires:

- Coverage;
- Coherence;
- Consequence.

Additionally, every required structural coverage element for that Marco must have been visited at least once.

This is not equivalent to consuming every possible prompt in the pool.

### CHAR-D1-017 — Marco Consolidation Package

Approved option: `OP3`.

A closing Marco produces a current historical snapshot that may include:

- historical synthesis;
- chronology;
- causal facts;
- concept/aspiration changes;
- relationships;
- social/territorial state;
- provisional mechanical state;
- pending consequences;
- downstream unresolved demands;
- future eligibility references.

Later Marcos may still transform it.

### CHAR-D1-018 — Functional Construction Target

Approved option: `OP3`.

Every Marco has a functional target describing which construction problem must be solved.

The target does not predefine the exact traits the character will receive.

### CHAR-D1-019 — Pending consequence as causal debt

Approved option: `OP3`.

An unresolved consequence can persist across:

- Marcos;
- Episodes;
- Intervals of Continuity.

It may:

- change eligibility;
- cause later disruption;
- constrain options;
- recur;
- worsen;
- resolve.

It cannot simply disappear because it is inconvenient.

## 3. Specialist-C downstream dispositions

| C decision | D1 disposition | D1 scope |
|---|---|---|
| `CHAR-C-015` | `RATIFIED WITH D1 SCOPE LIMIT` | Guided may embed C validation into natural-language Played History; UI/Quick/final exposure remain downstream |
| `CHAR-C-016` | `RATIFIED WITH D1 SCOPE LIMIT` | D1 ratifies explicit starting premises, bounded scopes, state eligibility and historical mutability; final prompt taxonomy/randomization/F chronology/H workflow remain with correct owners |
| `CHAR-C-019` | `DEFERRED TO CORRECT OWNER` | D1 outputs historical relationship references but does not define final Relationship Map construction/persistence/consolidation |

## 4. Closure matrix

| Q ID | Decision coverage | Closure |
|---|---|---|
| `CHAR-CREATE-Q-043` | `CHAR-D1-001`, `011`, `013` | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-044` | `CHAR-D1-002`, `012`, `014`, `015`, `017`, `019` | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-045` | `CHAR-D1-003`, `014` | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-046` | `CHAR-D1-004`, `011`, `014`, `016`, `018` | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-047` | `CHAR-D1-005` | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-050` | `CHAR-D1-006`, `011`, `012`, `013`, `014`, `015`, `016`, `017`, `018`, `019` | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-053` | `CHAR-D1-007`, `011`, `012`, `013`, `016`, `018` | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-055` | `CHAR-D1-008`, `012`, `015`, `017`, `018`, `019` | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-057` | `CHAR-D1-009` | `RESOLVED BY CHAR-D1 DECISION` |
| `CHAR-CREATE-Q-058` | `CHAR-D1-010` | `RESOLVED BY CHAR-D1 DECISION` |

## 5. Explicit downstream deferments

The following remain unresolved by D1:

- `Q-048` — torpor compression;
- `Q-049` — prompt-family taxonomy;
- `Q-051` — branching architecture;
- `Q-052` — randomization method;
- `Q-054` — reroll/veto/override policy;
- `Q-056` — negative-outcome/loss categories;
- `Q-059` — prompt-engine data dependencies/state transitions.

D1 also does not resolve E-owned persistence/memory/relationship questions or F-owned historical/revelation questions.

## 6. Potential retroactive triggers

`NONE CONFIRMED`

## 7. Blockers

`NONE`

## 8. Final verdict

`READY FOR SENIOR EDITOR REVALIDATION`