# NOVYDRES — Plano detalhado de implementação do Dramaturgo V1
Data: 2026-11-03. Escopo: arquitetura de PREPARAÇÃO, não geração de M2.04, não narrativa.
Estado de entrada confirmado: master 5bbab80266789a49449f0dd7c5d8706027dd187b; manifesto V16; M2.03.126 CLOSED; M2.04 NOT_STARTED.

## 1. Objetivo
A preparação improvisada durante o turno narrativo compete com continuidade, conhecimento dos NPCs, G25/G27, FV/XP e persistência. Separar um chat Dramaturgo (preparação completa auditada) e um chat Narrador (execução contingente).
Resultado: dossiê versionado com premissa, perguntas dramáticas, atos, quadros, cenas potenciais, batidas opcionais, NPCs, pistas, relógios, alternativas, consequências condicionais e handoff somente player-safe.

## 2. Precedência e fontes
Conferir .AGENT.md, .CONTEXTG.md, MIG-DEC-002, GITHUB_PRIMARY_CONTRACT_V4, DECISIONS_STATE_V9, EVENT_PROTOCOL_V5, G28/DEC-CR-020, SCENE_EXECUTION_PROTOCOL_V1, SESSION_TRANSITION_V1, LIVE_v012, HISTORY_INDEX_v012, NPC_KNOWLEDGE_PROVENANCE_V2, OPEN_THREADS_V2; buscar originais somente por IDs e correções pertinentes. Checkpoints históricos no .CONTEXTG não são vigentes.
CANÔNICO/FECHADO e APROVADO/CONGELADO são intocáveis. TARGET_SHEET_V2_APPROVED é meta, NÃO ficha adquirida. Conflitos -> CONFLICT, não ajuste silencioso.

## 3. Escopo e exclusões
INCLUIR: contrato Dramaturgo, schema de dossiê, template sintético, auditoria, regressões, bootstrap e handoff, adaptador do Narrador, protocolo V2 aditivo, manifesto V17, todos em novos caminhos copy-on-write.
EXCLUIR: preparar concretamente M2.04 sem solicitação específica de produção de sessão; iniciar M2.04, conferir crédito XP, curar FV, rolar dados, retcon, editar material fechado, mudar frequência de commits G28. Persistência por quadro/ato/sessão exigirá aprovação separada.
Planejamento é META-ARTEFATO, não evento diegético; dossiê pronto pode receber commit administrativo único, mas execução permanece G28 por CENA.

## 4. Modelo dramático
Provocação = experiência completa e perguntas dramáticas, não sequência garantida. Ato = função maior; quadro = ambiente/situação; cena = interação contínua; batida = virada opcional sem gravação independente.
Preparar atos (proposta, não número rígido), quadros e cenas como nós com gatilhos alternativos, saídas não exclusivas e contingências. Todo ato considera recusa, abandono, fracasso, sucesso, rota lateral. Exemplos de fala de NPC são possibilidades editoriais, não falas já proferidas.
NPCs com objetivos próprios, atitudes na ausência de PJ, recursos, segredos e conhecimento restrito; alegações históricas precisam de fonte. Pistas essenciais devem ter múltiplas rotas. A duração, local exato, diálogo e resultados não são garantidos. Questões morais abrem opções, não controlam Bartholomeu.
Usar organização de módulos de aventura como referência formal somente se fonte autorizada for verificada, sem copiar texto protegido nem importar fatos externos.

## 5. Epistemologia
ESTABLISHED = fato previamente confirmado e citado no histórico. PREPARED = oportunidade/novo conteúdo editorial, ainda não evento ocorrido, GM_PLAN. CONDITIONAL = alternativa futura condicionada. UNKNOWN = sem prova; não preencher por invenção. NPC_CLAIM não vira ESTABLISHED. GM_HIDDEN é marca de não divulgação textual, NÃO controle de acesso criptográfico: proprietário do repo pode abrir o arquivo.

## 6. Ciclo futuro: Chat A, preparação
1. Usuário ordena PREPARAR provocação, sem iniciar; confirmar HEAD/manifesto/LIVE/index.
2. Registrar source_checkpoint com commit, evento, estado, caminhos/SHAs e fonte; localizar relações relevantes sem ler toda a biblioteca.
3. Criar dossiê conforme PROVOCATION_DOSSIER_SCHEMA_V1: tema, situações, perguntas, atos/quadros/cenas/batidas, NPCs, pistas, clocks e contingências, sem resultado do PJ pré-escrito.
4. Verificar governança, gates de NPC, dados de ficha adquirida versus alvo e divergências históricas.
5. Validar PREPARATION_AUDIT_V1 e regressões; BLOCKED_CONFLICT impede promoção.
6. Publicar novo arquivo em chronicles/CHR-001/preparations/<episode_id>/DOSSIER_vNNN.json; um commit COW GitHub + compare + readback, com manifesto sucessor. Não alterar LIVE na preparação.
7. Entregar SOMENTE prompt player-safe com link do dossiê e commit, sem spoilers.

## 7. Ciclo futuro: Chat B, execução
Narrador verifica SHA imutável, depois manifesto corrente e checkpoint real; drift -> STALE_PLAN_REVIEW sem retcon silencioso. PRE_SESSION_LOCKED até autorização de transição de sessão. SESSION_TRANSITION_V1 governa crédito/FV/compras separadamente; só então primeira cena se jogador autorizar.
Carregar primeiro panorama e ficha do quadro vigente, consultar NPCs e fontes detalhadas sob demanda. Se o PJ divergir, descartar ou reordenar nós; nunca forçar roteiro. G25/G27 e NPC knowledge gate operam em tempo real. G28 continua um commit por CENA concluída, não por batida/quadro.

## 8. Critérios de aceite
- Nenhuma modificação de G28, TARGET, LIVE, HISTORY_INDEX, episódio fechado, estado histórico, NPC provenance e decisões aprovadas.
- Manifesto V17 é novo arquivo e aponta contratos; PREPARATION_LAYER_AVAILABLE_NOT_A_SESSION.
- Dois chats documentados; handoff não revela GM_HIDDEN.
- Schema exige plano inteiro estruturado, procedência, opções/contingências e hierarquia.
- Regressões: sem NPC onisciente, sem ação forçada, sem XP/FV, sem RNG, sem cena futura transformada em fato, sem spoiler no handoff, sem referência de checkpoint stale.
- Um commit de implantação com paths ADDED, verificação de HEAD e readback.
- Testes de contrato e esquema não equivalem a demonstração narrativa E2E, que fica pendente.

## 9. Trabalhos futuros isolados
A mudança de cadência para quadro/ato/provocação NÃO faz parte do Dramaturgo V1. Proposta separada deve simular recuperação do buffer e ser aprovada antes de alterar DEC-CR-020/G28.
