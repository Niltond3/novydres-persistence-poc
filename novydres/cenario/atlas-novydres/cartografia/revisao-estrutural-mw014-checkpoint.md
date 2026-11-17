---
document_id: MW014-STRUCTURAL-REVISION-REJECTION-CHECKPOINT
work_unit: MW-014
subject_id: world-atlas-novydres
status: OPEN_AWAITING_OWNER_GEOMETRY_REVIEW
owner_decision_on_e_local_revision: REJECTED
canonical_status: NOT_APPROVED
source_master_sha: 5931f306c1e547d169d6e4bbb69114d616a6011c
source_mw014_sha: aa0a5794edff80cc508a6439b1ce4dbef3ee6ca4
mw015_coastal_decision_sha: f0aef8324108cefbcb2cb0a4b9d2ce168e90f423
---

# MW-014 — checkpoint sem fechamento

O proprietário reprovou integralmente a tentativa de redistribuição local da E que apenas alongava manchas de ocupação, sem alterar os dez grandes polígonos de Ermo. Reprovação expressa em 17/11/2026. Não interpretar essa tentativa como candidata aprovada, nem como solução da proporção Ermo/habitável, isolamento do núcleo 1 ou ausência de tecido territorial no sul.

## Reabertura da dependência física

A restrição anterior de preservar incondicionalmente a geometria FIS-04 foi reconhecida como equivocada para responder a uma crítica estrutural. Reabrir a discussão dos limites de Ermo como **dependência geométrica da MW-014**, sem abrir nova unidade e sem reescrever o cânone. A MW-010 continua como única costa candidata corrente. Não alterar costa, ilhas, relevo, rios, afluentes, lagoas, bacias, termas ou nove âncoras aprovadas sem outra deliberação.

## Estudo exploratório local F (não publicado como geometria do GitHub)

Foi elaborado no chat um estudo candidato F que usa esqueletização geométrica dos dez envelopes de Ermo do modelo anterior, propõe uma rede conectada de corredores de largura significativamente menor e recalcula classes de ocupação sobre o território liberado. Medição local: união de Ermos anterior 2588.48 km², proposta F 1276.99 km² (-50.67%), sobre continente de 8167.74 km². As áreas não são resultados oficialmente aprovados.

A simulação conserva as dez camadas de referência físicas (exceto a própria geometria dos Ermos), as nove âncoras e a costa MW-010. Verificações locais: geometria válida, classes funcionais sem sobreposição de área com Ermos ou águas. A visualização comparativa e os GeoJSON candidatos foram gerados na conversa, porém **NÃO foram escritos na árvore GitHub** e não possuem status de fonte da verdade. Não reutilizar como aprovados. Artefatos locais em análise têm SHA-256:
- HTML: 14d2d809fdb5afdf72e7b3986a4d036359f0a2f6f138797757b94dd743d28a31
- PNG: 0c0f4a3ff456562243fba19479621664cf4de8e2b88e17cdf2105277756bb24b
- Ermo GeoJSON: 245f73776b8bbfdd78408a2a49e756d167e01a7d6d6a3aa8d5b20bf5b0edbd94
- Ocupação GeoJSON: 910034b8d353fffec6014499ad083e2bbc6b8adcddc5c93da9e4ddadbc366e33

**Pendência A:** deliberação visual expressa sobre a revisão dos Ermos FIS-04, em seguida sobre a distribuição funcional dependente; se aprovada, publicar dados estruturados com proveniência e validar topologia e leitura remota antes de fechar MW-014. Não gerar handoff de unidade seguinte, não canonizar nem avançar para raions/transporte.