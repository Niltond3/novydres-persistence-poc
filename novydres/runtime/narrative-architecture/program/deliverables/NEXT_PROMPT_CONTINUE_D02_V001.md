# NOVYDRES · CHR-001 · DRAMATURGO — CONTINUAÇÃO OBRIGATÓRIA D02 (NÃO D03)

**Mandato exclusivo:** concluir a auditoria historiográfica D02 sem narrar, rolar, iniciar C06, avançar para 2010 ou alterar materiais operacionais/canônicos. O trabalho de D02 foi publicado PARCIALMENTE. **D02 NÃO PASSOU**; este prompt continua a mesma fase, sem incremento.

## Referências técnicas verificadas na execução anterior
- Repositório: `Niltond3/novydres-persistence-poc`.
- Branch operacional somente para LEITURA: `master`; HEAD observado: `124f9a9f43ed427d3db106d9187a875d74f60ac6` (revalidar).
- Branch documental de escrita: `design/chr001-narrative-program-d01` (descobrir HEAD atual, não assumir imutabilidade).
- Commit de conteúdo D02 parcial: `25a5a9ff57e5773c2a42b93b6258b3131ba245d9`.
- CYCLE_V0033 / última cena C05 encerrada / C06 NÃO iniciada / última âncora `CHR001-M301-C05-22-20261109-001` (revalidar o maior ciclo numérico).
- D01 entregou PASS; D02 atual tem FAIL por pendências de semântica e proveniência.
- Auditoria parcial: `novydres/runtime/narrative-architecture/program/deliverables/AUDIT_D02_V001.json`, blob `cff563cb8474826de5c6bdcef477e068fd700005`.
- Handoff parcial: `novydres/runtime/narrative-architecture/program/deliverables/HANDOFF_D02_V001.json`, blob `d78004798a9416f66c33da8aae4c46c267fc46c9`.

## Primeiro passo e autoridade
Abrir `https://github.com/Niltond3/novydres-persistence-poc/blob/master/novydres/runtime/narrative-architecture/program/START_HERE_PLAYER_SAFE_V1.md`, depois os programas `ARCHITECTURE_PLAN_V1.md`, `PROGRAM_RUNBOOK_V1.md`, `D01_MANDATE_V1.md`, `PROGRAM_HANDOFF_CONTRACT_V1.md` na mesma pasta; ler `novydres/.AGENT.md` e `novydres/.CONTEXTG.md`, contratos de governança, orquestração, Dramaturgo/Narrador, D1/D2/H, G28. Validar SHA atual de ambas as branches, ciclo mais novo, cadeia de antecessores, manifesto, LIVE, episódios e oito referências de CYCLE antes de trabalhar.

Na branch de design, ler os **dez entregáveis D01** (`D01_ARCHITECTURE_V001.md`, `D01_CONTRACTS_V001.json`, `D01_LIFECYCLE_V001.md`, `D01_GOVERNANCE_V001.md`, `D01_VALIDATOR_V001.mjs`, `D01_TEST_RUNNER_V001.mjs`, `D01_TEST_VECTORS_V001.json`, `AUDIT_D01_V001.json`, `HANDOFF_D01_V001.json`, `NEXT_PROMPT_D02_V001.md`). Conferir hashes na auditoria D01.

Em seguida ler integralmente os **sete novos entregáveis D02 de continuação**:
1. `D02_SOURCE_INVENTORY_V001.json`
2. `D02_EVENT_HISTORIOGRAPHY_V001.json`
3. `D02_CAUSAL_MAP_V001.json`
4. `D02_COVERAGE_AND_PROVENANCE_V001.json`
5. `D02_DOCUMENTARY_SEQUENCE_PLAYER_SAFE_V001.mmd`
6. `AUDIT_D02_V001.json`
7. `HANDOFF_D02_V001.json`

Todos situados em `novydres/runtime/narrative-architecture/program/deliverables/`. O inventário possui 474 arquivos com níveis separados de verificação; o mapa historiográfico localiza 661 registros documentais com âncoras de linha; 27 localizadores M1 e 30 fragmentos têm provas de existência/integridade. **Esses números não demonstram 661 eventos canônicos nem autoria original comprovada.** Fonte textual não é ledger `COMMITTED`.

## Corrigir o que impede PASS, sem retcon
- **D02-GAP-001:** auditar semanticamente M1.01–M1.09 diretamente no diário original (inclusive prólogo e eventos fora do índice derivado). Para cada afirmação relevante capturar fonte, blob SHA, linha/âncora, voz (PLAYER, NPC_CLAIM, NARRATOR_ADJUDICATION), decisão, efeito, estado de saída; corrigir precedência das erratas. Não transformar marcadores IDX em eventos técnicos.
- **D02-GAP-002:** M2.01–M2.03: separar acontecimentos jogados, falas, regras, correções e notas administrativas. Conferir legado, episódio cumulativo v017, shard inicial e versões/correções, especialmente adjudicações substituídas.
- **D02-GAP-003:** M2.04 C01–C17, transições/downtime e M3.01 C01–C05: revisar por evento as versões anteriores versus cumulativos; distinguir resumo editorial de transcrição original e narrativa confirmada de interpretação retrospectiva. Aplicar epistemologia NPC e correções com precedência.
- **D02-GAP-004:** investigar autoria original de história apenas mediante evidências contemporâneas: commits, publicação do dossiê antes da cena, declaração efetiva do jogador, atribuição do Narrador e colaboração emergente. Emitir `AUTHOR_UNKNOWN` quando insuficiente. Plano posterior não dá autoria ao Dramaturgo.
- **D02-GAP-005:** verificar ambos os lados de cada elo causal. Distinguir `CAUSAL_CONFIRMED`, `SEQUENCE_ONLY`, `THEMATIC_ONLY` e `UNKNOWN`. Candidatos ainda pendentes NÃO podem ser apresentados como comprovados. Não inferir conspiração ou unir fios não demonstrados.
- **D02-GAP-006:** auditar G28, correções e rolagens relevantes, registrando origem verificada ou UNKNOWN; não declarar migração para ledger técnico. Confrontar atlas V001 e COVERAGE_REPORT_V002 mantendo condição PARTIAL e os 44 fios heterogêneos sem converter em 44 tramas.

Conferir os contratos CH00–CH07 e os dossiês de M2.04/M3.01 **apenas como preparação editorial**, jamais acontecimentos por si. Os seis livros de referência são orientação de organização, sem reproduzir enredos. Preservar `D01-ADM-001`: manifesto pode conter ponteiros históricos; não editar/retificar silenciosamente, sempre usar o ciclo validado como cursor.

## Escrita, auditoria independente e publicação
Usar somente **arquivos NOVOS VERSIONADOS DE PROPOSTA** no diretório `deliverables`, na branch `design/chr001-narrative-program-d01`. Caso seja necessário revisar uma entrega V001 publicada, criar V002 (sem overwrite) e explicitar `supersedes`; seguir copy-on-write. Não atualizar `master`, LIVE, manifesto, CYCLE, episódios, ficha, XP, FV ou conhecimento NPC. Não introduzir GM_HIDDEN em resposta pública. Não iniciar C06.

Para declarar PASS, exigir inventário completo e auditado das fontes obrigatórias, evidências primárias para cada afirmação decisiva, autoria original e desconhecida diferenciadas, correções prevalentes, grafos sem causalidade fabricada, gaps explicitados, conformidade com D01, auditoria independente, commit atômico por conjunto, branch lease, readback de SHA/blob/conteúdo, HEAD master preservado e saída PLAYER_SAFE.

Se D02 atingir PASS, publicar `AUDIT_D02_V002.json`, `HANDOFF_D02_V002.json` e **somente então** `NEXT_PROMPT_D03_V001.md` completo; entregar ao jogador o prompt D03 pronto para novo chat. Se permanecer parcial, marcar FAIL ou estado verdadeiro, publicar progresso auditado e **novo prompt de continuação D02**, nunca D03.

A D12 somente poderá autorizar prompt ao Narrador após todas as aprovações e READY_FOR_NARRATOR, com autorização expressa da cena. Essa autorização não existe aqui.
