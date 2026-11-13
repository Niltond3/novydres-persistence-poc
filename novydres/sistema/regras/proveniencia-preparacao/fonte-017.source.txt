# NOVYDRES — Validação semântica e cruzada do dossiê V1
Complementa JSON Schema; executável parcialmente por inspeção JS, parcialmente por auditoria narrativa humana/LLM. Não prometer prova automática de coerência semântica profunda.

## Verificações determinísticas
S01 — IDs de atos, quadros, cenas, batidas, NPCs, pistas, clocks, ramos e fallback são únicos em seu namespace; duplicidade BLOCK.
S02 — Cada clue_id de cena existe no catálogo de pistas; cada route_id de pista é único; pistas críticas possuem pelo menos duas vias distintas, não somente duas descrições idênticas.
S03 — Fontes estruturais do dossiê incluem MANIFEST, LIVE e HISTORY_INDEX do checkpoint com SHA; fonte CANON_SOURCE verificada no repositorio antes da publicação.
S04 — ESTABLISHED com CONFIRMED_EVENT precisa source_event_id; CANON_SOURCE precisa fonte de autoridade. PREPARED e CONDITIONAL não são EVENT_ID técnico.
S05 — Conhecimento NPC status KNOWN de fatos históricos exige EVENT_ID de origem; UNKNOWN não pode ter event_id inventado; CLAIMED/SUSPECTED não podem ser aplicados como verdade de mundo.
S06 — O source_checkpoint aponta para o último EVENT_ID e LIVE_sha verificáveis no momento da preparação; commit de publicação é descendente e não torna o plano obsoleto por si só. Antes de executar, comparar LIVE_sha/evento, não apenas HEAD.
S07 — Handoff retornado é somente prompt seguro; não conter texto dos campos GM_HIDDEN do dossiê, nomes de NPCs novos, títulos/objetivos de quadros nem pistas secretas; caminho neutro.
S08 — Não existem no plano objetos de resultado real ou de compra, rolagem, FV, Abraço/2010 consumado: estado do dossiê PUBLISHED_NOT_STARTED não altera estado do jogo.
S09 — Compilação do plano não exige que o primeiro quadro/cena ocorra; recusa/desvio/fracasso são alternativas válidas. Vários desenlaces não podem depender exclusivamente do mesmo teste/pista.
S10 — Nenhum metadado do plano é usado como gatilho de gravação por quadro/ato; G28 por CENA permanece intacta até decisão posterior.
S11 — Se o plano cita episódio histórico, confirmar referência e correção mais recente, conhecimento restrito e status entre FACT/CLAIM/UNKNOWN.
S12 — Publicação COW: nova versão, SHA parent, atômica, compare e readback, sem alterar antigos CANONICO/FECHADO e APPROVED/FROZEN.

## Resultados
PASS / FAIL / UNKNOWN com explicação e fonte. UNKNOWN em pré-condição decisiva bloqueia promoção; outras lacunas editoriais devem ser marcadas como UNKNOWN e tratadas sem invenção. Auditoria pré-publicação pode ser confirmada somente por chamada real de ferramenta. Regressões sintéticas não garantem êxito em narrativa real.
