---
document_id: novydres_character_creation_architecture_decision_inventory
version: 0.1.3
status: candidate_for_senior_editor_revalidation
date: 2026-08-21
scope: character_creation_novydres_architecture_inventory_RETRO_Q092_lineage_propagation
supersedes: novydres_character_creation_architecture_decision_inventory_v0_1_2.md
corrective_scope: RETRO-Q092_lineage_preserving_boundary_handoff_reclassification_only
substantive_question_changes: CHAR-CREATE-Q-092_active_meaning_reclassified_without_new_ID
target_gap: character_creation_novydres_architecture
decision_state: questions_only_no_rules_approved
authority_note: "This artifact inventories unresolved decision surfaces. It is not a decisions ledger and does not authorize any character-creation rule."
---

# Novydres Character Creation Architecture — Decision Inventory v0.1.2

## 1. Purpose

This file records unresolved material decision surfaces that later specialist workstreams must own before `character_creation_novydres_architecture` can close.

**Nothing in this inventory is an approved rule.** `CHAR-CREATE-Q-*` identifiers are question IDs only.

`Grill required = YES` means the future specialist should normally take the issue to `skill_grill_me_v1_1.md` after documentary and canonical research are exhausted. `CONDITIONAL` means an upstream choice must first activate the question.

`RETRO-CHAR-A-001` remains preserved: exactly two character-creation modes exist (`Rápido`, `Guiado`), both usable for PCs and NPCs.

`RETRO-Q092` propagation note: the approved 2026-08-21 retcon separates **Quick Character Creation** from a distinct **Quick Coterie Creation** execution surface. `CHAR-CREATE-Q-092` is preserved rather than deleted: its active meaning is now the character-side boundary/handoff. The coterie procedure itself consumes J2 and does not create a third character-creation mode or a 135th question.

## 2. Inventory

| ID | Decision surface | Why needed | Dependencies | Proposed subagent | Grill required | Blocking |
|---|---|---|---|---|---|---|
| CHAR-CREATE-Q-001 | Canonical starting creation sequence and mandatory starting fields | Needed to establish the V5 legality spine consumed by every mode. | Standalone Rules; official V5 Core | A | YES | MILESTONE |
| CHAR-CREATE-Q-002 | Attribute allocation baseline | Every mechanically complete character requires a legal Attribute package. | Official V5 Core | A | YES | MILESTONE |
| CHAR-CREATE-Q-003 | Skill allocation baseline | Defines the common mechanical competence input. | Official V5 Core | A | YES | MILESTONE |
| CHAR-CREATE-Q-004 | Specialty acquisition timing and legality | Prevents narrative specialties from becoming a parallel Skill mechanic. | Official V5 Core; Standalone catalogue policy | A | YES | MILESTONE |
| CHAR-CREATE-Q-005 | Discipline starting-selection baseline | Needed before any mode can produce a legal sheet. | Official V5 Core; admitted official expansions | A | YES | MILESTONE |
| CHAR-CREATE-Q-006 | Discipline-power selection interface | Creation must choose powers without duplicating the authoritative catalogue. | Standalone single-authority policy; admitted source inventory | A | YES | MILESTONE |
| CHAR-CREATE-Q-007 | Advantages/Backgrounds/Merits/Flaws selection interface | Creation owns selection order, not catalogue duplication. | Standalone Rules | A | YES | MILESTONE |
| CHAR-CREATE-Q-008 | Predator Type baseline and selection timing | Predator Type changes starting outputs and biography. | Official V5 Core; admitted official expansions | A | YES | MILESTONE |
| CHAR-CREATE-Q-009 | Convictions/Touchstones/Humanity baseline | Needed before local Bairrismo/Marco integration can be layered safely. | Official V5 Core | A | YES | MILESTONE |
| CHAR-CREATE-Q-010 | Derived values and starting-state fields | Health, Willpower, Hunger and other required fields must converge in all modes. | Official V5 Core; Standalone Rules | A | YES | MILESTONE |
| CHAR-CREATE-Q-011 | Clan-specific creation effects | Supported clans must be operable standalone and normalized across sources. | Official V5 Core; Player's Guide; admitted sources | A | YES | MILESTONE |
| CHAR-CREATE-Q-012 | Thin-Blood/Caitiff creation baseline | Supported options interact with local demographic rarity without becoming power penalties. | Official V5; Power Scale | A | YES | MILESTONE |
| CHAR-CREATE-Q-013 | Loresheet creation interaction | Determine where Loresheets enter creation without making them truth homes. | Official V5; Revelation Architecture | A | YES | MILESTONE |
| CHAR-CREATE-Q-014 | Official source-admission cut for character building | One book cannot be assumed to contain every supported option. | Standalone sourcebook admission policy; current official V5 line | A | YES | MILESTONE |
| CHAR-CREATE-Q-015 | Supersession/errata normalization rules for creation options | Creation must not surface obsolete duplicated options. | Standalone Rules | A | YES | MILESTONE |
| CHAR-CREATE-Q-016 | Homebrew option admission boundary at creation | Selected homebrew is allowed but must remain identified and curated. | Standalone Rules; editorial governance | A | YES | MILESTONE |
| CHAR-CREATE-Q-017 | Standard PC starting power envelope | Defines fair default without inheriting NPC population controls. | Power Scale NPC-POWER-099; A | B | YES | MILESTONE |
| CHAR-CREATE-Q-018 | Ancilla/older-PC creation envelope | Supports advanced chronicles without age-to-XP conversion. | Power Scale NPC-POWER-100; A | B | YES | MILESTONE |
| CHAR-CREATE-Q-019 | Generation choice/derivation at creation | Generation is genealogical and cannot be an age proxy. | Power Scale NPC-POWER-004; A | B | YES | MILESTONE |
| CHAR-CREATE-Q-020 | Starting Blood Potency procedure | Must remain inside Generation limits and trajectory logic. | Power Scale NPC-POWER-007/008; A | B | YES | MILESTONE |
| CHAR-CREATE-Q-021 | Torpor impact on pre-chronicle BP trajectory | Long histories need legal trajectory without automatic age conversion. | Power Scale; canonical V5 review | B | YES | MILESTONE |
| CHAR-CREATE-Q-022 | Discipline Depth starting envelope by mode | Constrains legal but excessive outputs. | Power Scale NPC-POWER-009/010; A | B | YES | MILESTONE |
| CHAR-CREATE-Q-023 | Discipline Breadth starting envelope by mode | Prevents historical play from producing unlimited breadth. | Power Scale; A | B | YES | MILESTONE |
| CHAR-CREATE-Q-024 | Power Density / extra-power handling at creation | Local extra powers within reached levels carry rarity weight. | Power Scale NPC-POWER-011/012 | B | YES | MILESTONE |
| CHAR-CREATE-Q-025 | Rare/out-of-clan acquisition proof standard | Played history may justify acquisition, but proof must be operationalized. | Power Scale NPC-POWER-011/039/067; D | B | YES | MILESTONE |
| CHAR-CREATE-Q-026 | Mechanical Load validation point | Needs pre/post audit without a universal point score. | Power Scale NPC-POWER-102 | B | YES | MILESTONE |
| CHAR-CREATE-Q-027 | Exceptional-background/asset envelope | Assets require source, control, maintenance, dependency and exposure. | Power Scale NPC-POWER-097; C | B | YES | MILESTONE |
| CHAR-CREATE-Q-028 | PC exception handling versus citywide rarity | PCs share causality; NPC demographics must not become automatic PC restrictions. | Power Scale NPC-POWER-099 | B | YES | MILESTONE |
| CHAR-CREATE-Q-029 | Legendary/Methuselah NPC protected-envelope interface | Bounds legendary creation without forcing hidden mechanics into canon. | B; F | I | YES | MILESTONE |
| CHAR-CREATE-Q-030 | Creation-time rootedness classification | Distinguishes local/resident/rooted/historical without age coupling. | Power Scale NPC-POWER-003/016 | C | YES | MILESTONE |
| CHAR-CREATE-Q-031 | Local-born/locally-formed Bairrismo starting treatment | Exact creation application remains open though authority permits territorial Conviction. | Power Scale NPC-POWER-026; A | C | YES | MILESTONE |
| CHAR-CREATE-Q-032 | Newcomer Bairrismo acquisition interface | Represents newcomers without granting consolidated Bairrismo by default. | Power Scale §L | C | YES | MILESTONE |
| CHAR-CREATE-Q-033 | Marco Territorial selection timing | Preferred but not mandatory; timing remains open. | Power Scale NPC-POWER-027; A | C | YES | MILESTONE |
| CHAR-CREATE-Q-034 | Marco Territorial versus ordinary Touchstone representation | Prevents conflation while using V5-compatible spaces. | Power Scale §L; A | C | YES | MILESTONE |
| CHAR-CREATE-Q-035 | Raion/domain placement as creation input versus output | Play Guidance sends territorial positioning into creation. | Play Guidance; Atlas | C | YES | MILESTONE |
| CHAR-CREATE-Q-036 | Faction/sect/institutional affiliation timing | Integrates setting without making every affiliation mandatory. | Chapters 04–06; Play Guidance | C | YES | MILESTONE |
| CHAR-CREATE-Q-037 | Creation-time Status acquisition boundary | Must not conflict with Chapter 05 Recognition/Status authority. | Chapter 05 v0.2.2 | C | YES | MILESTONE |
| CHAR-CREATE-Q-038 | Positional Status and office at creation | Office cannot silently grant personal mechanics; multi-office Status is non-cumulative. | Chapter 05 v0.2.2; Power Scale | C | YES | MILESTONE |
| CHAR-CREATE-Q-039 | Dignitas creation ownership and timing | Dignitas sits outside Chapter 05; creation needs only an interface. | Ventrue material; Chapter 05 migration authority | C | YES | MILESTONE |
| CHAR-CREATE-Q-040 | Prestações at creation | Determine whether starting boons/debts are mandatory, optional or advanced. | Chapter 05 v0.2.2 | C | YES | MILESTONE |
| CHAR-CREATE-Q-041 | Patrons/enemies/reputation/social debts mapping | Connects narrative relations to mechanics without forced one-to-one conversion. | Power Scale relationship vectors; A | C | YES | MILESTONE |
| CHAR-CREATE-Q-042 | Office Functional Fit validation | Officeholder must be sustainable without office becoming a stat floor. | Power Scale NPC-POWER-057/058 | C | YES | MILESTONE |
| CHAR-CREATE-Q-043 | Smallest played-history unit | Required before sequencing or prompt architecture. | B; A | D1 | YES | MILESTONE |
| CHAR-CREATE-Q-044 | Unit minimum outputs | Determines what an event may/should change. | A; B; C | D1 | YES | MILESTONE |
| CHAR-CREATE-Q-045 | Chronological advancement model | Supports characters across very different ages. | B | D1 | YES | MILESTONE |
| CHAR-CREATE-Q-046 | Age-scaling model for event count/density | Prevents both under- and over-simulation. | B | D1 | YES | MILESTONE |
| CHAR-CREATE-Q-047 | Quiet-period abstraction | Compresses uneventful decades/centuries. | B | D1 | YES | MILESTONE |
| CHAR-CREATE-Q-048 | Torpor compression within lifepath | Represents long absence without fake XP or event spam. | B; F; D1 | D2 | YES | MILESTONE |
| CHAR-CREATE-Q-049 | Prompt-family taxonomy | Required before original prompts can be commissioned. | A; C; F; D1 | D2 | YES | MILESTONE |
| CHAR-CREATE-Q-050 | Prompt sequencing prerequisites | Events may require Embrace, arrival, affiliation or relationships. | A; C | D1 | YES | MILESTONE |
| CHAR-CREATE-Q-051 | Branching architecture | Prior events must be able to affect later eligibility. | E; F; D1 | D2 | YES | MILESTONE |
| CHAR-CREATE-Q-052 | Randomization method | Balances discovery with legality and canon. | A; B; F; D1 | D2 | YES | MILESTONE |
| CHAR-CREATE-Q-053 | Player-choice versus constrained-random balance | Defines authorship versus discovery. | A; B | D1 | YES | MILESTONE |
| CHAR-CREATE-Q-054 | Reroll/veto/override policy | Handles impossible, unwanted or canon-conflicting results. | F; safety policy; D1 | D2 | YES | MILESTONE |
| CHAR-CREATE-Q-055 | Mechanical-consequence budget interface | Historical play cannot become unlimited XP. | B | D1 | YES | MILESTONE |
| CHAR-CREATE-Q-056 | Negative-outcome/loss categories | History needs cost without arbitrary core-mechanic deletion. | B; E; D1 | D2 | YES | MILESTONE |
| CHAR-CREATE-Q-057 | Safety/content calibration layer | Mature themes need table control without unnecessary duplicate systems. | Editorial governance | D1 | YES | MILESTONE |
| CHAR-CREATE-Q-058 | Collaborative versus solo execution mode | TYOV is solo-native; Novydres is collaborative tabletop. | Play Guidance; J1 | D1 | YES | MILESTONE |
| CHAR-CREATE-Q-059 | Prompt-engine data dependencies and state transitions | Later prompts need structured prior state. | E; F; D1 | D2 | YES | MILESTONE |
| CHAR-CREATE-Q-060 | Persistent memory subsystem versus narrative abstraction | Central adaptation choice affecting burden and historical knowledge. | D1; Revelation Architecture | E | YES | MILESTONE |
| CHAR-CREATE-Q-061 | Memory capacity/forgetting representation if retained | Only relevant if persistent memory is approved. | E memory decision | E | CONDITIONAL | DOWNSTREAM |
| CHAR-CREATE-Q-062 | Post-creation fate of generated memories | Temporary scaffold versus persistent record must be clear. | D1 | E | YES | MILESTONE |
| CHAR-CREATE-Q-063 | Relationship ontology | Needs structured outputs for Sire/Mawla/Childe/allies/rivals/etc. | A; D1 | E | YES | MILESTONE |
| CHAR-CREATE-Q-064 | Relationship state transitions during history | Needed if events transform bonds. | D1 | E | YES | MILESTONE |
| CHAR-CREATE-Q-065 | Relationship mechanical versus narrative mapping | Prevents every relation from becoming a V5 Background. | A | E | YES | MILESTONE |
| CHAR-CREATE-Q-066 | Mortal relationship death handling | Long-lived vampires outlive mortals. | D1; A | E | YES | MILESTONE |
| CHAR-CREATE-Q-067 | Descendants/institutions as temporal replacements | Supports continuity without automatic Touchstone inheritance. | A; D1 | E | YES | MILESTONE |
| CHAR-CREATE-Q-068 | Current Touchstone validity after historical creation | Final V5 sheet must distinguish dead historical contacts from current Touchstones. | A | E | YES | MILESTONE |
| CHAR-CREATE-Q-069 | Mask/identity replacement across eras | Long-lived identities need continuity without stacked free Backgrounds. | A; D1 | E | YES | MILESTONE |
| CHAR-CREATE-Q-070 | Haven/resource persistence and replacement | Historical assets need current validity. | A; B | E | YES | MILESTONE |
| CHAR-CREATE-Q-071 | Narrative resource terminology | Avoids collision with V5 Resources Background. | A; D1 | E | YES | MILESTONE |
| CHAR-CREATE-Q-072 | Narrative skill/capability terminology | Avoids collision with V5 Skills. | A; D1 | E | YES | MILESTONE |
| CHAR-CREATE-Q-073 | Supporting-character terminology | Avoids collision with mechanical relation traits. | A; D1 | E | YES | MILESTONE |
| CHAR-CREATE-Q-074 | Lasting consequence/mark destination rules | Determines mapping to Flaws/reputation/scars/secrets/descriptors or narrative only. | A; B; D1 | E | YES | MILESTONE |
| CHAR-CREATE-Q-075 | Canonical history event-source inventory for lifepath | Played history must draw from canon without invention. | Chapters 02–06; Editorial Map | F | YES | MILESTONE |
| CHAR-CREATE-Q-076 | Witness/participant/hearsay/late-arrival state model | Aligns biography with Historical Reach and knowledge limits. | Power Scale NPC-POWER-014; Revelation | F | YES | MILESTONE |
| CHAR-CREATE-Q-077 | Historical Reach assignment/update interface | Age cannot grant omniscience. | Power Scale §I | F | YES | MILESTONE |
| CHAR-CREATE-Q-078 | Protected-truth boundary during creation | Creation must never become a competing truth home. | Revelation Architecture | F | YES | MILESTONE |
| CHAR-CREATE-Q-079 | Player knowledge versus character belief separation | Guided creation may distinguish player context from character belief. | Revelation Architecture | F | YES | MILESTONE |
| CHAR-CREATE-Q-080 | Storyteller-only intervention points | Needed for secret-dependent history without exposing objective resolution. | Revelation Architecture; D1 | F | YES | MILESTONE |
| CHAR-CREATE-Q-081 | 1917 disappearance participation boundary | Major canon event requires controlled access. | Chapter 02; Revelation | F | YES | MILESTONE |
| CHAR-CREATE-Q-082 | Founding/major-war participation eligibility | Participation must respect age, presence and rarity. | Power Scale; chronology | F | YES | MILESTONE |
| CHAR-CREATE-Q-083 | Arrival-in-Novydres event architecture | Connects migration, rootedness and local history. | C; D1 | F | YES | MILESTONE |
| CHAR-CREATE-Q-084 | Beckoning historical exposure integration | Older eligible characters may have trajectory effects without deterministic removal. | Power Scale §§M–N; B | F | YES | MILESTONE |
| CHAR-CREATE-Q-085 | Historical Peak versus current 2010 profile | Prior authority can explain present effects without second full sheet. | Power Scale NPC-POWER-089 | F | YES | MILESTONE |
| CHAR-CREATE-Q-086 | Canon contradiction resolution procedure | Impossible generated outcomes need deterministic handling. | Revelation; governance; D1 | F | YES | MILESTONE |
| CHAR-CREATE-Q-087 | Mandatory common output fields in Quick Creation | Quick characters must be immediately usable and schema-compatible. | A; B; C | G | YES | MILESTONE |
| CHAR-CREATE-Q-088 | Quick mechanical allocation method | Accelerates common legal architecture without second system. | A; B | G | YES | MILESTONE |
| CHAR-CREATE-Q-089 | Quick narrative minimum | Enough identity/history/relations for Novydres operation. | C; Play Guidance | G | YES | MILESTONE |
| CHAR-CREATE-Q-090 | Quick Bairrismo/Marco handling | Local integration must survive fast creation. | C | G | YES | MILESTONE |
| CHAR-CREATE-Q-091 | Quick political/territorial placement handling | Play Guidance inputs must survive acceleration. | C; Play Guidance | G | YES | MILESTONE |
| CHAR-CREATE-Q-092 | Quick Character ↔ Quick Coterie boundary/handoff | Quick Character Creation must interoperate with a separate J2-governed Quick Coterie procedure without embedding coterie creation or creating a third character mode. | J2; C; Play Guidance | G | YES | MILESTONE |
| CHAR-CREATE-Q-093 | Quick secondary-NPC reuse boundary | Determines whether Quick shortcuts can support secondary NPC application profiles when compared against the finalized Guided path, without new ontology. | G; H | I | YES | MILESTONE |
| CHAR-CREATE-Q-094 | Quick-to-Guided upgrade path | Adds historical depth later without mechanical duplication. | G; D2 | H | YES | MILESTONE |
| CHAR-CREATE-Q-095 | Quick-mode validation checklist | Parity, V5 legality and local integration checks. | A; B; C | G | YES | MILESTONE |
| CHAR-CREATE-Q-096 | Guided-mode step ordering | Integrates mechanics and played history without circularity. | A; B; C; D2; E; F | H | YES | MILESTONE |
| CHAR-CREATE-Q-097 | Mechanics-first versus history-discovery interaction | Determines which traits are chosen versus discovered/justified. | A; D2 | H | YES | MILESTONE |
| CHAR-CREATE-Q-098 | Convictions discovery versus preselection | Must remain V5 legal while supporting history. | A; D2; E | H | YES | MILESTONE |
| CHAR-CREATE-Q-099 | Touchstone creation timing | Present-day Touchstones must survive long-history logic. | A; E | H | YES | MILESTONE |
| CHAR-CREATE-Q-100 | Guided-mode mechanical parity with Quick | More work must not silently mean more points. | B; G | H | YES | MILESTONE |
| CHAR-CREATE-Q-101 | Guided-mode stopping/completion criteria | Pre-chronicle workflow must be finite. | D2; E; F | H | YES | MILESTONE |
| CHAR-CREATE-Q-102 | Guided character artifact assembly | Temporary lifepath state must terminate in canonical model. | A; B; C; D2; E; F | H | YES | MILESTONE |
| CHAR-CREATE-Q-103 | Advanced/older PC guided profile | Older play must not default to escalation. | B; D2 | H | YES | MILESTONE |
| CHAR-CREATE-Q-104 | Coterie shared-history insertion point | Individual and group histories may intersect. | J2; D2 | H | YES | MILESTONE |
| CHAR-CREATE-Q-105 | Session-zero/Play Guidance handoff | Positioning enters; completed PCs/coterie return to workflow. | Play Guidance; G; J2 | H | YES | MILESTONE |
| CHAR-CREATE-Q-106 | NPC resolution-depth taxonomy | Need explicit differences among main/secondary/legendary/dependent/official/minor. | Chapter 07; Power Scale | I | YES | MILESTONE |
| CHAR-CREATE-Q-107 | NPC common-core mandatory fields by depth | Omissions by depth cannot change ontology. | A; B; C | I | YES | MILESTONE |
| CHAR-CREATE-Q-108 | Pre-sheet Power Envelope procedure | Relevant NPCs require envelope before numbers. | Power Scale NPC-POWER-055 | I | YES | MILESTONE |
| CHAR-CREATE-Q-109 | Post-sheet Power Scale audit | Needs second-pass plausibility/rarity/citywide review. | Power Scale NPC-POWER-055/056 | I | YES | MILESTONE |
| CHAR-CREATE-Q-110 | Main NPC history depth | When full played history is warranted remains open. | D2; E; F | I | YES | MILESTONE |
| CHAR-CREATE-Q-111 | Secondary NPC abbreviated history | Low-friction generation without fake completeness; I decides whether the depth profile consumes Quick or Guided. | D2; G; H | I | YES | MILESTONE |
| CHAR-CREATE-Q-112 | Legendary NPC protected-envelope profile | Preserves mystery while auditing scale. | B; F | I | YES | MILESTONE |
| CHAR-CREATE-Q-113 | Dependent/stat-block depth profile | Minimum operational completeness without full character treatment. | Chapter 07 | I | YES | MILESTONE |
| CHAR-CREATE-Q-114 | Recurring officeholder Functional Fit | Office importance may rely on resources/delegation rather than high stats. | B; C | I | YES | MILESTONE |
| CHAR-CREATE-Q-115 | Unknown-data preservation in generation/revalidation | Existing unknowns cannot be silently inferred. | Power Scale NPC-POWER-077 | I | YES | MILESTONE |
| CHAR-CREATE-Q-116 | Existing-profile revalidation procedure after milestone | Needs controlled queue, not automatic rewrite. | Chapter 07; Power Scale | I | YES | MILESTONE |
| CHAR-CREATE-Q-117 | Coterie creation placement in workflow | Before/after/interleaved/hybrid remains unresolved. | Play Guidance; A; C | J2 | YES | MILESTONE |
| CHAR-CREATE-Q-118 | Coterie type baseline and admitted expansions | Official group options require provenance review. | Official V5 Core; Player's Guide | J2 | YES | MILESTONE |
| CHAR-CREATE-Q-119 | Shared Domain creation | Must align with local territory/domain authority. | C | J2 | YES | MILESTONE |
| CHAR-CREATE-Q-120 | Coterie Advantages/Flaws ownership | Group mechanics stay in authoritative rules/catalogues. | A; Standalone Rules | J2 | YES | MILESTONE |
| CHAR-CREATE-Q-121 | Shared history procedure | Determines whether group history uses played engine. | D2 | J2 | YES | MILESTONE |
| CHAR-CREATE-Q-122 | Shared patron/enemy/obligation generation | Political integration without mandatory mechanic conversion. | C; E | J2 | YES | MILESTONE |
| CHAR-CREATE-Q-123 | Relationship graph among members | Structured bonds/tensions feed individual and group play. | E | J2 | YES | MILESTONE |
| CHAR-CREATE-Q-124 | Collective Power Profile validation | Groups require complementarity/reach/dependency audit. | Power Scale NPC-POWER-086/087 | J2 | YES | MILESTONE |
| CHAR-CREATE-Q-125 | Coterie output schema and Play Guidance return | Group must return stable social/territorial/political state. | Play Guidance; C | J2 | YES | MILESTONE |
| CHAR-CREATE-Q-126 | Canonical common character ontology | One model must underlie PC/NPC/played history. | A; B; C; D1; E; F; D2; G; H; I; J2 | K | YES | MILESTONE |
| CHAR-CREATE-Q-127 | Canonical output schema ownership by field | Prevents duplicate authority. | A; B; C; D1; E; F; D2; G; H; I; J2 | K | YES | MILESTONE |
| CHAR-CREATE-Q-128 | Quick/Guided equivalence validation | Same legal model; no systematic power premium. | G; H; B | K | YES | MILESTONE |
| CHAR-CREATE-Q-129 | PC/NPC common-core validation | NPC differences are depth/control differences, not parallel game. | H; I | K | YES | MILESTONE |
| CHAR-CREATE-Q-130 | Terminology normalization | Resolve Resource/Resources, Skill/Skills and related collisions. | E; A | K | YES | MILESTONE |
| CHAR-CREATE-Q-131 | V5 legality and source-provenance validation | Inherited/expanded/local rules need explicit authority. | A; B; C | K | YES | MILESTONE |
| CHAR-CREATE-Q-132 | Power Scale compliance validation | Preserves invariants/envelopes/NPC-only controls. | B; I; Power Scale | K | YES | MILESTONE |
| CHAR-CREATE-Q-133 | Revelation/canon validation | History creation cannot leak truth or contradict chronology. | F; H; I | K | YES | MILESTONE |
| CHAR-CREATE-Q-134 | Standalone and publication-architecture validation | Procedure self-contained; no duplicated catalogues. | Standalone; Play Guidance; Format; Editorial Map | K | YES | MILESTONE |

## 3. Count and distribution

Total unresolved question IDs: **134**.

| Execution owner/phase | Question IDs owned | Estimated specialist decision range |
|---|---:|---:|
| A — Core V5 Creation Baseline & Admission Interface | 16 | 18–25 material decisions |
| B — Character Power Envelope | 12 | 18–28 material decisions |
| C — Social, Territorial & Political Integration | 13 | 20–30 material decisions |
| D1 — Played History Core | 10 | 12–20 material decisions |
| E — Memory, Relationships & Temporal Persistence | 15 | 20–30 material decisions |
| F — History, Chronology & Revelation Integration | 12 | 15–25 material decisions |
| D2 — Played History Finalization / Integration | 7 | 8–15 material decisions |
| G — Quick Creation Mode | 7 | 10–18 material decisions |
| H — Guided Creation Mode / Integration | 11 | 15–25 material decisions |
| I — NPC Creation Application & Depth Profiles | 13 | 15–25 material decisions |
| J1 — Coterie Canonical Baseline | 0 | research preflight; no project decisions |
| J2 — Coterie Creation Architecture | 9 | 15–25 material decisions |
| K — Final Integration & Validation | 9 | 10–18 material decisions |

D1 and D2 are execution phases of the same broader Played History specialist domain. J1 is a canonical-research preflight with no `CHAR-CREATE-Q-*` ownership; J2 owns all coterie creation decisions. The total number of material question surfaces remains **134**.

RETRO-Q092 validation: `Q-092` remains one G-owned lineage surface; the separate Quick Coterie execution surface adds no question ID. G therefore remains at 7 inventory surfaces and J2 at 9.

The raw inventory count is deliberately larger than each expected grill. Several rows may collapse after canonical research, become conditional, or be resolved by existing authority. A specialist must **not** force one grill question per inventory row.

## 4. Governance

- Documentary memory first.
- Canonical-source research before V5 questions.
- One material decision owner only.
- No specialist may silently decide a question owned by another specialist.
- Later decision ledgers record only decisions actually grilled/approved.
- If documentary authority already answers a row, close it by authority rather than re-grilling.
- If a creation requirement conflicts with `novydres_npc_power_scale_citywide_v0_1_1.md`, report `POWER SCALE INTERFACE CONFLICT`; do not patch Power Scale.
- This inventory does not authorize specialist execution. Main Senior Editor must approve decomposition first.