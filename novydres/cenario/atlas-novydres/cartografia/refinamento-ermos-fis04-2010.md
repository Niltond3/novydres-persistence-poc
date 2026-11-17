---
document_id: MW-013-FIS04-ERMO-REFINEMENT-2010
subject_id: world-atlas-novydres
reference_year: 2010
work_unit: MW-013
workflow_status: REJECTED_REDESIGN_REQUIRED
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED
source_master_sha: cea4284fcf9cfa6fb531b7e693181420dcbddb56
source_branch_checkpoint: 7a67e197205afa87ecb20545bce847d33fc9c402
rejected_geometry_blob_sha: ea3d170930cf7e5a626bb8a800ca90004f2467a4
---
# MW-013 — Revisão de FIS-04 após rejeição da representação

## Decisão expressa do proprietário
O proprietário observou que **“essa representação não está boa”**, porque confundia os Ermos com maciços rochosos, tundra, brejos e outras unidades de relevo. A geometria MW-013 de dez pequenas manchas naturais foi **rejeitada como representação territorial de FIS-04**. Nenhuma geometria FIS-04 foi aprovada ou canonizada.

A revisão prévia passou em 11.795 asserções sintéticas, porém **essas verificações não testaram o significado territorial exigido**. O resultado não valida a cartografia dos Ermos. Os dez contornos rejeitados permanecem recuperáveis somente no histórico Git. O campo estruturado atual `wilderness_model.corridor_segments` está vazio até que uma candidata apropriada seja produzida.

## Definição correta a orientar a geometria
Os Corredores do Ermo representam **áreas de território que a expansão civilizacional não dominou de forma permanente**, independentemente da topografia dominante. São a natureza indomada, de múltiplos perigos e limites de habitabilidade, interposta entre e ao redor dos núcleos históricos de ocupação. Podem incluir montanhas, planícies, tundra, várzeas, floresta, litoral ou combinação desses ambientes. As quatro categorias canônicas GEO-003.5 são **contextos físicos**, não o critério exclusivo de delimitação.

A formação urbana policêntrica e o envio estratégico de emissários por Gilgamesh constam da fonte canônica `novydres/cenario/historia-global/formacao-policentrica-2010.json`. A expansão dessas ocupações foi condicionada pelos perigos do território; não presumir uma expansão radial de cidade contínua. O proprietário mencionou feras indomáveis, hordas, possíveis caerns Garou e riscos a Cainitas muito poderosos **como exemplos de explicações possíveis**, não como novos fatos cartográficos, domínios/caerns localizados ou aprovação de metatrama.

## Regra para a próxima variante
1. Desenhar **grandes extensões intersticiais e envolventes de natureza não submetida à ocupação**, com fronteiras irregulares e heterogêneas, sem usar o contorno de uma serra como perímetro obrigatório de Ermo.
2. Manter separadas as camadas de **território do Ermo**, **fisiografia** e **causas de perigo**. Estas últimas podem ser múltiplas ou desconhecidas.
3. Não inventar nem ratificar posições dos nove raions, dos núcleos de povoamento, das rotas de passagem, de caerns ou de criaturas; sem suas pegadas, a separação física de núcleos permanece **não demonstrada**.
4. Preservar rigorosamente costa MW-010, relevo MW-011 e hidrografia MW-012 como bases de trabalho não canônicas. A nova geometria não poderá invadir mar ou corpos lacustres como terra.
5. Travessias naturais ou artificiais podem atravessar Ermo, mas não implicam conurbação. GEO-012/013 continuam fora desta unidade.

## Estado da implementação
`macroermos-2010.proposal.json`: sem polígonos atuais, com interpretação territorial corrigida e aprovação `REJECTED_REDESIGN_REQUIRED`.
`visualizador-fisico-2010.html`: removidos os dez polígonos rejeitados, com alerta de que FIS-04 está em redesenho; as camadas MW-010 a MW-012 continuam inalteradas.
`validar-macroermos.mjs`: adaptado para verificar a ausência de geometria vigente e a preservação de estados e dependências; não confundir este teste de governança com validação de nova geometria.

**A:** nova proposta territorial de Ermo, comparação visual e todas as aprovações ainda pendentes. **B:** posição efetiva de núcleos urbanos só poderá ser comprovada em unidade posterior de ocupação. **C:** Garou, caerns, criaturas e metatrama não terão localização ou história fixadas em MW-013.

**MW-013 permanece ABERTO. Não emitir handoff.**

## Proposta A — malha territorial (segunda interpretação)
O proprietário solicitou uma malha irregular conectada de **natureza não domada**, ramificada entre núcleos cuja localização administrativa ainda não foi definida. O isolamento da maioria dos núcleos é a regra histórica; conurbações podem surgir com desenvolvimento tecnológico, eliminação de ameaças e alterações da habitabilidade, sem transformar isso em regra para todos os raions.

Diretrizes **topológicas verbais e provisórias**, não geocodificadas: Sulfok–Kingswell/Cidade Velha como continuidade urbana; separação por Ermo entre Bukovie–Kingswell e entre Bukovie–Alexandria; demais adjacências em aberto. Embora GEO-004.6A confirme o cinturão econômico Sulfok–Kingswell, ele **não torna conurbação obrigatória**: a indicação corrente permanece hipótese geométrica até aprovação formal, sem alteração canônica. Raion oficial: Alexandria.

`malha-territorial-ermos-fis04-2010.proposal.json`: nova proposta alternativa com 10 envelopes irregulares de territórios hostis com eixos conectados; sem fixar qualquer núcleo, bairro, raion ou rota. Os espaços sem Ermo **não** são automaticamente áreas urbanas. `comparador-malha-ermos-fis04-2010.html`: comparador geográfico 2D autocontido, ligado às mesmas geometrias de costa, relevo, rios e águas, com camadas ligáveis.

Validação preliminar JS: 10 componentes, 478 vértices, 818 testes de pontos e 51025 testes de cruzamento, sem autointerseções, invasões de mar ou lagoas; espinha conectada por nós compartilhados. Distância mínima de vértice à costa: 2219 m. Soma de área sintética bruta antes da fusão geométrica e descontagem de sobreposições: 3178 km², **não é área territorial**. Ainda não verificada união topológica rigorosa dos envelopes nem separação de núcleos; não rodou navegador nem CI.

**Porta de decisão atual:** aprovar a configuração morfológica geral da malha A como hipótese de trabalho, rejeitar ou pedir alterações. Isso **não** aprova fronteiras dos raions, perigos individuais, rotas ou canonização. A antiga `macroermos-2010.proposal.json` permanece rejeitada e vazia até aprovação explícita de substituição; não gerar handoff.


## Decisão do proprietário — composição aprovada, geometria ainda rejeitável
Em 16/11/2026, o proprietário **aprovou a composição territorial geral da malha A**, entendida apenas como organização macroterritorial conectada e ramificada dos Ermos. **Ressalva obrigatória:** os contornos atuais parecem excessivamente quadrados e semelhantes a pinceladas; necessitam refinamento substancial para parecerem **orgânicos**. A aprovação **não** abrange a forma final dos polígonos, a localização de raions, travessias, cores, nem canonização.

Critério para a próxima variante dentro de MW-013: conservar o esqueleto topológico aprovado, porém construir envelopes com ramificações de largura variável, curvas e reentrâncias naturais em escalas diferentes, conexões fluidas e contornos coerentes com o relevo e a hidrografia. Não gerar ruído aleatório decorativo: a geometria estruturada deve preceder a imagem. Entregar comparação 2D e submeter **a nova geometria** a aprovação individual e final antes de fechar. MW-013 permanece aberto, sem handoff.


## Refinamento orgânico B e regra de visão integral
Solicitação expressa do proprietário: refinar a borda quadrada/pincelada e **sempre apresentar o antes e o depois da composição completa**, sem omitir ilhas ou afluentes. A regra foi documentada em `cartografia/guide.md` nesta branch; não foi publicada em master.

`malha-territorial-ermos-fis04-2010.refined.proposal.json`: segunda candidata estruturada; 10 envelopes, mesmos eixos e relações; margens suavizadas por duas passagens de Chaikin, amostragem de perímetro a 480m e variação normal com quatro comprimentos de onda, condicionada a ausência de autointerseção e invasão de áreas aquáticas. Contornos de 478 para 2349 vértices; somente margens mudaram. Não foi fixado nenhum raion, núcleo urbano ou rota.

`comparador-integral-ermos-fis04-2010.html`: dupla vista integral simultânea, ANTES/DEPOIS, mesma escala e folha inteira. Compõe automaticamente a costa original, três ilhas, 7 áreas de relevo, 3 cristas, 9 cursos d'água, 3 corpos d'água, 1 trecho termal, 5 bacias opcionais e limiar de baía; eixos técnicos opcionais. Padrão de cores é somente auxílio de leitura e **não está aprovado para imagem final**. Todas as camadas de contexto têm as mesmas coordenadas de fonte nas duas vistas.

Pré-validação automática preliminar JS: 2349 consultas a pontos de anéis, ambas as costas terrestres e bordas internas respeitadas, nenhum anel autointersectante, nenhum corpo d'água cruzado ou englobado, componentes conectados pelo grafo de eixos original. Esta verificação é preliminar; não atesta união topológica exata dos envelopes, nem colonização, nem execução real de navegador/Node/CI. Inventário: {"coastline":1,"islands":3,"relief":7,"crests":3,"basins":5,"rivers":9,"waterbodies":3,"thermal":1}. Parser JavaScript da vista comparativa: SYNTAX_OK.

**GATE:** somente a composição macroterritorial A está aprovada; a nova borda orgânica B **aguarda aprovação expressa do proprietário**, podendo exigir novas iterações. Não fazer handoff nem canonização.


## Decisão individual — refinamento orgânico B aprovado
Em 16/11/2026, o proprietário respondeu **“Aprovo”** à apresentação e à pergunta sobre aceitar a versão orgânica B como **nova base de trabalho não canônica**. Escopo da aprovação: contornos orgânicos B, preservada a composição A já aprovada. Esta decisão **não é** o aceite consolidado final de MW-013 e **não canoniza** FIS-04, raions, cores, transportes ou perigos narrativos.

O arquivo `malha-territorial-ermos-fis04-2010.refined.proposal.json` registra `APPROVED_NONCANONICAL_WORKING_BASELINE`, mantendo `canonical_status=NOT_APPROVED`.

### Validação complementar integrada
Antes da gravação, foi executado em JavaScript o corpo do validador reproduzível `validar-malha-territorial-fis04.mjs` com os textos efetivos obtidos do GitHub e adapter local de leitura/asserções. Resultado: **{"status":"PASS","branch_parts":10,"union_components":1,"vertices":2349,"points":2689,"coast_water_edge_checks":180873,"self_intersection_pairs":360367,"full_visual":{"islands":3,"relief":7,"crests":3,"basins":5,"watercourses":9,"waterbodies":3,"thermal":1}}**. Conferidos: malha conectada como união por contato dos dez envelopes, nenhum cruzamento de costa, lagoas ou auto-interseção, preservação dos eixos, comparação exata dos dois conjuntos de anéis, e totalidade de costa, 3 ilhas, 7 relevos, 3 cristas, 5 bacias, 9 cursos d'água, 3 corpos d'água e trecho termal. Nenhuma camada antecedente modificada.

**Limite de validação:** teste lógico sintético no conector; Node CLI, navegador real, geodésia e pegadas urbanas não foram executados/certificados. As ilhas seguem hipóteses. A malha não atribui posições aos raions.

**GATE FINAL:** solicitar ao proprietário o aceite **consolidado** de FIS-04, explicitamente distinto das aprovações de composição e refinamento, após readback remoto da publicação. Somente depois poderá atualizar a proposta FIS-04 principal, fechar MW-013 e criar handoff, se as verificações finais continuarem PASS.


## Fechamento integral do MW-013 — aprovado expressamente pelo proprietário
**Decisão final:** em 16/11/2026, depois de aprovar separadamente a composição territorial A e o refinamento orgânico B, o proprietário respondeu **“Aprovo”** à pergunta de aceite **consolidado final** de FIS-04, com adoção da malha orgânica B exclusivamente como **base cartográfica de trabalho não canônica**.

**Entregáveis efetivos:**
- `macroermos-2010.proposal.json` atualizado como projeção estruturada integrada da malha B, com dez polígonos FIS-04 e referência precisa ao blob-fonte da variante refinada B. Cânone permanece `NOT_APPROVED`; antigo refinamento rochoso rejeitado permanece somente histórico.
- `malha-territorial-ermos-fis04-2010.refined.proposal.json` confirmado como autoridade da geometria candidata aceita. 10 componentes conectados, 2.349 vértices de borda; eixos territoriais mantidos.
- `visualizador-fisico-2010.html` novamente exibe a camada FIS-04 em conjunto com costa, **três ilhas hipotéticas**, relevo, hidrografia e demais referências; camada de Ermo não é categoria fisiográfica.
- `comparador-integral-ermos-fis04-2010.html` preserva ANTES/DEPOIS completos da aprovação; todas as feições físicas de contexto coincidem entre as vistas. Sua atualização visual não confere status a cores finais.
- `validar-malha-territorial-fis04.mjs`: topologia, conexões dos envelopes e comparação integral; `validar-macroermos.mjs`: leitura da proposta principal, igualdade com fonte B e completude de inventário.
- `guide.md`: protocolo obrigatório de visão integral ANTES/DEPOIS, com ilhas e todos os cursos de água.

**Validações:** corpo do validador da malha executado no conector com fontes GitHub: 10/10 envelopes conectados por contato, **2.689 pontos**, **180.873 testes de interação com costa e águas** e **360.367 pares de segmentos verificados contra autointerseção**, tudo PASS; 3 ilhas, 7 relevos, 3 cristas, 5 bacias, 9 cursos d'água, 3 corpos d'água e trecho termal íntegros no comparador. A integração principal foi conferida por comparação exata de coordenadas e scripts de visualização compiláveis. **Sem execução de browser/Node CLI/CI real**, nem certeza geodésica, mensuração oficial ou união geométrica materializada num polígono único.

**Estado final da unidade:** FIS-04 **OWNER_APPROVED_NONCANONICAL_WORKING_BASELINE_CLOSED_FOR_SCOPE**. Nenhum raion foi posicionado, não houve fronteira administrativa, transporte, alocação de seres sobrenaturais ou canonização. A separação real entre os núcleos será confrontada quando houver geometria urbana/raions. Áreas não demarcadas não equivalem automaticamente a urbanização.

**Pendências remanescentes A/B/C:** A da geometria FIS-04 desta unidade: **nenhuma**; B: integração posterior com ocupação e raions, conservação das travessias naturais e técnicas sem antecipar rotas; C: ameaças narrativas, controvérsias Cainitas e metatrama fora do escopo. A próxima unidade terá objetivo e aprovações independentes.

**MW-013: FECHADO EM ESCOPO. Não promover a master nem canonizar automaticamente.**
