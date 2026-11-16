---
document_id: MW-001-GEO-002-QUADRO-ESPACIAL
subject_id: world-atlas-novydres
fact_scope: GEO-002-quadro-metrico-extensao
reference_year: 2010
workflow_status: APPROVED_WORKING_HYPOTHESIS
canonical_status: NOT_APPROVED
owner_approval_date: 2026-11-16
owner_approval_scope: WORKING_FRAME_120X100_KM_AND_TERRESTRIAL_AREA_STUDY_RANGE_4000_TO_7000_KM2
owner_approval_effect: WORKING_ASSUMPTIONS_ONLY_NO_CANONICAL_GEOMETRY_OR_MUNICIPAL_AREA
truth_state: GM_PREPARED_PROPOSAL_NOT_CONFIRMED
visibility: PLAYER_SAFE
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
created_on: 2026-11-16
geometry_authority: none
---

# MW-001 — Proposta de quadro espacial e extensão de Novydres (2010)

## 1. Mandato e distinção de autoridade

**Aprovação explícita do proprietário em 16/11/2026:** o quadro local de **120 × 100 km** e a hipótese de **4.000–7.000 km² de superfície terrestre municipal em estudo** foram aprovados **como hipóteses operacionais para orientar a cartografia**. A convenção local de coordenadas, unidades e orientação aqui descrita passa a ser o referencial de trabalho de MW-002, sem converter o enquadramento em limites municipais canônicos. **Não foram aprovadas** geometria de costa, âncora real, perímetro, área municipal efetiva, localização individual de raions ou projeção geográfica definitiva. Este aceite não equivale ao fechamento integral de GEO-002.


**Objeto exclusivo:** resolver como **proposta**, e não como cânone, o referencial horizontal, as unidades, a orientação e a ordem de grandeza da extensão necessária ao futuro mapa. Não desenhar litoral, rios, limites municipais, raions, bairros ou transportes, nem gerar ilustração definitiva. A validação e o aceite deste documento significam que existe uma proposta rastreável; **não** significam aprovação substantiva.

A fonte da verdade continua nos assuntos proprietários do snapshot `27595ca32652efdef3d406eb91e4482299056bd9`. A arquitetura ADR-002, o PRD-ATLAS-001 e o guia `cartografia/guide.md` governam este documento. Não substituir `atlas-proposta.md` como proposta editorial geral e não criar um segundo assunto.

### Fatos vinculantes, reconciliados com seus arquivos atuais

- GEO-001.1: **7.000.000 residentes** em Novydres em 2010, sem distribuição espacial aprovada (`../populacao-2010.json`).
- GEO-002.1–002.3: Alasca, Estreito de Bering; predominância de terra continental, costa com grande baía, rios, lagoas e ilhas secundárias (`../localizacao-geral-2010.json`).
- **GEO-002.4 já está fechado em seu arquivo proprietário**, `../implantacao-litoral-baia-2010.json`: referência macrorregional no setor ocidental da Península de Seward, perto de Port Clarence; baía natural protegida, litoral externo, hinterlândia, ilhas secundárias. Não foi aprovado substituir Teller, Brevig Mission ou Port Clarence, nem copiar as margens reais literalmente. O `registro-decisoes.json` e referências anteriores que ainda apontam GEO-002.4 como aberto estão **desatualizados**; não prevalecem sobre o arquivo proprietário vigente.
- GEO-003.1–003.5, GEO-004.3 e GEO-014.1–014.2: vale geotérmico da Cidade Velha/Iknik em Kingswell, serras, tundra/permafrost, litoral abrigado e exposto; Rio Vasyl cruza o núcleo termal e deságua na grande baía; Ermos físicos interrompem a ocupação; aquecimento artificial é desigual (`../geotermia-aquecimento-2010.json`, `../macrorelevo-hidrografia-ermos-2010.json`, `../ermos-estrutura-territorial-2010.json`).
- GEO-004.2/GEO-004.5: nove raions, com nome oficial **Kingswell** para o raion ainda identificado tecnicamente por `district-chelsea` (`../raions-oficiais-2010.json`). A Cidade Velha é o **núcleo interno** e não o raion inteiro.
- GEO-004.4: macroposições em `../posicionamento-raions-2010.proposal.json` **não ratificadas**. A faixa econômica Cidade Velha–Sulfok é canônica, mas não sua linha ou largura (`../corredor-extrativo-old-town-sulfok-2010.json`).

## 2. Sistema local recomendado para elaboração (P1)

Um referencial **cartesiano local ficcional**, plano, em metros, antes de qualquer georreferenciamento real. Não é EPSG, não é latitude/longitude e **não** pode ser exportado como GeoJSON RFC 7946 sem transformação real validada.

| Propriedade | Proposta | Grau de autoridade |
| --- | --- | --- |
| Identificação provisória | `NOVYDRES-LOCAL-2010` | convenção de trabalho, não CRS oficial |
| Geometria horizontal | plano `x,y` | candidata |
| Unidades armazenadas | metro (`m`) | candidata; 1.000 unidades = 1 km de projeto |
| Origem `(0,0)` | centro abstrato do **quadro de estudo**, não Cidade Velha, Port Clarence nem centro municipal | candidata |
| Eixo `+x` | leste cartográfico | candidata |
| Eixo `+y` | norte cartográfico; `y` crescente para cima na carta, sem espelhamento | candidata |
| Rotação da grade | 0° **no quadro de desenho**; ainda não existe azimute geodésico absoluto aprovado | candidata |
| Terceiro eixo | altitude `z` e datum vertical **não atribuídos** | pendente em etapa física posterior |
| Ano | 2010, sem fixar data de censo ou estação meteorológica | já estabelecido |

**Precisão:** armazenar números inteiros de metros para facilitar operações é uma convenção computacional, **não** alegação de acurácia de 1 metro. No quadro geral, decisões continuam aproximadas em quilômetros; só feições locais aprovadas poderão receber detalhamento métrico.

## 3. Extensão de estudo e território: não confundir

**Proposta-base para uma primeira folha técnica:** quadro retangular de 120 km leste–oeste por 100 km norte–sul, **somente envelope de trabalho**. Os limites são:

~~~text
xmin = -60000 m    xmax = +60000 m
ymin = -50000 m    ymax = +50000 m
largura = 120000 m altura = 100000 m
área do QUADRO = 12000 km² (inclui mar, terra e zonas fora do município)
~~~

O envelope não estabelece quatro fronteiras municipais retas, tampouco uma projeção da baía; permite acomodar numa carta sintética a grande baía, costa e hinterlândia com vários núcleos separados por Ermos. **Os 12.000 km² não constituem a área de Novydres.** A folha pode ser redimensionada se a futura geometria validada exigir.

**Hipótese de dimensionamento territorial para discussão, não uma medição:** testar inicialmente um **intervalo aproximado de 4.000–7.000 km² de superfície terrestre municipal** (continente e ilhas menores), sem definir ainda os corpos d’água sob jurisdição municipal. Esse intervalo não corresponde a polígonos nem a área canônica. Serve apenas como teste de capacidade de abrigar sete milhões de pessoas em diversos núcleos densos separados por grandes Ermos; não autoriza calcular densidades oficiais, ocupação urbanizada ou área por raion. O município pode precisar de outro intervalo após o desenho físico; preservar o número populacional fechado.

**Alternativas de quadro para decisão, se o proprietário rejeitar a base:** 100 × 80 km (mais compacto) ou 160 × 120 km (maior afastamento entre núcleos). Essas alternativas também são envelopes, não limites. Evitar escolher a dimensão pelo formato de uma futura exportação 16:9.

## 4. Ancoragem no Alasca e compatibilidade futura

A única amarração hoje canônica é **macrorregional**, próxima a Port Clarence no oeste da Península de Seward. O quadro local **não determina** o centro da baía, a longitude de Kingswell ou o azimute da entrada marítima. Coordenadas geográficas reais de feições inventadas e o perímetro municipal seguem `null`.

**Fluxo proposto, condicionado a aprovação posterior:** (1) aprovar esquema físico e perímetro suficiente para identificar ao menos um ponto de controle; (2) escolher âncora geográfica compatível com a área real e declarar a transformação (translação, rotação, fator de escala, datum); (3) verificar o fuso da âncora; (4) transformar para WGS84 longitude/latitude quando necessário e usar um CRS projetado real em operações métricas. **WGS84 / UTM zona 3N, EPSG:32603 é apenas candidato técnico** se a ancoragem ficar na longitude pertinente ao setor de Port Clarence; sua seleção e adequação deverão ser verificadas, não presumidas. Nenhuma coordenada EPSG/geográfica é publicada nesta unidade.

Uma representação local inicial deve adotar esquema próprio com `crs: NOVYDRES-LOCAL-2010`, **não** cabeçalho GeoJSON fingindo WGS84. A futura exportação para GeoJSON exige transformação explícita e testes de ida e volta, além de registro da âncora e do erro tolerável.

## 5. Regras de consistência herdadas, ainda sem desenhar feições

1. Não transformar o quadro retangular em grade 3×3 de raions. Os nove polígonos futuros serão irregulares e administrativamente distintos dos núcleos urbanizados.
2. A maior parte da ocupação deve estar no continente; água da baía e ilhas não substituem terreno municipal. A boca da baía e a posição das ilhas **não** são especificadas aqui.
3. Rio Vasyl: futura linha contínua, de cabeceiras elevadas por Cidade Velha/Iknik à baía; foz em Sulfok e alinhamento exato continuam hipóteses, não fatos.
4. Preservar serras, tundra, várzeas e costa como Ermos com barreiras funcionais. Não usar ocupação urbana radial ou homogênea; travessias dependem de etapa própria.
5. A concentração de geotermia em Iknik e a dependência térmica de Bukovie são fatos; não usar mapas de calor radiais nem inferir geometrias de dutos nesta unidade.
6. Macroposições dos raions, portos, ferrovia e ilhas secundárias não passam a ser aprovadas apenas por caberem dentro do retângulo.
7. O mapa público não pode incluir dados narrativos restritos; este quadro espacial é por si só uma convenção pública de desenho, sem camada de domínio Cainita.

## 6. Testes proporcionais e critérios de aprovação substantiva

**Testes verificáveis já no documento:** `xmax-xmin=120000 m`, `ymax-ymin=100000 m`, área do quadro `12000 km²`; eixos ortogonais e ambas as direções positivas definidas; nenhuma coordenada de lugar, costa ou rio foi atribuída; `geometria_municipal=null` permanece; valor de habitantes não foi alterado.

**Decisão do proprietário para MW-001:** aprovada em 16/11/2026 a utilização do quadro de 120 × 100 km e do intervalo de 4.000–7.000 km² **como hipóteses de trabalho**. O referencial local de desenho descrito na seção 2 é a convenção operacional de MW-002. Alterações substantivas dessas hipóteses precisarão ser registradas e aprovadas; não exigir aprovação repetida para utilizá-las dentro desse escopo.

**Para fechar a parcela remanescente de GEO-002**, ainda são necessárias geometria física suficiente, perímetro ou delimitação municipal, cálculo de área efetiva, ancoragem geográfica quando couber e validação dos vínculos espaciais. GEO-002.4 permanece fechado em seu arquivo proprietário. Este documento não recebe status `CLOSED_CANON`.

**Aceite de MW-001, diferente de fechamento GEO-002:** proposta documentada, aprovada para orientar a modelagem, reconciliada com GEO-002.1–002.4 e geografia física canônica, sem mapa produzido ou canonização por inferência.

## 7. Questão técnica adjacente fora do mandato de edição MW-001

**Solicitação do proprietário:** alterar o ID do **raion** `district-chelsea` para o literal `district-Kingswell` (não confundir com o ID próprio do núcleo Cidade Velha). Kingswell já é seu nome oficial canônico. Trata-se de uma **migração de identificador**, não de renomeação substantiva da cidade, e **não foi executada em MW-001**, pois quebraria referências antes de uma alteração coordenada. Mapear e atualizar o diretório proprietário, `assunto.json`, `index.md`, catálogo derivado, `raions-oficiais-2010.json`, referências diretas e consumidores de `district-chelsea` em uma unidade autorizada específica. Respeitar maiúscula/minúscula do literal solicitado ou confirmar convenção técnica antes da migração. Não manter dois assuntos vivos como autoridades concorrentes.

## 8. Limites explícitos desta entrega

Nenhum desenho nem coordenada de feição canônica foi criado; nenhum rio, porto, raion, baía, área municipal ou latitude/longitude foi ratificado. A mudança persistida por MW-001 é **documental e aprovada somente para uso como hipótese operacional**, em branch de proposta. O plano de trabalho seguinte deverá partir dos arquivos proprietários atuais, não deste documento como autoridade factual. Consulte `cartografia/guide.md` para handoff.
