# V3.3 — Auditoria de execução ChatGPT Web e plano de correção

Data: 2026-11-20. Branch candidata: `mapwork-v3/v33-agent-pipeline-20261120`. Baseline lido: `113d21c25276119f33e189786f333cc9b4db652f`. **Somente implementação candidata; nenhuma mudança de cânone/U02.**

## Evidências diretas

- `scripts/pipeline.py` é a entrada de negócio, porém `PIPELINE.md` exige `python scripts/pipeline.py run` e caminhos locais para todos os módulos/arquivos. Conector GitHub lê conteúdo mas não executa Python nem materializa um checkout completo. A execução anterior permaneceu sem `pipeline_invoked` conforme checkpoint Kingswell.
- `scripts/web_runner.py` utiliza `subprocess`/Git CLI e `GITHUB_ACTIONS`, e seu contrato V3.2 não equivale a uma execução integral V3.3 no chat. Não torná-lo executor obrigatório.
- `v33_contracts.capability_preflight` aceita `verified:true` e texto para capacidades de GitHub/entrega/pesquisa; só bytes de arquivos de imagem são testados localmente. Declarações não provam operações nem ida-e-volta.
- `v33_acceptance._verify_artifact` exige SHA e presença de um campo geométrico não vazio, mas não audita objetivamente os cruzamentos, níveis, topologia e cobertura. `evaluate` aceita `full_image_visually_inspected:true` e texto livre de 30 caracteres por critério sem amarração a um evento host de inspeção.
- Os oito estágios são sequenciais, mas a geometria aceita de uma etapa não está obrigada a manter os modais e invariantes aceitos na etapa anterior. O relatório de Kingswell registra INF-01 ainda não aprovada, e lotes/POIs devem continuar proibidos.
- Os recibos de geração, máscaras, arte, visão e atlas dependem de arquivos locais. Falta bridge comprovado para recuperar código atual e imagens de Drive, entregar bytes ao avaliador/compositor e fazer o caminho inverso, com hash/identidade/origem/readback.
- A CLI retorna código 0 para bloqueios esperados (checkpoint), distinguindo `BLOCKED` no JSON; consumidores precisam inspecionar JSON, nunca inferir sucesso por exit 0.
- Verificado nesta auditoria: `Google Drive` retornou a U02 identificada por `1PrfWEcD07Gz5eX5r2qKGaRlecixVKh6r`; materialização real local SHA-256 `9d55965f45181e3b943552e32df0e8ad41b63c8974ffd6e670f447ffd36eb9a0`, 1448×1086. Isto prova **referência original**, não geração nativa nem composição.

## Plano de implementação — gates sequenciais

1. **Transporte Web, sem arquitetura paralela.** Adaptar a entrada existente para ser importada/invocada no runtime Python disponível no chat, mantendo a mesma função `run`. Implementar um bridge de `manifest` de arquivos/materialização GitHub/Drive com diretório temporário, verificação de blob Git e SHA-256, sem rede ou CLI dentro do Python. Registrar explicitamente o limite de qualquer conector cujo formato não permita bytes transferíveis. Nunca confiar em JSON `success` como readback.
2. **Semântica de status e capacidades.** Implementar sondas host para os recursos realmente usados; `PASS` apenas quando o gate for comprovado; `FAIL` para evidência inconsistente; `BLOCKED` para dependência externa legítima ausente. Provar ida-e-volta de bytes, inclusive PNG/máscara; impedir recibos inventados de desbloquear operação.
3. **Fiscalização cumulativa.** Extrair IDs do Markdown vigente e vincular cada tentativa a hashes de entrada e do estágio antecedente. Adicionar verificadores determinísticos independentes da visão: grafos, graus de cruzamento, classes/pixels, níveis, modais, máscaras, fronteiras e proteção. Reprovar geometria não verificável; reler todos os modais acumulados.
4. **Visão e reparo.** Exigir recepção e leitura real dos pixels pelo agente. Evidência de revisão deve enumerar dimensões, hashes, inspeções por critério e pares; relatório textual não certifica a semântica. Estado de falha bloqueia etapa; após três tentativas sem progresso, replanejamento; checkpoint com SHA dos arquivos.
5. **E2E Web sem arte de Kingswell.** Usar U02 verdadeira, registrar capability probe e realizar validações reais com casos negativos: hash falso, imagem ausente, relatório fabricado, estágio anterior inválido e tentativa de POI antes de INF-07. Testes de imagens de prova neutras são **diagnóstico**, nunca candidata artística de Kingswell.
6. **Persistência/readback.** Gravar somente candidato na branch, conferir blob/ref, documentar comandos sem terminal para retomada. Canonização permanece dependente de aceite visual final e autorização editorial separada.

## Condições de encerramento

Nenhum teste de fixture, GitHub Actions, bytes U02 isolados ou declaração do agente substitui uma execução E2E com geração nativa, inspeção e composição reais. Qualquer ferramenta sem bridge comprovado leva a `BLOCKED_CAPABILITY`. Sem progresso objetivo, não anunciar V3.3 Web conforme nem liberar arte/lotes/POIs.
