# NOVYDRES — Gate de preparação V2: extensão de PREPARATION_AUDIT_V1
Todos os A01–A14 V1 permanecem. Incluir:
XP01 BLOCK: carregar DEC-CR-021, TARGET V2, XP_ACT_CREDIT_POLICY_V1, LIVE e manifesto válidos. Teto aprovado 675 não se eleva por sessões.
XP02 BLOCK: schema V2, 1–5 atos substantivos; cada act_id único, xp_credit_nominal=10, xp_credit_status=PLANNED_NOT_GRANTED, sem divisões artificiais.
XP03 BLOCK: planned_act_count == acts.length e planned_credit_potential == 10 * acts.length.
XP04 BLOCK: grant_automatically_on_preparation=false e reward_is_new_xp=false; preparar NÃO atualiza LIVE ou crédito.
XP05 BLOCK: M2.03 CLOSED e sem atos recriados retroativamente; crédito histórico pendente segue avaliação legada separada.
XP06 BLOCK: atos resolvidos por recusa, fuga, sucesso ou fracasso reais podem qualificar; nunca garantir 50 porque cinco atos foram escritos.
XP07 BLOCK: G28 permanece por CENA; registros de ato não criam commits por ato, quadro ou batida.
XP08 BLOCK: handoff pelo formato V2 sem spoilers; fixture sintético nunca é jogo.
Falha -> BLOCKED_CONFLICT ou PENDING_PERSISTENCE. Auditoria e readback antes de promover PUBLISHED_NOT_STARTED.
