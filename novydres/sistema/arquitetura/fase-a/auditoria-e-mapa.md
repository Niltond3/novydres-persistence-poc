---
id: arch-phase-a-audit
status: CANDIDATO_PENDENTE_APROVACAO
scope: NOVYDRES_GLOBAL
classification: PLAYER_SAFE
---
# Auditoria de fronteiras e mapa de migração (somente leitura)

## Evidência de entrada
Repositório privado Niltond3/novydres-persistence-poc. HEAD design conferido em 2d1b5ca7e9afeccef2af922fc8248a33154a3317; árvore b877b8abce845beaab09955e99a5f3fed6f02fd0, resposta recursive não truncada, 842 blobs e 81 trees. Aproximadamente 687 nomes satisfazem padrão semelhante a revisão nominal, inclusive muitos sem serem estritamente cópias. Master na revisão: 44b5c2348ccd3bb2ea5edaaa918f2f55b197321b, HEAD divergiu em dois commits por lado; nele MANIFEST_V53 e CYCLE_V0038, diferente de MANIFEST_V51 e CYCLE_V0036 da branch. Não misturar claims e pins entre ambos. Números de caminhos e sua evolução NUNCA são gate nem KPI.

Contratos confrontados: ADR-001, .AGENT.md, .CONTEXTG.md (bootstrap histórico), .AGENT_V4.md, .CONTEXTG_V3.md, GITHUB_PRIMARY_CONTRACT_V4, G26, G28, START_HERE_V7/V9, ORCHESTRATION_CONTRACT_V8/V10, editorial_governance_v1_0, DECISIONS_STATE_V10, EVENT_PROTOCOL_V5, MIG-DEC-002, MANIFEST_V51/V53 e diretórios de orquestração. A autoridade ativa exige cadeia de ciclos/schema/hashes e manifesto pinado; esta inspeção de arquitetura NÃO certifica que a cadeia completa foi executada e validada operacionalmente.

## Matriz de fronteiras (candidata, não MOVE executado)
| Fonte atual | Destino proposto | Prova necessária / cautela |
|---|---|---|
| novydres/world/{history,geography,politics} | cenario/{historia,geografia,politica} | status editorial por documento e cada alegação; seis candidate não podem ser promovidos pelo nome |
| novydres/world/organizations, lineages | cenario/organizacoes, cenario/linhagens; identidades globais em personagens | variantes conflitantes e ownership; guardar origem |
| novydres/governance | sistema/governanca | preservar decision IDs, escopo global/local e cadeia de autoridade; sucessor político explícito |
| novydres/systems | sistema/regras | versão V5 semântica, perfil local não vira regra global |
| novydres/runtime/{scene-execution,orchestration,provocation-prep,xp,narrative-architecture} | sistema/narrativa e sistema/regras para contratos; cronicas/{id}/orquestracao, preparacao, biblia e auditorias para instâncias | distinguir código e schema de contratos de preparação, resultados e ciclo efetivo |
| novydres/chronicles/CHR-001/{LIVE*,HISTORY_INDEX*,character,episodes,events} | cronicas/CHR-001/{estado,episodios,registros,elenco} + personagens para identidade global | preservar texto e efeitos narrativos, estado e fontes históricas existentes; sem exigir faces/RNG ou conversão em ledger (DEC-23/DEC-24); deduplicação só com prova de igualdade |
| novydres/chronicles/CHR-001/{knowledge,narrative-atlas,npc-disposition,preparations,world,orchestration} | cronicas/CHR-001/{elenco,tramas,fios,historias,biblia,preparacao,orquestracao} | segredos e epistemologia, decisões de D02–D12 e fios abertos não viram fatos inventados |
| novydres/migration/{drive-archive,library-sources,binary-sources,...} | fontes/{originais-textuais,registro.json,midia} ou script/fixtures de migração | distinguir material probatório, cópia, metadados, prova histórica; binário original conforme política Drive |
| novydres/assets/drive-links | fontes/midia/registro.json | manter links/IDs privados e integridade declarada, sem transferir imagem ao GitHub |
| poc/{memory-v1,chr-test-001} | scripts/fixtures e resultados de teste apenas | PROIBIDO importar POC sintético como evento real |
| .github/workflows/* | .github/workflows/* reescritos | sem arquivo/caminho/command legado ou fallback na E; auditar strings e referências |

## Colisões conhecidas a NÃO resolver
1. CONFLICT-001: seis fontes editoriais marcadas candidate vs relato de fechamento posterior não auditado; manter ambos.
2. CONFLICT-002: discrepância de version de mapa editorial; não reescrever.
3. CONFLICT-003/003B: variantes de fonte de NPC com autoridade editorial pendente; não escolher silenciosamente.
4. Dependência de mídia Drive: originais visuais no Drive por decisão vigente, metadados e links no GitHub, cinco originais informados como pendentes em inventário anterior; verificar números e status novamente em D.
5. Texto histórico não comprova execução técnica de RNG ou ledger. DEC-23/DEC-24 dispensam essas reconstruções: conservar consequências, estado e fontes existentes, sem criar certificados nem registros por dado.
6. G24/DEC-CR-014 e editorial governance v1.0 exigem versionamento por cópia/nome. ADR-001 prevê arquivos estáveis Git-native. Requer sucessor formal e aprovação antes da ativação.
7. Design C36 e master C38 divergem: B exige reintegração explícita e validação contra HEAD atual, sem forçar master, sem regressar estado.

## Procedimento de cobertura integral para D
A é inventário estrutural, não reconciliação linha por linha de todos os relatos. D começa enumerando a árvore do master de entrada e registrando PARA CADA PATH: original SHA, categoria (operacional, imutável, cópia, fixture, geração, binário, suspeito), status de governança, owner novo, destino, tipo de transformação, hash/prova, visibilidade, vínculos, evidência, conflito, destino de história e test IDs. Abrir linha mesmo para fonte aparentemente duplicada; provar equivalência antes de aglutinar. Varredura de strings cobre Markdown, JSON, YAML, Python, JS, workflows, prompt, config, testes, documentação e referências fora do repo inventariadas. Paths da migração histórica ficam na árvore Git anterior, não em pastas de compatibilidade da HEAD final. Para fontes sem aprovação ou sem bytes disponíveis: BLOCKED/PENDING_EVIDENCE, sem supressão silenciosa. Prova final de D inclui cobertura de entradas, destinos resolvíveis e invariantes de conteúdo/visibilidade, não contagem de arquivos.

## A01 — Reconciliação de entrada (execução 2026-11-12)

**Estado:** `PASS` de A01 no escopo de reconciliação estrutural e fontes decisivas, sem migração, sem validação operacional completa, sem passagem automática do gate A. **Mandato:** mensagem expressa do jogador em 2026-11-12 autoriza executar A–D na branch candidata, sem cutover em master, ativação de runtime ou cenas. Fontes e medições são do GitHub nesta execução, não de relatórios anteriores.

### Snapshots, comparação e integridade

- **Design:** `5b55c12f4d041187ee597eb786049e7dbe5a22fc`, tree `8d18ced68b684f48a6fea6f39c734f493698c1af`; **master somente leitura:** `c9fcfc0c558cd17d58ec8c8272da3ed70182ff37`, tree `4894bebafcc872dcd7c772ea4d34e5d54079b810`. `compare_commits`: `diverged`, merge-base `cb9aa9e422fb0327e04e9eb0929e4ab678785405`, 15 commits design à frente, 28 atrás de master. Não efetuar merge automático nem importar estado atual de master por cópia cega.
- Árvores recursivas do GitHub não truncadas. **Design:** 895 blobs, 97 trees; **master:** 1.029 blobs, 81 trees. Blobs por caminho: 839 idênticos; 189 exclusivos de master; 55 exclusivos de design; 1 caminho comum divergente (`.github/workflows/novydres-marco-closure-v2.yml`). A contagem é de descoberta, nunca equivalência semântica ou KPI.
- No master, `CYCLE_V0045.json` (Git blob `14f746139ab0dda35ee5de95cf8a4536631534fd`) aponta `MANIFEST_V63.json` (Git blob `18b20257ad79c9b6a596c293f3445d28c64d8f71`). A referência ao predecessor C44 e **77/77 pares `path/blob_sha` do C45** coincidem com a árvore de master. Isto valida localizadores, **não** uma execução dos validadores da cadeia, nem disponibilidade de narrativa para esta tarefa.
- Design possui `CYCLE_V0036.json` (blob `213e0ba00bfcb75f7e37bd5be35fb1bd9495b920`) e `MANIFEST_V51.json` (blob `2a315f5593068e8ff8031cc6b3ca68846d926077`). O ciclo C36 está `PROVOCATION_CLOSURE_PENDING`, distinto da cabeça operacional posterior. master contém C37–C45 e M52–M63 ausentes da design. Não combinar `LIVE`, character, conhecimento ou orquestração entre os commits.
- O conector GitHub autenticado tem `pull=true`, `push=true`; leitura por ref/SHA, árvore, comparação, blobs e publicação com `expected_sha` estão disponíveis. A API de consulta a statuses e workflow runs respondeu; no commit de entrada design: **0 statuses e 0 workflow runs retornados**. Não representar CI não executado como PASS. Escrita/readback são aferidos pela publicação deste registro, não antecipadamente.

### Famílias cobridas, proprietário futuro e tratamento proposto

| Origem/escopo inspecionado | Dono ou tratamento na topologia futura | Critério da migração |
|---|---|---|
| Raiz `README.md`, `.AGENT*`, `.CONTEXTG*`, `MANIFEST*` | `AGENTS.md` / `CONTEXT.md` / `catalogo.json` como entradas; governança e instâncias de ciclo em owners específicos | Migrar descoberta, cadeia de autoridade e histórico por Git; não manter bootstrap operacional legado |
| `.github/workflows/` (5 design; 14 master) | Infraestrutura CI em `.github/workflows/` | Examinar os 10 exclusivos de master, 1 exclusivo de design e 1 compartilhado divergente; corrigir consumidores, imports e strings antes de ZERO LEGADO |
| `novydres/world/` | `cenario/`, perfis globais em `personagens/` | Origem editorial por capítulo, conflitos de status e variantes, sem promover candidate por inferência |
| `novydres/governance/` | `sistema/governanca/` | Preservar decisões, aprovações e texto canônico; produzir sucessores sem editar original congelado |
| `novydres/systems/` | `sistema/regras/` e fontes | Separar V5 (edição semântica), exceções locais, materiais de criação, scripts legados e documentação |
| `novydres/runtime/` | `sistema/narrativa/`, `sistema/regras/`, `cronicas/CHR-001/`, `scripts/` | Separar contratos gerais de instâncias, dados de preparação, resultados de teste e gates efetivos; reconciliar deltas recentes exclusivos de master |
| `novydres/chronicles/CHR-001/` | `cronicas/CHR-001/` e identidades em `personagens/` | Preservar texto jogado, fontes, recursos, conhecimento, eventos comprovados e UNKNOWN; sem nova cena nem ledger universal |
| `novydres/cronicas/` e `novydres/personagens/` da design | Candidatos do protótipo B, ainda não operacionais | Comparar com as fontes exatas em master, resolver gaps e repetir ensaios B após a emenda |
| `novydres/migration/`, `novydres/assets/drive-links/` e fontes externas controladas | `fontes/`, `scripts/migracao/`, histórico Git ou referência externa autorizada | Tratar metadados, direitos, 3 ZIP técnicos, texto original, proveniência e mídia sem cópia visual indiscriminada |
| `poc/` | `scripts/fixtures/` somente quando for evidência útil; senão retirar do HEAD operacional final | POC sintético não é evento de CHR-001 |
| `novydres/sistema/arquitetura/` | `sistema/arquitetura/` | ADR e backlog candidatos; aprovação e histórico preservados, nenhum roteador candidato ativado |

**Fontes controladas fora do Git:** política `MEDIA_STORAGE_POLICY_20261102_V1.md` mantém binários visuais originais no Drive e somente links/metadados no GitHub. `VISUAL_ASSET_REGISTRY_V2.json` indica 14 originais vinculados e **5 pendentes**; integridade por SHA-256 não é afirmada. Três ZIPs históricos constam em `migration/binary-sources/`, com SHA de blob Git verificável; sua presença não substitui políticas de mídia. Fontes Drive/Library sem bytes/permissão comprovados permanecem dependências pendentes, e jamais são reconstruídas por inferência.

### Autoridade narrativa e política — checagem limitada de A01

- `novydres/.AGENT.md` e `.CONTEXTG.md` são entradas com histórico de checkpoints superados. `.AGENT_V4.md` e `.CONTEXTG_V3.md` são os sucessores pinados no C45. A autoridade ativa depende da cadeia exata de ciclos, manifesto e contratos, não do nome de versão; estes documentos foram lidos, sem tornar o desenho ADR operacional.
- Fonte de **ficha-alvo**: `novydres/chronicles/CHR-001/character/TARGET_SHEET_V2_APPROVED.json`, blob `f8b62bf74f4f5f937a0f0d3b3462263d4a9d186c`, `APPROVED_LOCAL_TARGET_ACTIVE_NOT_BOUGHT`; separada de `ALLOCATED_SHEET_PROJECTION_V2.json`, blob `285e206f4ad956e1d6bdb6315366429aeb4d9bdf`, e do estado vivo posterior. Não tratar meta como compra, XP liberado, ação ou poder adquirido. A certificação final V5/2010 permanece pendente segundo `D12_MECHANICAL_GATES_MATRIX_V003_PLAYER_SAFE.md`.
- **Janela temporal:** arquivo `M3.02_TEMPORAL_TRANSITION_V2_PLAYER_SAFE.json`, blob `dca3e646bed186ddbce0448848bcbf66b1d60b31`, ancora o período de 1970 com data civil desconhecida; C45 registra M3.02 e mortalidade, sem Abraço. **2010** é alvo posterior da crônica principal, não data presente nem evento consumado. Não interpolar datas exatas nem aplicar elipse por esta auditoria.
- Questões preservadas: CONFLICT-001 (seis fontes candidate versus relato editorial posterior); CONFLICT-002 (schema version do mapa editorial); CONFLICT-003/003B (variantes de NPC e veredito pendente); cinco originais visuais faltantes; divergência da cadeia operacional; G19/G23/G24, DEC-CR-014 e `novydres_editorial_governance_v1_0.md` em tensão com Git-native/nomes estáveis do ADR. **A sucessão é proposta e depende de prova e autoridade própria antes de E**, não uma correção silenciosa. A relação da identidade familiar segue a retificação vigente nos documentos pinados, sem editar história.

### Repetições obrigatórias em B e limitações

`fase-b/gate-e-readback.json` permanece **B_REMEDIATION_REQUIRED**: recuperar por caso com fonte/citação localizável; corrigir falhas críticas; exercitar negativos e jornadas executáveis, idempotência e stale ref **remoto** em ref de sandbox; obter resultados Web reais e CI no commit correto, comparar gabarito isolado e medir o que for observável. DEC-19 permite `NOT_OBSERVABLE` apenas para tokens reais Web e bytes HTTP; DEC-21 substitui quotas por cobertura de risco sem apagar erros anteriores. DEC-25 exige comprovação dos controles e recuperação no mesmo chat antes de dispensar handoff por fase; DEC-26 admite pausa/renovação excepcional se fonte confiável não for restabelecida.

**A01 não conclui** A02–A07, B, nenhuma cadeia operacional inteira, migração de fontes externas, certificado de custo V5, equivalência semântica ou CI. Próxima tarefa elegível: A02 (topologia/granularidade), seguida das demais dependências de A. A07 consolida a emenda antes de retestar B.
