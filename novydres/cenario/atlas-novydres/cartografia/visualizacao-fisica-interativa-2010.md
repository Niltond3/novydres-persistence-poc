---
document_id: MW-008-VISUALIZACAO-FISICA-INTERATIVA-2010
subject_id: world-atlas-novydres
reference_year: 2010
workflow_status: PROTOTYPE_DELIVERED
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED_PROPOSAL_NOT_CONFIRMED
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
source_mw007_commit: 76fae4de92ff632c2c65faf5e94233863e960113
---

# MW-008 — Visualização técnica interativa das quatro geometrias candidatas

**Entrega:** `visualizador-fisico-2010.html`, HTML autônomo com dados embutidos e renderização SVG determinística. Abrir o arquivo localmente em navegador moderno; não requer servidor, bibliotecas remotas nem rede.

**Autoridade:** apenas a macro-organização relativa FIS-01..FIS-04 foi aprovada pelo proprietário em MW-007. Todas as geometrias desta visualização permanecem `NOT_APPROVED`. O HTML é **artefato derivado de revisão**, não fonte da verdade. Os quatro JSONs candidatos continuam sendo a geometria estruturada autoritativa **da proposta**, e as fontes canônicas do `master` permanecem superiores para fatos aprovados. Não utilizar esta imagem para inferir lugares, coordenadas geodésicas, dimensões oficiais, raions ou transportes.

## Fontes exclusivas de desenho

| Unidade | Arquivo no mesmo diretório | Git blob |
| --- | --- | --- |
| MW-002 | `macrogeometria-litoral-baia-ilhas-2010.proposal.json` | `0aefaa2161aa9b728fd03a4ec3d0daf522a81b4d` |
| MW-003 | `macrorelevo-2010.proposal.json` | `c5f6caaddfbef3a89fd5ce85a291ae972e9f35ab` |
| MW-004 | `macrohidrografia-2010.proposal.json` | `34918d5707abac23534df877a8c4b0ec4cefc834` |
| MW-005 | `macroermos-2010.proposal.json` | `2865c843b292c9d128bb2e957634de09c4e4b70a` |

O HTML embute **41 feições do inventário**: costa (1), ilhas (3), áreas de relevo (7), eixos de crista (3), bacias (5), cursos (9), corpos d'água (3) e Ermos (10). Em SVG apresenta **43 elementos selecionáveis**, pois adiciona somente 2 referências **derivadas** com IDs já existentes nas fontes: o limiar da boca da baía do índice costeiro 5 ao 19 e o trecho quente do Vasyl nos índices 3–5. O polígono de continente e o de baía são calculados a partir da **mesma linha de costa**, não constituem novos contornos canônicos.

**Conferência de fidelidade:** a lista compacta de todas as 41 geometrias do HTML foi comparada em pares de coordenadas com os quatro JSONs do checkpoint GitHub da unidade anterior; `41/41` registros coincidentes, zero divergências. Não foi alterada nenhuma feição-fonte.

## Funções e evidências

- Alternância de 9 camadas/auxílios, zoom, pan e enquadramento.
- Seleção de feições por ID, rótulo descritivo, classe e dimensão **sintética**, sem pretensão cadastral.
- Exportação do recorte atual como SVG.
- Verificação local em Chromium headless (desktop 1600×960 e mobile 390×844): JavaScript sem erros, 43 feições selecionáveis, 9 opções, alternância de cursos, zoom/restauração e exportação SVG testadas.
- **Limite de evidência:** isto não representa job de GitHub Actions, teste geodésico ou execução dos validadores Node do repositório. O relatório de MW-006 permanece `PASS_WITH_LIMITATIONS` no escopo sintético.

**Referência espacial:** `NOVYDRES-LOCAL-2010`, metros no quadro 120×100 km de estudo. A folha não é área municipal; nenhuma latitude/longitude, EPSG, altitude, área efetiva ou distância real foi canonizada.

**Escopo protegido:** sem alterações em `master`, geometrias candidatas, arquivos canônicos, raions, transportes ou runtime. Validação e eventual aprovação **de contornos** exigem etapa futura e decisão expressa distinta de MW-007.
