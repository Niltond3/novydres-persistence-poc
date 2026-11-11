---
id: arch-phase-a-index
status: CANDIDATO_PENDENTE_APROVACAO
scope: NOVYDRES_GLOBAL
authority: ADR-001
baseline_design_commit: 2d1b5ca7e9afeccef2af922fc8248a33154a3317
classification: PLAYER_SAFE
---
# NOVYDRES — Fase A · Índice e contrato de aceitação

Esta é a especificação PROPOSTA da arquitetura por assuntos. Não é nova entrada operacional, não concede autorização de migração, não substitui .AGENT.md, .CONTEXTG.md, ciclos, manifesto, G19/G23/G24/G26/G28 ou contratos editoriais. O único documento decisório já aprovado para a iniciativa é ../adr/001-subject-oriented.md. A fase B fica BLOQUEADA até aprovação expressa deste conjunto e reconciliação da baseline atual.

## Documentos coesos
- topologia-e-ownership.md: árvore de destino, responsabilidades e matriz de ownership.
- modelo-de-dados.md: ontologia, registro por assunto, IDs, relações, alegações, projeções e sigilo.
- git-e-roteadores.md: snapshots, escrita concorrente, histórico, interfaces Codex/Web, cache e recuperação.
- auditoria-e-mapa.md: auditoria estrutural, inventário de fronteiras, colisões e procedimento de equivalência.
- validacao-e-metricas.md: validadores implementáveis, ensaios de regressão, qualidade, tempo, tokens e proibição de legados.
- fases-b-e.md: contratos e gates detalhados de B, C, D e E; ponto de partida sem memória de chat.
- decisoes-e-gate.json: matriz de decisões pendentes, riscos, fontes e evidência do gate.
- schemas/subject-candidate.schema.json e schemas/record-candidate.schema.json: contratos de dados candidatos; NÃO são validadores ativos.

## Princípios fixos da proposta
Um assunto = um dono autoritativo para cada categoria de verdade e âmbito temporal; os outros assuntos usam referências por IDs. Um caminho corrente estável = uma única versão válida por commit Git; documentos históricos são recuperáveis pelo histórico Git, nunca pela descoberta de _Vnnn. Eventos, rolagens, decisões, aprovações e correções constituem registros adicionais imutáveis por política, validados por diff e proteção Git. Estado, sumários e catálogo são projeções. Distinguir fonte primária, declaração, observação, alegação, plano e UNKNOWN; não transformar inferência em acontecimento.

## Entrada e saída
Entrada de A: design HEAD acima; master observado em 44b5c2348ccd3bb2ea5edaaa918f2f55b197321b; o ramo divergiu de master em dois commits de cada lado. Os valores são observações de auditoria, não pins perpétuos. MASTER DEVE SER LIDO NOVAMENTE antes de B. A análise confirma existirem na design baseline 842 blobs / 81 diretórios e 687 nomes que seguem padrão semelhante a revisão no nome. CONTAGEM APENAS DIAGNÓSTICA, nunca KPI nem evidência de completude.
Saída de A: pacote candidato com commit Git e readback; status PENDING_APPROVAL e nenhuma alteração operacional. Aprovação de A autoriza apenas iniciar B em branch de design atualizada/reconciliada, não aprova automaticamente nova política em master, dados migrados ou cutover.

## Hierarquia e conflitos
A fonte atual continua a ser o master com o mais novo ciclo NUMERICAMENTE válido, predecessor e hashes de blobs verificados, seguido de manifesto exato e contratos nele pinados. Em master observado: MANIFEST_V53/CYCLE_V0038 com ORCHESTRATION_CONTRACT_V10, esquema/validador V12 e START_HERE_V9. Em design antigo: MANIFEST_V51/CYCLE_V0036. Não combinar esses snapshots. A arquitetura aqui é documentada a partir de design com checagem apenas administrativa de master. DEC-CR-014, governança editorial v1.0 e ADR-001 podem divergir quanto ao versionamento físico: a sucessão só passa a vigorar após decisão expressa e teste de equivalência. A auditoria preserva UNKNOWN e colisões pré-existentes.

## Política de comunicação (também obrigatória a qualquer agente B–E)
Ao encerrar fase/bloqueio: informar estado, SHA real, readback, pendência, recomendar CONTINUAR NESTE CHAT ou ABRIR CHAT LIMPO. Pedido só de decisão: RESPONDA AQUI e uma pergunta objetiva, sem prompt. Chat limpo necessário: prompt íntegro com ref verificada, escopo, gates, proibições e output PLAYER_SAFE; jamais segredos. Sem publicação: NOT_PUBLISHED. Sem gate PASS: handoff da MESMA fase, nunca da seguinte.
