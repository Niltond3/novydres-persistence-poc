# NOVYDRES — Auditoria de crédito de ato V1
A01 BLOCK: DEC-CR-021 e TARGET V2 cap 675; gastar ≤ orçamento. Fonte histórica 519 é legado; não tomar antigo XP_REMAINING=349 como limite efetivo depois de normalização.
A02 BLOCK: ACT_ID único, estável, planejamento versionado; no máximo cinco atos remuneráveis por provocação; distinção de quadro/cena/batida, sem fragmentação oportunista.
A03 BLOCK: presença de source_scene_event_id em episódio realmente COMMITTED; não aceitar GM_PLAN ou intenção hipotética como resolução. Recusa/saída válida pode resolver ato, mas precisa ser adjudicada.
A04 BLOCK: resolução não duplicada em ACT_RESOLUTION ledger e crédito anterior; reentrância ou readback não pagar duas vezes.
A05 BLOCK: avaliação e concessão somente por até 10/ato; máximo permitido = cap−spent−credit atual; permitir pagamento parcial se faltar espaço.
A06 BLOCK: creditar NÃO altera XP_TOTAL nem XP_SPENT nem XP_REMAINING; só xp_credit_available. Decisão orçamentária inicial de 675 é transação administrativa separada e já registrada sem prêmio de ato.
A07 BLOCK: compra só por autorização expressa, custo elegível, saldo/limite suficientes; não aplicar XP ao TARGET retroativamente.
A08 BLOCK: M2.03 sem atos planejados e encerrada; prêmio ainda pendente por regra legada, sem retrocriação de cinco atos ou dupla recompensa.
A09 BLOCK: política da transição de sessão não faz crédito/FV automático na abertura; FV segue regra local anterior.
A10 BLOCK: G28 commit em fim de CENA permanece; saldos e resoluções no mesmo commit de cena com readback, exceto transação administrativa específica.
A11 BLOCK: verificar XP_SPENT+XP_CREDIT_AVAILABLE ≤675 e XP_TOTAL−XP_SPENT=XP_REMAINING; não deixar saldo negativo.
A12 BLOCK: se custo equivalente 675 for revisto no futuro, abrir CONFLICT, não modificar cap do alvo ou ledger silenciosamente.
Resultado: PASS com event_id / ACT_ID / origem / SHA e status settled; senão DECLARED_PENDING, sem reivindicar XP concedido.
