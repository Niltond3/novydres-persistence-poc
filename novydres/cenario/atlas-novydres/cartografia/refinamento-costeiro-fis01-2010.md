---
document_id: MW-010-FIS01-REFINEMENT-2010
subject_id: world-atlas-novydres
reference_year: 2010
workflow_status: OPEN_PENDING_OWNER_REVIEW
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED_PROPOSAL_NOT_CONFIRMED
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
source_parent_commit: a1d6d900b4e823a53933408649581b110fafdfaf
---

# MW-010 — Variante refinada FIS-01 (proposta)

**Inventário substantivo do ponto:** (1) configuração de grande baía abrigada: diretriz aprovada; (2) refinamento efetivo de seu contorno: candidato publicado, aguardando aprovação/rejeição/ressalvas da versão; (3) 3 ilhas (duas internas, uma externa) somente hipótese revisável; número/contornos não canonizados.

## Artefato

Geometria ativa única: `macrogeometria-litoral-baia-ilhas-2010.proposal.json`, atualizada de 26 para 44 vértices. Histórico anterior está no commit `a1d6d900b4e823a53933408649581b110fafdfaf`/blob `0aefaa2161aa9b728fd03a4ec3d0daf522a81b4d`. As mudanças refinam cantos e reentrâncias sem inventar detalhes cadastrais, batimetria, EPSG ou limite municipal. Baía sintética anterior `1851.250 km²`, variante `1881.995 km²`; abertura sintética da boca `18.749 km`. Números de validação, não fatos oficiais.

Dependências de costa atualizadas em relevo, hidrografia e Ermos (vínculos de SHA, foz/segmento costeiro e limites relativos). Ilhas e geometria independente de cursos, relevo e Ermos permanecem iguais. O único visualizador ativo `visualizador-fisico-2010.html` tem três modos de comparação (novo, antigo e sobreposição), desenho SVG 2D grafite e azul dessaturado, sem fontes geométricas concorrentes: a linha antiga embutida é exclusivamente referência histórica da comparação.

## Validação e limitações

Pré-validação topológica interativa antes da escrita: costa e anel da baía simples; ilhas no corpo hídrico declarado; relevo e Ermos no lado terrestre; canais e foz nos vértices/segmentos referenciados; classes e quadro sintético mantidos. **Validação Node completa e visual em navegador ainda não confirmadas nesta nota**, não são declaradas PASS. Reexecutar os validadores `validar-macrogeometria-litoral.mjs`, `validar-macrorelevo.mjs`, `validar-macrohidrografia.mjs`, `validar-macroermos.mjs` e `validar-integracao-fisica.mjs` sobre a versão efetiva.

## Decisão requerida e gate

O proprietário deve examinar a variante MW-010 no comparador e decidir o contorno como `APROVADO`, `APROVADO_COM_RESSALVAS` ou `REJEITADO`. A eventual aprovação do contorno da proposta **não** canoniza automaticamente coordenadas. Corrigir ressalvas e validar versão final antes de fechamento. **Sem handoff e sem avanço** enquanto o ponto FIS-01 permanecer aberto, conforme `guide.md`.
