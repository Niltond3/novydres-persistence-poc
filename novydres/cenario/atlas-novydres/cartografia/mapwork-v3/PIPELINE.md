# Mapwork V3.2 — execução única, validação obrigatória e retomada

**Status em 20/11/2026:** infraestrutura executável implementada em branch candidata; **não é uma cidade gerada e não é cânone**. O fluxo falha fechado quando faltam dados reais, bytes, decisões ou conectores. A validação da fixture só prova o motor; não prova a cidade real.

## Única porta de entrada

```bash
python scripts/pipeline.py run --district sulfok --checkpoint /tmp/sulfok.json
python scripts/pipeline.py run --district kingswell --checkpoint /tmp/kingswell.json
python scripts/pipeline.py run --zone zones/<zona>/zone.json --spatial zones/<zona>/global-spatial-v31.json --reference /tmp/U02.png --checkpoint /tmp/estado.json
```

Leia `next_action`, `blockers`, `phase`, `inputs.*_sha256` e `architectural_report` do JSON. O agente executa **apenas** a próxima etapa permitida e roda `pipeline.py run` novamente. Não use `mapwork.py next`, `render` ou `urban_architecture.py` como fluxos independentes: eles são componentes internos ou compatibilidade legada. A pipeline **não** publica, canoniza ou aprova por conta própria.

## Máquina de estados, sem atalhos

| Etapa | Entrega objetiva | Bloqueio obrigatório |
|---|---|---|
| 0. BOOTSTRAP | Canon no SHA de master, sujeito geográfico, identidade, vizinhos e checkpoint persistido | Zona não encontrada: criar manifesto **a partir do cânone**, não inventar |
| 1. RESEARCH | Fontes externas datadas, tipologias e padrões urbanos comparáveis | Sem pesquisa, não perguntar preferências nem desenhar |
| 2. DECISIONS | Somente dúvidas substantivas, uma por vez | Falta de decisão impede esboço |
| 3. TECHNICAL_SKETCH | Mapa integral com transportes, bairros, quadras, POIs e bordas | Sem aprovação expressa do usuário, parar |
| 4. SPATIAL_MODEL | Rede global em coordenadas U02; solo/rios/vias/trilhos/bondes/metrô/aquedutos/dutos; polígonos de uso exclusivos | Manifesto real ausente, ou rede incompatível, impede planejamento |
| 5. SPATIAL_VALIDATION | `plan_city`: 100% território classificado, cruzamentos, quadras, masks, seams, fila integral | Fixture, U02 sem SHA verificado, costura sem autoridade, máscara falsa |
| 6. URBAN_DESIGN | Cada work unit recebe parcelas e footprints individuais, uso, pavimentos, caminho à rua; JSON determinístico versionado | Falta de unidade, divergência de conteúdo ou parcela inacessível |
| 7. ART_GENERATION | O agente invoca gerador de imagens sobre um trabalho pequeno, usando plano e referência | Somente depois de todos os gates técnicos e autorização de arte |
| 8. COMPOSITION | `--execute`: verificar PNG+mask+SHA; preservar tiles aprovados e impedir pixel protegido/reescrita anterior | Sem bytes anteriores, proteção, recibos ou plano integral, falhar |
| 9. REVIEW | Comparador ANTES/DEPOIS integral da candidata, no chat ou arquivo direto | Aprovação explícita da arte; nunca presumir |
| 10. PUBLISH | Agente externo faz Git CAS + Drive readback + gate editorial, confirma SHA remoto | Sem aprovação, não alterar ponteiro do cânone; handoff só após fechamento |

A pesquisa e geração de imagem são **ações externas**, executadas por um agente com ferramentas conectadas. GitHub Actions roda Python/testes, **não** recebe por padrão imagens privadas do Drive nem invoca automaticamente geradores de imagem. ChatGPT Web ou Claude Web sem ferramentas de execução/Drive equivalentes devem reportar bloqueio, não fingir que completaram uma etapa. Isto é uma exigência de capacidade, não um prompt que a substitua.

## Artefatos e comandos por estágio

1. `zones/<slug>/zone.json`: identidade, estado, aprovações e decisões existentes, não duplicar o raion.
2. `zones/<slug>/global-spatial-v31.json`: rede global, polígonos de território, perfil por uso, POIs, seams reservadas contra digest SHA da rede. O desenho precisa corresponder à U02 original; geometria sintética não serve.
3. `python scripts/pipeline.py run --zone ... --spatial ... --reference ... --design-unit WU-... --out /tmp/candidata`: produz `urban-design/WU-....json` com footprint individual e acesso calculado. Checar e registrar os vetores em Git por commit candidato; repetir por todas as unidades.
4. `python scripts/pipeline.py run --zone ... --spatial ... --reference ... --design-root zones/<slug>/urban-design`: compara **todos os planos vetoriais** com o que o motor regeneraria; depois checa `mask_receipt`, as aprovações e os assets. Art não está liberada apenas por existir arquivo.
5. `python scripts/pipeline.py run --zone ... --spatial ... --reference ... --design-root ... --assets /tmp/assets --before /tmp/tiles-aprovados --out /tmp/candidata --execute`: compõe **somente** se todos os arquivos, SHA e gates passaram. O comparador é candidato e exige revisão humana.

`--before` é obrigatório quando `world-state.json` referencia uma release anterior. O compositor mescla a base de cada tile com o aprovado e impede alterações de pixels aprovados: edições intencionais de obra anterior precisam de processo de autorização e reprojeto próprio, não de bypass. A pasta `--before` deve conter uma cópia **materializada e SHA-validada de todos** os tiles do último estado aprovado: `tiles` + `inherited_tiles`. O catálogo candidato referencia os tiles inalterados em `inherited_tiles` e conserva `parent_manifest_sha256`, sem duplicar PNGs; manifestos com `stage` não aprovado ou sem IDs remotos são rejeitados. Ao publicar, é obrigatório confirmar os IDs herdados e os novos, e tornar o conjunto novamente materializável no próximo checkpoint.

## Regras de geometria e arte

- Uma única autoridade espacial: `global-spatial-v31.json` e contratos globais de conectores; zonas não redefinem estrada/ferrovia/água.
- `plan_city` deriva os quarteirões pelo solo e work units por cobertura exata; metrô/dutos subterrâneos têm nível negativo e não recortam a malha superficial.
- Primeira zona pode reservar conectores `APPROVED_SCOPED` amarrados ao SHA da rede global. Com vizinho real, a verificação torna-se bilateral, sem substituir a reserva silenciosamente.
- Planejamento de edifícios atual usa células abstratas U02 como parcelas operacionais, **não** lote cadastral em metros: footprint, pavimentos, uso e rota pedonal são candidatos determinísticos. Antes de considerar urbanismo real final, revisar quadras, pátios, acessos veiculares, margens e proporções visuais no mapa integral.
- Nunca aumentar a resolução como se isso criasse novas ruas ou edifícios. Geração artística constrói os detalhes sobre o plano, não define a topologia.
- Preservar a U02, aprovação de esboço, usuários e decisões anteriores; jamais transformar `SKETCH_APPROVED` em aprovação de imagens.

## Testes de aceite e prova

- **Automáticos no GitHub Actions:** `mapwork.py audit`, `pipeline.py run` em Kingswell (deve mostrar dependência real e não publicar), pytest de máscaras, composição, colinearidade, rede subterrânea, seams, planos de edifícios.
- **Teste real obrigatório antes de chamar isso de concluído:** uma zona real com manifesto U02 vetorizado, referência privada SHA-verificada, todos os blocos e footprints acessíveis, 2 work units artísticos em tile compartilhado, imagem anterior intacta, rede e água intactas, ligação com zona vizinha, comparação integral acessível no chat, upload/readback, retomada em chat limpo.
- **Negativos:** alterar pixels protegidos; sobrepor arte anterior; conectar duas ferrovias sem nó ou cruzamento; mover seam do vizinho; faltar um plano de edifício; remover máscara; usar fixture como zona real; publicar sem aprovação → tudo deve bloquear.
- **CI verde não substitui** QA visual, conectores privados, revisão do proprietário ou proteção de branch/merge; tais controles precisam ser verificados separadamente.

## Pendências externas honestas

- Não há manifesto real vetorizado e totalmente classificado de Kingswell/Sulfok nem bytes U02/Drive disponíveis no CI. Por isso a pipeline hoje **corretamente bloqueia** geração real.
- O gerador de arte, inspeção visual de fachadas, reconstrução automática de ruas da imagem e comparador leve/lazy para milhares de tiles continuam sob responsabilidade de integrações/etapas específicas. Não chamar o fluxo de ponta a ponta concluído sem o teste real acima.
- Nenhum merge em `master`, nova release, alteração de imagem canônica ou publicação de zonas decorre desta branch.


## Contratos adicionais P1 (20/11/2026)

- Toda zona vizinha com `global-spatial-v31.json` existente deve ser lida e confrontada bilateralmente (sem aceitar reserva no lugar de contrato existente). Sem geometria de um vizinho ainda não gerado, somente reserva `APPROVED_SCOPED` ligada ao SHA da rede global é aceita.
- `special_sites` é obrigatório, mesmo quando vazio. Cada POI exige `block_id`, `point`, `footprint` e `entrance`, dentro de uma parcela acessível. O `spatial-plan.json` legado fornece a lista mínima de POIs a preservar. Morfologia exige `access_mode` e `access_clearance_units`, com corredor em escala U02 abstrata; não equivale a certificação viária métrica.
- Na fase GENERATING e posteriores, cada `work_unit` do plano requer um `element.kind=lot` com `work_unit_id` único e `core` idêntico ao bbox planejado. Antes da composição, máscaras de assets verificados são comparadas à área editável exata da unidade (não somente ao envelope).
- Para executar desde ChatGPT/Claude Web **sem filesystem**, criar pedido JSON em `web-requests/` usando CAS sobre o HEAD da branch candidata; o job hospedado retorna checkpoint/recibo em artefato do GitHub Actions. Não usar artefato temporário como estado canônico: persistir checkpoint no GitHub via commit CAS e confirmar blob/commit/ref. GitHub Actions sem Drive privado continua bloqueando etapas que exigem bytes. Não confundir o runner diagnóstico com um gerador de arte.


**Planejamento no runner Web:** a geometria estruturada pode produzir planos de quarteirões e edifícios sem carregar os bytes privados da U02; `source_bytes_verified` continua gate duro para AUTORIZAÇÃO DE IMAGENS, nunca para pesquisa ou pré-planejamento. Para agentes sem unzip/filesystem, `web_runner.py` expõe em logs de Actions `request_id`, `source_head_sha`, `blockers`, `inputs` e SHA do checkpoint. A persistência em Git exige CAS e readback por ação explícita do agente; se o conector não tiver operações de escrita CAS, bloquear com diagnóstico, sem inferir sucesso.


## Contratos P1 da V3.2 (candidate — 20/11/2026)

Os gates novos **falham fechados**. Não transformam uma geometria sintética em certificação de circulação real, nem autorizam o cânone.

- **Execução única:** `scripts/pipeline.py run` é a única entrada operacional. A composição `mapwork.composite` exige um contrato `NOVYDRES_MAPWORK_V32_COMPOSITION_CONTRACT_1` cujos SHA de zona, manifesto espacial, U02, planos individuais, assets, estado mundial e tiles anteriores são recalculados no momento do uso. A função `_compose_tiles` existe só como implementação interna e fixture; `mapwork.py audit` é diagnóstico.
- **Bordas:** vizinho já existente em qualquer status precisa de manifesto global. Para bordas de transporte, registrar `network_edge_id`, `level`, opcionalmente `network_node_id`, e perfil/largura/tipo compatíveis com os dois lados e a fronteira comum. Reserva `APPROVED_SCOPED` só vale quando ainda **não existe** zona vizinha.
- **POIs:** `special_sites` deve conciliar exatamente os IDs do plano aprovado (sem inventar/duplicar POI), ter `work_unit_id`, bloco/footprint e entrada na borda exterior, com acesso abstrato ao solo. POI não é um novo lote.
- **Acesso físico:** o grid U02 não tem conversão automática para metros. `physical_reference` requer origem declarada como `SURVEYED_APPROVED`, aprovação e evidência; `metres_per_unit`, larguras mínimas separadas para pedestres/veículos. Cada JSON de `urban-design/WU-....json` pode adicionar `physical_routes` com trajetos vetoriais indexados por **cada** `building.id`, `mode`, `width_m` e `points` da entrada à via em nível do solo. Um corredor passa por teste de largura ao longo do trajeto e detecção de footprints/barreiras nas unidades próximas. Sem referência física e trajetos, `physical_access_certified=false`, bloqueando arte.
- **Assets:** todo elemento local, incluindo `lot`, `special_building`, `poi`, `finish`, precisa de `work_unit_id`. `special_building`/POI exigem `building_id` e footprint coerente, POI ainda `site_id`. Todo pixel visível da máscara deve pertencer ao espaço editável da unidade; especial/POI fica limitado ao próprio footprint. Sobreposição de pixels de arte requer evidência explícita do proprietário para o par de elementos. Ruas, água, ferrovias, terreno e demais redes globais não são assets locais.
- **Web:** workflow em branch candidata usa `concurrency` por ref e checkout de histórico integral; antes de processar pedido Git, valida SHA remoto e percorre o intervalo completo do push, recusando múltiplos pedidos. O pedido é vinculado por `request_id`, commit e SHA do arquivo. Checkpoints e recibos incluem hashes dos inputs e logs mais artifact do Actions. Uma retomada `resume` exige que o agente versione em `web-checkpoints/<nome>.json` o checkpoint recebido e declare seu SHA256; qualquer adulteração, mudança de input ou divergência de fase falha. Retomada confere e repete o checkpoint, sem saltar gates; entradas novas exigem novo pedido/versionamento.

**Operacionalização Web:** o agente publica pedido somente na branch candidata, com `expected_parent_sha` igual ao pai do commit que inseriu/alterou o pedido. Uma execução deve incluir no máximo um pedido distinto por push. O runner não grava no repositório, não processa mídias privadas, não substitui pesquisa externa e não gera imagens.

**Evidência ainda ausente:** U02 privada aprovada, modelo espacial métrico autorizado, corredores individuais de cidade real, assets de imagem efetivos, compare ANTES/DEPOIS real e promoção remota de release. Nenhum teste sintético pode preencher essas lacunas. A declaração de `CORRIGIDO` em auditoria independente depende também de auditor revisar os caminhos alternativos, o diff e os resultados dos workflows; a PR não deve ser mesclada automaticamente.
