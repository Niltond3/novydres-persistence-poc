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
