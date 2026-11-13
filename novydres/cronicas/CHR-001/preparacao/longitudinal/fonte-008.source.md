# CH07 — Plano de implementação do Atlas Narrativo e Retrospectivo / CHR-001 V1
Status: PLANO EXECUTÁVEL PENDENTE DA PRÓXIMA EXECUÇÃO DO DRAMATURGO; autorização explícita do jogador em 2026-11-08. Este documento não é evento narrativo, não abre C04, não altera fontes congeladas nem programa trabalho em segundo plano.
Base observada: master 326c1dedfbc3fb51ac2d5d676537d46438cee19e; CYCLE_V0030 READY_FOR_NARRATOR; M3.01 C01–C03 CLOSED, C04 NOT_STARTED. Quando executar, redescobrir HEAD, sequência e estado (não usar esta base como atual perpetuamente).

## Objetivos de aceitação
A. Saber quais histórias foram JOGADAS, quais foram PREPARADAS por algum papel e quais foram reconstituídas posteriormente, incluindo informação e autoria desconhecidas.
B. Identificar TODO NPC tocado diretamente, mediado ou materialmente por Bartholomeu e relações NPC-NPC demonstradas, sem inventar afetos, contatos ou grau de confiança.
C. Obter estados históricos de cada NPC por checkpoint, seus objetivos próprios, pressões, capacidades, vínculos e conhecimento limitado.
D. Obter um mapa de arcos narrativos entre provocações, com dinâmica própria e eventos de escalada, sem reduzir tudo a Bart ou uma conspiração central.
E. Diagramar cronologia, elenco/relações e tramas com referências verificáveis.
F. Reusar o atlas para narrativas solo derivadas, com snapshot histórico, efeitos de divergências e sem reescrever CHR-001.
G. Após implantação, obrigar novas revisões do Dramaturgo a confrontar esses artefatos, preservando fluxo Narrador ↔ Dramaturgo.

## Etapa 0 — Preflight e autorização operacional
Validar HEAD/ciclo/manifesto/LIVE/last_event_id, .AGENT/.CONTEXTG, governança de fonte e contratos. Registrar uma fila de trabalho do atlas, não uma cena. Não publicar novo CYCLE nem mudar READY_FOR_NARRATOR exclusivamente para catalogar fatos. Se chamado quando next_role=NARRADOR, executar apenas auditoria documental separada e devolver o status correto; a revisão dramática só acompanha transição permitida. Se faltar fonte, CONFLICT/GAP; nunca declarar reconstrução concluída.
Inventário mínimo: legacy_character_full.source.txt e origem Drive arquivada; M1_INDEX_V01_DERIVED.json como localizador STALE; M2.01–M2.02 na fonte íntegra; M2.03 última versão válida, shards e correções; M2.04 última versão válida e encerramento M2; M3.01 episódio atual; HISTORY_INDEX e eventos G28; versões de NPC_KNOWLEDGE e OPEN_THREADS; dossiês das provocações e revisões; livro de decisões/retificações. Conferir nomes, aliases, fontes, timestamps e commits.

## Etapa 1 — Reconstrução episódica e autoria editorial
Criar cartões rastreáveis de M1.01–M1.09, M2.01–M2.03, M2.04 C01–C17 e downtime/closure, M3.01 C01 até último Cn realmente fechado. Para cada evento: quem declarou, quem narrou/adjudicou, fonte; data diegética ou UNKNOWN; atores; mudança verificável; event_id ou âncora legada; vínculo com arcos; custo; dívidas; status. Marcar autoria do enredo (PLAYER/NARRATOR/DRAMATURGO/SHARED/UNKNOWN) somente quando evidência permite. Diferenciar preparação ANTERIOR a cena de reconstrução POSTERIOR à cena, inclusive quando o Dramaturgo foi introduzido apenas durante a criação. Construir matrizes evento->ator, evento->arco, evento->fonte.

## Etapa 2 — Censo completo de NPCs
Partir dos 41 registros de NPC_KNOWLEDGE_PROVENANCE_V19 como baseline de pistas, NÃO como total garantido. Acrescentar todo figurante individuável com interação DIRETA, MEDIADA ou IMPACTO MATERIAL nas fontes primárias e qualquer NPC não coberto pelo registro operacional. Identificar aliases, personagens não nomeados, grupos/organizações, homônimos (ex.: Liev diferente de Lev), primeira/última aparição, grau de contato e se há apenas menção. Não presumir que toda pessoa no mesmo local interagiu com Bart. Para cada NPC, produzir histórico de estados e uma lista obrigatória de UNKNOWN para vida/morte, localização, metas, medo, ocupação e alianças não demonstradas. Sem fabricá-los para preencher campos.

## Etapa 3 — Grafo de relacionamentos em duas direções
Construir Bartholomeu->cada NPC tocado e cada NPC->Bartholomeu, e NPC->NPC onde há prova ou crença atribuída. Etiquetas separadas: família, amizade, rivalidade, hierarquia, emprego, dívida, temor, respeito, confiança, interesse, informação, dependência, segredo, coação, acordo e associação institucional; relações podem ser simultâneas e contraditórias. Distinguir FATO (casados), PERCEPÇÃO (NPC acredita), ALEGAÇÃO (NPC diz) e HIPÓTESE/PLANO. Registrar changes por evento, quem sabe, quem ignora, evidência e relação em cada checkpoint. Integrar, sem reescrever, escala relacional B (-5..+5), humor H e expressão P da disposição NPC existente. B UNKNOWN quando não houver base; nunca neutralidade 0 presumida. Relações entre NPCs podem existir sem Bart saber; mantê-las GM_HIDDEN e não exportar no player-safe.

## Etapa 4 — Retrospectiva de tramas
Agrupar cenas em ARCO apenas por causalidade verificável. Exemplos de famílias candidatas para auditoria (NÃO são vínculos confirmados entre si): identidade e família; trabalho e assinaturas; investigação Volnaya e pistas; oficina e integridade profissional; contato e política sobrenatural; escola; circulação urbana e poder institucional. Para cada arco: fonte de início, quem perseguia quais objetivos, oposição e constrangimentos, eventos protagonizados pelo jogador, fatos externos confirmados, o que ainda pode acontecer sem intervenção de Bart, prazos/gatilhos demonstrados, estado e responsáveis pelas próximas decisões. Tramas independentes podem cruzar por evento comprovado; NÃO estabelecer que Volnaya, empregadores, Gromov, vampiros ou instituições pertençam à mesma rede sem evidência.
Rastrear plano autoral original por dossiê e commit quando possível; se não houver dossiê anterior, registrar AUTHOR_UNKNOWN. Não transformar retrospectiva editorial em intenção passada do Narrador ou do Dramaturgo.

## Etapa 5 — Diagramação e atlas navegável
Publicar um ATLAS_SNAPSHOT_V001.json validável pelo schema V1 e um COVERAGE_REPORT_V001.json com taxas de fontes/eventos/atores/arestas/arcos examinados e lacunas explícitas. A partir do snapshot, gerar diagramas Mermaid versionados: RELACOES_BART_PLAYER_SAFE, RELACOES_NPC_PLAYER_SAFE (somente vínculos conhecidos), TRAMAS_PLAYER_SAFE e CRONOLOGIA_PLAYER_SAFE; se houver material GM, derivar uma visão interna separada SEM tratar caminho no Git como controle real de acesso. Diagramas contêm labels legíveis, IDs consistentes e legenda de status comprovado/suspeito/planejado. Não exibir futuro ou segredo ao jogador de modo involuntário. Diagrama sem correspondência no snapshot falha na validação.

## Etapa 6 — Pacotes para campanhas derivadas / solos
Para cada arco que suporte outra perspectiva, criar seed com data-as-of, protagonista alternativo possível, aparições/contatos comprovados, local e tempo, conflitos em andamento, objetivos e conhecimento limitados, informação desconhecida, fatos estáveis de CHR-001 e margens para ramificação. Não escrever automaticamente uma biografia de NPC sem fontes; um possível protagonista pode ter hiatos UNKNOWN. Se recontar a mesma época com novas decisões, derivar branch/chronicle próprio e assinalar divergência, sem sobrescrever a linha de Bartholomeu.

## Etapa 7 — Integração futura ao papel Dramaturgo e validação
Somente após snapshot minimamente auditado, propor versões sucessoras de role-adapter/contrato/schema e ativação COW por manifesto e ciclo quando a governança permitir. O preflight passará a exigir leitura do atlas atual; um novo dossiê deverá indicar quais arcos avançam, quais agentes agem independentemente, reações NPC-NPC, custo do não envolvimento, relógios condicionais, variação de relações, histórico e ponto de chegada M1–M5/2010. A revisão pós-G28 registrará delta do atlas na mesma transação autorizada ou falhará com PENDING_PERSISTENCE — nunca falsificar atualização. Preservar orquestração vigente até ativação efetiva.

## Critérios de qualidade e não aceitação
Não aceitar: apenas resumo literário sem evidências; um grafo que liga todos a Bart sem relações NPC-NPC; NPC com estado imaginado; metaconhecimento divulgado; autorias inventadas; converter planos GM em fato; supor todos os arcos dependentes do PC; grade de cenas obrigatórias; reescrever M1/M2 fechados; iniciar C04; reabrir XP/rolagens; marcar COMPLETE sem varredura. Aceitar PARTIAL auditável com lista de arquivos/lacunas e próxima etapa acionável; não prometer trabalho fora do turno.

## Estrutura de arquivos esperada na execução
- chronicles/CHR-001/narrative-atlas/ATLAS_SNAPSHOT_V001.json (ou versão sucessora)
- chronicles/CHR-001/narrative-atlas/COVERAGE_REPORT_V001.json
- chronicles/CHR-001/narrative-atlas/RECONSTRUCTION_NOTES_V001.md
- chronicles/CHR-001/narrative-atlas/diagrams/RELACOES_BART_PLAYER_SAFE_V001.mmd
- chronicles/CHR-001/narrative-atlas/diagrams/RELACOES_NPC_PLAYER_SAFE_V001.mmd
- chronicles/CHR-001/narrative-atlas/diagrams/TRAMAS_PLAYER_SAFE_V001.mmd
- chronicles/CHR-001/narrative-atlas/diagrams/CRONOLOGIA_PLAYER_SAFE_V001.mmd
- chronicles/CHR-001/narrative-atlas/scenarios/SOLO_REPLAY_INDEX_V001.json
- chronicles/CHR-001/admin/ATLAS_BACKFILL_QUEUE_V002.json (sucessor COW da fila)
Esses arquivos ainda NÃO existem por força desta publicação de planejamento; devem ser produzidos por trabalho fundamentado em fontes no próximo chamado aplicável.

Dependências: runtime/narrative-architecture/NARRATIVE_ATLAS_CONTRACT_V1.md; runtime/narrative-architecture/ATLAS_SNAPSHOT_SCHEMA_V1.json; admin/NEXT_DRAMATURGO_ATLAS_MANDATE_V1.md; admin/ATLAS_BACKFILL_QUEUE_V1.json.