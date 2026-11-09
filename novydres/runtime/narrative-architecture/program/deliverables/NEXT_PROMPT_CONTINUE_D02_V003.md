# NOVYDRES · CHR-001 · DRAMATURGO — CONTINUAR D02 (NÃO D03) · V003

STATUS: PLAYER_SAFE · **D02 FAIL; D03 BLOQUEADA**. Este é novo mandato de **CONTINUAÇÃO D02**, não a etapa D03. Não narre, role, inicie C06, adiante 2010, modifique cena fechada, estado mecânico, conhecimento NPC, manifesto, LIVE, CYCLE ou cânone. Não publique GM_HIDDEN no chat do jogador.

## Repositório e revalidação mandatória
- Repositório: `Niltond3/novydres-persistence-poc`.
- `master` SOMENTE LEITURA, HEAD observado `124f9a9f43ed427d3db106d9187a875d74f60ac6` (redescobrir, não assumir).
- Branch documental `design/chr001-narrative-program-d01`; o HEAD observado antes da publicação V003 foi `d1d84b4c6f99f9765d52ef0086637d17eb528144`. **Redescobrir por GitHub ref API**; o HEAD após esta publicação é necessariamente outro.
- O cursor deve ser o **maior ciclo numérico validado**, não um ponteiro possivelmente histórico do manifesto. Na observação V003: `CYCLE_V0033.json` blob `51afa7fa15ba7dc49a863dfe6f6bb0c539014a6a`, cadeia 1–33 íntegra, seis refs e dossiê/sidecar oito de oito conferidos; `LIVE_v037.json` blob `3c51465d548484f0bbf5a42cd7d6611f0b3bb85e`; manifesto `MANIFEST_V46.json` blob `be1c859bf5ae3f954cb9f0e07caab5c4800728ba`.
- Checkpoint observado `READY_FOR_DRAMATURGO`; C05 CLOSED, C06 NOT_STARTED, last_event_id `CHR001-M301-C05-22-20261109-001`. Revalidar todos os dados.

## Autoridade
Ler `novydres/.AGENT.md`, `novydres/.CONTEXTG.md`, os contratos G19/G23/G24/G25/G26/G27/G28, orquestração e Governança, Dramaturgo/Narrador, CH00–CH07 e os contratos locais. Começar por `novydres/runtime/narrative-architecture/program/START_HERE_PLAYER_SAFE_V1.md`, depois `ARCHITECTURE_PLAN_V1.md`, `PROGRAM_RUNBOOK_V1.md`, `D01_MANDATE_V1.md`, `PROGRAM_HANDOFF_CONTRACT_V1.md`. Dossiê é PREP, não evento jogado. `D01` passou com dez entregáveis no diretório abaixo; validar hashes e auditoria.

## Diretório e evidência acumulada
Tudo em `novydres/runtime/narrative-architecture/program/deliverables/`. A evolução é append-only, não sobrescrever V001/V002/V003.

### D02 anteriores (invariantes de evidência)
- `D02_SOURCE_INVENTORY_V001.json` — `2930c663076969d7bb1071220bbe7d862409fc23`
- `D02_EVENT_HISTORIOGRAPHY_V001.json` — `a1e5f007c8a9fad8581b1cd494f5ae1b94a40012`
- `D02_SOURCE_ASSERTION_CHECKS_V002.json` — `3b8e2b147ecfb3b56ca7ff48d696f9fdf8dd9162`
- `D02_SEMANTIC_CASEBOOK_V002.json` — `36477d8a87b70868823e5325704efc409e63b0d9`
- `D02_CAUSAL_MAP_V002.json` — `cdd9730869adf29fbf5d0215bcc1e592fe801cf7`
- `D02_AUTHORSHIP_EVIDENCE_V002.json` — `22eb0c07cc1deb74bafd27dfa11cd4780f0a0bc3`
- `D02_COVERAGE_AND_PROVENANCE_V002.json` — `27e1c5fdfd2083c1d3e8ed9de1c701e0d9a30bba`
- `AUDIT_D02_V002.json` — `8a9a3d1294c5ea6bf0d3fdebba35b07d4ea18863` — FAIL.
- `HANDOFF_D02_V002.json` — `5a4b0b53e8b36d527b7b7d3b8605acdbff39cb3a` — FAIL.

### D02 V003 — novos suplementos (verificar blobs/readback)
- `D02_CONTEXT_ANCHOR_AUDIT_V003.json` — `681555e3b289a76010948ce0d7c65f4937fec7c7`
- `D02_ASSERTION_TRIAGE_V003.json` — `e3eba41ee19709232f84cff961f963e73b7a1f48`
- `D02_SCENE_COVERAGE_MATRIX_V003.json` — `9492451142962c9b31a16899dcf7bc445478df9b`
- `D02_G28_ROLL_PROVENANCE_V003.json` — `cf87d78ac2ee60f91283754c3db12fef54eac3fa`
- `D02_CAUSAL_AUTHORSHIP_REVIEW_V003.json` — `d301b4d2b3f69c1f7a73d6d753da338f1b4f93c8`
- `D02_EDITORIAL_ADVERSARIAL_DESK_V003.json` — `e84b465f010998038716afc8ecfce073fd17515e`
- `AUDIT_D02_V003.json` — `34b7f69c9dde8bccc6dcbed880c78826f291092c` — FAIL.
- `HANDOFF_D02_V003.json` — `532d3152f2fbb1b7b946b65a497f4296cf5d0b49` — FAIL.
- Este arquivo: `NEXT_PROMPT_CONTINUE_D02_V003.md`; consultar o blob SHA após publicação.

**Atenção:** os 661 itens são localizadores documentais, NÃO 661 eventos COMMITTED. V003 fez triagem conservadora 661/661, porém **ZERO adjudicações semânticas independentes novas**. Das 28 âncoras requerendo contexto, 27 têm excerto alinhado no intervalo citado e uma é comentário editorial sem valor de evento ficcional: melhora estrutural, não prova autoria ou efeito. A matriz mostra grupos sem marcas próprias para prólogo M1.01 e downtime. Em G28 foram lidos sete arquivos de auditoria, 48 testes com verificação estrutural de faces/paradas onde informadas; a fonte original de RNG segue não comprovada quando não há log de ferramenta autenticável. A auditoria adversarial V003 fez controles de contenção, mas **NÃO é revisão editorial independente**.

## SEIS GAPS — todos bloqueantes
1. `D02-GAP-001`: prólogo M1.01 e M1.01–M1.09, incluindo material fora do índice, divisão por declaração PLAYER, NPC_CLAIM, NARRATOR, regra, errata, decisão, efeito e saída. Prólogo foi jogado antes de sua reclassificação; não forçar gate anterior.
2. `D02-GAP-002`: M2.01–M2.03, legado/shards/versões cumulativas, invalidações, correções e resultados reais; `M2.03 v007 invalid_partial` é artefato inválido e nunca prevalente.
3. `D02-GAP-003`: M2.04 C01–C17 + downtime, M3.01 C01–C05, de ambos os lados da evidência, resumo versus transcript original, conhecimento limitado dos NPCs, invalidação C04.08 e C04.09 válida; distinguir encerramento administrativo de decisão do PJ.
4. `D02-GAP-004`: investigar autoria original por história/cena, com documento ANTERIOR à criação e atribuição específica. Commit GitHub, plano anterior e narração posterior não comprovam automaticamente autoria original. `AUTHOR_UNKNOWN` é o resultado correto sem prova.
5. `D02-GAP-005`: examinar cada elo de ambos os lados com `CAUSAL_CONFIRMED / SEQUENCE_ONLY / THEMATIC_ONLY / UNKNOWN`; não usar identidade, objetos, semelhança temática ou local como prova de conspiração. `D02-CAUSE-002` permanece `SEQUENCE_ONLY` até prova original.
6. `D02-GAP-006`: auditar G28 por teste e faces de origem, roll tool/run IDs quando disponíveis, FV/XP sem mudanças, Atlas V001/COVERAGE_REPORT_V002 `PARTIAL`. Não converter resumo/editoria ou marcação de evento em ledger técnico `COMMITTED`.

**Pendências adicionais:** `D01-ADM-001` (ponteiros históricos de manifesto; não repará-los silenciosamente) e `D01-GAP-003`. Preservar precedência das correções: CORR-IDENTITY-002, CORR-M1.06-001, M2.03 correção de ataque/rolagem, C04.09 válida sobre tentativa C04.08 anulada.

## Trabalho de aceitação
Concluir revisão semântica **por afirmação**, com proveniência de fonte exata (path, blob, linha 1-based e tipo), decisão de jogador versus alegação de NPC versus narrador, consequências comprovadas e saída, epistemologia/UNKNOWN. Investigar manuscritos contemporâneos e chats originais se houver como autenticar; ausência deve permanecer UNKNOWN, não preenchida por intenção posterior. Conferir todos os elos causais, G28, versão, lacunas e estado. Exigir revisão editorial independente real por executor distinto ou revisão verificável com independência metodológica demonstrável; não se autodeclarar independente porque rodou mais um filtro.

Somente PASS com evidência de todos os gates abre D03. Se falhar, produzir arquivos NOVOS versionados V004 ou sucessores, `AUDIT_D02_V004.json`, `HANDOFF_D02_V004.json`, `NEXT_PROMPT_CONTINUE_D02_V004.md` e manter D02, sempre no branch documental. Se PASS real, somente então publicar o prompt D03. Não tocar master nem arquivos canônicos/fechados/aprovados/congelados. Publicar atomicamente por blob/tree/commit e atualizar branch com `expected_sha` lease e readback de todos os blobs + master + ciclo. Em conflito de lease parar e diagnosticar, nunca forçar silenciosamente. Saída de chat: apenas PLAYER_SAFE, IDs, hashes, gate, pendências e prompt íntegro. Sem GM_HIDDEN.

D12 é a única fase que poderá preparar retomada NARRADOR, e ainda depende de aprovações expressas, ciclo `READY_FOR_NARRATOR` e autorização de cena. Nada neste mandato autoriza C06.
