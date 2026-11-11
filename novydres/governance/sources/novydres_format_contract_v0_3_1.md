---
document_id: novydres_format_contract
version: 0.3.1
status: active
date: 2026-08-05
scope: clerical_patch_revelation_safety_migration
supersedes: novydres_format_contract_v0_3.md
depends_on:
  - novydres_editorial_governance_v1_0.md
  - skill_grill_me_v1_1.md
  - novydres_format_contract_v0_3.md
  - novydres_format_contract_v0_3_editorial_review_v0_1.md
  - novydres_revelation_architecture_contract_v0_1.md
  - novydres_revelation_architecture_editorial_review_v0_1.md
---

# Novydres — Format Contract v0.3.1 Clerical Patch

## 1. Authority

This document supersedes `novydres_format_contract_v0_3.md` for active use.

All normative content of v0.3 is incorporated by reference and remains unchanged **except for the three clerical corrections explicitly listed below**.

This patch introduces no new design decision.

## 2. Corrections

### C-01 — Active grill skill dependency

In the v0.3 frontmatter, replace:

`skill_grill_me_v1_0.md`

with:

`skill_grill_me_v1_1.md`

### C-02 — Section 5 version wording

Replace:

> These values MAY be used in v0.2 implementations and prototypes.

with:

> These values MAY be used in v0.3 implementations and prototypes.

No numerical value, margin rule or production status changes.

### C-03 — Section 23 version wording

Replace:

> Its layout, tiling, imposition, cropping or reflow behavior is outside v0.2.

with:

> Its layout, tiling, imposition, cropping or reflow behavior is outside v0.3.

No home-print policy changes.

## 3. Explicitly Unchanged

The patch does not modify:

- 250 × 250 mm trim;
- margins or live area;
- 12-column grid;
- gutter;
- 4.5 mm macro vertical rhythm;
- typography ranges;
- spacing tokens;
- image rules;
- container/border rules;
- DEU geometry;
- duplex semantics;
- Reader Access classifications;
- RA-008 ordinal-reference semantics;
- RA-011 removal of `dual_use`;
- RA-012 digital spoiler envelope;
- Raion, NPC or Rules Reference DEU rules;
- density guidance;
- home-print derivative policy;
- unresolved production values;
- production gates before v1.0.

## 4. Validation

For active interpretation, read:

`novydres_format_contract_v0_3.md`

with C-01 through C-03 replaced by this patch.

No other v0.3 wording is superseded.

## 5. Change History

### v0.3.1

- corrected obsolete grill-skill dependency;
- corrected two stale self-version references;
- made no substantive format or revelation-safety changes.