# Kingswell — Lotes e conectores V2 (preparação para arte)

**Base:** esboço integral `U02_KW_SKETCH_02` já aprovado, não alterar U02. Esta etapa **não** aprova uma nova imagem.

O plano original de seis famílias e sete grupos está preservado em `preparacao-tecnica.json`. Esta V2 o transforma em **14 janelas geométricas** com `core` e `envelope`, sem sobreposição dos cores (bleed de 1 pixel U02) e com os cinco POIs contidos nos respectivos cores. Não são polígonos cadastrais, máscaras finais ou cobertura integral dos quarteirões.

**Conectores:** 4 reservas sobre o **polígono irregular do esboço aprovado**, não sobre a caixa retangular de contexto. O auditor valida proximidade <=2 unidades U02 à borda; `audit_zone --strict` mantém bloqueio até verificação bilateral. **Conectores:** 4 reservas de borda (`KW-EXT-SUL-01`, `KW-EXT-SUL-02`, `KW-EXT-DRE-01`, `KW-EXT-DRE-02`) aparecem em `zone.json` e têm contrato geográfico em `lot-connectors-diagnostic.json`, porém **não estão assinados pelas zonas vizinhas**. A saída ferroviária regional `KW-EXT-RAIL-01` fica fora de Kingswell e **não pode virar conector exclusivo do raion**. Os 35 conectores internos são inventário de grafo: ruas, passagens e acabamentos **ainda exigem snap ao traçado U02**. As três pontes já aprovadas e duas balsas seguem preservadas.

**Retificações técnicas:** L07 não depende mais de lotes pertencentes a grupos futuros e L10 não depende de L09 (grupo posterior). Os IDs L01–L14 e GEN00–GEN06 permanecem.

**Limites de produção:** resolução 64 pixels detalhados por 1 pixel U02; limite por sublote atômico: 16×16 unidades U02 (1024×1024 pixels). Os macrolotes grandes devem ser subdivididos antes de arte. A geração continua BLOQUEADA até concluir subdivisão, máscaras preservando água/vias/trilhos, e contratos bilaterais de borda com Sulfok/Drevnigrad.

## Quadro de janelas

| Lote | Core [x0,y0,x1,y1] | Envelope [x0,y0,x1,y1] | Grupo |
|---|---|---|---|
| KW-L01 | `502,750,531,780` | `501,749,532,781` | KW-GEN-01 |
| KW-L02 | `670,773,711,810` | `669,772,712,811` | KW-GEN-01 |
| KW-L03 | `573,788,655,848` | `572,787,656,849` | KW-GEN-02 |
| KW-L04 | `805,803,854,854` | `804,802,855,855` | KW-GEN-02 |
| KW-L05 | `371,803,474,895` | `370,802,475,896` | KW-GEN-03 |
| KW-L06 | `691,875,727,908` | `690,874,728,909` | KW-GEN-03 |
| KW-L07 | `492,832,540,869` | `491,831,541,870` | KW-GEN-01 |
| KW-L08 | `729,909,771,942` | `728,908,772,943` | KW-GEN-03 |
| KW-L09 | `847,909,892,950` | `846,908,893,951` | KW-GEN-04 |
| KW-L10 | `903,806,975,898` | `902,805,976,899` | KW-GEN-03 |
| KW-L11 | `503,871,533,906` | `502,870,534,907` | KW-GEN-04 |
| KW-L12 | `552,871,625,929` | `551,870,626,930` | KW-GEN-04 |
| KW-L13 | `359,907,476,960` | `358,906,477,961` | KW-GEN-05 |
| KW-L14 | `389,963,545,1021` | `388,962,546,1022` | KW-GEN-05 |

**Próxima ação determinística:** subdividir macrolotes, construir máscaras geométricas, encaixar conectores físicos no raster U02 e validar continuidade bilateral. Sem imagens.

**Ajuste de implantação auditado:** L14 deslocado da área costeira rochosa para a faixa urbano-industrial sudoeste (core `338,905,357,953`), sem modificar o esboço aprovado ou a U02. A ferrovia regional continua fora do domínio de Kingswell.
