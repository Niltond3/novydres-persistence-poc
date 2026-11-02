# SCENE_CONTEXT — SC-M001-03 (POC sintética)

> PROJEÇÃO CONTEXTUAL; NÃO É FONTE PRIMÁRIA. Reabrir eventos originais quando necessário.

## Agora
Íris está no galpão de manutenção com Ivo. Ivo acabou de perguntar o que ela descobriu sobre a bomba. A fala/ação de Íris está pendente. Fonte: SIM-M001-E004.

## Causalidade relevante
- Íris declarou que inspecionaria a bomba antes de assinar qualquer liberação (SIM-M001-E001); não está confirmado que a inspeção terminou.
- Vale afirmou que um relatório atestava segurança (SIM-M001-E002, NPC_CLAIM não verificada).
- Um alarme de pressão disparou e foi ouvido por Íris e Ivo (SIM-M001-E003, WORLD_EVENT).
- Ivo pergunta pelo resultado da investigação (SIM-M001-E004, NPC_ACTION).

## Conhecimento de cada personagem
- **Ivo sabe:** ouviu a declaração de Íris, a afirmação de Vale e o alarme.
- **Ivo não sabe por fonte confirmada:** o conteúdo real do relatório, causa do alarme ou conclusão da inspeção.
- **Íris (jogadora):** escolhe sua resposta, pode buscar mais informações ou mudar o rumo da cena.

## Gatilhos de recuperação
Se a fala mencionar **relatório, Vale, bomba, inspeção ou alarme**, consultar HISTORY_INDEX; para alegações e sequência exata, consultar `episodes/M0.01/events-001-004.json`.

## Guarda-corpos
Sem retcon silencioso, sem ações voluntárias da PJ pela IA, sem transformar NPC_CLAIM em fato, sem inventar novo conhecimento do NPC, sem considerar o evento de teste como crônica real.

## Proveniência
Índice: `poc/memory-v1/HISTORY_INDEX.json`; entidades: `entities/npc-ivo.json`; arco: `arcs/arc-pump.json`; registros originais: `episodes/M0.01/events-001-004.json`.
