# NOVYDRES · CHR-001 · D02 — Parecer editorial independente V011

**Classe:** PLAYER_SAFE · **Status:** PASS_WITH_UNKNOWN · **Data:** 2026-11-09

**Revisor declaratório:** GPT-6 — `GPT6_D02_V011_SEPARATE_REVIEW_CONTEXT_20261109`, execução de revisão distinta do executor documental `D02_DOCUMENTARY_EXECUTOR` que produziu V001–V010. Assinatura: declaração editorial deste agente, **não** assinatura criptográfica nem revisão humana certificada.

**Objeto:** D02, apenas historiografia retrospectiva e proveniência até M3.01 C05. Não autenticar falas de ChatGPT, autoria original ou RNG que não possam ser provados.

## Método e âmbito

1. Revalidados por GitHub ref API: `master` `124f9a9f43ed427d3db106d9187a875d74f60ac6` e `design` `d6e2b776c3fadc69ec023ce395ff37b6bae57834`. Governança lida: `novydres/.AGENT.md`, `novydres/.CONTEXTG.md`, `PROGRAM_RUNBOOK_V1.md`, `D01_GOVERNANCE_V001.md` e `D02_INDEPENDENT_REVIEW_PROTOCOL_V004.json`. Conferidos artefatos V009 e os seis artefatos V010 exigidos.
2. A fila V009 possui **661 registros únicos**, com correspondência 1:1 aos 661 locators V001, agrupados em **33 unidades**. Todos os 661 usam `AUTHOR_UNKNOWN`, sem `original_chat_authenticated` nem `original_rng_authenticated`.
3. Os lotes V009 A–G foram confrontados por linha, incluindo cabeçalhos e trechos sem marcador, com os quatro blobs do `master`: **2.111 linhas arquivísticas comparadas**, **zero divergência de texto** e **zero duplicidade**, nos escopos legados M1.09–M2.02 (310), M2.03 (570), M2.04 (940), M3.01 (291). Isso prova fidelidade das cópias derivadas, NÃO completude de turnos originais. M1.02–M1.08 receberam checagem de locators e amostras; M1.01 002–003 continua sem transcrição original íntegra.
4. A amostra adicional usa o marcador central por linha em cada uma das 33 unidades, com IDs, SHAs e linhas no `D02_V011_SOURCE_SAMPLE.json`, além de checagens adversariais dirigidas a M1.01, cadeia M2.03, causalidade, correções, G28 e encerramento C05. **Transparência metodológica:** as conclusões V010 foram lidas antes da seleção determinística, de modo que NÃO se reivindica preseleção cronológica anterior à leitura. O controle contra seleção tendenciosa foi a conferência exaustiva do texto dos lotes V009, não apenas esses exemplos.

## Achados adversariais e resoluções

- **ERR-001 / ERR-002 — falsa aparência de ledger:** `D02_EVENT_HISTORIOGRAPHY_V001.json` tem `technical_ledger_committed_not_inferred:true` e `authority:PRIMARY_RECORDED_TEXT` em **661 fontes de registro e 27 fontes de locator**, apesar de **todos os 661** registros também declararem `not_technical_committed:true`. Não há autenticação de ledger técnico COMMITTED. **Resolução:** os 688 metadados conflitantes não são prova admissível; substituir sua interpretação pelos overrides V011 com `DERIVED_ARCHIVE` / `technical_ledger_committed_not_inferred:false`.
- **ERR-003 — intervalos antigos insuficientes:** em 102 de 661 registros V001, o `summary_excerpt` não está integralmente dentro do intervalo de linhas declarado (88 de M2.03, 14 de M2.04/M3.01). **Resolução:** proibir citação probatória desse trecho pelo intervalo antigo; usar os intervalos normalizados V009 comprovados por conferência textual ou deixar UNKNOWN. Não houve reinvenção de texto.
- **ERR-004 — classificação causal excessiva:** `D02-CAUSE-001` tinha `archival_type: CAUSAL_CONFIRMED` embora `original_two_sided_verified:false`. A linha local da cena indica desfecho reportado, mas não autentica causalidade original independente. **Resolução:** interpretação restrita a `LOCAL_DERIVED_SCENE_CLOSURE_OR_SEQUENCE_ONLY`; `D02-CAUSE-002/003/004` permanecem `SEQUENCE_ONLY`.
- **M1.01:** os trechos `legacy_character_full.source.txt:153–167` mostram prólogo e cena 004, com 002–003 explicitamente pendentes da Library. NPC proposto não vira fato jogado. **Resultado:** `UNKNOWN_SOURCE`, sem contradição original demonstrada.
- **M2.03 e precedência:** `D02_M203_VERSION_CHAIN_V009.json` documenta o v007 parcial inválido, progressão v007/v008/v016/v017 e shards derivados. Nenhum fragmento vira diálogo original autenticado. **Resultado:** cadeia derivada aceitável, autoria e RNG originais `UNKNOWN`.
- **G28:** 48 testes estruturais e 49 arranjos de faces relatados, nenhum erro de faixa ou pool nos controles prévios; recibos originais de execução não localizados. Aceitação histórica preserva resultado em mesa, **não** certifica execução da ferramenta. `Take Half` permanece determinístico, sujeito ao preflight arquivado.
- **Checkpoint:** `CYCLE_V0033.json` de SHA `51afa7fa15ba7dc49a863dfe6f6bb0c539014a6a` confirma C05 CLOSED, C06 NOT_STARTED, mortal, sem Abraço; sem atualização de XP/FV/cânone.

## Decisão dos seis requisitos

| Requisito | Julgamento | Limite que permanece |
|---|---|---|
| GAP-001 · M1 | PASS_WITH_UNKNOWN | M1.01 002–003 e eventuais turnos não indexados |
| GAP-002 · M2.01–M2.03 | PASS_WITH_UNKNOWN | Fonte derivada, sem chat de origem autenticado |
| GAP-003 · M2.04–M3.01 C05 | PASS_WITH_UNKNOWN | Completude de turns originais não provada |
| GAP-004 · autoria | PASS_WITH_UNKNOWN | `AUTHOR_UNKNOWN` em toda atribuição não atestada |
| GAP-005 · causalidade | PASS_WITH_UNKNOWN, com ERR-004 | Sem causa original bilateral confirmada |
| GAP-006 · RNG | PASS_WITH_UNKNOWN | `UNVERIFIABLE_ORIGINAL_EXECUTION` |

**Parecer:** `PASS_WITH_UNKNOWN` para o gate **epistêmico e documental D02** **após aplicação obrigatória da errata V011**. Não é `PASS_AUTHENTICATED`, não promove os registros à vigência canônica, não atesta completude de conversas nem abre o Narrador/C06. D03 pode prosseguir somente como camada de design, com conhecimento de NPCs limitado pela proveniência. `D01-ADM-001` continua administrativo em aberto e não é implicitamente resolvido.

**Vedações para D03:** ler `D02_V011_PROVENANCE_ERRATA.json` antes de consumir qualquer campo V001; nunca promover falas, hipóteses, causalidades, autoria, G28/RNG ou estados externos sem prova; preservar `UNKNOWN`; 0 retcon, 0 mudança no `master`, cânone, XP/FV e cenas encerradas.