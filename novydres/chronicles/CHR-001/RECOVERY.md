# NOVYDRES — Checkpoint de migração (02/11/2026)

**INATIVO / NÃO AVANÇAR CENA**. Para a fonte de verdade atual, consultar `novydres/MANIFEST.json`, `novydres/migration/PROGRESS.json` e `novydres/.AGENT.md` + `.CONTEXTG.md`.

**Bootstrapping da cena:** `novydres/chronicles/CHR-001/LIVE.json` + `HISTORY_INDEX.json`; para detalhes, abrir apenas o documento indicado pelo índice. Não duplicar o pacote de cena num segundo arquivo corrente.

**Conhecimento/pendências:** `novydres/chronicles/CHR-001/knowledge/NPC_KNOWLEDGE_PROVENANCE_V1.json` (9 pessoas) e `OPEN_THREADS_V1.json` (11 assuntos); M1 antigo em `episodes/historical/M1_INDEX_V01_DERIVED.json` (75 IDs) e M2 em `events/M2_SOURCE_MARKER_LOCATORS.json` (87 IDs). Índices não são ledger auditado.

**Mecânica:** pontos efetivamente comprados: `character/ALLOCATED_SHEET_PROJECTION_V1.json`. Paradas de teste na criação guiada: `character/MECHANICAL_GUIDED_CREATION_RULES_PROVENANCE_V1.json`, que comprova convenção de ficha-alvo provisória; não confundir com compra. XP 519 total, 170 gasto, 349 saldo, 20 crédito disponível; FV 6 máximo provisório, 5 dano superficial, 0 agravado, 1 livre.

**Última cena:** M2.03.073, `CHR001-M203-CHANGING-CLOTHES-20261102-001`, Bartholomeu Krauser mortal no vestiário hospitalar. Máscara posta, calças mal ajustadas; roupa de cima ainda em troca. Casaco feito por Mary está no banco, sem ser vestido; roupas manchadas ao alcance, faca na posse do personagem sem esconderijo definido. Funcionário de avental cinza viu roupas ensanguentadas e perguntou “Você veio da emergência?”. Jogador ainda não respondeu e declaração anterior terminou em “só”. Nada sobre o prognóstico do paciente, atual paradeiro da mulher ou poderes do homem pode ser completado como fato sem fonte.

**Integridade:** 190 registros = 148 fontes textuais por readback, 9 brutos por Git SHA (3 ZIP + 6 técnicos), 14 pastas, 19 visuais da Biblioteca pendentes. Seis capítulos de mundo possuem frontmatter `candidate`, apesar de relatos posteriores de fechamento. 45 objetos da POC permaneceram com os mesmos SHA. `LIVE.json` é INACTIVE_CANDIDATE e Drive é fonte operacional.

**Ensaios:** simulação de recuperação somente pelo GitHub no mesmo chat 15/15 em quatro leituras; verdadeiro teste em outra conversa ainda **PENDENTE**. Instruções em `novydres/migration/FRESH_CHAT_RECOVERY_TEST_V1.md`.

**Corte operacional:** MIG-DEC-002 NÃO emitida. Para atuar na crônica, concluir pendências e validar readback/cutover formal, preservando G19/G23 e DEC-CR-014. Não fazer alterações retroativas nem narrar por este handoff.
