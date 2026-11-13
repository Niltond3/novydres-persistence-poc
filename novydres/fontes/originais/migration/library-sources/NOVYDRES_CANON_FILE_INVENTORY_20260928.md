# NOVYDRES — Inventário de fontes, versões e destinos

**Data da auditoria:** 2026-09-28  
**Escopo:** arquivos que alimentam o cânone, registros de decisão, fontes visuais e material de bootstrap. Este inventário não cria nem altera decisões de lore, regras, mapa ou POIs.

## Como usar

O nome e o número de versão de um arquivo não bastam para concluir que ele é a autoridade atual. Compare o conteúdo, o frontmatter e o estado operacional posterior registrado no handoff. Preserve as categorias CANÔNICO / FECHADO, APROVADO / CONGELADO, PENDENTE, SUPERADO e REJEITADO / DESCARTADO sem harmonizar divergências por conta própria.

Os IDs abaixo são os Library file IDs retornados na auditoria. Os caminhos são caminhos da Library, não caminhos já instalados no diretório NOVYDRES.

## Projects e localização do material

- [Organizar RPG](https://chatgpt.com/g/g-p-6a06368b67608191b4f78c1c254f4762/project) contém boa parte dos chats editoriais, de canon e de mapa.
- [RPG Map](https://chatgpt.com/g/g-p-6aa767ecddb08191b9ca813ba8696f16/project) contém os chats por POI, testes visuais, revisões de mapa e o julgamento v2.
- A aba Fontes estava vazia nos dois Projects durante a auditoria. Os vereditos estão nas conversas; os bytes dos documentos e imagens estão na Library.
- O julgamento visual mais recente está em [v2 Pois](https://chatgpt.com/g/g-p-6aa767ecddb08191b9ca813ba8696f16/c/6ab526af-3a9c-83e9-af47-c4182e7a5195). Use-o para estado de POI; use os arquivos abaixo para obter o conteúdo.

## Destinos no bootstrap

| Destino relativo | Responsabilidade |
|---|---|
| 00_SOURCE/ | Handoff histórico, este inventário, adendos de auditoria e instruções de bootstrap. |
| 01_GOVERNANCE/ | Autoridade global, contratos editoriais, dependências, glossário e política de conflitos. |
| 10_CHAPTERS/01_WORLD_CANON/ | Introdução, história e cronologia. |
| 10_CHAPTERS/02_POLITICS_DOMAIN_FACTIONS/ | Facções, Concílio, leis, status, prestações, fé e ordens com função política. |
| 10_CHAPTERS/03_SYSTEM_MECHANICS/ | Regras transversais e contratos de regras standalone. |
| 10_CHAPTERS/04_CHARACTER_CREATION_A_K/ | Baseline e módulos de criação A–K, com ledgers e dependências. |
| 10_CHAPTERS/05_NPCS_POWER_SCALE/ | Escala de poder, decisões de NPC e perfis. |
| 10_CHAPTERS/07_PROVOCATIONS_MARCOS/ | Workstream L e conteúdo de Provocações/Experiências. |
| 10_CHAPTERS/08_CARTOGRAPHY_GEOGRAPHY/ | Geografia e conteúdo espacial do Atlas. |
| 10_CHAPTERS/09_MOBILITY_INFRASTRUCTURE/ | Vias, ferrovia, metrô, portos e aeroporto. |
| 10_CHAPTERS/10_MASTER_MAP/ | Estado e integração do Master Map. |
| 10_CHAPTERS/11_POI_REGISTRY/ | Índice de todos os 32 POIs, estados e referências aos assets. |
| 10_CHAPTERS/12_VISUAL_LANGUAGE/ | Gramática gráfica e anti-patterns visuais. |
| 10_CHAPTERS/13_PRODUCTION_PIPELINE/ | GIMP, XCF, PNG, versionamento e distinção entre implementado e planejado. |
| 20_ASSETS/maps/ | Master Map, referências cartográficas, mapas e tiles derivados. |
| 20_ASSETS/approved/ | Cópias de assets aprovados, somente após vínculo inequívoco a um veredito. |
| 20_ASSETS/generated/ | Saídas e alternativas ainda não aprovadas. |
| 20_ASSETS/references/ | Imagens usadas como referência de estilo ou comparação. |
| 90_ARCHIVE/ | Versões superadas, relatórios de migração e saídas descartadas, preservados sem exclusão. |

## 1. Handoff e instrução de bootstrap

| Arquivo | ID / localização | Função e destino |
|---|---|---|
| NOVYDRES_MASTER_HANDOFF_V1(1).md | libfile_7db5a2f2fef0819188003b2dbe200159; Library /NOVYDRES/ | Cópia duplicada do snapshot histórico global. O texto foi comparado integralmente com NOVYDRES_MASTER_HANDOFF_V1.md (libfile_ec374ce9c92c8191a719aa40fd300375) e é idêntico. Preserve o item da Library; não excluir. |
| NOVYDRES_PROJECT_BOOTSTRAP_PROMPT_WEB_V2.txt | libfile_a253b3a859088191a674105dadea8f28; Library /NOVYDRES/ | Instrução operacional para scaffold e migração. Não é canon. Destino 00_SOURCE/. Determina a raiz absoluta e proíbe usar outro caminho se ela estiver inacessível. |
| NOVYDRES_MASTER_HANDOFF_AUDIT_ADDENDUM_2026-09-28.md | artefato desta auditoria | Overlay append-only para corrigir localizações, estados e lacunas. Destino 00_SOURCE/. Não substitui nem reescreve V1. |
| NOVYDRES_CANON_FILE_INVENTORY_2026-09-28.md | artefato desta auditoria | Índice de fontes, funções, versões e destinos. Destino 00_SOURCE/. |

O chat “Consolidação do handoff” apresenta NOVYDRES_MASTER_HANDOFF_V1.md como arquivo final e o descreve como tendo 2.008 linhas. A comparação integral das duas cópias da Library encontrou texto idêntico e tamanho de 82.651 bytes em ambas; a extração da Library informa 2.007 linhas para cada uma. Prefira a cópia sem sufixo como fonte selecionada para `00_SOURCE/NOVYDRES_MASTER_HANDOFF_V1.md`, por corresponder ao nome do arquivo final no chat. Preserve a cópia `(1)` como duplicata histórica; a diferença de uma linha entre as contagens não indica divergência de conteúdo.

## 2. Governança editorial e contratos globais

| Arquivo | ID / localização | Função → destino |
|---|---|---|
| novydres_editorial_governance_v1_0.md | libfile_66e227ced93081919abce9c4fc02df09; /Organizar RPG/ | Autoridade e responsabilidades editoriais globais → 01_GOVERNANCE/PROJECT_RULES.md. |
| novydres_editorial_map_v0_9_4.json | libfile_a914395df4f08191802aa193a16d1dca; raiz | Mapa de capítulos, layout e fluxo editorial; guia de produção, não manuscrito → 01_GOVERNANCE/SOURCE_OF_TRUTH.md e referências dos capítulos. O filename diz v0.9.4, mas o campo interno schema_version é 0.9.3; registrar a discrepância. |
| novydres_format_contract_v0_3_1.md | libfile_62fd3ca783e4819190cc8e29993dcd81; /Organizar RPG/ | Formato editorial para os textos → 01_GOVERNANCE/PROJECT_RULES.md. |
| novydres_format_contract_decisions_v0_1.md | libfile_cd911111dd548191b04b4cb69c691e53; raiz | Ledger de decisões do contrato de formato → 01_GOVERNANCE/DECISIONS.md. |
| novydres_editorial_prohibitions_contract_v0_1.md | libfile_d8a0ed8313c48191bd876953ec8efc37; /Organizar RPG/ | Restrições editoriais retroativas → 01_GOVERNANCE/PROJECT_RULES.md. |
| novydres_prompt_reuse_contract_v0_1.md | libfile_c6dc9b3263088191b8576aa52eb2de49; /Organizar RPG/ | Reuso e preservação de prompts → 12_VISUAL_LANGUAGE/SOURCES.md e 13_PRODUCTION_PIPELINE/SOURCES.md. |
| novydres_standalone_rules_contract_v0_1.md | libfile_0dc522cd1fdc8191a33090f3d1f2e067; raiz | Regras necessárias para apresentação standalone → 03_SYSTEM_MECHANICS/SOURCES.md. |
| novydres_standalone_rules_decisions_v0_1.md | libfile_b847dfe0758081919179be951c927ee1; raiz | Decisões do contrato standalone → 03_SYSTEM_MECHANICS/DECISIONS.md. |
| novydres_play_guidance_contract_v0_1.md | libfile_9b78d6bbf9288191b8bfae8b476b9390; raiz | Play guidance e relação entre texto e uso em jogo → 03_SYSTEM_MECHANICS/SOURCES.md. |
| novydres_play_guidance_decisions_v0_1.md | libfile_b1dc3f24a2dc819199620d1a48b6382d; raiz | Ledger de play guidance → 03_SYSTEM_MECHANICS/DECISIONS.md. |
| novydres_revelation_architecture_contract_v0_1.md | libfile_b204ce808f348191b1175c9b779f0db3; raiz | Proteção de revelações e organização do acesso a informação → 01_WORLD_CANON/SOURCES.md e 06_CAMPAIGN_ARCHITECTURE/SOURCES.md. |
| novydres_revelation_architecture_decisions_v0_1.md | libfile_d4704f35da4481919e9d384ae07ab71b; raiz | Ledger do contrato de revelação → 01_GOVERNANCE/DECISIONS.md, com referências aos capítulos afetados. |
| novydres_retroactive_dependency_living_memory_policy_v0_1.md | libfile_601c16a36b008191bee2e27d3ab6ba14; raiz | Política para mudanças retroativas e dependências → 01_GOVERNANCE/PROJECT_RULES.md. |

As cópias da raiz e de /Organizar RPG dos contratos e decisões de Play Guidance foram comparadas e são textualmente idênticas. Use uma cópia no workspace; mantenha o ID da raiz como referência selecionada.

## 3. Capítulos de mundo, política e religião

| Arquivo | ID selecionado | Função → destino |
|---|---|---|
| 01_introducao_v0_2_1.md | libfile_abf00ea37f7481919643baa3920f1844; /Organizar RPG/ | Premissa e introdução player-safe → 01_WORLD_CANON/CANON.md ou arquivo de capítulo equivalente. |
| 02_historia_e_cronologia_v0_2_2.md | libfile_ec951e6d88888191ac890bf516e0aac3; /Organizar RPG/ | História e cronologia → 01_WORLD_CANON/CANON.md ou arquivo de capítulo equivalente. |
| 03_atlas_de_novydres_v0_2_2.md | libfile_21986feddd988191a7c0cee1c8d5804f; /Organizar RPG/ | Atlas textual, raions, locais e canon de POIs → 08_CARTOGRAPHY_GEOGRAPHY/CANON.md e 11_POI_REGISTRY/POI_INDEX.md, com uma única cópia canônica e referências cruzadas. |
| 04_faccoes_politica_conflitos_v0_2.md | libfile_542a7d6de4dc819186c211fcdc0c9d8e; raiz | Facções, política e conflitos → 02_POLITICS_DOMAIN_FACTIONS/CANON.md. |
| 05_concilio_leis_status_prestacoes_v0_2_2.md | libfile_0073a534fd888191a8b89f1466d77aec; raiz | Concílio, leis, status e prestações → 02_POLITICS_DOMAIN_FACTIONS/CANON.md; apontar regras de uso para 03_SYSTEM_MECHANICS. |
| 06_fe_heresia_e_ordem_v0_2_1.md | libfile_60b12e94aa308191897e77ebbbca8a36; raiz | Fé, heresia e ordem → 02_POLITICS_DOMAIN_FACTIONS/CANON.md, com referências de contexto a 01_WORLD_CANON. |

As cópias de 01, 02 e 03 na raiz e em /Organizar RPG foram comparadas integralmente e são textualmente idênticas. As versões listadas acima em /Organizar RPG são a cópia escolhida para o bootstrap porque ficam junto do Project editorial. O capítulo 05 v0.2.2 está de fato disponível na Library; a cópia localizada é a da raiz.

O frontmatter dos capítulos 01–06 apresenta status candidate. O handoff registra fechamento operacional posterior para o cânone editorial. Preserve as duas informações; não altere o frontmatter durante a migração.

## 4. NPCs e escala de poder

| Arquivo | ID / localização | Função → destino |
|---|---|---|
| novydres_npc_power_scale_citywide_v0_1_1.md | libfile_a6978d6b2ea881919265de0c399fd791; raiz | Escala de poder dos NPCs e aplicação da revisão corretiva → 05_NPCS_POWER_SCALE/CANON.md. Frontmatter: candidate_for_senior_editor_revalidation. |
| novydres_npc_power_scale_citywide_decisions_v0_1.md | libfile_d0f2cc93ff808191b0e7d131cff04fc4; raiz | Ledger de 106 decisões → 05_NPCS_POWER_SCALE/DECISIONS.md. |
| novydres_npc_power_scale_citywide_corrective_patch_report_v0_1.md | libfile_89530d48d1488191987787be1a5fd60b; raiz | Proveniência da correção da escala → 05_NPCS_POWER_SCALE/SOURCES.md; não é a escala em si. |
| iskander_yasupov_v0_9(2).md | libfile_dd23e68e87f481918e8e35c55015f20f; raiz | Perfil de Iskander → 05_NPCS_POWER_SCALE. Conteúdo comparado: a cópia é textualmente idêntica às cópias v0.9 na raiz e em 07_personagens. |
| madame_zoya_v0_9(2).md | libfile_f0e1c49d91b8819184b29f6240d9c9ef; raiz | Perfil de Madame Zoya → 05_NPCS_POWER_SCALE. É a cópia mais nova localizada; tem uma alteração textual em relação às cópias v0.9 anteriores, sem bump de versão. |
| novydres_chapter_07_iskander_zoya_decision_ledger_v0_1(1).md | libfile_afc654b09bfc8191b2bb32eedbfe4e6a; raiz | Ledger de decisões dos dois perfis → 05_NPCS_POWER_SCALE/DECISIONS.md. |

No perfil de Zoya, a cópia mais nova substitui a referência anterior a um truth-home por uma formulação que deixa o antecedente deliberadamente fora daquela narrativa. Isso é uma diferença de arquivo observada; o inventário não a transforma em nova decisão editorial.

## 5. Criação de personagem A–K e Workstream L

| Arquivo | ID / localização | Função → destino |
|---|---|---|
| novydres_character_creation_core_v5_baseline_v0_1.md | libfile_7266d897da18819190a1d64595fd249b; raiz | Baseline V5 da criação e regras-base → 04_CHARACTER_CREATION_A_K/CANON.md. |
| novydres_character_creation_specialist_a_v5_baseline_research_v0_1.md | libfile_32f1c3f3991c8191ae7e8233b5ffa8ea; raiz | Pesquisa de referência do especialista A → SOURCES.md; pesquisa não substitui decisões. |
| novydres_character_creation_specialist_a_decisions_v0_1.md | libfile_21c681b940e88191b0a8539ad5871f79; raiz | Decisões do especialista A → 04_CHARACTER_CREATION_A_K/DECISIONS.md. |
| novydres_character_creation_power_envelope_v0_1_1.md | libfile_ca68db3398108191806b2c51fa832079; raiz | Power Envelope corrigido → CANON.md e referências de 03_SYSTEM_MECHANICS. |
| novydres_character_creation_specialist_b_decisions_v0_1_1.md | libfile_79c9c8e09f208191966c63c4ffa0e6eb; raiz | Ledger B → DECISIONS.md. |
| novydres_character_creation_social_territorial_political_integration_v0_1_1.md | libfile_9822327fb3dc819188ee91aeec84736f; raiz | Integração social, territorial e política → CANON.md, com referências a 02_POLITICS_DOMAIN_FACTIONS. |
| novydres_character_creation_specialist_c_decisions_v0_1_1.md | libfile_6d9fe7e82eac81919b0d806254f644ff; raiz | Ledger C → DECISIONS.md. |
| novydres_character_creation_d1_played_history_core_v0_1.md | libfile_e844d53e8b2c819185c57b321155286a; raiz | Núcleo de Played History → CANON.md. |
| novydres_character_creation_d1_played_history_core_decisions_v0_1.md | libfile_65f4477422c48191abe0d6a01eeb265f; raiz | Ledger D1 → DECISIONS.md. |
| novydres_character_creation_d2_played_history_finalization_integration_v0_1.md | libfile_e8cb57f5601081919ee764b5f25fd161; raiz | Integração final de Played History → CANON.md. |
| novydres_character_creation_d2_played_history_finalization_integration_decisions_v0_1.md | libfile_663e9c760f9c8191bdfbbb1797189ef2; raiz | Ledger D2 → DECISIONS.md. |
| novydres_character_creation_e_memory_relationships_temporal_persistence_v0_1_1.md | libfile_ef2e2dbcfea081919dd6c59af8e0b49d; raiz | Memória, relações e persistência temporal → CANON.md. |
| novydres_character_creation_e_memory_relationships_temporal_persistence_decisions_v0_1_1.md | libfile_89648458f7248191b2cf00c175bc00d3; raiz | Ledger E → DECISIONS.md. |
| novydres_character_creation_f_history_chronology_revelation_integration_v0_1.md | libfile_6465da6fd4ec819180afe9bfe298c1e3; raiz | Integração de história, cronologia e revelação → CANON.md; respeitar o contrato de revelação. |
| novydres_character_creation_f_history_chronology_revelation_decisions_v0_1.md | libfile_1ca2acb3caf88191a031128092f682bf; raiz | Ledger F → DECISIONS.md. |
| novydres_character_creation_g_quick_creation_mode_v0_1_1.md | libfile_536b239696b08191a561d3ac875b9f9d; raiz | Procedimento de criação rápida → CANON.md. |
| novydres_character_creation_g_quick_creation_mode_decisions_v0_1_1.md | libfile_bdff165642b08191a34176da8b861351; raiz | Ledger G → DECISIONS.md. |
| novydres_character_creation_h_guided_pc_integration_v0_1.md | libfile_99c1fd52842c8191af69a897d8eeafa6; raiz | Integração da criação guiada para PCs → CANON.md. |
| novydres_character_creation_h_guided_pc_integration_decisions_v0_1_1.md | libfile_184e689bd8288191a799302258d89b49; raiz | Ledger H → DECISIONS.md. |
| novydres_character_creation_i_npc_application_depth_profiles_v0_1.md | libfile_0e292f2816408191af6c015a17066556; raiz | Profundidade de resolução de perfis NPC → CANON.md e referência a 05_NPCS_POWER_SCALE. |
| novydres_character_creation_i_npc_application_depth_profiles_decisions_v0_1.md | libfile_5d35534ffe608191999eea0d65094071; raiz | Ledger I → DECISIONS.md. |
| novydres_character_creation_j1_coterie_canonical_baseline_research_v0_1.md | libfile_71350f94c2f08191a3ee148602ba0325; raiz | Pesquisa de baseline para Coterie → SOURCES.md; não usar como decisão final isolada. |
| novydres_character_creation_j2_coterie_creation_architecture_v0_1.md | libfile_3d69dea4fc288191b676ad8cddcaebf0; raiz | Arquitetura J2 de criação de Coterie → CANON.md. |
| novydres_character_creation_j2_coterie_creation_architecture_decisions_v0_1.md | libfile_e82db59e0af4819186c91ab83f0aebc9; raiz | Ledger J2 → DECISIONS.md. |
| novydres_character_creation_k_final_integration_v0_1.md | libfile_dcff55e86b248191a1edb7a1decccdee; raiz | Integração final A–K → CANON.md. O frontmatter ainda diz candidate_for_senior_editor_closure; o handoff registra fechamento operacional posterior. |
| novydres_character_creation_k_final_integration_decisions_v0_1.md | libfile_4d6aaa48d3ec8191a77ecd207f0fa0ca; raiz | Ledger K → DECISIONS.md. |
| novydres_character_creation_architecture_decision_inventory_v0_1_3.md | libfile_597ddc0c4040819192d3f04230f68e82; raiz | Índice de decisões A–K → SOURCES.md/DECISIONS.md como mapa, não como substituto dos ledgers locais. |
| novydres_character_creation_novydres_architecture_audit_v0_1_4.md | libfile_386b3ffb3c7081918da3b9db1ca45b0b; raiz | Auditoria transversal da arquitetura → SOURCES.md; conservar o estado candidate do arquivo e o fechamento operacional posterior registrados no handoff. |
| novydres_character_creation_l_guided_content_handoff_v0_1(1).md | libfile_770a0e11c6f48191ab3a5bf6a1b18445; raiz | Handoff ativo do Workstream L → 07_PROVOCATIONS_MARCOS/STATE.md e SOURCES.md. É handoff de contexto, não patch de arquitetura. |

As cópias com sufixo (1) de G, ledger G, Power Envelope, ledger B, integração social/territorial, ledger C, inventário A–K e auditoria A–K foram comparadas e são textualmente idênticas às cópias sem sufixo. Prefira a cópia sem sufixo no workspace. Não foi localizado, no recorte auditado da Library, um corpus final completo de Provocações/Experiências além do handoff L.

## 6. Cartografia, Master Map e ativos visuais

| Arquivo | ID / localização | Função e estado |
|---|---|---|
| MasterMap.png | libfile_3c5c251ef98c8191944ecaddf6d9ae35; /RPG Map/; modificado em 2026-09-22 | Export raster chamado MasterMap. Destino de referência 20_ASSETS/maps/ e estado em 10_MASTER_MAP/STATE.md. É candidato visual, não fonte editável comprovada. |
| novydres-tiles.zip | libfile_1e588c3c9b4881919bb99d52b60f410e; /Organizar RPG/; modificado em 2026-09-08 | Pacote derivado de tiles. Destino 40_OUTPUTS/tiles/ ou 90_ARCHIVE; tiles derivam do Master e não redefinem geografia. |
| Gramática Visual Canônica de Novydres(1).png | libfile_8b331e2369b48191b12004d701f66fdc; /RPG Map/ | Referência visual candidata → 20_ASSETS/references/. O handoff e os vereditos textuais continuam sendo a autoridade; não foi possível identificar por metadados qual prancha foi a referência anexada em cada chat. |
| Legenda Cartográfica Visual de Novydres.png | libfile_1371b5c233108191a687b01a2e38a352; /RPG Map/ | Referência de legenda candidata → 20_ASSETS/references/ e 09_MOBILITY_INFRASTRUCTURE/SOURCES.md. |
| Guia Visual Cartográfico de Novydres.png | libfile_ba5a8ade17608191b85a5036b9e16a21; /RPG Map/ | Guia visual candidato → 20_ASSETS/references/ e 12_VISUAL_LANGUAGE/SOURCES.md. |

### PNGs com aprovação final encontrada na conversa v2

O vínculo abaixo usa o título do arquivo, a data de criação na Library e o veredito visível em v2 Pois. São os assets selecionados para cópia em 20_ASSETS/approved/; preserve também o arquivo original e registre a origem no POI_INDEX.

| POI | Arquivo | Library ID | Estado |
|---:|---|---|---|
| 01 | Arranha-céu monumental em gravura marrom-avermelhada.png | libfile_34219b1b60e88191a96cc05f6d216923 | Aprovado e congelado em v2. |
| 02 | Palácio Imperial em Gravura Borgonha.png | libfile_9f8d594d6230819189e5d89323028a7e | Aprovado e congelado após correção em v2. |
| 03 | Gravura Monocromática do Grande Banco Neoclássico.png | libfile_184cd9259534819195140f905f46d230 | Aprovado e congelado em v2. |
| 08 | Residência Diplomática Britânica em Linogravura.png | libfile_c40c8861389c8191936e73d5db4b86d7 | Aprovado e congelado em v2. |
| 10 | Catedral Ortodoxa em Gravura Bordô.png | libfile_b99156a8718081919b24b9b2c944939c | Aprovado e congelado em v2. |
| 11 | Universidade Teológica Imperial em Gravura.png | libfile_519c66396f288191b79365d7fccdc824 | Aprovado e congelado após correção em v2. |
| 18 | Gravura Vermelha de Complexo Aeroportuário.png | libfile_1bbab104bc6c81919cc328b9dbdc50a4 | Aprovado e congelado em v2; substitui o estado pendente do handoff anterior. |
| 19 | Porto Ártico Industrial em Gelo Quebrado.png | libfile_a196298024e08191b01bc9dff0d14de1 | Aprovado e congelado em v2; substitui o estado pendente do handoff anterior. |
| 22 | Bairro Histórico em Gravura Borgonha.png | libfile_251e6a0ba72c8191a90f547e352bac34 | Aprovado e congelado após correção em v2. |
| 26 | Avenida Judicial Neoclássica em Oxblood.png | libfile_a0b7c64e87188191b562b49c86f6fc61 | Aprovado e congelado após refação em v2. |
| 32 | Sinagoga Monumental em Gravura Burgundi.png | libfile_96a1ccdc6fbc8191a31468cf95fc6e6b | Aprovado e congelado em v2. |

### Pendências visuais e arquivos que não devem entrar como aprovados

| POI | Arquivo ou registro | Estado e destino |
|---:|---|---|
| 23 | Complexo Industrial de Abate em Gravura Ocre.png — libfile_8a0d44a956a88191a200a7f83818288c | A conversa termina em APROVADO COM CORREÇÃO e pede elementos litúrgicos integrados. Guardar em 20_ASSETS/generated/; não tratar como congelado. |
| 24 | Jardim de Carne Harker | Há prompt atualizado no fluxo v2, mas não foi localizado veredito final. Não há arquivo final associado com segurança nesta auditoria. |
| 25 | Farol Vintage em Gravura Borgonha.png — libfile_d41c6a5625f08191990794a0bdbcc093 | Candidato antigo. Sem aprovação final localizada; manter em generated/ ou referências. |
| 31 | Mesquita Imperial em Gravura Borgonha.png — libfile_cffacbd4ed588191a352bd210ef166cc | Candidato antigo. Sem aprovação final localizada; manter em generated/ ou referências. |
| 04–07, 09, 12–17, 20–21 | Saídas PNG associadas aos chats individuais | O handoff anterior marca esses POIs como aprovados/congelados. Ainda falta registrar um vínculo inequívoco arquivo-ID ↔ julgamento final para todos; não escolher entre imagens de nome semelhante por inferência. Preservar os estados e completar o vínculo durante bootstrap/QA. |
| 27–30 | Variantes visuais antigas | Descartadas do fluxo visual, mas o Atlas ainda contém o conteúdo textual. Manter a separação entre canon textual e estado visual. |

Não foi localizado XCF, PSD, ORA ou KRA do Master Map na lista auditada da Library. O handoff deve continuar marcando como não confirmado qual arquivo editável abrir no GIMP. Não usar MasterMap.png como substituto silencioso de um master editável.

## 7. Cópias, versões anteriores e histórico

As cópias de 01, 02 e 03 localizadas na raiz e em /Organizar RPG são textualmente idênticas; as cópias de Iskander também são idênticas. As cópias de Play Guidance citadas acima são idênticas. Os pares de Character Creation indicados na seção 5 também são idênticos.

Madame Zoya é diferente: a cópia mais recente em Library é madame_zoya_v0_9(2).md e tem uma frase alterada em relação ao arquivo v0.9 de 07_personagens. Sem bump de versão semântica, registre-a como cópia mais recente com divergência textual; não apague a cópia anterior.

Relatórios de migração, patch reports, prompts de subagente, variantes antigas do mapa editorial, arquivos com nomes genéricos/UUID e renders alternativos são material de proveniência ou histórico. Não entram no contexto carregado por padrão. Classifique-os em SOURCES.md ou 90_ARCHIVE e preserve somente quando forem necessários para rastrear uma decisão.

## 8. Ausências confirmadas nesta auditoria

- Não foi encontrada cópia final do arquivo editável do Master Map; apenas MasterMap.png foi identificado pelo nome.
- Não foi encontrado um POI Registry separado na Library; o inventário de 32 POIs está no Atlas e no handoff. POI_INDEX.md deve ser derivado no destino 11_POI_REGISTRY, sem apagar itens 27–30.
- Não foi encontrado um decisions_log.md separado para o pipeline visual.
- Não foi encontrado corpus completo de Workstream L além do handoff L v0.1.
- O nome do Project não implica que existam arquivos na aba Fontes; nos dois Projects auditados, ela estava vazia.
- O destino absoluto do bootstrap não estava acessível na máquina desta sessão. Por isso, nenhuma árvore foi criada neste ambiente.

## 9. Estado de conclusão e pendências da auditoria — 2026-09-28

Este inventário organiza os arquivos canônicos e auxiliares localizados, suas funções, relações de versão e destinos propostos no scaffold. Ele não fecha lacunas sem evidência nem declara concluída a migração física.

### Confirmado no material já auditado

- A cópia sem sufixo **NOVYDRES_MASTER_HANDOFF_V1.md** é a fonte escolhida para 00_SOURCE/; a cópia (1) permanece preservada e é textualmente idêntica.
- O adendo e este inventário funcionam como overlay de estado e mapa de fontes. Ambos devem acompanhar o handoff no 00_SOURCE/; nenhum deles reescreve o V1.
- Os estados registrados para os POIs 01, 02, 03, 08, 10, 11, 18, 19, 22, 26 e 32 são aprovados/congelados. POI 23 permanece aprovado com correção; POI 24 tem prompt atualizado sem veredito final localizado; não há aprovação posterior localizada para 25 e 31.
- Os vínculos de asset para 11 POIs aprovados estão descritos na seção 6. O restante exige vínculo por evidência direta entre Library ID e veredito; não escolher renders por semelhança de nome.

### Para fechar

1. Retomar a leitura direta dos chats, quando houver uma sessão Web autenticada funcional, para verificar o desfecho da correção do POI 23, os vereditos de 24, 25 e 31, e os vínculos exatos dos assets congelados ainda sem ID associado (04–07, 09, 12–17 e 20–21). A sessão de continuação de 28/09 terminou em erro OAuthCallback; não houve nova leitura desses chats.
2. Identificar a fonte editável vigente do Master Map, com caminho ou ID e versão/hash, e confirmar qual arquivo raster representa sua exportação. MasterMap.png sozinho não permite isso.
3. Localizar ou confirmar a ausência do corpus integral de Provocações/Experiências do Workstream L e seus registros de decisão, além de documentos canônicos que ainda não constem deste inventário.
4. Confirmar se o handoff, este inventário e o adendo devem ser adicionados como Fontes do Project NOVYDRES no ambiente Desktop. A aba Fontes estava vazia na observação autenticada anterior; nenhum upload foi feito nesta auditoria.
5. Executar o scaffold exclusivamente em /home/nilton_neto/Documentos/Backup/Notas/Personal Stuffs/RPG stuffs/NOVYDRES, numa sessão que consiga acessar esse caminho. Até essa execução, o bootstrap físico permanece pendente; não criar uma árvore alternativa.

As pendências acima são de verificação, proveniência ou operação. Não autorizam alterar material CANÔNICO/FECHADO ou APROVADO/CONGELADO, nem resolver os conflitos preservados no handoff.