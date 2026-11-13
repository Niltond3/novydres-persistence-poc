---
document_id: novydres_character_creation_h_guided_pc_integration
version: 0.1
status: candidate_for_senior_editor_revalidation
date: 2026-08-21
scope: character_creation_h_complete_guided_pc_integration
execution_node: H
target_gap: character_creation_novydres_architecture
owns_questions:
  - CHAR-CREATE-Q-094
  - CHAR-CREATE-Q-096
  - CHAR-CREATE-Q-097
  - CHAR-CREATE-Q-098
  - CHAR-CREATE-Q-099
  - CHAR-CREATE-Q-100
  - CHAR-CREATE-Q-101
  - CHAR-CREATE-Q-102
  - CHAR-CREATE-Q-103
  - CHAR-CREATE-Q-104
  - CHAR-CREATE-Q-105
reserved_questions:
  - CHAR-CREATE-Q-093: I-owned
companion_decision_ledger: novydres_character_creation_h_guided_pc_integration_decisions_v0_1.md
final_verdict: READY_FOR_SENIOR_EDITOR_REVALIDATION
---

# H — Complete / Guided PC Integration

## 1. Purpose

H assembles the already-approved character-creation authorities into one finite **Modo Guiado** workflow for player characters.

The Guiado is not a third mechanical system, a second economy, an XP progression minigame, a chronology simulator, a coterie lifepath, or a replacement for the Quick mode. It is one of exactly two character-creation modes: `Rápido` and `Guiado`.

Its distinctive function is to let a character's sheet, relationships, causal history and current 2010 state emerge together through Played History while preserving mechanical parity with the Rápido.

The core relation is:

`authorize → seed → discover / build through history → consolidate in 2010`

The user-facing experience should feel like genuine gain, loss, transformation and uncertainty. The internal architecture still enforces the already-authorized economy, legality and Power Profile without exposing that bookkeeping as player-facing language.

## 2. Normative upstream contracts

H preserves without reopening:

- A — V5 legality, admitted sources, trait legality and final mechanical completeness;
- B — Power Profile / Power Envelope authorization and post-sheet audit;
- G — economic/development chassis and Quick parity baseline;
- C — social, territorial and political current-state ontology;
- D1 — Played History core, Marcos, Alvo Funcional de Construção, Premissa Protegida, Dívida Causal and Marco sufficiency;
- D2 — Provocation eligibility/resolution, reroll/reinterpretation, consequence handling, state updates and callable Played History engine;
- E — historical truth, current memory/access, relationships, temporal persistence and 2010 consolidation;
- F — chronology, canon and Revelation boundary;
- J2 — coterie architecture and emergent shared-history model;
- Play Guidance — campaign/table input and post-creation operational backbone.

## 3. Governing invariants

1. Rápido and Guiado must converge on the same kind of legal, playable 2010 character.
2. The chronicle-authorized B Power Profile is chosen before Guided construction begins.
3. The G-compatible chassis/economy is the development budget used by Guiado; Guiado does not invent a second chassis.
4. Age/activity chassis and B Power Profile remain independent axes with compatibility constraints.
5. Played History does not grant a new economy. It makes already-authorized development appear, change, disappear or transform through causally meaningful events.
6. Player-facing text does not expose internal terms such as `saldo autorizado`, `alocação provisória`, `orçamento residual`, or guarantees that lost capacity will later be restored.
7. Provocations may say `ganhe`, `aprenda`, `aumente`, `perca`, `reduza`, `abandone`, `transforme`, `troque`, or equivalent when that is the actual experienced consequence.
8. Losses may be real and permanent where upstream authority allows. They do not create automatic refund or compensatory XP.
9. The mode as a whole may not be calibrated to make Guiado systematically stronger or weaker than Rápido for equivalent premises, Power Profiles, chassis and exception authorizations.
10. Specialist / Balanced / Generalist remain Quick presets only. Guided distribution emerges from trajectory and need not carry those labels.
11. A Marco never requires exhausting every Provocation in its pool.
12. A completed Marco is not normally reopened later to repair creation gaps.
13. The five-chapter History used by Rápido is a common narrative consolidation spine, not a new set of procedural Marcos.
14. The final artifacts of Rápido and Guiado are structurally and functionally equivalent.
15. `Unknown` is not false. Legitimate unresolved surfaces may remain unresolved where they do not block current operational state.

## 4. Guided construction model

### 4.1 Before Played History

The table establishes only what must be fixed before discovery begins.

At minimum, where applicable:

- chronicle premise and relevant table choices;
- protected concept elements;
- B Power Profile;
- activity-time chassis / economic frame already authorized by G;
- legal mechanical anchors that must be known before history can operate;
- any fixed Clan, Generation, Sire premise, chronicle-mandated relationship or other protected element;
- current or historical facts that Play Guidance, canon or Revelation requires to remain protected;
- coterie situation if already known.

There is no universal mandatory pre-history form beyond what the individual chronicle and authorities require.

### 4.2 During Played History

Provocations and Episodes do two things at once:

- construct the character's causal/narrative trajectory;
- construct, modify, transform or remove mechanical expressions on the sheet.

The player should experience these as actual consequences, not as bookkeeping operations against a hidden budget.

Internally, authoring and validation maintain the relation:

`authorized development capacity → historical cause → current or historical expression`

The same Episode may simultaneously affect:

- mechanical traits;
- relationships;
- Conviction candidates;
- Touchstone candidates;
- territorial/social state;
- memories or gaps;
- identity;
- coterie state;
- assets/liabilities;
- Dívida Causal;
- protected or unresolved historical surfaces.

### 4.3 Internal authoring rule for Provocations

Each Provocation should be designed with internal metadata sufficient to know:

- what must already be true for it to be eligible;
- what it can introduce;
- what it can transform or destroy;
- what surfaces it can touch;
- what happens if its intended target is absent;
- whether it can recur;
- what chassis/activity scopes require distinct treatment;
- what authority owns any mechanical or setting validation it invokes.

This is internal infrastructure. It must not become a player-facing branch tree or technical form.

## 5. Vocabulary boundary: internal architecture vs player-facing experience

### 5.1 Internal vocabulary

Editorial/design documents may use:

- authorized budget;
- remaining capacity;
- mechanical allocation;
- parity;
- chassis compatibility;
- residual capacity;
- trajectory revision;
- final consolidation;
- internal gain/loss calibration.

### 5.2 Player-facing vocabulary

Published Guided procedures should prefer concrete consequence language:

- gain;
- learn;
- increase;
- acquire;
- choose;
- mark;
- lose;
- reduce;
- abandon;
- erase;
- replace;
- transform;
- exchange.

The player is not promised that every loss will later be restored or that every point of theoretical capacity must be filled.

## 6. G↔H Parity Matrix

| Surface | Rápido | Guiado | Parity rule |
|---|---|---|---|
| Power authorization | B Profile before sheet | B Profile before Played History | Same B authority |
| Development economy | G chassis | Same G-compatible chassis/economy | No second Guided economy |
| Specialist/Balanced/Generalist | Explicit Quick presets | Not used as Guided presets | Guided distribution emerges from history |
| Attributes | Direct allocation | Seeded and/or built through Episodes | Same applicable economic/legality ceiling |
| Skills | Direct allocation | Built through historical development and consequence | Same economic authority; distribution may differ |
| Disciplines | Direct allocation | Developed/revealed through trajectory | Same B/A limits; no Episode-generated premium |
| Advantages/Backgrounds | Direct allocation | Acquired, transformed or lost through history | Same economy and current-state legality |
| Flaws | Direct selection | May emerge or worsen through history | No compensatory XP unless an upstream rule explicitly grants it |
| Generation/BP | Direct resolution under B/G | Fixed/derived and historically contextualized | Same legal pipeline |
| Predator Type | Direct where applicable | May be seeded or historically contextualized | Same canonical package authority |
| Humanity | Direct final selection in range | Historical trajectory may justify final value | No age-based free adjustment |
| Convictions | Direct | Protected principles may be seeded; final form may emerge | Same legal final package |
| Touchstones | Direct current selection | Historical candidates may emerge; 2010 current ones finalize | Same legal final package |
| Relationship Map | Built directly from current state | Built progressively and consolidated in 2010 | Same final artifact |
| Historical density | Concise synthesis | Played History | Mode difference allowed |
| Power premium | None | None | Hard gate |
| Individual losses | Possible through chosen current state | May occur through Played History | No automatic refund; mode cannot be systematically weaker |

Parity means common authority, common economic frame and absence of a mode premium. It does not mean two characters must have identical distributions.

## 7. Guided State Phase Matrix

| Phase | Fixed/protected | Provisional/discoverable | Must not be inferred freely |
|---|---|---|---|
| Pre-history | chronicle premise, B Profile, protected concept elements, mandatory canon/revelation boundaries, applicable chassis/economy | nonessential trait distribution, many relationships, causal provenance, many historical details | protected objective truth, illegal mechanics |
| Early Marcos | protected premise remains fixed | identity texture, formative relationships, abilities, losses, early moral direction | contradictions to canon/Revelation |
| Middle Marcos | prior closed facts unless legitimately transformed | social/territorial development, powers, resources, obligations, relationship transformations, coterie emergence | free power creation beyond authorized economy |
| Late Marcos | surviving protected/core state | costs, vulnerabilities, transformations, current-position provenance | forced historical completeness |
| 2010 / final Marco | current legal endpoint must become explicit | final expression of still-open current surfaces | unresolved mandatory operational state |

## 8. Convictions and Touchstones

### 8.1 Convictions

Before Played History, a player may protect moral principles, taboos, values or identity directions that are central to the concept without writing them immediately as final V5 Convictions.

During Played History:

- Episodes may originate candidate Convictions;
- existing principles may be tested or reformulated;
- historical Convictions may later be abandoned;
- a protected moral premise may not be silently overwritten.

At 2010 consolidation, the current Convictions are expressed in the legal A/V5 format and quantity.

Older characters do not receive extra Convictions merely because they have more history.

### 8.2 Touchstones

Played History may create many historically significant mortals and historical Touchstone candidates.

A historical person is not automatically a current Touchstone.

Only at the 2010 endpoint are current Touchstones mechanically final, subject to A/V5 legality and current meaningfulness.

Historical candidates may have:

- died;
- ceased to be relevant;
- transformed into another relationship;
- become the origin of a Conviction;
- left descendants, institutions or other causal continuities without automatic mechanical inheritance.

## 9. Advanced / older Guided characters

Child of the Night, Neonate, Ancilla, Elder and Methuselah use the already-approved activity-time chassis/economic frames.

Longer activity can require richer **Significant Coverage**, but never an Episode quota proportional to years or centuries.

The rule is:

`more materially significant trajectory → potentially more Significant Coverage`

not:

`more years → more Episodes → more XP`

Torpor, stable centuries, long continuity intervals and historical compression remain valid.

A Methuselah may therefore have a far longer chronology than a Neonate without requiring proportionally more dramatized Episodes.

## 10. Marco closure and Guided completion

### 10.1 Common narrative spine

The five-chapter History used by Rápido supplies the common dramatic consolidation spine:

1. A Ilusão de Estabilidade;
2. A Fissura;
3. A Negociação com o Abismo;
4. O Ponto de Ruptura;
5. A Adaptação Sombria.

These are narrative consolidation functions, not replacement procedural Marcos.

H maps their dramatic functions onto D1's already-approved Marcos and Alvos Funcionais without renaming or reopening D1.

### 10.2 Self-sufficient Marco design

Each Marco combines:

- D1 Alvo Funcional de Construção;
- an appropriate dramatic direction from the common History spine;
- an eligible Provocation pool calibrated to produce the necessary narrative and mechanical construction organically.

A Marco closes when its dramatic/construction function is sufficiently fulfilled.

The ordinary user-facing instruction should be closer to:

> Continue until this phase of the character's trajectory has answered what it needed to answer; then move forward.

There is no mandatory final checklist that sends the user back to earlier Marcos.

### 10.3 No catalogue exhaustion

A Marco does not close by seeing every Provocation.

Adding new Provocations to the catalog must not automatically increase minimum creation length or total economic capacity.

### 10.4 Final completion

The Guided mode ends when the last applicable Marco closes.

The last Marco already includes the 2010 convergence: who the character is now, where they stand, what remains, what threatens them, what they want, and what current relationships and liabilities survive.

A/B/C and other authority checks occur organically as surfaces are resolved. The required final B audit still exists architecturally, but should not become a large player-facing validation checklist.

If a genuine illegality is discovered at the end, use the smallest valid correction. Do not reopen prior Marcos as a normal procedure.

## 11. Guided Flow Matrix

| Stage | Player-facing activity | Internal function | Principal authority |
|---|---|---|---|
| 1. Scope | establish concept/premise boundaries | protect non-discoverable inputs | Play Guidance / D1 / F |
| 2. Power authorization | establish campaign power scope | B pre-sheet gate | B |
| 3. Activity/economy | establish activity-time frame | apply G-compatible chassis/economy | G/B |
| 4. Seed | define only indispensable anchors | avoid circularity before Played History | A/H |
| 5. Enter Marcos | roll/select eligible Provocations | D2 eligibility and state loop | D1/D2 |
| 6. Resolve Episodes | make choices, gain/lose/transform, write history | distribute development and causal state | D1/D2/A/B/C/E/F |
| 7. Close Marco | recognize the arc as sufficiently formed | D1 sufficiency + narrative synthesis | D1/H |
| 8. Coterie synchronization when applicable | resolve some Episodes in collective key | J2 group-state correlation | J2/D2/H |
| 9. Final Marco | establish 2010 self and current position | final current-state consolidation | H/C/E |
| 10. Final legality | local corrections if required | B post-sheet audit + A/C checks | B/A/C |
| 11. Handoff | begin chronicle from produced state | Play Guidance consumes outputs | Play Guidance |

## 12. Mechanical loss and risk

Guided must preserve a real sense of risk.

Provocations may produce genuine losses, degradations or transformations when legitimate.

The architecture must not reveal to the player that a hidden budget is expected to compensate them later.

However, authoring calibration must ensure:

- losses are not systematically concentrated so heavily that Guided is structurally weaker than Quick;
- destructive results do not routinely create unplayable characters;
- losses route through the correct trait/system authority;
- no loss automatically creates compensatory XP;
- no gain exceeds the already-authorized economic/power boundaries.

## 13. Quick→Guided Migration Matrix — INTERNAL DESIGN / VALIDATION ONLY

Q-094 is not a player-facing upgrade mechanic.

It is an internal portability benchmark used to stress-test the Guided architecture.

| Existing-character surface | Internal benchmark expectation |
|---|---|
| B Profile | must not be reopened merely because history is being reconstructed |
| existing legal sheet | Provocations must be able to operate around a known endpoint without duplicating economy |
| existing History | can be treated as compressed known causal material |
| current Relationship Map | must remain representable as a valid 2010 endpoint |
| current Convictions/Touchstones | historical provenance may be explored without requiring a second mechanical build |
| historical gaps | may be explored if compatible with protected truth |
| destructive Provocation | must define behavior when the target is already established or absent |
| gain result | must not duplicate already-existing capacity |
| repetition | must not assume every prior state was generated by the same Guided run |
| final endpoint | must remain concise and equivalent to ordinary character outputs |

The benchmark may also be applied to characters created through another legal creation route. Its purpose is architectural robustness, not publication as a conversion procedure.

Published rules should not instruct users to `upgrade`, `convert`, or `replay` a finished Quick character through Guided.

## 14. Coterie / shared-history integration contract

H consumes J2 without creating a coterie lifepath.

### 14.1 Insertion point

There is no mandatory Marco at which coterie creation begins.

The table may establish that:

- the coterie predates the current character trajectory;
- PCs form it during Played History;
- a PC joins an older coterie;
- a character leaves and later rejoins;
- the coterie forms only near 2010;
- no coterie exists.

### 14.2 Collective interpretation

When the coterie exists or becomes relevant, applicable Provocations may be interpreted in a **collective key**.

The individual Episode/Provocation remains the construction unit, but one resolution may simultaneously produce:

- individual development;
- member relationships;
- collective identity;
- shared obligation;
- shared patron/enemy;
- shared asset/liability;
- coterie-state change;
- collective consequence.

### 14.3 Authority split

- D2 owns event/provocation resolution;
- J2 owns group-state/coterie ontology;
- E owns persistence into 2010;
- each PC retains their own protected premise and biography authority;
- H owns only the synchronization/insertion behavior inside the Guided workflow.

No mandatory additional group Episodes are created by H.

## 15. Final Output Matrix

| Output | Required? | Final surface | Notes |
|---|---:|---|---|
| complete mechanical sheet | yes | character sheet | same structural endpoint as Quick |
| five-part consolidated History | yes | History | concise, causal, may contain legitimate gaps |
| Relationship Map | yes where relationally applicable | V5 tabletop Relationship Map | current materially relevant network |
| current social/territorial state | yes | sheet/history/map as appropriate | no redundant parallel inventory required |
| Convictions | yes per A/V5 | sheet | current 2010 set |
| Touchstones | yes per A/V5 | sheet + Relationship Map | current valid mortals only |
| Humanity | yes | sheet | final current value |
| coterie reference/state | conditional | coterie artifact/reference | only when applicable |
| Dívidas Causais | conditional | current notes / Storyteller preparation surface | only unresolved relevant consequences |
| current assets/identities | conditional | sheet/history/current notes | historical assets do not create current entitlement |
| legitimate Unknowns | conditional | appropriate player-safe or ST-facing surface | Unknown ≠ false |
| exceptional mechanical provenance | conditional | concise History/notes | only where materially needed |
| full Episode log | no | optional Caderno de Trajetória | non-normative |
| permanent Played History sheet | no | none | explicitly avoided |

## 16. Optional Caderno de Trajetória

A Guided player may optionally preserve the raw Played History process as a **Caderno de Trajetória**.

It may contain:

- Provocations;
- Episode responses;
- historical relationships;
- losses and transformations;
- discarded identities;
- historical versions of current beliefs;
- notes about past figures;
- memory gaps or subjective versions;
- causal origins of traits or debts.

The Caderno:

- is optional;
- is not a fifth mandatory character artifact;
- grants no XP, dots, rerolls, bonus dice or exclusive access;
- may support richer interpretation and continuity;
- may be consulted as fictional material when existing mechanics such as Memoriam legitimately make the past relevant;
- does not itself restore inaccessible memory or override Revelation/F.

The benefit of Guided is deeper causal familiarity with the character, not greater mechanical power.

## 17. Play Guidance handoff

### 17.1 Inputs to H

H may receive, only as needed:

- chronicle premise;
- table choices;
- protected character concept;
- Power Profile authorization;
- activity-time/chassis frame;
- fixed setting position or restrictions;
- mandatory relations/obligations;
- known coterie condition;
- protected Unknown/Revelation surfaces.

Play Guidance should provide only what Played History lacks authority to invent or what the chronicle needs protected before discovery.

### 17.2 Outputs from H

At the end of the last Marco, H returns:

- complete PC;
- final History;
- current Relationship Map;
- current territorial/social position;
- coterie state/reference where applicable;
- active relationships;
- unresolved Dívidas Causais;
- relevant enemies, obligations, vulnerabilities and dependencies;
- legitimate unresolved player-safe Unknowns;
- Storyteller-facing implications where allowed by Revelation/F.

H does not require a separate `write three plot hooks` stage. Hooks should emerge from surviving consequences and current state.

There is no additional character-creation phase after the last Marco. Session Zero may still exist under Play Guidance for table-level matters, but H does not redefine it.

## 18. C downstream dispositions

| Upstream C direction | H disposition | H implementation |
|---|---|---|
| CHAR-C-015 | RATIFIED BY H | internal social/territorial guardrails stay internal; Guided embeds them organically in eligibility, Provocations and current-state construction |
| CHAR-C-016 | RATIFIED WITH H SCOPE LIMIT | H owns placement of initial player/ST scope inputs; D1/D2 continue to own prompt eligibility, reroll and state logic |
| CHAR-C-019 | RATIFIED BY H | Relationship Map develops progressively and is consolidated to current 2010 relevance |

## 19. H→I contract

H does not decide Q-093.

I may consume:

- exactly two modes: Quick and Guided;
- one common PC/NPC ontology;
- Guided as an available depth/procedure dimension rather than a third NPC mode;
- the common final outputs: legal sheet, History, Relationship Map/current relation state, territorial/social state, current causal liabilities and applicable coterie references;
- the principle that historical depth can be abbreviated for NPCs without changing ontology;
- the principle that the same Guided architecture may be applied at reduced depth where I later authorizes it.

I must not infer from H that NPCs require full Played History or that Q-093 has been decided.

## 20. H→K requirements

K must preserve:

1. exactly two creation modes;
2. no Guided-only XP economy;
3. B pre-history authorization and post-sheet audit;
4. G-compatible chassis/economic parity;
5. player-facing gain/loss language without exposing hidden budget mechanics;
6. no Specialist/Balanced/Generalist requirement in Guided;
7. no age-proportional Episode quota;
8. no requirement to exhaust Provocation pools;
9. no final checklist that routinely reopens earlier Marcos;
10. the common five-part History as a consolidation spine, not replacement Marcos;
11. Conviction/Touchstone finalization rules;
12. optional Caderno de Trajetória with no mechanical bonus;
13. no player-facing Quick→Guided conversion mechanic;
14. coterie collective-key interpretation without coterie lifepath;
15. same final artifact structure for Quick and Guided;
16. Relationship Map as V5 tabletop artifact, not a software graph;
17. Unknown ≠ false;
18. Historical Peak ≠ current sheet;
19. no duplicate permanent Played History sheet;
20. final handoff directly into Play Guidance.

## 21. Retroactive triggers

H should trigger upstream review only if later implementation reveals a real contradiction with authority.

Potential triggers:

- a required Provocation effect cannot be expressed without creating XP/dots outside G/B;
- Guided parity cannot be achieved without changing an already-approved chassis;
- a Marco can only close by exhausting a Provocation catalog, contradicting D1/D2 sufficiency;
- final artifact equivalence cannot be maintained without changing E/G output architecture;
- coterie synchronization requires a separate coterie lifepath, conflicting with J2;
- a player-facing rule would need to expose internal C/B validation machinery contrary to approved anti-bureaucracy direction;
- current Touchstone/Conviction legality proves incompatible with the approved E/A boundary;
- a Publication implementation would require H to decide Q-093.

A retro trigger is not activated merely because a particular character is unusual or requires local correction.

## 22. Blockers

No architectural blocker remains inside H.

Downstream content-authoring work remains substantial, especially:

- actual Marco-to-dramatic-spine mapping;
- Provocation catalog design;
- per-scope/chassis mechanical effect calibration;
- gain/loss distribution testing;
- recurrence behavior;
- destructive-result safety and playability testing;
- coterie-capable Provocation authoring;
- publication language and layout.

These are implementation/design tasks, not unresolved H architecture questions.

## 23. Closure matrix

| Q ID | Subject | Resolution | Decision |
|---|---|---|---|
| Q-094 | Quick-to-Guided upgrade path | CLOSED as internal interoperability/portability benchmark; not player-facing conversion | CHAR-H-006 |
| Q-096 | Guided-mode step ordering | CLOSED by hybrid `authorize → seed → discover/build → consolidate` workflow | CHAR-H-001 |
| Q-097 | mechanics-first vs history-discovery | CLOSED by hybrid construction with protected anchors and history-driven distribution | CHAR-H-001 |
| Q-098 | Convictions discovery vs preselection | CLOSED by protected principles + historical discovery + 2010 consolidation | CHAR-H-002 |
| Q-099 | Touchstone creation timing | CLOSED by historical candidates + current 2010 mechanical finalization | CHAR-H-002 |
| Q-100 | Guided mechanical parity | CLOSED by common B/G authorization/economy and no mode premium | CHAR-H-003 |
| Q-101 | stopping/completion criteria | CLOSED by self-sufficient Marco closure; last Marco ends Guided | CHAR-H-004 |
| Q-102 | Guided artifact assembly | CLOSED by common final artifacts + optional non-normative Caderno | CHAR-H-005 |
| Q-103 | advanced/older Guided profile | CLOSED by activity chassis + Significant Coverage without age-proportional Episodes | CHAR-H-003 |
| Q-104 | coterie shared-history insertion | CLOSED by fiction/table-selected synchronized collective interpretation | CHAR-H-007 |
| Q-105 | Session Zero / Play Guidance handoff | CLOSED by direct input/output handoff with no additional creation phase | CHAR-H-008 |

`CHAR-CREATE-Q-093` remains OPEN and I-owned.

## 24. Final verdict

**READY FOR SENIOR EDITOR REVALIDATION**

H now has a finite Guided procedure, resolved mechanics/history interaction, Conviction/Touchstone timing, internal interoperability benchmark, Quick parity, advanced/older handling, coterie synchronization, final artifact assembly, and Play Guidance handoff.

I may begin after Senior Editor revalidation without H deciding Q-093.