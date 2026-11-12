---
document_id: novydres_editorial_prohibitions_contract
version: 0.1
status: active
date: 2026-08-05
scope: global_editorial_negative_rules
supersedes: null
depends_on:
  - novydres_editorial_governance_v1_0.md
  - novydres_format_contract_v0_3_1.md
  - novydres_revelation_architecture_contract_v0_1.md
  - novydres_play_guidance_contract_v0_1.md
  - novydres_standalone_rules_contract_v0_1.md
---

# Novydres — Editorial Prohibitions Contract v0.1

## 1. Purpose

This contract defines **what the Editor must explicitly reject** in any future Novydres artifact.

It exists to prevent technically correct internal-production concepts from leaking into published-facing prose.

This contract is global.

It applies to:

- chapters;
- NPC profiles;
- DEUs;
- appendices;
- rules text;
- player-facing text;
- Storyteller-facing text;
- handouts;
- captions;
- sidebars;
- navigation text;
- migration work;
- sub-agent outputs.

## 2. Fundamental Separation

Novydres has two distinct language layers:

### A. Production language

Internal language used by editors, agents, parsers and governance systems.

Examples:

- `player_safe`
- `storyteller_operational`
- `storyteller_secret`
- `Reader Access`
- `Character Knowledge`
- `Truth State`
- `truth_home`
- `DEU`
- `dual_use` historical references
- `resolution_mode`
- `gap_id`
- `closure_evidence`
- `ownership`
- `derived surface`
- `information contract`
- `source authority`
- `migration`
- `renderability`
- `parser`
- `frontmatter`
- `metadata`

These terms MAY appear in:

- frontmatter;
- JSON;
- schemas;
- editorial reviews;
- migration reports;
- design contracts;
- parser configuration;
- comments intended only for production.

They MUST NOT appear as part of normal supplement prose unless the term is itself genuinely part of the fictional or rules-facing vocabulary.

### B. Publication language

Language actually read by players and/or Storytellers as part of the book.

It must sound like:

- a Vampire: The Masquerade sourcebook;
- a city chronicle supplement;
- rules prose;
- setting prose;
- Storyteller guidance;
- in-world or editorially polished reference text.

It MUST NOT expose internal production architecture.

## 3. Mandatory Editorial Rejection — Production Jargon in Published Prose

The Editor MUST reject any artifact where reader-facing prose contains production jargon such as:

- “player-safe”;
- “Storyteller-only” as metadata-style labeling inside prose;
- “DEU”;
- “detachable editorial unit”;
- “truth home”;
- “Reader Access”;
- “Character Knowledge”;
- “Truth State”;
- “information ownership”;
- “derived surface”;
- “source of truth”;
- “canonical source field”;
- “migration-compliant”;
- “format-contract compliant”;
- “parser-safe”;
- “renderability-safe”;
- “this content belongs to another layer”;
- “this chapter owns X”;
- “this section is operational rather than lore-facing”.

These are editorial concepts, not reader-facing prose.

The underlying distinction may be implemented silently through structure, tone, placement and metadata.

## 4. Mandatory Editorial Rejection — Explaining the Book's Internal Architecture to the Reader

The Editor MUST reject prose that explains internal production design instead of simply presenting the book naturally.

Bad examples:

- “This section is player-safe.”
- “This entry is a DEU.”
- “This chapter is the authoritative truth home for this information.”
- “The following content is derived from Chapter 04.”
- “This page is designed to work as a detachable editorial unit.”
- “The Atlas owns spatial information while Chapter 04 owns political operation.”
- “This section uses the Revelation Architecture.”

These concepts may be true internally.

They MUST be invisible to the reader.

## 5. Acceptable Reader-Facing Equivalents

Internal concepts should be translated into natural publication language.

Examples:

Internal:
`player_safe`

Published:
No label is necessary in most cases.

Internal:
`storyteller_secret`

Published:
“Segredos do Narrador” or another natural section title, where appropriate.

Internal:
`DEU`

Published:
No technical label. The page simply functions independently.

Internal:
`truth_home`

Published:
No reader-facing equivalent is normally needed.

Internal:
`Character Knowledge: conditional`

Published:
“If your character belongs to...”, “Cainitas ligados à Ordem sabem...”, or other natural contextual prose when such signaling is needed.

Internal:
`uncertain / disputed truth state`

Published:
“Alguns afirmam...”, “A versão aceita entre...”, “Há quem sustente...”, “Ninguém concorda sobre...”.

## 6. Mandatory Editorial Rejection — Workflow Instructions Disguised as Setting Prose

The Editor MUST reject passages in setting chapters that read like internal workflow instructions.

Examples:

- “Use este raion as a player-safe reference.”
- “This material feeds the Play Guidance workflow.”
- “This content may later become a DEU.”
- “The Storyteller should consult the authoritative source.”
- “Cross-reference this information with Chapter 04 because it owns the operational layer.”

If actual Storyteller guidance is required, it must be written as genuine guidance for play, not production guidance.

## 7. Mandatory Editorial Rejection — Redundant Metatext

The Editor MUST reject metatext that merely explains obvious document behavior.

Examples:

- “This chapter presents the districts of the city.”
- “The following entries contain information about each raion.”
- “Use the references below to find more information in other chapters.”
- “This section is intended as a quick reference.”

Such text is allowed only when it materially improves orientation and is written naturally.

The default is to show structure through headings and composition rather than explain it.

## 8. Mandatory Editorial Rejection — Contract Language in Narrative Copy

Words like:

- MUST
- SHOULD
- MAY
- authoritative
- normative
- supersedes
- dependency
- validation
- closure
- artifact
- migration

MUST NOT appear in narrative setting prose merely because they exist in internal contracts.

They remain appropriate in:

- actual game rules;
- legalistic in-world text where fictionally justified;
- production documents.

## 9. Mandatory Editorial Rejection — Exposing Hidden Classification

The Editor MUST reject any published prose that accidentally tells the reader how the project internally classifies truth.

Bad:

- “This rumor is false.”
- “This is a partial truth.”
- “This claim is unresolved in the project.”
- “The true answer appears in Chapter 13.”

unless the artifact is explicitly Storyteller-facing and revealing that answer is its intended purpose.

Player-facing uncertainty must be conveyed through in-world epistemic language, not metadata labels.

## 10. Mandatory Editorial Rejection — Reader-Facing Implementation Notes

The following must never appear in finished supplement prose:

- placeholder asset instructions;
- parser instructions;
- page-side instructions;
- layout notes;
- Tailwind/HTML instructions;
- TODOs;
- “future chapter” implementation notes;
- unresolved internal questions;
- production statuses;
- version references;
- filenames.

They belong only to production metadata or audit documents.

## 11. Mandatory Editorial Rejection — Artificial Symmetry

The Editor MUST reject content added only to make sections structurally symmetrical.

Examples:

- inventing details so every raion has the same number of bullets;
- creating extra POIs to balance columns;
- inventing rumors because another entry has rumors;
- expanding minor NPCs only to match a template.

Content density follows relevance, not template symmetry.

## 12. Mandatory Editorial Rejection — Premature Closure

The Editor MUST reject any artifact that presents an unresolved or deferred design question as if it were settled.

Examples:

- final Storyteller secrets before base lore is stable;
- final campaign truths before principal NPCs are complete;
- exact page count before content architecture is stable;
- final DEU contract when only the general DEU architecture is approved.

## 13. Mandatory Editorial Rejection — Silent Lore Changes During Migration

Migration work MUST NOT silently rewrite lore.

The Editor must reject:

- untraceable date changes;
- renamed institutions without documentary authority;
- altered motivations;
- changed relationships;
- new secrets;
- new political outcomes;
- changes in jurisdiction;
- changed POI meaning;

unless supported by later authoritative memory or a new explicit decision.

## 14. Mandatory Editorial Rejection — Reports Substituting for Primary Artifacts

The Editor MUST NOT approve a migration because its report claims success.

Approval requires direct inspection of the primary artifact.

For every migrated chapter, the Editor MUST verify:

1. the complete body exists;
2. the body is readable in ordinary Markdown;
3. all major expected sections are physically present;
4. the report matches the artifact;
5. no internal-production language leaked into publication prose.

## 15. Mandatory Editorial Rejection — Renderer-Dependent Body Content

Human-readable supplement prose MUST NOT depend on:

- custom Markdown containers;
- proprietary directives;
- renderer-specific syntax;

in a way that makes the body disappear in a basic Markdown viewer.

Metadata may be parser-specific.

Body prose may not be.

## 16. Storyteller Guidance Exception

Storyteller-facing prose may explicitly instruct the Storyteller how to run material.

Acceptable examples:

- “Use Zara to increase pressure when...”
- “If the coterie refuses the offer...”
- “Keep the identity of the informant hidden until...”

This is **game-facing operation**, not production-facing operation.

The Editor must distinguish the two.

## 17. Rules Exception

Mechanical terminology belongs in rules text when it is part of the actual game.

Examples:

- Hunger;
- Blood Potency;
- Status;
- Rouse Check;
- Willpower;
- Difficulty.

Internal editorial terminology does not become acceptable merely because the book contains rules.

## 18. Required Editorial Test for Every Publication Artifact

Before approving any chapter/page/profile, the Editor must ask:

### Reader test
Could a player or Storyteller encounter an internal project-management term here?

If yes: reject and rewrite.

### Fiction/rules test
Does every visible term belong to:
- the fictional world;
- the actual game rules;
- normal book-navigation language?

If no: reject.

### Invisible architecture test
Could the same function be achieved through:
- placement;
- metadata;
- heading;
- tone;
- cross-reference;
- section separation;

without explaining the internal architecture?

If yes: remove the explanatory metatext.

## 19. Editorial Severity

Violations are classified as:

### BLOCKING
Publication-facing production jargon, hidden-truth leakage, renderer-hidden body, silent lore change.

### MAJOR
Excessive metatext, workflow language in setting prose, internal architecture explained to the reader.

### MINOR
Redundant orientation prose, awkward implementation-derived wording.

BLOCKING and MAJOR issues prevent editorial approval.

## 20. Authority

This contract is a global negative guard-rail.

Future sub-agent prompts for chapter migration/revalidation MUST include it in `depends_on`.

Future editorial reviews MUST explicitly check compliance.

Where an older artifact was approved before this contract but violates it, that artifact must be revalidated when its workstream is next touched or immediately if the violation materially affects reader-facing quality.