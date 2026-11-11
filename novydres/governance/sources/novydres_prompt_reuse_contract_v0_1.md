---
document_id: novydres_prompt_reuse_contract
version: 0.1
status: active
date: 2026-08-06
scope: prompt_documentary_reuse
depends_on:
  - novydres_editorial_governance_v1_0.md
  - skill_grill_me_v1_1.md
  - skill_caveman_v1_0.md
---

# Novydres — Prompt Reuse Contract v0.1

## 1. Purpose

Define mandatory documentary-reuse rules for every prompt created inside the Novydres project.

Prompts must orchestrate work.

Prompts must not duplicate project memory.

Versioned files remain canonical memory.

---

# 2. Fundamental Rule

**Never restate in a prompt information that already exists in canonical documentary memory.**

If a fact, rule, decision, taxonomy, workflow, constraint, list, mechanic, chronology, faction state, chapter ownership rule, or editorial guardrail already exists in a versioned project file:

the prompt MUST reference that file instead of reproducing the information.

The prompt must state:

1. **which file contains the authority**;
2. **where inside that file the information can be found**;
3. **what the agent must do with that information**.

---

# 3. Required Reference Form

Preferred pattern:

> Read `filename.ext`, section `X — Section Name`. Treat that section as authoritative for [subject].

If section numbering is unavailable:

> Read `filename.ext`, heading `Heading Name`.

If the source is structured JSON:

> Read `filename.json`, object/path `path.to.field`.

If exact heading/path cannot be guaranteed:

> Search `filename.ext` for the canonical term `Exact Term` and use the latest authoritative occurrence.

Prompts must favor precise documentary pointers over copied prose.

---

# 4. What Must Be Referenced, Not Rewritten

Do not duplicate existing documentary memory for:

- canon decisions;
- lore decisions;
- chronology;
- faction definitions;
- political relationships;
- rules mechanics;
- Status rules;
- Prestation rules;
- laws;
- office structures;
- Revelation Architecture;
- Format Contract rules;
- Play Guidance architecture;
- Standalone Rules architecture;
- Editorial Prohibitions;
- Gap Registry status;
- migration sequence;
- DEU rules;
- NPC profile architecture;
- skill behavior;
- grill rules;
- caveman rules;
- versioning rules;
- source-precedence rules;
- previously approved terminology;
- known POI inventories;
- raion inventories;
- chapter ownership boundaries.

If documented, point to source.

Do not paraphrase as substitute for source.

---

# 5. Prompt Content That May Be Written Directly

A prompt MAY contain:

- task-specific objective;
- active gap ID;
- allowed scope;
- prohibited scope;
- expected deliverables;
- exact filenames to create;
- stop condition;
- task-specific validation checklist;
- instructions needed only for this task and not already canonical elsewhere;
- documentary pointers;
- conflict-resolution procedure when source files disagree;
- temporary execution details not worthy of canonical memory.

If a task-specific instruction becomes reusable across future prompts, it SHOULD become its own versioned contract/skill instead of being repeatedly copied.

---

# 6. No Memory Forks

Duplicating canonical rules inside prompts creates memory forks.

Forbidden pattern:

- canonical contract says X;
- prompt copies X in prose;
- later contract changes to Y;
- old prompt still contains X.

Therefore:

**prompt copies are non-authoritative and must be avoided.**

A prompt should depend on canonical files, not mirror them.

---

# 7. Version-Aware References

Prompts SHOULD reference semantic document families when future versions may supersede current ones.

Example:

> Locate latest active `novydres_revelation_architecture_contract_*` and read section `Reader Access`.

When exact version is required for reproducibility:

> Use `novydres_revelation_architecture_contract_v0_1.md`, section `Reader Access`.

Choose based on task:

- reproducible historical migration: exact version;
- ongoing editorial behavior: latest active version.

---

# 8. Mandatory Prompt Bootstrap

Every project prompt must begin by directing agent to retrieve documentary memory before acting.

Minimum bootstrap:

1. locate files listed in `depends_on`;
2. verify latest/required versions;
3. read referenced sections;
4. build task context from files;
5. only then execute;
6. never ask user for information contained there.

---

# 9. Section-Level Precision

Do not say only:

> Read Chapter 05.

When the prompt needs one rule.

Say:

> Read `05_concilio_leis_status_prestacoes_v0_2_1.md`, section `Status Posicional`, and subsection governing shared/contested regency.

Precision reduces:

- token use;
- context drift;
- hallucination;
- accidental reliance on unrelated passages.

---

# 10. Discovery When Location Unknown

If prompt author knows the file but not exact section:

do not invent section number.

Use search instruction:

> Search `filename.md` for `exact canonical term`.

Example:

> Search `05_concilio_leis_status_prestacoes_v0_2_1.md` for `Príncipe Regente` and inspect all occurrences governing shared office authority.

Never fabricate headings, line numbers, JSON paths, or sections.

---

# 11. Cross-Document Decisions

When a rule is reconstructed from multiple files:

the prompt must cite all required sources and assign each role.

Example pattern:

> For current Sulfok state:
> - use `03_atlas...`, heading `Sulfok`, for spatial/jurisdiction authority;
> - use `04_faccoes...`, heading `Sulfok`, for present political pressure;
> - if conflict exists, apply source-precedence rules from `novydres_editorial_governance...`.

Do not merge these into a copied synthetic summary inside the prompt.

---

# 12. Skills

Skills are documentary memory.

Prompts must reference them instead of embedding their full text.

Examples:

- `skill_grill_me_*`
- `skill_caveman_*`

Only embed a skill when the prompt must operate outside access to project files.

If embedded for portability, clearly mark it as fallback, not canonical source.

---

# 13. Contracts

Global editorial rules must live in contracts.

A prompt that needs:

- Revelation rules;
- publication-language prohibitions;
- format rules;
- standalone rules;
- prompt-reuse rules;

must point to the respective contract.

Do not recopy contract contents.

---

# 14. Reports and Reviews

Prompts may use migration reports/reviews for:

- known defects;
- closure history;
- rationale.

But primary artifacts remain authoritative for actual content.

Prompt must never instruct agent to infer chapter contents from a report alone.

---

# 15. User Questions

Before asking user:

1. inspect documentary pointers in prompt;
2. search referenced files;
3. inspect related current artifacts;
4. apply `skill_grill_me_*`.

Question is forbidden if answer exists in documentary memory.

---

# 16. Prompt Review Test

Before finalizing any prompt, Editor must check:

### Duplication test
Did prompt restate a rule already documented?

If yes: replace copied text with file + location pointer.

### Fork test
Could copied prose become stale if source file changes?

If yes: remove copied prose.

### Precision test
Does each documentary dependency say where relevant information lives?

If no: add heading/path/search term.

### Sufficiency test
Could agent execute task by retrieving referenced files?

If no: add only missing task-specific instruction.

### Canon test
Is any prompt summary being treated as more authoritative than source file?

If yes: fix.

---

# 17. Exception — Minimal Guardrail Repetition

A prompt MAY repeat a tiny safety/stop condition when omission could cause irreversible or broad scope error.

Examples:

- “Do not start Chapter 06.”
- “Do not modify lore.”
- “Stop after producing listed artifacts.”

Even then, canonical details should remain referenced rather than recopied.

---

# 18. Exception — External / Detached Execution

If another agent will not have access to project memory files:

a self-contained prompt may embed required information.

It must explicitly say:

- embedded text is a snapshot;
- canonical source is named;
- snapshot date/version;
- canonical file wins if later available.

Within normal Novydres workflow, this exception should be rare.

---

# 19. Required Behavior of Senior Editor

When creating any future prompt, Senior Editor MUST:

1. identify reusable knowledge already documented;
2. avoid copying it;
3. point to exact file;
4. point to section/heading/path/search term;
5. describe only task-specific action;
6. create new canonical document when reusable rule does not yet exist;
7. version that new document;
8. make prompt depend on it.

---

# 20. Final Law

**Prompt = orchestration.**

**Files = memory.**

**Contracts = reusable rules.**

**Skills = reusable behavior.**

**Reviews = judgments.**

**Reports = evidence.**

**Primary artifacts = content authority.**

Never turn prompt into second copy of project memory.