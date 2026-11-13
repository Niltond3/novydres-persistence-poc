# NOVYDRES — Handoff de migração e recuperação verificado em 02/11/2026

**MIGRATION_IN_PROGRESS. NÃO CUTOVER. NÃO NARRAR.**

Repos: `Niltond3/novydres-persistence-poc`, branch `master`. Consultar SHA do HEAD na nova conversa. POC `poc/memory-v1/` intacta.

## Leituras de bootstrap
1. `novydres/MANIFEST.json`, `novydres/migration/PROGRESS.json`, `novydres/.AGENT.md` e `novydres/.CONTEXTG.md`.
2. `novydres/migration/VALIDATION_REPORT.md`, `CONFLICTS.md` e `INVENTORY.json`.
3. Para CHR-001: `novydres/chronicles/CHR-001/LIVE.json` e `HISTORY_INDEX.json` — ambos candidatos desativados. Consultar character state v008 e episódio M2.03 v008 conforme referências.
4. Sob demanda histórica: `episodes/historical/M1_INDEX_V01_DERIVED.json` (75 localizadores M1) e `events/M2_SOURCE_MARKER_LOCATORS.json` (87 identificadores textuais M2). Confirmar fatos decisivos no diário integral e aplicar correções.
5. Mecânica alocada: `character/ALLOCATED_SHEET_PROJECTION_V1.json` (125+45=170 XP, Sara e Mary como Touchstones históricas).

## Integridade e cobertura
Inventário **190**: 148 textos com igualdade de readback, 9 arquivos brutos com igualdade SHA de blob, 14 pastas enumeradas, 19 ativos visuais da Biblioteca ainda não transferidos. Fonte de verdade operacional continua Drive; nenhum dado sintético POC integrado à história.

Último checkpoint: **M2.03.073**. Bartholomeu Krauser, mortal, troca incompleta no vestiário; trabalhador de avental cinza pergunta 'Você veio da emergência?'. O jogador ainda não respondeu; sua declaração anterior termina incompleta em 'só'. Ferido permanece sob cuidados, prognóstico UNKNOWN. XP 519/170/349, crédito20; FV 6/5/0/1. Não criar eventos/rolagens.

## Próximo trabalho
Completar auditoria ficha/relacionamentos/conhecimento; solucionar fonte original de ativos visuais e autoridade world; validar recuperação realmente em chat limpo usando GitHub; somente então emitir decisão MIG-DEC-002 de cutover com readback. Preservar G19/G23 e DEC-CR-014 histórica.
