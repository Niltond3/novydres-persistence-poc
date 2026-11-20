# Revisão de arquitetura Mapwork V3 — 2026-11-20

**Status: AUDIT_RECORDED / ARCHITECTURE_REVISION_PROPOSED (não aprovada nem implementada).**
**Origem da crítica do proprietário:** o esboço visual aprovado de Kingswell não corresponde ao parcelamento completo da zona; a sequência deveria preservar a arquitetura acordada em vez de redefinir a geração a cada entrega.
**Escopo:** Mapwork V3 e Kingswell; **nenhuma alteração** da U02, do esboço U02_KW_SKETCH_02, das 55 aprovações, dos pixels, de master ou de world-state. O documento distingue constatação de proposta.

## Diagnóstico verificável

1. **Arquitetura original era um piloto, não a implementação completa.** `README.md` chama V3 de “piloto de infraestrutura” e diz expressamente que prova um mecanismo com *fixtures sintéticas*, não a geração real de Cidade Velha. O código atual executa auditoria, validação de ativos e composição de mosaicos, mas não oferece um planejador completo de ocupação/densidade nem uma decomposição urbana integral automática. Ao afirmar que a arquitetura garantia a geração da zona, foi sobrestimada a maturidade do produto.
2. **Descumprimento da ordem documentada.** `AGENT.md` item 5 e `templates/esboco.md` exigem mapa técnico integral com bairros, **quadras, lotes e densidades** antes da fila. O esboço efetivamente aprovado U02_KW_SKETCH_02 continha setores morfológicos, POIs, pontes e borda; não continha parcelação integral de quarteirões/edifícios nem densidades mensuráveis. O aceite visual do usuário é legítimo, mas foi promovido a `SKETCH_APPROVED` sem distinguir o nível macro do contrato de detalhe. O usuário não autorizou deduzir geração pronta.
3. **Nomenclatura e responsabilidade confundidas.** Os 14 itens `KW-L01..14` em `lotes-conectores-v2.json` são **retângulos de janelas de produção / âncoras**, não lotes cadastrais, quadras reais, cobertura por tipologia nem malha de ativos urbanos. A soma dos cores é 44.498 unidades² U02 para polígono candidato de 272.635 unidades²; **16,32% de cobertura geométrica bruta**, que inclui espaços não edificáveis e portanto não é taxa de tecido construído. 83,68% não têm macrolote atribuído. Dividir somente esses 14 retângulos em tarefas menores **não** cobre a zona.
4. **Gates incompletos.** A CI validou existência, IDs, coordenadas, cores sem sobreposição, itens pendentes, posições de POIs e testes sintéticos; não exige cobertura de classificação do território, cobertura de toda área elegível à geração, contiguidade real da rede de quadras, coerência semântica de densidade/uso, ou capacidade operacional de produzir centenas/milhares de assets. Logo, `38 passed` não é prova de adequação para produzir a cidade.
5. **Representação técnica desalinhada.** `zone.schema.json` usa `bounds` e cores retangulares, sem uma camada autoritativa de polígonos de ocupação, tipologias de quadra e máscara de restrições territoriais. Pontes, trilhos e água precisam de autoridade global própria, não apenas conectores por retângulo. O compositor faz fallback à U02 interpolada onde não houver novos ativos; portanto um mosaico pode ser tecnicamente válido e visualmente incompleto.
6. **Capacidade / escala não dimensionada por orçamento.** Escala 64 px detalhados por unidade U02 e tiles 512 px estão definidos, mas não há estimador obrigatório de volume de geração, unidades de trabalho e qualidade por grupo antes de iniciar. Não é aceitável fixar 14 ou 225 como número final sem derivar do plano territorial.

## Decisão de engenharia proposta (não automática)

**Preservar a ideia central** — referência U02 imutável, fontes e conectores globais, geração incremental por unidades mascaradas, armazenamento por SHA/ID, comparador integral, aprovação humana — **e completar a arquitetura faltante**, antes de gerar outra malha ad hoc.

### Camadas de autoridade (separadas)

A. `source_registry`: SHA U02, orientação, escala, releases e fontes aprovadas.
B. `global_network`: segmentos hidráulicos, ruas, pontes, trilhos, margens e contratos de borda com IDs persistentes, independentes dos lotes de arte.
C. `zone_territory`: **polígono real da zona**, classes territoriais mutuamente exclusivas (solo urbano, indústria, infraestrutura, água, Ermo, relevo/protegido, etc.), máscaras de editabilidade, e subáreas de morfologia. Diferenciar **classificação de 100% da área** de **geração de 100% da área edificável/alterável**.
D. `urban_morphology`: regras de quadra e parcela derivadas de ruas, usos, faixas de altura, intensidade de ocupação, vazios funcionais, tipologia histórica/operária/industrial, acessos, sítios especiais; regras verificáveis por setor. Densidade não equivale automaticamente a população absoluta (não há metro/pixel aprovado).
E. `work_unit_planner`: **gera automaticamente** tarefas/artifacts pela interseção entre geometria de ocupação, redes protegidas, unidades de processamento e catálogo de tipologias; limites de tamanho, bleed, dependências e orçamento. Não pede ao proprietário desenhar manualmente cada parcela ou escolher o número de lotes.
F. `render_and_quality`: assets gerados por lote/edifício especial, máscara derivada de geometria, costura, comparação integral, regressão topológica e aceite real.
G. `release_registry`: manifests, SHA, recibos Drive, readback, release aprovado e read-only do histórico.

### Estados/gates propostos

- `SKETCH_MACRO_APPROVED`: registra **exatamente** o aceite já dado para U02_KW_SKETCH_02. Não revoga aprovação e não declara parcelação concluída.
- `TERRITORY_CLASSIFIED`: união das classes = **100% do polígono da zona**, sem lacuna nem sobreposição de classe primária; água/Ermos/protegidos são classificados, **não** edificados.
- `MORPHOLOGY_READY`: setores têm regras urbanas e redes estruturantes derivadas da U02; blocos/parcelas podem ser programaticamente gerados; POIs preservados; controles de intensidade/área e seus limites não arbitrários.
- `WORK_UNITS_READY`: máscara elegível de produção = união exata das tarefas autorizadas, sem sobreposição de cores, sem tarefa sobre redes protegidas, com bleed controlado. A contagem é **resultado**, não entrada fixa.
- `CONNECTORS_READY`: redes globais e contratos de borda compatíveis com U02 e vizinhos; permitir primeira zona usando contrato global aprovado (não exigir que zona vizinha tenha arte concluída).
- `GENERATION_READY`: só após todos os gates anteriores, estimativa de volume/recurso, arquivo de filas reproduzível, testes reais, e autorização separada para iniciar arte.
- `IMAGE_REVIEW` / `PUBLISHED`: comparar mapa completo ANTES/DEPOIS, inspeção local e readback, aprovação humana da composição; nunca canonizar implicitamente.

### Critérios obrigatórios de teste, a implementar

- Teste sintético **e** integração com a zona real: a área classificada union corresponde ao polígono, sem gaps/overlaps e com tolerância explicitada.
- Conjuntos de `keep_base`, `generate`, `protected`, `outside_zone` são totalizantes, mutuamente consistentes, com semântica de edição; somente `generate` exige ativos detalhados.
- 100% da máscara `generate` atribuída às tarefas atômicas e um único core por pixel elegível; pixels fora da máscara não podem mudar.
- Geometria de redes reservadas/POIs e limites globais não pode ser sobrescrita; trincas/buracos entre tarefas e conectores cruzados são falhas bloqueantes.
- Limites de dimensão máximos e número/custo estimado de unidades; geração em lotes progressivos sem consumir todos os recursos de uma vez.
- Relatório de intensidade/densidade por setor baseado em forma urbana e tipologia, não em população extrapolada sem métrica.
- CI `PASS` deve discriminar `SCHEMA_VALID`, `COVERAGE_VALID`, `CONNECTORS_VALID`, `GENERATION_READY` e `VISUAL_QA`; nenhuma aprovação parcial pode ser apresentada como aceite do resultado completo.

## Plano de correção (sem avançar cartografia enquanto contrato não estiver implementado)

1. **ADR e esquemas:** versionar proposta de arquitetura V3.1, migrar estado `SKETCH_APPROVED` para substatus de aprovação macro preservando evidência, separar `macro_windows` de `work_units` e `urban_parcels`.
2. **Gates testáveis:** implementar classificações, cobertura, máscaras, redes e planejamento automático, com testes negativos contra o caso real Kingswell de 16,32% de macrolotes (o gate de cobertura deve reprovar a falsa completude).
3. **Validação ponta a ponta mínima:** executar uma zona sintética integral e um recorte de Kingswell como *prova de integração* (não imagem artística final), verificando o limite de recursos, costura e a passagem de estados.
4. **Só então** aplicar o planejador integral a Kingswell. A aprovação anterior do esboço continua válida para identidade e morfologia; não obrigar o proprietário a repetir as 55 respostas nem aprovar coordenadas técnicas isoladas.
5. Publicar novos checkpoints na branch candidata com CAS/readback; jamais alterar master, imagem U02 ou world-state aprovado sem gate próprio.

**Veredito:** falha **mista**, mas primariamente de implementação e governança da execução. A arquitetura conceitual estava correta na direção, porém incompleta em contratos e testes, e a implementação violou o seu próprio item 5. Não há evidência para afirmar que os 14 macrolotes constituam o loteamento integral da zona.
