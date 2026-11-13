# NOVYDRES · ADR-001 · aceite explícito de risco e simplificação de gates (2026-11-13)

**Autoridade:** ordem expressa do proprietário do projeto, nesta conversa: declarar D04 e D05 PASS com base nas provas existentes e verificar/simplificar o excesso dos gates D06/D07. Esta decisão é **aceite de risco residual**, não declaração de fatos técnicos não demonstrados. Não altera CANÔNICO/FECHADO, APROVADO/CONGELADO, a crônica operacional em master nem libera E02/E03.

## Decisões executivas

- **D04_PASS — aceite do proprietário.** 438/438 origens custodiadas; estado C45, XP/FV, autoridade, conhecimento por 38 atores e 47 registros, 44 tramas, mecânica provisória e 27 lotes do índice parcial foram validados por provas específicas. Continua NÃO PROVADA a cobertura semântica exaustiva de acontecimentos duradouros fora do índice histórico; não inventar eventos, rolagens, transcrições ou ledger universal.
- **D05_PASS — aceite do proprietário.** 399/399 origens mapeadas; 285 fontes inertes e 114 fontes recuperáveis pelo Git; 121 referências rastreadas em nove grupos. Duas trocas de política G26/G28 são autorizadas por DEC-18, sem comprovar runtime real. Os outros **119 vereditos continuam BLOCKED/behavioral unproven**: a aprovação de fase aceita esse risco e **não os converte em EQUIVALENT_VERIFIED**. A árvore permanece candidata.
- **D06 — gate enxuto por função e risco.** Única verificação integrada do HEAD integral: 1.029 origens, catálogo/ownership, estado/sigilo, testes negativos críticos, transação Git/CAS/readback, ZERO LEGADO; reutilizar provas válidas de C e D. Não exigir revisão individual de cada uma das 121 referências, ledger universal nem repetir testes determinísticos sem alteração.
- **D07 — revisão independente identificável, não 121 auditorias.** Confrontar riscos críticos, divergências editoriais, concessões de NPC, preparação/prosa, conhecimento, segredos, progressão e persistência no uso pretendido. Um parecer humano/agente independente identificável, com limitações claras; scripts/CI do próprio implementador não satisfazem sozinhos a independência. Repetir apenas testes afetados.

## Limites não dispensados

As lacunas são fatos documentados, não defeitos artificialmente corrigidos. D06 pode aprovar sua **integridade técnica** pelo fluxo efetivo; D07 permanece pendente até revisão independente identificável. A exigência de integridade histórica e funcional pré-cutover do ADR-001 §9 continua aplicável como risco a reconciliar ou decidir expressamente no próprio gate E; **D04/D05 PASS não é autorização de promoção**, não certifica qualidade narrativa futura, nem transforma preparação em fato jogado. Não escolher silenciosamente CONFLICT-001/002/003B.

Referência: ADR-001 DEC-16/17/18/20/21/22/23/24/26/27; escopo operacional condicionado ao E02 expressamente aprovado. Preserve os registros históricos de resultados negativos e SHAs anteriores.
