# NOVYDRES — Migration Recovery Handoff V3, 2026-11-02

**STATUS: MIGRATION_IN_PROGRESS / CUTOVER FALSE / DO NOT NARRATE.**

Este handoff substitui a seção de mídia do V2 e não altera fatos da crônica. Repositório: `Niltond3/novydres-persistence-poc`, branch `master`. Conferir HEAD e ler `novydres/MANIFEST_V2.json` e `novydres/migration/PROGRESS_V2.json` antes de agir. Contratos `.AGENT.md`/`.CONTEXTG.md` continuam vigentes com G19/G23/G24; não alterar cânone global.

## Política de mídia alterada por ordem explícita
Originais visuais ficam em Google Drive: https://drive.google.com/drive/folders/15eZF0RAiqSnlrWhXhgt8P58Tas49wq65. GitHub mantém somente IDs, URLs e metadados por `migration/VISUAL_ASSET_REGISTRY_V2.json` e auditoria `migration/DRIVE_MEDIA_MIGRATION_AUDIT_20261102_V1.json`. **14 PNG** da Biblioteca copiados por referência de arquivo original e conferidos por nome, formato e tamanho. **5** pendentes: Farol Vintage em Gravura Borgonha.png; Gramática Visual Canônica de Novydres(1).png; Guia Visual Cartográfico de Novydres.png; Legenda Cartográfica Visual de Novydres.png; novydres-tiles.zip. SHA-256 de origem de MasterMap calculado; SHA-256 de destino dos 14 ainda não conferido, não promover a verificação criptográfica. A versão atual do Git remove fragmentos binários MasterMap do HEAD; commits antigos mantêm histórico.

## Crônica e migração geral
Preservados: fontes textuais, nove arquivos brutos históricos do Drive (3 ZIP de código + 6 texto/código), índices e 30 shards derivados. Estado candidato CHR-001 **INATIVO**: M2.03.073, `CHR001-M203-CHANGING-CLOTHES-20261102-001`; Bartholomeu Krauser mortal, no vestiário do hospital. Funcionário de avental cinza perguntou “Você veio da emergência?”; jogador ainda não respondeu, e fala anterior termina em “só”. XP 519 total / 170 gasto / 349 disponível; crédito 20. FV alvo 6 / superficial 5 / agravado 0 / disponível 1. Nenhum evento, rolagem, XP ou Abraço novo.

Pendentes independentes da mídia: seis capítulos com `candidate` e relato posterior de fechamento; Madame Zoya v0.9 variantes com autoridade em aberto; NPC e ficha integral não exaustivamente conciliados; origem RNG/ledger COMMITTED não auditada; teste verdadeiramente em chat novo ainda não executado. O teste GitHub-only 15/15 ocorreu no mesmo chat. Não emitir MIG-DEC-002 antes desses gates.

Próxima recuperação: consultar primeiro `novydres/MANIFEST_V2.json`, depois este handoff, `migration/PROGRESS_V2.json`, `chronicles/CHR-001/LIVE.json`, `HISTORY_INDEX.json` e índices conforme necessários. Nenhuma narrativa por solicitação de migração.
