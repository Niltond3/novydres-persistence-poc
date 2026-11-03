# NOVYDRES — SESSION TRANSITION V1
Status: procedimento PROSPECTIVO, NÃO EXECUTADO nesta implantação.
Aplicável apenas quando jogador autorizar iniciar próxima provocação/sessão após M2.03 CLOSED. Abertura M2.04 proibida até completar gates.

## Pré-condições
- Confirmar HEAD, manifesto e LIVE atual; M2.03 CLOSED e M2.04 NOT_STARTED; sem transição já aplicada.
- Cada provocação = sessão na regra local, mas nova conversa não abre sessão; verificar session_id/recovery_id e idempotência.
- Fonte vigente de crédito: diário legado da criação guiada; curta 10, intermediária até 20, longa multipartes até 30, avaliadas por extensão/relevância. CREDIT é limite de uso de XP orçado, não prêmio que aumenta XP_TOTAL.
- Classificar M2.03 longa e propor até 30 de crédito para decisão/validação explícita; não assumir automaticamente lançamento de 30 e não premiar duas vezes.

## Sequência
1. Administrar fechamento anterior como fato: M2.03 permanece imutável e fechado.
2. Propor crédito variável M2.03 baseado na regra, verificar duplicidade e registrar EVENT_ID único; delta xp_credit_available somente após avaliação/aceite. XP_TOTAL=519, XP_SPENT=170, XP_REMAINING=349 até compras expressas.
3. Registrar abertura de sessão real SESSION_ID novo. Recuperar APENAS dano superficial de FV em min(superficial, max(Autocontrole, Determinação)); no estado provisório 5 superficial, atributos 3 e 3 -> recupera 3, passa a 2 superficial/4 disponíveis de máximo6. Não curar agravado sem regra específica. Exceções de cliffhanger devem ser evidenciadas, nunca presumidas.
4. Permitir oportunidade de compra de XP e calcular custo/eligibilidade, aguardando autorização expressa; não aplicar automaticamente atributos almejados ou especializações.
5. Gravar transição administrativa em novas versões state, LIVE, HISTORY_INDEX, manifesto, eventos, com lote único GitHub e readback; nunca editar v012/v018/V14.
6. Apenas depois apresentar primeira provocação M2.04 em evento próprio quando jogador autorizar a abertura; seguir G28 para a cena narrativa.

## Exemplos não aplicados
ANTES: XP 519/170/349 crédito20; FV max6 superficial5 agravado0 livre1.
SIMULAÇÃO se jogador aprovar crédito30: crédito50, XP totais/gasto/restante iguais. SIMULAÇÃO se abrir sessão real sem cliffhanger: FV max6 superficial2 agravado0 livre4.
Isto não é uma mudança da ficha nem um lançamento efetivo.

## Falha / conflito
Se M2.04 já estiver aberta, créditos duplicados, FV com trilha divergente, autoridade conflitante ou uma sessão anterior não conferida, STOP/CONFLICT, nada automático. Nunca curar por criar chat limpo ou fechar uma cena.
