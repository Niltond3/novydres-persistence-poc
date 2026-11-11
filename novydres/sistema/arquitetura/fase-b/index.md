# NOVYDRES — Fase B, protótipo isolado

**Gate B_REMEDIATION_REQUIRED.** Os quatro candidatos já publicados permanecem na branch de design, sem autoridade operacional, sem ativação de rotas e sem avanço para C.

## Readback e remediação — 2026-11-11

- A branch de escrita permaneceu em `6b56f907a3ca4683e010f654f212df16aa86af52` até a criação desta remediação. Master era somente leitura: observado inicialmente em `c26c0fbf15fff6c817182c06e6208e302b954f3a` e redescoberto em `d14e1a90de81f0348f2fd07062427b0602de3eb0` durante a tarefa; a árvore atual é `eb5a98b5fc2935eb8009e2b21bd921a001a9ddd2`. A mudança externa foi registrada sem reconciliação automática.
- No master atual, MANIFEST V57 (`c516d0e596a2cc8eb8da9e723d3b114d1dd0bf39`) e CYCLE V0042 (`47e9334b4c1696b8334c63ba938da25cf4f8e644`) são as versões mais recentes observadas. O ciclo aponta ao manifesto e ao V0041 (`06398ed7cbc19e315fb7d59b08cc807b3e36c88d`); 165/165 pares de caminho/SHA operacionais conferem. O estado do ciclo é `TEMPORAL_RECONCILIATION_REQUIRED`; cadeia histórica completa e replay não foram executados.
- A base de origem dos candidatos continua pinada em `c26c0fbf15fff6c817182c06e6208e302b954f3a`. Os 11 JSONs já publicados permanecem presentes, parseáveis e com SHA igual à árvore da branch. As 21 referências de seis fontes também correspondem por SHA ao master atual; o pin dos candidatos não foi reescrito.
- Três conversas temporárias reais no ChatGPT Web retornaram, por autodeclaração do modelo, 30/30 consultas, 12/12 negativos e 12/12 jornadas em cada rodada. Não houve citações por caso nem readback independente das respostas. Tokens reais e bytes HTTP não são expostos.
- Latência ponta a ponta observada: 92.868 ms (aprox.), 54.579 ms (aprox.) e 82.408 ms; p50 82.408 ms e p95 92.868 ms pelo método nearest-rank. A medição mistura duas somas aproximadas de ferramenta e um timer do navegador; não representa latência de serviço isolada.
- Codex: suítes independentes não executadas. Para o commit-base consultado, GitHub não reportou status, check-runs ou workflows.
- GitHub rejeitou uma atualização com expected SHA obsoleto sem mover a ref; duas chamadas protegidas de no-op no mesmo SHA preservaram a ref. Duas requisições protegidas concorrentes para o mesmo HEAD foram aceitas e a ref permaneceu intacta; escritores com commits concorrentes distintos não foram testados.

As comparações JSON locais continuam **PASS_SCOPED** (30/30), os negativos locais **PASS_SCOPED** (12/12) e as jornadas de mutação continuam **SIMULATION_ONLY** (12/12). Nenhum desses resultados substitui as execuções Codex faltantes, tokens reais, evidência Web por caso, teste entre escritores ou CI.

## Estado dos candidatos e conflitos

A classificação da trama permanece provisória e candidata; a história textual não equivale a ledger técnico COMMITTED; o cursor legado e as divergências seguem explícitos. Os quatro candidatos não foram recriados nem promovidos. Não houve alteração de master, runtime, cânone, eventos, rolagens, ficha, XP/FV, ciclos ou material congelado. Nenhuma rota foi ativada.

## Medição de navegação anterior

Três leituras diretas reais do conector Web: p50=421 ms, p95=443 ms, 14.034 caracteres. O ensaio de navegação complementar mediu legado em uma leitura (p50=438 ms, p95=500 ms, 58.743 caracteres) e candidato em três leituras (p50=1.247 ms, p95=1.353 ms, 2.064 caracteres). Houve menos texto e mais chamadas/latência naquele ensaio; não extrapolar para tokens ou para a suíte completa.

## Próxima ação

Continuar exclusivamente B: executar as três suítes Codex por categoria com medição observável, obter readback Web independente por caso, e executar CI/validator, concorrência e replay somente quando houver ambiente seguro e evidência reproduzível. **Fase C não autorizada.**
