---
document_id: MW-009-FIS01-REVISAO-COSTEIRA-2010
subject_id: world-atlas-novydres
reference_year: 2010
workflow_status: CLOSED_FOR_THIS_SCOPE_SCOPED_OWNER_APPROVAL_NONCANONICAL
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED_PROPOSAL_NOT_CONFIRMED
work_unit_status: CLOSED_FOR_THIS_SCOPE
handoff_to_next_point: ELIGIBLE_AFTER_REMOTE_CLOSE_BUT_NO_REPLAY_OF_EXISTING_MW010
owner_decision_on: 2026-11-16
owner_decision_keys: FIS-01-DECISION-1,FIS-01-DECISION-2,FIS-01-DECISION-3
owner_decision: PRESERVE_SHELTERED_BAY_REFINE_CONTOURS_AND_KEEP_THREE_ISLANDS_ONLY_AS_REVISABLE_HYPOTHESIS
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
source_mw008_commit: cf75cf87b4ffc2ea24edaa3e3c3ce35ff3607d39
owner_final_approval_date: 2026-11-17
owner_final_approval_scope: MW009_REFINED_COAST_BAY_ONLY_NOT_LATER_MW010_BASELINE
later_baseline_ref: mapwork/mw-010-refinamento-costeiro-fis01
later_baseline_coast_blob_sha: d72cf3eb2b3fac9473017a6bbfdc46ea1efb8577
---

# MW-009 — Revisão substantiva costeira, decisões 1, 2 e 3

## Decisão 1 — Baía protegida e refinamento do contorno

### Deliberação expressa do proprietário

**“FIS-01, decisão 1: mantenha a configuração da grande baía protegida, mas refine seus contornos antes de pedir aprovação geométrica.”**

**Interpretação estrita:**
1. **Preservar:** litoral predominantemente continental, costa externa exposta, grande baía natural protegida por promontório e ligação navegável ao mar; organização relativa já aceita em MW-007.
2. **Exigir revisão:** o traçado exato da costa, as concavidades, as projeções do promontório e o limiar cartográfico da boca **não estão aprovados**; antes de pedir opção G/aprovação geométrica, apresentar nova variante de contorno e sua justificativa físico-espacial.
3. **Não interpretar como autorização:** canonizar a configuração métrica atual (inclusive área sintética da baía ~1.851,25 km² e abertura ~18,4 km), aprovar número/posições/perímetros das ilhas, ancorar EPSG, decidir portos, vias, raions, limites municipais ou obra de engenharia.
4. **Padrão visual aprovado e obrigatório na revisão:** HTML/SVG 2D grafite/azul dessaturado e texturas discretas conforme `visualizacao-fisica-interativa-2010.md`; a representação é derivada da geometria estruturada.

**Situação do trabalho:** a diretriz foi aplicada em MW-009; a **geometria candidata refinada foi gerada e apresentada em comparação integral 2D**, permanecendo sujeita à avaliação expressa do proprietário. Os pontos antigos de ancoragem, incluindo desembocaduras, foram preservados.

## Fontes verificadas e relações de dependência

- `macrogeometria-litoral-baia-ilhas-2010.proposal.json` — costa candidata e ilhas: blob `0aefaa2161aa9b728fd03a4ec3d0daf522a81b4d` no checkpoint MW-008. A baía é derivada da sequência única de costa; limiar definido pelos índices 5 e 19 da costa candidata, sem ponte.
- `macrohidrografia-2010.proposal.json` — blob `34918d5707abac23534df877a8c4b0ec4cefc834`. A foz do Vasyl candidato coincide com vértice costeiro 12. Mover/inserir pontos costeiros exige remapear o índice da foz, revalidar conexão entre linha fluvial e costa e revisar lagoa/canal mareal e demais descargas.
- `macrorelevo-2010.proposal.json` — blob `c5f6caaddfbef3a89fd5ce85a291ae972e9f35ab`. Revisar interseções entre terreno rochoso, baixada/tundra e costa após qualquer alteração.
- `macroermos-2010.proposal.json` — blob `2865c843b292c9d128bb2e957634de09c4e4b70a`. Revisar polígonos de litoral externo, Ermos úmidos e eventuais interseções com água.
- `validacao-integrada-fisica-2010.md` — `PASS_WITH_LIMITATIONS` apenas na geometria **anterior**; não transferir esse resultado para a geometria refinada sem executar novamente verificações pertinentes.
- Cânone de master: `localizacao-geral-2010.json` e `implantacao-litoral-baia-2010.json`. Port Clarence é referência geográfica macrorregional, não contorno copiado nem autorização de deslocar comunidades reais.

## Critérios de desenho e aceite da futura variante

1. Manter grande baía naturalmente abrigada por cabo, faixa continental dominante e conexão com mar externo; evitar morfologia de arquipélago dominante.
2. Refinar linhas com qualidade visual legível em escala metropolitana **sem simular precisão de levantamento geodésico**. Não gerar milhares de vértices arbitrários ou detalhes não sustentados por relevo, estuários e dinâmica de costa.
3. Preservar ou reconectar explicitamente a hidrografia aprovada qualitativamente (Vasyl deságua na baía, atravessa vale termal; outras microbacias permanecem distintas). Se o ponto de foz mudar, ajustar referências e validar os dependentes em uma proposta conjunta.
4. **Conforme decisão 2**, manter duas ilhas internas e uma externa apenas como **hipótese operacional**, sujeita a mudança de número, áreas, posições e perímetros. Não inferir decisão sobre ocupação insular ou pontos de navegação.
5. Comparar variante e proposta original no **único visualizador 2D de revisão**, com diferença distinguível e sem introduzir fonte de geometria paralela.
6. Verificar anéis, interseções, posição terra/água, conexões de drenagem, relação com relevo e Ermos; documentação reproduzível, com limitações.
7. Solicitar nova decisão substantiva **somente após** apresentar variante refinada e impactos, sem converter `NOT_APPROVED` em `CLOSED_CANON`.

## Decisão 2 — Hipótese revisável das ilhas secundárias

O proprietário declarou: **“FIS-01, decisão 2: mantenha três ilhas como hipótese, duas internas e uma externa, sem fixar número ou contornos.”**

**Interpretação estrita:** conservar, no conjunto de trabalho, as duas ilhas internas e uma externa já presentes no JSON candidato, **sem converter esse inventário em quantidade canônica, sem aprovar posições nem limites e sem pressupor sua ocupação**. O desenho pode ser reduzido, ampliado ou redistribuído caso a análise geomorfológica, costeira ou de navegação futura evidencie necessidade; qualquer versão definitiva exigirá decisão expressa posterior. Não existem novos nomes, portos, instalações, áreas territoriais ou infraestrutura associados às ilhas por essa escolha.

**Consequência funcional:** a análise costeira deve preservar a possibilidade de águas protegidas e circulação na baía sem atribuir às ilhas papel obrigatório de barreira, porto, travessia ou polo urbano. Validar que ilhas continuem sobre água e separadas do continente na futura geometria; não tomar o esquema atual como prova geográfica física exata.

**Pendência A da unidade atual (MW-009):** obter decisão expressa do proprietário sobre a versão refinada já apresentada (aprovar, rejeitar ou aprovar com ressalvas); somente depois tratar ajustes e validação de fechamento conforme o guia. **Não há decisão adicional de contorno ou quantidade insular a exigir antes do refinamento.**

## Proposta refinada submetida à avaliação

Foi preparado o arquivo **único** de revisão `visualizador-fisico-2010.html`, mostrando **ANTES** (MW-002) e **DEPOIS** (MW-009) lado a lado, em duas folhas integrais de 120 × 100 km, sincronizadas para zoom e pan, com relevo, hidrografia, ilhas, bacias e Ermos. A camada antiga aparece também como tracejado opcional no mapa novo. A imagem é derivada de geometrias propostas estruturadas, não decide fatos por si.

A geometria foi atualizada **no mesmo** `macrogeometria-litoral-baia-ilhas-2010.proposal.json`; a versão anterior permanece auditável em Git. O litoral preserva os **26 vértices originais** (inclusive desembocaduras e boca da baía) e intercala **75 vértices sintéticos**, totalizando **101 vértices**. Os segmentos costeiros foram suavizados com desvios locais limitados a aproximadamente **0,82 km** da costa anterior, com incrementos de desenho de 100 m (não precisão cartográfica real). A pequena erosão/ondulação foi limitada para que as bacias candidatas permaneçam em terra.

Área sintética da baía: **1.851,25 → 1.845,255 km²** (−0,32%), **sem alterar a largura da boca**. Comprimento sintético da costa na folha: **248,677 → 250,034 km**. Não inferir domínio territorial, dimensão municipal ou navegação sazonal desses números. As **duas ilhas internas e a externa** mantêm os mesmos polígonos como hipótese (não aprovação de quantidade). O Rio Vasyl continua alcançando exatamente o ponto original de sua foz; quatro outros alvos litorâneos incluem a saída de lagoa, sem deriva.

As camadas FIS-02, FIS-03 e FIS-04 **não mudaram seus pontos**. Foram reconciliados apenas SHA de dependência e referências de índices litorâneos: costa→relevo→hidrografia→Ermos. A validação local via Shapely confirmou costa/baía simples, ilhas no mar, 7 polígonos de relevo, 5 bacias, 3 corpos d'água e 10 polígonos de Ermos em terra, 9 cursos e 5 desembocaduras conectadas. O HTML passou em Chromium headless desktop/mobile sem exceções JS, com 41 feições selecionáveis por mapa, alternância de camadas e zoom sincronizado. **Não equivale à execução comprovada dos validadores Node MW-002..MW-006; sem MDE, datum, EPSG, dados de gelo ou limites municipais.**

**Gate final nesta variante MW-009:** aceite geométrico expresso registrado em 17/11/2026, sem ressalvas ao contorno apresentado; **a geometria ainda é não canônica**. A aprovação pertence exclusivamente a esta revisão e não suplanta a variante posterior da MW-010. Qualquer promoção à base corrente requer reconciliação explícita com a cadeia MW-010–MW-014.

## Decisão 3 — Aceite expresso da variante refinada (17/11/2026)

Após receber o comparativo integral 2D MW-009 com as duas folhas completas, o proprietário declarou: **“Aprovo; o esquema de cores está bem melhor também.”**

**Efeito exato desta escolha:** `APROVADO` para o traçado continental de 101 vértices e a baía derivada nesta versão, sem ressalvas ao contorno. O comentário sobre as cores **reafirma** o padrão visual 2D grafite e azul dessaturado já aprovado, sem implicar alterações em geometria, altitude, raions ou infraestrutura. Ilhas continuam hipótese revisável (duas internas, uma externa) e **NÃO** tiveram seus polígonos/quantidade canonizados ou aprovados.

O `macrogeometria-litoral-baia-ilhas-2010.proposal.json` recebe seleção **escopada** `APPROVED_PENDING_PROPAGATION` para `coast-mainland-001` e `water-bay-main-001`; seu estado agregado permanece `NOT_APPROVED` porque inclui ilhas não aprovadas. Nenhum `CLOSED_CANON` é acionado.

**Divergência com trabalhos posteriores, identificada na verificação remota:** a branch `mapwork/mw-010-refinamento-costeiro-fis01`, commit `2a3932a015c8458226410ebfcd67d399b0a33e10`, e unidades MW-011–MW-014, utilizam outra costa de **44 vértices**, blob `d72cf3eb2b3fac9473017a6bbfdc46ea1efb8577`, já aprovada em 16/11/2026. A decisão atual **não altera nem revoga** essa variante anterior para a cadeia corrente; se ambas forem candidatas a base corrente, isso é um assunto substantivo novo que exige reconciliação explícita. Não emitir handoff fictício para MW-010, pois já existe e está fechada.

## Gate de fechamento da unidade MW-009

**MW-009 está FECHADA SOMENTE NESTE ESCOPO:** decisões 1/2 preservadas; decisão 3 aceita para a variante 101-vértices; arquivo estruturado, visualizador, inspeção visual e verificação geométrica sintética disponíveis. O fechamento é documental/cartográfico da revisão isolada, não canonização nem escolha automática da base usada nas unidades posteriores.

O gate do `guide.md` foi percorrido para **esta variante**, com decisão expressa, artefatos derivados e validação geométrica independente de candidatos. Verificações V8 da versão refinada: **0 erros** em contorno auto-intersectante, anéis de baía/terra/mar, 25 polígonos sobre terra, 33 segmentos fluviais, 100 segmentos costeiros, cinco desembocaduras, 10 inventários fluviais de Ermos, três eixos de cristas, relacionamentos de IDs, SHA de dependências e identidade dos 101 vértices do HTML. Resultado **PASS_WITH_LIMITATIONS**. Validação anterior Shapely e testes Chromium de zoom/camadas antes/depois também passaram. **Os validadores Node originais não foram executados nesta rodada**; sem altimetria, datum, coordenadas geodésicas, sazonalidade e limites municipais. Este estado não promove o fechamento de consumidores geográficos posteriores.

O handoff antigo emitido antes do aceite final foi prematuro e não constitui autoridade. **MW-010 já existe e foi fechada com outra variante de contorno (44 vértices), aprovada pelo proprietário em 16/11/2026; MW-011 a MW-014 a preservam**. Este registro posterior de aceite de MW-009 **não altera nem substitui** esses trabalhos. Se a intenção for adotar a variante MW-009 de 101 vértices como base atual, abrir uma unidade separada de **reconciliação explícita**, nunca reexecutar MW-010 ou transportar silenciosamente esta geometria.

## Escopo, validação e continuidade

**Este fechamento modifica apenas a branch MW-009**: registra aprovação parcial da costa/baía nos dados estruturados, atualiza referências SHA nas demais camadas sem alterar seus pontos, reforça o validador do estado parcial e atualiza o HTML 2D. **Não modifica** `master`, branch MW-010 ou posteriores, status das ilhas, geometrias não costeiras, validade de MW-006, raions, transportes, personagens ou crônica. O handoff, se necessário, deve apontar para os arquivos no GitHub, sem transportar geografia por prompt.

**A/B/C:** A = produzir variante de costa topologicamente verificável para futura aprovação; B = registrar efeito sobre foz, lagoa, Ermos litorâneos e navegabilidade sem projetar infraestrutura; C = redes/portos/raions e narrativa, fora desta revisão.
