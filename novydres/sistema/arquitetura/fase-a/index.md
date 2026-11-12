---
id: arch-phase-a-index
status: CANDIDATO_PENDENTE_APROVACAO
scope: NOVYDRES_GLOBAL
authority: ADR-001
baseline_design_commit: 2d1b5ca7e9afeccef2af922fc8248a33154a3317
classification: PLAYER_SAFE
---
# NOVYDRES — Fase A · Índice e contrato de aceitação

Esta é a especificação PROPOSTA da arquitetura por assuntos. Não é nova entrada operacional, não concede autorização de migração, não substitui .AGENT.md, .CONTEXTG.md, ciclos, manifesto, G19/G23/G24/G26/G28 ou contratos editoriais. O único documento decisório já aprovado para a iniciativa é ../adr/001-subject-oriented.md. Na execução futura do plano autorizado, B exige critérios de A comprovados e baseline reconciliada, sem confirmação adicional apenas pela transição (DEC-22). Nesta etapa não está autorizada a execução do plano.

## Atualização documental posterior à aprovação original

A aprovação histórica está em [aprovacao.json](aprovacao.json). A formulação inicial abaixo descreve aquele desenho; o estado posterior de B está em seu [gate](../fase-b/gate-e-readback.json). Na revisão atual, [ADR-001 DEC-16/DEC-17](../adr/001-subject-oriented.md#11-revisão-do-harness-narrativo) orienta o desenho: decisões aceitas da entrevista precedem a formulação anterior do ADR/A, e detalhes incidentais permanecem na prosa integral. O modelo de dados foi ajustado documentalmente, inclusive conforme DEC-23/DEC-24; schemas e ferramentas da baseline anterior ainda precisam de adequação nas tarefas futuras; não se reescreveram aprovações nem executaram novas provas.

## Documentos coesos
- topologia-e-ownership.md: árvore de destino, responsabilidades e matriz de ownership.
- modelo-de-dados.md: ontologia, registro por assunto, IDs, relações, alegações, estado atual e sigilo.
- git-e-roteadores.md: snapshots, escrita concorrente, histórico, interfaces Codex/Web, cache e recuperação.
- auditoria-e-mapa.md: auditoria estrutural, inventário de fronteiras, colisões e procedimento de equivalência.
- validacao-e-metricas.md: validadores implementáveis, ensaios de regressão, qualidade, tempo, tokens e proibição de legados.
- fases-b-e.md: contratos e gates detalhados de B, C, D e E; ponto de partida sem memória de chat.
- decisoes-e-gate.json: matriz de decisões pendentes, riscos, fontes e evidência do gate.
- schemas/subject-candidate.schema.json e schemas/record-candidate.schema.json: contratos de dados candidatos; NÃO são validadores ativos.

## Princípios fixos da proposta
Um assunto = um dono autoritativo para cada categoria de verdade e âmbito temporal; os outros assuntos usam referências por IDs. Um caminho corrente estável = uma única versão válida por commit Git; documentos históricos são recuperáveis pelo histórico Git, nunca pela descoberta de _Vnnn. DEC-23/DEC-24 definem estado atual por assunto, texto integral e histórico Git, sem ledger universal nem auditoria de faces. Decisões, aprovações e correções mantêm sua fonte histórica; registros adicionais só quando necessários. Sumários e catálogo são derivados; estado corrente é autoritativo no seu assunto. Distinguir fonte primária, declaração, observação, alegação, plano e UNKNOWN; não transformar inferência em acontecimento.

## Entrada e saída
Entrada de A: design HEAD acima; master observado em 44b5c2348ccd3bb2ea5edaaa918f2f55b197321b; o ramo divergiu de master em dois commits de cada lado. Os valores são observações de auditoria, não pins perpétuos. MASTER DEVE SER LIDO NOVAMENTE antes de B. A análise confirma existirem na design baseline 842 blobs / 81 diretórios e 687 nomes que seguem padrão semelhante a revisão no nome. CONTAGEM APENAS DIAGNÓSTICA, nunca KPI nem evidência de completude.
Saída de A: pacote candidato com commit Git e readback, escolhas substantivas resolvidas e nenhuma alteração operacional. Conforme DEC-22, depois de autorizado o plano para implementação, A PASS permite iniciar B em branch de design atualizada/reconciliada sem nova confirmação apenas pela fase. Essa transição não aprova ativação de política em master nem cutover; a autorização atual segue somente documental.

## Hierarquia e conflitos
A fonte atual continua a ser o master com o mais novo ciclo NUMERICAMENTE válido, predecessor e hashes de blobs verificados, seguido de manifesto exato e contratos nele pinados. Em master observado: MANIFEST_V53/CYCLE_V0038 com ORCHESTRATION_CONTRACT_V10, esquema/validador V12 e START_HERE_V9. Em design antigo: MANIFEST_V51/CYCLE_V0036. Não combinar esses snapshots. A arquitetura aqui é documentada a partir de design com checagem apenas administrativa de master. DEC-CR-014, governança editorial v1.0 e ADR-001 podem divergir quanto ao versionamento físico: a sucessão só passa a vigorar após decisão expressa e teste de equivalência. A auditoria preserva UNKNOWN e colisões pré-existentes.

## Política de comunicação (também obrigatória a qualquer agente B–E)
Ao encerrar fase/bloqueio: informar estado, SHA real, readback, pendência, recomendar CONTINUAR NESTE CHAT ou ABRIR CHAT LIMPO. Pedido só de decisão: RESPONDA AQUI e uma pergunta objetiva, sem prompt. Chat limpo necessário: prompt íntegro com ref verificada, escopo, gates, proibições e output PLAYER_SAFE; jamais segredos. Sem publicação: NOT_PUBLISHED. Sem gate PASS: handoff da MESMA fase, nunca da seguinte.
