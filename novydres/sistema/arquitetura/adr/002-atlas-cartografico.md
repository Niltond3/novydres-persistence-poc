---
adr_id: ADR-002
title: Arquitetura do Atlas Cartográfico Canônico de Novydres
status: APROVADO_PARA_PLANEJAMENTO
date: 2026-11-14
scope: NOVYDRES_ATLAS_CARTOGRAFICO
related_adr: ADR-001
owner_scope: novydres/sistema/arquitetura
visibility: PLAYER_SAFE
source_snapshot: 2880156293d11496669806a4b66bc4107d44573e
approval_scope: METODO_APROVADO_GEOGRAFIA_NAO_CANONIZADA
approved_on: 2026-11-14
---

# ADR-002 — Arquitetura do Atlas Cartográfico Canônico de Novydres

## 1. Contexto

A geração direta de um mapa completo por um modelo de imagens produziu forte atmosfera, mas não garantiu coerência de ruas, transportes, instituições, hidrografia, legendas ou continuidade entre recortes. O projeto agora precisa **definir progressivamente o próprio cânone geográfico**, preservando o cânone previamente existente, e produzir imagens que representem fatos e geometrias aprovados.

A arquitetura Git-native orientada por assunto do ADR-001 já está implantada. O assunto existente `world-atlas-novydres` mantém uma proposta editorial única para fatos ainda abertos e fontes canônicas únicas para fatos aprovados; raions e locais mantêm seus assuntos próprios. O novo projeto não pode recriar um catálogo paralelo de verdades nem transformar candidatos em fatos aprovados.

## 2. Decisão arquitetural proposta

Adotar, por aprovação expressa do proprietário, uma arquitetura **Git-native, subject-oriented e cartográfica por dados**, na qual:

1. ChatGPT Web conduz análise, planejamento, edições, verificações e revisão com o proprietário.
2. GitHub mantém decisões, dados espaciais, código de geração, histórico e resultados aprovados.
3. Um modelo geoespacial estruturado é a única fonte de geometria das visualizações.
4. Cartografia técnica vetorial é a representação-base; imagens generativas são acabamento e componentes ilustrativos, nunca autoridade de localização.
5. A cartografia admite propostas de novos bairros, instituições, redes e formação histórica, mas **a aprovação de um modelo visual não equivale à canonização do que ele inventar**.
6. O projeto opera dentro do ADR-001 e não muda o runtime de crônica, fatos protegidos ou gateways existentes.

## 3. Limites de autoridade e propriedade

- **Assunto de Atlas:** `novydres/cenario/atlas-novydres` é agregador cartográfico do território e dono de sua representação espacial; fontes editoriais obsoletas são retiradas da árvore corrente e recuperáveis somente pelo histórico Git, não como autoridade concorrente.
- **Raions, bairros e lugares:** os assuntos proprietários existentes em `novydres/cenario/geografia/` e `novydres/cenario/lugares/` mantêm a semântica de cada conceito. A cartografia guarda geometria e referência por ID, não uma segunda biografia ou verdade rival.
- **Outras entidades:** história, organizações, pessoas e eventos permanecem nos respectivos assuntos. A geometria os referencia quando necessária, respeitando sigilo e temporalidade.
- **Conflitos:** `CONFIRMED`, `NPC_CLAIM`, `GM_PREPARED`, `CONDITIONAL`, `UNKNOWN` e classificações editoriais do sistema vigente não são substituídos por um simples indicador `aprovado`. O registro cartográfico de proposta/decisão é **um estado de fluxo de trabalho distinto**, que mantém a autoridade epistêmica original.
- **Canonização:** informação nova com alcance global só se torna canônica após autorização substantiva e escrita no assunto proprietário, acompanhada do vínculo espacial aprovado. Citar a aprovação e preservar fontes e variantes anteriores.
- **Sigilo:** carta pública não incorpora domínios, refúgios, relações Cainitas nem outros dados restritos por simples presença técnica no repositório. Metadados `PLAYER_SAFE` não constituem ACL real.

## 4. Organização documental e técnica

Local proposto para o PRD e, futuramente, materiais cartográficos subordinados ao assunto já existente:

`novydres/cenario/atlas-novydres/cartografia/`

Documento arquitetural:

`novydres/sistema/arquitetura/adr/002-atlas-cartografico.md`

A organização poderá incluir, **somente conforme surgirem necessidades reais**, registros de decisões, regras espaciais, dados, estilos, validação e exportação. Não criar um segundo `assunto.json` sem justificar a criação de outro assunto e atualizar o catálogo derivado conforme as ferramentas do ADR-001. Não usar nomes com sufixos de revisão para arquivos correntes.

### Emenda expressa — fonte única (15/11/2026)

Depois que um fato recebe aprovação e propagação, qualquer documento corrente que contenha uma versão obsoleta e contraditória deve ser corrigido ou retirado da árvore atual. Para conteúdos não canonizados, manter **uma única versão candidata corrente**; projeções por raion/POI referenciam esta versão sem se tornarem autoridades independentes. A proveniência histórica fica nos commits Git, não em arquivos `deprecated` ou `archive` no HEAD. Não reescrever fatos jogados na crônica automaticamente.

## 5. Modelo de dados

Uma feição espacial relevante terá, quando aplicável:

- `feature_id` estável, `kind` e referência ao `subject_id` proprietário;
- geometria validada (ponto, linha, polígono, multipolígono) e sistema de referência explícito;
- período de validade ou ano de referência;
- fonte, decisão, estado epistêmico e estado do fluxo cartográfico;
- nome público, possíveis aliases e visibilidade;
- relações topológicas ou nós/arestas para redes; escala de exibição para símbolos e rótulos.

**Não falsificar latitude/longitude.** Até que uma referência geográfica seja escolhida, podem ser utilizadas coordenadas métricas locais documentadas em formato próprio. GeoJSON interoperável deve respeitar o sistema de coordenadas que sua especificação exige (WGS84); a conversão só ocorrerá após a definição verificável de ancoragem geográfica, ou será utilizada uma renderização própria de plano local claramente identificada. Não alegar escala real se extensão e medidas ainda forem hipóteses.

Para redes de transporte, o desenho visual da linha não substitui o grafo de estações, segmentos e conexões. Atribuir a cada ponte ou túnel suas entradas e saídas reais.

## 6. Ferramentas e execução

**Implementação preferencial, sujeita a protótipo:**

- GitHub pelo conector do ChatGPT Web para consultas e gravação textual com controle de concorrência;
- TypeScript ou Python para dados, regras procedurais, testes e renderização SVG;
- GitHub Actions para validação e geração automatizada quando configurado;
- MapLibre GL JS para visualizador interativo, se as coordenadas e o pipeline forem compatíveis;
- exportações SVG/PNG/PDF a partir do mapa técnico; imagem generativa somente para elementos artísticos controlados.

O uso de QGIS, Figma, infraestrutura externa ou edição manual não é obrigatório no início. Não presumir que um conector executa programas arbitrários: computação, builds e hospedagem precisam de ambiente efetivo e prova prática. Se houver limitação, reportar e propor alternativa que preserve o fluxo pelo ChatGPT Web.

**Hospedagem:** qualquer publicação online de mapas exige avaliação explícita de visibilidade e licenças. Um repositório privado ou um rótulo de sigilo não garantem que uma página publicada seja privada. Camadas restritas não devem ser entregues ao cliente público.

## 7. Ciclo de trabalho e controle de mudanças

1. Resolver o assunto e dependências em **um único SHA** do `master` e inventariar fatos relevantes.
2. Identificar fatos existentes, variantes, propostas e conflitos, com fonte e autoridade próprias.
3. Submeter ao proprietário somente decisões substantivas, agrupadas por impacto; mudanças triviais podem ser geradas segundo regras aprovadas.
4. Trabalhar em branch de proposta. Criar mudanças atômicas e verificáveis por commit; usar base/HEAD esperado e `force=false`, conciliando avanços concorrentes.
5. Validar schemas, IDs, topologia, cruzamento de legendas, integrações e não divulgação.
6. Conferir commit/ref/tree/arquivos no remoto; somente informar publicação após readback.
7. Após aprovação, integrar alterações ao assunto proprietário e atualizar catálogo/indexação derivados conforme ADR-001; a presença em branch de proposta **não** é canonização.
8. Reconstruir mapas afetados a partir da geometria única, sem rerenderização generativa de ruas como fonte.

Nenhum commit cartográfico altera cenas, rolagens, XP/FV ou decisões narrativas fechadas. Separar execução de cartografia de transações de jogo.

## 8. Regras cartográficas invariantes

- **Continuidade:** bordas entre setores não interrompem ruas, rios, ferrovias, litoral nem redes.
- **Identidade:** a mesma instalação é a mesma feição, independentemente do zoom; não duplicar números ou nomes sem justificativa.
- **Correspondência:** só entra na legenda o que está representado e identificável na escala pertinente.
- **Redes:** os segmentos atendem às conexões declaradas; cruzamentos sem ligação (viadutos, túneis) não viram entroncamentos falsos.
- **Escala:** mapas gerais simplificam detalhes em vez de inventá-los; recortes mais próximos revelam geometrias adicionais aprovadas ou geradas sob regras validadas.
- **Estética:** o grafismo de Vampiro V5 é camada de apresentação; ícones temáticos não substituem elementos cartográficos como a rosa dos ventos. Evitar duplicações decorativas e texto simulado ilegível.
- **Reprodutibilidade:** no mesmo commit, a versão técnica das camadas produz saída logicamente idêntica.

## 9. Portas de decisão antes da arte definitiva

**D0 — Inventário e reconciliação:** localizar fontes autoritativas, estabelecer fatos aceitos e registrar divergências, com atenção a população, raions, Rio Vasyl, localização da cidade e instituições. Não promover variantes candidatas automaticamente.

**D1 — Quadro geográfico:** aprovar abrangência, coordenadas, extensão, hidrografia, relevo, litoral, fronteiras, referência temporal e histórico urbano essencial.

**D2 — Sistema metropolitano:** aprovar organização dos centros, distribuição populacional, grandes corredores de transporte e infraestrutura de sustentação.

**D3 — Instalações e tipologia:** aprovar inventário e localização dos complexos obrigatórios, seus acessos, relações e hierarquia.

**D4 — Prontidão para cartografia final:** confirmar ausência de decisões críticas em aberto para o escopo renderizado, integrações topológicas válidas, símbolos correspondentes e condições de confidencialidade. Então produzir carta técnica e tratamento artístico.

Um **protótipo não canônico** de uma pequena região pode ocorrer cedo para provar a tecnologia; não equivale à liberação de imagens definitivas.

Bloqueios são **somente falhas materiais verificadas ou decisões de autoridade necessárias**. Não exigir relatórios repetitivos nem um gate para cada arquivo.

## 10. Alternativas consideradas

- **Megaprompt único para o gerador de imagem:** rejeitado como fonte de verdade; não preserva geometria ou correspondência institucional verificáveis.
- **Gerar separadamente 9 ou 25 tiles e uni-los:** rejeitado para a base; não garante continuidade.
- **Editor GIS manual como ferramenta obrigatória:** adiado; é possível testar geração assistida por código antes de impor operação manual.
- **Modelo vetorial e renderizador determinístico + acabamento artístico:** opção recomendada por suportar revisão incremental, rastreabilidade e exportação multiescala.

## 11. Consequências, riscos e aprovação

Benefícios: uma só cidade entre mapas, histórico Git, melhor controle de instituições e infraestrutura, produção incremental e variantes públicas/narrativas. Custos: planejamento, dados estruturados, testes e uma primeira implementação técnica. Riscos residuais: conectores e hospedagem podem exigir configuração; algoritmos de urbanismo não substituem juízo editorial; dados insuficientes não autorizam inventar precisão.

**Estado:** ADR-002 aprovado pelo proprietário em 14/11/2026 como diretriz de planejamento, sem ativar por si só runtime cartográfico. Este documento não canoniza uma localização, número populacional, malha viária, instalação, tecnologia definitivamente selecionada ou cronologia; a decisão arquitetural e o desenvolvimento seguem sujeitos à aprovação do proprietário e às regras do ADR-001.
