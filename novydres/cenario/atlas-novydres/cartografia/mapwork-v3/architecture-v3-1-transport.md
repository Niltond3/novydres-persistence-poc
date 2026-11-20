# Arquitetura V3.1 — transporte antes dos lotes

**Natureza:** implementação da infraestrutura de planejamento, não da arte de Kingswell.

## Definição de autoridade (decisão do proprietário, 20/11/2026)
**Lote = quadrante/quarteirão delimitado por vias e barreiras físicas**, não lote cadastral individual e **não** uma janela retangular arbitrária de geração.

Um lote pode conter vários edifícios, oficinas, fábrica, pátios, parque ou POI. `work_unit` é apenas uma subdivisão operacional com máscara/bleed para produzir a arte do lote sem destruir a estrutura existente.

### Hierarquia de definição
1. Fonte U02 / redes globais (vias, avenidas, artérias, autoestradas, vias de serviço, viadutos, viários em rampa/trevos, ferrovias de carga/passageiro e ramais, bondes, canais e rios).
2. Nós e conexões da rede: cruzamentos em nível, rotatórias, interseções, mudanças de nível, trevos e interfaces trilho-via; camada física vs topológica separadas.
3. Polígono territorial e classes de uso obrigatoriamente totalizantes (urbano, industrial, natureza, água e protegido); morfologia/ocupação por tipologia e bandas de altura.
4. Delimitação automática de lotes/quadrantes pela **rede ao nível do solo** + água/barreiras + contorno da zona, sem tratar viadutos como cruzamentos no nível da rua.
5. Dentro de cada quadrante, distribuição posterior de construções, pátios e POIs segundo a função da região.
6. Divisão operacional em *work units* com escala, tamanho máximo, máscara de alterações e dependências. **Não** exigir que o proprietário fixe número de lotes antes da rede.
7. Costuras bilaterais/contratos globais, verificação de máscaras e autorização expressa antes da primeira arte, mais comparação ANTES/DEPOIS integral.

### Modos de transporte incorporados
- Viário: `street`, `collector`, `avenue`, `arterial`, `expressway`, `service`, `ramp`.
- Ferroviário: `rail_main`, `rail_freight`, `rail_siding`.
- Bondes: `tram` compartilhado com rua ou em faixa reservada; não divide automaticamente o quadrante.
- Água: `river`, `canal` como barreira.
- Estruturas: nós `intersection`, `roundabout`, `interchange`, `rail_crossing`, `tram_junction`, `terminal`, `portal`; travessias `at_grade` ou `grade_separated`.
- `level` e `level_from/level_to` distinguem cruzamentos reais de viadutos; uma travessia em níveis diferentes não cria interseção ao nível da rua.

### Gates e semântica
- `SCHEMA_VALID`: contratos de entrada sem ambiguidades.
- `TRANSPORT_TOPOLOGY_VALID`: nós, ruas, ferrovias, ramais, bondes, níveis e cruzamentos verificáveis.
- `TERRITORY_CLASSIFIED`: 100% do território atribuído a exatamente uma classe primária.
- `MORPHOLOGY_VALID`: cada classe urbanizável tem regras de intensidade/uso/altura explícitas.
- `LOT_BOUNDARIES_VALID`: lotes derivados da conectividade e das barreiras ao nível do solo.
- `WORK_UNITS_VALID`: todos os pixels editáveis pertencem exatamente a uma tarefa atômica; tarefas respeitam orçamento e escala.
- `PROTECTED_MASKS_VALID`: ruas, trilhos, águas, pontes, margem, Ermos e faixas protegidas não mudam fora de máscara.
- `SEAM_CONTRACTS_VALID`: bordas das zonas assentadas em autoridade global ou verificadas dos dois lados.
- `GENERATION_READY`: TODOS os gates, base real, máscaras reais, planejamento executável e autorização do proprietário; fixture sintética nunca pode liberar geração.
- `RELEASE_VALID`: arte gerada passa pelos testes visuais, técnicos e aprovação do proprietário.

### Implementação
- `scripts/urban_architecture.py`: validador de nós, arestas, travessias/níveis, classificação territorial, morfologia, segmentação de lotes e planejamento de work units.
- `fixtures/topology-v31-synthetic.json`: caso sintético 64×64, duas ruas em cruz, bonde compartilhado e ferrovia elevada separada por nível.
- `tests/test_urban_architecture.py`: integração e testes negativos de cobertura, rede, máscara, orçamento e falsa prontidão.
- A U02 de Kingswell e as 55 decisões permanecem como fonte de fatos. O polígono U02_KW_SKETCH_02 permanece aprovado como esboço **macro**. Os 14 macrolotes V2 são **âncoras antigas não definitivas**, não representam os novos lotes.

**Não afirmar que a zona real está pronta porque a fixture passou.** A transição para execução de Kingswell exige inventário/geometria das vias reais e prova de cobertura da máscara editável da zona.

## Integração com a CI e prova contra falso PASS

O comando existente `mapwork.py audit` agora chama o módulo V3.1, valida um mapa sintético fechado com ruas, trilho elevado e bonde, e mede explicitamente o percentual de **janelas antigas** sobre o polígono real de Kingswell. Este percentual não equivale à taxa edificada: mostra por que os 14 retângulos são inadequados como loteamento. O campo `architecture_v31.real_zone_generation_ready` continua **false** até haver entrada territorial e redes vetorizadas da U02.

A V3.1 produz um programa tipológico para cada quadrante delimitado (ocupação-alvo, uso, faixas de pavimentos e POIs internos), mas não inventa pegadas de edifícios nem demografia sem dados. O campo `generation_ready` exige verificação dos bytes da imagem U02, recebimentos de máscara reproduzíveis, costuras bilaterais verificadas por conteúdo e evidência de autorização do proprietário. Um simples booleano marcado em JSON não libera arte.
