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

**KW-V3-D07 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** eixo logístico principal com vias de carga, oficinas, depósitos e pátios, articulado à malha urbana por ruas locais e ramais ferroviários apenas onde compatíveis.
- Evidência: “KW-V3-D07: Aprovo A — eixo logístico principal com vias de carga, oficinas, depósitos e pátios, conectado à malha urbana por ruas locais e ramais ferroviários onde compatíveis.”
- Consequência morfológica: hierarquia funcional para transporte pesado sem isolamento obrigatório do restante da cidade. **Não autoriza traçado, novo ramal, estação, conurbação nem arte.** Respeitar GEO-004.6A e a infraestrutura U02.

**KW-V3-D08 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** ruas estreitas e irregulares adaptadas a encostas, termas e Rio Vasyl; vias mais largas construídas depois, costurando a malha sem destruí-la.
- Evidência: “KW-V3-D08: Aprovo A — ruas estreitas e irregulares, adaptadas ao relevo, às termas e ao Rio Vasyl, com vias mais largas adicionadas posteriormente sem destruir a malha original.”
- Consequência: vielas e quadras orgânicas de tecido histórico preservadas onde possível, em convivência com eixos posteriores. **Ainda sem aprovação de traçados ou edifícios.**

**KW-V3-D09 — APROVADA COM RESSALVA EXPRESSA DO PROPRIETÁRIO (19/11/2026):**
- **Regra obrigatória do planejamento:** existem **exatamente três pontes históricas** de travessia do Rio Vasyl entre as margens. **Nunca foram construídas outras pontes sobre esse rio** após essas três. Balsas foram implantadas posteriormente, transportando **pessoas e veículos** entre as margens.
- Evidência: “KW-V3-D09: Aprovo A — Poucas travessias estruturantes (Com resalva). O núcleo antigo se conecta à margem posterior por poucas pontes principais, muito importantes para a organização urbana. Só existem três pontes históricas que conectam o Rio. Nenhuma outra foi construída no decorrer do tempo. O que aconteceu foi que balsas começaram a rodar e fazer a conexão de passagem de pessoas e veículos”.
- **Guardrail para geração cartográfica:** exigir contagem exata de três pontes no Rio Vasyl, proibir qualquer quarta ponte (inclusive implícita em nova rodovia/ramal), representar travessias alternativas por balsas. Se a referência U02 ou outros conectores parecerem contradizer a regra, **reportar divergência antes de editar a referência**; não deslocar ou eliminar o conector aprovado automaticamente.
- Não aprova as posições nem a geometria das pontes e dos terminais de balsas.

**KW-V3-D10 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** poucas rotas fixas de balsas, operando terminais estruturados com acesso à malha viária e capacidade de transportar pessoas e veículos.
- Evidência: “KW-V3-D10: Aprovo A — poucas rotas fixas, com terminais estruturados e capacidade de transportar pessoas e veículos.”
- Consequência funcional: representar travessias hidroviárias regulares articuladas às ruas, em complementação às três pontes históricas de KW-V3-D09. **Sem número ou local aprovado para as rotas, balsas e terminais; sem novas pontes.**

**KW-V3-D11 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** uma das **três únicas pontes históricas** se liga diretamente ao núcleo termal original; as outras duas atendem diferentes setores do vale e das expansões urbanas.
- Evidência: “KW-V3-D11: Aprovo A — uma ponte ligada ao núcleo histórico termal e as outras duas conectando setores diferentes da expansão urbana ao longo do vale.”
- Consequência: uma travessia histórica central e duas distribuídas, conectadas às redes viárias de seus setores, **sem novas pontes** e sem posições/traçados definidos. Respeitar a restrição KW-V3-D09, a referência U02 e seus conectores.

**KW-V3-D12 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** conjunto principal de nascentes no coração histórico termal; surgências secundárias distribuídas de forma irregular pelos arredores.
- Evidência: “KW-V3-D12: Aprovo A — conjunto principal de nascentes no coração histórico termal, com fontes secundárias distribuídas irregularmente pelos arredores.”
- Consequência morfológica: a implantação urbana deve reconhecer um polo termal original sem transformar toda Kingswell em área aquecida uniformemente. **Não define quantidade, vazões, temperaturas, fontes individualizadas ou geometria.**

**KW-V3-D13 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** pequenas instalações geotérmicas incorporadas aos quarteirões históricos, com equipamentos de maior escala nas áreas de transição industrial.
- Evidência: “KW-V3-D13: Aprovo A — pequenas instalações geotérmicas integradas aos quarteirões históricos, com equipamentos maiores na transição industrial.”
- Consequência: infraestrutura técnica incorporada sem substituir o núcleo termal por um único complexo industrial. **Não há aprovação de localização exata, tubulações, capacidade, geometria, arte ou canonização.** Preservar o desvio privilegiado do calor para Bukovie e as falhas de distribuição locais.

**KW-V3-D14 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa C aprovada expressamente:** distribuição térmica desigual principalmente por **uso dos edifícios**, com prioridade para instalações técnicas e atividades econômicas, enquanto moradias sofrem irregularidade de fornecimento mesmo quando próximas das fontes.
- Evidência: “KW-V3-D14: Aprovo C — distribuição térmica desigual sobretudo por uso dos edifícios, com prioridade para instalações técnicas e atividades econômicas e aquecimento irregular nas moradias.”
- Consequência: representar o contraste entre abastecimento de setores técnico-produtivos e fragilidade das moradias; **sem pressupor privação absoluta em todos os domicílios, localização, métricas ou responsáveis operacionais.** Mantém o desvio privilegiado para Bukovie, GEO-014 e o clima extremo.

**KW-V3-D15 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** tecido residencial denso e de uso misto. No núcleo, cortiços e edifícios históricos subdivididos; nas expansões, transição gradual para habitações operárias compactas, moradias sobre oficinas e quadras industriais-residenciais.
- Evidência: “KW-V3-D15: Aprovo A — tecido residencial denso e misto, com cortiços e edifícios históricos subdivididos no núcleo, passando gradualmente a habitações operárias, moradias sobre oficinas e quadras industriais-residenciais.”
- Consequência morfológica: adensamento habitacional sem tornar os bairros mono-funcionais, conservando diversidade histórica e continuidade com o corredor industrial. **Não define densidades numéricas, quantidade de edifícios, altura, lotes ou geometria.**

**KW-V3-D16 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** perfil de alturas escalonado e irregular: construções históricas comparativamente baixas e compactas; volumes médios nas expansões operárias; poucos marcos elevados.
- Evidência: “KW-V3-D16: Aprovo A — perfil escalonado e irregular, com construções históricas relativamente baixas e compactas, volumes médios nas expansões e poucos marcos altos.”
- Consequência morfológica: skyline de caráter não uniforme, mas com legibilidade de núcleo antigo e expansões; sem prédios altos distribuídos uniformemente nem obrigação de blocos horizontais grandes. **Não fixa número de andares, posições dos marcos, volumes individuais, polígonos ou arte.**

**KW-V3-D17 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** pedra e tijolo antigos, anexos de madeira, reformas posteriores com metal e concreto; fachadas variadas, envelhecidas, remendadas e adaptadas ao frio.
- Evidência: “KW-V3-D17: Aprovo A — pedra e tijolo antigos, anexos de madeira e reformas posteriores em metal e concreto; fachadas variadas, envelhecidas e adaptadas ao frio.”
- Consequência: linguagem arquitetônica em camadas, variando edifício a edifício e refletindo reapropriação histórica em 2010, sem importar automaticamente a linguagem própria de Drevnigrad. **Não há material obrigatório para cada prédio, nem aprovação de geometria ou arte.**

**KW-V3-D18 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** rede de pequenos largos, mercados de rua e pátios coletivos entre vielas, com poucos espaços maiores junto ao núcleo termal.
- Evidência: “KW-V3-D18: Aprovo A — rede de pequenos largos, mercados de rua e pátios coletivos entre as vielas, com poucos espaços maiores junto ao núcleo termal.”
- Consequência: sistema descentralizado de convivência e comércio a pequena escala, vinculado à malha orgânica original, sem uma praça gigante dominante. **Não fixa quantidades, implantação, dimensões, nome de praça, monumento ou geometria.**

**KW-V3-D19 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** proteção climática pontual por arcadas, coberturas e passagens abrigadas integradas às construções; largos e mercados externos permanecem.
- Evidência: “KW-V3-D19: Aprovo A — proteção climática pontual, com arcadas, coberturas e passagens abrigadas integradas às construções; largos e mercados externos permanecem.”
- Consequência: rede pública aberta e diversa com abrigos localizados, não uma cidade toda coberta ou aquecida. **A atividade externa permanece condicionada ao clima extremo e à infraestrutura precária; não há aprovação de engenharia, localização, tamanho ou geometria.**

**KW-V3-D20 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** marcos cívicos e religiosos distribuídos entre largos e quarteirões históricos reaproveitados, com funções comunitárias também nas expansões.
- Evidência: “KW-V3-D20: Aprovo A — marcos cívicos e religiosos distribuídos entre largos e quarteirões históricos reaproveitados, com funções comunitárias também nas expansões urbanas.”
- Consequência: conservar a pluralidade dos marcos no tecido antigo, estendendo funções comunitárias aos bairros novos sem criar centro monumental único. **Não confirma identidade, número, função atual ou implantação de templos, sedes ou POIs específicos, nem geometria ou arte.**

**KW-V3-D21 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** rede de serviços comunitários distribuídos pelos bairros, em edifícios pequenos e médios, frequentemente reaproveitados, com poucos equipamentos maiores próximos às vias principais.
- Evidência: “KW-V3-D21: Aprovo A — rede de serviços comunitários distribuídos pelos bairros, em edifícios pequenos e médios, frequentemente reaproveitados, com poucos equipamentos maiores próximos às vias principais.”
- Consequência: serviços cotidianos de proximidade integrados ao tecido misto, complementados por poucos equipamentos de escala maior próximos dos eixos viários. **Não aprova instituições ou locais específicos, quantidade, capacidade, qualidade de serviço, geometria ou imagens.**

**KW-V3-D22 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** frentes ribeirinhas mistas e descontínuas, com moradias densas, cais e armazéns antigos, pequenos acessos públicos e maior atividade logística na transição industrial.
- Evidência: “KW-V3-D22: Aprovo A — frentes ribeirinhas mistas e descontínuas, com moradias densas, cais e armazéns antigos, pequenos acessos públicos e maior atividade logística na transição industrial.”
- Consequência: margem heterogênea, com variações entre ocupação popular, vestígios comerciais antigos e logística mais intensa rumo à expansão industrial. **Não fixa localização de cais, armazéns, atracadouros ou terminais nem modifica contornos, pontes ou geometrias.**

**KW-V3-D23 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** acessos capilares por vielas, escadarias e passagens de pedestres conectam bairros e pequenos cais, complementados por poucos eixos viários e rampas capazes de atender balsas de veículos e logística.
- Evidência: “KW-V3-D23: Aprovo A — acessos capilares por vielas, escadarias e passagens de pedestres, complementados por poucos eixos viários e rampas para balsas de veículos e logística.”
- Consequência: preservar a capilaridade da malha antiga em vez de impor avenida marginal contínua, assegurando alguns acessos automotivos estruturantes ao rio. **Não aprova número, localização, traçado nem engenharia individual de rampas, escadas, vias ou terminais, e não altera a referência U02.**

**KW-V3-D24 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** pequenos cais históricos e acessos públicos permanecem distribuídos pela frente ribeirinha; os poucos terminais de balsas operam separadamente, com rampas e acessos viários próprios.
- Evidência: “KW-V3-D24: Aprovo A — pequenos cais históricos e acessos públicos distribuídos, separados funcionalmente dos poucos terminais de balsas, que terão rampas e acessos viários próprios.”
- Consequência: não converter a rede de pequenos cais históricos em terminais veiculares; organizar aproximações e rampas de balsas em poucos pontos funcionais. **Sem autorizar número, localização, dimensões, obras, nova ponte, geometria ou arte.**

**KW-V3-D25 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** rede logística escalonada: pequenos depósitos e operações leves junto aos antigos cais; pátios de transbordo maiores nas bordas do núcleo histórico, conectados ao corredor industrial compartilhado com Sulfok.
- Evidência: “KW-V3-D25: Aprovo A — rede escalonada, com pequenos depósitos e operações leves nos cais antigos e pátios de transferência maiores nas bordas do núcleo histórico, conectados ao corredor industrial.”
- Consequência: hierarquia de cargas leves nos cais históricos para transbordos mais volumosos nas bordas, sem transformar o núcleo antigo em pátio de carga pesada. **Não define quantidade, localização, novos ramais ou estradas, operação das balsas, capacidade, geometria ou arte.**

**KW-V3-D26 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** corredor principal de cargas com acessos seletivos a pátios e galpões, complementado por ruas locais para moradias e comércio, sem sobrecarga de caminhões nas vielas históricas.
- Evidência: “KW-V3-D26: Aprovo A — corredor principal de cargas com acessos seletivos aos pátios e galpões, complementado por ruas locais que atendem moradias e comércio sem sobrecarregar as vielas históricas.”
- Consequência: separação hierárquica do tráfego pesado sem isolar funcionalmente bairros ou impor hiatos urbanos artificiais na transição com Sulfok. **Não cria vias, ramais, pontes, traçados, geometrias ou arte.** Preservar U02.

**KW-V3-D27 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa B aprovada expressamente:** grandes galpões, pátios murados e complexos fabris predominam junto ao corredor de cargas; oficinas e moradias se concentram principalmente nas ruas secundárias.
- Evidência: “KW-V3-D27: Aprovo B — grandes galpões, pátios murados e complexos fabris predominam junto ao corredor de cargas, enquanto oficinas e moradias ocupam principalmente ruas secundárias.”
- Consequência: frente industrial de porte maior e caráter produtivo nítido no corredor, convivendo com bairros operários adjacentes. **Sem inventar separação desocupada, fronteira impermeável com Sulfok, edifícios, alturas, lotes ou geometrias.** Preservar U02.

**KW-V3-D28 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa B aprovada expressamente:** contraste direto entre muros altos/fundos de fábricas e ruas residenciais estreitas, com poucos elementos de transição.
- Evidência: “KW-V3-D28: Aprovo B — contraste direto, com muros altos e fundos de fábricas confrontando ruas residenciais estreitas, com poucos elementos de transição.”
- Consequência: interface fabril-residencial abrupta e opressiva, sem corredor intermediário de oficinas obrigatórias; preservar a malha contínua D06 e entradas de carga seletivas D26. **Não fixa posição, gabarito, materiais de muros, traçado, geometria ou imagem.**

**KW-V3-D29 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** quarteirões industriais fechados, com galpões ao redor de pátios internos, portões de carga voltados ao corredor principal e muros junto às ruas residenciais.
- Evidência: “KW-V3-D29: Aprovo A — quarteirões industriais fechados, com galpões ao redor de pátios internos, portões de carga voltados ao corredor principal e muros junto às ruas residenciais.”
- Consequência: logística intramuros organizada em pátios de manobra e galpões adjacentes, com acessos seletivos ao corredor pesado e fundos murados confrontando bairros. **Não impõe forma idêntica a todo quarteirão nem aprova número, dimensão, posição, edifícios individuais ou geometrias.**

**KW-V3-D30 — APROVADA_PELO_PROPRIETÁRIO (19/11/2026), escopo conceitual candidato do Mapwork V3:**
- **Alternativa A aprovada expressamente:** galpões com telhados amplos e variados, predominantemente baixos ou médios, com poucas chaminés e torres técnicas altas como marcos ocasionais.
- Evidência: “KW-V3-D30: Aprovo A — galpões com telhados amplos e variados, predominantemente baixos ou médios, com poucas chaminés e torres técnicas altas como marcos ocasionais.”
- Consequência: grandes coberturas industriais com perfil majoritariamente baixo/médio e pontuais marcos técnicos verticais, sem formar uma floresta contínua de chaminés. **Não aprova quantidades, alturas, locais, novas instalações, geometrias ou arte.**

**Próxima decisão substantiva, ainda ABERTA:**
`KW-V3-D31` — qual o estado de conservação predominante dos complexos fabris de Kingswell em 2010?
- **A (recomendada):** industriais ainda em funcionamento, mas desgastados e remendados, com fachadas escurecidas, coberturas reparadas e manutenção irregular; alguns setores desativados.
- **B:** declínio industrial profundo, com grande parte dos complexos vazios ou parcialmente ocupados, pátios deteriorados e poucas operações regulares.
- **C:** operação industrial relativamente forte, com galpões conservados e modernizados, apesar das precariedades do entorno residencial.
A decisão trata da atmosfera física e ocupação relativa, não da produção exata ou de edifícios individuais. Preservar D17, D27-D30 e base U02; **sem geometrias ou imagens**.

**Pendência editorial identificada:** `novydres/CONTEXT.md` mantém referência toponímica antiga, superada por GEO-004.1/GEO-004.5 do mesmo snapshot. Corrigir por processo editorial próprio; não alterado neste checkpoint.
