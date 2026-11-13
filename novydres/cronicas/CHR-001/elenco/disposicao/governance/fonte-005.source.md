# NOVYDRES / CHR-001 — Predisposição situacional de NPCs V1
STATUS: IMPLEMENTAÇÃO LOCAL STAGED; não altera cânone, material congelado, G25/G27/G28, LIVE, CYCLE ou cenas fechadas. A autorização do jogador para implementar não abre a C15 nem permite mutação silenciosa do ciclo READY_FOR_NARRATOR.
FONTE: solicitação do jogador de régua -5..+5, humor -2..+2, componente relacional -3..+3, oscilação situacional e custo mínimo de contexto.

## Escopo e autoridade
Aplicável EXCLUSIVAMENTE à CHR-001 após ativação prospectiva segundo ACTIVATION_V1.md. Nunca usar como regra global de NOVYDRES ou como nova mecânica de dados V5. Herda .AGENT.md, .CONTEXTG.md, decisões, proveniência NPC, orquestração e G26/G28. Sem retcon de C01–C14, substituição do dossiê vigente, aprendizado onisciente, compras, XP/FV ou poderes.
A personalidade e interesses determinam COMO o NPC reage; a pontuação não força ação, submissão, agressão, perdão, revelação nem sucesso. Um NPC em +5 pode negar o que viola seus limites; um NPC em -5 pode permanecer cortês.

## Fórmula
H = humor geral [-2,+2]. B = vínculo habitual específico com o interlocutor [-3,+3]. Cada pressão relacional ativa tem delta inteiro -2..+2 e evidência.
R = clamp(B + soma(pressões ativas), -3, +3).
P = H + R, portanto -5..+5. Sem perfil para o NPC, NÃO inventar temperamento ou números canônicos; usar apenas o dossiê/história e interpretação neutra provisória. Sem relação cadastrada, baseline operacional provisória 0 (não é fato de distanciamento afetivo). A diferença de valores é editorial, não medida clínica.
-5..-4: resistência forte; -3..-2: baixa receptividade; -1..+1: moderação; +2..+3: receptividade; +4..+5: receptividade muito alta. São INDÍCIOS de tom e abertura, não resultados mecânicos.

## Gatilhos e duração
1. Não recalcular por turno, frase ou troca de chat. Avaliar somente quando NPC e interlocutor entram em interação social relevante.
2. Humor por JANELA TEMPORAL fundada em tempo diegético (evento de origem + period_key). No mesmo key, reusar humor, inclusive após troca de chat. Data UNKNOWN permanece UNKNOWN; sem nova janela por calendário real ou número de chat.
3. Novo humor: quando existir causa comprovada, CONTEXT com valor -2..+2 e event_id; senão, dois dados independentes d3 e H=d3a-d3b por motor real, com registro de faces e origem. Se RNG auditável não estiver disponível, NEUTRAL_FALLBACK=0 identificado, nunca simular sorteio ou inventar causa.
4. Pressões de interação: somente fatos/atos/efeitos substantivos com source_event_id e impacto qualificado (-1/+1 ordinário, -2/+2 excepcional com justificativa). A mesma fonte não gera pressão duplicada para o mesmo vínculo. Um comentário trivial não exige delta.
5. Pressões podem atravessar cenas SOMENTE se permanecem causalmente pertinentes. Persistir até três pressões ativas por par (mais que isso exige revisão/consolidação fundamentada; nunca descartar silenciosamente). Resolver pressão com evento comprovado; não apagar atrito automaticamente ao amanhecer e não salvar cada micro-oscilação.
6. O vínculo B só muda diante de alteração substantiva da relação, com event_id. Humor não redefine B. A soma é truncada, não acumulada além de R [-3,+3].
7. Se a cena terminar sem alteração duradoura, nenhuma nova versão do estado é necessária. Humor só é persistido se sua continuidade realmente importar para o período seguinte.

## Papéis e epistemologia
DRAMATURGO: caracteriza expressão positiva/negativa, objetivo, limites e vínculos dos NPCs relevantes em camada prospectiva, sem predefinir suas falas ou humores. Perfis iniciais são PROPOSTAS EDITORIAIS ANCORADAS, jamais novos fatos ou conhecimentos.
NARRADOR: carrega somente participantes relevantes, calcula no início da interação, ajusta apenas por causas observáveis, interpreta pelo perfil e demais eventos/rolagens. Não mostra números necessariamente ao jogador. Não pode gerar uma causa para justificar o humor sorteado. Mantém buffer efêmero por cena.
G28: consolida ao fim da cena SOMENTE deltas persistentes no STATE_VNNN copy-on-write, registra origem no episódio, atualiza ponteiro no LIVE sucessor, juntamente com restante do commit atômico e readback. Nenhum commit por batida.
G25/G27: nunca somar P a pool, dificuldade, dados, FV ou sucesso sem uma decisão mecânica separada e expressa. Nenhum NPC ignora seus conhecimentos restritos.
AUDITOR: valida schema, faixas, eventos de suporte, período, ausência de duplicação, prefixo, referência e SHA.

## Antialucinação
Não converter teste social em mudança automática de afeto. Não reconstruir valores retroativamente. Não transformar ausência de registro em hostilidade ou confiança. Não deduzir sexo, saúde, sono, TPM, trauma, segredos ou motivações por resultado numérico. Não resolver conflito de fontes silenciosamente. Em dúvida sobre pressão, preservar UNKNOWN e manter neutralidade do ajuste até evidência; jamais preencher para tornar NPC agradável ou hostil.
