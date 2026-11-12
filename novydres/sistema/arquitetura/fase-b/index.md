# NOVYDRES — Fase B, remediação técnica

**Gate: B_REMEDIATION_REQUIRED.** Fase C não foi iniciada nem autorizada. Os quatro candidatos existentes permanecem em estado candidato, sem ativação de rotas.

## Estado observado — snapshot histórico da remediação

- Escrita limitada à branch `design/subject-oriented-migration`, cujo parent esperado é `35862b10000883ac8e607f9de1a87d945b21c1a5`. Master somente leitura no SHA `0418f70ca0f01827de993273da191453a16d9857`.
- A comparação do master desde c26 identificou 11 commits e 55 caminhos alterados; nenhum dos caminhos dos candidatos nem das seis fontes pinadas mudou. O efeito é de atualidade/cronologia. Não houve reconciliação factual.
- MANIFEST V59 e CYCLE V0044 foram lidos no master atual. O manifesto, ciclo e seis pins operacionais conferem 9/9. Links de predecessor C42→C43→C44 conferem. A divergência de linhagem entre M57/M58/M59 foi preservada.
- Fontes: 6/6 path/SHA conferem no snapshot original c26 e no master atual; cinco fontes também estão na árvore de design. CYCLE_V0041 permanece somente no snapshot/master, sem cópia para design. Proveniência não foi reescrita.
- Candidatos: 5/5 envelopes válidos; 16/16 pins de candidato e 21/21 referências de fonte verificados. Sete de oito relações resolvem; uma está explicitamente fora do escopo. UNKNOWN permanece. A trama segue provisória e a história textual não comprova ledger técnico COMMITTED.
- Codex CLI: três rodadas reais da suíte de 30 consultas; 51/90 correspondências agregadas. Na avaliação registrada, o requisito fixo era 30/30. B-Q29/B-Q30 falharam nas três rodadas. Negativos e jornadas não foram testados como operações reais: os fixtures não trazem payload executável e critério de readback.
- ChatGPT Web: os três resultados antigos são autodeclarados, sem dados por caso nem readback independente. Nenhuma nova sessão Web foi executada aqui; estado INSUFFICIENT_EVIDENCE.
- Promoção remota protegida: três atualizações fast-forward por `expected_sha`, `force=false`; a primeira teve parent exato 35862. O último readback antes deste commit confirmou dez blobs, 16 pins de candidato, seis fontes em c26 e master inalterada. Esta consolidação será promovida com lease esperado sobre cdf1 e lida de volta.
- Concorrência real local no Git bare isolado: dois commits distintos no mesmo parent, um CAS vencedor e um escritor obsoleto rejeitado. Isso prova somente o comportamento local. GitHub remoto: um no-op protegido no HEAD passou; escritores remotos concorrentes não testados.
- CI não tem execuções no HEAD de design consultado. Telemetria Codex registrou tokens e bytes locais de trace; p50/p95 das três rodadas não é observável. Tokens/bytes HTTP Web não são expostos.

## Artefatos de remediação

- [Evidências por caso e métricas](evidencias-remediacao-final-2026-11-11.json)
- [Resultado de testes atualizado](resultado-testes.json)
- [Gate e readback](gate-e-readback.json)
- [Conflitos e proveniência](conflitos.json)
- [Medições de navegação](navegacao-web.json)
- [Protocolo reproduzível para três sessões Web](protocolo-chatgpt-web-3-sessoes.md)

Os fixtures novos são sanitizados: não contêm gabarito nem respostas factuais. Os relatórios omitem valores de respostas e conteúdo restrito.

## Emenda de desenho posterior a confrontar

A [simplificação narrativa vinculada ao ADR-001 §11](../simplificacao-narrativa/index.md) documenta decisões de condução e uma revisão candidata dos procedimentos. Não integra as evidências de teste acima nem altera este gate. Antes de executar candidatos afetados, delimitar a emenda de A e quais contratos/casos de B precisam de nova verificação; preservar falhas e aprovações históricas. C continua sem liberação por este registro.

O [plano integral A–E](../plano-integral/index.md) passa a concentrar a decomposição de todo o ADR. É planejamento posterior, não evidência adicional de B; nenhuma tarefa ou exceção foi aprovada por sua existência.

## Decisão

B continua em remediação. Não promover candidatos, não ativar rotas, não alterar master/runtime/cânone/eventos/rolagens/ficha/XP/FV/ciclos/material congelado. Na avaliação histórica acima, a exceção de telemetria ainda era proposta. Posteriormente, em 2026-11-11, o jogador a aceitou como DEC-19 do ADR: somente tokens reais e bytes HTTP Web indisponíveis ficam NOT_OBSERVABLE. Não cobre falha de precisão, evidência Web ausente, casos não executáveis ou CI. Essa decisão altera o critério futuro, não os resultados registrados nem o gate atual. Posteriormente, o jogador aceitou Q-04 como DEC-21: a suíte futura será dimensionada por riscos e repetição justificada, em vez da quota fixa. Aplicar os critérios revisados de A; não executar o protocolo histórico de três sessões como obrigação corrente. Os resultados antigos, falhas conhecidas e lacunas de execução continuam preservados, sem novo PASS por alteração de critério.

## B01 — Reconciliação GitHub (2026-11-12)

O protótipo histórico C41 de NPC, trama, história e estado foi cotejado com fontes e campos localizáveis em `matriz-equivalencia.json#b01_reconciliation_2026_11_12`. O `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` avançou a C45/M63 sem modificar os seis blobs de origem; recursos XP/FV mantiveram-se consistentes na projeção comparada, mas o cursor não é o do candidato. A discrepância é explícita e não promove o protótipo. UNKNOWN, NPC_CLAIM, fronteira do personagem, trama provisória e ausência de ledger técnico continuam intactos. Esta prova de estrutura não conclui revisão semântica independente, Codex, CI, negativos ou concorrência remota: **B_REMEDIATION_REQUIRED**; C bloqueada.

## Retomada B02–B05 verificada em 2026-11-12

- **B02:** `CODEX_NOT_EXECUTED` nesta conexão Web; histórico 51/90 e falhas B-Q29/B-Q30 preservados.
- **B03:** 30/30 comparações automatizadas de respostas congeladas antes da leitura do gabarito, com fonte e localizadores por caso em `resultado-testes.json`. Não se apresentou como revisão semântica independente nem como nova rodada Codex.
- **B04:** runner isolado e workflow em `.github/workflows/adr001-phase-b-isolated.yml` executados no [GitHub Actions 43155672041](https://github.com/Niltond3/novydres-persistence-poc/actions/runs/43155672041), sucesso com 12/12 negativos, 12/12 jornadas e sete guardas adicionais; duas leituras inexistentes deram HTTP 404. Ref remota descartável `test/adr001-b04-20261112`: um único vencedor, blob conferido, falhas concorrente/stale com erro GraphQL genérico, causa específica não demonstrada; limpeza dessa ref requer ferramenta com permissão de exclusão.
- **B05:** `B_REMEDIATION_REQUIRED`, pois Codex real, revisão semântica independente e prova da classe da rejeição stale seguem pendentes, entre limites de integração. `master` preservada; nenhum canônico, cena, recurso ou runtime alterado. DEC-25 `PARTIAL_OBSERVED_NOT_CERTIFIED`; DEC-26 vale só para unidade não recuperável. Próxima elegível: recuperar B02 em canal Codex real, revisar B03 independentemente e fechar B04 antes de repetir B05. **Não iniciar C.**

## B03–B05 — checkpoint de auditoria adicional (2026-11-12)

O ChatGPT Web verificou `design@0ce0d215`, `master@c9fcfc0c` e sandbox `8c6e72a2` por refs GitHub. CI [43155927667](https://github.com/Niltond3/novydres-persistence-poc/actions/runs/43155927667) confirmou `success`. A auditoria separada em `resultado-testes.json#b03_locator_followup_2026_11_12` conferiu 30/30 pins e localizadores, mais igualdade de oito campos B-Q29/B-Q30 entre candidato histórico C41, fonte LIVE_v038 e projeção de recursos em LIVE_v039 no master. Os dois curingas antigos foram discriminados por campo. A auditoria de localizadores **não** constitui revisão semântica independente; B-Q26 exige leitura contextual.

B02 real Codex e revisão independente permanecem pendentes. B04: a ref descartável confirma commit vencedor e parent; erro GraphQL genérico não certifica stale. As 12 negativas, 12 jornadas e sete guardas com CI são sintéticos, não provas do runtime real nem de perda de confirmação remota. Sem operação segura de exclusão de ref nesta conexão. **B_REMEDIATION_REQUIRED**; DEC-25 parcial, DEC-26 por unidade, C bloqueada. Readback do novo commit deve ser verificado após a publicação, sem tocar runtime, `master` ou cânone.

## B02–B05 — Codex real e retestação focada (2026-11-12)

- **B02:** Codex CLI 0.150.1 executou 30 consultas reais em workspace temporário somente leitura, com C41 e candidato pinados e master C45 excluído. Uma revisão semântica independente aprovou 17 casos e encontrou 13 afirmações genéricas sobre projeção/ledger sem suporte nos localizadores citados. A causa foi a instrução do executor que exigia esse aviso em todas as respostas. Apenas os 13 casos afetados foram repetidos com o prompt corrigido; a revisão independente passou 13/13. Cobertura efetiva: 30/30, incluindo B-Q26, B-Q29 e B-Q30. As falhas históricas de B-Q29/B-Q30 não têm causa identificável porque as respostas antigas não foram preservadas. Evidência integral restrita em `resultado-testes.json#b02_codex_real_2026_11_12`.
- **B03:** a classificação automática Web anterior continua 30/30. As respostas brutas antigas não existem no checkpoint: `RAW_RESPONSES_UNAVAILABLE_FOR_INDEPENDENT_REVIEW`. Não houve reconstrução nem revisão retroativa pela nova saída Codex.
- **B04:** CI isolada no commit publicado passou; ela continua sintética. O probe remoto com `expected_sha` anterior recebeu erro GraphQL genérico; a ref e `master` ficaram inalteradas, portanto rejeição stale não foi comprovada. Não existe rota real de escrita para testar idempotência, payload conflitante, guards de autoridade/conhecimento/divulgação/prova ou recuperação após perda de confirmação.
- **B05:** `B_REMEDIATION_REQUIRED`; commit `b73eb073` foi lido de volta com parent, árvore e cinco blobs conferidos; CI [43212545361](https://github.com/Niltond3/novydres-persistence-poc/actions/runs/43212545361), job [131163549104](https://github.com/Niltond3/novydres-persistence-poc/actions/runs/43212545361/job/131163549104), passou no runner isolado sintético. Permanecem sem prova a revisão das respostas Web brutas ausentes, a proteção da rota real de escrita, stale SHA remoto, DEC-25 geral e p95 histórico Web. DEC-26 continua limitada à unidade histórica Web irrecuperável; C não iniciada. Próximo: recuperar as respostas Web originais se houver cópia e reavaliar B05; os testes de rota B04 aguardam que a rota real exista. Não iniciar C.

## Aplicação prospectiva de DEC-27 (2026-11-12)

A obrigação de provar separadamente Codex e ChatGPT Web foi revogada por decisão posterior do jogador. Os resultados por canal acima continuam históricos; `CODEX_NOT_EXECUTED` não é, por si, bloqueador corrente. A prova B02 de recuperação com revisão independente pode ser reutilizada se código, fontes e contrato não mudaram. A rota preferida é ChatGPT Web + GitHub/Actions, com prova de integração quando houver diferença relevante. Seguem obrigatórios executor B04 remoto, revisão semântica independente prevista, exercícios narrativos contextuais e métricas observáveis. B05 continua em remediação até prova; não aprovar retroativamente respostas Web desaparecidas.

## DEC-27 — Provas novas e B05 corrente (2026-11-12)

O contrato agora exige **prova por função e risco**, sem duplicar Codex/Web por interface. A evidência histórica Codex com revisão independente (30/30 efetivos) permanece reutilizável no seu snapshot, mas não aprova retroativamente as respostas Web antigas ausentes. Em nova rodada Web foram congeladas seis respostas (`00d1633`); três eram incompletas frente às perguntas integrais e foram retestadas sem apagar o erro (`c8afeab`). O avaliador determinístico posterior passou no Actions `43221036507`, com 6/6 efetivos, sem reivindicar revisão semântica independente.

B04 agora usa REST e Git em uma ref descartável real. O Actions `43220528637` registrou publicação/readback, transação repetida idempotente, mesmo ID com payload conflitante rejeitado, dez controles negativos, recuperação após confirmação suprimida, dois escritores com único vencedor e `git push --force-with-lease` obsoleto rejeitado explicitamente como `stale info`; erro REST 422 genérico continua não classificado como lease. Ref de teste removida. O runner posterior passou também em `43221036507`. A correção DEC-25 lê a decisão vigente diretamente do ADR em commit fixo, com teste CI subsequente ainda por conferir neste checkpoint. Perda efetiva de rede não foi induzida; testes não representam runtime em produção.

Oito exercícios narrativos fictícios e um resultado causal adicional foram preservados. Uma conferência contextual pelo próprio executor identificou a primeira versão N-06 como mero preparo, corrigida por um enquadramento com ação de PJ explicitamente fornecida; **revisão editorial independente permanece PENDING**. Uma coleta nova pareada de latência/bytes de corpo JSON REST foi implementada, sem inferir p95 histórico Web. O resumo atual permanece em `gate-e-readback.json#b05_dec27_current`: **B_REMEDIATION_REQUIRED**, C bloqueada, master/campanha/runtime inalterados.
