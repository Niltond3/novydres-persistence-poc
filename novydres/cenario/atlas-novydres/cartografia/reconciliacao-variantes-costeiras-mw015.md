---
document_id: MW-015-FIS01-RECONCILIACAO-VARIANTES-2010
subject_id: world-atlas-novydres
work_unit: MW-015
work_unit_status: OPEN_AWAITING_OWNER_SUBSTANTIVE_DECISION
canonical_status: NOT_APPROVED
geometry_replacement_authorized: false
source_master_sha: d9c24a0e889cb61c9050a0d4f1a818520aa49dc1
mw009_source_ref: mapwork/mw-009-revisao-costeira-fis01
mw009_checkpoint: beaede435e3538db951d310802ac1f665c3b51e5
mw014_source_ref: mapwork/mw-014-macroposicoes-nucleos-urbanos
mw014_checkpoint: aa0a5794edff80cc508a6439b1ce4dbef3ee6ca4
visual_file: comparador-reconciliacao-costeira-mw015.html
owner_decision: PENDING
---

# MW-015 — Conciliação das variantes costeiras MW-009 e MW-010

**Estado: ABERTO — decisão substantiva do proprietário pendente.** Nenhum contorno foi substituído; nenhum dado canônico de master, nenhuma branch MW-009–014 nem geometria de outras camadas foi editada por MW-015. A presente branch parte do HEAD MW-014 e somente adiciona arquivos de análise/visualização.

## Bootstrap e autoridades

Bootstrap corrente executado no `master` `d9c24a0e889cb61c9050a0d4f1a818520aa49dc1`, lendo `novydres/AGENTS.md`, `CONTEXT.md` e `catalogo.json` no mesmo SHA e resolvendo `world-atlas-novydres`. Contratos consultados: ADR-002, PRD-ATLAS-001, `cartografia/guide.md` e fontes do assunto. O guia de `master` é a autoridade de apresentação/fechamento, inclusive visualização integral ANTES/DEPOIS e proibição de handoff prematuro.

- MW-009 HEAD `beaede435e3538db951d310802ac1f665c3b51e5`: `macrogeometria-litoral-baia-ilhas-2010.proposal.json`, blob `70469509c01f68358c16659a99c332794a051309`. Costa `coast-mainland-001` de **101 vértices**; baía derivada de índices [20,76]; aprovação expressa em 17/11/2026, para o contorno continental e a baía apenas, `APPROVED_PENDING_PROPAGATION`; não canonizada e não integrada à base posterior.
- MW-010 HEAD `2a3932a015c8458226410ebfcd67d399b0a33e10`: costa **44 vértices**, baía derivada de [6,33], blob `d72cf3eb2b3fac9473017a6bbfdc46ea1efb8577`; aprovada em 16/11/2026 como base cartográfica **não canônica** atual. MW-011, MW-012, MW-013 e MW-014 conservam seu blob costeiro.
- MW-011 HEAD `03d4d2dbeec3d298f200de4169cbdba35dea1051`; MW-012 `216754fc6f21c1b52804a0ad6b9eb4cf6526a6ed`; MW-013 `cee95e61bcdb525e2cf8b88da842ce5ea950200f`; MW-014 `aa0a5794edff80cc508a6439b1ce4dbef3ee6ca4`.
- `master` não possui esta base cartográfica candidata; não existe promoção automática para fonte canônica. As duas aprovações são válidas nos escopos originais, sem revogação implícita.

## Comparação quantitativa (somente plano local sintético NOVYDRES-LOCAL-2010)

| Indicador | MW-009 aprovada isoladamente | MW-010, base de MW-014 |
|---|---:|---:|
| Vértices continentais | 101 | 44 |
| Índices de perímetro da baía na linha | [20,76] | [6,33] |
| Área calculada da baía (km² sintéticos) | 1.845,255 | 1.881,995 |
| Terra dentro da folha 120×100 km (km² sintéticos, sem ilhas) | 8.214,3900 | 8.167,7425 |
| Ilhas candidatas | 3 (2 internas, 1 externa) | As mesmas 3, idênticos anéis |

A variante MW-009 aumenta a área de terra recortada na folha em **46,6475 km² líquidos** comparada à MW-010; não é área municipal e não prova expansão urbana. Diferença de baía de **−36,740 km²** na MW-009. Nenhum datum EPSG, batimetria, limite de cidade, densidade ou extensão municipal é inferido. A contagem 101 vs. 44 não é nota de qualidade nem precisão geodésica.

## Interfaces com MW-011–MW-014

As outras geometrias da comparação vêm literalmente dos arquivos estruturados de MW-014, mantidas iguais à esquerda/direita:
- 7 envelopes de macrorelevo e 3 cristas; `macrorelevo-2010.proposal.json` blob `cccc4eaac09b192a299108389bef3494f1f15bda`.
- 9 cursos d'água inclusive afluentes, 5 bacias, 3 corpos d'água e trecho termal; `macrohidrografia-2010.proposal.json` blob `d0912bb8b420a8a29b0de602f4eb05f179da3b0c`.
- 10 envelopes orgânicos de Ermo (2.349 vértices combinados); `malha-territorial-ermos-fis04-2010.refined.proposal.json` blob `eac63da71d49fbe55d79da2ee82fbafae609decd`.
- 9 pontos de ancoragem urbana aprovados somente para base de trabalho não canônica em MW-014; nenhuma posição mudada. MW-014 **continua aberta**, incluindo candidata E funcional ainda aguardando revisão visual, não canonizada.

**Validação exploratória reproduzida com os JSONs remotos:**
1. As cinco saídas costeiras de cursos d'água permanecem sobre ambas as geometrias de costa (distância linear 0 m do ponto final à polilinha): Rio Vasyl [25000,2000], curso meridional [1000,-22000], curso setentrional [-42000,43000], saída da lagoa continental [-45000,-42000] e canal de maré [23000,-3500].
2. Teste de vértices contra polígonos de terra: entre 7 relevos, 10 Ermos, 9 cursos, 3 lagos, 5 bacias e 9 âncoras, somente a bacia `basin-northern-exposed-001` apresentou 2 vértices aquáticos em **ambas** as versões, portanto é condição preexistente, não efeito específico da migração; polígono de bacia não equivale a limite de solo firme.
3. Comparação 500 m, centros das 48 mil células da proposta funcional E: 235 células (~58,75 km² amostrados) identificadas como terra apenas sob MW-009 (classe 0, sem uso atribuído); 47 células (~11,75 km²) como terra apenas sob MW-010. Destas últimas, **7 células (1,75 km² raster)** classificadas nas classes 1 (3), 2 (1) e 3 (3) pela candidata E da MW-014 cairiam em mar sob MW-009 sem nova máscara. Esse conflito é uma contagem de centros de células e **não** prova interseção geoespacial exata nem qualifica os usos como aprovados.
4. A troca hipotética exigiria novas verificações de interseções, anéis, referências de costa nos JSONs de relevo e hidrografia, envelopes de Ermo, máscara funcional E e quaisquer consumidores. As aprovações de MW-011–014 não podem ser automaticamente transportadas para um sistema geométrico diferente.

**Limitações:** testes exploratórios executados em JS do conector, não equivalem a certificação GIS completa, Node/CI ou navegador real. Não foi executada uma rebase, fusão ou propagação das geometrias. Toda aprovação MW-015 ainda requer deliberação, implementação/consolidação escolhida, validação efetiva e revisão final.

## Artefato visual e alternativas substantivas

`comparador-reconciliacao-costeira-mw015.html`: duas folhas integrais 2D síncronas, mesma escala, orientação, gráfico e todas as camadas; esquerda **MW-009 apenas no litoral**, direita **MW-010→014**; mesmo material posterior em ambas para revelar impactos da troca, sem mascará-los como reconciliados. Camadas técnicas opcionais, E opcional explicitamente não aprovada; botão de exportar SVG. HTML autônomo com geometrias incorporadas. Revisão efetiva do proprietário pendente.

**Decisão única a solicitar:**
- **A — Manter MW-010 como base corrente não canônica**, sem substituir geometria; preservar MW-009 como variante aprovada isolada em histórico/proveniência.
- **B — Selecionar MW-009 como nova candidata de base não canônica**, autorizando **somente nesta MW-015** adaptação/remascaramento de dependências afetadas, atualização de referências, validação integrada e uma nova comparação integral para aceite final; seleção inicial **não** canoniza e **não** aprova automaticamente geometria posterior.
- **C — Solicitar uma terceira composição de costa**, conservando MW-010 até apresentar/validar/obter aceite da variante integrada.

A recomendação técnica inicial é **A** caso não haja preferência visual inequívoca a favor da geometria MW-009: evita reabrir a interface de MW-011–014 e preserva integralmente as duas aprovações. A alternativa **B** é viável como proposta de trabalho mas precisa do aceite e da propagação explícitos.

**Inventário de decisões:** uma escolha A/B/C do proprietário, seguida (conforme escolha) de validação da versão efetiva e eventual aceite visual final. Nenhuma resposta foi fornecida nesta unidade até o momento. Status `OPEN_AWAITING_OWNER_SUBSTANTIVE_DECISION`.

**Não produzir handoff MW-016 e não fechar MW-015** até cumprir todos os critérios do `guide.md`. Não alterar `master`, crônica, história ou runtime.
