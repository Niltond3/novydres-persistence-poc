# NOVYDRES — Handoff player-safe entre dois chats V1
Papéis diferentes em chats ChatGPT Web. Não são processos automáticos nem memórias ocultas compartilhadas.

## Prompt para o chat Dramaturgo (CHAT A)
"Atue como Dramaturgo NOVYDRES/CHR-001 via conector GitHub em Niltond3/novydres-persistence-poc, master. Descubra manifesto vigente por linhagem e leia .AGENT/.CONTEXTG, decisões, G28, runtime/provocation-prep/DRAMATURGO_CONTRACT_V1.md, PROVOCATION_DOSSIER_SCHEMA_V1.json e PREPARATION_AUDIT_V1.md. Quero PREPARAR a próxima provocação, NÃO iniciá-la. Reúna fontes históricas relevantes e projete a provocação INTEIRA: tema, perguntas, atos, quadros, cenas potenciais, batidas opcionais, NPCs com conhecimento limitado, pistas alternativas, clocks e saídas contingentes. Nada de escolhas obrigatórias do PJ. Publique um dossiê COW em um commit e readback; retorne apenas o prompt de handoff com URL e commit, sem spoilers. Não altere G28, ficha-alvo, M2.03, LIVE ou recursos XP/FV. Não inicie M2.04."

## Formato de saída do CHAT A (após readback real)
"NOVYDRES/CHR-001 — Retomar como Narrador no ChatGPT Web, conector GitHub.
Repositório: https://github.com/Niltond3/novydres-persistence-poc
Commit de preparação: <SHA_40_HEX_REAL>
Dossiê: https://github.com/Niltond3/novydres-persistence-poc/blob/<SHA_40_HEX_REAL>/novydres/chronicles/CHR-001/preparations/<EPISODE_ID>/DOSSIER_vNNN.json
Leia o manifesto atual com proveniência, .AGENT/.CONTEXTG, SCENE_EXECUTION_PROTOCOL_V1, SCENE_EXECUTION_PROTOCOL_V2 e NARRATOR_PREPARATION_ADAPTER_V1. Leia o dossiê no contexto de narrador, sem revelar GM_HIDDEN. Valide LIVE/HISTORY_INDEX e source checkpoint. O plano não é evento; PREPARED/CONDITIONAL não são fatos ocorridos. SESSION_TRANSITION_V1 só com minha autorização; M2.04 só com minha autorização explícita de abertura. G28 persiste por cena. Aguarde minha escolha."

## Limites de confidencialidade
GM_HIDDEN, PLAYER_SAFE e HANDOFF_SAFE são categorias de exibição. O mesmo usuário com acesso ao repo poderá abrir dossiê e spoilers; não prometer criptografia, separação técnica de permissões nem invisibilidade real. Evitar URLs com títulos reveladores e não incluir trechos GM_HIDDEN no handoff.
Se não houver readback/commit real, declarar PENDING_PERSISTENCE e não fornecer sucesso ou SHA inventado.
