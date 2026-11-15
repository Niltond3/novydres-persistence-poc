---
document_id: PRD-ATLAS-001
title: Atlas Cartográfico Canônico de Novydres
status: APROVADO_PARA_PLANEJAMENTO
date: 2026-11-14
subject_id: world-atlas-novydres
owner_scope: novydres/cenario
visibility: PLAYER_SAFE
source_snapshot: 2880156293d11496669806a4b66bc4107d44573e
approval_scope: METODO_APROVADO_GEOGRAFIA_NAO_CANONIZADA
approved_on: 2026-11-14
---

# PRD — Atlas Cartográfico Canônico de Novydres

## 1. Visão e finalidade

Construir progressivamente a geografia urbana de Novydres (recorte de referência: 2010) e produzir, a partir dela, uma cartografia coerente, editável, verificável e visualmente gótico-punk, adequada a Vampiro: A Máscara V5. O Atlas **não é somente um ilustrador**: poderá propor novas definições de território, bairros, história urbana, infraestrutura e instituições, submetendo as decisões relevantes à governança do NOVYDRES antes de sua canonização.

**Princípio:** a geometria e os fatos aprovados geram as imagens; imagens geradas nunca estabelecem fatos ou posições por si mesmas.

## 2. Autoridade e ponto de partida

- Reutilizar o assunto existente `world-atlas-novydres`, em `novydres/cenario/atlas-novydres/`. Não criar um atlas concorrente.
- Consultar `AGENTS.md`, `CONTEXT.md` e `catalogo.json` no mesmo commit, conforme ADR-001.
- A única proposta editorial corrente para fatos geográficos ainda abertos é `../atlas-proposta.md`. Versões anteriores foram retiradas da árvore corrente e continuam recuperáveis apenas por commits Git. A proposta não canoniza automaticamente raions ou locais.
- Os nove **raions administrativos** não equivalem à grade cartográfica 3×3; qualquer grade de tiles é apenas uma maneira de exportar o território.
- A aprovação expressa do proprietário autoriza este PRD e o ADR-002 como diretrizes do trabalho cartográfico. **Não aprova nova geografia, novos números populacionais, mudança de história ou publicação de mapa definitivo.**
- Respeitar a separação entre geografia global, conceitos de distritos, locais, conhecimento por personagem e história de crônica. Fatos conflitantes permanecem assinalados até decisão expressa.

## 3. Pessoas e usos

1. **Proprietário/diretor criativo:** decide cânone, conflitos relevantes, prioridades e linguagem narrativa.
2. **Agente cartográfico no ChatGPT Web:** pesquisa fontes autorizadas, propõe, modela, implementa, valida e publica alterações aprovadas via GitHub.
3. **Narrador:** consulta a cartografia e, quando autorizado, camadas restritas de ambientação.
4. **Jogador/leitor:** consulta versão urbana pública, sem informações secretas.
5. **Sistema técnico:** gera mapas consistentes de várias escalas sem reinventar geografia.

## 4. Escopo do produto

**Incluído:** limites e extensão da cidade; relevo, costa, água e gelo; desenvolvimento histórico e crescimento urbano; raions e bairros; densidade e população; vias, pontes, túneis, transporte público, metrô, ferrovias e terminais; aeroporto, portos, geotermia, energia, aquecimento, água e saneamento; instalações administrativas, saúde, segurança, educação e outros serviços; mapas técnicos oficiais; visualização interativa; exportações multiescala e camada editorial inspirada no clima gótico-punk de V5.

**Incluído com restrição:** camadas Cainitas e outras informações narrativas somente quando sua visibilidade e autorização estiverem claras; nunca incorporadas silenciosamente à carta pública.

**Fora do escopo inicial:** novo runtime da crônica, alteração de ficha/XP/FV, reprodução de marcas ou páginas oficiais de V5, simulação completa de tráfego e certificação de engenharia civil. A precisão pretendida é **coerência ficcional e cartográfica verificável**, não precisão cadastral de uma cidade real.

## 5. Requisitos funcionais

- **RF-01 — Base única:** o mapa geral, recortes 3×3/5×5, mapas distritais e exportações derivam da mesma geometria versionada, nunca de redesenhos independentes.
- **RF-02 — Identificação estável:** entidades espaciais importantes possuem ID estável, tipo, nome, fonte/proveniência, tempo de referência, estado de aprovação e relação com assunto proprietário.
- **RF-03 — Geografia física:** o modelo descreve limites, topografia, hidrografia, costa, ilhas, Ermo e zonas térmicas; mudanças não quebram relações espaciais existentes sem sinalização.
- **RF-04 — Rede viária:** vias possuem hierarquia e conexões reais entre segmentos; ruas, rodovias, pontes, túneis e vias de acesso não são somente textura visual.
- **RF-05 — Transporte:** metrô, trem urbano, carga, intercâmbios, estações, depósitos e linhas obedecem a conexões topológicas e atendem à distribuição metropolitana proposta.
- **RF-06 — Serviços e instituições:** instalações representadas têm localização e implantação física adequadas à escala (ponto, edifício, lote ou complexo), identificação única e vínculo com vias/transportes apropriados.
- **RF-07 — Coerência urbana:** padrões residenciais, comerciais, industriais e institucionais refletem crescimento histórico, relevo, capacidade infraestrutural e desigualdade socioespacial.
- **RF-08 — Legendas honestas:** um item da legenda só descreve uma entidade mapeada; instituição citada como existente precisa estar registrada e localizável. Símbolos, índices e rótulos não podem divergir.
- **RF-09 — Multiescala:** níveis de detalhe dependem de zoom/escala; recortes preservam alinhamento exato de rios, vias, divisas e infraestrutura.
- **RF-10 — Camadas distintas:** carta urbana pública, camada editorial V5 e sobreposições narrativas utilizam base compartilhada; conteúdo restrito não vaza em exportações públicas.
- **RF-11 — Histórico de decisões:** propostas, aprovações, rejeições e correções relevantes são rastreáveis por fonte e commit, sem duplicar a verdade.
- **RF-12 — Produção:** renderizar uma carta técnica vetorial, exportações raster sob resolução solicitada (incluindo 3840×2160 quando apropriado), e visualizador interativo quando viável.
- **RF-13 — Revisão incremental:** uma alteração de bairro, instituição ou linha modifica somente seus dados proprietários e atualiza automaticamente todas as visualizações afetadas.
- **RF-14 — Auditoria pré-imagem:** é possível listar as decisões geográficas em aberto que bloqueiam uma representação definitiva.

## 6. Critérios de qualidade e aceite

- Toda entidade rotulada como existente em um mapa oficial possui ID e posição rastreáveis.
- Pontes e túneis conectam trechos reais; estações pertencem a linhas; instalações são alcançáveis pelas redes pertinentes, salvo isolamento intencional documentado.
- Não há cortes artificiais em bordas de tiles; os recortes são geometricamente derivados.
- A geração técnica pode ser repetida a partir do mesmo commit e produzir a mesma cartografia lógica.
- Legendas, topônimos, localização e tipologia passam em conferência cruzada.
- A representação arquitetônica é proporcional ao zoom: edifícios ordinários não exigem desenho individual no mapa geral; complexos relevantes exigem pegada espacial identificável.
- O acabamento V5 privilegia a cidade contemporânea decadente — arquitetura histórica, industrial e brutalista, desigualdade, grafismo editorial sóbrio — e evita fantasia medieval, molduras imperiais, rosa dos ventos temática e tipografia ilegível.
- Versão pública não contém informações exclusivas de narrador ou conhecimento não permitido ao leitor.
- Exportação 4K é um **formato final de saída**, não promessa de detalhe nativo do gerador de imagens.

## 7. Processo incremental e entregas

**P0 — Inventário do existente:** mapear fontes/assuntos, fatos, variantes, conflitos, lacunas e grau de autoridade. Nenhum dado candidato vira cânone por extração automática.

**P1 — Decisões fundamentais:** estabelecer quadro espacial, ano/estação do atlas, extensão, população, raions, hidrografia, litoral, condicionantes do Ermo e evolução histórica. Registrar decisões com fonte.

**P2 — Protótipo técnico controlado:** provar com dados sintéticos ou trecho não canônico edição via ChatGPT Web/GitHub, conectividade, validação e exportação. O protótipo não canoniza geografia.

**P3 — Modelo urbano:** definir centros, bairros, densidades e usos do solo; relacionar com história e topografia aprovadas.

**P4 — Infraestrutura:** construir redes contínuas de transporte, aquecimento, energia, água, saneamento e logística.

**P5 — Equipamentos e instituições:** distribuir e cadastrar edifícios e complexos principais; validar capacidade e acessibilidade em termos plausíveis.

**P6 — Carta técnica:** renderizar e auditar mapa completo, simbologia, legendas e recortes a partir do modelo.

**P7 — Atlas artístico:** aplicar tratamento editorial V5 sem deslocar geometrias; gerar variantes públicas e narrativas autorizadas.

Cada fase encerra com uma **entrega utilizável e checklist curto de inconsistências materiais**, não uma coleção de gates burocráticos.

## Decisão canônica posterior — GEO-001.1 (15/11/2026)

O proprietário fixou em **7.000.000 residentes** a população municipal de Novydres no ano de referência 2010, abrangendo os nove raions. O dado autoritativo reside em `../populacao-2010.json`. As afirmações populacionais obsoletas foram retiradas dos arquivos correntes, em cumprimento da política de fonte única. GEO-010 (distribuição) e GEO-002/GEO-004 (extensão e limites) permanecem abertos.

### Decisões posteriores — GEO-002.1 a GEO-002.3 (15/11/2026)

Localização regional e configuração principal continental e costeira, com grande baía natural, rios, lagoas naturais, fontes termais e ilhas apenas secundárias, aprovadas pelo proprietário. A cidade **não** será concebida como ilha ou arquipélago. A geotermia de águas termais é a base principal do aquecimento, mas sua origem geológica, capacidade e rede dependem de GEO-014. **Fonte única vigente:** `../localizacao-geral-2010.json`; formas, posição exata, área, escala e projeção seguem abertas.

### Fechamentos GEO-003.1 e GEO-014.1 (15/11/2026)

A origem geológica profunda da geotermia, sua concentração abundante na Cidade Velha e a distribuição de aquecimento irregular e desigual foram aprovadas. **Única fonte autoritativa:** `../geotermia-aquecimento-2010.json`. A vinculação administrativa da Cidade Velha a Chelsea e a rede detalhada ainda aguardam decisões.

### Fechamento GEO-004.1 (15/11/2026)

O núcleo histórico Cidade Velha (Old Town) pertence ao raion Chelsea, conforme [fonte canônica única](../../geografia/district-chelsea/cidade-velha-2010.json). Esse vínculo não canoniza os perímetros dos bairros, a totalidade das fronteiras nem a cronologia de Pristan Vasilieva.

### Fechamento GEO-004.2 (15/11/2026)

Os nove raions administrativos oficiais foram ratificados. A **fonte única** de seus nomes e existência é [`raions-oficiais-2010.json`](../raions-oficiais-2010.json). Nenhuma macroposição, fronteira, subbairro ou domínio Cainita foi aprovado nesta subdecisão.

### Fechamentos GEO-004.3, GEO-005.1 e GEO-005.2 (15/11/2026)

A posição dos núcleos urbanos e os mapas futuros **devem obedecer** à fonte territorial de Ermos `../ermos-estrutura-territorial-2010.json` e à fonte histórica `../../historia-global/formacao-policentrica-2010.json`. Não aplicar geração radial/contínua nem tratar Ermos como gradientes decorativos de arquitetura; a geometria real de barreiras naturais e travessias condicionará a urbanização. Foi aprovada a estratégia de Gilgamesh de distribuir emissários Cainitas conforme aptidões, geografia e interesses políticos, consolidando senhorios locais subordinados. A única fonte desse fato é `../../historia-global/formacao-policentrica-2010.json`. Nenhum clã ou emissário específico foi atribuído aos nove raions, e nenhum senhorio fundador foi equiparado automaticamente a um raion moderno.

### Fechamento GEO-005.3 — Continuidade dos domínios e evolução territorial (15/11/2026)

Não exigir correspondência 1:1 entre senhorios e raions modernos, porém **não criar alterações de senhor, clã dominante ou extensão de domínios Cainitas apenas para preencher o mapa**. Cada mudança precisa ter causa histórica forte, período, atores, mecanismo e consequências, submetidas à aprovação. Ao construir a geografia de cada núcleo, desenvolver simultaneamente sua história. Fonte única `../../historia-global/formacao-policentrica-2010.json`. A hipótese Ventrue/Chelsea/Bukovie não é canônica.

## 8. Decisões a fechar antes de imagens definitivas

A fase P0 deverá produzir um inventário exaustivo do que já foi decidido, do que permanece aberto e das dependências de cada escolha. Candidatos iniciais a decisão prioritária:

1. Localização fictícia e sistema de referência espacial; extensão e escala plausíveis.
2. População-base e distribuição entre raions (população-base de 7.000.000 em 2010 já canonizada, com distribuição por raion em aberto).
3. Nove raions, fronteiras e relação com bairros e corredores do Ermo.
4. Rio Vasyl/Reka Vasilya, nascentes, cursos, deságue, ilhas, costas, baías e gelo; compatibilidade com esboços anteriores.
5. Marcos cronológicos do crescimento metropolitano, industrialização e infraestrutura térmica.
6. Rede primária de transporte e interfaces de aeroporto, portos e ferrovia.
7. Instituições existentes, hierarquia administrativa e complexos obrigatórios.
8. Critérios para nomes, símbolos, camadas narrativas, confidencialidade, projeção e apresentação editorial.

**Gate de prontidão para a imagem definitiva:** todas as decisões críticas para a área/escala renderizada devem estar aprovadas ou explicitamente classificadas como não bloqueantes; nenhuma contradição crítica deve ser escondida por composição artística. Pré-visualizações técnicas e protótipos não canônicos são permitidos e claramente identificados.

## 9. Riscos e limitações

- **Alucinação visual:** geração de imagens pode inventar edifícios, vias e nomes; mitigar com geometria travada e renderização determinística.
- **Falsa precisão:** geometria inventada ou medidas não calibradas não recebem escala/lat-long oficiais sem justificativa.
- **Escopo excessivo:** um atlas de milhões de habitantes não exige cadastro manual de cada prédio; aplicar detalhe por nível e importância.
- **Conflito de autoridade:** documentos candidatos, cenários e eventos podem divergir; manter proveniência e decisão humana.
- **Segredos:** não hospedar informações restritas em site ou artefato publicamente acessível.
- **Automação incompleta:** conectores, CI e publicação dependem de permissões/configuração; verificar capacidade antes de prometer execução sem intervenção.

## 10. Condição de sucesso

O produto será bem-sucedido quando qualquer distrito puder ser ampliado e revisado sem perder sua relação com a cidade inteira; quando vias, transporte e instituições corresponderem a dados verificáveis; quando a cartografia pública e a narrativa compartilharem a mesma cidade; e quando o projeto puder evoluir por novos prompts, sem reconstrução integral nem canonização silenciosa.

**Estado desta versão:** aprovado pelo proprietário em 14/11/2026 para orientar o planejamento. Nenhum elemento geográfico novo é aprovado por este texto.
