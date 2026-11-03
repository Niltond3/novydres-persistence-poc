# NOVYDRES — Gate de auditoria de preparação V1
Aplicar ANTES de publicar dossiê concreto, registrando PASS/FAIL/UNKNOWN e fontes.

A01 BLOCK: HEAD, manifesto, LIVE, HISTORY_INDEX, parent e evento fonte conferidos; nenhum arquivo antigo reescrito.
A02 BLOCK: solicitação é preparar, não iniciar; M2.03 CLOSED e M2.04 NOT_STARTED; dossiê PUBLISHED_NOT_STARTED não altera LIVE.
A03 BLOCK: fatos ESTABLISHED com source_event_id / CANON_SOURCE; NPC_CLAIM, boato ou memória de modelo nunca promovidos a fatos.
A04 BLOCK: conhecimento de NPC requer evento, observação e proveniência; GM_HIDDEN não vaza para jogador/NPC.
A05 BLOCK: atos contêm quadros, quadros contêm cenas POTENCIAIS e batidas opcionais; ao menos duas saídas contingentes por cena, incluindo opção que acomode recusa ou desvio.
A06 BLOCK: nenhuma fala/decisão/compra/FV/sucesso do PJ pré-escrita como fato; futuro Abraço ou crônica 2010 não imposto.
A07 BLOCK: os eventos de relógio/offscreen são condicionais; nenhum XP, FV, RNG, ledger ou evento diegético nesta fase.
A08 BLOCK: ficha TARGET não é adquirida, especializações provisórias limitadas à DEC-CR-019, sem powers futuras.
A09 BLOCK: pistas críticas alcançáveis por mais de uma via; nenhum ponto único de falha ou obrigatoriedade de cena.
A10 BLOCK: handoff somente caminho, SHA e instruções; sem GM_HIDDEN ou título/spoiler. Sigilo por política de apresentação, não bloqueio do acesso ao repo.
A11 BLOCK: COW em novos arquivos, um commit para publicação, expected_sha, compare e readback; sem sobrescrever dossiê anterior.
A12 BLOCK: G28 inalterada; não instalar cadência por quadro/ato/sessão nesta etapa.
A13 BLOCK: sem conflito silencioso: CANON > decisões > eventos > plano. STALE_PLAN_REVIEW quando source checkpoint divergir.
A14 BLOCK: não reutilizar preparation_id/version nem executar plano já publicado como se fosse evento. Testes documentais não são E2E.

Resultado: se todos passarem, promover PUBLISHED_NOT_STARTED; caso contrário manter DRAFT ou BLOCKED_CONFLICT e explicitar falta. A transição SESSION_TRANSITION_V1 só ocorre depois, quando o jogador autorizar.
