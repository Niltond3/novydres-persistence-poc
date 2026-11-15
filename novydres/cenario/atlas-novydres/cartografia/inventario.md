---
document_id: INVENTARIO-ATLAS-P0
title: Inventário de fontes, geografia e lacunas do Atlas de Novydres
status: LEVANTAMENTO_PRELIMINAR_PARA_REVISAO
date: 2026-11-14
subject_id: world-atlas-novydres
owner_scope: novydres/cenario
visibility: PLAYER_SAFE
source_snapshot: 7ce8e88c122a5d80879e30a23b1f3be159cac727
reference_year: 2010
scope: P0_STRUCTURAL_WORLD_ATLAS_INITIAL_PASS
geometry_approved: false
---

# P0 — Inventário geográfico, urbano, territorial e político de Novydres

> **Atualização de 15/11/2026:** GEO-001.1, GEO-002.1 e GEO-002.2 fechados com fontes únicas respectivas em `../populacao-2010.json` e `../localizacao-geral-2010.json`. Diagnósticos anteriores abaixo são memória de investigação, não autoridade editorial. O Atlas possui uma única proposta corrente.

> **Fechamento posterior GEO-001.1 (15/11/2026):** população municipal residente de **7.000.000 em 2010** aprovada pelo proprietário e registrada no assunto dono em `../populacao-2010.json`. O texto abaixo documenta a situação histórica anterior à decisão; suas referências a divergência populacional são **evidências superadas**, não alternativas vigentes. Permanecem abertas a geometria específica de GEO-002, GEO-003, GEO-004 e GEO-010.

## Complemento P0 — dossiê cruzado de decisões

O inventário inicial foi ampliado por um dossiê com **22 respostas documentais, 22 recomendações e critérios específicos de fechamento**, pelo registro estruturado e por um contrato de propagação. **Ainda não há nova decisão canônica fechada.** O cruzamento inclui as fontes territoriais, políticas, históricas e referências episódicas localizadas; a varredura exaustiva de episódios e efeitos territoriais permanece dependência obrigatória por item, conforme o dossiê.

Arquivos associados:
- `cartografia/dossie-geografico.md`
- `cartografia/registro-decisoes.json`
- `cartografia/contrato-propagacao.md`

`P0_CROSS_REFERENCE_IN_PROGRESS`; `1/22_CLOSED_CANON`. Dados históricos divergentes permanecem preservados como fontes de auditoria, não como autoridades ativas concorrentes.

## 1. Objetivo, limites e método

Inventariar **o que já foi documentado, o que pode ser aproveitado, o que diverge e o que exige decisão**, antes de criar a geografia oficial de 2010. Este registro não canoniza fatos, pessoas, domínio, medidas, facções, rotas nem coordenadas. É a **primeira passagem estrutural** de P0: cobertura de fontes do mundo, nove distritos, 32 POIs e referências políticas principais. Ainda será necessário auditar dependências da crônica e demais fontes dispersas para encerrar P0 exaustivamente.

Classificação utilizada:
- **D — Documentado:** consta de fonte com localização/proveniência conhecida. Não implica aprovação de conteúdo.
- **V — Variante/conflito:** há formulações concorrentes ou insuficiência de autoridade.
- **L — Lacuna:** não existe especificação suficiente nas fontes nucleares inspecionadas para desenhar ou medir; **não é prova de inexistência no mundo**.
- **F — Fechado:** existe decisão explícita e suficiente para uso canônico/arquitetural dentro de seu escopo. **Nenhum dado geográfico novo recebeu F nesta inspeção**.
- **A — A conferir:** fonte externa ao núcleo consultado, assunto de personagem/crônica ou informação situada ainda precisa de reconciliação.

Estados editoriais/epistêmicos de fontes (`CANDIDATE`, `UNKNOWN` etc.) são mantidos **separados** das classes do inventário acima.

**Snapshot único pesquisado:** master `7ce8e88c122a5d80879e30a23b1f3be159cac727`. A branch de documentação é de proposta. Não usar imagens criadas anteriormente pelo gerador como prova territorial, funcional ou política.

## 2. Fontes e cobertura realizada

1. `novydres/AGENTS.md`, `CONTEXT.md` e `catalogo.json` do mesmo SHA (153 assuntos indexados). Consulta estruturada do catálogo para localizar propriedades e dependências.
2. `novydres/cenario/atlas-novydres/{assunto.json,index.md,registro.json,segmentos.json,atlas-proposta.md,atlas-proposta.md}`. Fontes de atlas 0.2 e 0.2.2; 9 raions, 32 POIs, 2 variantes custodiadas; status de fonte candidato.
3. **9 de 9** `novydres/cenario/geografia/district-*/conteudo.json`. Em todos, `CANDIDATE_NOT_OPERATIONAL`, `UNKNOWN`, `NOT_SELECTED` e **uma única projeção da proposta editorial corrente**. A avaliação das antigas versões ocorreu antes da consolidação, cujo histórico está disponível somente no Git.
4. **32 de 32** `novydres/cenario/lugares/poi-*/conteudo.json`. Todos `CANDIDATE_NOT_OPERATIONAL`, `UNKNOWN`, `NOT_SELECTED`, com **uma única projeção da proposta corrente** por POI. São 32 **registros selecionados de interesse**, não o total de instalações da cidade.
5. `novydres/cenario/politica-global/atlas-proposta.md` (facções, vetores e conflitos), `atlas-proposta.md` (Concílio e leis), `fonte-003.source.md` (fé e instituições); todos documentos de origem candidatos.
6. `novydres/cenario/historia-global/atlas-proposta.md` e `atlas-proposta.md` (introdução e cronologia), também candidatos.
7. `novydres/cenario/organizacoes/concilio-cruz-espada/conteudo.json`, `legiao-coroa-ferro/conteudo.json`; conceitos documentados, sem promoção epistêmica/editorial.
8. `novydres/cenario/organizacoes/escala-de-poder/fonte-001..004.source.md`; há registro de decisões de NPC de escala global, mas documentação ainda indica necessidade de revalidação editorial. O mapa não pode presumir automaticamente lotações, presença ou hierarquias regionais.
9. Existência de assuntos de NPC global (`npc-iskander-yasupov`, `npc-madame-zoya`, `npc-samir-haddad`) confirmada. **Não foi realizado censo completo dos personagens da crônica por localização**: depende de fontes restritas, temporalidade e distinção entre NPC global versus ocorrência em cena.

**Fora da cobertura exaustiva nesta passagem:** todos os detalhes de cenas CHR-001, cada decisão histórica fora desses arquivos, instalações incidentais mencionadas em episódios, NPCs episódicos, materiais multimídia, fontes externas e projetos de imagens. Esses itens ficam como `A` e serão vasculhados em passes posteriores antes de declarar P0 fechado.

## 3. Divisões territoriais e domínio — fonte candidata, não cânone ratificado

Os nomes, macroposições e esferas abaixo são documentados na fonte de Atlas 0.2.2; fronteiras precisas inexistem no material inspecionado.

| Raion | Macroposição documentada | Vocação urbana | Domínio/jurisdição da fonte | Estado |
|---|---|---|---|---|
| Dunwich | Noroeste | Ermo, vilas, fronteira, acesso | Gangrel sob Concílio | D |
| Levi | Norte | Arquivos, observatórios, saúde discreta | Malkavian sob Concílio | D |
| Alexandria | Nordeste | Alfândega, costa, justiça, seguros | Lasombra sob Concílio | D |
| Chelsea | Oeste | Centro antigo, cortiços, rios, religião, desigualdade | Estados Livres, fora da jurisdição formal do Concílio | D |
| Bukovie | Centro | Governo, finanças, calor privilegiado | Ventrue sob Concílio | D |
| New London | Leste | Diplomacia, Suprema Corte, canais | Banu Haqim sob Concílio | D |
| Sulfok | Sudoeste | Porto, aeroporto, indústria e ferrovia | Em disputa: Estados Livres vs. pressão Gangrel; não integra plenamente Concílio | D/V |
| Drevnigrad | Sul | Cidade antiga, indústria envelhecida, linhagens | Tzimisce sob Concílio | D |
| Vasyl Bay | Sudeste | Fé, ensino teológico, costa e prisão | Toreador sob Concílio | D |

**Observações:**
- A fórmula de fonte "sete raions formais + dois fora da jurisdição formal plena" corresponde à tabela, mas deve ser validada por autoridade editorial antes de virar informação cartográfica fechada.
- **Nosferatu:** domínio transversal proposto no subterrâneo (metrô, galerias, esgoto e termas), **sem raion de superfície**.
- Domínio, jurisdição formal, controle de fato, influência local, presença de agentes, apoio de instituição mortal, acesso e hostilidade **são dimensões diferentes**. Evitar simplificação "um clã = exclusividade de raion".
- Falta geometria de limites e subbairros, zonas de influência secundária, bordas de guerra, áreas neutras, enclaves, Elysia e censos de Cainitas por região.
- Raions **não são** tiles A1–C3; 3×3 ou 5×5 são divisões técnicas de exportação.

## 4. Política, seitas, conflitos, atores e influência — situação documental

**Documentado nas fontes públicas candidatas:**
- Concílio da Cruz e Espada e sua crise de sucessão; concorrência política entre Dominique e Vladmir Mishkin; possibilidade política do Terceiro Caminho.
- Estados Livres em Chelsea e disputa de Sulfok; interesses próprios de Hecata, Nosferatu e agentes logísticos em Sulfok.
- Gangrel como força de fronteira/Ermo, Tzimisce e Draco Pact, Lasombra e Jurisdição das Sombras; Banu Haqim em funções jurídicas.
- Ordem Urukiana, Legião da Coroa de Ferro, Legião de Aníbal e rede Nosferatu como instituições/competências transversais que **não cabem** em polígono único de clã.
- Três pilares religiosos e influências Cainitas predominantes — Toreador/Ortodoxia, Banu Haqim/Islã, Malkavian/Judaísmo — **não equivalem a propriedade da fé ou domínio sobre seus fiéis**.
- Exemplos de atores de circulação pública no capítulo político: Dominique e Vladmir Mishkin; Zara "Chispa", Sergei Orlov e Khalil Al-Rashid; Kuthulun; Wilhelmina Harker; Dom Sebastião; Grigori, Mikhail e Mariya Vasiliev. Referências a atores **não** provam residência, controle de quarteirão, endereço, presença em 2010 ou autoridade editorial final.

**Frentes de conflito publicamente descritas, a espacializar se aprovadas:** sucessão Mishkin, captura da Lei, fé/ordens, proteção do Ermo, calor/desigualdade Bukovie–Chelsea, insurgência, Sulfok/logística, reconhecimento Lasombra, soberania do Crisol e cidade subterrânea.

**Não definido no modelo cartográfico:** matriz clã×raion com níveis de presença/influência, recursos efetivamente controlados, rivais e aliados por faixa territorial, personagens importantes com domicílio/refúgio e alcance de mobilização, fronteiras de tensão, zonas neutras e territórios sobrepostos. Não deduzir automaticamente a partir de estereótipos de clã. Política mortal e política Cainita exigem camadas separadas, com controle de divulgação.

## 5. Inventário dos 32 locais de interesse da fonte candidata

Atenção: são 32 **POIs editoriais nomeados**, não levantamento completo de prédios, hospitais, escolas ou demais serviços.

| Raion | POIs documentados |
|---|---|
| Bukovie | 01 Torre de Inverno; 02 Palácio de Âmbar; 03 Exchange Hall; 04 Feudo de Dominique Mishkin; 05 Prefeitura de Novydres |
| New London | 06 Suprema Corte; 07 Salão do Conselho; 08 Embaixada Mithraica/Consulado; 09 Canais de Vidro |
| Vasyl Bay | 10 Catedral de Santa Sophia; 11 Universidade Imperial Teológica; 12 Seminário Santo Vasyl Dreznov/Salão do Conselho; 13 O Crisol |
| Chelsea | 14 Salão do Conselho; 15 Estação Geotérmica Periférica; 16 Capelas da Fome Branca/Cathedral Streets; 17 Assembleia dos Estados Livres; 32 Grande Sinagoga Beit HaZikaron |
| Sulfok | 18 Aeroporto Internacional; 19 Docas Quebra-Gelo; 20 Campus Técnico-Industrial da Universidade; 21 Pátio Ferroviário |
| Drevnigrad | 22 Bairro das Casas Antigas; 23 Matadouro Litúrgico; 24 Jardim de Carne Harker |
| Alexandria | 25 Farol; 26 Ruas dos Tribunais; 31 Grande Mesquita de Al-Nur |
| Levi | 27 Observatório da Rede Ártica; 28 Arquivo Levi |
| Dunwich | 29 Estação de Guarda do Ermo; 30 Círculo das Vilas Antigas |

Em cada caso são conhecidos **nome e raion candidato**; faltam coordenadas, lote, forma, dimensão, conexão viária, capacidade, função pública exata, operador, estado em 2010, e fronteira entre conhecimento público e revelação narrativa. Para alguns, a "implantação" é uma zona, corredor ou complexo, não um prédio isolado.

## 6. Geografia física e evolução — dados documentados versus lacunas

| Assunto | O que existe nas fontes candidatas (D) | O que falta para fechar (L/V) |
|---|---|---|
| Macroterritório | Ártico, relação com Alasca/Estreito de Bering, rio quente e costa | Posição/ancoragem exata, extensão, área terrestre/marítima e CRS |
| Água | Rio Vasyl/Reka Vasilya: Chelsea, canais que emergem em New London, deságue em Sulfok | Nascentes, bacia, geometria, tributários, pontes, ilhas, baías, congelamento sazonal |
| Ermo | Corredores entre raions, áreas de risco e limites da urbanização | Polígonos, travessias, classificação ambiental, riscos, infraestrutura, status jurisdicional |
| Topografia | Colinas, costa ártica, antigas zonas urbanas | Modelo de relevo, desnível, substrato, áreas de inundação e proteção |
| História | Fundação associada a 1423; etapas 1917, 1950–1989, 1990–1998, crise em 2010 | Transformação física por época, bairros por idade, cronologia das obras, reconciliação histórica |
| Clima | Frio extremo, desigualdade de calor, canais/áreas aquecidas | Sazonalidade, regime de gelo, dados de projeto e operação urbana |
| População | **Cânone fechado em 2010:** 7.000.000 residentes, fonte única `../populacao-2010.json` | Distribuição por raion e perfil demográfico ainda em aberto |

**Risco de falsa base visual:** esboços gerados anteriormente usaram Arkham/Miskatonic, 3×3 e outros nomes/posições que não equivalem automaticamente ao atlas atual do GitHub. **Não importar topônimos, rios ou avenidas dessas imagens como cânone** sem decisão explícita.

## 7. Inventário funcional da cidade — cobertura e lacunas

Classificação para **fontes nucleares lidas**, não declaração sobre a inexistência de conteúdos incidentais em toda a história.

| Domínio | Evidência atual | Lacuna central |
|---|---|---|
| Administração territorial | Governo municipal em Bukovie; subprefeituras e conselhos por raion | Sedes e sedes regionais, competências, cartórios e postos de atendimento |
| Segurança | Guarda do Ermo, segurança privada/política e controles de passagem | Delegacias, distritos policiais, bombeiros, bases de resgate, proteção civil, prisões ordinárias |
| Justiça e registro | Suprema Corte em New London; corredores judiciais em Alexandria, cartórios mencionados | Fóruns locais, cartórios por área, defensorias, arquivo registral, competência judicial |
| Saúde | Hospitais referidos no conceito de Levi; clínicas e influências em Drevnigrad | **Quantidade total de hospitais e clínicas, tipos, leitos, trauma, maternidade, emergências, ambulâncias, morgues** |
| Morte e memória | Sinagoga/memorial, igrejas, espaços históricos | **Quantidade e localização de cemitérios**, crematórios, funerárias, sepultamento em solo congelado |
| Educação | Universidade Teológica em Vasyl Bay, campus técnico em Sulfok | Escolas, institutos, hospitais universitários, outras universidades, bibliotecas e laboratórios |
| Mobilidade urbana | Metrô e pátio ferroviário mencionados, aeroporto, porto | **Rede completa de metrô, bonde, trem, ônibus, ferry, linhas, frequência, terminais e integração tarifária** |
| Transporte viário | Travessias do Ermo, posto rodoviário, zonas de serviço | **Grafo de ruas, avenidas, rodovias, túneis, pontes, acessos, anéis e hierarquia** |
| Logística | Aeroporto e docas de Sulfok, ferrovias industriais | Capacidade de carga/passageiros, corredores de distribuição, pátios, portos menores |
| Aquecimento | Rede geotérmica, desigualdade Chelsea–Bukovie, estação periférica e túneis | **Plantas e subestações, zonas térmicas, dutos, redundância, falhas, concessionárias, carga e reserva** |
| Água, resíduos e energia | Dependência metropolitana de infraestrutura e sistemas subterrâneos | Captação, tratamento, adutoras, saneamento, drenagem, resíduos, energia e telecomunicações |
| Habitação e uso do solo | Arquétipos distritais e zonas históricas | Densidades, bairros, moradias, empregos, comércio, proteção histórica, expansão e segregação |
| Religião e cultura | Catedral, mesquita, sinagoga, seminário, tradição plural | Paróquias, pequenos templos, centros culturais, museus, parques, instalações comunitárias |
| Economia e serviços | Finanças em Bukovie; comércio, indústria e logística | Mercados, centros comerciais, bancos, sedes, distribuidores, empregos e polos regionais |
| Sistemas de emergência | Travessias hostis e instalações isoladas | Planos de evacuação, estoques, abrigos térmicos, comunicação de crise e acesso hospitalar |

**Interpretação essencial:** um aeroporto nomeado entre os 32 POIs **não prova** que a cidade possui somente um aeroporto; um hospital mencionado **não determina** a quantidade de hospitais; nenhuma ilustração gerada comprova número de delegacias ou linhas.

## 8. Matriz de decisões geográficas a fechar

IDs estáveis propostos **para questões de planejamento**, não novas entidades canônicas. As decisões serão tomadas com o proprietário, agrupadas por dependência.

| Ordem | ID | Decisão / produto | Dependência principal |
|---|---|---|---|
| Fundação | GEO-001 | **Fechado GEO-001.1:** 7.000.000 residentes em 2010; não reabrir conflito antigo como valor vigente | Fonte canônica `../populacao-2010.json`; GEO-010 distribuição aberta |
| Fundação | GEO-002 | Localização do território, projeção e sistema de medidas | GEO-001 apenas se área for população-dependente |
| Fundação | GEO-003 | Costa, ilhas, Rio Vasyl, relevo e corredores do Ermo | GEO-002 |
| Fundação | GEO-004 | Limites geográficos dos 9 raions e áreas fora de raions | GEO-003 |
| Fundação | GEO-005 | Cronologia espacial de assentamento, expansão e obras urbanas | GEO-003/004, história |
| Política | GEO-006 | Confirmação de jurisdição política e domínio primário por raion em 2010 | GEO-004, política |
| Política | GEO-007 | Matriz clã/seita × raion/bairro com influência, acesso, aliança, hostilidade e controle institucional | GEO-006 |
| Política | GEO-008 | Registro de NPCs e forças relevantes, presença, residência, sedes, refúgios e projeção de poder por área | GEO-007, fichas e sigilo |
| Política | GEO-009 | Frentes de conflito, zonas neutras, enclaves, fronteiras disputadas e jurisdição subterrânea | GEO-007/008 |
| Urbano | GEO-010 | Densidade e população por raion/bairro | GEO-001/004 |
| Urbano | GEO-011 | Zoneamento: emprego, indústria, moradia, serviços, áreas protegidas | GEO-005/010 |
| Urbano | GEO-012 | Rede viária principal, pontes e túneis | GEO-003/011 |
| Transporte | GEO-013 | Metrô, ferrovia de passageiros e carga, bonde, ônibus, ferry, estações e corredores | GEO-010/012 |
| Infraestrutura | GEO-014 | Aquecimento geotérmico e zonas de distribuição térmica | GEO-003/010/011 |
| Infraestrutura | GEO-015 | Água, esgoto, drenagem, resíduos, energia, telecomunicações | GEO-010/014 |
| Serviços | GEO-016 | Governo, subprefeituras, justiça, cartórios e registros | GEO-004/010/012 |
| Serviços | GEO-017 | Hospitais, clínicas, emergências, maternidades, atenção básica e ambulâncias | GEO-010/012/013 |
| Serviços | GEO-018 | Cemitérios, crematórios, funerárias, necrotérios e serviços mortuários | GEO-003/010/012 |
| Serviços | GEO-019 | Polícia, bombeiros, emergências, resgate, defesa civil e prisões | GEO-010/012/013 |
| Serviços | GEO-020 | Educação, instituições de fé, cultura, parques, comércio e equipamentos de bairro | GEO-010/011/013 |
| Pontos | GEO-021 | Verificação de existência, função, capacidade e implantação física dos 32 POIs herdados | GEO-004/011/012 |
| Publicação | GEO-022 | Tipos de mapa, legendas, sigilo, estilos, escala e divisão dinâmica de tiles | GEO-003..021, ADR-002 |

**Porta de prontidão:** primeiro fechar GEO-001..005 e reconciliação da política principal; depois as redes e cadastros. Nem toda rua secundária e clínica precisará de uma deliberação manual, desde que sejam geradas por regras urbanas aprovadas e não usurpem o cânone.

## 9. Próximo passe necessário para P0 completo

Ainda é preciso executar, por fontes identificadas e uma revisão temporal até 2010:

1. Contrastar o atlas com capítulos de política/fé e com cada ficha/marco de NPC relevante para residência, alcance e relações, sem converter informação secreta em mapa público.
2. Varrer os episódios e registros de CHR-001 por **lugares e infraestrutura incidentais já estabelecidos**, preservando acontecimentos e restringindo sua divulgação.
3. Verificar possíveis decisões do usuário posteriores às fontes de agosto de 2026, sobretudo população, rios, nomes, autoridade dos raions e redes.
4. Conferir decisões de escala NPC e a diferença entre força pessoal, capacidade institucional, influência local e soberania territorial.
5. Publicar um registro resolvido com: item, fonte/linha, autoridade, temporalidade, impacto, decisão necessária, proposta de solução e dependência — sem exigir microaprovações.

**Conclusão desta versão:** existem 9 conceitos de raion e 32 POIs bem estruturados, além de significativa política urbana/Cainita; não há ainda evidência suficiente de **geometria, rede de serviços, linhas de transporte e distribuição municipal** para fechar o mapa. A fase P0 permanece aberta; este arquivo é inventário de descoberta, não declaração de cobertura exaustiva de todo o projeto.
