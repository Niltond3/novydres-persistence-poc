# NOVYDRES — Migration Recovery Handoff V2, 2026-11-02

**STATUS: MIGRATION_IN_PROGRESS / CUTOVER FALSE / DO NOT NARRATE.**

Repo: `Niltond3/novydres-persistence-poc`, branch `master`. Verify latest HEAD before acting. Original PO C directory `poc/memory-v1/` preserved with 45 objects unchanged from initial baseline.

## Bootstrap for agent in a new ChatGPT Web conversation
1. Read `novydres/MANIFEST.json`, `novydres/migration/PROGRESS.json`; this V2 handoff is the newest migration recovery record.
2. Read `novydres/.AGENT.md` and `novydres/.CONTEXTG.md`; G19/G23/G24, DEC-CR-014 and all relevant authority rules still apply.
3. Read `novydres/chronicles/CHR-001/LIVE.json` + `HISTORY_INDEX.json`. Both are **INACTIVE_CANDIDATE**, not independently validated technical ledgers.
4. Use `HISTORY_INDEX.json` to discover NPC knowledge, open threads and history sources. For older event details, read `novydres/chronicles/CHR-001/historical/VERIFIED_SHARD_CATALOG_V1.json` and only the matching verbatim shard(s). Never infer that missing lexical markers prove missing historical facts.
5. If mechanical issue, consult `character/ALLOCATED_SHEET_PROJECTION_V1.json` (purchases) and `character/MECHANICAL_GUIDED_CREATION_RULES_PROVENANCE_V1.json` (provisional target-sheet pools in guided creation).

## Source-preserving progress and gates
Inventory **193** records: 151 text-source records **including one exact duplicate alias** (150 distinct verified archive paths), 9 verified original Drive raw files (3 ZIP, 6 code/text), 14 enumerated folders, 19 Library visual original files **NOT transferred**. Thirty further derived source-text shards were verified byte-for-byte at the text level against unchanged originals, 23 from legacy diary (406,151 UTF-16 units) + 7 from episode M2.03 v008 (111,894). These shards are **derived copies**, not 30 new source records. Catalog contains 91 lexical event IDs and 14 lexical name hints; two historical identifiers recovered in 3 GitHub-only reads.

Madame Zoya v0.9: variant `madame_zoya_v0_9.md` twice in Library with exact same text; variant `v0_9(1)` distinct frontmatter; `v0_9(2)` changes one narrative clause without version bump. All copies preserved; editor approval / authority remains OPEN. Six main world chapters have frontmatter `candidate`, while later archival handoff reports closure; don't silently promote. Original Library POIs/MasterMap/tiles pending original-byte route.

GitHub-only same-conversation deterministic recovery: 15/15 checks with four reads. Actual independent NEW CHAT test: **NOT YET RUN**; read-only instructions in `novydres/migration/FRESH_CHAT_RECOVERY_TEST_V2.md`. Do not claim it was tested just because this handoff can be read.

## CHR-001 operational source and current checkpoint
Drive remains operational source until **MIG-DEC-002** is formally validated and activated; no new technical `COMMITTED` ledger created by migration. Character: Bartholomeu Krauser (not Krause), mortal, future Gangrel only; guided creation M2.03.073. Last source event `CHR001-M203-CHANGING-CLOTHES-20261102-001`. Hospital staff changing room, medical mask on, large but poor-fitting trousers, upper clothes changing; Mary-made coat on bench, bloody original garments nearby; knife in Bartholomeu's control, exact concealment UNKNOWN. Gray-apron worker saw bloodied clothing and asked: “Você veio da emergência?” Bartholomeu has NOT responded. Player's last sentence ends unfinished with “só”, never complete by inference. Unknown patient's medical outcome, Nadezhda current location, Gromov capabilities. NPC accounts are NPC_CLAIM, not verified facts.

XP: total519, spent170, remain349, spend-credit available20. WP provisional maximum6, superficial5, aggravated0, available1. No new roll, WP cost, XP purchase, Embrace, or 2010 campaign transition. Two historical Touchstones: Mary and Sara (2010 validation open).

## Next action before cutover
Independently test GitHub-only fresh-chat recovery; resolve 19 Library originals or establish formal exception; verify editorial authority; finish broader mechanics/relationship audit; then, only with supporting evidence and approval, write decision MIG-DEC-002 and prove Git persistence/readback. Do not advance storytelling by migration request alone.
