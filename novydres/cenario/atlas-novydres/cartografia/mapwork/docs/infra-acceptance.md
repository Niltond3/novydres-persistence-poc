# Aceite técnico de infraestrutura e urbanização

Fonte vinculante dos 32 critérios por etapa para `scripts/pipeline.py`.
Nenhum PASS textual ou hash isolado demonstra coerência sem inspeção visual real.
Os critérios são cumulativos e exigem PNG integral, rede estruturada,
SHA dos bytes originais, máscara autorizada, topologia bilateral e revisão
visual associada ao hash atual. Falha em qualquer critério exige reparo,
regeneração e nova validação; jamais antecipa a próxima etapa. O controle
de tentativas e suas condições de parada são definidos em `PIPELINE.md`.

## Etapas e critérios auditáveis

### INF-01 — Hierarquia viária completa

- [ ] `INF-01.01` A prévia cobre **toda a área-alvo**, com levantamento de ruas locais, coletoras, avenidas, arteriais e autoestradas existentes/necessárias; vias não foram substituídas por poucas linhas genéricas ou traçadas por cima de edifícios.
- [ ] `INF-01.02` Cada corredor possui geometria compatível com a U02, hierarquia, sentido/função quando pertinente, largura/servidão de passagem em unidades justificadas e pontos de entrada/saída documentados; não inventar escala métrica.
- [ ] `INF-01.03` Cada rua tem continuidade e extremidades coerentes (interseção, cul-de-sac legítimo, divisa ou estrutura), sem junções próximas mas soltas, vias suspensas ou travessias de rios não explicadas.
- [ ] `INF-01.04` A morfologia é orgânica e adequada ao setor: malha histórica, bairros operários, eixos industriais, litoral e relevo; não impor grade arbitrária ou infraestruturas fisicamente improváveis.

### INF-02 — Desníveis, pontes, viadutos e trevos

- [ ] `INF-02.01` **Todos os cruzamentos** têm relação explícita: interseção em nível, passagem superior/inferior, ferrovia em nível devidamente autorizada ou sobreposição sem ligação; o grafo não conecta níveis diferentes automaticamente.
- [ ] `INF-02.02` Viadutos, elevados, rampas, túneis, trevos, acessos e saídas presentes ou necessários estão individualmente localizados e possuem geometria de entrada/saída, continuidade, nível e função operacional coerentes.
- [ ] `INF-02.03` As três pontes históricas KW-B01/B02/B03 são preservadas na posição e função aprovada; qualquer outra travessia existente na U02 é distinguida de uma nova proposta, sem presumir autorização.
- [ ] `INF-02.04` Raio de curva, largura, encosta, água, faixa construída, travessia de pedestres e acessibilidade visual não apresentam conflitos inexequíveis ou ocultos; a revisão visual aponta correções concretas.

### INF-03 — Ferrovias e logística

- [ ] `INF-03.01` O corredor ferroviário pesado ocidental, os terminais existentes de passageiros e cargas e os acessos regionais são preservados, sem deslocamento, estação internacional extra ou descontinuidade na U02.
- [ ] `INF-03.02` A rede ferroviária candidata possui trilhos, curvas, desvios, pátios, bitolas/interfaces quando evidenciadas e logística de carga plausíveis; terminais têm acesso operacional ferroviário e rodoviário.
- [ ] `INF-03.03` Cada encontro com via, água e outra ferrovia possui topologia e nível explícitos, com viaduto, passagem ou cruzamento real; não confundir proximidade geométrica com conexão.
- [ ] `INF-03.04` Todo elemento ferroviário novo exige autorização editorial; na falta dela, a solução usa infraestrutura existente ou registra impedimento, nunca cria canonicidade silenciosa.

### INF-04 — Bondes e mobilidade de superfície

- [ ] `INF-04.01` Para cada via candidata que receberá bonde, justificar largura/compartilhamento, função, continuidade, paradas e acesso de embarque; vias inadequadas são explicitamente excluídas.
- [ ] `INF-04.02` Traçados de bonde têm conexão operacional (incluindo retornos/terminais quando cabíveis), curvas e interface com veículos/pedestres, sem trilhos que parem em edificações ou sumam da malha.
- [ ] `INF-04.03` Cruzamentos de bondes com via/ferrovia/água identificam nível, preferência/compartilhamento e proteção, mantendo todos os eixos aprovados.
- [ ] `INF-04.04` O agente valida na prévia todas as escolhas de bonde, comparando capacidade e espaço da rua com a morfologia local antes de aceitar.

### INF-05 — Metrô e infraestruturas subterrâneas

- [ ] `INF-05.01` Respeitar KW-PROP-006 opção A em Kingswell: metrô atravessa expansão operária **sem cortar o microcentro termal KW-HIST**; não presumir união dos dois componentes de máscara por túnel inventado.
- [ ] `INF-05.02` Qualquer trajeto, estação, portal, profundidade, ventilação e interface com ferrovia/viário possui autoridade específica; quando dependente de aprovação ainda ausente, marcar bloqueio editorial em vez de inventar.
- [ ] `INF-05.03` A rede subterrânea não corta quadras de superfície, não interfere em pilares/canais e tem transições físicas coerentes com os níveis de vias, túneis, aquecimento e geotermia.
- [ ] `INF-05.04` O agente confere sobreposição macro e recortes críticos, preservando o núcleo termal e a ligação com raions vizinhos sem conexões fictícias.

### INF-06 — Integração global da rede

- [ ] `INF-06.01` Uma única autoridade topológica combina rodovias, ruas, viadutos, pontes, ferrovias, bondes, metrô, hidrografia e seus níveis; cada junção tem responsáveis e não há duas redes paralelas contraditórias.
- [ ] `INF-06.02` Todos os conectores de Sulfok, Drevnigrad e demais vizinhos relevantes são conferidos **bilateralmente**, incluindo direção, largura, nível, identificação e continuidade; falta de contraparte não é falsificada como conexão aprovada.
- [ ] `INF-06.03` A auditoria automática detecta pontas soltas, saltos, sobreposições proibidas, cruzamentos não tipados, isolamento indevido e continuidade de água/terreno; não há conflitos desconhecidos aceitos.
- [ ] `INF-06.04` O agente inspeciona a **prévia integral e os recortes críticos** comparando todos os modais à U02, redes vizinhas, relevo, vias de carga e acessos de emergência; cada falha produz correção rastreável.

### INF-07 — Classificação territorial e proteção

- [ ] `INF-07.01` **100% dos pixels do polígono candidato** têm exatamente uma classe primária — urbano, industrial, natural, água ou protegido — sem sobreposição nem áreas restantes.
- [ ] `INF-07.02` Margens, rio, encostas, Ermos, solo edificável, faixa operacional de trem e hierarquia de circulação coincidem com a U02 e com os vetores já aprovados.
- [ ] `INF-07.03` Áreas protegidas, servidões, redes e estruturas existentes são descontadas de qualquer máscara futura de geração; fora de máscaras autorizadas os pixels não mudam.
- [ ] `INF-07.04` Só depois do PASS de INF-01 a INF-07 o agente pode iniciar quadras e lotes derivados das vias reais; não utilizar janelas retangulares artificiais como quarteirões.

### URB-08 — Quadras, edifícios e POIs, após infraestrutura

- [ ] `URB-08.01` Quarteirões são componentes fechados por ruas, rios e barreiras reais; work units são subdivisões técnicas, não lotes ou edifícios.
- [ ] `URB-08.02` As edificações têm limites individuais, ocupação e circulação plausíveis; acesso de pedestre/serviço/frete validado no solo sem atravessar água, ferrovia ou vizinhos.
- [ ] `URB-08.03` Os cinco POIs existentes de Kingswell ocupam áreas acessíveis e auditadas, sem mover ou inventar marcos sem autorização; nenhum POI cobre faixa operacional.
- [ ] `URB-08.04` A cobertura útil por unidades é integral e sem duplicatas; aprovações da infraestrutura e do raster permanecem vinculadas aos mesmos SHA-256.


## Perfil executável dos dados espaciais (vinculante)

O agente continua seguindo os 32 critérios acima. A estrutura mínima de dados
abaixo torna **matematicamente verificáveis** seus requisitos de modal e
cobertura, sem substituir a inspeção semântica. Cada rodada precisa do mesmo
modelo cumulativo, dos pixels reais da máscara de zona e de geometria
individual de nós, arestas, cruzamentos e níveis; até existir modelo suficiente,
FAIL. A aprovação da etapa anterior vincula a geometria por SHA-256. Alteração
de rede já aprovada exige reabrir/revalidar as etapas dependentes.

```json
{
  "schema":"NOVYDRES_MAPWORK_SPATIAL_PROFILE",
  "stage_modes":{
    "INF-01":["road"],
    "INF-02":["road"],
    "INF-03":["road","rail"],
    "INF-04":["road","rail","tram"],
    "INF-05":["road","rail","tram","metro"],
    "INF-06":["road","rail","tram","metro"],
    "INF-07":["road","rail","tram","metro"],
    "URB-08":["road","rail","tram","metro"]
  },
  "coverage_stages":["INF-07","URB-08"],
  "territory_classes":["urban","industrial","natural","water","protected"]
}
```

As máscaras referenciadas pela geometria são PNGs binários exatamente nas
mesmas dimensões da U02, vinculadas a SHA-256. A geometria tem schema
`NOVYDRES_MAPWORK_INFRA_GEOMETRY`, `zone_mask`, `network.nodes`,
`network.edges`, `network.crossings`, `reference_size`, `source_sha256` e
`previous_stage_sha256` (exceto INF-01). A revisão visual exige observações
regionais com hashes calculados sobre os pixels dos recortes da prévia.
Essas provas atestam consistência de bytes e cobertura de inspeção, **não** que
o modelo humano/LLM avaliou corretamente a estética ou o planejamento urbano.
