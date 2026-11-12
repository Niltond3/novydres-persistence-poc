# CHR-001 — Revisão de encerramento episódico alternativo M3.01 V003

**Classificação:** PLAYER_SAFE
**Decisão:** encerramento episódico possível em C05-22, mediante a transição documental C37 validada.
**Escopo:** apenas o limite local de M3.01. A rota de criação e seus critérios seguem pendentes.

## Base reconciliada

- Ciclo de origem: CYCLE_V0036.json, blob 213e0ba00bfcb75f7e37bd5be35fb1bd9495b920.
- Manifesto de origem: MANIFEST_V51.json, blob 2a315f5593068e8ff8031cc6b3ca68846d926077.
- Último evento confirmado: CHR001-M301-C05-22-20261109-001.
- Ledger persistente: OPEN_THREADS_V23.json, blob c33f7e48b9c4b5ef98e2b6ac998b8375502308f5.
- Recibo da escolha expressa: PLAYER_DECISION_M301_EPISODIC_CLOSURE_V001_PLAYER_SAFE.json, blob 474a5f64987ac220de0d92214898df32842d3bd8.

## Critérios episódicos

As cenas efetivamente jogadas de C01 a C05 têm seus encerramentos locais G28 registrados. O ponto de C05-22 é reconciliado entre o ciclo e os registros de estado. Nenhuma unidade opcional não iniciada precisa ser jogada para satisfazer uma quota; ela permanece quieta, não recusada. A escolha do jogador autoriza o encerramento episódico alternativo, sem exigir que conflitos de mundo ou consequências persistentes sejam resolvidos.

Não há causa admitida para preparar C06 no D04 vigente. Isso impede abrir outra cena agora, mas não impede o encerramento episódico escolhido: não se inventa causa, oferta, recusa ou evento offscreen para preencher sequência.

## Critérios do Marco e da criação guiada

O Marco M3.01 pode fechar como episódio porque seus conflitos iniciados chegaram a conclusões locais registradas e há escolha explícita no checkpoint reconciliado. A rota de criação guiada, os requisitos de adaptação e qualquer revisão futura continuam pendentes segundo seus próprios gates. Encerrar o episódio não declara esses objetivos cumpridos, não determina a disposição da rota e não equivale a graduação ou CHARACTER_READY.

## Estado preservado

A transição deve manter sem alteração os seis refs de estado, os refs mecânicos e a ativação registrados em C36, inclusive o ledger persistente acima. Relações, consequências, conhecimentos, incertezas e conflitos abertos continuam conforme o estado jogado. Eles podem ser retomados somente sob unidade futura distinta, causa efetiva, reconciliação de estado e gates próprios; esta revisão não antecipa seu conteúdo ou resultado.

## Saída operacional

C37 registra somente o fechamento de M3.01, mantém C06 como NOT_STARTED, next_role=NONE e os gates de preparação, cena e Narrador fechados. Não inicia C06 ou M3.02, não cria cena nem autorização narrativa. A publicação só ocorre depois de todos os validadores e do readback remoto passarem.
