---
document_id: MW-009-FIS01-REVISAO-COSTEIRA-2010
subject_id: world-atlas-novydres
reference_year: 2010
workflow_status: REFINEMENT_MW010_PUBLISHED_PENDING_OWNER_DECISION
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED_PROPOSAL_NOT_CONFIRMED
work_unit_status: OPEN
handoff_to_next_point: BLOCKED_UNTIL_POINT_CLOSED
owner_decision_on: 2026-11-16
owner_decision_keys: FIS-01-DECISION-1,FIS-01-DECISION-2
owner_decision: PRESERVE_SHELTERED_BAY_REFINE_CONTOURS_AND_KEEP_THREE_ISLANDS_ONLY_AS_REVISABLE_HYPOTHESIS
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
source_mw008_commit: cf75cf87b4ffc2ea24edaa3e3c3ce35ff3607d39
---

# MW-009 — Revisão substantiva costeira, decisões 1 e 2

## Decisão 1 — Baía protegida e refinamento do contorno

### Deliberação expressa do proprietário

**“FIS-01, decisão 1: mantenha a configuração da grande baía protegida, mas refine seus contornos antes de pedir aprovação geométrica.”**

**Interpretação estrita:**
1. **Preservar:** litoral predominantemente continental, costa externa exposta, grande baía natural protegida por promontório e ligação navegável ao mar; organização relativa já aceita em MW-007.
2. **Exigir revisão:** o traçado exato da costa, as concavidades, as projeções do promontório e o limiar cartográfico da boca **não estão aprovados**; antes de pedir opção G/aprovação geométrica, apresentar nova variante de contorno e sua justificativa físico-espacial.
3. **Não interpretar como autorização:** canonizar a configuração métrica atual (inclusive área sintética da baía ~1.851,25 km² e abertura ~18,4 km), aprovar número/posições/perímetros das ilhas, ancorar EPSG, decidir portos, vias, raions, limites municipais ou obra de engenharia.
4. **Padrão visual aprovado e obrigatório na revisão:** HTML/SVG 2D grafite/azul dessaturado e texturas discretas conforme `visualizacao-fisica-interativa-2010.md`; a representação é derivada da geometria estruturada.

**Situação do trabalho:** diretriz de revisão aprovada; **a geometria refinada ainda precisa ser produzida, confrontada com dependências e novamente submetida à avaliação**. Nenhuma alteração de pontos foi efetuada apenas por este registro.

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

**Pendência A da unidade atual (MW-009):** produzir a variante costeira refinada e inspecionável no padrão HTML/SVG 2D aprovado, reconciliar dependências físicas, executar validação pertinente e submetê-la ao proprietário. **Não há decisão adicional de contorno ou quantidade insular a exigir antes do refinamento.**

## Gate de fechamento da unidade MW-009

**MW-009 permanece ABERTA:** a aceitação da organização costeira e a hipótese das ilhas são decisões intermediárias, não encerramento do ponto FIS-01.

Conforme a regra agora registrada em `guide.md`, **não gerar handoff nem prompt MW-010** antes de: (1) produzir variante de contorno refinada e versão atualizada do visualizador 2D; (2) verificar impactos com Rio Vasyl, microbacias, relevo, Ermos e ilhas provisórias; (3) submeter a versão consolidada ao proprietário e registrar seu aceite/rejeição/ressalvas; (4) corrigir problemas materiais, concluir as validações pertinentes e verificar o commit remoto. A rejeição de uma variante exige corrigir ou encerrar expressamente a opção descartada; não autoriza inferir a aprovação de outra.

O handoff e prompt MW-010 anteriormente emitidos após a mera decisão sobre as ilhas foram **prematuros e estão revogados como autorização de avanço**. Em caso de limite de contexto, fazer somente checkpoint/nota de retomada da **mesma MW-009**, sem declarar fechamento.

## Escopo, validação e continuidade

**Este registro documental das decisões 1 e 2 não modifica** `master`, JSONs físicos, validação MW-006, visualizador 2D, raions, transportes, personagens ou crônica. As alternativas e premissas que ainda carecem de aprovação permanecem propostas. Quando houver fechamento integral e somente então for permitido um handoff, ele deverá apontar para este arquivo no GitHub, nunca usar o texto do prompt como fonte de autoridade.

**A/B/C:** A = produzir variante de costa topologicamente verificável para futura aprovação; B = registrar efeito sobre foz, lagoa, Ermos litorâneos e navegabilidade sem projetar infraestrutura; C = redes/portos/raions e narrativa, fora desta revisão.

## Anotação MW-010 — pendência de aceite

Variante costeira estruturada refinada e comparador publicados na branch `mapwork/mw-010-refinamento-costeiro-fis01`, sem canonização. A decisão expressa sobre o contorno revisado segue pendente. O ponto FIS-01 continua aberto; handoff proibido até o gate de fechamento do `guide.md`.
