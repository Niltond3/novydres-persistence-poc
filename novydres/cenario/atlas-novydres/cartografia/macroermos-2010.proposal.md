---
document_id: MW-005-MACROERMOS-NOTAS
subject_id: world-atlas-novydres
year: 2010
workflow_status: PROPOSED_PENDING_OWNER_REVIEW
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
dependent_hydro_checkpoint: 4185b05dcecee4a9a4fcacdf8efa5b7bde61c714
---

# MW-005 — Proposta de macrogeometria dos Corredores do Ermo (2010)

## Entregável, autoridade e proveniência

A fonte geométrica única desta unidade é [macroermos-2010.proposal.json](macroermos-2010.proposal.json), com verificador [validar-macroermos.mjs](validar-macroermos.mjs). Há **10 polígonos candidatos** para as quatro classes naturais canônicas: três setores de cristas/contrafortes, três de tundra/permafrost, duas várzeas e duas faixas costeiras expostas. A soma sintética é **801.590 km²**; não constitui área oficial de Ermo, área municipal ou cobertura territorial exaustiva. A identificação é descritiva, não batiza lugares oficialmente.

A modelagem utiliza o quadro de MW-001 aprovado como hipótese operacional e referencia, sem redibujar, a costa de MW-002, o relevo de MW-003 e a hidrografia de MW-004, todos **não aprovados como geometria canônica**. O arquivo estruturado registra os hashes Git dos três objetos dependentes, o commit 4185b05dcecee4a9a4fcacdf8efa5b7bde61c714 e o snapshot de master 27595ca32652efdef3d406eb91e4482299056bd9. As autoridades de GEO-003.5 e GEO-004.3 continuam em `../macrorelevo-hidrografia-ermos-2010.json` e `../ermos-estrutura-territorial-2010.json`, sem edição.

## Modelo físico e topologia

- **Cristas:** três polígonos contidos nos envelopes fisiográficos setentrional, oriental e meridional de MW-003; nascentes fluviais que os atravessam representam drenagem natural, não infraestrutura.
- **Tundra:** um segmento nordeste e dois sudoeste, ambos ancorados nas planícies candidatas; os dois fragmentos sudoeste preservam o lago de MW-004 sem recortá-lo nem cobri-lo.
- **Várzeas:** uma no baixo meridional associado à microbacia independente e outra junto ao curso inferior candidato do Rio Vasyl, sem transformar o rio inteiro em Ermo.
- **Litoral:** duas faixas em terra firme próximas de trechos **externos e expostos** da linha costeira candidata, distintas da enseada protegida e sem estabelecer novas margens.

As interseções de polígonos com cursos naturais são explicitamente registradas por ID no JSON e verificadas. A presença de um rio em um Ermo não configura ponte, estrada, ponto de travessia, canal artificial nem autorização de circulação livre. Os dez polígonos não se interceptam entre si nem invadem mar, lagos ou lagoas.

Os segmentos não são o perímetro de um décimo raion. A morfologia de barreiras é representada materialmente, mas **não se prova ainda que cada núcleo urbano ficará separado**: não existem polígonos aprovados de núcleos e raions. Não inferir ocupação ou corredores de transporte a partir dos espaços entre essas feições.

## Teste e limites

Da raiz do repositório:

```sh
node novydres/cenario/atlas-novydres/cartografia/validar-macroermos.mjs
```

O verificador compara os hashes Git dependentes e respectivos estados, referencial espacial, tipos e IDs, geometrias de anéis, colisões terra/mar/lagoas, ancoragem no relevo, proximidade ao litoral exposto, interseções de cursos d'água, ausência de sobreposição entre segmentos e exclusões de escopo. As verificações de geometria foram reproduzidas por JavaScript no orquestrador do ChatGPT antes da publicação; **a execução de Node no checkout remoto não é afirmada** sem workflow observável.

Não foram determinados altitudes, risco quantitativo, largura física de passagens, tráfego, limites urbanos, raions, travessias de GEO-012/GEO-013 ou ancoragem geodésica. Costa, relevo e hidrografia candidatos poderão exigir revisão de todos estes segmentos.

## Decisão pendente e aceite

O proprietário poderá **aprovar, corrigir ou rejeitar** esta hipótese de dez polígonos, sem aprovar implicitamente MW-002, MW-003 ou MW-004. A aceitação técnica de MW-005 significa entrega estruturada e validação sintética, **não canonização**. A próxima unidade deverá escolher explicitamente seu próprio objetivo e verificar os arquivos do GitHub, sem tratar este handoff como fato.
