# Implementação da correção arquitetural V3.1 — fechamento técnico

**Data:** 20/11/2026  
**Escopo:** contrato, implementação e testes do motor de planejamento urbano Mapwork V3.1  
**Status:** IMPLEMENTADO / VALIDADO EM FIXTURE + REGRESSÃO DA ZONA REAL. **Não implica geração de Kingswell pronta**.

## Regra inequívoca do proprietário

**O lote é o quarteirão/quadrante delimitado pela infraestrutura de transporte ao nível do solo e pelas barreiras físicas relevantes.** Dentro dele fica o conteúdo: prédios, oficinas, fábricas, pátios e POIs. Uma `work_unit` é unidade interna de processamento de imagem; não é lote urbano.

A divisão da cidade decorre da geometria de ruas, avenidas, arteriais, vias expressas, trevos, viadutos, interseções, ferrovias, bondes, rios, canais e zonas protegidas. Um viaduto elevado não cria uma interseção falsa no solo.

## Entregas implementadas

| Bloco | Componente | Prova / condição |
|---|---|---|
| Redes globais e transporte | `scripts/urban_architecture.py` | Nós/arestas, classes de via, linha férrea, bonde, níveis, viadutos, trevos, rotatórias, rampas, interseções, crossings separados por nível |
| Contrato formal | `schemas/urban_architecture_v31.schema.json` | Entradas tipadas e validadas; sem depender de inferência do chat |
| Território | `classify_territory` | 100% do polígono classificado; classes exclusivas, com furos para corpos d'água |
| Morfologia | `_morphology_rules` e `block_programs` | Tipologia, mistura de usos, faixa de pavimentos e alvo relativo de ocupação por quadrante |
| Lotes/quadras | `_label_blocks` | Componentes conectados por rua/barreira, não 14 retângulos escolhidos arbitrariamente |
| Work units | `derive_work_units` | 100% dos pixels editáveis associados exatamente uma vez; controle de escala e tamanho |
| Fila incremental | `generation_queue` | Batches determinísticos, sem perder/duplicar work units; estado PENDING_UNAUTHORIZED |
| Segurança e costuras | `plan_city`, `verify_no_protected_edits` | SHA real da U02, fingerprints de máscaras, correspondências bilaterais de conectores, proteção de pixels e autorização separada |
| Pipeline agente | `mapwork.py audit`, `mapwork.py next`, `AGENT.md`, `README.md` e template da zona | Instrução agora exige redes globais antes de lotes; auditor impede que os 14 macrolotes sejam tomados como cobertura completa |
| Regressão | `tests/test_urban_architecture.py`, `tests/test_mapwork.py` | **65 testes aprovados** no workflow 44736967670, incluindo caso sintético e auditoria do Kingswell real |

## Limite declarado, não disfarçado

- **Arquitetura V3.1** (motor, contratos, testes, integração de agente): implementada e validada em candidato.
- **Geometria de Kingswell**: não está pronta para geração. O esboço MACRO U02_KW_SKETCH_02 permanece aprovado, mas as ruas e trilhos reais ainda precisam ser extraídos/vetorizados da referência e o território classificado com máscaras válidas. Os 14 retângulos antigos cobrem somente ~16,32% do polígono bruto; não são lotes verdadeiros.
- A fixture sintética prova a computação de quadras e tarefas; **não** prova que a topologia real da U02 foi reconstruída.
- O modelo de ocupação usa metas relativas de forma urbana, não inventa população por pixel nem edifícios não documentados.
- As máscaras sintéticas são provas de contrato; o próximo trabalho com dados reais deve obter ativos e encaixes verificáveis. Sem status `GENERATION_READY`, **nenhuma arte**.

## Próxima entrada técnica do mesmo processo Kingswell

`BUILD_GLOBAL_TRANSPORT_AND_TERRITORY_V31`: reconstruir a autoridade viária/ferroviária/bondes/rios de U02, harmonizar bordas e níveis e classificar 100% do território. Executar o planejador V3.1 para derivar os lotes e tarefas. Só após estes gates discutir início de geração artística; não reabrir decisões de identidade ou os marcadores de conflito X01–X03 removidos.

**Governança:** todos os arquivos estão na branch candidata `mapwork-v3/kingswell-planejamento-20261119`; `master` e a U02 permanecem intactos. Não é release canônica nem fechamento final de Kingswell.
