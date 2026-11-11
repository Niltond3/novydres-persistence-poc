# SCENE_CONTEXT — SC-LOAD-WORKSHOP-03

**Memória contextual recuperada do índice e de eventos; POC sintética.** Scene anchor: SIM-LOAD-001-E021.

## Cena
Íris retornou ao galpão, onde está Ivo. O relatório de Vale ainda não foi verificado. O alarme ocorreu (SIM-M001-E003), causa desconhecida. Não declarar concluída a inspeção nem realizada a assinatura.

## Memória causal recuperada após oito eventos
Íris fez em casa a Leta a promessa: "Eu prometo a você: não vou assinar antes de conferir tudo." (evento **SIM-LOAD-001-E013**; indexado em `HISTORY_INDEX.json > arcs.arc-promise.event_refs` e presente em `LIVE.json > event_buffer`). Compromisso continua ativo.

## Conhecimento compartimentado
- Íris: sabe que fez a promessa.
- Leta: ouviu a promessa (SIM-LOAD-001-E013); não foi automaticamente informada dos acontecimentos posteriores.
- Ivo: NÃO ouviu a promessa na cena doméstica; nenhuma notícia dela foi comunicada a Ivo.
- Vale: suas afirmações permanecem NPC_CLAIM, sem garantia de verdade.

## Limites
O passado restringe contradição, não determina fala da PJ nem reação do NPC. Em conflito, abrir eventos originais por refs.

## Novo conhecimento de Ivo — SIM-LOAD-001-E024
Íris declarou em voz alta no galpão: "Não vou assinar. Fiz uma promessa para Leta.". Agora Ivo ouviu essa **declaração da PJ** sobre a existência de uma promessa a Leta. Não se presume que Ivo tenha testemunhado a promessa original de SIM-LOAD-001-E013, saiba seu texto literal completo ou acredite nela. O conteúdo exato da fala é testemunhado; a promessa original está documentada pelo evento 13.
