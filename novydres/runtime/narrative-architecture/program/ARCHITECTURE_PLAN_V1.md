# NOVYDRES — PLANO DE ARQUITETURA NARRATIVA V1
Status: PLAYER_SAFE / PROPOSTO / D00 CONCLUÍDO / NÃO PROMOVIDO À NORMA OPERACIONAL.
Programa: D01–D12, execução em chats limpos com validação e handoff; este arquivo é fonte de planejamento, NÃO cânone da história, não constitui licença para retcon, cenas, XP ou FV.
Escopo: NOVYDRES genérico + reconstrução CHR-001 Bartholomeu Krauser (CORR-IDENTITY-002); base de auditoria: master @ 471ca26926c8413ed2c452806f27217f1cb57bc3; CYCLE_V0033 READY_FOR_DRAMATURGO; C01–C05 CLOSED, C06 NOT_STARTED. O executor deve redescobrir HEAD e ciclo atuais.

## 1. Referências oficiais pesquisadas (material no Google Drive)
Os livros originais permanecem no Drive por direitos autorais; NÃO copiá-los integralmente ao GitHub, não reproduzir seus enredos ou grandes trechos. Síntese analítica original sem spoilers de histórias de Bart:
- [Fall of London, 2020](https://drive.google.com/file/d/1OiiJ1ywrJT2jKbBMs8Z501mZ9HGWA7yR/view), seis capítulos, Storyteller Goals, cenas, Aftermath, múltiplas escolhas e epílogo. Referência: orientação macro, preparação da conclusão sem privar agência.
- [Let the Streets Run Red, 2020](https://drive.google.com/file/d/1LOPs6P_L8qENb6rWIlpcNKsZ4Va4S6Hb/view), quatro histórias; Story Breakdown de bastidores antes dos capítulos, diferentes rotas e decisão final; Power Prey pp.15–45. Referência: causa fixa, descobertas plurais, encerramentos distintos.
- [Cults of the Blood Gods, 2021](https://drive.google.com/file/d/1GOAOqaWCVSL9OCoGfqe8P_Rf_RLSvtXo/view), ecologias de cultos e Styx and Bones; facções com crenças, hierarquia, interesses e iniciativa; aventura em capítulos com consequências e epílogo. Referência: atores que agem fora de cena.
- [The Crimson Gutter, 2024](https://drive.google.com/file/d/1MYcG6kXMpIHBMea4XebbyS-KnePVTit-/view), 21 histórias modulares e recorrência de NPCs; identificação da razão de envolvimento do grupo, metas do Narrador e personagens, variações e efeitos de escolhas. Referência: histórias independentes/intercaláveis com progresso temático consistente.
- [Trails of Ash and Bone, 2021](https://drive.google.com/file/d/1Fz25d90Nnc5q3LhFZWpEL_T2jZSgQwDq/view), quatro histórias completas: The Wellspring, The Family, Open Your Eyes e Old Wounds. Esta última permite configurações alternativas de um crime; FIXAR os detalhes antes de jogar a investigação. Referência: mistério configurável antes da narração, não verdade improvisada depois de pistas.
- [Forbidden Religions, 2021](https://drive.google.com/file/d/1lR-4lmWf3UZvXy2sMwgu_uNoM-GDGd5n/view), material de crenças, estruturas, atividades, antagonismos e ganchos, não uma campanha completa. Referência: transformar facções em mecanismos de ação com meios/limites.

## 2. Diagnóstico verificável de CHR-001
Base: ATLAS_SNAPSHOT_V001.json / COVERAGE_REPORT_V002.json (PARTIAL, até C04), OPEN_THREADS_V23.json (após C05), M3.01_DOSSIER_V5.json, M2.04_DOSSIER_V9.json, programa CH00–CH07.
- Atlas: 7 agrupamentos de arcos; 391 event cards (382 PLAYED, 9 UNVERIFIED); 55 entidades NPC; 49 vínculos; 5 solo seeds; só 34 cards ligados a arcos de modo explícito; a ausência de vínculo no atlas NÃO prova ausência de causalidade. Autor original UNKNOWN para grande maioria de cards.
- 7/7 arcos têm causal_premise e agentes, 0/7 campo de forças opositoras preenchido, 0/7 objetivo terminal/closure formalizado; seis arcos têm indicação de ação autônoma.
- OPEN_THREADS_V23 contém 44 registros heterogêneos, que NÃO equivalem a 44 tramas e não têm condições terminais estruturadas.
- Dossiês de provocações têm atos, pistas, relógios e autonomia; a deficiência é entre a arquitetura global da campanha e o preparo local de sessões.
- CH00–CH06 estabelecem direção para o ano de 2010 e a necessidade de Abraço/experiências caínitas dramatizadas, sem garantir ainda uma trajetória robusta e editorialmente finita.
- Não transformar o envelope visto em C05, a caixa Y.B., o contato profissional de Daniel, Volnaya ou outros fios em conexões causais comprovadas sem evidência. Nenhum desfecho de mistério confirmado é descrito aqui.
- A narrativa da C05 mostra potencial dramático de relações, humor, perda e escolha moral, bem como o risco de eternizar novos ganchos se os fatos não forem classificados como pista, incidente, consequência ou detalhe.

## 3. Hierarquia recomendada, SEM confundir com autoridade dos Marcos D1
MUNDO/CÂNONE -> CRÔNICA -> MARCOS (função de atos estruturais) -> HISTÓRIAS/PROVOCAÇÕES -> CENAS -> BEATS condicionais.
TRAMAS atravessam perpendicularmente Marco/história/cena, com escopo CHRONICLE/MAJOR/MEDIUM/MINOR. FIOS são evidências, questões ou consequências dentro das tramas, ou INCIDENTAL e BACKGROUND_UNKNOWN.
- Crônica de criação guiada é jogo JÁ VIVIDO, não descarte da história. Horizonte: 2010; campanha principal separada e só deve ser aberta após gate de ficha, biografia e Marcos.
- Marco ≈ ato é leitura dramatúrgica, não nova equivalência mecânica; D1/D2/H congelados prevalecem.
- Provocação é história jogável com problema local, conflito e encerramento, não lista obrigatória de cenas. Uma história pode tocar várias tramas.
- Cena é oportunidade espacial/temporal de mudança, com entrada, stakes e saída. Beat é operação reativa, opcional ou revelação sob pré-condições. Nenhum beat força diálogo/ação do PC.

## 4. Verdade, causalidade e encerramento
Cada trama persistente exige: origem/evento inaugural; justificativa e pergunta dramática; verdade autoral de bastidores (ou variante escolhida e BLOQUEADA antes de usar a primeira pista); agentes com metas, recursos, medos e limites; oposição; meios de descoberta (rotas alternativas); consequências do não envolvimento; relógios condicionalmente disparados; destinos possíveis e critérios terminais verificáveis.
Terminais possíveis: RESOLVED, FAILED, ABANDONED_WITH_CONSEQUENCES, RESOLVED_OFFSCREEN_WITH_EVIDENCE, SUPERSEDED_WITH_PROVENANCE; SUSPENDED exige gatilho/prazo de revisão. Uma conclusão não precisa encerrar toda repercussão.
Fonte histórica e plano posterior são objetos diferentes: CANON_EVENT, PLAYER_DECLARATION, NPC_CLAIM, GM_PREPARED, GM_LOCKED_TRUTH, CONDITIONAL, UNKNOWN, NEW_AUTHORIAL_DESIGN_POST_HOC, PROPOSED_RETCON. Planejamento autoral novo não prova intenção pretérita.
Não interligar tramas pela vontade de ter 'grande conspiração'. Vínculos CAUSAL exigem fonte, vínculos THEMATIC não permitem inferências de autoria ou identidade, NONE é opção válida.

## 5. Modelos de dados a projetar em D01 e validar em D10
PLOT_CONTRACT: plot_id, scope, public_title, status, origin_event_refs, causal_premise, inciting_cause, dramatic_question, why_matters, pc_hook_noncoercive, actors, opposition, constraints, source_evidence, authorial_provenance, gm_truth_ref, clue_graph, clocks, branch_endings (success/failure/refusal/offscreen), closure_test, plot_links, knowledge_scopes, spoiler_class, version, approval.
CHRONICLE_BIBLE: chronicle_id, canon_dependencies, genre_promise, macro_question, M1–M5 functions/sufficiency, character_transformation_opportunities, historical_period_constraints, timeline_to_2010, playable_post_embrace_coverage, central_plot_ids, final_states_by_choice, graduation_gate, frozen_boundaries.
STORY_CONTRACT: story_id, parent_plot_ids, marco_id, inciting_incident, why_now, goals, nonmandatory_entry, NPC_agendas, dramatic_question, escalation, critical_choice, closure_routes, consequences, timebox_soft, relevant_sources, state.
SCENE_CONTRACT: scene_id, story_id, present_actors, viewpoint_limits, stakes, state_preconditions, fact_refs, what_changes, optional_beats, reactive_beats, pre_roll_gate, exit_conditions, refusal_paths.
BEAT_CONTRACT: beat_id, trigger, known_truth_refs, agency, intended_change, allowed_actions, forbid_claims, if_not_triggered.
PLOT_LEDGER: immutable event_refs, actor clocks, NPC knowledge, clue dispositions, current plot state, terminal evidence; handoffs only after readback.
HANDOFF: full SHA/branch, verified source state, phase_scope, deliverables source_sha, gates PASS/FAIL, pending approvals, next_phase prompt, public_safe.

## 6. O que deve existir ANTES da primeira cena
Preparado e versionado: verdades necessárias à investigação; limites do mundo; agentes independentes; conflitos; custos; gatilhos; múltiplas resoluções; direção de crônica e função de história; fonte das pistas planejadas; fallback se PC recusar/sair/fracassar. Não planejar falas imutáveis do protagonista, sequência compulsória, resultado de dados, destino arbitrário da investigação ou obrigação de aceitar serviços.
Narrador pode improvisar ambiente e reação local coerente, mas não originar um culpado, verdadeiro motivo ou novo arco secreto persistente sem procedimento de submissão/revisão ao Dramaturgo. Emergências do jogo podem exigir uma pausa de preparação; nunca retconar em silêncio.

## 7. Governança de autoria, correções e segredo
Preservar eventos fechados; nunca escrever por cima de arquivos CANÔNICO/FECHADO ou APROVADO/CONGELADO. Alterações propostas vão para branch de design, versionamento COW, avaliação de autoridade e leitura de confirmação. Retcons classificados GAP_FILL_PROSPECTIVE / INTERPRETATION / RETCON_SOFT / RETCON_HARD / CANON_CONFLICT; os dois tipos RETCON exigem aprovação explícita do jogador antes da aplicação; conflito não deve ser harmonizado silenciosamente.
GM_HIDDEN é uma classe de divulgação, não proteção de acesso: mesmo GitHub privado pode ser lido pelo proprietário. O jogador recebe somente PUBLIC_SAFE, IDs opacos, estado e diff de governança; sem título, resumo, nome de arquivo ou mensagem de commit que antecipe segredo. Nunca anexar GM truth ao handoff exibido. Quando houver exigência de isolamento técnico real, separar armazenamento e acessos antes de gravar segredos.

## 8. Programa faseado
D00 (este diagnóstico) -> D01 (ontologia e contratos) -> D02 (historiografia M1–C05) -> D03 (NPCs e relações) -> D04 (mapa e classificação de tramas) -> D05 (lacunas, decisões e retcons: PROPOSTAS sem execução) -> D06 (bíblia de crônica e jornada até 2010) -> D07 (bíblia de cada trama, verdades e finais) -> D08 (histórias/provocações, cenas/beats prospectivos e backlog) -> D09 (criação guiada, progressão, pós-Abraço e gates até 2010) -> D10 (schemas, role adapters e validadores) -> D11 (auditoria adversarial e literária) -> D12 (integração autorizada, release validada, handoff ao Narrador).
D01 deve fixar a semântica proposta; D02–D05 não precisam inventar verdade para lacuna; D06 e D07 definem o AUTORAL FUTURO respeitando fatos anteriores; D08 e D09 tornam o plano jogável e finito; D10 aplica sem alterar contrato congelado; D11 teste independente; D12 promove APENAS depois da aprovação explícita. D12 não deve forçar READY_FOR_NARRATOR se os gates da orquestração não o permitirem.

## 9. Critérios de qualidade Q0–Q8
Q0 proveniência fidedigna e estados epistêmicos. Q1 fatos causais e NPCs independentes. Q2 verdade de investigação pré-fixada ANTES de pista significativa. Q3 jogabilidade com >=2 rotas de descoberta para informação crítica e alternativas para recusa/falha. Q4 conclusão verificável e múltiplos destinos sem finais automáticos. Q5 horror gótico-punk, horror pessoal V5, agência moral e NPCs diversos não perpetuamente solícitos. Q6 cadeia plot->story->scene->event->knowledge->NPC->clue->clock->outcome e COW. Q7 transformação suficiente e chegada a 2010 possível sem sorte nem proteção de roteiro. Q8 spoiler-safe em prompts, relatórios e diagramas.
Alarmes propostos, NÃO gatilhos de imposição: duas cenas substantivas sem delta dramático => PACING_REVIEW; três revisões sem progresso ou suspensão fundamentada => PLOT_STAGNATION_REVIEW. Nunca inventar evento/offscreen por ter passado uma revisão.

## 10. Fontes canônicas operacionais existentes
- novydres/.AGENT.md; novydres/.CONTEXTG.md (contêm checkpoints históricos; sempre confrontar LIVE/ciclo atuais)
- novydres/runtime/orchestration/ORCHESTRATION_CONTRACT_V1.md; DRAMATURGO_ROLE_V1.md/V2.md; NARRADOR_ROLE_V1.md/V2.md
- novydres/runtime/narrative-architecture/NARRATIVE_ATLAS_CONTRACT_V1.md (proposto, anterior, não confundir com nova aprovação)
- novydres/runtime/provocation-prep/DRAMATURGO_CONTRACT_V3.md e LONGITUDINAL_PROGRESS_GATE_V1.md
- novydres/chronicles/CHR-001/preparations/global/CH00..CH07
- novydres/chronicles/CHR-001/narrative-atlas/ATLAS_SNAPSHOT_V001.json e COVERAGE_REPORT_V002.json
- novydres/chronicles/CHR-001/knowledge/OPEN_THREADS_V23.json, NPC_KNOWLEDGE_PROVENANCE_V21.json
- novydres/chronicles/CHR-001/orchestration/CYCLE_V0033.json: histórico de entrada D00, não fixar como atual para D01.

## 11. Gate de promoção
Plano de design NÃO é vigência. Só depois de D11 PASS, correções/remediações, aprovação do usuário e D12 bem sucedido pode entrar em uso como contrato ativo, com readback SHA e handoff explícito ao Narrador. Até lá nenhuma nova cena é autorizada por este programa; não alterar o ciclo de criação guiada.
