# NOVYDRES — Fase B, remediação técnica

**Gate: B_REMEDIATION_REQUIRED.** Fase C não foi iniciada nem autorizada. Os quatro candidatos existentes permanecem em estado candidato, sem ativação de rotas.

## Estado observado

- Escrita limitada à branch `design/subject-oriented-migration`, cujo parent esperado é `35862b10000883ac8e607f9de1a87d945b21c1a5`. Master somente leitura no SHA `0418f70ca0f01827de993273da191453a16d9857`.
- A comparação do master desde c26 identificou 11 commits e 55 caminhos alterados; nenhum dos caminhos dos candidatos nem das seis fontes pinadas mudou. O efeito é de atualidade/cronologia. Não houve reconciliação factual.
- MANIFEST V59 e CYCLE V0044 foram lidos no master atual. O manifesto, ciclo e seis pins operacionais conferem 9/9. Links de predecessor C42→C43→C44 conferem. A divergência de linhagem entre M57/M58/M59 foi preservada.
- Fontes: 6/6 path/SHA conferem no snapshot original c26 e no master atual; cinco fontes também estão na árvore de design. CYCLE_V0041 permanece somente no snapshot/master, sem cópia para design. Proveniência não foi reescrita.\n- Candidatos: 5/5 envelopes válidos; 16/16 pins de candidato e 21/21 referências de fonte verificados. Sete de oito relações resolvem; uma está explicitamente fora do escopo. UNKNOWN permanece. A trama segue provisória e a história textual não comprova ledger técnico COMMITTED.
- Codex CLI: três rodadas reais da suíte de 30 consultas; 51/90 correspondências agregadas. O requisito fixo é 30/30. B-Q29/B-Q30 falharam nas três rodadas. Negativos e jornadas não foram testados como operações reais: os fixtures não trazem payload executável e critério de readback.
- ChatGPT Web: os três resultados antigos são autodeclarados, sem dados por caso nem readback independente. Nenhuma nova sessão Web foi executada aqui; estado INSUFFICIENT_EVIDENCE.
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

## Decisão

B continua em remediação. Não promover candidatos, não ativar rotas, não alterar master/runtime/cânone/eventos/rolagens/ficha/XP/FV/ciclos/material congelado. A proposta de exceção é limitada à telemetria de tokens e bytes HTTP Web indisponível; não cobre falha de precisão, evidência Web ausente, casos não executáveis ou CI. Não adotar exceção silenciosamente.
