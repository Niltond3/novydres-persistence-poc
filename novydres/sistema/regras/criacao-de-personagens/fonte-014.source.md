---
document_id: novydres_character_creation_g_quick_creation_mode
version: 0.1.1
status: candidate_for_senior_editor_revalidation
date: 2026-08-21
scope: character_creation_g_quick_creation_mode_b_g_interface_and_q092_boundary_patch
supersedes: novydres_character_creation_g_quick_creation_mode_v0_1.md
corrective_scope: B_G_interface_pre_sheet_gate_post_sheet_audit_and_RETRO_Q092_boundary_only
execution_node: G
owns:
  - CHAR-CREATE-Q-087
  - CHAR-CREATE-Q-088
  - CHAR-CREATE-Q-089
  - CHAR-CREATE-Q-090
  - CHAR-CREATE-Q-091
  - CHAR-CREATE-Q-095
  - CHAR-CREATE-Q-092
deferred:
  - CHAR-CREATE-Q-093
  - CHAR-CREATE-Q-094
companion_decisions:
  - novydres_character_creation_g_quick_creation_mode_decisions_v0_1_1.md
---

# Novydres by Night — Character Creation G: Quick Creation Mode

## 1. Purpose

The Quick Creation Mode creates a complete, legal, immediately playable character for Novydres in 2010 without running Played History.

It is not a reduced ontology and does not produce a lesser character. A character created through Quick Creation must be capable of ending in the same kind of final game state as a character created through the other authorized creation path. What differs is the construction procedure, not the final legality or completeness of the character.

Quick Creation is direct. It does not simulate a chronological lifepath, does not award XP because of age, and does not require reconstruction of historical episodes.

The mode uses:

- one authorized active-time chassis;
- independent allocation geometries for Attributes, Skills, and Disciplines;
- linear totals for Advantages/Backgrounds/Loresheets and Specialties;
- Generation chosen independently of chassis;
- Blood Potency paid normally;
- a concise but definitive five-chapter History;
- a functional Relationship Map;
- direct placement of the character in Novydres in 2010.

## 2. Scope boundaries

### 2.1 What Quick Creation does

Quick Creation produces an individual character with:

- identity and concept;
- Clan or other applicable vampiric condition;
- Generation;
- Blood Potency;
- Attributes;
- Skills;
- Specialties;
- Disciplines and powers;
- Advantages, Backgrounds, Merits, Loresheets where applicable;
- Flaws;
- Predator Type when applicable;
- Humanity;
- Convictions and Touchstones under the applicable baseline;
- derived traits;
- concise definitive History;
- current social, political, territorial, and relational placement;
- a functional Relationship Map.

### 2.2 What Quick Creation does not do

Quick Creation does not:

- run Played History;
- run Episodes or Provocations as a lifepath;
- use age as XP;
- require a year-by-year chronology;
- create a coterie;
- define the architecture of the Guided Mode;
- create a parallel trait ontology;
- create a separate social/political/territorial inventory when the same information is already represented by mechanical traits, History, and the Relationship Map.

### 2.3 Coterie retcon

Character Quick Creation does not include coterie creation.

There will be a separate **Quick Coterie Creation DEU**, placed alongside the **Quick Character Creation DEU**. It is a distinct group-construction surface, not a third character-creation mode. J2 remains the coterie architecture authority; this G artifact owns only the character-side boundary and handoff.

For formal juridical coterie formation in Novydres, this procedure points to `05_concilio_leis_status_prestacoes_v0_2_2.md` → **Leges Coterium**: only the Príncipe Regente, with the Primógeno's blessing, may form a coterie. G adds no further recognition category or local coterie law.

The character-side handoff records only what is already true or later needed by the separate coterie procedure: whether a coterie already exists, which individual choices refer to it, and the character-side relations/assets/obligations that may be consumed by J2-governed coterie construction. Coterie outputs may later return to the character's current state and Relationship Map without rerunning character creation.

## 3. Core construction principle

The five chassis are not mandatory stages of one character's evolution.

Each chassis is built independently against the same Child of the Night baseline:

- Child of the Night: baseline +0 XP
- Neonate: baseline +140 XP
- Ancilla: baseline +275 XP
- Elder: baseline +670 XP
- Methuselah: baseline +1,195 XP

The labels measure expected active development for construction purposes. They are not strict chronological-age packages.

A chronologically ancient vampire who spent most of existence inactive may use a lower chassis. Conversely, a character with unusual development may use a higher chassis when the chronicle premise authorizes it.


### 3.1 B Power Profile ↔ Quick chassis interface

B and G answer different questions.

- **Power Profile:** what level/range of power is authorized by the chronicle premise.
- **Quick chassis:** what economic/development template Quick uses to construct the character.

The constructs are independent axes, but they are not independent permissions: a chassis or preset never overrides the authorized B envelope. Chassis labels remain active-development labels and do not map automatically to Profile 1/2/3.

#### 3.1.1 Normative interface contract

1. **B authorizes power.** The chronicle first authorizes Profile 1, 2, or 3 and records any `Exceptional Start` / `Declared Outlier` authorization.
2. **G structures construction.** A Quick chassis supplies an economic/development template: total available construction budget, reference arrays, linear totals, and BP reference. It is not a Power Profile and grants no permission to exceed B.
3. **The axes are independent but constrained.** Age, activity label, social stratum, and chassis name do not determine the B Profile. A character may use any chassis whose actual construction can remain inside the authorized envelope or pass the applicable B gate.
4. **Preset legality is result-based.** A ready preset is usable only when its actual Generation/BP/Depth/Breadth/Mastery/Power Density/Mechanical Load/rarity composition fits the authorization. A preset printed under a chassis is not independently entitled.
5. **If a preset exceeds the envelope, correct locally first.** In order: choose another preset inside the chassis; redistribute legally inside the chassis budget; leave XP unspent when no legal in-envelope purchase remains; or, if the intended power is essential, pass B's gateway to a higher authorized Profile, `Exceptional Start`, or `Declared Outlier`. No suppressed/capped trait creates credit elsewhere.
6. **If the gate is denied, the character remains local-correction work.** Use a compatible configuration or chassis; do not automatically discard the entire character.
7. **Post-sheet audit remains mandatory as an internal/normative validation.** It checks the actual result against authorized Profile, Generation, BP, Discipline Depth, Breadth, Mastery Load/Power Density where triggered, Mechanical Load, rarity debt, and exception/outlier state. This audit does not require a large player-facing checklist.

#### 3.1.2 Profile × chassis compatibility

The matrix classifies the chassis as a construction route, not every individual ready preset as automatically legal. A cell marked `COMPATIBLE WITH LOCAL ADJUSTMENT` means at least one normal in-chassis configuration can be brought inside the profile without changing B; a particularly high preset may still require the B gateway. `REQUIRES EXCEPTION GATE` means the chassis cannot be treated as an ordinary expression of that profile and needs formal B authorization/elevation before the intended high construction is retained.

| Quick chassis | B Profile 1 | B Profile 2 | B Profile 3 | Exceptional Start | Declared Outlier |
|---|---|---|---|---|---|
| Child of the Night | ORDINARILY COMPATIBLE | ORDINARILY COMPATIBLE | ORDINARILY COMPATIBLE | ORDINARILY COMPATIBLE | ORDINARILY COMPATIBLE |
| Neonate | COMPATIBLE WITH LOCAL ADJUSTMENT | COMPATIBLE WITH LOCAL ADJUSTMENT | ORDINARILY COMPATIBLE | ORDINARILY COMPATIBLE | ORDINARILY COMPATIBLE |
| Ancilla | REQUIRES EXCEPTION GATE | COMPATIBLE WITH LOCAL ADJUSTMENT | COMPATIBLE WITH LOCAL ADJUSTMENT | ORDINARILY COMPATIBLE | ORDINARILY COMPATIBLE |
| Elder | REQUIRES EXCEPTION GATE | REQUIRES EXCEPTION GATE | COMPATIBLE WITH LOCAL ADJUSTMENT | COMPATIBLE WITH LOCAL ADJUSTMENT | ORDINARILY COMPATIBLE |
| Methuselah | REQUIRES EXCEPTION GATE | REQUIRES EXCEPTION GATE | REQUIRES EXCEPTION GATE | COMPATIBLE WITH LOCAL ADJUSTMENT | ORDINARILY COMPATIBLE |

Preset stress points that drive the classifications:

- Neonate `4/2` exceeds ordinary Profile-1 Depth and uses Profile-2 exceptional focal Depth; its lower presets or redistribution provide the local-adjustment route.
- Ancilla `5/2/1` exceeds Profiles 1–2 ordinary space and is material Profile-3/exception territory; `4/3/2` is Profile-2 exceptional focal Depth; its broad Generalist construction requires Breadth review.
- Elder presets carry multiple ratings 4–5 and broad out-of-Clan development. Profile 3 can host an Elder chassis only after composition-level local audit/adjustment; lower Profiles require a B exception gate.
- Methuselah presets contain multiple Discipline 5s and breadth beyond ordinary Profile-3 space. They therefore require a formal exception path unless a `Declared Outlier` is already authorized; `Exceptional Start` may still require local reduction/redistribution rather than entitlement to the printed preset.

## 4. XP cost model

Equivalent XP is calculated from the natural floor of 0, level by level.

### 4.1 Progressive traits

| Trait | Cost of each increase | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| Attribute | new level ×5 | 5 | 15 | 30 | 50 | 75 |
| Skill | new level ×3 | 3 | 9 | 18 | 30 | 45 |
| Clan Discipline | new level ×5 | 5 | 15 | 30 | 50 | 75 |
| Out-of-Clan Discipline | new level ×7 | 7 | 21 | 42 | 70 | 105 |
| Caitiff / Thin-Blood Discipline | new level ×6 | 6 | 18 | 36 | 60 | 90 |
| Blood Potency | new level ×10 | 10 | 30 | 60 | 100 | 150 |

### 4.2 Linear traits

- New Specialty: 3 XP each.
- Advantage / Merit / Background / Loresheet: 3 XP per dot, linear.
- Blood Sorcery Ritual: level ×3 XP.
- Thin-Blood Formula: level ×3 XP.
- Other separately acquired ritual-like options use their applicable rule and are not bundled into Discipline rating.

### 4.3 Flaws

Flaws do not generate XP. Additional voluntary Flaws also do not generate XP.

## 5. Allocation geometries

Geometries apply only where the form of distribution materially matters:

- Attributes;
- Skills;
- Disciplines.

They do not apply to Advantages/Backgrounds/Loresheets, Specialties, Generation, Blood Potency, Humanity, Flaws, Predator Type, Convictions/Touchstones, or derived traits.

A character may choose a different geometry on each geometric surface.

### 5.1 Specialist
Concentrates power into fewer areas and accepts meaningful valleys.

### 5.2 Balanced
Distributes power between peaks, support, and breadth.

### 5.3 Generalist
Favors broad coverage without abandoning priorities. Generalist does not mean homogeneous, indiscriminate, or filling every Skill or Discipline. The conceptual baseline is the V5 Jack of All Trades profile: broad competence with visible priorities.

## 6. Master chassis matrix

### 6.1 Economic overview

| Chassis | Materialized sheet value | Additional XP budget over Child | Free XP |
|---|---:|---:|---:|
| Child of the Night | 379 | +0 | 0 |
| Neonate | 519 | +140 | 0 |
| Ancilla | 653 | +275 | 1 |
| Elder | 1,044 | +670 | 5 |
| Methuselah | 1,574 | +1,195 | 0 |

The baseline economic value of Child of the Night is 379 XP, including one open Specialty.

### 6.2 Cost by surface

| Chassis | Attributes | Skills | Disciplines | Advantages | Specialties | BP | Free |
|---|---:|---:|---:|---:|---:|---:|---:|
| Child of the Night | 205 | 120 | 20 | 21 | 3 | 10 | 0 |
| Neonate | 240 | 150 | 65 | 42 | 12 | 10 | 0 |
| Ancilla | 270 | 177 | 95 | 63 | 18 | 30 | 1 |
| Elder | 325 | 225 | 320 | 81 | 33 | 60 | 5 |
| Methuselah | 400 | 300 | 600 | 126 | 48 | 100 | 0 |

## 7. Child of the Night

### Attributes — 205 XP
- Specialist: `4/4/3/3/2/2/1/1/1`
- Balanced: `4/3/3/3/2/2/2/2/1`
- Generalist: `3/3/3/3/3/3/2/1/1`

### Skills — 120 XP
- Specialist: `4/3/3/3/2/2/2/1/1/1`
- Balanced: `3/3/3/2×5/1×7`
- Generalist: `3/2×8/1×10`

Breadth: 10 / 15 / 19.

### Disciplines — 20 XP
All geometries use Clan `2/1`. This is a deliberate **Floor Collapse**.

### Common values
- Advantages: 7 dots
- Specialties: 1
- Blood Potency reference: 1
- Minimum Flaws: 2 dots
- Humanity recommended: 6–8, reference 7
- Predator Type: none

## 8. Neonate

### Attributes — 240 XP
- Specialist: `5/4/3/3/2/2/2/1/1`
- Balanced: `4/4/3/3/3/2/2/2/1`
- Generalist: `4/3×6/1×2`

### Skills — 150 XP
- Specialist: `5/3×4/2×3/1×2`
- Balanced: `4/3×4/2×4/1×4`
- Generalist: `4/3/2×8/1×10`

Breadth: 10 / 13 / 20.

### Disciplines — 65 XP
- Specialist: Clan `4/2`
- Balanced: Clan `3/3/1`
- Generalist: Clan `3` + out-of-Clan `2/1/1`

Any external acquisition remains subject to normal access and provenance.

### Common values
- Advantages: 14 dots
- Specialties: 4
- Blood Potency reference: 1
- Minimum Flaws: 3 dots
- Humanity recommended: 5–8, reference 7
- Predator Type: yes

## 9. Ancilla

### Attributes — 270 XP
- Specialist: `5/4/4/3/2/2/2/2/1`
- Balanced: `4/4/4/3/3/2/2/2/2`
- Generalist: `5/3×5/2×3`

### Skills — 177 XP
- Specialist: `5/4/3×4/2×3/1`
- Balanced: `4/4/3/3/2×7/1×6`
- Generalist: `4/3/3/2×10/1×7`

Breadth: 10 / 17 / 20.

### Disciplines — 95 XP
- Specialist: Clan `5/2/1`
- Balanced: Clan `4/3/2`
- Generalist: Clan `3/2/2` + out-of-Clan `2/1/1`

### Common values
- Advantages: 21 dots
- Specialties: 6
- Blood Potency reference: 2
- Minimum Flaws: 4 dots
- Humanity recommended: 5–7, reference 6
- Predator Type: yes
- Free XP: 1

## 10. Elder

### Attributes — 325 XP
- Specialist: `5/5/5/4/3/1/1/1/1`
- Balanced: `5/5/4/3/3/3/2/2/1`
- Generalist: `5/4/4/3/3/3/3/2/2`

### Skills — 225 XP
- Specialist: `5/5/4/4/3×3/2×2/1`
- Balanced: `5/4/4/3×4/2×4/1×4`
- Generalist: `5/4/3×3/2×9/1×5`

Breadth: 10 / 15 / 19.

### Disciplines — 320 XP
- Specialist: Clan `5/5/3` + out-of-Clan `4/4`
- Balanced: Clan `5/5/3` + out-of-Clan `4/3/2/1`
- Generalist: Clan `4/3/3` + out-of-Clan `4/3/3/2/2/1/1`

### Common values
- Advantages: 27 dots
- Specialties: 11
- Blood Potency reference: 3
- Minimum Flaws: 6 dots
- Humanity recommended: 4–7, reference 5
- Predator Type: yes
- Free XP: 5

## 11. Methuselah

### Attributes — 400 XP
- Specialist: `5/5/5/5/3/3/3/1/1`
- Balanced: `5/5/5/4/4/3/2/2/2`
- Generalist: `5/4/4/4/4/4/3/3/2`

### Skills — 300 XP
- Specialist: `5×3/4×3/3×3/2×2/1`
- Balanced: `5×2/4×2/3×5/2×5/1×5`
- Generalist: `5/4/3×7/2×10/1×3`

Breadth: 12 / 19 / 22.

No Skill distribution may exceed the actual number of Skills available on the character sheet. Generalist does not require filling all Skills.

### Disciplines — 600 XP
- Specialist: Clan `5/5/3` + out-of-Clan `5/5/5/5`
- Balanced: Clan `5/5/3` + out-of-Clan `5/5/4/4/4`
- Generalist: Clan `5/5/3` + out-of-Clan `5/3×6/2×3`

### Common values
- Advantages: 42 dots
- Specialties: 16
- Blood Potency reference: 4
- Minimum Flaws: 8 dots
- Humanity recommended: 3–7, reference 4
- Predator Type: yes

## 12. Generation and Blood Potency

Generation is not fixed by chassis.

Quick Creation permits any admitted Generation in the creation scope, approximately from 14th through 4th Generation, subject to applicable legality.

Generation itself costs no XP.

Blood Potency reference by chassis:

- Child of the Night: BP 1
- Neonate: BP 1
- Ancilla: BP 2
- Elder: BP 3
- Methuselah: BP 4

If the selected Generation requires a higher minimum Blood Potency, the character must pay the full XP necessary to reach that minimum from the same global chassis budget. There is no subsidy or compensation for low Generation.

## 13. Predator Type

Predator Type represents feeding and hunting habits developed through unlife.

- Child of the Night: no Predator Type
- Neonate: Predator Type
- Ancilla: Predator Type
- Elder: Predator Type
- Methuselah: Predator Type

Predator Type is a fixed package. Its benefits remain source-bound and do not become fungible XP.

## 14. Flaws

Minimum Flaw dots by chassis:

- Child of the Night: 2
- Neonate: 3
- Ancilla: 4
- Elder: 6
- Methuselah: 8

Rules:

- the floor is measured in dots, not number of distinct Flaws;
- no artificial concentration cap is imposed where rules allow concentration;
- additional Flaws are allowed but do not grant XP;
- only materially relevant, non-redundant Flaws count toward the intended floor;
- important relational Flaws should appear on the Relationship Map when their counterpart remains active and relevant.

Flaws represent meaningful vulnerability and accumulated cost, not a direct XP exchange for power.

## 15. Humanity

Humanity uses recommended ranges, not automatic age-based reduction:

- Child of the Night: 6–8, reference 7
- Neonate: 5–8, reference 7
- Ancilla: 5–7, reference 6
- Elder: 4–7, reference 5
- Methuselah: 3–7, reference 4

Humanity does not alter the global XP budget unless a specific rule explicitly creates such an exchange.

High Humanity in an old character and low Humanity in a young character are both legal when the definitive History supports them.

## 16. Convictions and Touchstones

Convictions and Touchstones do not scale by chassis. They follow the applicable baseline.

Convictions should be written as operational principles rather than abstract values and should be causally legible in the character's History.

Touchstones are concrete, current relationships and must appear on the Relationship Map when active.

No additional number of Convictions or Touchstones is required merely because a character is older or has higher Humanity.

## 17. Advantages, Backgrounds, positions, and resources

Mechanical positions, resources, relations, obligations, and vulnerabilities are represented through the applicable mechanical traits when such traits exist.

The History provides the cause and trajectory behind them. The Relationship Map identifies the agents who remain materially relevant.

Quick Creation does not create a redundant parallel inventory of social, political, and territorial state where the information is already adequately represented.

Narrative relations that do not require mechanical representation remain narrative.

## 18. Rootedness, Bairrismo, and territorial state

Quick Creation resolves current territorial and local state directly from the definitive History.

Bairrismo is not progressed through stages during Quick Creation. It is inferred from what the character actually lived and established. Time alone does not establish Bairrismo.

A newcomer may validly end creation with little or no local rootedness, no Marco, no Domain, no local Status, and only minimal local relations.

A Marco Territorial is conditional and never derives automatically from residence, feeding, ownership, Domain, age, XP, or Bairrismo alone.

## 19. Canonical five-chapter History

Every Quick-created character writes the final History using the canonical five-chapter layout. This document does not define how any other creation mode produces that layout.

The five chapters are narrative consolidation functions, not new procedural Marcos.

### I — A Ilusão de Estabilidade

Establish who the character believed themselves to be, what formed their character, what they valued, what they wanted, and what security, relationship, identity, or belief seemed stable.

Core prompt:

> What did you believe you were building, and what truth about yourself or the world allowed you to believe it would last?

### II — A Fissura

Establish the first undeniable break in the previous stability, what could no longer be ignored, what loss began, and what made return impossible or compromised.

Core prompt:

> When did you first realize that you could no longer remain who you believed yourself to be?

### III — A Negociação com o Abismo

Establish attempts to preserve control, rationalizations, alliances and bargains, morally ambiguous choices, skills/resources/influence/powers acquired as strategies of survival or control, and relationships converted into tools or obligations.

Core prompt:

> What did you do to convince yourself that you were still in control?

### IV — O Ponto de Ruptura

Establish the event or cluster of events that made the old self-conception untenable, the real price of survival/power/compromise, and losses, crimes, consequences, and vulnerabilities that remain meaningful.

Core prompt:

> What did you sacrifice, destroy, accept, or become in order to continue?

### V — A Adaptação Sombria

Establish the 2010 endpoint: what remains, what has been accepted or corrupted, what is still preserved, current place in Novydres, important current relations, Ambition, what may still be lost, and what the character believes comes after achieving the Ambition.

Core prompt:

> What remains of you now, what do you still refuse to lose, and what do you believe you will finally have if you achieve what you want?

### 19.1 Length and form

The expected final History is approximately five concise paragraphs, one substantial paragraph per chapter as a normal target. This is not a hard word count.

A full prose biography, fictional chapters, chronological diary, or Prelude is not required.

A Prelude is optional and may be subjective, dramatized, or written in first person. It never replaces the definitive History.

The History is declarative and causal: it records what actually happened, why it happened, and what resulted, except where an intentional Unknown or protected revelation applies.

## 20. Mechanical provenance in History

The History does not justify every dot. It must, however, make significant or exceptional acquisitions causally legible, such as multiple out-of-Clan Disciplines, high Status, exceptional political reach, rare Loresheets, unusual resources, major offices, significant territory, large ritual repertoires, and exceptional social assets.

Several traits may share one causal explanation.

## 21. Relationship Map

Quick Creation produces an initial functional Relationship Map.

It should contain current materially relevant relations, including active Touchstones. Historical figures with no present consequence may remain only in the History.

The Relationship Map is a tabletop play aid, not a computational graph.

## 22. Operational sequence

1. **Authorize the B Power Envelope before sheet construction:** determine the chronicle-authorized Profile and whether `Exceptional Start` / `Declared Outlier` authorization applies.
2. Choose a Quick chassis and preset/configuration compatible with that authorization.
3. Choose an Attribute geometry.
4. Choose a Skill geometry.
5. Choose a Discipline geometry.
6. Distribute Advantages and Specialties.
7. Choose/derive Generation and resolve the legal Blood Potency cost through B's `Generation hard bounds → Profile envelope → Trajectory validation → Final BP` pipeline.
8. Spend remaining or returned global XP only on legal in-envelope purchases; unspendable XP may remain unspent and never creates off-envelope entitlement.
9. Apply Predator Type where applicable.
10. Choose required Flaws.
11. Resolve Humanity, Convictions, and Touchstones.
12. Write the definitive five-chapter History.
13. Resolve the current state in Novydres through traits, History, and relationships.
14. Build the Relationship Map.
15. Resolve derived values and remaining legality issues.
16. Run B's post-sheet envelope audit and correct any excess locally before finalization.

## 23. Validation

Validation remains continuous and conversational during creation. Narrator and player naturally correct illegal ratings, budget overrun, invalid Generation/BP combinations, inaccessible acquisitions, missing causal support for exceptional traits, contradictory current state, and any chassis/preset construction that would exceed the authorized B envelope.

B's post-sheet audit is nevertheless a normative final validation layer: it checks the actual character against authorized Profile, Generation, BP, Discipline Depth/Breadth, triggered Mastery/Power Density concerns, Mechanical Load, rarity debt, and exception/outlier state. Failure triggers localized correction first, not automatic character rejection.

There is no mandatory player-facing final checklist procedure.

If layout space allows without compressing more important information, the DEU may include only an extremely small reminder:

> **Legal · dentro do orçamento · coerente · situado · jogável.**

If even that competes with useful content, it is omitted.

## 24. DEU architecture

### Front — mechanical construction

Priority content:

- chassis;
- Attribute arrays;
- Skill arrays;
- Discipline arrays;
- Advantages;
- Specialties;
- BP reference;
- minimum Flaws;
- Humanity ranges;
- Predator Type applicability;
- XP;
- compact construction sequence.

### Reverse — character construction

Priority content:

- five canonical History chapters;
- concise prompts for each chapter;
- provenance guidance;
- Relationship Map guidance;
- one small completed History example if space allows;
- only optional minimal validation reminder.

The DEU must not compress essential content merely to preserve secondary boxes or summaries.

## 25. Closure matrix

| Question | Disposition | Basis |
|---|---|---|
| CHAR-CREATE-Q-087 | CLOSED | minimum final output defined |
| CHAR-CREATE-Q-088 | CLOSED | chassis, budgets, geometries, and global XP rules defined |
| CHAR-CREATE-Q-089 | CLOSED | definitive five-chapter History defined |
| CHAR-CREATE-Q-090 | CLOSED | Bairrismo / Marco direct-resolution rule defined |
| CHAR-CREATE-Q-091 | CLOSED | social/political/territorial expression through traits + History + Relationship Map |
| CHAR-CREATE-Q-092 | CLOSED — ACTIVE MEANING RETCONNED TO BOUNDARY/HANDOFF | Quick Character Creation does not create coterie; G owns only the character-side handoff to the separate J2-governed Quick Coterie surface |
| CHAR-CREATE-Q-093 | OPEN / I-owned | no G decision |
| CHAR-CREATE-Q-094 | OPEN / H-owned | no G decision |
| CHAR-CREATE-Q-095 | CLOSED | continuous localized validation defined |

## 26. Handoffs and retro triggers

### H

G establishes only the final five-chapter History layout as a shared output requirement. G does not define the internal architecture, sequence, prompt logic, consolidation method, or coterie procedure of the Guided Mode.

### Coterie workstream

A separate Quick Coterie Creation DEU is required and is not embedded in Quick Character Creation. Its coterie ontology and rules are governed by J2. G supplies only the character endpoint/input handoff and receives later coterie outputs where they affect current character state or the Relationship Map. The surface is registered here without creating a new DAG node; first-class node registration, if later desired, requires Senior Editor action.

### I

Questions owned by I remain open and must not be preempted by G.

### B revalidation

The five active-time chassis are creation-budget structures, not replacements for B's Power Envelope profiles. This successor resolves the interface: B authorizes Profile/exception state before construction; G then selects a compatible chassis/configuration; B audits the actual result after construction.

The Power Envelope remains an authorization and audit layer rather than an automatic equalizer. `CHAR-B-001–025` are unchanged.

## 27. Final verdict

**G — Quick Character Creation: READY FOR SENIOR EDITOR REVALIDATION. Q-092 is preserved in G with its active meaning narrowed to the character-side boundary/handoff; actual Quick Coterie construction remains a separate J2-governed surface. Q-093/Q-094 remain downstream-owned.**

The mechanical chassis matrix, Quick Creation flow, final output, five-chapter definitive History, current-state integration, Flaw floors, Humanity ranges, Predator Type applicability, and continuous validation approach are consolidated.

The separate Quick Coterie Creation DEU and all Guided Mode architecture remain outside this document.