# RELATÓRIO — POC Memória Contextual / load-001

**Status:** teste funcional sintético concluído com sucesso; **NÃO** autoriza migração automática. Repositório GitHub privado `Niltond3/novydres-persistence-poc`. Toda escrita ficou em `poc/memory-v1/`; nenhuma escrita na crônica real ou no Drive.

## Escopo e fonte
Fixture `SCENARIOS.json` contém 26 acontecimentos SINTÉTICOS seq 005–030, sem sorteios reais, sem narrativa espontânea do jogador e sem confundir log operacional com CHRONICLE_STORE_V0_2 técnico. Os eventos iniciais seq001–004 vieram de fixture **CHR-SIM-002**, identificados no índice como `synthetic_seed_import`; não são CHR-001.

## Execução
- **26/26** eventos gravados e relidos com IDs únicos, números 005–030 sem lacunas.
- **21 turnos comuns** somente LIVE: 1 `update_file` e 1 `fetch_file` por turno com estado/SHA disponível.
- **5 turnos especiais:** 011 transição, 013 promessa/atualização causal, 021 transição, 024 mudança de conhecimento de NPC, 025 rotação. Cada um usa `create_tree + create_commit + update_ref` e readback de 3 arquivos.
- Somando **apenas as operações de mutação + readback de cada turno**: `21×2 + 5×6 = 72` chamadas. Não corresponde ao TOTAL de chamadas de toda a execução: houve leituras extras de HEAD/tree, preparação de fixtures, auditorias e recuperação do índice.
- No turno 025: 15 eventos (005–019) arquivados integralmente; buffer 020–025 preservado, seis eventos. LIVE caiu de **13.589** para **5.725** caracteres, redução de **7.864 caracteres (~57,9%)** no caso medido.
- Ao final, LIVE seq 030 contém **11 eventos ativos** (020–030), arquivo anterior contém **15** (005–019), total 26, sem IDs repetidos.
- A promessa seq013 foi recuperada em seq021 após oito eventos, com registro de que **Leta ouviu a promessa, Ivo não**. Em seq024 Ivo passou a ouvir **uma fala posterior sobre a existência da promessa**, sem ser convertido retroativamente em testemunha da promessa original.
- Cold bootstrap **simulado, na mesma conversa**: leitura de LIVE, SCENE_CONTEXT e HISTORY_INDEX (3 arquivos), mais arquivo 005–019 (1) para conferir promessa histórica; não é prova de retomada em outro chat.
- Rolagem: dado fixo [3,9,10,4] em seq017, escolha sintética de não gastar FV em seq018, dados preservados, FV sem gasto; não foi teste de RNG real nem regra V5 completa.
- Recuperação técnica: commit criado sem atualização de branch; HEAD anterior permaneceu vigente. Publicação posterior + readback aprovados; nova tentativa identificou o `RECOVERY_PROBE` já presente, dispensando duplicação. **Não é teste de falha real da rede.**

## Achado de segurança semântica
No roteiro inicial, Leta recebia conhecimento sobre Vale e relatório sem fonte verificável. O roteiro sintético foi retificado **antes** do turno seq012; o teste subsequente manteve conhecimento limitado. Isso demonstra a utilidade do controle, não garante que o agente narrador nunca cometa a mesma falha.

## Limites da prova
A sequência foi executada por um orquestrador de chamadas programáticas com entradas sintéticas pré-definidas. O agente **não** foi testado produzindo livremente uma crônica de 26 turnos; não houve teste de novo chat real, estresse de limite de contexto, conflitos com documentos canônicos, erros de rede genuínos, latências rigorosamente medidas ou reconstrução integral da narrativa. Não inferir confiabilidade estatística de longo prazo a partir de 26 sucessos.

## Ajustes propostos (V1.1)
1. Incorporar `scene.context_packet` dentro de LIVE, eliminando sincronização obrigatória de SCENE_CONTEXT.md para uma transição comum.
2. Retirar `active_scene` do índice como campo operacional; LIVE é a única fonte do ponto atual de cena.
3. Atualizar HISTORY_INDEX apenas quando alterar links/entidades/arcos ou arquivar; declarar `pending_index_updates` em LIVE para não perder fatos ainda não indexados.
4. Manter consulta sob demanda a eventos originais; preservar separação entre alegação, observação, intenção, conhecimento e contradição.
5. Um novo teste deve usar dados distintos, contexto embutido em LIVE, retorno de promessa **após** arquivo, e comparar chamadas/bytes contra a V1.

## Gates para migração real
- Conciliar última cadeia validada de Drive (a última conferência fora deste ensaio identificou CONTEXTG V2.0, STATE v008, M2.03 v008; pesquisar novamente antes do corte).
- Preservar documentos canônicos congelados e a decisão vigente DEC-CR-014 até autorização explícita substitutiva.
- Validar integridade de cada fonte legada, eventos/rolls com proveniência, lacunas e conflitos sem silenciosamente resolvê-los.
- Testar bootstrap em chat novo real; comparar em casos narrativos adversariais/longos; ensaiar rollback.
