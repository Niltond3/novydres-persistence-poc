# NOVYDRES — Immediate migration recovery handoff

Classification: MIGRATION_IN_PROGRESS. Last valid commit should be read from master HEAD at resume; no cutover.
Start reads in order: novydres/MANIFEST.json; novydres/.AGENT.md; novydres/.CONTEXTG.md; novydres/migration/PROGRESS.json; novydres/migration/VALIDATION_REPORT.md; novydres/migration/INVENTORY.json and CONFLICTS.md.
Novel world work: historical inventory novydres/migration/HISTORICAL_LIBRARY_CATALOG.json, source text under world/, systems/, governance/sources/. No POI binary originals imported.
Chronicle current sources novydres/chronicles/CHR-001/episodes/M2.03_v008.source.txt and character/state_v008.source.txt; historical full diary under character/legacy_character_full.source.txt.
Candidate V1.1: novydres/chronicles/CHR-001/LIVE.json and HISTORY_INDEX.json, both INACTIVE. Do not narrate; need full field, relationship and provenance audit.
All imported texts had source-versus-GitHub fetch_file exact string comparison; 87 source texts verified, 19 binary assets pending and 82 catalogue records remain unresolved. POC isolated.
Priority action: classify and copy remaining Drive items; audit full character V5 sheet and NPC history; complete binary transfer and world authority checks; validate bootstrap in separate conversation; formally cut over only when all required gates pass.
Do not repeat event M2.03.073, reroll M2.03.072 or rewrite earlier source. DEC-CR-014 remains historical Drive copy-on-write; Git cutover decision MIG-DEC-002 not yet adopted.
