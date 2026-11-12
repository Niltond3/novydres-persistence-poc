# NOVYDRES — Bootstrap de Dramaturgo e Narrador no ChatGPT Web V2
É uma EXTENSÃO ao CHATGPT_WEB_BOOTSTRAP_V1, que permanece como referência histórica. Não substitui G28 nem a transição de sessão.

## 1. Preparar uma sessão — chat A
Abrir um chat NOVO e colar o prompt em runtime/provocation-prep/HANDOFF_AND_SECRECY_V1.md, seção "Prompt para o chat Dramaturgo". Exigir leitura dos documentos, criação do dossiê integral, checks e commit GitHub. O Dramaturgo retorna apenas link + SHA + prompt para o segundo chat. Nenhum dos documentos atuais contém dossiê narrativo real M2.04.

## 2. Executar sessão preparada — chat B
Novo chat ChatGPT Web com conector GitHub, usar o handoff confirmado do chat A. Narrador carrega manifesto vigente, .AGENT/.CONTEXTG, LIVE, HISTORY_INDEX, SCENE_EXECUTION_PROTOCOL_V1, SCENE_EXECUTION_PROTOCOL_V2 e NARRATOR_PREPARATION_ADAPTER_V1. Conferir source checkpoint e gate do NPC.
O conteúdo integral do dossiê deve ser legível ao narrador, mas suas partes GM_HIDDEN NÃO devem ser exibidas ao usuário por padrão. Carregar panorama e quadro relevante antes de gerar cena.
M2.04 continua NOT_STARTED até decisão explícita, inclusive após criação do dossiê. SESSION_TRANSITION_V1 controla XP/FV. G28 controla gravação de cena.

## 3. Se não houver dossiê
A camada pode estar instalada sem sessão preparada; não inventar arquivo, link, conteúdo ou commit. Informar PREPARATION_NOT_YET_CREATED. Não tentar usar fixture sintético de runtime como provocação.
