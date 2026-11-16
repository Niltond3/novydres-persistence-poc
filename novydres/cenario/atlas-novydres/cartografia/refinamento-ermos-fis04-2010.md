---
document_id: MW-013-FIS04-ERMO-REFINEMENT-2010
subject_id: world-atlas-novydres
reference_year: 2010
work_unit: MW-013
workflow_status: OWNER_DECISIONS_PENDING
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
source_parent_commit: 216754fc6f21c1b52804a0ad6b9eb4cf6526a6ed
source_ermo_blob_sha: 83e21a758e439ba1abaa873b94deef2af2ec9b3b
coast_working_blob_sha: d72cf3eb2b3fac9473017a6bbfdc46ea1efb8577
relief_working_blob_sha: cccc4eaac09b192a299108389bef3494f1f15bda
hydro_working_blob_sha: d0912bb8b420a8a29b0de602f4eb05f179da3b0c
---
# MW-013 — Proposta de refinamento dos Corredores do Ermo (FIS-04)

## Escopo e estado
Geometria **candidata, não canônica e sem aprovação do proprietário**. GEO-003.5 e GEO-004.3 continuam a ser as fontes canônicas. Costa continental MW-010, relevo MW-011 e hidrografia MW-012 são bases de trabalho aprovadas, não canônicas; ilhas permanecem hipótese. Não definir raions, rotas, travessias, áreas oficiais ou ocupação urbana.

## Proposta
Dez polígonos não exaustivos: três rochosos, três de tundra/permafrost, duas várzeas e dois trechos costeiros expostos. Cada aresta recebe dois vértices intermediários com perturbação moderada, arredondada a 50 metros locais; antigos pontos principais são preservados. Os mesmos tipos, âncoras de relevo, relações hídricas e identidades permanecem. Isto é refinamento de representação geométrica, não levantamento natural real.

Vértices originais: 60; novos: 180. Área sintética somada MW-005: 801.590 km²; MW-013: 800.421 km². Esses números **não são área municipal ou área oficial dos Ermos**.

## Gates de decisão (um por vez)
1. FIS-04.1 — cristas setentrionais, contrafortes orientais e cristas meridionais: PENDENTE.
2. FIS-04.2 — tundra nordeste e duas manchas sudoeste: PENDENTE.
3. FIS-04.3 — várzea meridional e várzea inferior do Vasyl: PENDENTE.
4. FIS-04.4 — litoral exposto setentrional e sudoeste: PENDENTE.
5. Aceite global da revisão FIS-04: PENDENTE.

Aprovações parciais não fecham MW-013. Não emitir handoff antes da aprovação global, validações finais e leitura remota.

## Pré-validação
Geometria sintética verificada pelo JavaScript no conector: anéis simples, interiores em terra e relevo apropriado, zero colisões de costa, lago, lagoa e ilhas, referências de interseção de cursos naturais preservadas, nenhum Ermo sobreposto aos demais. Comparador no arquivo `visualizador-fisico-2010.html`: MW-013, MW-005, sobreposição. Não houve teste real de navegador, Node/CI ou validação geodésica. Não inferir altitudes, permafrost medido, alagamentos, separação efetiva de cidades ou travessias.

## Pendências A/B/C
A: deliberações individuais, aceite final, validação e readback conclusivos. B: funções de separação ainda qualitativas, a depender de futuros núcleos urbanos. C: raions, transportes, política e narrativa fora do escopo.
