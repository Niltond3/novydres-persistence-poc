# NOVYDRES — Fase B · Handoff complementar PLAYER_SAFE · 2026-11-11

**Estado:** B_REMEDIATION_REQUIRED. Fase C não iniciada. Candidatos não promovidos. Não confundir este relatório com estado narrativo da CHR-001.

## Referências
- Design inicial e parent esperado: `e213de0ec6e40df22afed3039636c94bb37d705b`; base tree `c7b732bd2762ee3b9796c73cf3cd6a02c351b848`.
- Master somente leitura: `c9fcfc0c558cd17d58ec8c8272da3ed70182ff37`.
- Baseline histórica de proveniência: `c26c0fbf15fff6c817182c06e6208e302b954f3a`.
- Novo relatório desta etapa: `evidencia-chatweb-parcial-2026-11-11.json`.
- Contratos propostos para os 24 casos ainda sem execução integrada: `contratos-testes-negativos-jornadas-2026-11-11.json`.
- Os relatórios anteriores permanecem intactos; não usar C36/MANIFEST_V51 como handoff da Fase B.

## Constatações
- GitHub: 16/16 blobs candidatos e 6/6 fontes no snapshot original e no master atual; 21/21 source_refs; 5/5 envelopes com campos mínimos. Uma relação externa ao protótipo permanece declarada, não inventada. UNKNOWN e sigilo preservados.
- 30/30 consultas com path, blob SHA e locator relidos diretamente no conector; 29 verificações locais limitadas e uma sem avaliação semântica. **Isso não é precisão de 30/30 do agente Web**: o oráculo estava visível e não houve avaliação cega/independente, nem três sessões independentes.
- B-Q29/B-Q30: os recursos têm identidade campo a campo entre candidato e fonte histórica. Falhas anteriores do Codex persistem sem causa isolada, já que não há trace íntegro de resposta e scorer para as três rodadas.
- Testes negativos 0/12 e jornadas integradas 0/12. Foram adicionados payloads e critérios para futura execução isolada; especificação não é execução.
- Tentativa remota inofensiva de stale expected SHA: erro GraphQL genérico e HEAD intacto; controle com expected SHA correto teve sucesso. CAS stale **NOT_OBSERVABLE como rejeição especificamente comprovada**.
- Master avançou 12 commits/51 caminhos desde 0418; fontes dos protótipos não mudaram; avanço operacional atual documentado CYCLE_V0045/MANIFEST_V63, sem reconciliação factual e sem merge.
- CI/check-runs/commit statuses para a design inicial: zero observados; validadores e suites Codex não rodaram nesta sessão.

## Gates pendentes
1. Executar três sessões Web **independentes e cegas** com scoring separado, resposta por ID e refs verificadas. O presente chat não substitui nenhuma dessas sessões.
2. Executar os casos adversariais e jornadas em repositório descartável com executor real, asserções e readback (nunca master nem design compartilhada).
3. Reexecutar as três rodadas Codex, preservar resposta bruta em ambiente restrito e trace do scorer, focando B-Q29/B-Q30.
4. CI/validadores reais para a branch design e prova remota CAS com resultado de erro diagnosticável. Telemetria Web de tokens/bytes HTTP continua NOT_OBSERVABLE sem exceção aprovada.
5. Reavaliar a Fase B. NÃO iniciar C nem inferir PASS.

**Recomendação: ABRIR CHAT LIMPO** apenas para continuar a Fase B, com o HEAD final comprovado após publicação deste pacote.
