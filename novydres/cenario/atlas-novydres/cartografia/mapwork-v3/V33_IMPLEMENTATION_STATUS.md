# Mapwork V3.3 — implementação candidata e evidências

**Branch:** `mapwork-v3/v33-agent-pipeline-20261120`  
**Base imutável V3.2:** `adb5e0bfe32544cd5b30b1beaa509ae6b677d8da`  
**PR:** #8 (draft, contra `mapwork-v3/pipeline-unificada-20261120`)  
**Cânone:** NÃO ALTERADO. Sem aceite final do proprietário. Sem merge.

| Etapa | Situação verificável | Evidência / pendência |
|---|---|---|
| 0. Baseline | IMPLEMENTADA | `v33-baseline.json`; V3.2 preservada |
| 1. Executor ChatGPT Web | PARCIAL / BLOQUEANTE | `pipeline.py` não exige Actions; falta demonstração real de transferência de imagem nativa à pasta local e dos recursos de entrega |
| 2. Linguagem natural/escopo | CONTRATO IMPLEMENTADO | `v33_contracts.validate_intent`; resolução semântica pelo agente; índice de assuntos deve ser reconstruído no HEAD de master; marco ambíguo bloqueia |
| 3. Pesquisa/decisões | CONTRATO IMPLEMENTADO | `validate_research`, `validate_proposals`, `validate_inventory`, bloqueio de elementos sem autorização; requer fontes e consentimentos reais em cada intervenção |
| 4. Planejamento urbano | PARCIAL / BLOQUEANTE | Parcelas multicélula, morfologia variável e acessibilidade abstrata; nenhuma geometria territorial completa e real de Sulfok/entorno da Torre Ventura foi demonstrada |
| 5. Imagens nativas | CONTRATO IMPLEMENTADO, CAPACIDADE NÃO PROVADA | Receitas e máscara por unidade; SHA do PNG e máscara ligados ao compositor; geração e materialização real em ChatGPT Web ainda não testadas |
| 6. Auditoria/autorreparo | PARCIAL | Gates deterministicamente falham fechados; revisão visual independente; limite de três tentativas no ledger; ciclo autônomo real de correção de imagem não demonstrado |
| 7. Alta resolução/comparador | TESTADO COM FIXTURES | Só tiles afetados, herança de outros, comparador integral com zoom e ZIP offline; abrir no celular real e validar grande atlas ainda pendente |
| 8. Persistência/aceite | BLOQUEADA | Contratos de SHA e reinício; falta teste ponta a ponta em sessões reais, CAS/readback de releases com assets privados e aprovação visual final |

## Evidências reais de regressão

A suíte `tests/test_v33_contracts.py` e `tests/test_v33_urban.py` cobre autorização negativa, máscara protegida, PNG/SHA, substituição controlada, retomada, parcelamento, intents e saída móvel. Os testes da V3.2 permanecem para detectar regressão. O resultado oficial em GitHub Actions é o último workflow `mapwork-v3-ci.yml` que concluir PASS na HEAD da branch; não substituir esse resultado por execuções em commits anteriores.

## Critérios que permanecem ABERTOS

1. Provar no executor ChatGPT Web que uma imagem nativa efetivamente chega ao compositor e é reaberta via SHA local e mask SHA, sem simulação.
2. Validar escala/composição em atlas grande com entrega direta ao usuário, inclusive celular.
3. Obter fontes, limites e decisões explícitas de Sulfok; gerar e auditar uma composição real e pedir revisão somente ao final.
4. Localizar Torre Ventura por fonte exata; sem identificação inequívoca, bloquear, sem inventar.
5. Demonstrar recuperação de interrupção com assets privados por Drive, Git CAS/readback, testes negativos e publicação apenas após aceite visual.

**Resultado: V3.3 candidata parcialmente implementada; NÃO IMPLEMENTED/NOT READY FOR CANON.** Não usar contagens de testes em fixtures para alegar cumprimento dos cinco critérios reais.


## Ajuste de auditoria visual (candidato)

Foi adicionado o validador interno `scripts/v33_visual.py`, invocado exclusivamente pela entrada `pipeline.py run`. Pareceres de unidade vinculam os SHA de PNG, máscara, U02, plano e imagens de vizinhos em borda; o parecer global, posterior à composição, vincula SHA de tiles, overviews ANTES/DEPOIS, U02 e recibos de imagem. O modelo deve analisar os pixels; o código verifica documentação, cobertura e integridade, não a estética. Teste de imagens sem geração real não demonstra execução ponta a ponta. Kingswell ainda depende de rede espacial e máscaras reais.
