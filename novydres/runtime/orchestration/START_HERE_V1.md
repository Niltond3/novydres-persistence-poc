# NOVYDRES / CHR-001 — Entrada única para chats limpos (V1)
**Acesse primeiro este documento apenas quando o handoff não estiver disponível.** O handoff normal carrega ID de ciclo e commit e economiza buscas. Repositório Niltond3/novydres-persistence-poc, master.

1. Verifique HEAD master. Liste APENAS novydres/chronicles/CHR-001/orchestration/ e escolha o CYCLE_VNNNN.json numericamente maior (não escolha MANIFEST antigo por ordem lexical). Confira seq, predecessor, último event_id e blob SHAs das referências. Se falhar, BLOQUEIE.
2. Abra ORCHESTRATION_CONTRACT_V1 e o role-adapter do papel indicado pelo ciclo; o manifesto de ativação é MANIFEST_V30 ou sucessor normativo válido.
3. READY_FOR_DRAMATURGO: carregar plano atual, LIVE, últimas cenas e somente fontes históricas necessárias; produzir PLAN_REVISED/PLAN_REVALIDATED e novo ciclo no GitHub. READY_FOR_NARRATOR: executar UMA cena a partir de preparação validada, sem escolher ações do protagonista; ao fechar fazer G28 + ciclo e handoff. PROVOCATION_CLOSURE_PENDING/BLOCKED: não narrar.
4. A cada fase, um commit atômico COW, readback, então emitir o prompt mínimo. Se falhou, NÃO dizer "salvo" nem transferir para chat limpo.
5. Não revisar M2.04 na implantação deste contrato: o ciclo inaugural está READY_FOR_DRAMATURGO e C10 permanece bloqueada até aquela revisão futura.

Contratos de papéis: novydres/runtime/orchestration/DRAMATURGO_ROLE_V1.md e NARRADOR_ROLE_V1.md.
Templates: HANDOFF_DRAMATURGO_TO_NARRADOR_V1.md e HANDOFF_NARRADOR_TO_DRAMATURGO_V1.md.
