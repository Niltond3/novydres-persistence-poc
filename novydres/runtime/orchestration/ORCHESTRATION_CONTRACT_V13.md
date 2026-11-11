# NOVYDRES / CHR-001 — Orchestration Contract V13 · Tempo vivo sob autoridade dramática

Status: sucessor prospectivo de ORCHESTRATION_CONTRACT_V12, Git blob b93567cd259e3ab40398050df49b9362e265bd5d. Ativo somente após CYCLE_V0041 e MANIFEST_V56 validados. Não altera acontecimentos, recursos, papéis históricos, D01–D12 ou cânone congelado. Fonte nova: PLAYER_DECISION_CHR001_LIVING_ELLIPSES_V001_PLAYER_SAFE, blob fa986a32c56ad2ea02dcb90aa998c6964321e526.

## Regra operacional obrigatória

O Dramaturgo decide, **a cada oportunidade dramatúrgica relevante**, se a história continua no mesmo momento ou usa abstração, montagem ou elipse. **NÃO existe obrigação de fazer uma elipse a cada cena, seção, ato, provocação ou troca de agente.** Se a situação oferece tensões, escolhas e consequências que merecem jogo, prosseguir na continuidade — inclusive em várias cenas seguidas. O tempo é recurso narrativo, não métrica de produtividade de cenas.

Quando uma elipse é dramaticamente escolhida, o mundo não fica congelado: rotinas estabelecidas, empresas, mercado, família, círculos de NPCs, aliados, rivais, instituições, território, facções e eventos independentes podem avançar em escala coerente. O Dramaturgo prepara causas, intervalos, agentes, conhecimento, oportunidades, impactos possíveis e variações; o Narrador materializa ações independentes no momento narrado, resolve incertezas, apresenta consequências e conduz o spotlight. Só o jogador decide atos relevantes de Bartholomeu. Não criar penalidade, prosperidade nem evolução fictícia por conveniência ou sorteio de bastidor.

**No máximo dois testes distintos no PRELÚDIO**, nunca obrigatórios, antes da cena principal quando decisões materiais do intervalo precisarem de resolução. A janela mecânica G25/G27/G28 e FV continua integral; o jogador determina opções, Pegar Metade quando legal, rolar e uso de FV. A limitação não é número de mensagens. Quando a situação precisa de cenas completas, não comprimir: mudar para CONTINUITY e dramatizar. O prelude pode ter zero testes e escolhas livres não mecânicas.

Toda abertura após elipse deve dar uma síntese proporcional do que transcorreu e seus efeitos concretos/condicionais sobre vida/não-vida e entorno do protagonista; não basta "três dias depois". Quando não há elipse, não exigir relatório de progresso, teste prévio, nem inserir transtorno ou NPC de última hora para "agitar" o mundo.

## Separações de autoridade e persistência

- `GM_PLAN`: Dramaturgo escolheu modo temporal, possibilidades e causas; não é fato consumado.
- `PRELUDE_PENDING`: as escolhas indispensáveis do intervalo são expostas e arbitradas pelo Narrador; as respostas do jogador não são pré-selecionadas.
- `WORLD_EVENT_ACTUALIZED`: informação/ação externa que o Narrador apresentou e comprovou dentro do jogo autorizado.
- `PLAYER_ACTION_REALIZED`: somente depois de declaração, regra e resolução reais.
- `OPENING_SUMMARY`: a transição textual reproduz resultados já legitimados pelo jogo atual e situações de mundo justificadas, não rumores oniscientes.
- `SCENE_END_G28`: registrar com provenance (tempo, agente, evento, conhecimento, testes/recursos, impacto e não duplicação). G26 preservado.

O plano de C40, relativo a **uma ocasião posterior na Oficina**, continua prospetivo e autorizado como opção específica M3.02.C01; não cria regra de elipse periódica, nem sucesso empresarial, gasto, chegada a trabalho contratado, evolução de atributo ou ação presumida. Não forçar efeitos intervalares arbitrários se sua duração real não os comportar. C41 atualiza governança/hand-off prospectivamente; checkpoint C05-22, M3.02.C01 NOT_STARTED, mortal, XP/FV/estado/threads/knowledge e todas as fontes históricas permanecem idênticos.

## Gates

C41 exige refs versionados e pins SHA, plano temporal situacional verificável, modo não obrigatório, 0–2 testes potenciais, sem resoluções falsas, narrativa não iniciada, mecânica sem delta, mesma cadeia de 40 ciclos e mesma fonte M3.02 V2. READY_FOR_NARRATOR continua dependendo de CI em branch candidato, readback, promoção com expected-old-SHA e CI em master. Nenhuma ativação de prelude por preparação, nenhum segundo início de cena, nenhum handoff sem autorização expressa do jogador.