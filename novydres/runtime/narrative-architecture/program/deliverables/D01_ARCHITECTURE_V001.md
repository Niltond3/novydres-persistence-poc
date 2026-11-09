# NOVYDRES — D01 · Ontologia e Arquitetura Narrativa V001
STATUS: PLAYER_SAFE | PROPOSTO | NÃO OPERACIONAL. Não contém fatos secretos nem novos eventos de CHR-001.
Fontes: ARCHITECTURE_PLAN_V1, PROGRAM_RUNBOOK_V1, D01_MANDATE_V1, D1/D2/H, contratos de orquestração, atlas e Dramaturgo. Em todo conflito, autoridade existente prevalece; a presente arquitetura NÃO a substitui.

## 1. Estrutura e relações
`MUNDO/CÂNONE -> CRÔNICA -> MARCO (função de construção) -> EPISÓDIO DE HISTÓRIA / HISTÓRIA-PROVOCAÇÃO -> CENA -> BEAT CONDICIONAL`.
O grafo TRAMA é **transversal**, não hierárquico: uma TRAMA pode cruzar múltiplos marcos, episódios, histórias, cenas e períodos; cada vínculo tem tipo e fonte. FIO é uma pergunta, vestígio, pista candidata ou dívida, nunca uma trama por definição.
- CRÔNICA: contêiner editorial (genre_promise, pergunta macro, horizonte, vínculos de cânone, requisitos de chegada, múltiplos estados finais). A campanha principal de 2010 é distinta da criação guiada já jogada.
- MARCO: **Contrato de Construção D1** com Alvo Funcional, Cobertura, Coerência, Consequência, superfícies obrigatórias e pacote de consolidação. "Ato dramático" é metáfora estrutural, não nova mecânica ou período obrigatório.
- EPISÓDIO DE HISTÓRIA D1: unidade atômica `entrada -> provocação -> resposta/interpretação do PC -> consequência -> saída`; pode conter várias cenas e intervalo temporal flexível. Não confundir com arquivo de episódio da persistência.
- PROVOCAÇÃO DE BIBLIOTECA D2: entrada independente e elegível materialmente, até três incidências (descoberta, complicação, consequência); **não** organizar em árvore de prompts/desbloqueios. Seleção aleatória D2 e adaptação local CHR001_CURATED_SESSION têm origens/autoridades diferentes e exigem registro do método efetivo.
- HISTÓRIA / PROVOCAÇÃO DE SESSÃO / SIDE QUEST: problema jogável autocontido com entrada não compulsória, por_que_agora, pergunta, objetivos de agentes, escalada possível e encerramentos locais. Pode contribuir para várias TRAMAS, sem obrigação de cumpri-las.
- CENA: oportunidade de mudança espaço-temporal com stakes, pré-condições, conhecimento dos presentes, alternativas à entrada/fracasso/recusa e saída; não prevê gesto, fala ou resultado obrigatório do PC.
- BEAT: reação facultativa/condicional por gatilho verificável; não é roteiro de falas ou decisões. Se condição falha, o beat não ocorre.
- TRAMA: conflito causal de escopo CHRONICLE/MAJOR/MEDIUM/MINOR, com origem, pergunta, porquê, objetivos independentes de agentes, oposição, pressão, pistas, relógios, destinos distintos e critérios verificáveis de término. Pode ser independente de outras tramas; convergência não é obrigação.
- FIO: PLOT_THREAD / CONSEQUENCE / CLUE_CANDIDATE / INCIDENTAL / BACKGROUND_UNKNOWN. Inventários de fios heterogêneos não determinam quantidade de TRAMAS.
- ACTOR: PC, NPC individual ou organização, com snapshot as_of, metas, medos, limites, recursos, posição e conhecimento rastreado. NPC->PC, PC->NPC e NPC->NPC são arestas **dirigidas independentes**. Conhecimento não se presume recíproco.
- FACT/SOURCE, CLUE, CLOCK, OUTCOME, KNOWLEDGE: fontes auditadas e afirmações separadas de alegações; pista oferece informação por acesso, relógio só muda por condição causal e capacidade; desfecho se comprova por evidência, não por intenção de autor.

## 2. Grafos e causalidade
Links de TRAMAS: CAUSAL (fonte verificável), THEMATIC (sem inferência factual), NONE (sem relação postulada), UNKNOWN (pendente). Nenhum vínculo se torna causal por proximidade de cenário, coincidência de NPC ou conveniência de metaplot. Não transpor conhecimento de um NPC a outro, nem de uma época a outra sem evento de aquisição. Para cada ligação registrar direction, as_of, source_event_ref, source_blob_sha, epistemic_status e authorial_provenance.
O atlas histórico é índice e evidência derivada, não fonte que substitua episódio original. Uma autoria posterior NEW_AUTHORIAL_DESIGN_POST_HOC nunca é evidência da intenção pretérita do Narrador/Dramaturgo.

## 3. Conteúdo mínimo antes de jogar
Biblia: pergunta macro, promessas de tom, limites de cânone, M1–M5 e gates até 2010 como **oportunidades** e não desfechos impostos.
Trama: premissa causal verificável, agentes e restrições, iniciativa mesmo sem PC, pelo menos caminhos de sucesso/falha/recusa/offscreen, evidências terminais e revisão se suspensa.
Investigação: verdade autoral escolhida e LOCKED antes de expor a primeira pista crítica, com pelo menos duas rotas independentes para informação crítica; ausência de lock bloqueia cena investigativa, não permite improvisar culpado.
História: incitante, por que agora, interesse da crônica/marco, escolha real, atrito e repercussões, no mínimo uma saída local legítima sem encerrar toda a trama.
Cena: estado e permissões, stakes, conhecimento NPC, mudança possível, saída e pre-roll G25; Narrador mantém improvisação ambiental, não cria fatos secretos estruturais.
Beat: gatilho, ator autorizado, mudança contingente, limite epistêmico, resultado se não ocorrer.

## 4. Encerramento / suspensão / abandono
Estados de TRAMA: DRAFT, LATENT, ACTIVE, ESCALATING, SUSPENDED, RESOLVED, FAILED, ABANDONED_WITH_CONSEQUENCES, RESOLVED_OFFSCREEN_WITH_EVIDENCE, SUPERSEDED_WITH_PROVENANCE. Terminais exigem terminal_evidence_refs, closure_test aplicado e preservação de sequelas/causal_debts. SUSPENDED exige reason, review_owner e review_trigger (não apenas "um dia"). Abandono é escolha possível e acarreta mundo independente; não punição arbitrária.
Estados de HISTÓRIA: DRAFT, ELIGIBLE, IN_PLAY, SUSPENDED, CLOSED_RESOLVED, CLOSED_FAILED, CLOSED_REFUSED, CLOSED_ABANDONED. A história pode fechar com TRAMA aberta. Cenas: PREPARED, READY, IN_PLAY, SUSPENDED/INTERRUPTED, CLOSED. Beats não acionados não se tornam eventos. Fonte: UNKNOWN/LOCATED/VERIFIED/CONFLICT; a falta de prova implica UNKNOWN, não falso.

## 5. Progresso e agência
A janela de 2010, o Abraço e as experiências vampíricas jogadas são requisitos editoriais de suficiência da criação guiada, mas não autorizam ocasião ou resposta forçada, roteiro invulnerável, XP automático ou data inventada. Preparar alternativas causalmente sustentáveis para recusa, falha, morte/ausência de agentes, elipses e descoberta precoce. Caso uma condição indispensável se torne inviável por fatos de jogo, registrar BLOCKED_DESIGN e consultar o jogador; nunca modificar o passado silenciosamente.
Alarmes editoriais, sem efeito no mundo: duas cenas substantivas sem delta => PACING_REVIEW; três revisões sem progresso, conclusão ou suspensão justificada => STAGNATION_REVIEW. Não fabricar ação offscreen como solução do alarme.

## 6. Qualidade verificável
Teste técnico: identidade/estado/fonte/verdade/pista/relógio/rotas/ciclo/COW/segredo. Teste literário separado: horror gótico-punk, tensão estrutural, instituições com poder assimétrico, NPCs que resistem e querem algo próprio, contraste humano, diversidade e custo das escolhas. Horror não equivale a violência gratuita; tensão não equivale a railroading. Ambos são necessários à promoção. Contratos e testes em arquivos irmãos D01; D10 fará implementação formal.
