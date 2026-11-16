---
document_id: MW-010-FIS01-REFINEMENT-2010
subject_id: world-atlas-novydres
reference_year: 2010
workflow_status: CLOSED_FOR_THIS_SCOPE
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED_PROPOSAL_NOT_CONFIRMED
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
source_parent_commit: a1d6d900b4e823a53933408649581b110fafdfaf
final_owner_decision_on: 2026-11-16
final_owner_decision: APROVADO
work_unit: MW-010
---

# MW-010 — Fechamento FIS-01: litoral refinado de Novydres (2010)

## Decisões substantivas (inventário e deliberações completas)

1. Grande baía naturalmente protegida e continente predominante: **diretriz preservada de FIS-01/MW-009**, sem legitimar área, distância ou latitude oficiais.
2. Refinar e comparar contorno antes de solicitar aceite: **implementado** sobre a geometria estruturada candidata; HTML 2D aprovado como padrão de revisão.
3. Ilhas secundárias: permanecem **hipótese revisável de duas internas e uma externa**, sem decisão de quantidade final, contornos, posições ou ocupação.
4. **Aceite final expresso da versão refinada:** em 16/11/2026 o proprietário declarou **“Aprovo o contorno refinado na integra”**. Resultado: **APROVADO**, sem ressalvas, exclusivamente para o contorno continental refinado como **base cartográfica de trabalho não canônica**. Não se estende à geometria das ilhas, área oficial da baía, ancoragem, raions, vias, portos, transportes ou demais camadas.

## Implementação efetiva

- Geometria candidata corrente única: `macrogeometria-litoral-baia-ilhas-2010.proposal.json`. O contorno aprovado mantém **44 vértices**, baía derivada de [6,33], contra 26 vértices e [5,19] da versão histórica. Geometria histórica exclusiva em Git; visualizador possui cópia histórica apenas para comparação, não como outra autoridade.
- Valores sintéticos **não oficiais**: área de baía da variante 1.881,995 km² (original 1.851,250 km²); boca cartográfica 18,749 km. Folha local 120×100 km, não é limite municipal.
- Geometrias de ilhas, macrorelevo, hidrografia interior e Ermos não foram redesenhadas pela decisão; suas referências de costa/SHAs dependentes foram reconciliadas.
- A aprovação de costa foi registrada em `approval.owner_approval_for_refined_mainland_coastline`; os metadados globais `approval.owner_approval_for_this_geometry: null`, `cartographic_workflow: PROPOSED_PENDING_OWNER_REVIEW` e `canonical_status: NOT_APPROVED` permanecem intencionais, pois o mesmo JSON também contém ilhas ainda não ratificadas.
- O único HTML ativo `visualizador-fisico-2010.html` apresenta variante, original e sobreposição no padrão 2D aprovado; indicação de aceite do contorno atualizada.

## Evidência de validação final

- **133/133 checagens automáticas de JS no ambiente do conector**, sobre os quatro JSONs e o HTML imediatamente anteriores ao registro formal: anéis simples e limites da folha; águas/terra; ilhas separadas do continente; 7 polígonos de relevo, 9 cursos d'água, 10 Ermos; referências e desembocaduras (inclusive Rio Vasyl); SHAs; inventário de 44 IDs espaciais; e **41/41 geometrias de origem coincidindo exatamente** com os registros do HTML.
- **Zero falhas detectadas** naquelas checagens. A atualização final é de metadados de aprovação, textos e SHAs dependentes: não altera coordenadas. Após a escrita, conferir novamente SHA, parent/tree, geometria invariável, referências de dependência e registros visuais.
- **Limitações declaradas:** validadores Node do repositório e navegador headless não foram executados nesta sessão; sem MDE, batimetria, ancoragem EPSG, medição geodésica ou ensaio de navegabilidade. Resultado técnico **PASS_WITH_LIMITATIONS**, não certificação física real.
- A inspeção visual final foi submetida ao proprietário nesta conversa e recebeu aceite **APROVADO** sem ressalvas.

## Gate de encerramento e continuidade

**FIS-01 CLOSED_FOR_THIS_SCOPE**, exclusivamente para a variante do contorno como base de trabalho. **Nenhum contorno canonizado**; não houve escrita em `master` nem avanço para raions, transportes, runtime ou história. Classes de pendências: A = nenhuma bloqueante para o aceite de contorno; B = conservar as interfaces costeiras com demais camadas e ilhas provisórias; C = infraestrutura e narrativa fora do escopo.

**Próxima unidade sugerida (não executada): MW-011 — revisão geométrica FIS-02 do macrorelevo**, respeitando a costa de trabalho aprovada; submeter eventuais decisões substantivas separadamente. Entregável: variante/avaliação de relevo com validação da interface costa/águas/Ermos, sem canonização. Critério: decisão do proprietário + revisão publicada e verificada. Bootstrap sempre em `master` e leitura do `guide.md` do GitHub, não deste handoff como fonte factual.
