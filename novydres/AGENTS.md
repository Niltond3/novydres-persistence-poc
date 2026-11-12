# NOVYDRES — entrada candidata do ADR-001 (não operacional)

Este arquivo é somente um candidato nas fases C/D. O runtime corrente permanece em `master`, com seus ciclos, manifestos e contratos vigentes. **Não iniciar cenas, promover fontes, atribuir XP/FV ou fazer cutover a partir daqui.**

Para uma consulta de migração autorizada, fixe um commit exato da branch `design/subject-oriented-migration`, leia `CONTEXT.md` desse mesmo commit e então `catalogo.json`. Resolva `subject_id` por igualdade exata. Confirme `index.md` e blobs do mesmo snapshot antes de consultar apenas os arquivos pertinentes. Falha de ID/autoridade exige `NOT_FOUND` ou bloqueio explícito: nada de rotas legadas, busca aproximada ou memórias de outros chats.

Os identificadores e metadados derivados não autorizam divulgar material oculto. O acesso do agente não é conhecimento do jogador, protagonista ou NPC. DEC-16/17/18/20/21/23–27 do ADR-001 orientam este desenho; aprovação operacional e cutover continuam pendentes.
