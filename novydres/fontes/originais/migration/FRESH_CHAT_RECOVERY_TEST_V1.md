# NOVYDRES — Teste independente de retomada em chat limpo

**Status:** TESTE PENDENTE, não executado em uma conversa nova. **Objetivo:** validar se uma instância ChatGPT Web sem acesso ao chat anterior reconstrói estado e causalidade apenas do GitHub.

## Prompt para copiar em conversa nova

> Recupere o projeto real NOVYDRES e a CHRONICLE_001 exclusivamente pelo plugin GitHub conectado, conta Niltond3, repositório `Niltond3/novydres-persistence-poc`, branch `master`. Não use memória de outras conversas, Google Drive, POC sintética ou inferências para preencher lacunas. Primeiro leia `novydres/MANIFEST.json` e `novydres/migration/PROGRESS.json`, depois `novydres/.AGENT.md`, `novydres/.CONTEXTG.md`, `novydres/chronicles/CHR-001/LIVE.json` e `HISTORY_INDEX.json`. Só abra arquivos complementares se o índice ou a questão o exigir, com a menor quantidade sensata de leituras.
>
> **Sem narrar, sem escrever no repositório e sem criar eventos**, reporte: estado/gate da migração; episódio e checkpoint real; última declaração literal do jogador e sua parte inconclusa; o que aconteceu e a fala do NPC no ponto atual; roupas, casaco, faca, itens e pessoas na cena; números de XP e FV; o fundamento correto para atributos usados nas rolagens do modo guiado versus pontos comprados; relações e conhecimento limitado de quatro NPCs relevantes e suas fontes; três pendências antigas de M1/M2, separando fatos de alegações; quais ativos e decisões impedem cutover. Inclua event_id, caminhos GitHub consultados e número exato de leituras. Se não houver evidência, diga UNKNOWN; se houver conflito, mostre-o sem resolver por inferência. Não consulte nenhum arquivo chamado `FRESH_CHAT_ACCEPTANCE_RUBRIC` durante a reconstrução.

## Protocolo externo de aceitação

- Verificar que o agente realmente só usou o conector GitHub e que não tinha histórico desta conversa.
- Confrontar resposta com `LIVE.json`, `HISTORY_INDEX.json`, `NPC_KNOWLEDGE_PROVENANCE_V1.json`, `OPEN_THREADS_V1.json`, `MECHANICAL_GUIDED_CREATION_RULES_PROVENANCE_V1.json` e textos integrais.
- Avaliar erros positivos falsos como críticos: PC recebeu ação não declarada; NPC alegou fatos que passaram a canônicos; fonte POC confundida com história real; rolagem não auditada apresentada como auditada; status vigente incorreto; gasto de XP/FV fictício; MasterMap ou capítulo candidato promovido silenciosamente.
- Teste não é aprovação automática de cutover: precisa ser revisado e registrado como `FRESH_CHAT_RECOVERY_VERIFIED` com URL/ID de conversa e evidência disponível.
- Em cenário normal, um turno dentro da cena precisa do LIVE já lido; recuperação de contexto histórico específica pode pedir INDEX + fonte focal. Na inicialização realmente limpa, contrato/governança adicionam leituras deliberadas. A meta da POC de baixo custo não dispensa validação.

## Evidência de ensaio já concluído

`novydres/migration/RECOVERY_TEST_GITHUB_ONLY_001.json`: script isolado no mesmo chat, **15/15** testes, **4** leituras do GitHub (LIVE, índice, conhecimentos e episódio), sem Drive. Não equivale a uma conversa nova de fato.
