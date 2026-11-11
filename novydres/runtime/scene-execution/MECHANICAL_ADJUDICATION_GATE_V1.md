# NOVYDRES — MECHANICAL ADJUDICATION GATE V1
Status: subordinado a MOTOR_MECANICO_V5_V1_1, G25/DEC-CR-015, G27/DEC-CR-017, DEC-CR-019, ficha efetivamente adquirida e convenção provisória autorizada.

1. Classificar intenção: NO_ROLL | SIMPLE | OPPOSED | EXTENDED | SPECIAL; não rolar ações banais nem transformar hipótese em ação.
2. Identificar origem de cada traço: ALLOCATED_CURRENT, TARGET_PROVISIONAL_PER_DECISION, EXPLICIT_LOCAL_EXCEPTION ou UNAVAILABLE. TARGET não é compra; não ativar poderes futuros.
3. Fixar pool, skill, atributo, modificadores causais, dificuldade/oposição e stakes ANTES dos dados. Nunca pós-ajustar dificuldade para justificar consequência.
4. Especialização: Briga (Agarrar) +1 somente no escopo aprovado DEC-CR-019; outras especializações alvo ainda NÃO autorizadas globalmente. Ofícios/Mecânica Automóveis em M2.03.119 é aplicação histórica de um teste aceito, PENDING_RULE_AUDIT, nunca precedente geral.
5. Calcular half_successes=floor(pool_final/2). Se legal e suficiente, oferecer Pegar Metade ou Rolar e AGUARDAR resposta do jogador. Em oposição dramática, legalidade NÃO decorre só da matemática.
6. Se escolher Pegar Metade, não gerar RNG, não oferecer FV sobre faces inexistentes; usar apenas resultado fixo legal.
7. Caso escolha Rolar, executar método disponível que REALMENTE gere dados e permita auditoria das faces; registrar ferramenta, chamada, faces, data/ordem, resultado, dificuldade, modificadores. Caso ferramenta não disponível, RNG_NOT_VERIFIABLE; NÃO inventar sorteio. Faces históricas apenas transcritas = UNVERIFIED_CHAT_PRESENTATION.
8. Após resultado preliminar, inclusive sucesso, exibir janela opcional de FV com trilha verificada, faces elegíveis e até 3 falhas rerroláveis conforme motor; só descontar mediante autorização explícita e uma vez por roll_id; então finalizar consequência.
9. Conflitos, danos, defesa do NPC, Take Half ou sucesso a custo seguem critérios do motor V5 e G28; não garantir vitória por intenção nem usar ataque focal sem dificuldade adequada.
10. Dano/recuperação, XP, Vantagens e poderes exigem deltas explícitos e auditáveis; não creditar 30 XP totais por recompensa de provocação.

## Resultado do gate
NO_ROLL_VALID | PRE_ROLL_OFFER_REQUIRED | AWAITING_PLAYER_CHOICE | AWAITING_VERIFIABLE_RNG | AWAITING_WP_CHOICE | FINAL_RESOLVED | RULE_AUDIT_PENDING.
Sem confirmação necessária, não completar o passo seguinte em silêncio. O registro técnico histórico CHRONICLE_STORE_V0_2 não está auditado como ledger COMMITTED.
