---
subject_id: architecture-narrative-simplification
status: EMENDA_CANDIDATA_NAO_OPERACIONAL
visibility: PLAYER_SAFE
---
# Contexto — Corte do harness narrativo

Data: 2026-11-11. PLAYER_SAFE. Emenda de desenho vinculada ao [ADR-001, seção 11](../adr/001-subject-oriented.md#11-revisão-do-harness-narrativo), integrada às fases A–E. O programa narrativo D00–D12 é uma das entradas a revisar, não o ADR nem um substituto de A–E. Este documento contém contexto de planejamento; não é um contrato operacional vigente.

## Diretriz de interpretação

Conforme ADR-001, DEC-17, as decisões da entrevista anteriores à integração do ADR às tarefas têm precedência sobre seu desenho original. Resolver por elas as questões já respondidas e adaptar a documentação; consultar o jogador somente quando restar escolha nova. DEC-16 (Q-01 aceita) delimita estrutura para fatos duradouros e prosa integral para detalhes incidentais, com consulta à fonte se ganharem relevância. Esta orientação não altera o limite documental da etapa atual.

## Problema e resultado esperado

O usuário relatou rotina técnica prolongada sem finalidade dramática clara, excesso de testes, cortes que abandonaram intenções relevantes, pouco avanço temporal, consequências insuficientes e NPCs que cediam diante de cordialidade. A disposição numérica foi criada para conter essa última falha; sua retirada precisa preservar essa função.

O resultado esperado é uma condução que desenvolva conflitos, relações e consequências e avance até os destinos combinados da criação guiada. O jogador declara escolhas do personagem e joga o drama; a operação documental habitual deve ficar a cargo do agente. Não é objetivo transformar cada interação numa auditoria nem garantir por instrução que um modelo nunca erre.

## Bases verificadas e limitação da análise anterior

| Base | Evidência em 2026-11-11 | Uso permitido neste plano |
|---|---|---|
| Checkout inicial | Branch `design/chr001-narrative-program-d01`, HEAD `be674bed8072509e9434843f8e588d2c56741161`; árvore inicialmente limpa. | Fonte da primeira análise, não destino desta emenda. |
| Branch correta do ADR | `design/subject-oriented-migration`, HEAD local e remoto `3cc958c110012c61c2d56b2868643174a7eed388`; selecionada após descoberta das outras branches. | Base desta entrega documental; não equivale à campanha atual. |
| `master` remoto | `c9fcfc0c558cd17d58ec8c8272da3ed70182ff37`, obtido com `git ls-remote` e `git fetch origin master`. | Snapshot de referência para desenhar a migração; redescobrir antes de executar. |
| Divergência | Branch inicial contra `master`: 45/33 commits exclusivos; branch correta do ADR contra `master`: 14/28. | Não fazer merge, rebase, substituição de árvore ou escolha automática de vencedores. |
| Cursor da branch inicial | CYCLE_V0034 / MANIFEST_V48, M3.01; declara C05 encerrada e C06 não iniciada. | Histórico da branch inicial. Não congelar a campanha nesse ponto. |
| Cursor remoto observado | CYCLE_V0045 / MANIFEST_V63, M3.02; declara C01 encerrada, C02 não iniciada e `READY_FOR_NARRATOR`. | Registro do que o arquivo declara. A cadeia completa, CI e permissão de execução não foram certificadas nesta análise. |

A crítica inicial usou a branch errada para localizar o ADR. O rascunho de ADR separado foi retirado; esta entrega complementa o ADR-001 existente. `master` já incorporou correções de spotlight, elipses e imersão; não é correto tratá-las como trabalho inexistente. Nenhuma cena é autorizada pela leitura de seu status neste documento.

## Situação do programa arquitetural

A foi aprovada para desenho em `fase-a/aprovacao.json`. O índice e o gate de B registram **B_REMEDIATION_REQUIRED**: 51/90 correspondências nas três rodadas Codex frente ao requisito de 30/30 por rodada; evidência Web insuficiente, operações negativas/jornadas não executáveis e CI não executada. São resultados registrados nos documentos, não testes reexecutados nesta entrega. A simplificação não transforma esses resultados em PASS nem dispensa correção de precisão e recuperação.

Esta revisão é emenda candidata de A. Deve delimitar quais contratos e casos de B mudam e quais evidências continuam válidas. As aprovações e os relatórios históricos não serão reescritos para parecer que a emenda já havia sido testada. Na execução futuramente autorizada do plano, C depende do gate comprovado de B e D depende de C, sem nova confirmação apenas por fase (DEC-22); E depende de D, revisão independente e autorização expressa de cutover. Nenhuma dessas condições foi satisfeita por escrever este plano.

## Evidência consultada

Todos os caminhos abaixo são relativos à raiz do repositório. “Inicial” designa `be674be`; “ADR” designa `3cc958c`; “Remota” designa o `master` `c9fcfc0`. Consultar o objeto Git correspondente, sem combinar pins entre snapshots. A fundamentação pública basta para esta proposta; nenhum segredo de trama é reproduzido.

| Fonte | Base | Constatação e limite |
|---|---|---|
| `novydres/sistema/arquitetura/adr/001-subject-oriented.md` | ADR | Decisão existente, fases A–E, caminhos estáveis, propriedade por assunto e ZERO LEGADO em E. Esta entrega acrescenta a seção 11 candidata. |
| `novydres/sistema/arquitetura/fase-a/aprovacao.json` e `fases-b-e.md` | ADR | A aprovada para desenho; gates e escopos de B–E preservados. |
| `novydres/sistema/arquitetura/fase-b/index.md` e `gate-e-readback.json` | ADR | B permanece em remediação; há lacunas de precisão e comprovação, não apenas excesso de procedimento. |
| `novydres/runtime/narrative-architecture/program/ARCHITECTURE_PLAN_V1.md` e `PROGRAM_RUNBOOK_V1.md` | Inicial | Programa D00–D12; contratos de trama/história/cena/beat e preparação obrigatória. Documentos de planejamento não provam vigência de todas as suas propostas. |
| `novydres/runtime/orchestration/ORCHESTRATION_CONTRACT_V1.md` e `ORCHESTRATION_CONTRACT_V2.md` | Inicial | Obrigação explícita de outra conversa e revisão da provocação inteira a cada cena. |
| `novydres/.AGENT_V4.md`, `.CONTEXTG_V3.md` e `runtime/orchestration/ORCHESTRATION_CONTRACT_V19.md` | Remota | Entrada por ciclo, pins, fontes, gates e sucessões de contratos. V19 acrescenta regras de uma cena específica e mantém referência a V18. |
| `novydres/runtime/orchestration/DRAMATURGO_ROLE_V4.md` e `NARRADOR_ROLE_V4.md` | Remota | Elipses exigem pacote e inventário dos fios; revisão pode bloquear a entrega. Já há orientação de evitar impor a auditoria ao jogador. |
| `novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_CHR001_SIGNIFICANT_SCENE_SPOTLIGHT_V001_PLAYER_SAFE.json` e `PLAYER_DECISION_CHR001_LIVING_ELLIPSES_V001_PLAYER_SAFE.json` | Remota | Há decisões prévias sobre cenas significativas e mundo em movimento. A consulta a prioridades e a exigência de jogar perdas/conquistas substanciais desta entrevista precisam ser incorporadas à revisão, sem apagar o registro anterior. |
| `novydres/runtime/scene-execution/PACING_TEMPORAL_FRAMING_V3.md` e `ELLIPSIS_PRELUDE_PROTOCOL_V1.md` | Remota | Há continuidade de objetos e vínculos, modos temporais e prelúdio opcional de até dois testes. O novo desenho precisa substituir requisitos incompatíveis explicitamente. |
| `novydres/chronicles/CHR-001/npc-disposition/CONTRACT_V2.md` e `narrative-tone/GOTHIC_PUNK_HORROR_GUARDRAILS_V1.md` | Inicial | Já se exige autonomia, atrito e distinção entre simpatia e concessão. Repetir isso não demonstra melhora comportamental. |
| `novydres/runtime/narrative-architecture/program/deliverables/D11_TEST_RESULTS_V019_PLAYER_SAFE.json` | Remota | Declara 58/58 verificações por reducer determinístico e zero cenas jogadas. O próprio relatório limita o alcance; não certifica qualidade narrativa. |
| `.github/workflows/novydres-m302-c02-final-v23.yml` e `novydres-m302-post-g28-v20.yml` | Remota | Workflows ligados a versões e checkpoints específicos acumulam verificação de predecessores. Substituição deve distinguir regressão histórica de validação do estado atual. |
| `poc/memory-v1/ARCHITECTURE_V1_1.md` | Inicial | Experimento de checkpoint/pacote de contexto e histórico recuperável. Não está automaticamente autorizado como persistência da campanha. |

As verificações foram leitura e comparação Git. Não foram executados validadores narrativos, testes de jogo, CI remoto ou uma auditoria completa de todos os documentos. Não se atribui causalmente toda falha de narração à quantidade de regras; isso é uma hipótese a verificar na substituição.

## Escopo

Incluído: fluxo de narração/dramaturgia, autoridade operacional, memória e recuperação, preparação, NPCs, ritmo/elipses, progressão guiada, persistência, validadores e CI relacionados ao fluxo, documentação de entrada e retirada das dependências substituídas.

Preservado: fatos jogados, decisões do jogador, recursos e resultados confirmados, cânone/fonte fechados, distinções de conhecimento, textos e fontes históricas, conteúdo aproveitável de D01–D12 e o desenvolvimento do suplemento.

Fora do escopo desta emenda: criar aplicativo/plataforma de agentes, reescrever cenas anteriores, jogar durante a documentação, alterar regras V5 sem decisão própria, refazer o suplemento ou promover invenções locais a cânone geral. O inventário integral e a transformação de toda a árvore continuam obrigações de D/E do ADR; esta emenda detalha a parcela narrativa, sem dispensar o restante da migração.

## Vocabulário do corte

- **Simplificação:** reunir ou reduzir uma obrigação preservando sua função necessária.
- **Modificação:** mudar comportamento, responsabilidade ou estrutura; explicitar o que substitui e o que preserva.
- **Exclusão do fluxo ativo:** um procedimento deixa de ser exigido. Antes de E, candidatos continuam isolados. Em E, caminhos antigos saem da árvore operacional, não ficam numa pasta de arquivo morto.
- **Deleção física:** retirar arquivo da árvore corrente, preservando o histórico Git. Informação necessária é migrada ao dono correto; redundância pode ser retirada com fonte e recuperação comprovadas. Este plano não executa nem autoriza deleções agora; E já exige retirar as rotas antigas após seus gates e autorização.

## Pontos de atenção delimitados

1. A entrevista exige a ficha inteira e destinos fixos; textos antigos admitem rota alternativa/incompleta. Atualizar o contrato prospectivo com essa escolha, sem simular liberdade sobre o desfecho obrigatório nem adulterar resultados passados.
2. A entrevista usa o limite público de final de 1970. Fontes anteriores contêm uma janela mais restrita. Preservar a restrição previamente aprovada até conferir sua autoridade; esta conversa não autorizou silenciosamente afrouxá-la nem permite revelar planejamento oculto.
3. “Substancial” é um critério dramático: mudança duradoura de relação, posição, compromisso, segurança ou condição do protagonista. A primeira ocorrência ambígua exige uma pergunta curta, não uma taxonomia exaustiva de perdas e ganhos.
4. A migração precisa reconciliar a branch do ADR, a branch narrativa inicial e o `master` atual. Sua solução técnica cabe à execução; divergência de intenção do jogador exige consulta, não harmonização automática.
5. Q-02 foi aceita como DEC-18: agrupar texto e mudanças por resposta, publicar e verificar antes da entrega. Não adiar até o fim da cena. A espera por resposta e a pausa em falha foram aceitas; contratos e ferramentas sucessores devem implementar recuperação sem repetição de resultados ou perda de escolhas. A decisão está tomada; a implementação permanece futura.

Continuação: [desenho e impactos](desenho.md), depois [backlog integral e sequência](../plano-integral/tarefas.md).
