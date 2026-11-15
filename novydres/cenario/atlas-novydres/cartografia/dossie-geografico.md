---
document_id: DOSSIER-GEO-001-022
subject_id: world-atlas-novydres
status: PROPOSTAS_NAO_CANONIZADAS
visibility: PLAYER_SAFE
source_snapshot: 7ce8e88c122a5d80879e30a23b1f3be159cac727
created_on: 2026-11-14
census_year: 2010
canonical_decisions_closed: 1
---

# Dossiê decisório GEO-001 a GEO-022 — Novydres

> **Nenhuma recomendação deste dossiê é um fato canônico.** Os 22 tópicos são pacotes de decisão para aprovação expressa. Os estados técnicos dos arquivos de origem (`UNKNOWN`, `CANDIDATE`, `NOT_SELECTED`) não são convertidos em aprovação por este documento.

## Método de cruzamento

Usamos um mesmo snapshot operacional de `master` (`7ce8e88c122a5d80879e30a23b1f3be159cac727`) e as entradas `AGENTS.md`, `CONTEXT.md`, `catalogo.json`. Conferimos as duas variantes do Atlas, nove raions e 32 POIs, fontes dos capítulos de política, Concílio, fé e história; registros das organizações principais, arquitetura de poder de NPCs, episódios/indexes selecionados da CHR-001 e exemplos de fatos de cena. O catálogo expõe **41 dependentes diretos** do Atlas (9 raions + 32 POIs); relações literárias ou de crônica não se esgotam nesse índice.

### Resultados transversais

- O Atlas 0.2.2 é fonte candidata; não é uma lei geográfica automaticamente vigente. Sete raions têm textos idênticos nas duas variantes de conceito; Sulfok e Vasyl Bay têm redações de referência/editorial diferentes, **sem prova de divergência topológica material** apenas por isso. As 32 duplas POI foram conferidas, com texto igual e autoridade `NOT_SELECTED`.
- As fontes documentam **mais de 8 milhões**, enquanto o novo pedido de construção usa **7 milhões**; é conflito de definição, não ajuste numérico tácito.
- Domínio, influência, aliança, controle institucional, direito de passagem e presença são variáveis independentes. O mapa oficial mortal não deve revelar relações Cainitas reservadas.
- Uma afirmação de personagem em cena (ex.: endereço dito por Rada) não transforma esse endereço em instalação municipal validada ou em identidade de outra obra; revisar conhecimento situado antes de espacializar.
- É impossível garantir 'zero fontes históricas divergentes' sem destruir proveniência. O contrato de fechamento exigirá **zero autoridades operacionais concorrentes** para o mesmo fato/recorte temporal; fontes antigas ficam identificadas e não são consultadas como segunda verdade.
- A revisão transdisciplinar ainda **não demonstra inspeção de cada linha de todos os episódios/arquivos da crônica**. A camada episódica é dependência obrigatória a validar antes de fechamento de conceitos afetados; não se declara P0 `PASS` nesta versão.

## Dossiês por tópico

### GEO-001 — População-base em 2010

**GEO-001.1 FECHADO (15/11/2026):** 7.000.000 residentes no município em 2010, incluindo os nove raions; fonte vigente `../populacao-2010.json`. As duas menções arquivadas a mais de oito milhões permanecem preservadas e **não têm autoridade concorrente para este valor**. Não está fechada a distribuição por raion.

- **Situação:** `CLOSED_CANON_GEO-001.1` — população municipal em 2010 **fechada** (somente este valor/escopo).
- **Resposta ao inventário:** O Atlas de origem diz 'mais de oito milhões'; a diretriz atual do proprietário menciona 7 milhões. Nenhum número de habitantes por raion foi ratificado.
- **Recomendação:** Recomendo propor 7 milhões de residentes no território municipal de 2010, por ser a preferência mais recente, mas **não reinterpretar** o valor antigo como população metropolitana sem decidir expressamente se é substituído, outro recorte ou outro período.
- **Critério de fechamento:** Aprovar número, data, perímetro censitário e tratamento explícito da fonte >8 milhões.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [HIST](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/historia-global/fonte-002.source.md#L100-L150).
- **Proprietários/dependências a conferir:** `world-atlas-novydres`, `world-history-novydres`, `district-*`.

### GEO-002 — Localização, dimensão, coordenadas e escala

- **Situação:** `ABERTO` — decisão canônica **aberta**.
- **Resposta ao inventário:** Há referência histórica à travessia do Estreito de Bering e ambiente ártico, mas sem polígono, projeção, largura, área ou âncora cartográfica aprovada.
- **Recomendação:** Fixar primeiro domínio métrico local com origem, unidades e extensão; só depois adotar ancoragem real no Alasca e transformação apropriada, compatível com costeira, geologia e clima. Não fabricar latitude/longitude.
- **Critério de fechamento:** Aprovar limite municipal, área habitável, extensão, orientação, datum/projeção ou plano local explícito.
- **Fontes verificadas:** [HIST](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/historia-global/fonte-002.source.md#L100-L150) · [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185).
- **Proprietários/dependências a conferir:** `world-atlas-novydres`, `district-*`.

### GEO-003 — Litoral, relevo, Ermo e Rio Vasyl

- **Situação:** `PARCIAL_DOCUMENTADO` — decisão canônica **aberta**.
- **Resposta ao inventário:** Rio Vasyl morno em Chelsea, canais emergentes em New London, deságue em Sulfok; corredores do Ermo entre raions. Faltam geometria de costa, nascentes, baías, ilhas, pontes, solos e sazonalidade.
- **Recomendação:** Construir topologia hídrica e relevo em escala metropolitana antes de desenhar vias. Justificar fisicamente a comunicação entre cursos de água, canais subterrâneos e porto; distinguir água natural, artificial e geotérmica.
- **Critério de fechamento:** Aprovar geometrias-mestras de costa, rios, cursos subterrâneos, gelo, Ermo, ilhas e grandes desníveis.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [HIST](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/historia-global/fonte-002.source.md#L100-L150).
- **Proprietários/dependências a conferir:** `world-atlas-novydres`, `district-*`, `poi-09`, `poi-19`.

### GEO-004 — Raions, bairros e fronteiras administrativas

- **Situação:** `PARCIAL_DOCUMENTADO` — decisão canônica **aberta**.
- **Resposta ao inventário:** Nove raions têm nomes e macroposições nas duas fontes; todos os nove assuntos estão em UNKNOWN/NOT_SELECTED. Nenhuma fronteira territorial fechada foi observada.
- **Recomendação:** Conservar provisoriamente os nove nomes do Atlas e gerar polígonos administrativamente contíguos ou deliberadamente descontínuos; cadastrar enclaves e território fora de raion. Manter grade de tiles independente.
- **Critério de fechamento:** Aprovar lista oficial, fronteiras, áreas especiais, hierarquia raion→bairro→quadra e topônimos/aliases.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [CAT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/catalogo.json).
- **Proprietários/dependências a conferir:** `world-atlas-novydres`, `district-*`, `poi-*`.

### GEO-005 — Formação histórica e expansão urbana

- **Situação:** `PARCIAL_DOCUMENTADO` — decisão canônica **aberta**.
- **Resposta ao inventário:** Fontes discutem 1423/fundação, 1917, 1950–1989, 1990–1998 e 2010; não há mapa de expansão, idade construtiva ou implantação das grandes obras.
- **Recomendação:** Usar fases espaciais rastreáveis: assentamentos antigos, núcleo fluvial, infraestrutura pré-industrial, militar/industrial na Guerra Fria, declínio e reforma. Vincular estilo de quarteirão à época, sem reescrever acontecimentos.
- **Critério de fechamento:** Aprovar linhas do tempo de implantação, mudanças de nome, principais obras e continuidade entre eras.
- **Fontes verificadas:** [HIST](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/historia-global/fonte-002.source.md#L100-L150) · [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185).
- **Proprietários/dependências a conferir:** `world-history-novydres`, `world-atlas-novydres`, `district-*`.

### GEO-006 — Jurisdição territorial cainita e seitas predominantes

- **Situação:** `CANDIDATO_NAO_RATIFICADO` — decisão canônica **aberta**.
- **Resposta ao inventário:** Atlas apresenta Gangrel/Dunwich, Malkavian/Levi, Lasombra/Alexandria, Estados Livres/Chelsea, Ventrue/Bukovie, Banu Haqim/New London, Sulfok disputado, Tzimisce/Drevnigrad, Toreador/Vasyl Bay; sete raions sob Concílio e dois fora de jurisdição plena.
- **Recomendação:** Tomar a grade política do Atlas como proposta prioritária, ratificando domínio e seita separadamente por 2010. Sulfok deve permanecer explicitamente disputado, sem preenchimento com cor de clã único.
- **Critério de fechamento:** Aprovar por raion: soberania formal, controle efetivo, legitimidade contestada, seita, vigência e exceções.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [POL](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/politica-global/fonte-001.source.md#L50-L175) · [LAW](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/politica-global/fonte-002.source.md#L134-L242).
- **Proprietários/dependências a conferir:** `district-*`, `world-politics-novydres`, `org-*`.

### GEO-007 — Influência de clãs, alianças e hostilidades por área

- **Situação:** `LACUNA_DE_MATRIZ` — decisão canônica **aberta**.
- **Resposta ao inventário:** Fontes fornecem hegemonias gerais, favores, pactos, jurisdição transversal Nosferatu, Hecata em Sulfok e influência religiosa; não há matriz clã×bairro com graus de presença, hostilidade e recursos.
- **Recomendação:** Criar matriz multidimensional de influência por clã/facção e raion/bairro: presença, domínio, acesso, autoridade, recursos, oposição e neutralidade. 'Ausente' só com evidência; caso contrário 'não determinado'.
- **Critério de fechamento:** Aprovar influências primárias e secundárias, zonas de não acesso, rivalidades e natureza/capacidade de cada mecanismo de controle.
- **Fontes verificadas:** [POL](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/politica-global/fonte-001.source.md#L50-L175) · [FAITH](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/politica-global/fonte-003.source.md#L36-L107) · [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [NPC](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/organizacoes/escala-de-poder/fonte-004.source.md).
- **Proprietários/dependências a conferir:** `world-politics-novydres`, `org-*`, `district-*`, `npc-*`.

### GEO-008 — Personagens e atores importantes por território

- **Situação:** `INVENTARIO_INCOMPLETO` — decisão canônica **aberta**.
- **Resposta ao inventário:** Há atores públicos citados — Dominique/Vladmir Mishkin, Zara Chispa, Kuthulun, Wilhelmina Harker, Dom Sebastião, entre outros — mas o cadastro global não estabelece todos os endereços, residências, recursos, jurisdição e presença em 2010.
- **Recomendação:** Criar índice espacial por **ID de personagem** com papéis, presença por época, domínio, influência, ativos, local público ou restrito e grau de certeza. Ficha global é dona da identidade; estado da crônica é dono dos acontecimentos.
- **Critério de fechamento:** Aprovar associação região↔ator, papéis e alcance, e classificar explicitamente o que pode aparecer na carta pública.
- **Fontes verificadas:** [POL](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/politica-global/fonte-001.source.md#L50-L175) · [NPC](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/organizacoes/escala-de-poder/fonte-004.source.md) · [CHR](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cronicas/CHR-001/estado/index.md#L32-L100).
- **Proprietários/dependências a conferir:** `npc-*`, `world-politics-novydres`, `district-*`, `chr001-*`.

### GEO-009 — Zonas de conflito, interesse e fronteiras políticas

- **Situação:** `PARCIAL_DOCUMENTADO` — decisão canônica **aberta**.
- **Resposta ao inventário:** Dez frentes narrativas são indicadas no quadro político: sucessão, justiça, fé, Ermo, desigualdade térmica, anarquistas, Sulfok, Lasombra, Crisol, subterrâneo. Falta representação territorial verificável.
- **Recomendação:** Modelar como feições temporais de tipo corredor, polígono, ponto e rede com grau de disputa e ator responsável; distinguir conflito atual, ameaça potencial e rumor.
- **Critério de fechamento:** Aprovar onde cada conflito acontece, fronteiras de risco e enclaves; evitar que qualquer zona secreta apareça na carta municipal.
- **Fontes verificadas:** [POL](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/politica-global/fonte-001.source.md#L50-L175) · [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185).
- **Proprietários/dependências a conferir:** `world-politics-novydres`, `district-*`, `poi-*`, `npc-*`.

### GEO-010 — População, densidade e uso diurno/noturno por raion

- **Situação:** `LACUNA` — decisão canônica **aberta**.
- **Resposta ao inventário:** Macroperfil urbano (centro rico, cidade velha densa, industrial, rural/periférica) está descrito, mas sem números por raion, demanda de viagens, emprego ou densidades plausíveis.
- **Recomendação:** Depois de GEO-001/004, distribuir população residencial com somatório fechado e população diurna de trabalho separada; incluir ocupação aquecida e baixa densidade de Ermo.
- **Critério de fechamento:** Ratificar matriz populacional de cada raion, densidade, empregos e capacidade térmica compatível.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [HIST](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/historia-global/fonte-002.source.md#L100-L150).
- **Proprietários/dependências a conferir:** `district-*`, `world-atlas-novydres`.

### GEO-011 — Bairros, zoneamento, tipologia e desigualdade

- **Situação:** `PARCIAL_DOCUMENTADO` — decisão canônica **aberta**.
- **Resposta ao inventário:** Há vocações históricas e sociais por raion; faltam perímetros de bairros, usos do solo, quarteirões, moradias, áreas de proteção e transição entre paisagens.
- **Recomendação:** Definir centros de atividade, zonas residenciais de diferentes densidades, indústria, comércio, instituições, parques/Ermo e expansão histórica; a estética gótico-punk deve decorrer desse desenho realista.
- **Critério de fechamento:** Aprovar bairros e macrozonas, regras procedurais locais, proteção do Ermo e diretrizes construtivas.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [HIST](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/historia-global/fonte-002.source.md#L100-L150).
- **Proprietários/dependências a conferir:** `district-*`, `world-atlas-novydres`.

### GEO-012 — Vias, pontes, túneis, acesso e hierarquia rodoviária

- **Situação:** `LACUNA_DE_REDE` — decisão canônica **aberta**.
- **Resposta ao inventário:** Posto rodoviário de Dunwich, corredores, circulação industrial e passagens são mencionados; não há grafo viário geral nem conexões entre raions em dados espaciais.
- **Recomendação:** Criar hierarquia expressa/arterial/coletora/local/industrial, nós de troca, travessias únicas e acessos de emergência; separar cruzamento em desnível de conexão em nível.
- **Critério de fechamento:** Aprovar corredores estruturais, pontes/túneis e conectividade metropolitana testável antes de detalhar ruas.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [POI](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L189-L522) · [CHR](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cronicas/CHR-001/estado/index.md#L32-L100).
- **Proprietários/dependências a conferir:** `world-atlas-novydres`, `district-*`, `poi-*`, `chr001-*`.

### GEO-013 — Metrô, trem, bonde, ônibus, ferry e transporte de carga

- **Situação:** `LACUNA_DE_LINHAS` — decisão canônica **aberta**.
- **Resposta ao inventário:** Fontes mencionam metrô/subterrâneo Nosferatu, pátio ferroviário e porto/aeroporto, mas não cadastraram traçado das linhas, estações, intervalos, terminais ou interfaces de ônibus/bonde.
- **Recomendação:** Projetar rede integrada em camadas: metrô troncal, ferrovia suburbana/carga, corredores de ônibus, bonde onde histórico urbano justificar, balsas se água navegável; definir IDs de linhas e estações **após** demanda/centros.
- **Critério de fechamento:** Ratificar tipo, linhas, nós, terminais, cobertura entre raions e separação do acesso subterrâneo restrito.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [POL](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/politica-global/fonte-001.source.md#L50-L175) · [POI](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L189-L522).
- **Proprietários/dependências a conferir:** `world-atlas-novydres`, `district-*`, `poi-21`, `world-politics-novydres`.

### GEO-014 — Geotermia, calefação, tubulações e zonas térmicas

- **Situação:** `PARCIAL_DOCUMENTADO` — decisão canônica **aberta**.
- **Resposta ao inventário:** Existe estação periférica em Chelsea, aquecimento privilegiado de Bukovie e alegações conflitantes de desvio térmico; a crônica apresenta manutenção real, sem rede municipal completa.
- **Recomendação:** Criar grafo de geração→troca→bombeamento→distribuição→edifícios, com capacidade por zona, redundância e falhas; mapear **a desigualdade observável**, mas não converter rumor de sabotagem/desvio em verdade absoluta.
- **Critério de fechamento:** Aprovar plantas, setores de aquecimento, prioridades de carga, corredores técnicos e estado de operação em 2010.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [HIST](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/historia-global/fonte-002.source.md#L100-L150) · [POL](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/politica-global/fonte-001.source.md#L50-L175) · [CHR](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cronicas/CHR-001/estado/index.md#L32-L100).
- **Proprietários/dependências a conferir:** `world-atlas-novydres`, `district-*`, `poi-15`, `chr001-*`.

### GEO-015 — Água, esgoto, drenagem, resíduos, eletricidade e comunicações

- **Situação:** `LACUNA` — decisão canônica **aberta**.
- **Resposta ao inventário:** O rio, galeria e redes técnicas aparecem no lore, mas a estrutura, capacidade e os operadores dos serviços urbanos não são definidos com extensão cartográfica.
- **Recomendação:** Derivar sistemas principais da topografia, população e zonas urbanas; criar camadas de redes públicas separadas das vias clandestinas/secretas, com estações de tratamento e subestações.
- **Critério de fechamento:** Aprovar instalações troncais, bacias de atendimento, operadores e interligações críticas; não exigir cadastro domiciliar.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [HIST](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/historia-global/fonte-002.source.md#L100-L150) · [CHR](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cronicas/CHR-001/estado/index.md#L32-L100).
- **Proprietários/dependências a conferir:** `world-atlas-novydres`, `district-*`, `poi-*`.

### GEO-016 — Prefeitura, subprefeituras, cartórios, tribunais e registros

- **Situação:** `PARCIAL_DOCUMENTADO` — decisão canônica **aberta**.
- **Resposta ao inventário:** Prefeitura (Bukovie), Suprema Corte (New London), conselhos regionais e governo semidemocrático estão descritos; cartórios mencionados, sem distribuição de unidades e competências detalhadas.
- **Recomendação:** Adotar uma sede governamental central em Bukovie e um polo administrativo por raion conforme o sistema político, com fóruns, cartórios e unidades locais distribuídos por demanda e acesso. Confirmar a nomenclatura institucional da cidade.
- **Critério de fechamento:** Ratificar arquitetura do governo, sedes, rede de repartições, competências e polígonos de implantação de todos os complexos nomeados.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [POI](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L189-L522) · [LAW](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/politica-global/fonte-002.source.md#L134-L242).
- **Proprietários/dependências a conferir:** `world-atlas-novydres`, `poi-05`, `poi-06`, `poi-07`, `poi-12`, `district-*`.

### GEO-017 — Saúde: hospitais, clínicas, emergência e atenção primária

- **Situação:** `LACUNA_DE_DIMENSIONAMENTO` — decisão canônica **aberta**.
- **Resposta ao inventário:** Levi menciona instituições hospitalares; Drevnigrad contém clínica privada Harker. Não há contagem municipal, leitos, urgência, maternidades ou cobertura por tempo de viagem.
- **Recomendação:** Definir rede hierárquica para o censo aprovado: hospitais terciários, hospitais gerais regionais, maternidades, clínicas de bairro, postos 24h, ambulâncias e rotas de resgate; quantidades derivadas de cobertura e capacidade, não da ilustração.
- **Critério de fechamento:** Aprovar número e categorias de hospitais/centros, capacidade, localização por raion, operadores e acesso invernal.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [POI](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L189-L522).
- **Proprietários/dependências a conferir:** `district-levi`, `district-drevnigrad`, `poi-24`, `world-atlas-novydres`.

### GEO-018 — Cemitérios, necrópoles, crematórios e funerárias

- **Situação:** `LACUNA_DE_CADASTRO` — decisão canônica **aberta**.
- **Resposta ao inventário:** Os 32 POIs do atlas não incluem uma rede municipal de cemitérios. Isso não prova inexistência de sepultamentos ou instalações mortuárias no mundo.
- **Recomendação:** Dimensionar sepultamento e cremação para população, mortalidade e clima/permafrost; separar cemitérios históricos religiosos, grandes parques funerários, crematórios, funerárias e necrotérios, com rotas e restrições ambientais.
- **Critério de fechamento:** Aprovar número, capacidade, localização e instituições mortuárias, e determinar quais são de interesse Cainita.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [HIST](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/historia-global/fonte-002.source.md#L100-L150).
- **Proprietários/dependências a conferir:** `world-atlas-novydres`, `district-*`, `poi-*`.

### GEO-019 — Polícia, bombeiros, resgate, proteção civil e prisões

- **Situação:** `LACUNA_DE_COBERTURA` — decisão canônica **aberta**.
- **Resposta ao inventário:** Estação de Guarda do Ermo e O Crisol aparecem como instalações especiais, mas não há malha municipal definida de delegacias, quartéis, bases de ambulância, bombeiros ou presídios ordinários.
- **Recomendação:** Planejar serviços por população, distância, risco industrial, Ermo e acessibilidade; distinguir polícia civil, serviços de incêndio, resposta ártica e penitenciárias. O Crisol não substitui a rede carcerária comum.
- **Critério de fechamento:** Aprovar quantidade, jurisdição, capacidade e distribuição das bases, incluindo redundância em isolamento por nevasca.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [POI](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L189-L522).
- **Proprietários/dependências a conferir:** `world-atlas-novydres`, `poi-13`, `poi-29`, `district-*`.

### GEO-020 — Educação, religião, cultura e serviços comunitários

- **Situação:** `PARCIAL_DOCUMENTADO` — decisão canônica **aberta**.
- **Resposta ao inventário:** Catedral de Santa Sophia, Universidade Teológica, mesquita Al-Nur, sinagoga Beit HaZikaron, seminário e campus técnico estão descritos; faltam escolas e equipamentos cotidianos por bairro.
- **Recomendação:** Planejar escolas, universidades, bibliotecas, centros culturais e equipamentos de vizinhança por perfil demográfico. Manter influência Cainita sobre fiéis distinta de propriedade mortal ou controle eclesiástico.
- **Critério de fechamento:** Aprovar distribuição de equipamentos e classificação de polos religiosos/culturais com controle mortal e influência noturna separados.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [FAITH](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/politica-global/fonte-003.source.md#L36-L107) · [POI](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L189-L522).
- **Proprietários/dependências a conferir:** `poi-10`, `poi-11`, `poi-12`, `poi-20`, `poi-31`, `poi-32`, `district-*`.

### GEO-021 — 32 locais nomeados e outros complexos relevantes

- **Situação:** `32_CANDIDATOS_SEM_GEOMETRIA` — decisão canônica **aberta**.
- **Resposta ao inventário:** Há 32 POIs com nome e raion, e 32 assuntos locais separados, todos com duas variantes idênticas e autoridade NOT_SELECTED; nenhum possui geometria cadastral aprovada nesta base.
- **Recomendação:** Auditar cada POI por ID, confirmar existência em 2010, papel, operador, superfície/lote, área, capacidade, mobilidade e divulgação; diferenciar bairro, corredor, estação, prédio e complexo. Acrescentar novos locais essenciais sem renumerar antigos.
- **Critério de fechamento:** Ratificar catálogo de equipamentos obrigatórios e polígono/posição para cada um, com referência ao assunto proprietário e sem duplicações.
- **Fontes verificadas:** [POI](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L189-L522) · [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [CAT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/catalogo.json).
- **Proprietários/dependências a conferir:** `world-atlas-novydres`, `poi-01..poi-32`, `district-*`.

### GEO-022 — Mapa oficial, atlas V5, tiles, legenda e confidencialidade

- **Situação:** `ARQUITETURA_APROVADA_DADOS_ABERTOS` — decisão canônica **aberta**.
- **Resposta ao inventário:** PRD e ADR-002 já estão aprovados para planejamento; não há geometria única, mapa técnico validado nem inventário de legenda aptos a imagens finais.
- **Recomendação:** Gerar primeiro carta vetorial técnica determinística, depois diagramação gótico-punk V5; tiles 3×3/5×5 somente recortes da geometria; versões pública e restrita separadas. Proibir ícones sem entidade e decoração pseudo-cartográfica.
- **Critério de fechamento:** Só fechar quando GEO-001..021 pertinentes à escala estiverem fechados e forem executados testes de geometrias, redes, rótulos, visibilidade e exportação.
- **Fontes verificadas:** [AT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/atlas-novydres/fonte-001.source.md#L54-L185) · [POL](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/cenario/politica-global/fonte-001.source.md#L50-L175) · [CAT](https://github.com/Niltond3/novydres-persistence-poc/blob/7ce8e88c122a5d80879e30a23b1f3be159cac727/novydres/catalogo.json).
- **Proprietários/dependências a conferir:** `world-atlas-novydres`, `district-*`, `poi-*`, `cartografia/*`.

## Candidatos cuja auditoria transversal ainda é obrigatória

Antes de qualquer `CLOSED_CANON`, executar a busca por dependências no snapshot atual: (i) todos os assuntos de raion e POI; (ii) personagens globais e fontes de política relacionadas; (iii) episódios e registros temporais da crônica com geografia ou personagens de interesse; (iv) fatos de fonte já aprovados por decisão expressa; (v) documentos e visualizações derivadas. Não reconstruir fatos antigos a partir de interpretações posteriores.

**Status global:** `P0_CROSS_REFERENCE_IN_PROGRESS`, `22/22_TOPICS_RECOMMENDATIONS_DRAFTED`, `1/22_CANON_CLOSED`. Não liberar geração de arte definitiva. Protótipos sintéticos claramente identificados não alteram esse status.
