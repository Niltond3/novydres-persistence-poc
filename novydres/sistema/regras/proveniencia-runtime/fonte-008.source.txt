# NOVYDRES — G25 / DEC-CR-015: oferta obrigatória de Pegar Metade antes dos dados

**Status: APROVADA pelo jogador, 2026-11-02. Escopo: CHR-001, modo guiado e crônica futura.**
**Fonte de autorização:** declaração do jogador na conversa de retomada: "sempre que você gerar dificuldade de uma rolagem, se tiver a possibilidade de pegar metade do resultado. E isso for um sucesso, a possibilidade disso ser viável tem que ser exposta ao jogador antes da rolagem acontecer."
**Autoridade:** decisão operacional local, subordinada à governança CANÔNICA/FECHADA e APROVADA/CONGELADA, regras V5 e DEC-CR-013/014. Não altera material canônico e não retroage sobre rolagens antigas.

## G25 — GATE MANDATÓRIO PRÉ-ROLAGEM

1. Antes de GERAR QUALQUER FACE, fixar tipo do teste, pool FINAL de dados (atributo + perícia + modificadores elegíveis), dificuldade/oposição, riscos e circunstâncias. Não fixar dificuldade depois de saber as faces.
2. Calcular `half_successes = floor(pool_final / 2)`. Trata-se de metade da **parada total de dados**, NÃO da quantidade de sucessos que a rolagem produziria.
3. Avaliar elegibilidade do recurso *Take Half / Pegar Metade* de acordo com o regulamento aplicável: não é um direito universal em conflitos/oposições dramáticas ou situações em que a regra exige dados; não substituir teste obrigatório, nem acionar Blood Surge, FV ou efeitos de dados. Dificuldade deve estar fixada; em teste oposto a disponibilidade só pode ser afirmada se a regra específica permitir, sem presumir resultado da oposição.
4. Se e SOMENTE se Take Half for permitido **e** `half_successes >= dificuldade`, o narrador DEVE, **antes de lançar qualquer dado**, apresentar explicitamente ao jogador: parada, dificuldade, cálculo de metade, sucesso garantido sob esse método, limites do efeito e opções **[Pegar Metade] / [Rolar]**. É VETADO lançar os dados antes de o jogador escolher. O jogador pode preferir rolar para buscar margem, críticos ou outros efeitos; o narrador não escolhe por ele.
5. Se o recurso for permitido, mas insuficiente para atingir a dificuldade, ou não permitido pelas circunstâncias, registrar a razão da inaplicabilidade no preflight, sem alegar sucesso garantido. Quando útil, informar brevemente por que não pode ser ofertado.
6. Se o jogador escolhe Take Half, **não gerar RNG**. Persistir escolha, parada, dificuldade, elegibilidade, resultado fixo e efeito com proveniência e readback G19/G24. Não abrir janela de rerrolagem por FV sem dados efetivamente rolados.
7. Se o jogador escolhe Rolar, executar o motor de dados, publicar faces e resultado provisório (sucesso OU falha), e então abrir a **janela de FV após a rolagem e ANTES da consequência**, sujeita à autorização, trilha de FV, elegibilidade e regras vigentes. Nenhum gasto automático. Persistir e fazer readback antes da narrativa evolutiva.
8. Falha em oferecer Take Half quando legal e suficiente = **PRE_ROLL_GATE_VIOLATION**. Se ainda não foram geradas faces, não rolar e oferecer a opção. Se dados já foram gerados, não ocultar, descartar, rerrolar ou inventar uma nova origem; declarar conflito de procedimento, preservar evidências e solicitar a decisão corretiva do jogador antes de resolver o efeito. Não retcon de resultados aceitos.
9. Esta obrigação é um GATE tão forte quanto a janela voluntária de FV: **Take Half antes dos dados; FV depois dos dados, antes da consequência**. Ambos integram preflight e G19 de persistência, sem substituir a agência do jogador.

## Protocolo mínimo do narrador
- `PRE_ROLL`: evento; intenção; tipo; pool_components; pool_final; difficulty/opponent; stakes; eligibility_take_half; half_successes; reason; offer_required.
- `AWAITING_TAKE_HALF_CHOICE` quando `offer_required=true`. **Nenhum sorteio** antes da resposta.
- `TAKE_HALF_RESOLVED` se aceito, sem RNG; ou `ROLL_PRELIMINARY` seguido de `AWAITING_WP_CHOICE` se optou pelos dados.
- `FINAL` e efeitos somente depois dos gates, registro copy-on-write GitHub-first e readback verificado.

**Exemplo matemático:** 7 dados, dificuldade 3: `floor(7/2)=3`. **Se** a situação admitir Take Half, é vitória garantida de 3 sucessos e a escolha deve ser oferecida ANTES da rolagem. Se for teste dramático cuja regra exija rolar, o cálculo 3≥3 NÃO torna Take Half legal.
**Situação específica M2.03.073:** fala seca "Sim" e intimidação sem agressão, solicitadas no turno anterior, **não foram gravadas em novo checkpoint**; nenhuma rolagem válida foi promovida no GitHub. Ao retomar, realizar preflight sob G25 antes de qualquer dado; não declarar resultado, sucesso, resposta do funcionário ou conclusão da troca de roupa aqui.
