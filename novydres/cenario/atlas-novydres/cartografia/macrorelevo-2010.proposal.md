---
document_id: MW-003-MACRORELEVO-NOTAS
subject_id: world-atlas-novydres
year: 2010
workflow_status: PROPOSED_PENDING_OWNER_REVIEW
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
working_frame_commit: b92721da0bc85f1d497668423e2a8f64d81ba9f4
dependent_coast_commit: b76d646955a08177957f90340792c780af5cc8f8
---

# MW-003 — Macrogeometria candidata do relevo de Novydres (2010)

## Entregável e única fonte geométrica

A geometria estruturada desta unidade está exclusivamente em
[`macrorelevo-2010.proposal.json`](macrorelevo-2010.proposal.json).
Este texto explica sua leitura; não é uma segunda base cartográfica.
Seu validador reproduzível é [`validar-macrorelevo.mjs`](validar-macrorelevo.mjs).

A branch MW-003 deriva de `mapwork/mw-002-macrogeometria-costeira` no
checkpoint `b76d646955a08177957f90340792c780af5cc8f8`. Portanto, a costa
continua **candidata e sujeita à aprovação do proprietário**. O referencial local
120 × 100 km de MW-001 foi aprovado somente para modelagem, sem limite municipal.

Fontes canônicas preservadas, no `master` `27595ca32652efdef3d406eb91e4482299056bd9`:
`../macrorelevo-hidrografia-ermos-2010.json`,
`../ermos-estrutura-territorial-2010.json`,
`../geotermia-aquecimento-2010.json`,
`../implantacao-litoral-baia-2010.json` e
`../localizacao-geral-2010.json`.
O PRD-ATLAS-001 (`cartografia/prd.md`) exige geometria única, IDs e proveniência;
as propostas não se tornam fatos por representação gráfica.

## Hipótese morfológica proposta

1. **Depressão interior termal** — um polígono situado em terra firme para testar
   uma posição de vale abrigado associado ao núcleo histórico de Cidade Velha/Iknik.
   Não é o perímetro de Iknik, Kingswell ou de fontes termais individuais.
2. **Serras e contrafortes** — três massas rochosas candidatas nos setores norte,
   leste interior e sul interior, cada uma com eixo de crista qualitativo. Podem
   condicionar futuras divisórias de drenagem e barreiras de Ermo, sem fixar
   passagens, rodovias ou altitudes.
3. **Tundra e baixadas** — duas unidades de tundra/permafrost e uma baixada
   potencialmente encharcada. A atribuição é geomorfológica e não afirma inundação
   permanente, camada contínua de gelo superficial ou ocupação urbana.
4. **Baía e litoral externo** — preservados como classes canônicas e referenciados
   por IDs e intervalos da costa de MW-002; não há nova linha litorânea independente.

São **sete polígonos de âncora fisiográfica e três eixos de crista**.
A soma sintética dos sete polígonos é **1.953,375 km²**. **Não** equivale à
área municipal, à superfície total de terra, à cobertura exaustiva dos Ermos
ou a uma estatística territorial aprovada. Áreas não cobertas permanecem
**não classificadas**; não são por isso planas ou urbanizadas.

As coordenadas são inteiros métricos sintéticos, sem precisão geodésica;
`NOVYDRES-LOCAL-2010` não é EPSG/WGS84. Não existem cotas altimétricas,
datum vertical, MDE, curvas de nível, taxas de declive ou nomes inventados
de montanhas. O eixo de crista não é rota de transporte.

## Vínculos canônicos e limites

- **GEO-003.3**: vale termal, serras, tundra, baía e litoral exposto coexistem;
  os polígonos definem apenas hipótese de posicionamento dessas classes.
- **GEO-003.4**: o Rio Vasyl cruza o núcleo termal da Cidade Velha e deságua na
  baía natural. **Nenhuma coordenada de sua nascente, curso ou foz é proposta**;
  os divisores de águas são uma hipótese futura, não dedução dos eixos de crista.
- **GEO-003.5 e GEO-004.3**: barreiras rochosas, tundra, várzeas e costa são
  condicionantes reais da separação de núcleos. `possible_ermo_type` não é
  o perímetro final de um Corredor do Ermo e nunca constitui décimo raion.
- **GEO-003.1/003.2 e GEO-014**: a geotermia natural é localizada na Cidade
  Velha; não se inferem isotermas radiais, vulcões superficiais, dutos ou
  funcionamento detalhado da calefação.
- **MW-002**: a boca, os contornos da baía e as ilhas permanecem dependências
  candidatas. Uma futura revisão da costa obriga revisão geométrica deste relevo.

Não se traçam raions, limites municipais, bairros, ferrovias, estradas, túneis,
portos, pontes, bacias hidrográficas ou instituições. Também não se altera
a história ou o runtime da crônica.

## Validação e aceite

Na raiz do repositório:

```sh
node novydres/cenario/atlas-novydres/cartografia/validar-macrorelevo.mjs
```

A rotina verifica:
- SHA Git do blob costeiro dependente e estado **não aprovado** da costa;
- quadro e CRS local de MW-001, sem limite municipal ou datum;
- vértices inteiros, dentro da folha, polígonos simples, áreas plausíveis para
  âncoras macroscópicas, ausência de sobreposição;
- todas as áreas em terra continental, sem invadir costa, baía ou ilhas;
- eixos de crista contidos nos próprios polígonos e sem cruzar suas bordas;
- cinco classes canônicas representadas por três famílias de áreas mais
  referências topológicas à baía e ao litoral exposto;
- manutenção explícita dos estados de proposta e ausência de geometria
  de rio, raions, termas ou vias.

**Resultado da validação geométrica preliminar (JavaScript de modelagem):**
7 áreas sem sobreposições ou colisões costeiras; 3 eixos com vértices em
seus polígonos de referência. A execução do validador Node deve ser
confirmada separadamente; a publicação dos arquivos não equivale por si
só a um teste de CI concluído.

## Decisão substantiva pendente

O proprietário poderá aprovar, pedir mudanças ou rejeitar a hipótese de:
(1) vale termal interior; (2) três faixas de serra; (3) duas planícies e
uma baixada; (4) associação relativa à costa candidata. Aprovar este
esboço **não** canoniza novas posições até que as fontes proprietárias e
consumidores sejam reconciliados pelo contrato de propagação.

**Status:** proposta MW-003 concluída como artefato editável; GEO-003.3–003.5
continuam fechados apenas no escopo qualitativo já aprovado, sem
ratificação dos polígonos aqui documentados.
