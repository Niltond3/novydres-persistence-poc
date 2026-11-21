**ChatGPT Web V3.3:** antes de chamar qualquer comando Shell ou alegar que `pipeline.py` não pode rodar, leia [`WEB_RUNTIME_V33.md`](WEB_RUNTIME_V33.md). Recupere o cache de código do Drive, compare cada Git blob ao HEAD no GitHub e use `v33_web_bridge.run_web` em Python, chamando exatamente a pipeline canônica. Não considere declaração textual como evidência; não peça decisões editoriais para resolver falhas de ferramentas. O gate INF-01 de Kingswell permanece bloqueado.

## V3.3 — protocolo visual obrigatório (candidato)

Antes de seguir as etapas abaixo, consulte [VISUAL_REVIEW_PROTOCOL_V33.md](VISUAL_REVIEW_PROTOCOL_V33.md). A imagem é gerada nativamente pelo agente, sem API. A pipeline confere artefatos e comprovantes com SHA, enquanto o agente analisa visualmente cada máscara e seus pares, e depois o atlas completo; sem parecer de unidade e parecer macro reais, não se solicita aprovação. O preflight não exige imagem ainda não gerada. A correção não cria cânone nem dispensa planejamento urbano prévio.

# NOVYDRES MAPWORK V3.3 — CONTRATO PRIORITÁRIO DO AGENTE

**Este bloco V3.3 prevalece sobre as instruções V3.2/V3.1 mantidas abaixo para histórico e regressão.**
**Estado: CANDIDATO / SEM CANONIZAÇÃO.** Não alegar que foi validada geração artística real até existir prova de transferência e composição no executor ChatGPT Web.

### Fluxo que o agente DEVE executar
0. Fazer bootstrap do HEAD atual de `master`: `novydres/AGENTS.md`, `CONTEXT.md`, `catalogo.json` no MESMO commit, mais ADR-002, PRD-ATLAS-001 e `cartografia/guide.md`. Validar referencial U02 em SHA. Não usar snapshot candidato como fonte canônica.
1. Interpretar entrada livre com identidade exata e produzir `NOVYDRES_MAPWORK_V33_INTENT_1`. Os quatro modos são `CREATE_REGION`, `REFINE_AREA`, `EDIT_ELEMENT`, `ADD_ELEMENT`. Se Torre Ventura (ou outro marco) não existir na fonte resolvida, NÃO inventar suas coordenadas.
2. Provar ferramentas reais: GitHub leitura/escrita e readback, Web, geração nativa ChatGPT, acesso local à imagem gerada, entrega de arquivos no chat. Se faltar capacidade, checkpoint BLOCKED. Nunca chamar Actions como runner obrigatório.
3. Pesquisar regiões análogas do mundo real com fontes independentes, URL, data, observação, relevância e adaptação. Pesquisa enriquece; nunca altera cânone por analogia.
4. Produzir registro versionado de propostas por ID, localização, impacto e origem. Perguntar UMA decisão substantiva ainda aberta por vez. Nenhum equipamento, ponte, rua, POI, novo prédio singular ou programa ordinário pode ser criado sem ID aprovado ou inventário/conjunto delimitado expressamente. `APPROVED_WITH_CONDITIONS` exige comprovar condições antes da arte. Rejeitado não volta como arte.
5. Derivar rede, quadras, parcelas, edifícios e máscaras no planejador existente com `pipeline.py`. Auditar vizinhos dos DOIS lados. U02 é abstrata; não prometer largura em metros sem medição autorizada. **Não solicitar aprovação do esboço técnico**: decisões vêm antes; projeto técnico é auditado internamente.
6. Criar receita de imagem para unidade autorizada, chamar ferramenta nativa ChatGPT, materializar bytes no executor, verificar SHA-256, dimensões, máscara, pixels protegidos, vias, continuidade, estética. Registrar inspeção visual separada; até três tentativas de reparo por unidade, depois bloquear. Nunca usar imagem simulada como prova de transferência.
7. Compor via `pipeline.py --execute --intent ...`. Todos os receipts DEVEM corresponder exatamente ao PNG e à máscara do asset aplicado; verificar novamente na entrada do compositor. Para `REFINE_AREA`, alteração aprovada só dentro da máscara editável; proteger o resto, inclusive arte já aprovada.
8. Entregar mapa integral ANTES/DEPOIS com zoom real e tiles on demand. Distribuir pelo próprio chat o pacote ZIP portátil, não um HTML isolado sem as imagens. No celular, apresentar visões gerais PNG juntamente com o ZIP quando disponíveis.
9. **Só após aprovação explícita da composição final:** persistir assets privados/IDs no backend aprovado, atualizar registros por Git CAS com expected HEAD e readback remoto; canonização exige autorização editorial adicional. Sem merge automático, sem handoff prematuro.

**Entrada de negócio única:** `python scripts/pipeline.py run ...`. `v33_flow.py`, `v33_contracts.py`, `v33_urban.py`, `v33_viewer.py`, `urban_content.py` e `mapwork.py` são bibliotecas internas. O uso legado `--district` permanece somente como diagnóstico regressivo, não autoriza `--execute`.

### Contratos materiais
- `--intent`: JSON de intenção com SHA de `master`, `scope-index.json` recomposto para o mesmo SHA e limites reais autorizados.
- `--capabilities`: receipts host reais; `--research-file`: evidências externas datadas; `--decisions-file`: decisões explícitas; `--inventory-file`: IDs exatos e sua fonte de autoridade.
- `--design-unit`: gera plano técnico; `--recipe-unit`: receita nativa a partir de plano assinado; `--audit-unit`: auditoria raster e visual; `--ledger`: tentativas e checkpoints.
- `--image-receipts`: um comprovante com imagem, máscara e aprovação visual do agente por work unit; `--editable-mask`: obrigatório para refinamento; `--reference`: U02 original com SHA.
- Falha de digest, proposta não autorizada, geometria não canônica, fixture, fonte sem readback ou transferência não comprovada = FAIL/BLOCKED. Não prometer completar mais tarde sem execução concreta.

**Limites atuais da candidata:** Sulfok ainda não tem geometria real nem decisões V3.3 da intervenção; Torre Ventura ainda requer localização canônica inequívoca. Sem os dois testes reais de aceitação não declarar V3.3 totalmente implementada.

---

## Histórico V3.2 abaixo (não usar gate de esboço na V3.3)

# Mapwork V3 — contrato do agente ChatGPT Web

## V3.2 — caminho obrigatório único

Leia `PIPELINE.md`. Após bootstrap do master em SHA fixo, execute `python scripts/pipeline.py run --district <id>` (ou `--zone` com manifesto existente), interprete SOMENTE `next_action` e `blockers`, efetue a etapa externa solicitada com as ferramentas efetivamente disponíveis e rode novamente. Salve checkpoints candidatos no GitHub com verificação de ref/tree/commit; não invente resultado de comando não executado. Pesquisa vem ANTES das perguntas. Planejamento espacial e plano individual de edifícios são obrigatórios ANTES da arte. `mapwork.py` e `urban_architecture.py` são módulos internos/compatibilidade, não pipelines alternativas. Na ausência de runner/Drive/gerador de imagem, pare com bloqueio explícito. `--execute` só compõe a candidata e nunca publica.

**Entrada:** "gere <zona>", "refine <quarteirão/lote>" ou "edite <edifício especial>". Nunca afirmar execução em segundo plano. Em sessões grandes, registrar checkpoint verificável na branch candidata e continuar a mesma unidade em conversa posterior, sem handoff prematuro.

1. **Bootstrap:** leia o HEAD remoto de master e AGENTS.md, CONTEXT.md, catalogo.json no mesmo SHA; resolva `world-atlas-novydres`, o owner geográfico exato e `cartografia/guide.md`. Leia `mapwork-v3/config.json`, `world-state.json`, template e última release global aprovada. A existência de uma branch candidata V3 não torna essa branch autoridade de cânone.
2. **Inventário:** classifique cada premissa como CANON, APPROVED_SCOPED, CANDIDATE ou UNKNOWN, com referências. **Correção do proprietário em 19/11/2026:** Cidade Velha = raion Kingswell inteiro (`district-chelsea`). O antigo ID `chelsea-cidade-velha` é alias de proveniência, não uma segunda zona. O microcentro original termal é parte morfológica interna; não gerar segundo polígono. O nome formal indígena anteriormente atribuído ao núcleo foi substituído por correção expressa do proprietário de 2026-11-19. Não invente limite, metragem, densidade nem POI. Traga do Google Drive apenas assets apontados por IDs no manifesto, verificando SHA.
3. **Pesquisa:** pesquise online tipologias arquitetônicas de cidades reais compatíveis com história/clima/densidade da zona; forneça URLs, data e analogia, separando fato histórico de proposta ficcional. Busque relações urbanas (transporte, instituições, largura de ruas, espaços comuns) sem presumir soluções universais.
4. **Decisões:** identifique perguntas substantivas ainda abertas, apresente uma por vez; grave resposta inequívoca no registro candidato. Não faça o usuário aprovar minúcias puramente técnicas. Reconciliar vizinhos e conectores antes de esboçar. Se geometria conflitar com zona aprovada, não reescreva a outra silenciosamente.
5. **Esboço:** mapa técnico 2D **integral**, com zonas vizinhas, redes, bairros, quadras, lotes, densidades, POIs e edifícios especiais. Breve quadro de alterações. Obter aprovação EXPRESSA da versão do esboço; sem aprovação, parar.
6. **Fila:** por padrão gerar 1 asset artístico por **lote**, incluindo pátio, múltiplos edifícios, neve, envelhecimento. Máscara por lote com core+bleed restrito; permitir aparência que ultrapasse lote mas não destrua conectividade semântica. Marcar edifícios relevantes como `special_building` e gerar isoladamente. Contexto da geração inclui vizinhos, iluminação, mesma escala e vista estritamente top-down 2D (90 graus), compatível com U02.
7. **Ciclo por asset:** gerar → inspeção visual → encaixar na máscara → verificar dimensões exatas na escala 64× e SHA → refazer somente se necessário. No máximo 3 tentativas automáticas por item; se persistir falha, checkpoint BLOCKED e diagnóstico. Não alterar a máscara para acomodar uma imagem sem registrar decisão. Não gerar a zona inteira como uma imagem única.
8. **Armazenamento:** para cada asset e máscara locais, use o bridge de arquivos do ChatGPT para enviar ao diretório `/Google Drive/NOVYDRES_MAPWORK_V3_ASSETS/` (ou o upload_file do conector quando tiver file_uri), obtenha ID real e confira metadata com Google Drive plugin. Guarde SHA256 + Drive ID em `asset` e `mask`. Nunca exponha URLs privados como links visuais. Arquivos sem readback ficam PENDING, não VERIFIED.
9. **Composição:** baixar os assets requeridos para pasta local temporária; executar o comando unificado `pipeline.py run --execute` após validação de plano, todos os planos de edifícios e máscaras, no sistema de coordenadas global. A ordem de composição segue `layer_order`; a geração por lote não tem permissão de sobrescrever a topologia de ruas/trilhos. Conectores da zona são validados contra todas as zonas vizinhas. Avaliar visualmente continuidade de fachadas, neve, sombras, telhados, água e costuras.
10. **Comparação:** usar o último release global **aprovado** como ANTES (se nenhum, U02); incorporar o alvo novo no DEPOIS. Entregar arquivo HTML interativo no chat e prévia integral; zoom deve ler os tiles reais, não aumentar apenas o baseline. Se não conseguir produzir visualização acessível, não solicitar aprovação.
11. **Fechamento:** após sua aprovação explícita da composição efetiva, gravar asset receipts e manifests no GitHub por transação Git CAS e confirmar ref/tree/blobs remotamente. Não mudar fontes canônicas ou world-state aprovado sem o gate editorial Atlas. Só emitir handoff da próxima unidade quando `guide.md` permitir.

**Estados:** PLANNING → SKETCH_APPROVED → GENERATING → VISUAL_REVIEW → OWNER_APPROVED → PUBLISHED. Falha técnica = BLOCKED no checkpoint, sem promoção silenciosa. `pipeline.py run` mostra a próxima ação determinística; pesquisa, perguntas e geração permanecem responsabilidade das ferramentas do agente, não do script.

**CI e verdade:** o workflow em PR **não** garante bloqueio de merge se branch protection indisponível. O agent gate recusa publicação com teste vermelho; não confundir proteção operacional com proteção GitHub administrada.


## Arquitetura V3.1 — obrigatória antes de gerar Kingswell

**Lote urbano = quadrante/quarteirão delimitado pela infraestrutura no nível do solo.** Construções, fábricas, oficinas e POIs são ocupantes internos; uma `work_unit` é somente unidade atômica de geração. A autoridade global inclui ruas, avenidas, artérias, trevos, viadutos, ramais ferroviários, bondes, água e conexões entre zonas. `U02_KW_SKETCH_02` está aprovado como esboço MACRO; a malha de lotes não está concluída e os 14 retângulos legados não são lotes da cidade. Antes de qualquer geração visual, executar e seguir `scripts/urban_architecture.py` e `architecture-v3-1-transport.md`, obter 100% de território classificado e área editável coberta, topologia e costuras verificadas. A saída da pipeline unificada para Kingswell, enquanto faltar geometria real, deve bloquear na construção do manifesto espacial, sem permitir arte.
