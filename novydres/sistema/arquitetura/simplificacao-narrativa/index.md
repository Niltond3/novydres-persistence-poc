---
subject_id: architecture-narrative-simplification
kind: architecture-plan
owner: sistema/arquitetura
scope: NOVYDRES_GLOBAL_DESIGN_WITH_CHR001_LOCAL_DECISIONS
status: EMENDA_CANDIDATA_NAO_OPERACIONAL
visibility: PLAYER_SAFE
sources:
  - commit: 3cc958c110012c61c2d56b2868643174a7eed388
    path: novydres/sistema/arquitetura/adr/001-subject-oriented.md
  - commit: c9fcfc0c558cd17d58ec8c8272da3ed70182ff37
    scope: operational-reference-only
related_ids: [ADR-001, CHR-001]
allowed_roles: [design, dramaturgo, narrador, auditor, jogador]
validation: links-and-traceability-documents-only
---
# Simplificação narrativa — Emenda de desenho do ADR-001

- [Decisões confirmadas e limites da emenda — ADR-001 §11](../adr/001-subject-oriented.md#11-revisão-do-harness-narrativo).
- [Contexto, evidências, escopo e situação das fases](contexto.md).
- [Desenho, destinos, matriz de intervenções e verificação](desenho.md).
- [Plano integral do ADR e backlog único A01–E03](../plano-integral/index.md).

Os documentos deste assunto compartilham o `subject_id` acima. As fontes e os snapshots públicos estão no contexto; a entrevista desta conversa fundamenta as decisões, sem equivaler a evento ficcional ou autorização operacional. Este índice não é entrada de narração, não duplica estado e não promove o candidato. Gate de B: consultar seu [registro existente](../fase-b/gate-e-readback.json), que esta emenda não substitui.

DEC-20 orienta esta revisão e todo o ADR: retirar limites excessivos quando as escolhas aceitas já bastarem; levar casos ainda ambíguos à entrevista Grill with Docs, com recomendação e consequência concreta. Registrar cortes, simplificações e substituições na matriz existente e nas tarefas afetadas, sem criar outra camada de controle.

O antigo recorte de dez tarefas foi substituído pelo backlog integral. Este assunto conserva a análise narrativa; não mantém uma fila concorrente de implementação.
