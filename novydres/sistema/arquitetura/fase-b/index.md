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
