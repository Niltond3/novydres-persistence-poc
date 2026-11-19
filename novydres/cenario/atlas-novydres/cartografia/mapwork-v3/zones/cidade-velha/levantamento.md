# Mapwork V3 — Cidade Velha (Kingswell): levantamento inicial

**Status:** PLANNING / CANDIDATE_RESEARCH_ONLY; não é aprovação de geometria, instalação, POI, arte ou cânone.
**Snapshot autoritativo:** master `876b764bcc23ca2ea2949f5ec505ce85bac46701` (19/11/2026).
**Sujeito proprietário:** `district-chelsea`; núcleo `chelsea-cidade-velha`. A região não corresponde ao raion inteiro.
**Agente:** `novydres/cenario/atlas-novydres/cartografia/mapwork-v3/AGENT.md`.
**Referência visual:** U02 aprovada, Drive ID `1PrfWEcD07Gz5eX5r2qKGaRlecixVKh6r`, PNG 1448×1086, SHA256 `9d55965f45181e3b943552e32df0e8ad41b63c8974ffd6e670f447ffd36eb9a0`, verificado por download e cálculo local.
**Estado global V3:** `world-state.json`: nenhuma zona criada; `last_approved_global_release=null`; não há conectores V3 já gerados.

## CANON — fatos vinculantes (fontes no snapshot)

- Nome formal do núcleo histórico e do raion é Kingswell, nome comum Cidade Velha; IDs estáveis distintos. Núcleo, limites, população e área ainda sem definição. Fonte: `novydres/cenario/geografia/district-chelsea/cidade-velha-2010.json` (GEO-004.1) e `revisao-toponimo-2010.json` (GEO-004.5); **não reintroduzir nome indígena anterior**.
- Região originalmente habitada por comunidades originárias antes de 1423. Gilgamesh dedicou o posto Ventrue Kingswell em 1423, com uma única Ordem Urukiana dotada de atuação religiosa/ritual. Crescimento gradual; não atribuir aos povos originários os ritos fictícios do culto. Fonte: `origens-mortais-e-culto-fundador.json`, `gilgamesh-culto-fundador-e-leis-de-sangue.json`, `preparacao-urukiana-antes-de-1423.json`.
- Ventrue exploraram termas/minerais; expulsos em 1917 para Bukovie. Kingswell permaneceu anarquista; Sulfok passou aos anarquistas em 1945; cerco econômico e social persistente em 2010. Fontes: `novydres/cenario/historia-global/ascensao-ventrue-old-town-bukovie-2010.json`, `revolta-anarquista-1917-invasao-saba-1945.json`, `novydres/cenario/politica-global/dominio-anarquista-old-town-sulfok-2010.json`, `cerco-estados-livres-kingswell-sulfok-2010.json`. Camada cainita não entra automaticamente na carta mortal pública.
- Vale protegido com geotermia abundante e Rio Vasyl atravessando a Cidade Velha, afluentes e foz na grande baía, sem contornos aprovados. Aquecimento precário e desigual: parte privilegiada do calor desviada para Bukovie. Fontes: `novydres/cenario/atlas-novydres/macrorelevo-hidrografia-ermos-2010.json`, `geotermia-aquecimento-2010.json`.
- Um corredor econômico histórico Kingswell–Sulfok concentra extração, indústria pesada e logística, sem obrigação de conurbação contínua. Ermos de cristas, tundra, várzeas e litoral restringem acessos. Fontes: `corredor-extrativo-old-town-sulfok-2010.json`, `ermos-estrutura-territorial-2010.json`.
- A população municipal de 2010 é 7 milhões em nove raions; parcela no núcleo histórico é desconhecida. Fontes: `populacao-2010.json`, `raions-oficiais-2010.json`.
- O terminal internacional de passageiros do Expresso Transberíngio em Sulfok é fato canônico GEO-013.1; não inventar parada internacional em Kingswell.

## APPROVED_SCOPED / CANDIDATE — visual, não geoespacial canônico

- U02 é a última base ilustrada aprovada para trabalho. De U03 em diante, visualmente trocam-se os rótulos Vasyl Bay e New London, mantendo o local do POI 34. Isso conflita com o terminal de passageiros canônico em Sulfok; reconciliação de identidade/serviço ainda obrigatória. Fonte: `cartografia/topdown/t03-u02/topdown_approval_state.json`, `u03_remapeamento_zonas.json`.
- Inventário visual aprovado apenas quanto ao escopo editorial/identidades apresenta uma **área de busca de Kingswell no sul-central da U02**, `district-chelsea`, com envelope **não aprovado como fronteira**. Ref. `cartografia/edicao-raster/inventarios/inventario-espacial-v3-aprovado.json`. A área não determina onde está o núcleo `chelsea-cidade-velha`.
- POIs visuais candidatos do raion Kingswell: `poi-14` Salão do Conselho, `poi-15` Estação Geotérmica Periférica, `poi-16` Capelas da Fome Branca, `poi-17` Assembleia dos Estados Livres, `poi-32` Grande Sinagoga Beit HaZikaron. **Localizações individuais, edificações e existência canônica não ratificadas** por esse inventário; não transformar pontos candidatos em monumentos definitivos.
- `posicionamento-raions-2010.proposal.json` sugere macroposição west-interior para Kingswell, enquanto a U02 aprovada para arte coloca área de busca Kingswell no sul-central: diferença entre proposta editorial e base visual, não autorização para mover uma ou outra.

## UNKNOWN — bloqueios relevantes do desenho técnico

1. Forma/extensão do núcleo Cidade Velha **dentro** do raion Kingswell, especialmente as margens e travessias do Rio Vasyl; não há geometria nem área aprovada.
2. Relações de lote, quadra, largura viária, ruas/bonde, densidades, pavimentos, população local e metragens; não inferir metros a partir da referência U02.
3. Posições exatas de fontes termais, captadores, tubulações, racionamento, vias, pequenas pontes, redes técnicas e limites dos Ermos.
4. Status/localização dos POIs candidatos e adjacências com setores vizinhos; ferrovias e pontos em conflito dependem de reconciliação.
5. Edifícios históricos específicos e evolução de 1423–2010 (não interpretar uma analogia como existência de edifício).

## Pesquisa de analogias reais (consulta em 19/11/2026)

| Referência real | Observação verificada | Aplicação ficcional candidata, NÃO cânone | Restrição |
|---|---|---|---|
| Tallinn, Estônia | Centro histórico de malha radial e edifícios medievais, madeira na periferia | Quarteirões irregulares e lotes historicamente sobrepostos | Não copiar cronologia ou cidades medievais inteiras |
| Vyborg, Rússia | Centro histórico moldado por camadas suecas, finlandesas e russas | Alvenaria envelhecida, mistura tipológica e reformas dissonantes | Outra origem cultural e clima |
| Old Québec, Canadá | Núcleo alto/baixo associado a encostas e atividade portuária | Terraços urbanos, hierarquia viária por topografia e travessias | Fortificações históricas não implicam muralha em Kingswell |
| Yakutsk, Rússia | Construção em permafrost utiliza soluções de fundação variadas, incluindo pilotis e ventilação | Pátios técnicos e fundações diferenciadas por setor, onde o permafrost ocorre | Necessidade estrutural específica não comprovada nos lotes fictícios |
| Nome, Alasca | Pressões de gelo/temporais/incêndios sobre patrimônio e infraestrutura | Contraste entre núcleo urbano e frentes degradadas | Cidade real não tem densidade/escala de Novydres |

**URLs acessadas 19/11/2026:**
- https://whc.unesco.org/en/list/822/
- https://www.wmf.org/monuments/vyborg-historic-center
- https://whc.unesco.org/en/list/300/
- https://mpi.ysn.ru/en/research/field-sites/108-english-uk/research/field-sites/1523-foundations
- https://dnr.alaska.gov/parks/oha/clg/AlaskaCLGs/Nome.htm

## Pré-planejamento (SEM geometria ou arte)

1. Preservar U02 integral e a macro área visual de busca sem torná-la fronteira oficial.
2. Propor núcleo original de ocupação/termas/Rio Vasyl e separar **posteriormente** expansões de 1423, ciclo minerador, faixa industrial e adensamento do século XX, com múltiplas densidades e tipologias.
3. Formular grafo global de acessos, ruas, pontes, tranvia/bonde e dutos com conectores consistentes, preservando canais e Ermos.
4. Fazer o mapa técnico integral ANTES/DEPOIS somente após a resolução de decisões substantivas; nenhuma ilustração PNG prévia à aprovação expressa do esboço.
5. Não avançar a PLANNING para SKETCH_APPROVED; nenhuma canonização, release global ou handoff.

**KW-V3-D01 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** núcleo histórico **compacto** em torno do vale termal e do Rio Vasyl, com expansões industriais **fora do núcleo histórico, porém dentro do raion Kingswell**.
- Evidência: mensagem expressa do proprietário: “KW-V3-D01: Aprovo a opção A — núcleo histórico compacto em torno do vale termal e do Rio Vasyl; expansões industriais fora do núcleo, ainda dentro do raion Kingswell.”
- Consequência espacial: separar perímetro do núcleo histórico, zonas de expansão no mesmo raion, corredor extrativo até Sulfok e redes de travessia. **Aprovação conceitual não aprova polígono, metragem, edifícios, pontes, densidade nem cânone do Atlas.**

**KW-V3-D02 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** núcleo histórico inicialmente concentrado em uma margem do Rio Vasyl, com expansão posterior para a outra.
- Evidência: “KW-V3-D02: Aprovo A — núcleo histórico inicialmente concentrado em uma margem do Rio Vasyl, com expansão posterior para a outra.”
- Consequência cartográfica: distribuição assimétrica da idade do tecido urbano nas duas margens; travessias e ocupação ulterior devem respeitar a cronologia proposta. **Não define qual margem é mais antiga, nem pontes, cronologia, perímetros ou cânone oficial.**

**KW-V3-D03 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** fontes termais e abrigos estruturaram o núcleo original na margem inicial; comércio e instalações fluviais desenvolveram-se próximos.
- Evidência: “KW-V3-D03: Aprovo A — as fontes termais e os abrigos estruturaram o núcleo original; comércio e instalações fluviais desenvolveram-se próximos.”
- Consequência morfológica: privilegiar núcleo termal e função de abrigo como origem, deixando o mercado e acessos ribeirinhos relacionados, mas não como centro primordial. **Não aprova localização de fontes, cais, edificações, traçado ou cânone.**

**KW-V3-D04 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** sobreposição gradual: a malha urbana humana anterior permaneceu em grande parte, recebendo edifícios de poder e culto e praças remodeladas durante o período de domínio de Gilgamesh e suas camadas posteriores.
- Evidência: “KW-V3-D04: Aprovo A — sobreposição gradual: a malha urbana anterior permaneceu em grande parte, com inserções de edifícios de poder, culto e praças remodeladas.”
- Consequência morfológica: sobrepor diferentes períodos de edifícios e espaço público sem substituir uniformemente a malha termal original. **Não aprova sítios ou monumentos concretos nem canoniza sobrevivências específicas até 2010.**

**KW-V3-D05 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** reapropriação funcional predominante das construções históricas para moradias, mercados, oficinas e usos comunitários, mantendo alguns monumentos e ruínas.
- Evidência: “KW-V3-D05: Aprovo A — reapropriação funcional das construções históricas para moradias, mercados, oficinas e usos comunitários, mantendo alguns monumentos e ruínas.”
- Consequência morfológica: reutilização do tecido construído em vez de abandono total ou substituição uniforme, com coexistência de estruturas monumentais e ruínas. **Não aprova edificações individuais, quantidades, localização ou canonização.**

**KW-V3-D06 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** transição contínua, orgânica e de uso misto entre construções históricas, cortiços, oficinas e galpões, com indústria mais intensa em direção ao corredor de Sulfok.
- Evidência: “KW-V3-D06: Aprovo A — transição urbana contínua e orgânica, com mistura gradual de construções históricas, cortiços, oficinas e galpões, intensificando a atividade industrial em direção a Sulfok.”
- Consequência morfológica: evitar vazio artificial ou fratura estilística dentro de Kingswell; **não forçar conurbação obrigatória com Sulfok** (GEO-004.6A), nem aprovar traçados, lotes, eixos, geometria ou arte.

**Próxima decisão substantiva, ainda ABERTA:**
`KW-V3-D07` — como organizar o eixo logístico do cinturão produtivo de Kingswell, orientado para Sulfok?
- **A (recomendada):** um eixo principal de vias de carga e espaços produtivos, com oficinas/depósitos/pátios relacionados, conectado a ruas locais; ramais ferroviários apenas onde compatíveis com a base aprovada.
- **B:** malha distribuída de eixos menores de transporte, com tráfego de cargas e instalações dispersas, sem eixo logístico dominante.
- **C:** faixa pesada relativamente segregada da malha residencial, com travessias estruturadas em pontos específicos.
A escolha deve respeitar o corredor econômico GEO-004.6A sem inventar geometria, novas estações internacionais em Cidade Velha ou conurbação inter-raions obrigatória.

**Pendência editorial identificada:** `novydres/CONTEXT.md` mantém referência toponímica antiga, superada por GEO-004.1/GEO-004.5 do mesmo snapshot. Corrigir por processo editorial próprio; não alterado neste checkpoint.
