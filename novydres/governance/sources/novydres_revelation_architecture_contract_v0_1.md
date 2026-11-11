---
document_id: novydres_revelation_architecture_contract
version: 0.1
status: candidate
date: 2026-08-05
scope: gap_arch_003_resolution
target_gap: GAP-ARCH-003
supersedes: null
depends_on:
  - novydres_editorial_governance_v1_0.md
  - skill_grill_me_v1_0.md
  - novydres_gap_registry_v0_2.json
  - novydres_next_gap_decision_v0_2.md
  - novydres_format_contract_v0_2.md
  - novydres_play_guidance_contract_v0_1.md
  - novydres_play_guidance_decisions_v0_1.md
  - novydres_play_guidance_editorial_review_v0_1.md
  - latest novydres_editorial_map_*.json
decision_log: novydres_revelation_architecture_decisions_v0_1.md
---

# Novydres — Global Revelation Architecture Contract v0.1

## Purpose

This contract defines the authoritative global architecture for revelation, audience safety, in-fiction knowledge, uncertain information, secrets, progressive discovery, cross-references and information ownership across Novydres.

Its purpose is not to write hidden lore, Chapter 13, Loresheets, adventures or replacement chapter prose. Its purpose is to make every future information item classifiable without reopening GAP-ARCH-003.

For any future claim, an editor must be able to determine:

1. who may read it;
2. what a character may know;
3. what its objective truth status is internally;
4. how it may be presented player-facing;
5. where its authoritative truth lives;
6. whether it may be restated elsewhere;
7. whether a cross-reference is required;
8. how it may appear in a physical editorial unit;
9. whether its navigation metadata creates spoiler risk.

## Gap Being Resolved

**GAP-ARCH-003 — Fechar arquitetura global player-facing versus Storyteller-facing.**

The project already contains local patterns for player-safe prose, rumors, superscript references, Loresheets, Storyteller operational guidance, Storyteller secrets and DEU safety. This contract unifies them into one global information architecture.

---

# 1. Core Model

Novydres MUST treat the following as independent dimensions:

1. **Reader Access** — who may safely read the artifact.
2. **Character Knowledge** — what a character is reasonably entitled to know in-fiction.
3. **Truth State** — the project's internal objective status of a claim.
4. **Information Form** — how the claim circulates in-fiction or is presented editorially.
5. **Truth Ownership** — where the authoritative resolution lives.

These dimensions MUST NOT be collapsed into one taxonomy.

A player may be allowed to read something that their character does not know.

A Storyteller-facing passage may be operational without being secret.

A rumor may be true, false, partial, disputed or unresolved.

A true claim does not have to be presented to players as an objectively certified fact.

---

# 2. Audience Model

## 2.1 Reader Access Classes

The authoritative reader-access vocabulary is:

### `player_safe`

The content may be freely read and handled by players without crossing a protected spoiler boundary.

`player_safe` does **not** mean:

- every character knows it;
- it is objectively true;
- it is common mortal knowledge;
- it is mechanically available to every character.

### `storyteller_operational`

The content is reserved for the Storyteller because it supports preparation, operation, tracking, scene management, NPC operation or chronicle management.

It is **not automatically hidden lore**.

Examples of function, not content:

- preparation procedure;
- pressure tracking;
- scene-use instructions;
- reaction logic;
- operational reminders.

### `storyteller_secret`

The content contains a protected answer, resolution, hidden context or revelation whose unrestricted player access could compromise discovery, mystery, uncertainty or plot.

## 2.2 Storyteller-facing Is Not Synonymous with Secret

`storyteller_operational` and `storyteller_secret` are distinct and MUST remain distinguishable in metadata and editorial ownership.

Operational guidance MUST NOT become a secret repository merely because only the Storyteller reads it.

## 2.3 `dual_use` Is Obsolete

`dual_use` has no valid revelation meaning and is considered redundant.

The approved rule is:

- free circulation is sufficiently represented by `player_safe`;
- operational usefulness to both players and Storytellers is not a safety class;
- any content can be operationally useful to more than one audience without requiring a third access category.

### Retroactive removal requirement

All existing **uses and mentions** of `dual_use` in revelation/safety metadata, editorial instructions, DEU declarations, format examples and future production-facing documentation MUST be removed retroactively.

After migration, `dual_use` MUST NOT remain as an accepted safety value.

Where an existing artifact currently uses `dual_use`, it MUST be reclassified according to actual circulation safety:

- freely shareable → `player_safe`;
- not freely shareable → appropriate Storyteller-only classification.

This requirement is a downstream corrective dependency on format-governance maintenance even though this contract does not rewrite the existing format contract file itself.

---

# 3. Reader Access vs Character Knowledge

Reader access and character knowledge MUST always be evaluated separately.

A passage may be `player_safe` while its information is unavailable to a newly arrived character.

The player-facing product MUST NOT require hiding ordinary setting-reading material merely because a specific character lacks that knowledge.

Conversely, character access MUST NOT be inferred merely because the player has read the material.

---

# 4. Character Knowledge Model

The smallest authoritative controlled vocabulary is:

### `public`

Knowledge reasonably accessible through public mortal society, common observation, public records or ordinary social presence.

### `cainite_common`

Knowledge normally available to Cainites reasonably integrated into Novydres.

### `conditional`

Knowledge requiring an explicit fictional gate.

Possible gates include, without creating new global states:

- clan;
- faction;
- office;
- initiation;
- relationship;
- origin;
- Loresheet;
- investigation;
- domain experience;
- status;
- specific discovery.

`conditional` MUST carry or point to the relevant condition when that condition matters operationally.

### `unknown`

Knowledge that MUST NOT be presumed as starting character knowledge.

## 4.1 Internal Semantics vs Published Syntax

The codes `public`, `cainite_common`, `conditional` and `unknown` are primarily editorial metadata.

They MUST NOT be mechanically repeated as visible badges throughout publication.

Publication syntax follows this principle:

> **Classification is explicit in editorial data; reader-facing signaling appears only when required for interpretation.**

A section may establish a knowledge context once. Individual paragraphs do not need repetitive labels unless:

- knowledge becomes more restricted than the section baseline;
- the access condition matters in play;
- readers could otherwise infer incorrect character access;
- materially different groups receive different versions.

Natural-language publication is preferred where possible, for example:

- “Membros iniciados sabem que…”
- “Entre os Cainitas estabelecidos…”
- “Os registros públicos indicam…”
- “Recém-chegados dificilmente conheceriam…”

---

# 5. Truth / Knowledge States

The internal `truth_state` vocabulary is:

### `established`

The project has an authoritative objective resolution and treats the claim as true.

### `disputed`

Competing versions materially remain in tension at the relevant level, or no uncontested in-fiction version exists.

### `partial`

The claim contains material truth but is incomplete or meaningfully distorted by missing context.

### `false`

The project has an authoritative objective resolution and the claim does not correspond to it.

### `unresolved`

The project itself has not yet determined the objective answer.

## 5.1 Truth States Are Internal

Truth states exist for:

- governance;
- editorial audit;
- continuity;
- Storyteller resolution where appropriate;
- truth ownership.

They MUST NOT be displayed player-facing as reliability badges or truth certificates.

Player-facing presentation MUST NOT say, in metanarrative terms, that a claim is `true`, `false`, `partial` or `unresolved` merely because the internal metadata does.

This restriction protects:

- mystery;
- red herrings;
- propaganda;
- contradictory testimony;
- investigative play;
- narrative ambiguity.

## 5.2 Hidden Truth Is Not a Separate Truth State

A protected truth may simply be:

- `truth_state: established`
- `reader_access: storyteller_secret`

Reader access and truth status remain orthogonal.

---

# 6. Player-Safe Information

Player-facing setting lore SHOULD speak from within the world rather than from an omniscient external voice whenever certainty itself could affect play.

Authorial forms may include:

- records;
- tradition;
- common Cainite understanding;
- testimony;
- official explanation;
- received history;
- institutional doctrine;
- scholarly interpretation;
- rumor;
- local consensus.

Core principle:

> **Player-facing lore speaks from inside the world; it does not certify truth from outside it.**

A true statement and a red herring may therefore receive equally plausible player-facing treatment.

Operational facts necessary to use the setting MAY still be stated directly when doing so does not expose hidden truth or create a reliability signal that compromises intended uncertainty.

---

# 7. Information Form

`rumor` is an information form, not a truth state.

A rumor may internally be:

- `established`;
- `disputed`;
- `partial`;
- `false`;
- `unresolved`.

Other information forms may include, when useful:

- official account;
- public record;
- testimony;
- institutional teaching;
- propaganda;
- tradition;
- scholarly claim;
- eyewitness report.

The contract does not require a large fixed form taxonomy. Forms are used only when they change presentation or editorial behavior.

---

# 8. Rumor Architecture

Rumors may represent:

- true but unverified information;
- distortion;
- propaganda;
- incomplete truth;
- deliberate lie;
- contradictory versions;
- unresolved possibilities.

A player-facing rumor MUST NOT reveal its internal `truth_state`.

The existence, prominence or visual form of a rumor SHOULD NOT by itself tell players whether it is important, true or false.

Not every rumor requires an explicit Storyteller-facing answer in Chapter 13.

A rumor requires an authoritative objective home only when the project has actually resolved its objective status and that resolution must be maintained for continuity.

---

# 9. Disputed / Partial / False Information

## 9.1 `disputed`

Player-facing material may present multiple credible versions without selecting one as externally authoritative.

## 9.2 `partial`

The player-facing version may be accurate in what it says while omitting decisive context.

The omission MUST NOT be labeled to players as “partial truth”.

## 9.3 `false`

False in-fiction claims may be presented with full rhetorical and documentary credibility when appropriate.

The publication MUST NOT weaken a red herring merely because editorial metadata knows it is false.

## 9.4 `unresolved`

An unresolved item MUST remain genuinely unresolved at the project level.

Editors MUST NOT invent a hidden answer merely to complete a matrix.

---

# 10. Storyteller Operational Information

Storyteller operational material exists to help run the game.

It MAY include:

- preparation procedures;
- state tracking;
- pressure management;
- NPC activation guidance;
- scene-management advice;
- consequence handling;
- usage instructions.

It MUST NOT become the default storage location for hidden truth.

If operational guidance depends on a secret, it SHOULD reference the authoritative secret rather than silently reproducing the full resolution unless local operation requires a minimal restatement.

---

# 11. Storyteller Secret Information

`storyteller_secret` is reserved for:

- hidden objective resolutions;
- protected causal explanations;
- concealed identities or motives;
- secret structural relationships;
- hidden historical resolution;
- other revelations whose unrestricted player access would damage discovery.

Every secret that has an objective resolution MUST have one authoritative truth home.

---

# 12. Loresheet Revelation Role

Loresheets are legitimate progressive-revelation surfaces.

They MAY provide:

- privileged context;
- `conditional` character knowledge;
- less distorted versions;
- parts of a `partial` truth;
- confirmation of previously uncertain elements;
- clues that move a character closer to objective truth;
- progressive revelation across levels.

Higher levels MAY reveal a specific truth when explicitly designed to do so.

However:

> **A Loresheet is not the authoritative truth repository by default.**

If a Loresheet exposes a truth whose authoritative home exists elsewhere, its wording is derived from that source.

Loresheets MUST NOT create competing objective resolutions.

They MAY reference deeper Storyteller-only context when necessary.

This contract does not define Loresheet mechanics.

---

# 13. Chapter 13 Responsibility

The future **Segredos do Narrador** chapter is the default authoritative home for **global or structural setting secrets** whose objective resolution is not owned by a more specific artifact.

It MAY contain:

- objective resolution;
- hidden causal context;
- links back to player-facing claims;
- affected chapter/entity metadata;
- indexes of related claims;
- Storyteller consequences of a revelation.

It MUST NOT become:

- a dump of every rumor;
- a verification catalogue for every uncertain sentence;
- a replacement for adventure-specific secrets;
- a replacement for operational guidance.

The mere existence of a player-facing rumor does not require a dedicated Chapter 13 entry.

---

# 14. Authoritative Truth Ownership

Every objectively resolved hidden or uncertain claim MUST have **one and only one** authoritative `truth_home`.

Possible homes include:

- Chapter 13 for global setting secrets;
- an adventure for adventure-specific secrets;
- a thematic source for non-secret authoritative information;
- another explicitly designated artifact where scope requires it.

`appearance_locations` may be many.

`truth_home` may be one.

Derived surfaces MUST NOT silently become competing authorities.

If the project has not decided the answer, the truth state is `unresolved`; no artificial truth home is created.

---

# 15. Reference Marker Contract

Superscript markers are **local ordinal counters only**.

They are not semantic codes.

Valid behavior:

- first local reference → `¹`;
- second → `²`;
- third → `³`;
- fourth → `⁴`;
- and so on.

No number carries a fixed meaning.

Specifically:

- `²` does not mean player-permissible expansion;
- `³` does not mean Storyteller secret;
- no superscript number identifies a specific chapter or pipeline.

The destination semantics live in the reference record and target metadata, not in the printed ordinal.

## 15.1 Footnote Rendering

The publication-facing reference resolves in the footer using the conceptual form:

**`Capítulo: Título geral, página`**

Exact typography remains a downstream implementation concern.

## 15.2 Multiple References

Any number of references may exist as sequentially counted local superscripts.

Numbering may restart according to the publication unit/page rules chosen by the final production implementation; the number itself remains semantically empty.

---

# 16. Cross-Reference Rules

A cross-reference is mandatory when its absence could:

1. create false local authority;
2. hide a protected access boundary;
3. break an operational dependency;
4. prevent locating required deeper context;
5. leave a derived rule without its mechanical authority;
6. leave an isolated DEU without necessary deeper context;
7. disconnect a player-facing uncertain claim from a required authoritative resolution.

A cross-reference is optional when it provides only nonessential further reading.

Core rule:

> **Reference when omission could misrepresent ownership, safety or operation.**

## 16.1 Reference Text and Spoiler Safety

Reference labels and destination titles visible to players MUST themselves satisfy player-safe navigation rules.

A cross-reference MUST NOT reveal a hidden answer merely through its title.

## 16.2 Missing Destinations

A mandatory reference whose destination does not exist or cannot be resolved is a **publication-blocking validation error**.

If the destination is intentionally deferred, the source must carry explicit editorial unresolved/dependency metadata rather than a fake publication-ready reference.

## 16.3 Isolated DEUs

A detached or separately printed DEU MUST preserve enough reference information to locate deeper context without depending on the surrounding spread.

---

# 17. Duplication Rules

Novydres allows **minimal functional restatement**, not duplication of authority.

A derived surface MAY repeat information when necessary to operate independently, provided that the restatement:

- is smaller than the authoritative treatment;
- preserves the same semantics;
- adds no new objective resolution;
- does not become a competing source;
- references the authoritative home when ownership or deeper context matters.

Core rule:

> **Repeat enough context to operate; never enough authority to compete.**

Whole passages SHOULD NOT be duplicated merely to make a DEU, Loresheet or guidance surface exhaustive.

---

# 18. Progressive Revelation

Progressive revelation may move a character through increasingly privileged or accurate information without requiring every step to expose internal truth labels.

A valid progression may look conceptually like:

common version → privileged version → partial confirmation → deeper clue → objective resolution

The publication SHOULD avoid visual or metadata signals that tell players which step is “the real one”.

Progression may occur through:

- play;
- investigation;
- Loresheets;
- faction access;
- office;
- relationships;
- adventures;
- Storyteller revelation.

---

# 19. DEU Safety Mapping

## 19.1 Safety Classes

For revelation purposes:

### `player_safe`

The entire unit may circulate freely among players.

### Storyteller-only units

A unit not safe for free player circulation must be treated as Storyteller-only and its individual internal content may still distinguish:

- `storyteller_operational`;
- `storyteller_secret`.

## 19.2 Physical Envelope Rule

If a physical unit can be handed to or manipulated by players:

> **the whole physical unit belongs to the same player-safe spoiler envelope.**

Therefore:

- front player-safe + back secret is forbidden;
- a hidden reverse is not acceptable safety;
- a warning such as “do not turn over” is not sufficient;
- fold, reverse or adjacent handling MUST NOT expose protected answers.

Player-safe and secret companion units MUST be physically separable.

## 19.3 `dual_use` Removal

`dual_use` MUST be removed retroactively from DEU safety declarations and documentation.

Its former intended behavior is expressed through actual safety plus ordinary functional description.

---

# 20. Dramatis Personae Interface

Dramatis Personae remains authoritative for NPC presentation, identity, relations, statistics and its approved local information layers.

NPC profiles MUST follow the global revelation rules:

- player-facing identity/history must use player-safe epistemic presentation;
- rumors remain information forms, not truth labels;
- objective hidden answers do not live in player-facing profile text;
- hidden resolutions point to their authoritative truth home;
- knowledge gates use the Character Knowledge model;
- superscript references are ordinal only;
- profile navigation labels must not leak secret answers.

This contract does not redesign NPC layout or individual secrets.

---

# 21. Play Guidance Interface

Play Guidance remains an operational conversion layer.

Its player-facing surfaces MUST be `player_safe`.

Its Storyteller-facing surfaces may be `storyteller_operational`.

Play Guidance MUST NOT become the default repository of `storyteller_secret` information.

When an operational workflow depends on a secret, Play Guidance should reference the secret's authoritative home and restate only what is operationally necessary.

This preserves the established distinction:

**Storyteller-facing ≠ secret.**

---

# 22. Campaign / Adventure Interface

Future campaigns and adventures consume the global revelation architecture.

Adventure-specific secrets MAY live only in the adventure when they are not global setting truths.

A global setting truth used by an adventure remains owned by its global `truth_home`.

An adventure MAY reference Chapter 13 or another authoritative source rather than duplicating the full resolution.

Adventure handouts MUST be `player_safe`.

Adventure navigation, handout names, indexes and reference labels MUST NOT expose secret answers.

An adventure MAY progressively reveal global truths but MUST NOT create a contradictory authoritative version unless it explicitly changes canon through an authorized project decision.

---

# 23. Digital Navigation Safety

Navigation metadata is content for spoiler-safety purposes.

The spoiler envelope includes:

- table of contents;
- PDF bookmarks;
- index entries;
- page titles;
- section titles;
- cross-reference labels;
- link text;
- exported page/deck names where user-visible;
- search-visible headings and labels.

A protected answer MUST NOT be leaked through navigation metadata.

Use neutral topic identification rather than answer-bearing titles.

For example, prefer a title conceptually equivalent to:

**“O assassinato do Regente”**

over:

**“Quem realmente assassinou o Regente: X”**

when the identity itself is protected.

This contract defines the requirement, not the technical PDF pipeline.

---

# 24. Publication Validation Rules

A publication audit MUST verify at minimum:

1. Every information item has a valid Reader Access classification when safety is nontrivial.
2. Reader Access is not conflated with Character Knowledge.
3. `conditional` knowledge identifies or references its gate where operationally necessary.
4. Player-facing content does not visibly expose internal truth-state labels.
5. Player-facing lore does not accidentally certify hidden truth through omniscient wording where uncertainty matters.
6. Every objectively resolved hidden/uncertain claim has one authoritative `truth_home`.
7. No claim has competing authoritative resolutions.
8. `unresolved` claims are not silently resolved in derived surfaces.
9. Rumors are not treated as inherently false or uncertain.
10. Loresheets do not become accidental competing truth repositories.
11. Storyteller operational guidance is not misclassified as secret merely because it is Storyteller-facing.
12. No player-safe physical unit contains protected hidden truth on another face, fold or easily exposed region.
13. All `dual_use` uses and mentions are removed from active project metadata/documentation after migration.
14. Every mandatory cross-reference has a valid destination.
15. Superscript ordinal numbers carry no semantic meaning.
16. Footnote destinations remain understandable on isolated DEUs.
17. Derived restatements do not create local competing authority.
18. Player-visible navigation metadata does not expose secret answers.
19. Adventure-specific secrets do not overwrite global truth ownership.
20. Every player-facing uncertain claim is framed sufficiently for the intended in-fiction interpretation.

Any violation of rules 4, 6, 7, 12, 13, 14 or 18 is publication-blocking.

---

# 25. Information Placement Decision Procedure

For every future information item, editors SHOULD apply this sequence:

1. **May players safely read it?**
   - yes → `player_safe`;
   - no, operational only → `storyteller_operational`;
   - no, protected revelation → `storyteller_secret`.

2. **What may characters know?**
   - `public`;
   - `cainite_common`;
   - `conditional`;
   - `unknown`.

3. **What does the project know objectively?**
   - `established`;
   - `disputed`;
   - `partial`;
   - `false`;
   - `unresolved`.

4. **How does the information circulate?**
   - direct operational statement;
   - record;
   - rumor;
   - testimony;
   - doctrine;
   - propaganda;
   - other appropriate in-fiction form.

5. **Where does objective authority live?**
   - assign one `truth_home` when resolved;
   - leave unresolved when genuinely undecided.

6. **Is this location authoritative or derived?**
   - authoritative → full responsibility allowed;
   - derived → minimal functional restatement only.

7. **Is a cross-reference mandatory?**
   - yes when ownership, safety or operation would otherwise be obscured.

8. **Can the physical/digital surface leak the answer?**
   - validate front/back, detached use, titles, bookmarks, index and labels.

---

# 26. Dependencies

This contract depends on:

- editorial governance for final authority and audit;
- Play Guidance for the established player-safe vs Storyteller-operational distinction;
- format governance for DEU physical behavior and for retroactive removal of `dual_use`;
- Dramatis Personae for NPC-specific implementation;
- future Chapter 13 for structural Storyteller secrets;
- future Loresheet work for progressive reveal implementation;
- future campaign/adventure contracts for local secret ownership;
- future PDF pipeline for technical navigation-safety enforcement.

---

# 27. Deferred Questions

The following remain intentionally outside GAP-ARCH-003:

- actual Chapter 13 content;
- actual hidden answers;
- specific rumor truth resolutions;
- individual NPC secrets;
- exact Loresheet mechanics;
- final player/ST product packaging strategy;
- exact PDF implementation;
- exact parser schema syntax;
- exact frontmatter field names beyond conceptual requirements;
- exact typography/icons for knowledge signaling;
- final footnote typography;
- adventure format;
- campaign plots;
- automated validation implementation.

The removal of `dual_use` from existing project artifacts is **not** deferred as a design question; only the mechanical migration work is downstream.

---

# 28. Approved Decisions

- **RA-001** — Three Reader Access classes: `player_safe`, `storyteller_operational`, `storyteller_secret`.
- **RA-002** — Character Knowledge uses `public`, `cainite_common`, `conditional`, `unknown`.
- **RA-003** — Knowledge-state codes are internal metadata; publication uses contextual natural-language signaling by default.
- **RA-004** — Truth states use `established`, `disputed`, `partial`, `false`, `unresolved`, and are opaque to players.
- **RA-005** — Player-facing lore uses an epistemically situated in-fiction voice rather than external truth certification.
- **RA-006** — Every resolved claim has one authoritative `truth_home`; Chapter 13 is not the mandatory home of every rumor.
- **RA-007** — Loresheets support progressive revelation but are not authoritative truth homes by default.
- **RA-008** — Superscript references are ordinal counters only; no fixed meaning is attached to `²`, `³` or any other number.
- **RA-009** — Cross-references are mandatory when needed to preserve ownership, safety or operation.
- **RA-010** — Minimal functional restatement is allowed; competing duplication of authority is forbidden.
- **RA-011** — `dual_use` is redundant and must be retroactively removed from project use and mention; physical player-safe envelopes remain indivisible.
- **RA-012** — Navigation metadata is inside the spoiler-safety envelope.

---

# 29. Rejected Alternatives

The architecture rejects:

- merging Reader Access and Character Knowledge;
- a large badge-heavy publication taxonomy;
- showing players internal truth-state labels;
- treating rumor as synonymous with falsehood;
- using visual certainty labels that reveal red herrings;
- requiring every rumor to have a Chapter 13 entry;
- using Loresheets as default secret repositories;
- encoding revelation semantics in superscript reference numbers;
- exhaustive cross-referencing of every optional dependency;
- unrestricted duplication across surfaces;
- placing player-safe content on one side and protected secrets on the reverse;
- retaining `dual_use` as an active safety class;
- allowing bookmarks, indexes or titles to reveal secret answers.

---

# 30. Risks

## 30.1 Over-signaling

Too many visible labels can turn metadata into a player-facing truth detector.

**Mitigation:** codes remain internal; publication signaling is contextual.

## 30.2 Red-herring collapse

If true and false claims are visually distinguished, false leads lose narrative weight.

**Mitigation:** internal truth states are not exposed player-facing.

## 30.3 Authority drift

Repeated summaries may gradually contradict the authoritative source.

**Mitigation:** single `truth_home` plus minimal functional restatement.

## 30.4 Secret leakage through format

Reverse pages, bookmarks or index entries may expose answers.

**Mitigation:** physical and digital spoiler envelopes.

## 30.5 Chapter 13 inflation

A requirement to resolve every rumor centrally could turn Chapter 13 into an unwieldy catalogue.

**Mitigation:** contextual truth ownership.

## 30.6 Legacy `dual_use`

Existing files may retain a now-rejected category.

**Mitigation:** mandatory retroactive migration and publication validation failure until removed.

---

# 31. Closure Assessment

GAP-ARCH-003 is architecturally saturated at candidate level.

Under this contract, another editor can determine for any future information item:

- who may read it;
- what characters may know;
- what truth state it has internally;
- how player-facing certainty must be handled;
- where objective authority lives;
- whether repetition is allowed;
- whether a cross-reference is required;
- how it may safely appear in a DEU;
- whether navigation creates a spoiler;
- where objective truth must ultimately be resolved.

No further substantive grill is required for this gap at candidate stage.

This document does **not** mark GAP-ARCH-003 as resolved. Final judgment remains with the main editorial chat.