# Auditoria de prontidão para imagem — Kingswell / Cidade Velha (2026-11-19)

**Status:** diagnóstico CANDIDATE, NÃO é aprovação de geometria, imagem, cânone ou esboço.
**Base candidata da auditoria:** branch `mapwork/kingswell-planejamento-20261119`, parent `e40b6af8e83881eccb719e0f91798b4b933fc485`; fonte de cânone permanece `master` `876b764bcc23ca2ea2949f5ec505ce85bac46701`.
**Diagnóstico:** D01–D55 suficientes para identidade e direção de arte, INSUFICIENTES para a fase de geração detalhada. Não prolongar entrevista de minúcias até construir e confrontar um esboço espacial verificável.

## Matriz de prontidão

| Contrato | Situação | Consequência |
|---|---|---|
| Identidade histórica, mistura de usos, arquitetura, envelhecimento, clima, luz | DEFINIDO conceitualmente por D01–D55 | Apto para guiar composição e prompts de lote; detalhes menores podem ser resolvidos tecnicamente |
| Base U02 e escala de raster | REFERÊNCIA VERIFICADA 1448×1086, SHA 9d55965f45181e3b943552e32df0e8ad41b63c8974ffd6e670f447ffd36eb9a0; detalhe 64×, tiles 512 | Referência visual imutável; pixel U02 não é unidade métrica |
| Escopo espacial | BLOQUEANTE: núcleo Cidade Velha `chelsea-cidade-velha` ≠ raion Kingswell `district-chelsea`; nenhum perímetro de núcleo aprovado | Delimitar recorte editável no inventário U02, preservando contexto e vizinhos |
| Esboço estruturado | BLOQUEANTE: nenhuma `zones/cidade-velha/zone.json`, nenhum `bounds`, `connectors`, `elements`, lotes ou `sketch_approved` | Não é possível gerar/compor/validar uma zona real |
| Hidrografia, margens, três pontes e conectores U02 | BLOQUEANTE ESPACIAL: decisões conceituais D02, D09–D11 não têm correspondência topológica validada com a imagem | Desenhar candidata de curso do Rio Vasyl, três travessias e conexões; detectar incompatibilidades antes da arte |
| Malha, quadras, lotes, densidade e POIs | BLOQUEANTE: não há geometria de intervenção nem validação de relação entre tecido histórico e industrial; POIs de Kingswell são candidatos, não localizações canônicas | Gerar esboço técnico da zona **e da cidade integral** para comparação, com função e implantação dos especiais; perguntar ao proprietário só onde for indispensável |
| Pesquisa de tipologias reais | REFERÊNCIAS presentes em `levantamento.md`; não há entradas em `zone.json` | Migrar referências para manifesto estruturado após escolher geometria |
| Zonas vizinhas | NÃO GERADAS V3; `world-state.json` tem `zones={}` | Preparar contratos de borda/autoridade U02, sem exigir geração prévia dos raions vizinhos |
| Inspeção e aceite | NÃO EXECUTADO: nenhum esboço integral, prévia ANTES/DEPOIS nem aceite expresso | Só gerar assets após aprovação do esboço |
| Assets e readback | ZERO ASSETS V3; `last_approved_global_release=null` | Persistir por lote, máscara, verificação local e Drive apenas após gate visual |

## Riscos técnicos encontrados nos contratos do repositório

1. `mapwork.py audit` só examina `zones/*/zone.json`; como não há zone.json na branch, o comando pode relatar `PASS` com `zones_checked=0`. Isto **não** atesta Kingswell.
2. `.github/workflows/mapwork-ci.yml` observa pushes em `mapwork/**`, mas esta branch é `mapwork/**`. Logo, o push de checkpoint atual não está coberto por esse gatilho de CI. PRs para master podem acionar verificação, mas isso não equivale a proteção de branch.
3. `zone.schema.json` define `bounds` e `core/envelope` como retângulos; máscaras fornecem detalhe pixelar, porém o teste não comprova continuidade interna das vias, lotes sem sobreposição às vias, os três cruzamentos funcionais ou relações topológicas dos POIs.
4. `connector_match(..., require_all=True)` exige manifestos de todos os vizinhos; a primeira zona não pode depender de arte de vizinhos ainda inexistentes. Precisa haver representação explícita e validável das bordas aprovadas da U02.
5. A U02 aprovada é mapa superior top-down. `config.json` define `illustrated_2d_oblique` para os assets; antes de gerar, conciliar representação e encaixe sem mudar orientação ou geometria global.
6. O tamanho potencial de Kingswell em 64× e tiles de 512×512 exige fatiamento e critérios de inspeção por lote; não prometer HTML monolítico leve no celular. `README.md` já reconhece a limitação.

## Ordem correta a seguir

1. Manter D56 como `DEFERRED` não bloqueante; NÃO transformar preferência implícita em aprovação.
2. Reconstruir a amostra relevante da U02 e confrontar área de busca sul-central de Kingswell com Rio Vasyl, vias, relevo, ferrovia, Ermos, Sulfok e Drevnigrad. Inventário de 2010 fornece envelope **não canônico**, e o núcleo Cidade Velha não tem perímetro oficial.
3. Preparar geometria **candidata** de escopo, núcleo histórico, setores de expansão, vias preservadas, margens, pontes, conectores, quarteirões e lotes, usando projeção coerente com U02. Não transformar isso em cânone por derivação.
4. Implementar/fixar validações espaciais úteis e corrigir CI candidato antes de alegar gates executáveis.
5. Exibir **esboço integral comparativo no chat**, com áreas protegidas e lista objetiva de mudanças; solicitar somente escolhas espaciais realmente indeterminadas, uma de cada vez, antes de aprovar o esboço.
6. Após aprovação expressa, preencher `zone.json`, preparar contratos de borda, gerar por lote e verificar máscaras/tiles, depois comparação integral e aceite final.

**Critério de encerramento da entrevista:** não é número de perguntas; é ausência de decisões substantivas pendentes que afetem geometria, implantação, conectores, distribuição morfológica ou direção visual. Perguntas históricas/operacionais não bloqueiam imagem se não alterarem esses elementos. D01–D55 permanecem aprovadas. Nenhum novo artefato visual foi criado nesta auditoria.
