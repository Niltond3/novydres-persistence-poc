---
id: arch-phase-a-validation
status: CANDIDATO_PENDENTE_APROVACAO
scope: NOVYDRES_GLOBAL
classification: PLAYER_SAFE
---
# Validadores, regressão e cutover ZERO LEGADO

## Validações determinísticas mínimas (fase C implementa)
V01 schema: validação de JSON/YAML e version dos schemas; dados nunca coergidos silenciosamente.
V02 IDs: uniqueness por namespace, casefold/Unicode normalizado, ID por owner, enum status, subject_id e kind obrigatórios.
V03 refs: toda relação referencia assunto existente, schema de destino correto, timestamp e direção; índice inverso apenas derivado; rotas de fonte por ID e commit.
V04 autoridade: owner único de cada campo/escopo/tempo, role e governança comprovados por decisão; estado epistêmico/visibilidade/proveniência obrigatórios; conflito explicitamente classificado.
V05 eventos: ledger insert-only no diff contra base e contra ancestral histórico, nenhum registro editado/excluído, idempotência, correction explícita, causalidade e autoria/intent checadas no nível formal.
V06 estado: reconstrução determinística de projeções a partir de registros auditados e checkpoints; comparar checksum/fields/saldo XP/FV/fome e last event. Eventos sem prova não entram.
V07 ciclo: simular gates de papéis/transições, impedir narrar por documento candidato, manter pin exato de manifest/schema/contrato/estado e predecessor.
V08 sigilo: varredura para valores GM_HIDDEN nos documentos/public prompts, nomes/commits e metadados; revisão contextual independente obrigatória além de string matching.
V09 catálogo: determinismo byte-a-byte, unicidade ID, todos os destinos e índices resolvidos, content index hash sem circularidade, nenhum desvio não gerado.
V10 Git: commit único, parent esperado, proteção de refs, re-leitura dos blobs e árvore; rejeitar force, sha stale, alteração de congelados não autorizada e divergência sem resolução.
V11 mídia: licença, localização e integridade reais dos originais quando aplicável, preservando Drive como mídia primária expressa; não inventar SHA ou URL.
V12 legado: parser de árvore HEAD FINAL + scanner AST/JSON/text/URLs de imports/config/schemas/CI/scripts/prompts/workflows; qualquer rota antiga, symlink, alias, wrapper, fallback ou leitura compatível -> FAIL.

Nenhum validador puramente sintático garante que uma fala pertence ao PJ, que um NPC sabe uma informação, ou que a cronologia é dramáticamente correta. Essas verificações são gate editorial humano e teste adversarial; proibir alegar 100% de segurança sem evidência. UNKNOWN legítimo e conflito não aprovado são estados válidos, exceto quando sua resolução é precondição de uma operação.

## Evidências e reprovação de E
E só PASS se a HEAD promovida contiver EXATAMENTE topologia nova para todos os recursos operacionais do repositório. Zero caminhos de runtime antigo; zero nomes _Vnnn como revisão atual (V5 da edição é permitido); zero diretórios legacy/archive ativos; zero aliases, symlinks, redirects, imports, strings de rotas antigas em qualquer consumo operacional. A CI inspecciona toda a árvore, não apenas novydres/; texto histórico aprovado dentro de fato pode citar nomes antigos como citação de proveniência, mas não pode acionar recuperação. Se a distinção histórica/operacional não for provada, FAIL. Todos os arquivos de histórico necessários vivem em commits/tags antigos, não no HEAD como fallback. O catálogo corrente só aponta para assuntos novos. Inspecionar serviços externos como dependências; não prometer ausência universal fora do repositório. Assegurar CI anti-regressão em commits seguintes.

Antes da promoção: verificar todos os registros autorizados, narrativa literal, correções, rolagens, decisões, relações, conhecimento, fontes, mídia, regras, estado e ciclos; nenhum retcon e nenhuma perda. Congelados não podem ser mutados sem nova autorização. Preparar tag de checkpoint pré-cutover e plano de incidente; publicar candidato em branch; revisão independente e aprovação explícita; promover atomicamente com lease; readback de commit, catálogo, índices, origem dos registros e smoke tests em snapshot fixo. Em falha, master antigo segue ativo. Após cutover, rollback é exceção explícita de incidente, não rota permanente.

## Suíte fixa e métricas de sucesso
B estabelece baseline sobre mesmo conjunto de tarefas e IDs antes/depois; guardar consultas, expected evidence e respostas aceitas em fixture sem spoilers. Mínimo 30 perguntas de recuperação (10 mundo/regras, 10 personagem/relacionamentos/conhecimento, 10 cronologia/episódios/estado), 12 testes negativos de autoria/alegações/UNKNOWN/segredos/retcon/G26/G28 e 12 jornadas de mutação/concorrência/idempotência. Usar 3 execuções em Codex e 3 em ChatGPT Web para cada classe; sem pressupor que resultados de uma ferramenta provam outra.

Medidas:
- precisão factual: 100% em invariantes críticos (evento, autoria PJ, XP/FV, canon/congelamento, segredos e cursor); recuperação de campos não críticos >= baseline, divergência documentada e sem false CONFIRMED;
- completude: 100% das entradas do inventário auditadas quanto a owner/destino ou GAP bloqueante; 100% de refs resolvidas; 0 registros históricos perdidos/editados;
- segurança: 0 vazamentos PLAYER_SAFE, 0 ações não autorizadas, 0 _Vnnn legados como rotas operacionais no HEAD final;
- leitura: registrar tokens reais da entrada e documentos lidos, chamadas de ferramenta, bytes transmitidos e número de documentos por tarefa, mediana/p95 em mesmas 30 consultas; não piorar mediana/p95 de tokens e leituras versus baseline, alvo aspiracional de reduzir >=20% sem criar PASS fictício;
- tempo: registrar latência p50/p95 de leituras e escrita com ambiente, erro e repetições; não exigir ganho numérico sem baseline, mas regressão p95 >10% exige justificativa formal e aprovação;
- escrita: commits por jornada, payload de blobs, leituras de verificação, falha CAS, fanout de arquivos mudados, retry idempotente; meta 1 commit atômico por transação de estado, sem write amplification desnecessário;
- navegação: 100% das queries por ID devem apontar a owner único ou NOT_FOUND explícito, zero fuzzy fallback, no máximo bootstrap+catalogo+index+fontes necessárias;
- integridade reprodutível: hash Git de cada origem/saída, tree diff, protocolo de replay e resultados CI com run ID/commit. Se CI indisponível, NOT_EXECUTED, nunca PASS.
Quantidade absoluta de arquivos não é métrica de sucesso, mesmo que diminua ou aumente.

## Gate de fases
A: documentos e lacunas com readback, somente PENDING_APPROVAL até decisão do jogador.
B: casos protótipos completos, sem ativação, equivalência e baseline da suíte comprovadas.
C: validadores/roteadores executados com testes negativos em dois canais, sem regressão de integridade.
D: cobertura de todas as fontes com provas de equivalência e owners; sem silenciar conflitos.
E: auditoria final ZERO LEGADO + testes + aprovação + promoção atômica; FAIL absoluto se sobrar rota antiga.
