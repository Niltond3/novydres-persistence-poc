# NOVYDRES — Economia de crédito de XP por ato resolvido V1
STATUS: DEC-CR-021 aprovada pelo jogador em 2026-11-03; somente CHR-001 criação guiada e futuras provocações planejadas. Fonte hierárquica DECISIONS_STATE_V10 e TARGET_SHEET_V2_APPROVED. Este contrato não altera o cânone nem a cadência G28.

## 1 — Semântica imutável
- BUDGET_TOTAL / XP_TOTAL = teto pré-aprovado do alvo, 675 XP equivalentes locais na TARGET V2, sujeito à auditoria final de custos. A quantidade de provocações NUNCA altera o orçamento total. Antes era envelope 519: snapshot histórico, substituído agora por normalização explícita do teto aprovado; NENHUM XP foi conquistado ao normalizar.
- XP_SPENT = 170, compras já aprovadas. XP_REMAINING = 675−170 = 505, capacidade do orçamento não consumida, NÃO liberada automaticamente para gastos.
- XP_CREDIT_AVAILABLE = 20, limite operacional ainda disponível para autorização de compras. Não é XP extra além dos 675. Seu uso consome orçamento restante.
- XP_UNLOCK_CAPACITY = max(0, 675 − XP_SPENT − XP_CREDIT_AVAILABLE) = 485, capacidade ainda não liberada por atos ou por auditoria histórica autorizada.
- XP_TOTAL deve ser sempre igual ao orçamento aprovado; alterar o alvo posteriormente exige nova decisão e auditoria, nunca reescrever compras ou histórico.

## 2 — Fórmula de liberação
Para ato elegível com ACT_ID único e fonte de resolução confirmada:
 nominal = 10
 efetivo = min(nominal, max(0, BUDGET_TOTAL − XP_SPENT − XP_CREDIT_AVAILABLE))
 XP_CREDIT_AVAILABLE_novo = XP_CREDIT_AVAILABLE_antigo + efetivo
 XP_TOTAL_novo = XP_TOTAL_antigo = 675
 XP_SPENT_novo = XP_SPENT_antigo
 XP_REMAINING_novo = XP_REMAINING_antigo
A aplicação deve percorrer atos resolvidos não pagos uma única vez, em ordem de seus eventos. Se XP_SPENT + XP_CREDIT_AVAILABLE >= BUDGET_TOTAL, efetivo=0. Na última liberação parcial pode ser menor que 10. Status do ato = SETTLED_CREDIT / SETTLED_ZERO_AT_CAP; a mesma resolução não pode gerar crédito novamente.

## 3 — O que é ato elegível
O Dramaturgo prepara como padrão de 1 a 5 atos SUBSTANTIVOS, cada qual com pergunta dramática distinta, situação e stakes próprios. Cinco atos plenamente resolvidos têm potencial até 50 de crédito, condicionado ao teto. Não produzir atos extras artificiais por dividir batidas/cenas/quadro ou pela quantidade de mensagens.
Preparar/abrir/citar ato NÃO libera 10. Resolver significa fechar legitimamente a questão dramática: sucesso, fracasso, recusa, fuga ou desvio que a solucione, sem obrigar o PJ a seguir o plano. Ato ignorado, abandonado mas ainda aberto, não resolvido, ou interrompido antes de resolução = 0 até comprovação. Ato EMERGENTE pode substituir ato planejado não resolvido com justificativa explicitada; não contar os dois e não exceder cinco créditos de atos por provocação sem nova autorização editorial.
Cada resolução: preparation_id, episode_id, act_id, source_scene_event_id validado, ACT_RESOLUTION_ID único, resolution_type, adjudication, event chronology e crédito efetivo. Duplicação no ledger ou histórico impede segundo crédito.

## 4 — Compras
Somente após pedido e aprovação expressa do jogador. Elegibilidade e custo conforme sistema V5/local vigentes; custo <= XP_CREDIT_AVAILABLE e custo <= XP_REMAINING e nenhuma compra futura de poder/benefício antecipado.
Novo SPENT = velho SPENT + custo
Novo CREDIT_AVAILABLE = velho CREDIT_AVAILABLE − custo
Novo REMAINING = BUDGET_TOTAL − novo SPENT
Invariant: SPENT+CREDIT_AVAILABLE não muda em uma compra; jamais negativo, jamais acima de 675.
Não aplicar compra porque há crédito: oferta não é autorização.

## 5 — Quando gravar
Ato resolvido só se torna crédito canônico ao consolidar evento real. Usar buffer da cena, registro de resolução e batch G28 de fechamento da cena, sem commits extras por batida/ato. No fechamento de provocação reconciliar atos sem prêmio anterior; ler G26 em falha. G28 permanece por CENA, NÃO por quadro, ato ou sessão.
Um eventual crédito histórico do M2.03 continua pendente e sujeito à regra LEGADA curta/média/longa na avaliação própria; não inventar atos retroativamente para multiplicar prêmio. Nunca conceder duas vezes a mesma conclusão.

## 6 — Exemplos simulados, NÃO aplicados
Situação atual após normalização do cap: TOTAL=675, SPENT=170, REMAINING=505, CREDIT=20; ainda não desbloqueado=485.
Futuros 5 atos efetivamente resolvidos e válidos: nominal 50, efetivo 50 -> CREDIT=70, TOTAL=675, REMAINING=505, SPENT=170.
Exemplo próximo ao teto: SPENT=660, CREDIT=5, faltam 10 não liberados; resolver 2 atos concede 10 no primeiro e 0 no segundo; CREDIT=15; TOTAL=675.
No teto: SPENT=675, CREDIT=0 -> quaisquer novos atos =0. Também SPENT=600, CREDIT=75 -> quaisquer novos atos =0, porque todos os 675 já estão gastos ou liberados.
Compra simulada 15 com saldo de crédito 70: SPENT=185, CREDIT=55, REMAINING=490, TOTAL=675; não houve experiência extra.
