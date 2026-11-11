# NOVYDRES — MASTER HANDOFF V1

> **Documento-raiz de continuidade, auditoria e retomada operacional**
>
> Este documento não é um resumo promocional. É um handoff de projeto. Sua função é permitir que outro agente, outro modo do ChatGPT ou outro ambiente de trabalho retome **Novydres by Night** sem depender da memória da conversa que o produziu e sem reabrir decisões fechadas por acidente.

---

## 0. IDENTIDADE DO PROJETO

| Campo | Estado |
|---|---|
| Projeto | **Novydres by Night** |
| Sistema-base | **Vampire: The Masquerade V5**, com cânone próprio, regras locais/homebrew e arquitetura editorial standalone |
| Recorte temporal principal | **2010** |
| Localização cartográfica corrente | **Northern Alaska, Bering Strait Urban Zone** |
| Nome histórico da cidade | **Novo Endereço de Gilgamesh, o Rei Legislador** / **Новый адрес** |
| Handoff | **NOVYDRES — MASTER HANDOFF V1** |
| Data do handoff | **2026-09-27** |
| Finalidade | Transferir estado canônico, decisões, rejeições, regras, números, artefatos, cartografia, produção visual, pendências e próximo ponto de trabalho |
| Estado geral | Projeto **ativo**, com múltiplas frentes em estágios diferentes; não existe um único “status do projeto” |
| Princípio de continuidade | Nenhuma decisão fechada pode ser substituída silenciosamente por preferência nova, inferência ou reconstrução aproximada |
| Fonte espacial principal atual | **Master Map** |
| Relação Master Map → tiles | **O Master Map é a fonte espacial principal; tiles são derivados dele, nunca geografia independente** |
| Ambiente operacional decidido em 2026-09-27 | Fechar este handoff; usar o **Project** como fonte documental de verdade; desenvolver/decidir em **Work/Desktop**; pós-processar o mapa no **GIMP**; preservar editável XCF e exportar PNG |

### 0.1 Classes de estado usadas neste handoff

- **CANÔNICO / FECHADO** — decisão ou conteúdo cuja substância não deve ser reaberta sem trigger explícito.
- **APROVADO / CONGELADO** — asset/solução visual aprovada. Não deve ser reinterpretada durante produção ordinária.
- **APROVADO COM CONDIÇÕES** — válido, porém com gate, dependência, QA ou sincronização ainda exigida.
- **EM DESENVOLVIMENTO** — frente ativa e não concluída.
- **PROVISÓRIO** — hipótese, benchmark ou estrutura útil que não adquiriu autoridade canônica final.
- **PENDENTE DE DECISÃO** — escolha material ainda aberta.
- **REJEITADO / DESCARTADO** — solução testada ou item explicitamente abandonado.
- **SUPERADO** — já foi válido ou usado no processo, mas autoridade posterior o substituiu.

---

# 1. COMO USAR ESTE HANDOFF

## 1.1 Hierarquia de autoridade

Quando fontes divergirem, usar esta ordem:

1. **Decisão posterior explicitamente aprovada pelo usuário**.
2. **Artefato versionado mais novo que declara supersession/correção sem alteração substantiva indevida**.
3. **Decision ledger / contrato de autoridade do workstream**.
4. **Artefato principal do workstream**.
5. **Editorial Map vigente**.
6. **Capítulo canônico consolidado**.
7. **Registro de conversa datado**.
8. **Material legado, export antigo, prompt histórico ou proposta de assistente**.

Uma decisão mais nova só substitui uma antiga **na superfície que ela efetivamente alterou**. Exemplo: a nova posição gráfica de Sulfok no Master Map pode superar a linha “Posição no mapa: Sudoeste” do Atlas para fins cartográficos sem apagar a função industrial, o conflito político ou os POIs de Sulfok.

## 1.2 Regra contra harmonização silenciosa

Se duas fontes válidas divergem:

- registrar a divergência;
- identificar qual camada cada uma governa;
- marcar a dívida de sincronização;
- **não** fabricar uma terceira solução intermediária;
- **não** editar retroativamente o texto antigo sem decisão de patch.

### REGRA → MOTIVO → ERRO QUE EVITA

**REGRA:** separar cânone textual, cânone sistêmico, geografia visual e assets visuais.  
**MOTIVO:** eles evoluíram em velocidades diferentes.  
**ERRO QUE EVITA:** apagar lore legítimo porque um carimbo foi descartado, ou restaurar geografia antiga porque ainda aparece num capítulo textual fechado.

## 1.3 “Congelado” não significa “imune a QA”

Em 2026-09-24 foi autorizado reabrir POIs congelados caso estivessem abaixo do padrão visual consolidado pós-POI 04. O conjunto explicitamente apontado para reanálise foi:

`01, 02, 03, 08, 10, 11, 22, 26, 32`.

Portanto:

- freeze impede redesign arbitrário;
- QA transversal posterior pode justificar correção;
- uma correção aprovada volta a ser congelada;
- não transformar essa exceção em permissão para reabrir tudo.

## 1.4 Não preencher lacunas

Quando este documento disser que uma informação está ausente, pendente, referenciada ou não verificada:

**não completar por conhecimento de V5, Wikipédia, memória genérica ou “o que faria sentido”.**

---

# 2. VISÃO GERAL DO PROJETO

Novydres é uma metrópole ártica vampiresca fundada como o **Novo Endereço de Gilgamesh, o Rei Legislador**, situada no extremo norte do Alasca, na zona urbana do Estreito de Bering. Em 2010 ela combina uma metrópole mortal semidemocrática, um domínio cainita juridicamente próprio e aliado à Camarilla, um sistema territorial radicalmente moldado pelo frio e pelo **Ermo**, instituições religiosas e jurídicas fortes, e uma crise de sucessão na ausência do fundador.

A cidade possui **9 raions oficiais**. O **Ermo não é um décimo raion**: é uma macrofeição geográfica transversal/intersticial. A malha urbana não deve ser lida como arquipélago; o principal agente de separação é o Ermo e o terreno hostil, não a água.

A estrutura cainita central é o **Concílio da Cruz e Espada**: instituição legítima e opressiva, com corrupção histórica pós-1917, cuja autoridade convive com disputas internas, Estados Livres, instituições religiosas, domínios clânicos e uma crise dinástica Mishkin.

A sucessão é polarizada por **Dominique Mishkin** e **Vladmir Mishkin**. A cidade continua marcada pela ausência de Gilgamesh, pelo Beckoning, pela Segunda Inquisição, pelo legado de Vasya Ivanoff e pela morte de Mikhail Mishkin.

O suplemento é concebido como **standalone V5**, com sistemas locais auditáveis, Criação de Personagem completa, Power Envelope, escala de poder de NPCs, Bairrismo, Marco Territorial, política/status/prestações, fé/ordem e um modo de criação Guiado baseado em história vivida e Provocações sem transformar idade em XP.

A frente visual de 2026-09 consolidou um **Master Map linework-first**, seguido por refinamento em tiles e carimbos de POIs. A relação de autoridade é unilateral:

> **MASTER MAP → TILES / STYLES / EXPORTS**

Nunca o contrário.

---

# 3. ÍNDICE DE WORKSTREAMS

| Workstream | Objetivo | Estado atual | Autoridade / artefatos | Última decisão material conhecida | Próxima ação |
|---|---|---|---|---|---|
| Governança editorial | Controle de versões, autoridade, retroatividade, revelação, standalone e formato | **CANÔNICO / FECHADO** na arquitetura | `novydres_editorial_governance_v1_0.md`, contratos correlatos | decisões devem ser propagadas sem sobrescrever fontes | manter como camada de governança |
| Editorial Map | Fonte de roteamento documental e estados de capítulos | **CANÔNICO / FECHADO** na versão mais nova encontrada | `novydres_editorial_map_v0_9_4.json` | capítulos 01–06 mapeados; Atlas 0.2.2 autoridade | usar para localizar owners; não tratá-lo como substituto do conteúdo |
| Capítulos 01–06 | Introdução, história, Atlas, facções, Concílio, fé | **CANÔNICO / FECHADO**, com pequenas dívidas documentais históricas | capítulos versionados 0.2.x | GAP-MIGRATION-001–006 encerrados | só reabrir por trigger material |
| Atlas / geografia textual | 9 raions, infraestrutura, POIs, visão player-safe | **CANÔNICO / FECHADO** como conteúdo; posições cardeais antigas têm dívida de sync com Master Map | `03_atlas_de_novydres_v0_2_2.md` | 32 POIs e 9 raions consolidados | sincronização futura apenas se editor aprovar patch cartográfico |
| Escala de poder NPC | Impedir power creep e calibrar a cidade | **CANÔNICO / FECHADO** na arquitetura; artefato v0.1.1 possui frontmatter de revalidação | `novydres_npc_power_scale_citywide_v0_1_1.md`, decisions | 106 decisões preservadas; geração individual passou a depender da arquitetura de personagem | retomar NPCs sob gates I/K |
| Criação A–K | Uma ontologia, dois modos, PCs/NPCs, coterie e integração | **CANÔNICO / FECHADO** na arquitetura do projeto; alguns arquivos ainda carregam status “candidate” | A–K + decision ledgers | K integrou uma ontologia e Rápido/Guiado | implementação/publicação, não redesign |
| Workstream L | Conteúdo Guiado, Provocações, Experiências, Episódios, Marcos | **EM DESENVOLVIMENTO** | prompt L + D1/D2/E/F/H/K | M1/M2 em stress test; erosão/continuidade fechada em princípios | continuar corpus a partir do estado validado |
| Workstream M | Calibração/playtest posterior | **PENDENTE / DOWNSTREAM** | referenciado por K/L | ainda não é autoridade sobre o corpus | executar após conteúdo suficiente |
| Capítulo 07 / NPCs | Perfis individuais coerentes com Power Scale e Criação | **EM DESENVOLVIMENTO** | Iskander, Zoya e fila de NPCs | arquitetura desbloqueada; perfis antigos devem ser revalidados, não descartados sem auditoria | revalidar/generar por prioridade |
| Dignitas / honrarias | Regionalizar autoridade Ventrue e premiações | **EM DESENVOLVIMENTO** | decisões em JSON/conversas | famílias Gilgamesh e Concílio fechadas; Mishkin/Ivanoff ainda abertas | consolidar capítulo/artefato próprio antes de publicação |
| Master Map | Fonte espacial total da cidade | **APROVADO / CONGELADO** na macroestrutura, com refinamentos locais e sync de POIs | imagem/master + regras cartográficas | macrogeografia/topologia/terrenos/mobilidade congelados; não fazer passe global arbitrário | consolidar versão editável final e registrar POIs selecionados |
| Transporte do Master Map | Vias, ferrovia, metrô e estações legíveis | **APROVADO COM CONDIÇÕES / refinamento** | decisões 08–22/09 | representação foi revisada várias vezes; rede ferroviária teve reset intermediário | aplicar somente a última convenção ao arquivo-base, sem alterar geografia |
| POIs visuais | Criar carimbos coerentes e integrá-los ao Master Map | **EM DESENVOLVIMENTO** | assets de Library + prompts/correções | maioria congelada; 18,19,23,24,25,31 pendentes; 27–30 descartados do fluxo visual | concluir fila pendente e QA pós-04 |
| Tiles | Refinamento local derivado do Master Map | **APROVADO COM CONDIÇÕES** | esquema 5×5 / 25 tiles | Home Tile único; overlaps só para continuidade; Crisol Home T20 | gerar/refinar apenas após Master atual |
| GIMP / pipeline final | Pós-processamento não destrutivo e export | **DECIDIDO / A OPERACIONALIZAR** | decisão 2026-09-27 | Work/Desktop + GIMP; XCF editável, PNG export | criar estrutura local versionada e manter changelog |
| Publicação/layout final | Transformar arquitetura em suplemento legível | **EM DESENVOLVIMENTO / PARCIAL** | Format Contract, matriz editorial, capítulos | antigas restrições rígidas de páginas foram retiradas em patches de governança | não restaurar metas antigas sem autoridade atual |
| Loresheets locais | Bairrismo/culto/linhagens e vínculos específicos | **MISTO: vários fechados, catálogo total não encerrado** | decisões por personagem/fação | Culto ao Rei Legislador, Legião de Aníbal, Rede Ártica etc. preservados | integrar sem criar duplicações |

---

# 4. CÂNONE DO MUNDO

## 4.1 Localização, escala e identidade

**CANÔNICO / FECHADO**

- Novydres situa-se no **norte do Alasca, zona urbana do Estreito de Bering**.
- Ano de referência: **2010**.
- O nome fundacional é **Novo Endereço de Gilgamesh, o Rei Legislador**.
- A fundação por Gilgamesh é registrada em **1423**.
- O Atlas atual descreve uma cidade com **mais de 8 milhões de habitantes**. Há registro anterior de aproximadamente **8,4 milhões**; a redação mais recente player-safe preferiu “mais de oito milhões”. Não normalizar os dois números sem patch editorial.
- A hipótese de Novydres ter sido originalmente território canadense e depois vendida aos EUA **não está fechada**. Existe como ideia histórica discutida, mas a data e a própria adoção final não foram confirmadas no cânone documental recuperado.

## 4.2 Cronologia âncora

| Data / período | Fato | Estado |
|---|---|---|
| **1423** | Gilgamesh cruza a região do Estreito de Bering e funda o Novo Endereço | **CANÔNICO / FECHADO** |
| **1632** | Pacto de Draco / base jurídica da presença Tzimisce | **CANÔNICO / FECHADO** |
| **1832** | Tratado de 1832 existe como premissa histórica importante ligada a Levi/Novydres | **CANÔNICO / FECHADO** quanto à existência; detalhes não reconstituídos aqui |
| **1917** | marco associado à corrupção posterior do Concílio | **CANÔNICO / FECHADO** como eixo de projeto; não explicar além da autoridade documental |
| **1945** | Wilhelmina Harker atua como general contra o Sabá | **CANÔNICO / FECHADO** |
| Era Beckoning | Vasya Ivanoff deixa a Regência; Samira al-Malik parte para a Gehenna War; vazio político se amplia | **CANÔNICO / FECHADO** |
| Pós-Beckoning | Mikhail Mishkin morre; narrativa oficial e verdade secreta divergem | **CANÔNICO / FECHADO** |
| **2010** | presente de jogo; Dominique × Vladmir; Concílio ainda governa; cidade sob múltiplas pressões | **CANÔNICO / FECHADO** |

### Mikhail Mishkin

**CANÔNICO / FECHADO**

- morreu pouco depois do Beckoning de Vasya;
- versão oficial: seu refúgio foi destruído pela Segunda Inquisição;
- verdade protegida: **Vladmir o matou em combate direto**;
- motivo associado: Vladmir julgava Dominique a favorita de Mikhail e inadequada ao legado de Gilgamesh.

Não transformar esta verdade protegida em conhecimento player-safe comum.

## 4.3 Governo mortal

**CANÔNICO / FECHADO**

Novydres possui estrutura mortal **semidemocrática**:

- Primeiro-Ministro eleito a cada quatro anos;
- representante das três grandes religiões escolhido por cúria conjunta entre líderes ortodoxos, muçulmanos e judeus;
- representante do governo dos EUA, normalmente senador ou emissário federal, cuja presença física varia;
- cada raion possui subprefeitura, conselho local, orçamento e autoridade real sobre serviços.

Serviços com importância diegética:

- aquecimento;
- transporte;
- comunicação;
- energia;
- obras;
- abastecimento;
- segurança urbana.

A desigualdade térmica é estrutural e política. Em Novydres, **calor é infraestrutura e poder**.

## 4.4 Governo cainita

**CANÔNICO / FECHADO**

Cadeia formal:

`Príncipe → Senescal → Regência`

Em 2010, a cadeia continua juridicamente relevante, mas a ausência/fragilidade de seus ocupantes faz dela mais princípio que paz.

O domínio de Novydres:

- é aliado à Camarilla;
- é juridicamente distinto;
- possui leis e instituições próprias;
- não deve ser reduzido a “mais uma cidade Camarilla”.

### Concílio da Cruz e Espada

**CANÔNICO / FECHADO**

- legítimo;
- opressivo;
- corrompido historicamente, com marco pós-1917;
- governa formalmente 7 dos 9 raions;
- convive com dois territórios fora de sua jurisdição plena;
- não é uma instituição falsa ou meramente decorativa.

Clãs historicamente representados no eixo do Concílio: Ventrue, Banu Haqim, Toreador, Malkavian, Nosferatu, Gangrel e Tzimisce. Brujah/Estados Livres ficam fora do arranjo central. Tremere possuem presença limitada e não devem ser automaticamente promovidos a assento político. O Ministério é historicamente banido no material de projeto.

## 4.5 Sucessão Mishkin e linhagem Ventrue

**CANÔNICO / FECHADO**

Genealogia fechada:

`Ventrue → Gilgamesh → Samira al-Malik → Vasya Ivanoff → Mikhail Mishkin → Dominique / Vladmir`

Gerações: **3 → 8**.

A disputa Dominique × Vladmir é central, mas não resume toda política da cidade.

### Casa Mishkin

**CANÔNICO / FECHADO em conceito; PENDENTE em algumas explicações**

A Casa Mishkin é:

- dinastia Ventrue;
- originalmente mortal;
- posteriormente transformada em instituição cainita;
- composta por sangue da Casa, ramos mortais, vinculados e adoções políticas.

**Sobrenome Mishkin não prova descendência de Vasya.**

Questão ainda aberta: por que a Casa produziu/absorveu tantos vampiros e qual é a explicação histórica completa para sua densidade cainita.

## 4.6 Figuras políticas e institucionais preservadas

### Wilhelmina Harker

**CANÔNICO / FECHADO em função e alinhamento conhecido**

- Primogênita Tzimisce.
- Guardiã política do Pacto de Draco.
- General contra o Sabá em 1945.
- Humanidade: **4**.
- Apoia Vladmir publicamente.
- Oposição explícita a Dominique baseia-se em permissividade excessiva, vagueza interpretativa das Leis de Sangue, abrigo de autoridade Camarilla externa e risco de erosão da soberania local/Pacto de Draco.
- Motivações ocultas adicionais não devem ser inventadas.

Convicção aceita:
> “Um juramento só é prisão até que se prove digno de ser território.”

Touchstone registrado:
**Dr. Elias Harker**.

### Kuthulun, “A Lua de Sangue”

**CANÔNICO / FECHADO no núcleo**

- Primogênita Gangrel.
- filha de Batu / descendente de Hannibal no material de linhagem.
- liderança conquistada no Gather.
- Humanidade: **5**.
- lealdade prioritária ao domínio de Novydres, não a um dos irmãos Mishkin.
- Loresheet aceita: **A Legião de Aníbal**.
- Não criar Loresheet individual redundante para Kuthulun.

Uma formulação de Conviction territorial foi proposta anteriormente, mas não deve ser elevada a cânone sem registro explícito de aprovação.

### Miriam Abramovich

**CANÔNICO / FECHADO no núcleo**

- ligada à **Rede Ártica**;
- possui também **A Linhagem de Miriam**;
- participa pessoalmente do Concílio;
- Yonah pode falar em seu nome em circunstâncias apropriadas.

### Grigori Vasiliev

**CANÔNICO / FECHADO na ficha-base citada**

- Matusalém, 5ª Geração;
- Blood Potency **6**;
- prioridade disciplinar: Blood Sorcery > Animalism > Obfuscate > Oblivion > Auspex;
- Loresheets: **A Linhagem de Grigori** e **O Escafandro dos Amaldiçoados**;
- não adicionar terceiro Loresheet individual sem decisão nova.

## 4.7 Raions: autoridade política e função urbana

> **IMPORTANTE:** a tabela abaixo separa o **cânone funcional do Atlas** das **posições do Master Map de setembro**, porque as posições cardeais mudaram durante a construção cartográfica.

| Raion | Controle / função canônica | “Posição no mapa” do Atlas 0.2.2 | Layout do Master Map de setembro | Estado do conflito |
|---|---|---|---|---|
| Dunwich | Gangrel; fronteira, vilas, caça, travessias | Noroeste | Norte/Nordeste | posição textual antiga deve ser sincronizada; função não muda |
| Levi | Malkavian; memória, Rede Ártica, pesquisa discreta | Norte | Norte | compatível |
| Alexandria | Lasombra; jurídico, documentos, passagem, costa | Nordeste | Leste/Sudeste | posição textual desatualizada frente ao Master |
| Chelsea / Old Town | Estados Livres; pobreza, religião, calor falho, anarquismo | Oeste | Sudeste | posição textual desatualizada frente ao Master |
| Bukovie | Ventrue; centro financeiro/administrativo | Centro | núcleo central, associado ao eixo Midtown sem criar décimo raion | compatível em função |
| New London | Banu Haqim; diplomacia, direito, canais mornos | Leste | Sul-central | posição textual desatualizada frente ao Master |
| Sulfok | disputado; indústria, aeroporto, porto, ferrovia | Sudoeste | Leste/Nordeste | conflito cartográfico explícito; usar Master para render |
| Drevnigrad | Tzimisce; bairros antigos, matadouros, tradição territorial | Sul | Oeste/Noroeste | posição textual desatualizada frente ao Master |
| Vasyl Bay | Toreador; fé pública, universidade, penitência | Sudeste | Sudoeste | posição textual desatualizada frente ao Master |

**APROVADO COM CONDIÇÕES:** para mapas, o Master Map posterior é a autoridade espacial. O Atlas 0.2.2 permanece autoridade de lore até patch específico. Isso é uma dívida de sincronização documental, não licença para reescrever o Atlas inteiro.

## 4.8 Ermo

**CANÔNICO / FECHADO**

- não é raion;
- não é parque;
- não é “zona 10”;
- é macrofeição transversal/intersticial;
- separa bairros/raions mais do que a água;
- produz rotas perigosas, corredores congelados, postos, infraestrutura abandonada e assimetria de acesso.

## 4.9 Rio Vasyl / Reka Vasilya

**CANÔNICO / FECHADO**

- eixo térmico natural;
- corpo principal ligado a Chelsea;
- canais subterrâneos emergem em New London;
- deságue/integração portuária em Sulfok;
- desigualdade térmica e acusações de desvio para Bukovie são politicamente relevantes;
- a causa, intenção e extensão do desvio permanecem disputadas na ficção.

## 4.10 Fé e instituições religiosas

Três pilares religiosos principais:

1. Ortodoxia;
2. Islã;
3. Judaísmo.

Âncoras:

- **Catedral de Santa Sophia** — Ortodoxia, Vasyl Bay;
- **Grande Mesquita de Al-Nur** — Islã, Alexandria;
- **Grande Sinagoga Beit HaZikaron** — Judaísmo, Chelsea.

Os clãs associados são pilares históricos/influências, **não proprietários absolutos** das instituições.

### Ordem Urukiana

**CANÔNICO / FECHADO na estrutura-base**

- **Chancelaria do Saber**;
- **Legião da Coroa de Ferro**;
- **Círculo do Santo Vasyl Dreznov**.

Não fundir essas três estruturas nem tratá-las como nomes alternativos da mesma coisa.

## 4.11 Segunda Inquisição

**CANÔNICO / FECHADO como ameaça estrutural**

Opera por múltiplas superfícies urbanas e institucionais. O projeto preserva operações/nomes como **Tiamat** e **Nergal** em contextos próprios. Não converter toda presença federal, jurídica, portuária ou religiosa em SI sem evidência local.

---

# 5. SISTEMA, REGRAS E MECÂNICAS

## 5.1 Princípio de sistema

**CANÔNICO / FECHADO**

Novydres é V5 com regras locais. O suplemento final deve ser utilizável à mesa sem software obrigatório. Matrizes, flags, JSONs e ledgers são ferramentas editoriais; não devem virar burocracia obrigatória para o jogador salvo decisão explícita de publicação.

## 5.2 Ontologia comum

K fechou uma ontologia comum para PCs, NPCs, Rápido e Guiado. Oito superfícies editoriais:

1. estado mecânico;
2. estado narrativo atual;
3. estado histórico;
4. estado subjetivo/memória;
5. estado social/territorial;
6. estado relacional;
7. estado de coterie/grupo;
8. proveniência/protegido/desconhecido.

Isso **não** significa oito formulários obrigatórios para o jogador.

## 5.3 Power Envelope

**CANÔNICO / FECHADO**

Regra central:

`autorização de poder ≠ orçamento econômico ≠ profundidade de resolução ≠ auditoria pós-ficha`

- B / Power Envelope autoriza o tipo de poder possível.
- G estrutura economia do Rápido.
- H estrutura construção Guiada.
- I decide profundidade de resolução de NPC.
- Power Scale/B auditam o resultado materializado.

### Invariantes

- Geração ≠ idade ≠ Blood Potency.
- Idade não concede poder automaticamente.
- Anos ativos não viram XP.
- Torpor não gera créditos mecânicos.
- Excepcionalidade exige causalidade/proveniência.
- Fraquezas não “pagam” poder.
- Autoridade institucional não equivale a capacidade de confronto.
- História longa não equivale a onisciência.
- `unknown ≠ absent ≠ false ≠ not applicable`.

### Perfis internos de B

Nomes internos provisórios:

- Baseline;
- Established;
- Advanced;
- estado excepcional/outlier separado.

Não publicar esses nomes automaticamente. “Elder” não implica Advanced; Advanced não implica elder.

### Gate de exceção

Baixa Geração, alto Depth/Breadth, Power Density e combinações raras geram **rarity debt** qualitativa e podem exigir:

- ajuste;
- justificação;
- autorização;
- excepcionalidade formal.

## 5.4 Custos econômicos exatos da Criação Rápida

**CANÔNICO / FECHADO**

| Traço | Regra de custo | Rating 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| Attribute | novo nível ×5 | 5 | 15 | 30 | 50 | 75 |
| Skill | novo nível ×3 | 3 | 9 | 18 | 30 | 45 |
| Clan Discipline | novo nível ×5 | 5 | 15 | 30 | 50 | 75 |
| Out-of-Clan Discipline | novo nível ×7 | 7 | 21 | 42 | 70 | 105 |
| Caitiff / Thin-Blood Discipline | novo nível ×6 | 6 | 18 | 36 | 60 | 90 |
| Blood Potency | novo nível ×10 | 10 | 30 | 60 | 100 | 150 |

Traços lineares:

- Specialty nova: **3 XP**;
- Advantage / Merit / Background / Loresheet: **3 XP por dot**;
- Blood Sorcery Ritual: **nível ×3 XP**;
- Thin-Blood Formula: **nível ×3 XP**.

Flaws não geram XP.

## 5.5 Geração e Blood Potency

**CANÔNICO / FECHADO**

- Generation é independente do chassis.
- Generation em si custa **0 XP**.
- escopo de Criação Rápida permite aproximadamente **14ª até 4ª Geração**, sujeito à legalidade aplicável.
- BP de referência do chassis não é subsídio.
- Se a Geração exigir BP mínimo acima da referência, o personagem paga o custo integral desse BP usando o mesmo orçamento global.
- não existe compensação por escolher Geração baixa.

Regra B:

`Generation hard bounds → Profile envelope → Trajectory validation → Final BP`.

A tabela oficial completa de hard bounds por Geração não é reimpressa neste handoff; ela permanece autoridade do baseline V5/admission layer. Não preencher de memória.

## 5.6 Bairrismo

**CANÔNICO / FECHADO no conceito; implementação detalhada pertence ao truth-home próprio**

- ligação social/territorial profunda;
- progressiva para recém-chegados;
- não é rating universal novo;
- não concede bônus automático de resistência só por existir;
- não decorre de idade, Geração ou BP;
- deve aparecer organicamente em história, relações, território e escolhas.

## 5.7 Marco Territorial

**CANÔNICO / FECHADO no conceito-base**

- Touchstone urbano adicional;
- possui custo/risco próprios;
- recém-chegados só o estabelecem depois de enraizamento;
- não confundir com Touchstone humano comum;
- não inventar a mecânica completa dentro do workstream C/G: ela tem autoridade própria.

## 5.8 Loresheet “Culto ao Rei Legislador”

**CANÔNICO / FECHADO**

- níveis **1–5**;
- criação permite até **nível 2**;
- não dar acesso ilimitado a autoridade de Gilgamesh por custo baixo.

## 5.9 Coterie

**CANÔNICO / FECHADO na arquitetura J2**

- não é terceiro modo de criação;
- Quick Character Creation não cria coterie;
- existe superfície separada de **Quick Coterie Creation DEU**;
- coterie formal em Novydres exige fundamento/razão e sanção apropriada do Príncipe/autoridade;
- grupos informais podem ser clandestinos;
- no Guiado, coterie pode surgir organicamente na história sem criar lifepath paralelo.

## 5.10 Status, cargos, Dignitas e Prestações

A Criação consome os sistemas dos capítulos/artefatos de autoridade. Não deve duplicá-los.

- Status pessoal exige base mecânica/legal e proveniência social reconhecida.
- cargo exige premissa, autoridade, elegibilidade e **Office Functional Fit**.
- múltiplos cargos não geram automaticamente soma arbitrária de Status Posicional.
- Prestações e dívidas devem permanecer causalmente legíveis.

### Dignitas

**EM DESENVOLVIMENTO / parte fechada**

Dignitas é hierarquia Ventrue interna. Cargos do Concílio podem testemunhar/justificar feitos, mas não concedem Dignitas sozinhos.

Autoridades válidas já registradas:

- Gerúsia;
- Praetor;
- Strategos;
- Diretoria/Board.

#### Honrarias de Gilgamesh — fechadas

| Honraria | Nível |
|---|---:|
| Selo do Rei Legislador | 3 |
| Portador da Muralha | 3 |
| Guardião da Tábua | 2 |
| Touro de Uruk | 4 |
| Coroa da Primeira Muralha | 5 |

#### Honrarias do Concílio — fechadas

| Honraria | Nível |
|---|---:|
| Edito Vermelho | 2 |
| Mandato Cruzado | 3 |
| Corrente do Jurista | 3 |
| Estandarte Negro | 4 |
| Pacto Imperial | 5 |

Famílias Mishkin e Ivanoff: **PENDENTE DE DECISÃO / consolidação**. Não transformar propostas antigas em catálogo final.

---

# 6. CRIAÇÃO DE PERSONAGEM

## 6.1 Arquitetura final

**CANÔNICO / FECHADO**

Existem exatamente dois modos:

1. **Rápido**
2. **Guiado**

Ambos servem PCs e NPCs.

Invariante:

`QUICK ⊆ GUIDED ⊆ COMMON MODEL`

Difere o procedimento, não a legalidade final.

NPC “Integral / Abbreviated / Operational” é profundidade editorial de resolução, não modo de criação.

## 6.2 Fluxo Rápido

Ordem consolidada:

1. autorização pré-ficha de Power Profile / excepcionalidade em B;
2. escolha de chassis compatível;
3. geometria independente de Attributes;
4. geometria independente de Skills;
5. geometria independente de Disciplines;
6. totais lineares;
7. Generation/BP;
8. gasto do XP restante;
9. Predator Type quando aplicável;
10. Flaws;
11. Humanity / Convictions / Touchstones;
12. History definitiva;
13. estado atual em Novydres;
14. Relationship Map;
15. auditoria localizada/pós-ficha.

### REGRA → MOTIVO → ERRO QUE EVITA

**REGRA:** chassis não autoriza poder.  
**MOTIVO:** chassis é economia de construção; B define envelope.  
**ERRO QUE EVITA:** usar “Methuselah” como passe automático para múltiplas Disciplines 5 ou baixa Geração.

## 6.3 Matriz econômica dos cinco chassis

| Chassis | Valor materializado | Budget adicional sobre Child | XP livre autorizado |
|---|---:|---:|---:|
| Child of the Night | **379** | **+0** | **0** |
| Neonate | **519** | **+140** | **0** |
| Ancilla | **653** | **+275** | **1** |
| Elder | **1,044** | **+670** | **5** |
| Methuselah | **1,574** | **+1,195** | **0** |

Observação indispensável:

- Ancilla materializa 653 e conserva 1 XP livre dentro de orçamento autorizado de 654.
- Elder materializa 1,044 e conserva 5 XP livres dentro de orçamento autorizado de 1,049.
- não “corrigir” os valores materializados para igualar o budget: o XP livre é deliberado.

## 6.4 Custo por superfície

| Chassis | Attributes | Skills | Disciplines | Advantages | Specialties | BP | Livre |
|---|---:|---:|---:|---:|---:|---:|---:|
| Child | 205 | 120 | 20 | 21 | 3 | 10 | 0 |
| Neonate | 240 | 150 | 65 | 42 | 12 | 10 | 0 |
| Ancilla | 270 | 177 | 95 | 63 | 18 | 30 | 1 |
| Elder | 325 | 225 | 320 | 81 | 33 | 60 | 5 |
| Methuselah | 400 | 300 | 600 | 126 | 48 | 100 | 0 |

Os valores são referência de engenharia dos presets. O orçamento total é global; o jogador não fica preso a quotas por superfície quando construir legalmente por XP.

## 6.5 Geometrias

Aplicam-se **somente** a:

- Attributes;
- Skills;
- Disciplines.

Não se aplicam a Generation, BP, Humanity, Flaws, Predator Type, Convictions/Touchstones, Advantages lineares, Specialties ou derivados.

Cada superfície pode usar uma geometria diferente.

- **Specialist** — picos concentrados e vales reais.
- **Balanced** — mistura de picos, suporte e cobertura.
- **Generalist** — cobertura ampla com prioridades visíveis; não significa preencher tudo.

## 6.6 Arrays exatos — Attributes / Skills / Disciplines

### Child of the Night

**Attributes — 205 XP**

- Specialist: `4/4/3/3/2/2/1/1/1`
- Balanced: `4/3/3/3/2/2/2/2/1`
- Generalist: `3/3/3/3/3/3/2/1/1`

**Skills — 120 XP**

- Specialist: `4/3/3/3/2/2/2/1/1/1`
- Balanced: `3/3/3/2×5/1×7`
- Generalist: `3/2×8/1×10`

Breadth: `10 / 15 / 19`.

**Disciplines — 20 XP**

Todas: Clan `2/1`. Deliberate **Floor Collapse**.

**Valores comuns**

- Advantages: 7 dots
- Specialties: 1
- BP ref.: 1
- Flaws mín.: 2 dots
- Humanity: 6–8, ref. 7
- Predator Type: nenhum

### Neonate

**Attributes — 240 XP**

- Specialist: `5/4/3/3/2/2/2/1/1`
- Balanced: `4/4/3/3/3/2/2/2/1`
- Generalist: `4/3×6/1×2`

**Skills — 150 XP**

- Specialist: `5/3×4/2×3/1×2`
- Balanced: `4/3×4/2×4/1×4`
- Generalist: `4/3/2×8/1×10`

Breadth: `10 / 13 / 20`.

**Disciplines — 65 XP**

- Specialist: Clan `4/2`
- Balanced: Clan `3/3/1`
- Generalist: Clan `3` + out-of-Clan `2/1/1`

**Comuns**

- Advantages: 14 dots
- Specialties: 4
- BP ref.: 1
- Flaws mín.: 3
- Humanity: 5–8, ref. 7
- Predator Type: sim

### Ancilla

**Attributes — 270 XP**

- Specialist: `5/4/4/3/2/2/2/2/1`
- Balanced: `4/4/4/3/3/2/2/2/2`
- Generalist: `5/3×5/2×3`

**Skills — 177 XP**

- Specialist: `5/4/3×4/2×3/1`
- Balanced: `4/4/3/3/2×7/1×6`
- Generalist: `4/3/3/2×10/1×7`

Breadth: `10 / 17 / 20`.

**Disciplines — 95 XP**

- Specialist: Clan `5/2/1`
- Balanced: Clan `4/3/2`
- Generalist: Clan `3/2/2` + out-of-Clan `2/1/1`

**Comuns**

- Advantages: 21 dots
- Specialties: 6
- BP ref.: 2
- Flaws mín.: 4
- Humanity: 5–7, ref. 6
- Predator Type: sim
- Free XP: 1

### Elder

**Attributes — 325 XP**

- Specialist: `5/5/5/4/3/1/1/1/1`
- Balanced: `5/5/4/3/3/3/2/2/1`
- Generalist: `5/4/4/3/3/3/3/2/2`

**Skills — 225 XP**

- Specialist: `5/5/4/4/3×3/2×2/1`
- Balanced: `5/4/4/3×4/2×4/1×4`
- Generalist: `5/4/3×3/2×9/1×5`

Breadth: `10 / 15 / 19`.

**Disciplines — 320 XP**

- Specialist: Clan `5/5/3` + out-of-Clan `4/4`
- Balanced: Clan `5/5/3` + out-of-Clan `4/3/2/1`
- Generalist: Clan `4/3/3` + out-of-Clan `4/3/3/2/2/1/1`

**Comuns**

- Advantages: 27 dots
- Specialties: 11
- BP ref.: 3
- Flaws mín.: 6
- Humanity: 4–7, ref. 5
- Predator Type: sim
- Free XP: 5

### Methuselah

**Attributes — 400 XP**

- Specialist: `5/5/5/5/3/3/3/1/1`
- Balanced: `5/5/5/4/4/3/2/2/2`
- Generalist: `5/4/4/4/4/4/3/3/2`

**Skills — 300 XP**

- Specialist: `5×3/4×3/3×3/2×2/1`
- Balanced: `5×2/4×2/3×5/2×5/1×5`
- Generalist: `5/4/3×7/2×10/1×3`

Breadth: `12 / 19 / 22`.

**Disciplines — 600 XP**

- Specialist: Clan `5/5/3` + out-of-Clan `5/5/5/5`
- Balanced: Clan `5/5/3` + out-of-Clan `5/5/4/4/4`
- Generalist: Clan `5/5/3` + out-of-Clan `5/3×6/2×3`

**Comuns**

- Advantages: 42 dots
- Specialties: 16
- BP ref.: 4
- Flaws mín.: 8
- Humanity: 3–7, ref. 4
- Predator Type: sim

### Gate B ↔ G

Presets não são entitlement. Exemplos registrados:

- Neonate `4/2` já pressiona Profile 1.
- Ancilla `5/2/1` é materialmente Profile 3/exceção em envelopes inferiores.
- Elder requer auditoria de composição.
- Methuselah com múltiplas Disciplines 5 exige caminho excepcional quando B não tiver autorizado outlier.

## 6.7 Flaws

**CANÔNICO / FECHADO**

Mínimos:

`Child 2 / Neonate 3 / Ancilla 4 / Elder 6 / Methuselah 8 dots`

- medidos em dots, não quantidade de Flaws;
- sem artificial cap de concentração quando as regras permitirem;
- extras não geram XP;
- só Flaws materialmente relevantes/não redundantes contam;
- Flaws relacionais ativos entram no Relationship Map.

## 6.8 Humanity

**CANÔNICO / FECHADO**

- Child: `6–8`, referência 7
- Neonate: `5–8`, referência 7
- Ancilla: `5–7`, referência 6
- Elder: `4–7`, referência 5
- Methuselah: `3–7`, referência 4

Idade não reduz Humanity automaticamente.

## 6.9 Predator Type

**CANÔNICO / FECHADO**

- Child: nenhum
- Neonate+: sim
- pacote fixo;
- não converte benefícios em XP fungível.

## 6.10 Convictions e Touchstones

**CANÔNICO / FECHADO**

- não escalam por chassis;
- Convictions devem funcionar como princípios operacionais, não slogans abstratos;
- precisam ser causalmente legíveis na History;
- Touchstones atuais/significativos aparecem no Relationship Map.

## 6.11 History Rápida: cinco capítulos

**CANÔNICO / FECHADO para escrita direta do modo Rápido**

1. **A Ilusão de Estabilidade**
2. **A Fissura**
3. **A Negociação com o Abismo**
4. **O Ponto de Ruptura**
5. **A Adaptação Sombria**

**Não cometer o erro de declarar que esses cinco capítulos são automaticamente os cinco Marcos processuais de D1/L.** O próprio artefato G afirma que eles são funções narrativas de consolidação para o modo Rápido.

## 6.12 Guiado

**CANÔNICO / FECHADO na arquitetura; corpus em desenvolvimento**

Fluxo:

`autorizar → semear → descobrir/alocar → consolidar`

Princípios:

- mesma legalidade e economia autorizada do Rápido;
- jogador não recebe orçamento secreto extra por viver mais história;
- Provocações/Episódios justificam, descobrem e alocam estado autorizado;
- idade/era/Episódio não gera XP;
- perdas podem ser permanentes;
- não existe refund automático;
- conclusão ocorre quando Marcos aplicáveis têm cobertura suficiente, não quando prompts ou XP foram “zerados”;
- sem fase adicional obrigatória depois do fechamento;
- artefato final é equivalente ao Rápido;
- **Caderno de Trajetória** é opcional e não mecânico.

---

# 7. NPCs, FACÇÕES E ESCALA DE PODER

## 7.1 Escala de poder

**CANÔNICO / FECHADO**

Não existe “Power Score” universal.

A arquitetura audita dimensões como:

- estrato/antiguidade;
- rootedness;
- Generation;
- BP;
- Discipline Depth;
- Breadth;
- Mastery Load;
- Power Density;
- competência;
- capacidade de confronto;
- autoridade institucional;
- capacidade mobilizável;
- leverage social;
- alcance histórico;
- vantagem territorial;
- conhecimento;
- dependências;
- poder coletivo.

**NPC-POWER-001..106** permanecem a ledger preservada.

## 7.2 Profundidade de resolução NPC

I trabalha com perfis editoriais internos de resolução — Integral, Abbreviated e Operational — mais tratamentos protegidos/legendários. Esses rótulos não devem ser automaticamente publicados para jogador.

Menor resolução significa menos informação explicitada, **não** que traços ou história “não existam”.

## 7.3 Perfis de teste existentes

### Iskander Yasupov

Perfil antigo completo, mas a mecânica deve ser revalidada contra a arquitetura final.

Pontos-alvo de revalidação já registrados:

- Generation 8;
- BP 4;
- Discipline Depth/Breadth/Power Density;
- dependências;
- Bairrismo/rootedness;
- Beckoning;
- Office Functional Fit.

Não reconstruir do zero sem primeiro testar o perfil existente.

### Madame Zoya

Revalidar:

- Generation 11;
- BP 2;
- Discipline/ritual breadth;
- dependências rituais;
- Bairrismo/rootedness;
- múltiplos cargos sem stacking indevido de Status;
- Revelation protection;
- três rituais que permaneceram uma superfície não resolvida em revisões anteriores.

## 7.4 Fila de NPCs preservada

Principal:

- Kuthulun;
- Bishop Konstantin;
- Wilhelmina Harker;
- Dom Sebastião de Avis;
- Miriam Abramovich;
- Fatima al-Faqadi;
- Zara/Zarina;
- Sergei Orlov;
- Khalil Al-Rashid.

Secundários/dependentes conforme necessário:

- Mikhail Vasiliev;
- Mariya Vasilieva;
- Leah ben Avraham.

Legendários/protegidos:
- Gilgamesh;
- Levi;
- Baba Yaga;
- Durga Syn.

Não transformar “fila” em ordem rígida se o próximo episódio editorial exigir dependência diferente.

---

# 8. CAMPANHA, EXPERIÊNCIAS, PROVOCAÇÕES E MARCOS

## 8.1 D1 — estrutura de Played History

**CANÔNICO / FECHADO**

Fluxo de Episódio:

`entrada → provocação → decisão/interpretação → consequência → saída`

Princípios:

- cronologia contínua com saltos flexíveis;
- densidade de Episódios segue **Significant Coverage**, não idade;
- períodos quietos podem existir como **Intervalos de Continuidade**;
- Provocações esgotadas deixam de gerar Episódios;
- Marcos são contratos funcionais de fechamento;
- Power Envelope não pode ser criado/destruído livremente pelo processo narrativo.

## 8.2 Workstream L

**EM DESENVOLVIMENTO**

Estrutura de trabalho aprovada:

`Provocação → Experiência → Episódio → Marco`

Marcos não são “eras”. Eles cumprem função dramática/de construção.

Estado recuperado:

- **M1 — A Ilusão de Estabilidade**
- **M2 — A Fissura**
- alvo inicial: **20 Provocações por Marco**
- sorteio/seleção: **2d10**
- Incidências I–III podem romper homeostase positiva ou negativamente; não significam automaticamente dano.

### ATENÇÃO SEMÂNTICA

Os nomes M1/M2 coincidem com os dois primeiros capítulos da History Rápida. Isso não autoriza afirmar que todos os cinco capítulos de G são automaticamente os cinco Marcos de L. Apenas M1/M2 foram explicitamente recuperados neste workstream.

## 8.3 Stress tests preservados

Playtest inicial:

- 2 personagens: um Matusalém e uma Criança da Noite;
- rodar M1→M2;
- tentativa de forçar cobertura integral gerou rerolls excessivos;
- faixa registrada: aproximadamente **42–113 rerolls** em cenários de cobertura forçada;
- conclusão: cobertura suficiente/coerente é preferível a “marcar cada prompt”.

Resultados registrados:

- M1: 7/8 Experiences em um teste de cobertura;
- M2: 8/8;
- 3/4 Episodes em uma configuração de stress.

Pesos de teste registrados em material de trabalho:

- M1: `5 / 4 / 3 / 2`
- M2: `6% / 4% / 2%`

**PROVISÓRIO / PLAYTEST:** preservar os valores como dado de calibração; não extrapolar interpretação matemática nova sem o ledger L que os originou.

## 8.4 Levi como stress test longitudinal

Premissas preservadas:

- Matusalém com mais de 2.000 anos;
- 83 Experiences no stress test citado;
- múltiplos ciclos de construção, perda, torpor, migração, sucessão, erosão e retorno;
- Senescal de Gilgamesh;
- Novydres, Miriam e Tratado de 1832 preservados como premissas;
- 1917 não deve ser usado para inventar explicação definitiva do desaparecimento.

## 8.5 Erosão e Continuidade

**CANÔNICO / FECHADO como princípio L**

- perdas afundam XP; não há refund;
- Continuity pode preservar investimento;
- preservação pode exigir erosão autobiográfica ou reformulação de identidade;
- material/institucional/relacional pode ser destruído sem apagar automaticamente o passado;
- torpor, obsolescência, deslocamento e reconstrução são formas possíveis de transformação;
- Quick/Guided precisam convergir sem prêmio sistêmico de poder ao Guiado.

---

# 9. CARTOGRAFIA — REGRAS CANÔNICAS

## 9.1 Autoridade

**CANÔNICO / FECHADO**

- 9 raions.
- Ermo transversal.
- Master Map é autoridade espacial principal.
- tiles são derivados do Master Map.
- Styles/exports não podem introduzir geografia nova.

## 9.2 Tamanho e composição do Master de referência

**APROVADO / CONGELADO no checkpoint**

- alvo conceitual: **1536×1536**;
- linework-first;
- handmade;
- noir/gótico;
- quase monocromático frio;
- preto/carvão/cinza frio com vinho/oxblood/vermelho queimado como acento;
- alto contraste controlado.

O tamanho 1536² é checkpoint de produção, não licença para perder resolução no pós-processamento. Upscale/export podem ser posteriores.

## 9.3 Geografia atual do Master

Layout consolidado de setembro:

- Bukovie / eixo Midtown: núcleo;
- Drevnigrad: O/NO;
- Levi: N;
- Dunwich: N/NE;
- Sulfok: L/NE;
- Alexandria: L/SE;
- New London: S-central;
- Vasyl Bay: SO;
- Chelsea / Old Town: SE;
- O Crisol: extremo SE, ilha/península fortificada conforme leitura costeira final.

**REGRA:** água não é principal separador.  
**MOTIVO:** a cidade deve parecer metrópole ártica fragmentada pelo Ermo, não arquipélago.  
**ERRO QUE EVITA:** cada raion virar uma “ilha urbana” autônoma.

## 9.4 Terrenos

Camadas importantes:

- água quase preta;
- gelo claro;
- terreno congelado explícito;
- rocha com hachura angular;
- vegetação discreta;
- pântano orgânico;
- relevo por curvas/hachuras;
- neve/tundra limpa;
- industrial por pátios/trilhos;
- Ermo com leitura física real, sem fronteira artificial.

Não é necessário um polígono genérico de “área urbana”.

## 9.5 Vias

Decisão mais recente consolidada:

- não manter divisão obrigatória entre rua local/coletora/arterial como categorias publicadas;
- uma categoria comum de **Rua** pode carregar a identidade gráfica antes atribuída à coletora;
- autoestradas/rotas maiores devem continuar perceptíveis quando existentes;
- malha não deve ser simplificada a ponto de perder densidade urbana.

Polígonos viários experimentais foram removidos num reset intermediário.

## 9.6 Ferrovia

### Histórico de mudanças

1. versão anterior: **dois trilhos paralelos + travessas**;
2. revisão posterior: linha branca simples/traços sequenciais;
3. revisão de 22/09 consolidada no registro de projeto: **linha única escura + dormentes regulares**, sem dupla linha, sem simples tracejado e sem serrilhado.

Portanto:

**SUPERADO:** “duas linhas paralelas” como regra final.  
**SUPERADO:** “ferrovia = linha tracejada simples” como regra final.  
**ATUAL:** linha única escura com dormentes regulares.

Rede lógica:

- núcleo ferroviário ao norte em área pouco ocupada;
- entroncamentos/derivações;
- ramais contínuos e conectados;
- independência da malha rodoviária;
- ferrovia pode cruzar por cima/baixo;
- ferrovia nunca “vira rua”.

Houve um **reset intermediário** em que ferrovias e estações foram removidas do arquivo. Isso não equivale a decisão de abolir a ferrovia da cidade.

## 9.7 Estações

Convenção recuperada:

- ferroviária: retângulo/barra conforme versão de legenda corrente;
- metrô: círculo, com `M` branco na variante mais recente de legenda.

A ausência visual de estações em passes intermediários foi um defeito/pendência, não retcon de infraestrutura.

## 9.8 Metrô

- linha única com tracejado curto;
- deve ser legível contra terreno e vias;
- não confundir com ferrovia;
- sem camada própria de bonde/tram no Master atual.

### Bondes

**PENDENTE / NÃO REPRESENTADOS**

A camada de bondes não foi adotada no Master atual. Não desenhar por inferência.

## 9.9 Aeroporto e porto

Devem ser discretos como infraestrutura cartográfica, mas reconhecíveis:

- Aeroporto Internacional em Sulfok;
- Docas Quebra-Gelo em Sulfok;
- relação logística com ferrovia/indústria sem transformar a cidade em diagrama técnico.

## 9.10 POIs no mapa

- POIs selecionados devem existir no Master Map.
- Não colocar carimbo em tile se o POI não tiver posição/master footprint.
- POIs não devem virar microedifícios genéricos.
- no mapa macro, POI deve ser mais detalhado que tecido comum, mas subordinado à geografia.
- halos, quando usados, devem ser discretos e orgânicos; “halo tecnológico” foi rejeitado.
- `O Crisol` é exceção insular deliberada.

## 9.11 Labels

A regra visual madura proíbe saturação de labels no campo cartográfico:

- sem nomes de ruas;
- sem etiquetas de POI sobre cada objeto;
- sem transformar distritos em placas enormes;
- título/legenda podem existir como interface do mapa, separados da geografia.

---

# 10. MASTER MAP — ESTADO DETALHADO

## 10.1 Estado de freeze

**APROVADO / CONGELADO na macroestrutura**

Checkpoint aprovado:

- geografia;
- topologia;
- posições macro de POIs;
- mobilidade;
- terrenos;
- atmosfera;
- Crisol;
- moldura/título/legenda como composição.

Não fazer novo passe global sem causa.

### Única classe de edição permitida sem reabrir o macrodesign

- limpeza;
- legibilidade;
- correção de representação gráfica de camadas já decididas;
- integração de POI aprovado;
- ajuste local necessário ao tile;
- pós-processamento que não altera a topologia.

## 10.2 Microarquitetura comum

**REJEITADO / REMOVIDO**

A tentativa de preencher toda a cidade com microedifícios reduziu legibilidade e competiu com POIs.

Regra atual:

- tecido urbano por malha/linework;
- não modelar cada casa/edifício comum;
- POIs singulares recebem leitura arquitetônica superior.

## 10.3 O Crisol

**APROVADO / CONGELADO — freeze forte**

- extremo sudeste;
- leitura de prisão moderna sobre fortaleza/estrutura antiga;
- não castelo de fantasia;
- isolado sem virar motivo para toda cidade ser arquipélago;
- metrô e ferrovia não entram no complexo;
- conexão viária/causeway única conforme checkpoint;
- estruturas de crucificação vazias permanentes fazem parte do POI;
- Home Tile corrigido para **T20**, não T25, no esquema 5×5.

## 10.4 Tiles

**APROVADO COM CONDIÇÕES**

Esquema atual recuperado:

- **5×5 = 25 tiles**;
- T13 = centro;
- cada POI possui **Home Tile** único;
- overlap só para continuidade visual/footprint;
- tile não redefine posição;
- footprints densos preliminares não são automaticamente canônicos.

### SUPERADO

- antigo esquema **3×3 / 9 tiles** é histórico e não deve reaparecer como grade atual.
- códigos antigos A1–C3 continuam úteis apenas para rastrear prompts legados, não para produção nova.

---

# 11. REGISTRO COMPLETO DE POIs

## 11.1 Regra de dupla camada

O Atlas 0.2.2 contém **32 POIs canônicos como conteúdo**. O fluxo visual mais novo descartou **27–30**. Não existe evidência suficiente neste handoff de que o descarte visual tenha sido acompanhado por retcon editorial do Atlas.

Portanto:

- **conteúdo/lore:** 27–30 ainda existem no Atlas fechado;
- **asset visual atual:** 27–30 = REJEITADO / DESCARTADO;
- **publicação final:** requer sincronização explícita para decidir se permanecem como locais sem carimbo ou se haverá retcon editorial.

Não apagar silenciosamente.

## 11.2 Tabela mestre

| # | POI | Raion textual | Estado visual atual | Diretriz / observação de produção |
|---:|---|---|---|---|
| 01 | Torre de Inverno | Bukovie | **APROVADO / CONGELADO; sujeito a QA pós-04** | arranha-céu oligárquico contemporâneo; vidro/aço/pedra; podium; setbacks; coroamento severo; sem igreja/castelo |
| 02 | Palácio de Âmbar | Bukovie | **APROVADO / CONGELADO; corrigido** | imperial russo sóbrio; corpo central + alas; sem francês/Beaux-Arts/mansardas/cúpula cortesã |
| 03 | Exchange Hall | Bukovie | **APROVADO / CONGELADO; sujeito a QA** | bolsa histórica; pórtico monumental; neoclássico tardio com influência imperial russa; riqueza contida |
| 04 | Feudo Pessoal de Dominique Mishkin | Bukovie | **APROVADO / CONGELADO** | domínio murado privado, vila viva; portões modernos plausíveis; mansão, mercado, escola, hospital/reformatório, bosque; evitar simetria palaciana/medieval |
| 05 | Prefeitura de Novydres | Bukovie | **APROVADO / CONGELADO** | frontal/simétrica; escadaria cívica; linguagem municipal, não tribunal/catedral |
| 06 | Suprema Corte de Novydres | New London | **APROVADO / CONGELADO** | frontal/simétrica; massa institucional pesada; escadaria cívica; juridicamente austera; sem símbolos religiosos/palacianos |
| 07 | Salão do Conselho de New London | New London | **APROVADO / CONGELADO** | frontal; reduzir ogivas/pináculos; cívico, não gótico religioso |
| 08 | Embaixada Mithraica / Consulado | New London | **APROVADO / CONGELADO; sujeito a QA** | frontal britânica compacta; muro baixo, portão, guaritas; sem brasão/coroa/bandeira |
| 09 | Canais de Vidro | New London | **APROVADO / CONGELADO** | linear; continuidade da água e passarelas; simplificar microdetalhe; não battlemap |
| 10 | Catedral de Santa Sophia | Vasyl Bay | **APROVADO / CONGELADO; sujeito a QA** | ortodoxa russa; oblíqua; branco/transparência preservados; sem recortes preenchidos em vermelho escuro |
| 11 | Universidade Imperial Teológica | Vasyl Bay | **APROVADO / CONGELADO; corrigido** | imperial russa sóbria; acadêmica; sem palácio francês; remover textos/brasões/coroas/cruzes excessivas |
| 12 | Seminário de Santo Vasyl Dreznov / Conselho de Vasyl Bay | Vasyl Bay | **APROVADO / CONGELADO** | complexo medieval convertido, claustro e capela integrada; não castelo militar |
| 13 | O Crisol | Vasyl Bay / extremo SE | **APROVADO / CONGELADO — freeze forte** | top-down territorial; prisão moderna em estrutura antiga; crucificações vazias permanentes; Alcatraz/Shutter como leitura, não cópia |
| 14 | Salão do Conselho de Chelsea | Chelsea | **APROVADO / CONGELADO** | sede cívica desgastada/ocupada; não monumentalizar ao nível de Bukovie |
| 15 | Estação Geotérmica Periférica | Chelsea | **APROVADO / CONGELADO** | oblíqua; massa técnica + tanques/tubos/chaminés; miniatura industrial legível; não blueprint |
| 16 | Capelas da Fome Branca | Chelsea | **APROVADO / CONGELADO; corrigido** | distribuído; 4–5/5 capelas modestas e variadas, anexos simples; reduzir pedra/vegetação; não fileira homogênea |
| 17 | Assembleia dos Estados Livres | Chelsea | **APROVADO / CONGELADO** | salão industrial/comunitário adaptado; identidade sindical/popular; menos monumental que governo central |
| 18 | Aeroporto Internacional de Novydres | Sulfok | **EM DESENVOLVIMENTO / PENDENTE DE APROVAÇÃO FINAL** | redesign 25/09: oblíquo/paralelo; terminal horizontal, torre, fingers, hangares, pista/taxiways; sem sci-fi/base militar/top-down técnico |
| 19 | Docas Quebra-Gelo de Sulfok | Sulfok | **EM DESENVOLVIMENTO / PENDENTE** | redesign 25/09: cais pesados, quebra-gelo, guindastes, armazéns, gelo fragmentado, industrial soviético-russo; sem marina/cruzeiro/base |
| 20 | Campus Técnico-Industrial da Universidade Imperial Teológica | Sulfok | **APROVADO / CONGELADO** | 3–4 edifícios; labs/oficinas/galpão; moderno funcional; não universidade clássica ou fábrica pesada |
| 21 | Pátio Ferroviário | Sulfok | **APROVADO / CONGELADO** | infraestrutura de carga moderna circa 2010; trilhos/desvios/plataformas/galpões; reduzir microtrilhos |
| 22 | Bairro das Casas Antigas | Drevnigrad | **APROVADO / CONGELADO; refeito/corrigido** | tecido urbano denso, russo/eslavo, ruas/becos atravessando; casas 1–3 pisos; sem perímetro murado; evitar aldeia/mediterrâneo |
| 23 | Matadouro Litúrgico de Drevnigrad | Drevnigrad | **EM DESENVOLVIMENTO / PENDENTE** | grande complexo de abate industrial antigo; galpões, ventilação, docas, currais; liturgia discreta; sem gore/templo/fábrica genérica |
| 24 | Jardim de Carne Harker | Drevnigrad | **PENDENTE** | arquitetura clínica/estufa/pavilhões/labs; corpo como subtexto, não gore/body horror explícito; arquitetura primeiro |
| 25 | Farol de Alexandria | Alexandria | **PENDENTE** | footprint superior/top-down com edifício de serviço/pátio/acesso costeiro; não desenhar farol lateral como ilustração isolada |
| 26 | Ruas dos Tribunais | Alexandria | **APROVADO / CONGELADO; sujeito a QA** | linear; rua como eixo; 5–8 edifícios judiciais variados; corredor jurídico, não campus uniforme |
| 27 | Observatório da Rede Ártica | Levi | **REJEITADO / DESCARTADO do fluxo visual** | continua presente no Atlas textual até decisão editorial contrária |
| 28 | Arquivo Levi | Levi | **REJEITADO / DESCARTADO do fluxo visual** | idem |
| 29 | Estação de Guarda do Ermo | Dunwich | **REJEITADO / DESCARTADO do fluxo visual** | idem |
| 30 | Círculo das Vilas Antigas | Dunwich | **REJEITADO / DESCARTADO do fluxo visual** | idem |
| 31 | Grande Mesquita de Al-Nur | Alexandria | **PENDENTE** | instituição islâmica urbana monumental/acolhedora; Banu Haqim é pilar histórico, não proprietário; visual final não recuperado/fechado |
| 32 | Grande Sinagoga Beit HaZikaron | Chelsea | **APROVADO / CONGELADO; sujeito a QA de padrão** | ashkenazi leste-europeia; oblíqua; simbologia discreta; reduzir Estrela de Davi/texto; não igreja/mesquita/palácio |

## 11.3 Fila visual conhecida

Última fila explícita antes de novas correções:

`18 → 19 → 23 → 24 → 25 → 31`

18 e 19 receberam novos prompts em 25/09, mas nenhum veredito final posterior foi recuperado neste handoff. Portanto continuam pendentes.

---

# 12. LINGUAGEM VISUAL CANÔNICA

## 12.1 Carimbos / assets de POI

**CANÔNICO / FECHADO**

- imagem unitária;
- fundo **100% transparente**;
- tinta única **oxblood**;
- gravura/carimbo/xilogravura;
- alto contraste;
- textura discreta de impressão;
- sem texto;
- sem moldura;
- sem cenário genérico;
- sem 3D;
- sem blur;
- sem glow;
- sem vinheta;
- sem gradiente.

Áreas claras/brancas são leitura positiva:

> **preservar branco ou convertê-lo em transparência; não substituir automaticamente por vermelho escuro.**

## 12.2 Gramática por categoria

- monumental cívico/religioso: frontal ou oblíqua;
- infraestrutura: oblíqua/paralela quando leitura arquitetônica importa;
- territorial: top-down quando a forma do lugar é o conteúdo;
- corredor: linear;
- conjunto distribuído: múltiplas unidades sem fundi-las num único edifício;
- tecido urbano: deve parecer recorte conectado à cidade, não diorama isolado.

## 12.3 Anti-pattern — “miniatura urbana”

**REJEITADO como formulação de prompt para tecido urbano**

Motivo: o termo levou o modelo a criar pequenos enclaves isolados, murados e “arrumadinhos”, reduzindo organicidade.

Substituição:

- “trecho de tecido urbano contínuo”;
- “ruas e becos atravessam a composição”;
- “frentes de rua conectadas ao exterior”;
- “sem perímetro delimitando o conjunto”.

## 12.4 Anti-patterns gerais

Evitar:

- cidade-ilha;
- halos tecnológicos;
- battlemap;
- blueprint técnico quando a categoria pede objeto arquitetônico;
- microarquitetura indiscriminada;
- simetria palaciana onde o lugar deve ser orgânico;
- Beaux-Arts/francês por default;
- medievalização genérica de Novydres;
- arquitetura mediterrânea em bairros antigos;
- excesso religioso em instituições civis;
- brasões/coroas/bandeiras/textos inventados;
- sci-fi em aeroporto/porto;
- marina/turismo/cruzeiro em Sulfok;
- base militar por default;
- body horror explícito no Jardim Harker;
- excesso de pedras/vegetação decorativa que transforma cidade em ruína;
- preenchimento de recortes claros com oxblood, destruindo contraste.

## 12.5 Estética arquitetônica

Direção geral:

- russo/eslavo;
- gótico europeu somente onde arquitetonicamente justificável;
- brutalismo funcional;
- imperial russo sóbrio;
- industrial soviético-russo;
- modernidade fria circa 2010.

Não transformar “influência russa” em cúpulas ortodoxas em todo prédio.

---

# 13. PIPELINE DE PRODUÇÃO VISUAL

## 13.1 Fluxo operacional decidido

**DECIDIDO EM 2026-09-27**

`Project/Work → decisão → geração/asset → GIMP → XCF → PNG → inspeção → aprovação → changelog`

### Camadas de verdade

- **Project**: fonte documental de verdade.
- **Master Map editável/XCF**: fonte visual de trabalho.
- **PNG**: export/render para inspeção/publicação, não master editável.
- **POI registry / decisions log**: preservam estado e impedem regressão.

## 13.2 Diretórios propostos

Estrutura sugerida, ainda não demonstrada como criada no filesystem:

- `10_MASTER_MAP/`
- `20_POIS/`
- `poi_registry.md`
- `decisions_log.md`

**PROVISÓRIO / A IMPLEMENTAR** até existir de fato.

## 13.3 Estados visuais

Fluxo recomendado/aceito:

`DRAFT → APPROVED → FROZEN`

Reabertura só por:

- erro objetivo;
- conflito com cânone posterior;
- QA transversal explicitamente autorizado;
- integração impossível no Master;
- decisão do usuário.

## 13.4 Regra de pós-processamento

GIMP pode:

- limpar fundo;
- normalizar transparência;
- equalizar contraste;
- ajustar escala;
- alinhar POI ao Master;
- corrigir bordas;
- compor layers;
- preservar qualidade.

GIMP **não deve**:

- redesenhar geografia por conveniência;
- inventar vias;
- mudar posição de raion;
- criar POI ausente;
- “embelezar” removendo Ermo;
- transformar linha ferroviária em outro sistema;
- alterar freeze sem registro.

## 13.5 MCP/CLI

MCP/CLI do GIMP foi discutido como possível automação. Não há neste contexto prova de pipeline automatizado final instalado/configurado.

**PENDENTE / FUTURO.**

Não escrever o handoff como se a automação já existisse.

---

# 14. REGRAS DE WORKFLOW E INTERAÇÃO

## 14.1 POIs: um por vez

**CANÔNICO PARA O FLUXO VISUAL ATUAL**

- usuário envia imagem;
- agente avalia;
- agente não gera/edita imagem sem pedido explícito;
- se houver correção, entregar o melhor prompt final de uma vez;
- não oferecer “versão simples” para depois melhorar;
- respostas curtas e decisivas.

Vereditos:

- `APROVADO`
- `APROVADO COM CORREÇÃO`
- `REJEITADO`

Fechamento:

`APROVADO. Congelado.`

## 14.2 Handoff antes de migração de ambiente

Decisão de 27/09:

1. consolidar handoff aqui;
2. salvar no Project;
3. operar em Work/Desktop;
4. preservar desenvolvimento em arquivos versionados;
5. usar GIMP para pós-processamento;
6. registrar toda decisão material.

Não transferir apenas “prompts recentes”. O handoff deve viajar junto dos truth-homes.

## 14.3 Política de prompt visual

Antes de escrever prompt:

1. identificar estado do POI;
2. ler diretriz canônica;
3. identificar erro específico da versão anterior;
4. preservar acertos;
5. corrigir somente o necessário quando a base é boa;
6. “redesenhar do zero” somente quando explicitamente decidido.

## 14.4 Respostas editoriais

Preferência operacional do usuário para Novydres:

- direto;
- curto quando o pedido é decisão pontual;
- uma recomendação principal + motivo;
- “entendi” para confirmação simples;
- não gerar imagem sem solicitação;
- não reexplicar o projeto inteiro durante microdecisões.

Este MASTER HANDOFF é exceção deliberada porque sua função exige exaustividade.

---

# 15. REJEITADOS, SUPERADOS E ANTI-REGRESSÃO

| Item | Estado | Contexto / motivo | Substituição |
|---|---|---|---|
| 3×3 / 9 tiles como produção atual | **SUPERADO** | pipeline inicial de junho | 5×5 / 25 tiles derivados do Master |
| 30 POIs como catálogo completo | **SUPERADO** no Atlas | Atlas migrou 30→32 | catálogo textual 32 |
| POIs 27–30 como carimbos atuais | **REJEITADO / DESCARTADO visualmente** | decisão 24/09 | não produzir asset; lore textual ainda exige sync |
| cidade como arquipélago | **REJEITADO** | água dominava separação | Ermo/terreno = separador principal |
| microedifícios comuns em todo mapa | **REJEITADO** | ruído e perda de hierarquia | malha limpa + POIs detalhados |
| halos tecnológicos | **REJEITADO** | estética incompatível | halos discretos/orgânicos quando necessários |
| universal top-down/blueprint para todo POI | **SUPERADO** | útil em fase cartográfica, ruim para arquitetura | gramática por categoria |
| ferrovia = dois trilhos paralelos como regra final | **SUPERADO** | revisões de legibilidade | linha escura única + dormentes |
| ferrovia = mero tracejado | **SUPERADO** | confundia com metrô | linha escura única + dormentes |
| bondes inventados | **REJEITADO como inferência** | camada não adotada | nenhuma camada própria |
| “miniatura urbana” em prompts de bairro | **REJEITADO** | gera enclave murado | tecido urbano contínuo |
| casas antigas como vila rural/mediterrânea | **REJEITADO** | POI22 | bairro eslavo denso |
| Palácio de Âmbar francês/Beaux-Arts | **REJEITADO** | estilo errado | imperial russo sóbrio |
| Universidade como palácio | **REJEITADO** | leitura errada | massa acadêmica institucional |
| Seminário como castelo militar | **REJEITADO** | leitura errada | complexo histórico convertido |
| Assembleia como parlamento palaciano | **REJEITADO** | incompatível com Estados Livres | salão industrial/comunitário |
| aeroporto sci-fi/base militar | **REJEITADO** | circa 2010 | infraestrutura moderna austera |
| docas turísticas/marina | **REJEITADO** | Sulfok industrial | porto quebra-gelo pesado |
| História Guiada = XP por idade/era | **REJEITADO** | quebra paridade | economia autorizada fixa |
| Flaws gerarem XP | **REJEITADO / FECHADO** | power inflation | Flaws sem XP |
| idade → BP/poder automático | **REJEITADO / FECHADO** | conflita com Power Envelope | trajetória + Generation hard bounds |
| NPC como terceiro modo de criação | **SUPERADO / RETCONNED** | arquitetura A corrigiu decomposição | exatamente Rápido e Guiado |
| inventário paralelo redundante de estado social | **REJEITADO** | duplicava ficha/history/RM | traits + History + Relationship Map |
| cobertura de Provocações por exaustão | **REJEITADO** | rerolls artificiais | Significant Coverage / closure funcional |
| fixar rigidamente páginas antigas de publicação | **SUPERADO** onde Format/Editorial Map retirou autoridade | layout antigo vazou como regra | obedecer contratos editoriais atuais |

---

# 16. QUESTÕES ABERTAS

## 16.1 Bloqueadoras para produção imediata do mapa final

1. **Sincronização 27–30:** descarte visual significa apenas “sem carimbo” ou futuro retcon do catálogo textual? Não decidir por inferência.
2. **POIs pendentes:** 18, 19, 23, 24, 25 e 31 ainda precisam de fechamento visual.
3. **Master editável atual:** estabelecer qual arquivo XCF/PNG é a versão operacional única antes do próximo pós-processamento.
4. **Transporte final renderizado:** confirmar que a versão física do Master usa a convenção ferroviária mais nova e que não conserva linhas superadas.
5. **Atlas × Master:** posições cardeais do Atlas precisam de patch editorial futuro ou serão mantidas como texto histórico? Decisão editorial necessária antes de republicar mapa/texto juntos.

## 16.2 Importantes, mas não bloqueadoras de um próximo POI

- explicação completa da alta densidade vampírica da Casa Mishkin;
- honrarias Mishkin/Ivanoff;
- três rituais pendentes de Zoya;
- status final de certas fichas antigas do Capítulo 07 após I/K;
- completar corpus L além de M1/M2;
- calibrar M formalmente;
- decidir eventual camada de bondes;
- catalogar arquivo visual individual de todos os POIs no novo Project.

## 16.3 Refinamentos

- revisar todos os congelados contra padrão pós-04 sem redesenhar os que passam;
- padronizar stroke/densidade/contraste/white-space dos carimbos;
- confirmar matriz espacial dos POIs selecionados no esquema 5×5;
- registrar overlaps reais;
- consolidar legenda final sem poluição.

## 16.4 Futuro

- edição/publicação final dos capítulos posteriores;
- Quick Coterie DEU;
- composição editorial das regras de criação para leitura standalone;
- eventual automação GIMP/MCP/CLI;
- export de tiles finais e QA de continuidade de bordas.

---

# 17. SE O PROJETO FOR RETOMADO AGORA, COMECE DAQUI

## 17.1 Primeiro: fixe as fontes

1. Coloque este `NOVYDRES_MASTER_HANDOFF_V1.md` no Project.
2. Identifique e fixe como referência:
   - `novydres_editorial_map_v0_9_4.json`;
   - `03_atlas_de_novydres_v0_2_2.md`;
   - Power Scale v0.1.1 + decisions;
   - Character Creation K + G/H/B/C authorities;
   - arquivo atual do Master Map;
   - registry atual de POIs.
3. Não faça nenhuma alteração visual antes de saber qual Master é o editável vigente.

## 17.2 Segundo: feche a fila visual pendente

Retomar na fila:

`18 → 19 → 23 → 24 → 25 → 31`

Para 18 e 19, começar dos redesigns de 25/09, não das versões anteriores.

## 17.3 Terceiro: QA transversal

Depois da fila, auditar especialmente:

`01, 02, 03, 08, 10, 11, 22, 26, 32`

Critérios:

- traço;
- densidade;
- contraste;
- leitura em miniatura;
- gravura;
- transparência;
- coerência representacional.

Reabrir apenas os que efetivamente falharem.

## 17.4 Quarto: integrar ao Master

- inserir todos os **POIs selecionados**;
- respeitar posições congeladas;
- não restaurar 27–30 automaticamente;
- preservar Ermo, relevo, vias, água, Crisol e transporte;
- verificar ferrovia/metro conforme convenção final;
- não criar geografia via tile.

## 17.5 Quinto: pós-processar no GIMP

- XCF versionado;
- layers nomeados;
- PNG de inspeção;
- comparação antes/depois;
- registrar alteração em changelog;
- congelar export aprovado.

## 17.6 Em paralelo, fora da frente visual

Quando houver janela editorial:

- continuar L a partir de M1/M2, sem voltar ao desenho de A–K;
- retomar NPCs com revalidação localizada, não rebuild automático;
- resolver Dignitas Mishkin/Ivanoff em artefato próprio;
- preparar sync cartográfico do Atlas somente após Master final.

---

# 18. ARTEFATOS E FONTES DE VERDADE

## 18.1 Governança e editorial

| Artefato | Papel | Acesso no contexto do handoff |
|---|---|---|
| `novydres_editorial_map_v0_9_4.json` | mapa editorial mais novo localizado | disponível na Library e consultado |
| `novydres_editorial_governance_v1_0.md` | autoridade editorial | **REFERENCIADO, MAS NÃO DISPONÍVEL NESTE CONTEXTO.** conteúdo integral não relido nesta auditoria |
| `novydres_prompt_reuse_contract_v0_1.md` | reuso de prompts | **REFERENCIADO, MAS NÃO DISPONÍVEL NESTE CONTEXTO.** |
| `novydres_editorial_prohibitions_contract_v0_1.md` | proibições editoriais | **REFERENCIADO, MAS NÃO DISPONÍVEL NESTE CONTEXTO.** |
| `novydres_standalone_rules_contract_v0_1.md` | standalone | referenciado por dependências; texto integral não relido |
| `novydres_play_guidance_contract_v0_1.md` | play guidance | referenciado |
| `novydres_revelation_architecture_contract_v0_1.md` | proteção/revelação | referenciado |
| `novydres_format_contract_v0_3_1.md` | formato editorial | referenciado |
| `novydres_retroactive_dependency_living_memory_policy_v0_1.md` | retroatividade | referenciado |

## 18.2 Capítulos

| Artefato | Estado |
|---|---|
| `01_introducao_v0_2_1.md` | autoridade referenciada; não relido integralmente nesta sessão |
| `02_historia_e_cronologia_v0_2_2.md` | autoridade referenciada |
| `03_atlas_de_novydres_v0_2_2.md` | **disponível e lido integralmente** |
| `04_faccoes_politica_conflitos_v0_2.md` | autoridade referenciada |
| `05_concilio_leis_status_prestacoes_v0_2_2.md` | dependência confirmada por Character Creation C; usar v0.2.2 como versão mais recente localizada por referência |
| `06_fe_heresia_e_ordem_v0_2_1.md` | disponível por busca / autoridade referenciada |
| `07_personagens/iskander_yasupov_v0_9.md` | referenciado |
| `07_personagens/madame_zoya_v0_9.md` | referenciado |

## 18.3 NPC Power Scale

- `novydres_npc_power_scale_citywide_v0_1_1.md` — disponível/consultado.
- `novydres_npc_power_scale_citywide_decisions_v0_1.md` — referenciado como ledger de 106 decisões.

## 18.4 Character Creation

Disponíveis/recuperados ao menos por Library/search:

- `novydres_character_creation_core_v5_baseline_v0_1.md`
- `novydres_character_creation_specialist_a_decisions_v0_1.md`
- `novydres_character_creation_power_envelope_v0_1_1.md`
- `novydres_character_creation_specialist_b_decisions_v0_1_1.md`
- `novydres_character_creation_social_territorial_political_integration_v0_1_1.md`
- `novydres_character_creation_specialist_c_decisions_v0_1_1.md`
- `novydres_character_creation_d1_played_history_core_v0_1.md`
- `novydres_character_creation_d1_played_history_core_decisions_v0_1.md`
- E/F/D2 artifacts
- `novydres_character_creation_j2_coterie_creation_architecture_v0_1.md`
- `novydres_character_creation_g_quick_creation_mode_v0_1_1.md`
- `novydres_character_creation_g_quick_creation_mode_decisions_v0_1_1.md`
- `novydres_character_creation_h_guided_pc_integration_v0_1.md`
- `novydres_character_creation_h_guided_pc_integration_decisions_v0_1_1.md`
- I NPC depth artifacts
- `novydres_character_creation_k_final_integration_v0_1.md`
- `novydres_character_creation_k_final_integration_decisions_v0_1.md`

### Nota de estado de K

O arquivo K recuperado possui frontmatter de **candidate_for_senior_editor_closure**, mas o estado de projeto posterior tratou A–K como arquitetura fechada e liberou trabalho downstream. Preservar as duas informações:

- **decisão operacional posterior:** arquitetura A–K fechada;
- **metadado do arquivo recuperado:** ainda diz candidate.

Isso é dívida documental, não motivo automático para reabrir A–K.

## 18.5 Workstream L

Prompt/arquitetura L foi localizado. O corpus completo mais recente de Provocações/Experiências não foi integralmente materializado nesta auditoria.

**REFERENCIADO, MAS NÃO DISPONÍVEL NESTE CONTEXTO.** para qualquer arquivo final L não listado nominalmente acima.

## 18.6 Fontes legadas

- `ai-studio-export-2026-06-12.md`
- `MATRIZ_EDITORIAL_RESUMIDA.md`
- `MATERIAL_FINAL_INTEGRADO_v0.9.md`
- `novydres 1-50.pdf`
- variantes históricas de Editorial Map
- prompts/tiles de junho

Usar para rastrear origem, nunca para substituir autoridade posterior.

## 18.7 Imagens / assets

Conhecidos/referenciados:

- Master Map atual e versões anteriores;
- `Mapa Gótico de Novydres.png` em histórico de Library;
- mapas costeiros/intermediários usados na frente visual;
- assets individuais de POI criados durante setembro.

O usuário informou que os POIs não descartados foram criados e estão na Library, porém os **nomes/IDs exatos de todos os arquivos visuais não foram enumerados neste handoff**.

**INTEGRIDADE NÃO CONFIRMADA — REQUER VERIFICAÇÃO** antes de montar o diretório definitivo.

---

# 19. CHANGELOG CONSOLIDADO DE DIREÇÃO

## Junho de 2026

- cartografia em blueprint estrutural;
- grade 3×3;
- 30 landmarks;
- título “Metropolitan Cartographic Atlas — 2010 — Northern Alaska, Bering Strait Urban Zone”;
- foco em validação espacial antes de acabamento;
- início da matriz editorial e consolidação de capítulos.

## Julho–início de agosto

- governança editorial, formatos, revelação, play guidance e standalone;
- capítulos 01–06 migrados para contratos atuais;
- Atlas fecha em **32 POIs**;
- Editorial Map chega a v0.9.x;
- Power Scale NPC fecha arquitetura.

## Agosto — Character Creation

- auditoria A–K;
- exatamente dois modos;
- Power Envelope separado de chassis;
- Quick fecha budgets/arrays;
- Guided fecha integração;
- I fecha profundidade NPC;
- K fecha ontologia comum e downstream;
- Workstream L autorizado.

## Agosto–setembro — Guided Content

- Provocação → Experiência → Episódio → Marco;
- M1/M2 testados;
- cobertura forçada rejeitada;
- erosão/continuidade passam a preservar paridade sem refund.

## 8–9 de setembro — Master Map

- Master 1536²;
- macrogeografia consolidada;
- Ermo como principal separador;
- linework/noir;
- microedifícios comuns removidos;
- 5×5 / 25 tiles;
- Crisol congelado;
- ferrovia/metro sofrem revisões gráficas.

## 22–25 de setembro — POIs

- regra permanente Master Map → Styles/tiles;
- linguagem de carimbo oxblood + transparência;
- POIs avaliados individualmente;
- 27–30 descartados visualmente;
- maioria congelada;
- padrão pós-04 força QA transversal;
- 18/19/23/24/25/31 permanecem fila aberta;
- 22 é refeito para tecido urbano denso;
- 18/19 recebem redesign do zero.

## 27 de setembro — migração operacional

- decisão de produzir handoff integral antes da mudança;
- Project = fonte documental;
- Work/Desktop = desenvolvimento e execução;
- GIMP = pós-processamento;
- XCF editável + PNG export + changelog.

---

# 20. CHECKLIST DE INTEGRIDADE

| Verificação | Resultado |
|---|---|
| Identidade, data, propósito e multiplicidade de frentes registrados | **OK** |
| Hierarquia de autoridade e regra contra sobrescrita silenciosa | **OK** |
| Mundo: localização, 2010, governo mortal/cainita, sucessão, raions, Ermo | **OK** |
| 9 raions preservados e Ermo não tratado como décimo | **OK** |
| conflito Atlas-posições × Master Map explicitado | **OK** |
| Power Envelope, paridade e gates preservados | **OK** |
| custos XP exatos preservados | **OK** |
| budgets 379/519/654 autorizado/1049 autorizado/1574 preservados sem arredondamento | **OK** |
| valores materializados 653/1044 + XP livre preservados | **OK** |
| arrays completos de cinco chassis preservados | **OK** |
| Flaws, Humanity, Predator Type, Generation/BP preservados | **OK** |
| Rápido e Guiado mantidos como únicos modos | **OK** |
| NPC depth não promovido a terceiro modo | **OK** |
| D1/L, M1/M2, 20 posições e 2d10 preservados | **OK** |
| relação Master Map → tiles explicitamente preservada | **OK** |
| 5×5 preservado e 3×3 marcado superado | **OK** |
| terreno, vias, ferrovia, metrô, estações, porto/aeroporto registrados | **OK** |
| evolução contraditória da ferrovia registrada em vez de harmonizada silenciosamente | **OK** |
| todos os 32 números/nome de POI registrados | **OK** |
| 27–30 preservados como conflito conteúdo × visual | **OK** |
| status visual de todos os POIs registrado | **OK**, com ressalva de que vereditos posteriores não recuperados mantêm 18/19/23/24/25/31 pendentes |
| padrão oxblood/transparência/contraste registrado | **OK** |
| anti-pattern “miniatura urbana” registrado com motivo | **OK** |
| pipeline Work/GIMP/XCF/PNG/changelog registrado | **OK** |
| rejeições e supersessions principais contextualizadas | **OK** |
| artefatos principais listados | **OK** |
| filenames/IDs de cada asset visual individual enumerados | **INTEGRIDADE NÃO CONFIRMADA — REQUER VERIFICAÇÃO.** |
| corpus L completo, linha a linha, inventariado | **INTEGRIDADE NÃO CONFIRMADA — REQUER VERIFICAÇÃO.** |
| todos os ledgers A–K reproduzidos decisão por decisão | **INTEGRIDADE NÃO CONFIRMADA — REQUER VERIFICAÇÃO.** Este handoff preserva arquitetura e decisões materiais, não duplica centenas de linhas de ledgers fonte |
| versão física exata do Master Map a ser aberta no GIMP identificada por hash/caminho | **INTEGRIDADE NÃO CONFIRMADA — REQUER VERIFICAÇÃO.** |
| destino final dos POIs 27–30 no texto publicado decidido | **INTEGRIDADE NÃO CONFIRMADA — REQUER VERIFICAÇÃO.** |
| eventual transferência Canadá→EUA datada e canonizada | **INTEGRIDADE NÃO CONFIRMADA — REQUER VERIFICAÇÃO.** |

---

# A. ESTADO ATUAL EM 1 PÁGINA

**Novydres by Night** está estruturalmente maduro, mas não “pronto”. O cânone editorial básico 01–06, a escala de poder NPC e a arquitetura de criação A–K estão fechados. O conteúdo Guiado L ainda está em desenvolvimento. O Capítulo 07/NPCs pode ser retomado mediante revalidação contra I/K. A cartografia macro foi consolidada em um Master Map linework-first, com 9 raions e Ermo como separador principal, mas a camada visual de POIs e alguns detalhes de transporte ainda exigem finalização e pós-processamento.

A cidade está em 2010, no norte do Alasca/Estreito de Bering. O Concílio da Cruz e Espada é legítimo e opressivo. Gilgamesh está ausente; Vasya saiu com o Beckoning; Mikhail morreu; Dominique e Vladmir disputam sucessão. Os nove raions possuem identidades clânicas/políticas fortes. Chelsea e Sulfok ficam fora/à margem da jurisdição plena do Concílio. Nosferatu dominam transversalmente a infraestrutura subterrânea.

A Criação de Personagem possui somente Rápido e Guiado. Child of the Night vale 379 XP; adicionais são +140, +275, +670 e +1,195. Generation é independente do chassis; BP deve ser pago. Flaws nunca concedem XP. Quick/Guided devem convergir em poder e legalidade. Guided não premia idade.

O Master Map é a fonte espacial. Tiles 5×5 derivam dele. O antigo 3×3 está superado. A macrogeografia está congelada; não fazer passe global novo. O Crisol possui freeze forte. A ferrovia passou por revisões: a regra atual registrada é linha única escura com dormentes, distinta do metrô tracejado curto.

O Atlas textual lista 32 POIs, mas o fluxo visual descartou 27–30. Isso é conflito de camada, não licença para apagar lore. Os assets congelados concentram-se em 01–17, 20–22, 26 e 32, com QA autorizado em alguns. A fila visual aberta é 18, 19, 23, 24, 25 e 31. 18/19 já receberam redesigns novos, mas ainda precisam de veredito final recuperado/aplicado.

Padrão visual: oxblood, alto contraste, fundo 100% transparente, gravura/carimbo, sem texto, sem 3D/glow/gradiente. Branco/transparência deve ser preservado. Para bairros, nunca usar formulação que force “miniatura urbana” isolada/murada; construir tecido contínuo.

A retomada correta é: fixar fontes no Project → identificar Master editável → concluir POIs pendentes → QA transversal dos congelados → integrar tudo no Master → GIMP/XCF → PNG de inspeção → aprovação → changelog.

---

# B. PRÓXIMAS AÇÕES CONHECIDAS

1. Salvar este handoff no Project como raiz de continuidade.
2. Materializar/localizar o Master Map editável corrente e registrar caminho/hash/versão.
3. Criar `poi_registry.md` e `decisions_log.md` a partir deste handoff, se ainda não existirem.
4. Retomar POI 18 e 19 pelos prompts/redesigns de 25/09 e obter veredito.
5. Fechar 23, 24, 25 e 31.
6. Rodar QA pós-04 nos congelados relevantes.
7. Resolver explicitamente a política de publicação dos POIs 27–30.
8. Integrar somente POIs selecionados no Master.
9. Confirmar ferrovia/metro/estações na versão física final.
10. Pós-processar em GIMP de modo não destrutivo.
11. Exportar PNG, revisar continuidade entre tiles e congelar.
12. Em paralelo editorial: continuar Workstream L; revalidar NPCs; fechar Dignitas Mishkin/Ivanoff; preparar futuro patch Atlas × Master.

---

# C. POSSÍVEIS LACUNAS DO HANDOFF

Este handoff foi construído a partir de decisões de conversa, memória do projeto e artefatos da Library recuperados durante a auditoria. Ele é propositalmente conservador onde a evidência não foi integralmente relida.

Lacunas que **não devem ser preenchidas por inferência**:

- nomes/IDs/caminhos exatos de todos os PNGs dos POIs na Library;
- hash/caminho da versão do Master a abrir no GIMP;
- corpus L completo após os stress tests já registrados;
- detalhe integral de cada uma das 106 decisões NPC-POWER;
- cada uma das decisões A–K em forma de ledger completa;
- tabela completa de hard bounds Generation↔BP do baseline oficial;
- explicação final do vínculo territorial Canadá→EUA;
- decisão editorial final sobre 27–30;
- qualquer veredito de 18/19/23/24/25/31 posterior ao último registro explicitamente recuperado;
- detalhes ocultos/protegidos cuja própria arquitetura exige não exposição;
- estado de automação real de GIMP por MCP/CLI.

Para qualquer um desses pontos, a ação correta é **recuperar a fonte**, não reconstruir por memória.
---

## REGRA FINAL DE CONTINUIDADE

> **Nenhum agente que receba este handoff está autorizado a “melhorar” Novydres apagando rastros de decisão.**
>
> Quando houver dúvida: localizar a autoridade, preservar a versão anterior, registrar o conflito, fazer a menor alteração necessária e atualizar o changelog.