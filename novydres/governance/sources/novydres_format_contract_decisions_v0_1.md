---
document_id: novydres_format_contract_decisions
version: 0.1
status: candidate
date: 2026-08-04
scope: format_contract_grill_decisions
supersedes: null
depends_on:
  - novydres_format_contract_v0_1.md
  - skill_grill_me_v1_0.md
---

# Novydres — Format Contract Decision Log v0.1

## D-01 — Meaning of Detachable

**Decision:** Use editorial detachability, not physical tear-out pages.

**Rationale:** Selected pages must work independently without compromising the premium bound-book experience.

**Alternative rejected:** Perforated/physically removable pages or a removable section.

**Consequence:** Detachability is an information-architecture property.

**Source question:** Grill Q1.

---

## D-02 — Visual Identity of Detachable Units

**Decision:** DEUs must remain atmospheric RPG-book pages and must not resemble cards, dashboards, or wiki panels.

**Rationale:** A strongly modular UI language would damage the intended *Vampire* atmosphere.

**Alternative rejected:** Literal card/tile system.

**Consequence:** Use typography, spacing and alignment before containers.

**Source question:** User clarification after Q1.

---

## D-03 — Default Extent

**Decision:** Single page is the default; two-page units require justification.

**Rationale:** Single pages are ideal for independent consultation while two pages remain valuable for conceptually complete dossiers.

**Alternative rejected:** Equal unrestricted status for pages/spreads; single-page-only restriction.

**Consequence:** “Single-page first, duplex by justification.”

**Source question:** Grill Q2.

---

## D-04 — Duplex Dossier

**Decision:** A two-page main NPC spread should also function as front/back of one independently printed sheet.

**Rationale:** Main dossiers are naturally complete as a two-sided operational object.

**Alternative rejected:** Treating the two pages as unrelated detachable pages.

**Consequence:** Stable identity across both sides and no critical gutter dependency.

**Source question:** User clarification after Q2.

---

## D-05 — Duplex Semantics

**Decision:** Front = understand/inhabit; back = operate/reference.

**Rationale:** Separates atmosphere and identity from table operation without imposing a rigid geometric template.

**Alternative rejected:** Fully self-contained duplicate sides; no semantic relationship.

**Consequence:** Applies as a default principle to justified duplex DEUs.

**Source question:** Grill Q3.

---

## D-06 — Home Printing

**Decision:** Remove A4/Letter home-print compatibility as a requirement.

**Rationale:** The master format should not compromise readability or square-format composition to fit domestic paper.

**Alternative rejected:** A4-derived master size or automatic reduction.

**Consequence:** 250 × 250 mm remains the master. Any home-print edition is a future derived product.

**Source question:** Grill Q4.

---

## D-07 — Binding Reference

**Decision:** Design for sewn hardcover as the reference edition.

**Rationale:** Better supports premium production, durable consultation and spread use.

**Alternative rejected:** Perfect binding as the master constraint; binding-neutral conservative layout.

**Consequence:** Larger inner margin remains, but spreads can be used more confidently.

**Source question:** Grill Q5.

---

## D-08 — Selective Detachability

**Decision:** Pages must earn DEU status through meaningful table utility.

**Rationale:** Universal self-containment would turn the book into a manual/dashboard and weaken sequential reading.

**Alternative rejected:** Every page detachable; only a tiny appendix class detachable.

**Consequence:** Chapter openings, continuous history and atmospheric transitions may remain normal pages.

**Source question:** Grill Q6.

---

## D-09 — Visible DEU Marker

**Decision:** Use a small glyph in the footer.

**Rationale:** Makes detachable pages discoverable without creating a strong UI badge.

**Alternative rejected:** No visible marker; large labels/ribbons.

**Consequence:** Final glyph design is deferred.

**Source question:** Grill Q7.

---

## D-10 — Safety Classification

**Decision:** Player-safe and Storyteller-only content may not coexist on the same physical DEU.

**Rationale:** A detachable page can circulate at the table; hidden boxes or secret reverse sides create disclosure risk.

**Alternative rejected:** Marked ST boxes; player front/ST reverse.

**Consequence:** Safety applies to the whole unit.

**Source question:** Grill Q8.

---

## D-11 — Existing Storyteller Secrets Architecture

**Decision:** Use existing Storyteller Secret pages as the hidden-information counterpart to public DEUs.

**Rationale:** The project already has a secret-reference architecture; a new overlay system would duplicate it.

**Alternative rejected:** New 1:1 Storyteller Overlay system.

**Consequence:** Public-to-secret mapping may be many-to-many, and secret pages must independently earn DEU status.

**Source question:** Grill Q9 plus user clarification.

---

## D-12 — Type-specific Information Contracts

**Decision:** Each DEU family will use mandatory core + optional modules, but exact fields are deferred to its own contract.

**Rationale:** This preserves consistency without prematurely forcing wiki-like identical field sets.

**Alternative rejected:** Fixed universal fields; completely unconstrained content.

**Consequence:** v0.1 defines taxonomy and principles only.

**Source question:** Grill Q10 plus user clarification.

---

## D-13 — Raion Map Requirement

**Decision:** A map is fundamental to the future Raion DEU contract.

**Rationale:** Spatial orientation is essential to a district reference.

**Alternative rejected:** Treating the map as merely optional.

**Consequence:** Exact map size, fields and supporting modules are deferred to the Raion-specific design task.

**Source question:** User clarification after Q10.

---

## D-14 — Grid Architecture

**Decision:** Use one universal invisible base grid with derived editorial modes.

**Rationale:** Preserves cross-book consistency while allowing prose, maps, dossiers and rules to behave differently.

**Alternative rejected:** One rigid layout for all pages; independent chapter grids.

**Consequence:** Grid is structural, not visually exposed.

**Source question:** Grill Q11.

---

## D-15 — Overflow Policy

**Decision:** Resolve density editorially before typographically.

**Rationale:** Readability and table utility take priority over forcing arbitrary content into a nominal page extent.

**Alternative rejected:** Shrink typography to preserve page count; unrestricted local decisions.

**Consequence:** Remove redundancy, simplify optional modules, recompose, then promote to duplex before reducing type below contract ranges.

**Source question:** Grill Q12.

---

# Deferred Questions

- final DEU field contracts;
- final fonts;
- final glyph;
- final color/ornament system;
- exact Raion layout beyond the map requirement;
- exact NPC/faction/law/location/institution/antagonist/phenomenon/Loresheet contracts;
- whole-book pagination;
- final printer/paper specifications;
- derived A4/Letter edition;
- final parser and Tailwind schema.

# Implementation Consequences

- existing A4-era page-count constraints require migration review;
- existing fixed card-grid instructions must not automatically become the 250 × 250 visual grammar;
- Storyteller-safe separation must be represented in source metadata;
- duplex units need front/back semantic metadata;
- prototypes should precede whole-book repagination.

# Recommended Next Step

Return both candidate files to the main editorial chat for judgment. If accepted as the basis for v0.2, prototype exactly three content families: one Raion, one main NPC duplex dossier, and one Chapter 05 rules reference.