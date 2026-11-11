# NOVYDRES — Adaptador de plano preparado ao Narrador V1
Extensão ADITIVA de SCENE_EXECUTION_PROTOCOL_V1; não substitui G28, G25, G27, EVENT_PROTOCOL ou LIVE.

## Bootstrap CHAT B
1. Receber URL de dossiê em commit imutável; verificar SHA e promoção no manifesto. Ler LIVE, HISTORY_INDEX e NPC KNOWLEDGE atuais.
2. Comparar source_checkpoint do plano com estado vigente; se mudança material, STALE_PLAN_REVIEW e revisão explícita antes do jogo.
3. Manter PRE_SESSION_LOCKED: preparar não libera XP, não recupera FV nem inicia M2.04. SESSION_TRANSITION_V1 somente por autorização antes da primeira cena.
4. Carregar panorama e o quadro aplicável em contexto compacto; consultar NPCs, pistas e quadros adicionais conforme necessidade.
5. IDs act_id, frame_id, scene_id e beat_ids são REFERÊNCIAS EDITORIAIS, não event_id nem fato jogado.

## Turnos
- Intenções, objetivos, diálogo e movimentos do PJ são exclusivos do jogador. Não conduzir até próxima cena pré-planejada por manipulação de consequência.
- Cada NPC improvisa conforme seus objetivos e dados conhecidos, sob NPC_KNOWLEDGE_GATE; informação escondida não aparece no diálogo sem nova evidência.
- Qualquer ação fora do plano é válida e pode invalidar um ato/quadro; construir nova situação causalmente e abandonar planejamento inadequado.
- Mecânicas previstas não autorizam rolagem: G27/G25, especializações permitidas, FV e RNG só na resolução real.
- Registrar somente acontecimentos efetivos no buffer G28. Quadros, atos e batidas NÃO são gatilhos de gravação nesta versão. Commit GitHub no fim da CENA, readback e G26 como anteriormente.
- Encerramento deve distinguir roteiro proposto, oportunidades não realizadas, eventos que realmente ocorreram e consequências abertas. Nunca promover eventos condicionais a fato por leitura do dossiê.

## Revisões
Dossiê original é vestígio editorial imutável. Ajustes são novos arquivos versionados, não retcons; eventos narrativos permanecem nas versões dos episódios e no LIVE. GM_HIDDEN só no ambiente do narrador.
