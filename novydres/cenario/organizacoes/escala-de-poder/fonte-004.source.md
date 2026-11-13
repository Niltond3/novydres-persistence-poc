---
document_id: novydres_npc_power_scale_citywide
version: 0.1.1
status: candidate_for_senior_editor_revalidation
date: 2026-08-11
supersedes: novydres_npc_power_scale_citywide_v0_1.md
scope: npc_power_scale_citywide_minimal_corrective_patch
patch_scope:
  - authority_provenance_classification
  - stale_iskander_zoya_benchmark_state
decision_authority:
  artifact: novydres_npc_power_scale_citywide_decisions_v0_1.md
  coverage: NPC-POWER-001..NPC-POWER-106
  state: unchanged
target_gap: npc_power_scale_citywide
generation_gate: mandatory
next_mandatory_gate: character_creation_novydres_architecture
npc_generation_status: blocked_by_next_mandatory_gate
---

# Novydres NPC Power Scale — Citywide Architecture v0.1.1

## A. Purpose and authority

This document consolidates the citywide power-scale architecture for Cainite NPCs in Novydres. Its purpose is to prevent power creep, preserve historical and political coherence, and provide an auditable framework for judging whether individual characters, groups, lineages, institutions, and demographic concentrations fit the setting.

This workstream does **not** define a complete character-creation workflow. It defines the invariants, rarity controls, causal rules, and audit lenses that a later character-creation architecture must respect.

Formal readiness of this workstream is distinct from permission to resume Chapter 07 NPC generation.

**Workstream verdict:** READY FOR SENIOR EDITOR REVALIDATION  
**NPC generation:** BLOCKED BY NEXT MANDATORY GATE — `character_creation_novydres_architecture`

Core boundary principle:

> Power Scale ends when it can judge plausibility, causality, relative rarity, and citywide impact; it does not need to construct the entire character by itself.

### A.1 Authority and provenance classification

This patch adds provenance labels only. It does **not** change any rule, threshold, exception, or decision in `NPC-POWER-001–106`.

Authority classes used by this framework:

- `CANONICAL V5` — a rule or premise directly attributed to published V5 material. Where the supplied documentary corpus does not expose a sufficiently precise source pointer, the claim remains bounded and is marked `CANONICAL SOURCE POINTER REQUIRED` rather than receiving fabricated certainty.
- `NOVYDRES PROJECT CANON` — an established fact or supernatural premise of the Novydres setting, independent from whether it creates a new mechanic.
- `NOVYDRES LOCAL RULE / HOMEBREW` — a Novydres-specific mechanical rule, threshold, timing rule, exception, or causal interaction that is not represented here as an official V5 mechanic.
- `EDITORIAL INFERENCE` — a calibration, audit lens, taxonomy, benchmark, or causal interpretation used to preserve coherence without becoming V5 canon or diegetic setting fact.

These classes are mutually documentary, not mechanical: classification never changes how a rule functions. `EDITORIAL INFERENCE` never cascades into canon merely by repeated use.

#### A.1.1 Section authority map

| Framework location | Primary authority | Qualification / source pointer |
|---|---|---|
| §B Canonical V5 baseline | `CANONICAL V5` + bounded `EDITORIAL INFERENCE` | See §B.1; unsupported precision is marked `CANONICAL SOURCE POINTER REQUIRED`. |
| §C Novydres-specific premises | `NOVYDRES PROJECT CANON` | Setting premises already established by project canon. |
| §§D–K; §§O–U | `EDITORIAL INFERENCE` implementing approved project decisions | Audit architecture from `novydres_npc_power_scale_citywide_decisions_v0_1.md`; canonical V5 mechanics mentioned inside those sections retain their canonical authority. |
| §F statement that Generation is genealogical; §G generation BP bounds | `CANONICAL V5` | Direct baseline principle; exact book/page pointer remains `CANONICAL SOURCE POINTER REQUIRED` in this documentary corpus. |
| §H.2 additional powers within already reached Discipline levels | `NOVYDRES LOCAL RULE / HOMEBREW` | Explicitly identified as a local rule in the framework and decision `NPC-POWER-011`. |
| §L Bairrismo existence and territorial phenomenon | `NOVYDRES PROJECT CANON` | Established Novydres supernatural premise. |
| §L operational use of Conviction/Touchstone/Humanity spaces | `NOVYDRES LOCAL RULE / HOMEBREW` | Local implementation using V5-compatible mechanical spaces; not presented as an official V5 Bairrismo rule. |
| §§M–N Beckoning eligibility, BP intensity, duration, Desire progression, trigger handling, Bairrismo interaction | `NOVYDRES LOCAL RULE / HOMEBREW` | Decisions `NPC-POWER-017–029`; the general existence of the Beckoning remains a V5 premise, but these Novydres procedures are local. |
| §N.1 diablerie suppression, duration, and non-stacking | `NOVYDRES LOCAL RULE / HOMEBREW` | Decisions `NPC-POWER-030–032`; no claim of official V5 mechanics. |
| §P demographic pyramid, soft ratios, rarity distributions | `EDITORIAL INFERENCE` | Citywide calibration and governance, not V5 population law. |
| §R benchmark states | `EDITORIAL INFERENCE` | Documentary audit only; does not alter profile canon. |

## B. Canonical V5 baseline

The architecture uses only the V5 premises materially required by this workstream. Authority is separated from project interpretation below.

| Baseline input | Authority | Provenance state | Use in this architecture |
|---|---|---|---|
| Generation is genealogical rather than an age category. | `CANONICAL V5` | `CANONICAL SOURCE POINTER REQUIRED` | Prevents age from determining Generation. |
| Generation constrains Blood Potency through minimum/maximum limits. | `CANONICAL V5` | `CANONICAL SOURCE POINTER REQUIRED` | Supplies the hard legality layer used in §G. |
| Blood Potency can change across long vampiric trajectories and Torpor is materially relevant to that trajectory. | `CANONICAL V5` | `CANONICAL SOURCE POINTER REQUIRED` | Supports separation of age from a one-step BP conversion; this framework does not restate the full V5 progression rule. |
| Disciplines are purchased/developed as character mechanics rather than awarded automatically by chronological age. | `CANONICAL V5` | `CANONICAL SOURCE POINTER REQUIRED` | Supports the prohibition on age automatically granting Discipline dots. |
| Specific access narratives for unusual/out-of-clan powers are required by this project as causal explanation. | `EDITORIAL INFERENCE` | Decision-led project interpretation; see `NPC-POWER-011`, `039`, `067`. | Audits acquisition plausibility without claiming a universal V5 narrative prerequisite. |
| Published V5 NPCs can be compared as examples. | `EDITORIAL INFERENCE` | Decision `NPC-POWER-101`. | Calibration/precedent only; never a hard cap or budget. |
| The Beckoning is a V5 setting premise affecting elder/lower-generation Kindred. | `CANONICAL V5` | `CANONICAL SOURCE POINTER REQUIRED` | Supplies only the existence/background premise. Exact Novydres eligibility, intensity, duration, triggers, suppression, and exceptions are local rules in §§M–N. |
| Methuselah-scale figures are exceptional relative to ordinary Kindred populations. | `EDITORIAL INFERENCE` built from V5 setting categories | No precise canonical population-law claim is made. | Justifies declared-outlier audit rather than a canonical demographic quota. |

### B.1 Canonical-source boundary

The supplied documentary corpus for this patch does not provide sufficiently precise book/page pointers for the baseline claims above. No citation is fabricated. Each affected claim is therefore preserved at the minimum level needed by the approved architecture and carries `CANONICAL SOURCE POINTER REQUIRED` until a separately authorized provenance-research pass supplies exact references.

No local Beckoning procedure in §§M–N should be read as official V5 mechanics.

## C. Novydres-specific premises

Novydres in 2010 is shaped by four interacting historical pressures:

1. A centuries-old Cainite legal and territorial order dating to the foundation of the city.
2. The disappearance of Gilgamesh and subsequent political succession after 1917.
3. The Beckoning, which removes or displaces a material part of the elder layer and creates succession gaps.
4. Bairrismo, a real supernatural territorial phenomenon tied to belonging, anchoring, and the defense of Novydres.

The city must therefore feel old without being saturated by active elders, politically dense without making every officeholder mechanically supreme, and historically deep without granting omniscience to ancient characters.

## D. Power dimensions

There is no universal Power Score. Character power is multidimensional.

Primary audited dimensions include:

- chronological/social stratum;
- rootedness;
- Generation;
- Blood Potency;
- Discipline Depth;
- Discipline Breadth;
- Mastery Load;
- Power Density;
- mechanical load;
- competence profile;
- confrontation capacity;
- institutional authority;
- mobilizable capacity;
- social leverage;
- historical reach;
- territorial advantage;
- knowledge capability/access/rarity;
- power dependencies;
- perceived capability;
- collective power when operating as part of a recurring group.

No single dimension replaces the others.

## E. Population strata

### E.1 Chronological/social strata

The following are flexible normative bands, not hard promotions:

| Stratum | Normative active non-life band |
|---|---:|
| Criança da Noite | ~0–15 years |
| Neófito | ~16–85 years |
| Ancilla | ~85–245 years |
| Ancião | ~245+ years |
| Matusalém | exceptional; not an automatic age promotion |

Active time, torpor, trajectory, social recognition, and historical participation can complicate boundaries.

### E.2 Rootedness

Rootedness is an independent axis:

`Forasteiro → Residente → Enraizado → Histórico`

There is no fixed year requirement. Rootedness does not automatically grant Blood Potency, Discipline dots, Status, Marco Territorial, or stronger Bairrismo.

### E.3 Presence State

Characters can exist in the setting without being part of the active demographic pyramid.

Editorial states:

- **Active** — directly operating in 2010; counts in the active demographic pyramid.
- **Absent** — away through Beckoning, exile, travel, withdrawal, or equivalent; may retain a Shadow of Influence.
- **Dormant** — in Torpor; has no routine conscious agency but may retain a Legacy of Influence.
- **Eliminated** — destroyed or otherwise removed from active and potential agency.

Historical existence is therefore distinct from active population.

### E.4 Resident versus transient population

The demographic pyramid measures the resident/operationally established population.

Temporary outsiders are tracked as `Transient Presence`. They do not automatically count as residents, but materially powerful visitors are still audited and may create `CONDITIONAL CITYWIDE PRESSURE`.

## F. Generation architecture

Generation is genealogical, not chronological.

Normative statistical bands:

| Stratum | Expected Generation band |
|---|---|
| Criança da Noite | 13th–16th |
| Neófito | 12th–13th |
| Ancilla | 10th–11th |
| Ancião | 9th or lower |
| Matusalém | predominantly 3rd–7th |

These are expectations, not limits.

Low Generation in a young vampire is possible but requires genealogical coherence and rarity accounting. Old age does not retroactively lower Generation.

### F.1 Generation rarity

Rarity classes are qualitative:

- 14th–16th: common/variable among the youngest cohort;
- 12th–13th: common;
- 10th–11th: significant minority;
- 8th–9th: rare;
- 6th–7th: exceptional;
- 4th–5th: extraordinary;
- 3rd: singular/cosmological.

No rigid quotas are imposed, but the citywide distribution must not silently become an elder farm.

## G. Blood Potency architecture

Blood Potency uses three layers:

1. **Generation hard bounds** — canonical minimum and maximum BP.
2. **Individual trajectory** — active years, torpor, exceptional experiences, potent blood, and other legitimate causes.
3. **Stratum benchmark** — descriptive only, never a mechanical entitlement.

Derived Blood Potency benefits and penalties come from actual BP, never directly from age category.

Within a Generation range, the distribution should generally be tilted toward the lower and middle parts of the range. Reaching the ceiling is independently exceptional.

This creates two separate rarity questions:

- rarity of the Generation itself;
- rarity of BP saturation within that Generation.

## H. Discipline and power architecture

Disciplines are audited across independent dimensions:

- **Depth** — highest developed rating;
- **Breadth** — number of Disciplines materially developed;
- **Mastery Load** — how many Disciplines are at 4–5 dots;
- **Power Density** — number of known powers relative to the Discipline levels reached.

### H.1 Soft benchmarks

| Stratum | Depth | Breadth |
|---|---:|---:|
| Criança da Noite | 1–2 | 1–2 |
| Neófito | 2–3 | 2–3 |
| Ancilla | 3–4 | 2–4 |
| Ancião | 4–5 | 3–5 |
| Matusalém | 5 recurrent | 4+ |

These are soft calibration ranges, not automatic entitlements or caps.

### H.2 Acquisition rules

Out-of-clan Disciplines, amalgams, rare powers, and additional powers require concrete acquisition paths such as:

- mentor;
- coterie;
- institutional access;
- debt or boon;
- blood access;
- diablerie;
- lineage tradition;
- specific historical opportunity.

Time only creates opportunity. It does not itself grant powers.

Novydres also permits the local rule that additional powers may be acquired within Discipline levels already reached without increasing the Discipline rating, but this increases Power Density and therefore rarity burden.

### H.3 Power Density

Editorial states:

- `Standard`
- `Expanded`
- `High`
- `Exceptional`

Extra powers never fake a higher Discipline rating.

## I. Historical-reach architecture

Historical Reach is independent from age and measures actual participation plus preserved access to reliable memory.

Editorial levels:

- **I — Contemporary**
- **II — Witness**
- **III — Historical Veteran**
- **IV — Living Memory**
- **V — Foundational**

Age does not grant omniscience. A character may be old and poorly informed, or comparatively younger and exceptionally well connected to archives, witnesses, or institutions.

`Historical Peak` may be recorded when a prior period of greater authority, capability, or influence materially explains the 2010 state. It does not require reconstructing a second full historical sheet.

## J. Political and institutional power architecture

Political power is independent from personal mechanics.

Institutional power is audited through:

- formal authority;
- jurisdiction;
- legitimacy;
- resources;
- mobilization;
- access;
- constraints;
- chain fragility.

A young vampire may hold major office after the Beckoning while still suffering an `Experience Deficit`.

Positional Status does not accumulate across offices. Formal office never automatically grants Blood Potency, Disciplines, historical knowledge, or personal combat capacity.

### J.1 Mobilizable Capacity

Separate personal power from what a character can mobilize through:

- agents;
- subordinates;
- institutions;
- resources;
- jurisdiction;
- alliances;
- infrastructure.

Audit agent quality, speed, loyalty, political limits, cost, and chain fragility.

### J.2 Domain Competence

Institutional specialists may possess extraordinary superiority in a narrow domain without being globally powerful. `Domain Competence` creates indispensability without automatic dominance.

## K. Relationship hierarchy

Relationships are contextual vectors, not a single ladder.

Relevant forms include:

- personal coercion;
- institutional authority;
- social leverage;
- historical leverage;
- indirect protection or retaliation;
- boons and obligations;
- information asymmetry;
- dependency.

Lineage transmits opportunity and burden, not mastery.

A lineage may justify low Generation, access, mentors, traditions, resources, protection, enemies, expectations, boons, and claims. It does not automatically grant BP, Discipline mastery, density, combat ability, authority, or historical knowledge.

`inherit access ≠ inherit mastery`.

## L. Bairrismo integration

**Authority:** `NOVYDRES PROJECT CANON` for the existence/nature of Bairrismo; `NOVYDRES LOCAL RULE / HOMEBREW` for its mechanical implementation through V5-compatible Conviction/Touchstone/Humanity spaces.

Bairrismo is not a numeric Power Scale trait.

Rootedness is the primary predictor of exposure and consolidation; age, Generation, and BP are independent.

The phenomenon operates through two existing V5-compatible spaces:

1. a territorial Conviction oriented toward protection of Novydres, a raion, institution, community, place, or another concrete local anchor;
2. moral rupture when departure or abandonment becomes equivalent to abandoning that anchor.

Broad Convictions trigger more frequently and diffusely. Narrow Convictions trigger less often but can be more visceral.

Marco Territorial is a preferred but not mandatory Touchstone-like anchor. It does not create or automatically intensify Bairrismo.

Outsiders generally move through signs of belonging before consolidated Bairrismo:

- Forasteiro: no consolidated territorial Conviction by default;
- Residente: signs may appear;
- Enraizado: consolidation may occur after a narrative belonging milestone;
- Histórico: no automatic second layer.

Thin-Bloods and Caitiff can become rooted under normal rules, but their continued presence in Novydres is demographically rare and therefore demands trajectory explanation.

## M. Beckoning integration

**Authority:** the Beckoning itself is a `CANONICAL V5` setting premise; every eligibility threshold, BP-intensity band, duration, Desire-progression rule, trigger procedure, and Novydres exception stated in this section is `NOVYDRES LOCAL RULE / HOMEBREW` unless explicitly identified otherwise.

The Beckoning is treated as a selective demographic hollowing of the old and powerful layer, not a total wipe.

Generation determines ordinary eligibility:

- 3rd–9th: eligible;
- 10th+: normally not eligible;
- canonical exceptions may override this filter.

Age itself does not determine eligibility.

Blood Potency determines intensity:

| BP | Intensity | Label |
|---:|---:|---|
| 0–1 | 0 | Latent |
| 2–3 | 1 | Whisper |
| 4–5 | 2 | Call |
| 6+ | 3 | Imperative |

Duration when triggered:

- Intensity 0: none;
- Intensity 1: remainder of the current night;
- Intensity 2: 3 consecutive nights;
- Intensity 3: 7 consecutive nights.

During affected nights, each new Desire must advance the Call.

The Beckoning is triggered through normal Compulsion opportunities when fictionally pertinent. There are no periodic border or removal checks.

## N. Bairrismo × Beckoning interaction

**Authority:** `NOVYDRES LOCAL RULE / HOMEBREW`. This interaction is approved Novydres mechanics and is not presented as an official V5 Beckoning rule.

The two phenomena do not cancel one another.

The Beckoning shapes Desire toward the Call. Bairrismo makes territorial abandonment morally and emotionally intolerable.

This creates tension rather than a new resistance stat.

A rooted character may attempt to remain through partial compliance, research, preparation, agents, misdirection, bonds, wrong clues, or equivalent fictional means. Prolonged resistance at Intensity 3 is extraordinary.

Bairrismo provides no automatic anti-Beckoning bonus.

### N.1 Diablerie suppression

**Authority:** `NOVYDRES LOCAL RULE / HOMEBREW`. Suppression eligibility, victim-BP duration bands, and non-stacking behavior are local rules.

Diablerie may temporarily suppress manifestation of the Beckoning without removing eligibility or intensity.

Duration is based on victim BP:

| Victim BP | Suppression |
|---:|---|
| 0–1 | 1 month |
| 2–3 | 3 months |
| 4–5 | 1 year |
| 6–7 | 3 years |
| 8+ | 5 years |

Successive diableries do not stack. Keep the longer of the remaining duration and the newly calculated duration.

Repeated use creates major moral, political, and supernatural explanatory debt.

## O. Outlier architecture

Methuselah-scale, cosmological, or otherwise dominant figures must be treated as `Declared Outlier` when they sit outside the ordinary demographic architecture.

A declared outlier must answer:

- why this being exists;
- whether they are actually present in 2010;
- what limits their operational agency;
- what unique function they serve;
- why that function cannot simply be assigned to a strong elder.

Legendary editorial status is not equivalent to Methuselah status. Methuselah status is not equivalent to rulership.

### O.1 Exceptionalities

Qualitative exception classes:

- `Concentrated`
- `Composite`
- `Dominant`

`Dominant` normally implies Declared Outlier treatment.

A character may be exceptional because of power, trajectory, or both. These are distinct.

Thin-Bloods and Caitiff in Novydres are demographically rare. A rooted member of either condition may therefore be a high `Trajectory Exception` without being a high `Power Exception`.

## P. Rarity controls

### P.1 2010 demographic pyramid

The active resident population should form a normative pyramid:

- broad base: Crianças da Noite + Neófitos;
- smaller center: Ancillae;
- narrow active elder layer;
- residual individually named Methuselah/outlier presence.

A healthy citywide calibration is roughly 3–5 active Ancillae per active elder in representative population, without treating this as a hard quota.

Local raions and clans do not need to mirror the citywide pyramid.

### P.2 Survival funnel

Older cohorts should represent a smaller active fraction due to cumulative attrition through:

- Final Death;
- diablerie;
- conflict;
- Torpor;
- departure;
- withdrawal;
- Beckoning;
- other losses.

No actuarial rate is required.

### P.3 Clan/raion asymmetry

Distribution may be intentionally asymmetric by local history, migration, Embrace policy, war, institutional function, or lineage.

Primary interpretation order:

1. Novydres-specific clan identity;
2. local history;
3. institutions and raion;
4. individual trajectory;
5. broad canonical clan tendencies.

No global stereotype should override local clan identity.

Local divergence categories may include:

- Dissident;
- Displaced;
- Reformist;
- Marginal;
- Functional Exception.

### P.4 Caitiff and Thin-Blood presence

Both are demographically rare in Novydres.

They remain distinct categories, but the citywide audit also tracks their combined presence outside or at the margins of ordinary clan structures:

- `Residual`
- `Noticeable`
- `Overrepresented`

Two separate rarities must not silently sum into a common population.

### P.5 Ordinary Population Baseline

The nonexceptional active center of the city is mostly young/Neonate/Ancilla, common Generation, lower-to-middle BP, soft Discipline norms, few exceptional concentrations, and predominantly localized influence.

Ordinary does not mean featureless. Ordinary characters may have a clear defining peak.

Relative ordinary envelopes vary by stratum:

- Criança da Noite: limited, concentrated, dependent;
- Neófito: consolidated, local;
- Ancilla: more depth, relations, and function without automatically becoming elite;
- Ancião: ordinary among elders remains rare citywide and is still not universal excellence;
- Matusalém: no ordinary baseline; Declared Outlier.

There is no `Stratum = Threat Tier` rule.

### P.6 Functional Saturation

The city is audited not only for number of exceptional NPCs, but for redundant exceptional solutions to the same problem.

States:

- `Low`
- `Redundant`
- `Saturated`

Healthy institutional redundancy differs from repeated exceptional redundancy.

Post-Beckoning continuity may be categorized as:

- `Continuity`
- `Fragility`
- `Gap`

### P.7 Citywide Exception Register

The final architecture maintains a qualitative register of deliberate concentrations, asymmetries, and improbable trajectories by:

- scope;
- cause;
- consequence;
- status.

It is memory, not a slot system or quota.

Register-wide density may be read as:

- `Healthy`
- `Dense`
- `Saturated`

The audit asks whether enough ordinary, fragile, incomplete, and median space remains in the setting.

## Q. History ↔ mechanics consistency rules

Every exceptional characteristic creates explanatory debt.

Three gates apply:

1. **Legality** — does the construction respect V5 rules and approved Novydres rules?
2. **Individual plausibility** — does the character's trajectory explain the characteristic?
3. **Citywide coherence** — does the addition preserve rarity and distribution?

Possible is not free.

### Q.1 Current profile versus historical peak

The 2010 profile is authoritative for current power.

Historical Peak is recorded only when a prior state materially explains current:

- reputation;
- enemies;
- Prestações;
- legacy;
- succession;
- residual influence.

### Q.2 Actual versus perceived capability

When material, use `Perception Gap`:

- `Aligned`
- `Overestimated`
- `Underestimated`

Reputation can have real political effects without altering the sheet.

### Q.3 Competence Profile

Attributes, Skills, and Specialties do not scale automatically with age.

Use:

- `Core Competence`
- `Supporting Competence`
- `Incidental Competence`
- `Weak/Obsolete Areas`

Centuries create opportunity, not universal mastery.

### Q.4 Asset Portfolio

Material Advantages and Backgrounds require:

- `Source`
- `Control`
- `Access`
- `Mobilization`
- `Maintenance`
- `Dependency`
- `Exposure`

Time allows accumulation and erosion.

### Q.5 Psychological Resilience

Resolve, Composure, and Willpower are trajectory-dependent and not derived from age, Generation, BP, Status, or editorial importance.

When material, distinguish:

- `Baseline Resilience`
- `Pressure Points`
- `Recovery/Support`

This grants no automatic resistance to Beckoning or Bairrismo.

### Q.6 No retrospective XP entitlement

Do not calculate historical power by `age × XP rate`.

XP may later be used as a construction or validation tool, but age never creates an owed mechanical budget.

### Q.7 Mechanical Load Audit

A sheet may be audited qualitatively as:

- `Lean`
- `Focused`
- `Broad`
- `Dense`
- `Saturated`

This detects distributed mechanical inflation without becoming a score.

### Q.8 Counterweight, not Currency

Weaknesses, Flaws, dependencies, and counterplay do not pay for exceptional power.

Always distinguish:

- `Power Source`
- `Power Dependency`
- `Counterplay`

A vulnerability makes power contestable; it does not make power free.

### Q.9 Defining Peak and Constraint

Every materially relevant NPC should have a legible operational silhouette.

At minimum:

- `Defining Peak` — what makes the character operationally important;
- `Dependency / Constraint` — what sustains, localizes, or limits that power;
- `Counterplay` — when relevant, how it can be challenged.

A defining peak need not be a 5-dot trait or citywide exceptional capability.

## R. Existing NPC benchmark audit

This benchmark is documentary only. It does not complete sheets, infer missing mechanics, or resume NPC generation.

Unknown stays Unknown.

| NPC | Age/era | Generation | BP | Mechanical scale | Political scale | Bairrismo | Beckoning | Classification | Revalidation need |
|---|---|---:|---:|---|---|---|---|---|---|
| Mikhail Vasiliev | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | known roster relevance; details incomplete | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | complete under future character-creation gate |
| Mariya Vasilieva | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | known roster relevance; details incomplete | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | complete under future character-creation gate |
| Kuthulun | older historical figure; exact data UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | materially important lineage/political figure | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | targeted documentary completion before mechanics |
| Bispo Konstantin | historical/old; exact mechanics UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | principal political/institutional relevance | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | complete under future gate; audit exceptionalities if concentrated |
| Wilhelmina Harker | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | principal relevance | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | complete under future gate |
| Dom Sebastião | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | principal relevance | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | complete under future gate |
| Miriam Abramovich | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | principal relevance | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | complete under future gate |
| Fatima | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | principal relevance | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | complete under future gate |
| Iskander Yasupov | Embrace c. 1794 | 8 | 4 | full current v0.9 profile exists; mechanical completion pending; unresolved Discipline-power dependencies preserved | high positional relevance as Sheriff | UNKNOWN | ordinarily eligible; Intensity 2 if triggered under Novydres local rule | TARGETED REVALIDATION | targeted revalidation against approved citywide power-scale architecture; verify Generation/BP/Discipline envelope, exceptionalities, Bairrismo and Beckoning exposure later; no values changed here |
| Zoya | Embrace 1918 | 11 | 2 | full current v0.9 profile exists; mechanical completion pending; unresolved ritual/mechanical dependencies preserved | Harpia Maior + Chanceler; positional Status non-cumulative | UNKNOWN | normally ineligible by Generation under Novydres local rule | TARGETED REVALIDATION | targeted revalidation against approved citywide power-scale architecture; verify Generation/BP/Discipline envelope, ritual breadth/depth, exceptionalities, Bairrismo and Beckoning exposure later; no values changed here |
| Zara | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | principal relevance | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | complete under future gate |
| Sergei | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | principal relevance | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | complete under future gate |
| Khalil | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | principal relevance | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | complete under future gate |
| Gilgamesh | Foundational; active history from 1423, disappeared 1917 | UNKNOWN | UNKNOWN | revelation-protected/deferred | foundational historical authority | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | protected-envelope audit only; do not infer hidden mechanics |
| Vasya | historical elder/regent; called by 2010 | UNKNOWN | UNKNOWN | mechanics deferred | former regency / major historical-political weight | UNKNOWN | Beckoning materially established | TARGETED REVALIDATION | preserve Presence State and Shadow/Legacy distinction; mechanics deferred |
| Levi | legendary; exact era UNKNOWN | UNKNOWN | UNKNOWN | revelation-protected/deferred | legendary/historical | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | protected-envelope audit only |
| Baba Yaga | legendary lineage figure | UNKNOWN | UNKNOWN | revelation-protected/deferred | legendary/historical lineage significance | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | protected-envelope audit only |
| Durga Syn | legendary | UNKNOWN | UNKNOWN | revelation-protected/deferred | legendary/historical | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | protected-envelope audit only |
| Leah | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | secondary/embedded relevance | UNKNOWN | UNKNOWN | COMPLETE WHEN GENERATED | complete if/when individualized |

### R.1 Benchmark interpretation

`PASS` means enough material exists to test the relevant dimensions and no incompatibility is found.

`COMPLETE WHEN GENERATED` means concept/lore may remain valid, but the character lacks enough mechanics for full audit and has no known defect that requires reopening now.

`TARGETED REVALIDATION` means a material known point requires focused verification before mechanical completion.

`FULL REVALIDATION` is reserved for broad conflict with the architecture.

The absence of information is neither evidence of balance nor evidence of defect.

## S. Future NPC-generation requirements

Future relevant NPC generation must use two passes.

### S.1 Pre-sheet Power Envelope

Before full numbers, establish at least:

- narrative/setting role;
- chronological stratum;
- rootedness;
- Presence State;
- Generation rarity range;
- plausible BP range;
- Discipline shape;
- Defining Peak;
- Threat Profile or primary operational vector when relevant;
- institutional/social/historical power;
- Power Dependencies;
- exceptionalities;
- Bairrismo exposure;
- Beckoning eligibility/intensity if applicable.

### S.2 Post-sheet audit

After mechanics are generated, verify:

- Generation/BP legality;
- Discipline depth, breadth, mastery, and density;
- Mechanical Load;
- Competence Profile;
- Asset Portfolio;
- Power Dependencies;
- rarity and exception burden;
- published benchmark calibration;
- citywide impact.

A material upward change to the sheet requires rechecking the Power Envelope.

### S.3 Collective power

Recurring coteries, cells, teams, and small groups may require `Collective Power Profile`:

- `Complementarity`
- `Coordination`
- `Shared Resources`
- `Collective Reach`
- `Critical Dependencies`
- `Collective Threat Vector`

Collective Coverage may be:

- `Focused`
- `Complementary`
- `Comprehensive`

A Comprehensive small group can be collectively exceptional even if all members are individually reasonable.

## T. Existing NPC revalidation requirements

Every existing NPC is subject to universal audit but proportional intervention:

- `PASS`
- `COMPLETE WHEN GENERATED`
- `TARGETED REVALIDATION`
- `FULL REVALIDATION`

No automatic nerf, rewrite, or reopening follows from this architecture.

Existing unknown values must remain:

- `KNOWN`
- `INFERABLE`
- `UNKNOWN`

Editorial inference does not become canon and cannot cascade into later decisions as if established fact.

Legendary or revelation-protected NPCs may use a protected envelope:

- `Scale Known`
- `Mechanics Deferred`
- `Revelation Protected`

Protected does not mean unlimited.

## U. Retroactive dependency signals

### U.1 Mandatory next gate — character creation

The approval of this Power Scale does **not** by itself authorize resumption of Chapter 07 NPC generation.

A separate workstream must be closed first:

`character_creation_novydres_architecture`

Required scope:

- common character-construction core;
- PC and NPC derivations;
- modes/depth of resolution;
- causal history → resources → relations → capabilities → sheet;
- integration with the Power Scale;
- validation metrics;
- different resolution needs for incidental, secondary, principal, legendary, and other future categories;
- integration with the already deferred fast/full guided PC-creation architecture;
- preservation of Novydres-specific identity.

### U.2 Integration Contract for the future character-creation workstream

The future architecture must preserve these invariants:

1. Generation ≠ age ≠ BP.
2. Exceptional capability requires acquisition and trajectory.
3. Power remains vector-based, never reduced to a universal score.
4. Structural and conditional power remain distinct.
5. Rootedness/Bairrismo are not reducible to age or BP.
6. `Unknown stays Unknown` for incomplete existing NPCs.
7. Relevant NPCs use a pre-sheet Power Envelope and post-sheet audit.
8. Individual and citywide exceptionalities remain auditable.
9. Different resolution depths are allowed; incidental NPCs do not require full-character treatment.
10. The sheet is a consequence of trajectory, not a collection of numbers retroactively justified by biography.
11. Age cannot be converted into automatic retrospective XP.
12. Shared character invariants apply to PCs and NPCs, while citywide population controls remain NPC/setting-side controls.

### U.3 Institutional Battle interface

Control, Access, Mobilization, territorial infrastructure, fortress strength, and mobilizable organizational power directly interface with a future `Institutional Battle` mechanics workstream.

This document does not define those mechanics. The future workstream must consume these distinctions rather than flatten them into personal power.

### U.4 Editorial-map governance

This document reports dependencies. It does not itself modify `novydres_editorial_map` or Chapters 01–06.

## V. Validation checklist

Before Senior Editor approval, confirm:

- [x] No universal Power Score introduced.
- [x] Generation separated from age.
- [x] BP bound to Generation plus trajectory.
- [x] Discipline Depth, Breadth, Mastery Load, and Power Density separated.
- [x] Published NPCs treated as calibration, not caps.
- [x] Elder demographics reduced by survival funnel and Beckoning.
- [x] Active population separated from historical/potential power mass.
- [x] Torpor, absence, and elimination distinguished.
- [x] Institutional power separated from personal mechanics.
- [x] Mobilizable Capacity separated from personal capacity.
- [x] Bairrismo integrated without a new numeric trait.
- [x] Beckoning integrated without a new resistance trait.
- [x] Methuselah/outlier architecture defined.
- [x] Ordinary population baseline defined without average-sheet template.
- [x] Citywide Exception Register defined without quotas.
- [x] Thin-Blood and Caitiff rarity treated separately and jointly audited.
- [x] Competence, resources, and psychological resilience protected against age-based inflation.
- [x] Retrospective XP entitlement rejected.
- [x] Mechanical Load Audit defined.
- [x] Weaknesses do not pay for power.
- [x] Defining Peak and Dependency/Constraint required for materially relevant NPCs.
- [x] Collective Power Profile defined.
- [x] Existing NPC benchmark included without generating missing mechanics.
- [x] `Unknown stays Unknown` preserved.
- [x] Next mandatory character-creation gate recorded.
- [x] NPC generation remains blocked after this workstream until that gate closes.
- [x] Authority classes distinguish `CANONICAL V5`, `NOVYDRES PROJECT CANON`, `NOVYDRES LOCAL RULE / HOMEBREW`, and `EDITORIAL INFERENCE`.
- [x] No local Beckoning or diablerie-suppression procedure is presented as canonical V5.
- [x] Iskander and Zoya are recognized as existing full v0.9 profiles while remaining mechanically non-final and `TARGETED REVALIDATION`.
- [x] `NPC-POWER-001–106` remain unchanged.

## W. Final readiness verdict

**READY FOR SENIOR EDITOR REVALIDATION**

The `npc_power_scale_citywide` workstream is conceptually closed under `Closure by Invariants + Auditability`.

The architecture can now judge:

1. **Plausibility** — whether a characteristic fits V5 and Novydres.
2. **Causality** — whether a trajectory explains how the character acquired or retained it.
3. **Relative Rarity** — whether the feature is ordinary, rare, exceptional, or outlier-scale in the city.
4. **Citywide Impact** — whether adding the character/group materially changes the power distribution of Novydres.

No additional character-construction microdecisions should be added to this workstream unless a blocking gap is discovered against one of those four functions.

**NPC-generation readiness remains blocked.**

Required sequence:

`npc_power_scale_citywide`
→ Senior Editor revalidation
→ `character_creation_novydres_architecture`
→ Senior Editor gate revalidation
→ only then eligibility to resume `GAP-NPC-001 / GAP-NPC-010` and Chapter 07 NPC generation.