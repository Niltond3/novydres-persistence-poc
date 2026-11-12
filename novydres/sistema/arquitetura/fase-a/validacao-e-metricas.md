---
id: arch-phase-a-validation
status: CANDIDATO_PENDENTE_APROVACAO
scope: NOVYDRES_GLOBAL
classification: PLAYER_SAFE
---
# Validadores, regressão e cutover ZERO LEGADO

Emendas documentais em 2026-11-11 e 2026-11-12: aplicar DEC-16–DEC-27 do [ADR-001 §11](../adr/001-subject-oriented.md#11-revisão-do-harness-narrativo). DEC-19 aceita a exceção estrita de métricas Web; DEC-20 exige revisão dos limites excessivos. DEC-21 aceita a substituição das quotas fixas por cobertura de riscos, detalhada abaixo e no [plano integral](../plano-integral/index.md); não reescrever as evidências anteriores. DEC-23/DEC-24 substituem ledger/replay universal e auditoria de faces por estado atual, texto integral, Git e efeitos materiais. Nenhum teste ou gate é executado por esta emenda.

## Validações determinísticas mínimas (fase C implementa)
V01 schema: validação de JSON/YAML e version dos schemas; dados nunca coergidos silenciosamente.
V02 IDs: uniqueness por namespace, casefold/Unicode normalizado, ID por owner, enum status, subject_id e kind obrigatórios.
V03 refs: toda relação referencia assunto existente, schema de destino correto, timestamp e direção; índice inverso apenas derivado; rotas de fonte por ID e commit.
V04 autoridade: owner único de cada campo/escopo/tempo, role e governança comprovados por decisão; estado epistêmico/visibilidade/proveniência obrigatórios; conflito explicitamente classificado.
V05 histórico/transação: preservar texto jogado e fontes de decisões; verificar correções explícitas e idempotência. Estado corrente pode ser atualizado com fonte e diff Git. Não exigir ledger universal, insert-only de todo campo, registro por rolagem ou faces de dados (DEC-23/DEC-24).
V06 estado: conferir coerência dos recursos/ficha, consequência narrada, fontes e ponto de retomada no snapshot publicado; testar retomada em contexto renovado e após falha. Não exigir reconstrução universal por replay nem reexecução de dados. Divergência material exige conciliação antes de confirmação.
V07 continuidade: verificar o snapshot Git e os contratos efetivos, autoria, intenção pendente, cursor e transações de estado; impedir que documento candidato seja tratado como estado operacional. Conforme DEC-02/DEC-18, não exigir transição de papel, troca de chat ou novo manifesto por cena. Autorizações efetivamente necessárias continuam distintas de descoberta documental.
V08 sigilo: varredura para valores GM_HIDDEN nos documentos/public prompts, nomes/commits e metadados; revisão contextual independente obrigatória além de string matching.
V09 catálogo: determinismo byte-a-byte, unicidade ID, todos os destinos e índices resolvidos, content index hash sem circularidade, nenhum desvio não gerado.
V10 Git: commit único, parent esperado, proteção de refs, re-leitura dos blobs e árvore; rejeitar force, sha stale, alteração de congelados não autorizada e divergência sem resolução.
V11 mídia: licença, localização e integridade reais dos originais quando aplicável, preservando Drive como mídia primária expressa; não inventar SHA ou URL.
V12 legado: parser de árvore HEAD FINAL + scanner AST/JSON/text/URLs de imports/config/schemas/CI/scripts/prompts/workflows; qualquer rota antiga, symlink, alias, wrapper, fallback ou leitura compatível -> FAIL.

Nenhum validador puramente sintático garante que uma fala pertence ao PJ, que um NPC sabe uma informação, ou que a cronologia é dramáticamente correta. Essas verificações são gate editorial humano e teste adversarial; proibir alegar 100% de segurança sem evidência. UNKNOWN legítimo e conflito não aprovado são estados válidos, exceto quando sua resolução é precondição de uma operação.


## Continuidade no ChatGPT Web — condição de DEC-25

Q-07 foi aceita com condição: o objetivo é executar A–E no ChatGPT Web com GitHub, preservando a proteção contra erros que motivava chats limpos e handoffs. Não basta instruir o modelo a se autoavaliar. Esta especificação propõe reutilizar os contratos e validadores existentes; a eficácia só será conhecida após prova em B/C. Q-08 foi aceita como DEC-26 em 2026-11-12, definindo o risco residual e a parada excepcional sem dispensar a prova dos controles.

| Controle / momento | Evidência e recuperação propostas | Tarefas |
|---|---|---|
| Entrada de tarefa e mudança relevante de snapshot | Recuperar do GitHub o commit, a tarefa, as decisões e as fontes afetadas. Comparar checkpoint e HEAD antes de escrever; mudança de HEAD exige reconciliar, não misturar snapshots. | A05, B03–B04, C02–C04 |
| Proposta de alteração | Reutilizar V01–V12 aplicáveis para detectar IDs/caminhos inexistentes, referências quebradas, inconsistência de estado estruturado, mudança fora do escopo autorizado e alteração histórica indevida. Conferir afirmações decisivas contra o conteúdo da fonte, além de verificar a existência do link. Comparação semântica assistida não é prova determinística. | A06, B02–B04, C01–C07 |
| Declaração de conclusão | Exigir resultado externo consultável: commit/diff/readback e, quando aplicável, run CI com commit, conclusão e logs reais. Mensagem do próprio chat dizendo PASS não substitui execução. Uma etapa sem evidência não libera sua dependente. | A05–A06, B05, C07–C08, D06–D07, E03 |
| Divergência detectada | Suspender a alteração/avanço afetado; reler fontes e último checkpoint confirmado, identificar a causa, corrigir a proposta no escopo e repetir apenas as verificações afetadas. Retomar no mesmo chat quando a divergência estiver resolvida. Não repetir a mesma tentativa sem informação nova nem reverter fatos/recursos publicados para facilitar recuperação. | A05–A06, B04, C03–C05, C07 |
| Conclusão de tarefa/fase e interrupção | Atualizar um checkpoint curto no registro de progresso existente: tarefa/fase, último commit confirmado, escolhas aplicáveis, provas, pendências e próxima unidade elegível. Handoff usa esses dados; não criar outro arquivo por teste ou obrigar transportar prompts entre fases. | A07, C04–C05, D05 |

**Limites de automação.** Os scripts/CI precisam executar fora do raciocínio livre do chat e produzir resultados recuperáveis pela integração disponível. A05 verifica acesso real a refs/arquivos por SHA, escrita autorizada, disparo ou acompanhamento de CI e leitura dos resultados; não presume que qualquer conexão GitHub ofereça essas ações. B usa o executor mínimo isolado, C entrega a ferramenta final. Se um controle exigido não puder ser executado/observado no Web, registrar a lacuna: simulação em qualquer ferramenta não satisfaz a condição. Nenhuma API nova, serviço permanente ou segundo agente obrigatório por tarefa está implícito.

**Casos de prova.** Integrar à cobertura por riscos de DEC-21: fonte inexistente; fonte existente que não sustenta a conclusão; decisão antiga usada contra a emenda; tarefa declarada concluída sem saída/run correspondente; checkpoint divergente do HEAD; correção e retomada no mesmo chat. Incluir revisão semântica contextual para o caso em que todos os campos são válidos, mas a interpretação é falsa. Medir quais falhas foram detectadas e quais passaram; não chamar isso de detector universal nem presumir equivalência a chat limpo sem comparação. Reutilizar os casos de B e os validadores existentes quando cobrirem o risco.

**Limite aceito (DEC-26 / Q-08, 2026-11-12).** Esses controles reduzem falhas verificáveis, mas não garantem ausência de alucinação semântica; o jogador aceita o risco residual de erros não detectados. Manter a revisão independente já prevista e permitir continuidade enquanto as provas forem válidas. Se a recuperação não restabelecer fonte/estado confiável, pausar a unidade afetada e fornecer handoff para renovação excepcional do chat. Outras tarefas só podem seguir se forem independentes da pendência. Não prometer que o Web inicia novo chat sozinho, que mede toda sua saturação ou que trabalha indefinidamente sem novo turno/limites da plataforma. A aceitação resolve a política de exceção e o risco residual, sem comprovar os controles de DEC-25.

Referência metodológica: a [documentação oficial da OpenAI sobre avaliações](https://developers.openai.com/api/docs/guides/evaluation-best-practices) recomenda avaliação específica da tarefa, automação e calibração com julgamento humano; a [orientação sobre agentes](https://developers.openai.com/api/docs/guides/agent-builder-safety) explicita que mitigações não eliminam todos os erros. São orientação para o desenho, não comprovação de capacidades do ChatGPT Web ou deste repositório.

## Evidências e reprovação de E
E só PASS se a HEAD promovida contiver EXATAMENTE topologia nova para todos os recursos operacionais do repositório. Zero caminhos de runtime antigo; zero nomes _Vnnn como revisão atual (V5 da edição é permitido); zero diretórios legacy/archive ativos; zero aliases, symlinks, redirects, imports, strings de rotas antigas em qualquer consumo operacional. A CI inspecciona toda a árvore, não apenas novydres/; texto histórico aprovado dentro de fato pode citar nomes antigos como citação de proveniência, mas não pode acionar recuperação. Se a distinção histórica/operacional não for provada, FAIL. Todos os arquivos de histórico necessários vivem em commits/tags antigos, não no HEAD como fallback. O catálogo corrente só aponta para assuntos novos. Inspecionar serviços externos como dependências; não prometer ausência universal fora do repositório. Assegurar CI anti-regressão em commits seguintes.

Antes da promoção: verificar todos os registros autorizados, narrativa literal, correções, rolagens, decisões, relações, conhecimento, fontes, mídia, regras, estado e ciclos; nenhum retcon e nenhuma perda. Congelados não podem ser mutados sem nova autorização. Preparar tag de checkpoint pré-cutover e plano de incidente; publicar candidato em branch; revisão independente e aprovação explícita; promover atomicamente com lease; readback de commit, catálogo, índices, origem dos registros e smoke tests em snapshot fixo. Em falha, master antigo segue ativo. Após cutover, rollback é exceção explícita de incidente, não rota permanente.

## Suíte por riscos e métricas de sucesso
B estabelece baseline e candidato sobre casos e IDs comparáveis, com fontes fixadas e gabarito separado do executor. DEC-21 substitui a quota de 30 consultas, 12 negativos e 12 jornadas repetidas três vezes em cada canal. Esses casos existentes são insumos reutilizáveis, não contagem mínima nem prova automática de cobertura.

- Cobrir recuperação de mundo/regras, personagem/relações/conhecimento e cronologia/episódios/estado; incluir as falhas históricas de B-Q29/B-Q30 e outros defeitos ainda pertinentes. Não excluir um caso porque falhou nem mudar seu gabarito para aprovar o candidato.
- Cobrir autoria, UNKNOWN, segredos, retcon, recursos, persistência, correções, idempotência, concorrência, confirmação perdida e recuperação. Vincular cada risco a caso, resultado esperado e evidência. Quando procedimentos antigos forem substituídos, testar a função sucessora, sem ressuscitar o procedimento só para satisfazer o fixture.
- Executar testes determinísticos uma vez por versão relevante; repetir após mudança que invalide a prova. Compartilhar evidência quando código, fontes, contrato e risco permanecerem válidos. Exercitar a rota real de leitura/escrita adotada; teste adicional de outro executor só é necessário se diferença concreta invalidar a prova, conforme DEC-27.
- Justificar a amostragem dos comportamentos variáveis do agente e repetir seletivamente para concorrência, falhas e suspeita de intermitência. Uma resposta correta não demonstra confiabilidade geral. Não impor três rodadas indistintas nem declarar falhas intermitentes eliminadas por amostra pequena.

A06 fecha essa cobertura antes da execução de B. Relatórios registram casos executados, falhas e limitações; não produzem novo PASS a partir da redução da suíte. Métricas antes/depois usam casos e condições comparáveis. Mediana/p95 só são relatados com dados suficientes e método explícito; amostra insuficiente é declarada, sem percentis inventados.

Medidas:
- precisão factual: 100% em invariantes críticos (evento, autoria PJ, XP/FV, canon/congelamento, segredos e cursor); recuperação de campos não críticos >= baseline, divergência documentada e sem false CONFIRMED;
- completude: 100% das entradas do inventário auditadas quanto a owner/destino ou GAP bloqueante; 100% de refs resolvidas; 0 registros históricos perdidos/editados;
- segurança: 0 vazamentos PLAYER_SAFE, 0 ações não autorizadas, 0 _Vnnn legados como rotas operacionais no HEAD final;
- leitura: registrar tokens reais da entrada e documentos lidos, chamadas de ferramenta, bytes transmitidos e número de documentos por tarefa, mediana/p95 sobre os mesmos casos comparáveis e com amostra adequada; não piorar mediana/p95 de tokens e leituras versus baseline, alvo aspiracional de reduzir >=20% sem criar PASS fictício;
- tempo: registrar latência p50/p95 de leituras e escrita com ambiente, erro e repetições; não exigir ganho numérico sem baseline, regressão p95 >10% exige investigação e justificativa. Conforme DEC-22, esse percentual técnico isolado não impõe nova aprovação; consultar o jogador se houver impacto material de experiência, mudança de escopo/autoridade ou decisão não resolvida;
- escrita: commits por jornada, payload de blobs, leituras de verificação, falha CAS, fanout de arquivos mudados, retry idempotente; meta 1 commit atômico por transação de estado, sem write amplification desnecessário;
- navegação: 100% das queries por ID devem apontar a owner único ou NOT_FOUND explícito, zero fuzzy fallback, no máximo bootstrap+catalogo+index+fontes necessárias;
- integridade reprodutível: hash Git de cada origem/saída, tree diff, procedimento reproduzível de verificação e resultados CI com run ID/commit. Se CI indisponível, NOT_EXECUTED, nunca PASS.
DEC-19: quando o ChatGPT Web não expuser tokens reais ou bytes HTTP, registrar NOT_OBSERVABLE para esses campos. A exceção não equivale a sucesso medido, não exige estimativa substituta e não impede a avaliação dos demais critérios. Manter consultas, respostas, fontes, documentos/chamadas/leituras e tempos quando observáveis. Falha factual, teste não executado e ausência de evidência operacional ou CI não são cobertos. Não exigir prova de redução percentual sobre valores indisponíveis.

Quantidade absoluta de arquivos não é métrica de sucesso, mesmo que diminua ou aumente.

## Gate de fases
A: documentos e lacunas com readback, critérios completos e escolhas substantivas resolvidas. DEC-22 permite transições A–D pelos critérios comprovados depois da autorização futura de implementação do plano; nova confirmação apenas por fase não é exigida. A etapa atual continua documental.
B: casos protótipos completos, sem ativação, equivalência e baseline da suíte comprovadas.
C: validadores/roteadores executados com testes negativos no fluxo efetivamente adotado, sem regressão de integridade.
D: cobertura de todas as fontes com provas de equivalência e owners; sem silenciar conflitos.
E: auditoria final ZERO LEGADO + testes + aprovação + promoção atômica; FAIL absoluto se sobrar rota antiga.

## A06 — Cobertura por risco, gabarito isolado e fronteira de execução (2026-11-12)

**Entrada:** A02–A05 publicados; branch design `b22f03e7190e4bed39cdf6b1dce7b123a40aff01`. **Decisões:** DEC-17/19/20/21/23/24/25/26. **Estado:** especificação de gates B/C e matriz de prova completa; estes testes permanecem **NOT_EXECUTED** nesta A06 e não substituem o gate B anterior.

### Artefatos históricos relidos e limites

- `fase-b/fixtures-consultas.json`: **30 IDs B-Q01..B-Q30**, em três grupos (mundo/regras, NPC/relações/conhecimento, cronologia/estado), com **`expected_from_source` e `actual_from_candidate` no mesmo arquivo**. Isso exige projeção estrita somente de `id/group/name/request/snapshot` ao executor, **sem as respostas e gabaritos**. O avaliador independente recebe o arquivo integral em passo separado. O booleano `pass` é resultado histórico de comparação, **não** acerto de um agente real.
- `fase-b/fixtures-negativos.json`: **B-N01..B-N12**, `mode=ACTUAL_LOCAL_DETERMINISTIC_ASSERTION_NOT_REMOTE_ATTACK`; não contam como ataque executado contra rota real sem payload isolado, esperado, readback e invariantes pós-rejeição.
- `fase-b/fixtures-mutacoes.json`: **B-M01..B-M12**, `mode=SIMULATED_TRANSACTION_PREDICATE_NOT_REMOTE_GIT_WRITE`; não contam como concorrência remota ou alteração atômica real.
- `fase-b/matriz-equivalencia.json`: 4 assuntos NPC/trama/história/estado, **6 source_refs** com SHA do snapshot `c26c0fbf15fff6c817182c06e6208e302b954f3a`. Fonte histórica não é HEAD corrente: a comparação de C41 com C45 atual deve distinguir **equivalência ao snapshot fonte** e **prontidão do estado atual**.
- `fase-b/resultado-testes.json` e `gate-e-readback.json` permanecem `B_REMEDIATION_REQUIRED`; Codex histórico 51/90, casos B-Q29/Q30 falhos em todas as rodadas. `B-Q29` e `B-Q30` medem recursos XP e FV; podem falhar por misturar o checkpoint histórico C41 ao C45, não se deve ajustar seu gabarito ao erro. Os demais erros do canal, respostas sem localizador e lacunas negativas/CI seguem relevantes.
- A04 documenta obrigação de trajetória e ficha, não comprova V5 final. DEC-24 dispensa face individual, **não** medição e conservação dos efeitos materiais de XP/FV.

### Matriz mínima de riscos, executor, oráculo e reprovação

| Risco / função | Evidência mínima e seleção justificada | Executor/validação | Reprovação |
|---|---|---|---|
| Descoberta de owner, caminho, ID e commit | Amostra representativa dos quatro assuntos, referências exatas das 6 fontes; ID ausente, colidido e hash divergente | B01 reconcilia mapa; B02/B03 recuperam no fluxo aplicável; auditor verifica árvore e blob em SHA fixo | Owner duplo, fallback, fonte inexistente, hash errado, ID inventado |
| Mundo/regra e status editorial | B-Q01..Q10 como **pool reutilizável**, estratificação de status/UNKNOWN/alegações; fonte factual original em avaliador isolado | B02/B03; C01/C02 determinístico | `candidate` promovido, claim como fato, ausência convertida em negação |
| NPC, aliases, relações, conhecimento e divulgação | B-Q11..Q20, negativos N01/N02/N03/N04/N05/N06/N09 e caso semântico de informação correta atribuída a ator errado | B02/B03 + revisor independente; C01/C05 para invariantes | Atribuição de conhecimento não provada, segredo/identidade vazados, resultado social anulado |
| História, cronologia, autoria e prosa | B-Q21..Q28, B-N07/08/11, M06/09/10/11; trecho integral + fonte e classificação de preparo | B01/B02/B03/B04, depois C04/C05 | Novo evento por migração, data inventada, cena iniciada, texto histórico perdido |
| Recursos críticos, aquisição versus meta | **B-Q29/Q30 obrigatórios até defeito resolvido**, M07, N09/N10; avaliar no C41 histórico e C45 corrente separadamente | B02/B03 com oráculo independente; C01/C04, revisão de deltas | XP/FV divergente, teto ≡ crédito, compra inventada, convenção provisória ≡ aquisição |
| Persistência, autoria, idempotência, concorrência | B-M01..M12 conforme cobertura e novas operações de stale/confirmation-lost; sandbox temporário isolado, dois writers, `tx_id` igual/diferente | B04 executa API GitHub real e confirma HEAD/blobs; C03 implementa transação definitiva | Segundo commit duplicado, lease stale aceito, ref forçada, escrita mestre/cânone, confirmação por autorrelato |
| Continuidade e recuperação DEC-25 | Injetar fonte ausente, fonte existente mas irrelevante, decisão antiga superada, checkpoint diferente do HEAD, PASS sem run, recuperação na mesma conversa | B03/B04 Web real + avaliador independente; C04/C07 replay **de teste**, não ledger narrativo | Avança apesar de divergência, não detecta erro verificável, omite limitação ou não fornece handoff DEC-26 |
| Narrativa, elipse, NPCs, mistério e revisão de políticas | Exercícios fictícios específicos A04, incluindo recusa/êxito social, salto não obrigatório, intenção persistente, verdade de mistério fixada, correção material | B04/C05, revisão editorial contextual independente; D04/D05 verificam regras sucessoras | Plano vira evento, tira agência, troca verdade central, deixa cadência G28 antiga como fallback depois de E |
| Segredos e metadados | Payload GM_HIDDEN sintético por sentinel em fixture isolada + revisão contextual de saída/commits/paths | B04/C05/C07 revisor que não publica segredo, scanner de strings + avaliação | Qualquer divulgação proibida em output PLAYER_SAFE, título, caminho ou handoff |
| CI, ZERO LEGADO e equivalência | CI com commit/run IDs, scanner em toda a árvore, exact-path refs e comparador de bytes/owner | C06/C07 e D06/D07; E03 auditoria independente | Qualquer rota operacional antiga no HEAD final, import órfão, run inexistente, autopass sem prova |

**Seleção DEC-21:** os 30/12/12 históricos são **pools**, não quotas. Neste ponto, como B-Q29/Q30 continuam falhos e os 30 casos não têm todos localização/citação verificadas, os **30 IDs B-Q** permanecem selecionados inicialmente como baseline comparável, com eventual redução **somente após** mapear cobertura de risco, validar equivalência de gabarito e documentar por que cada exclusão é segura; não usar número menor para esconder falhas. Os 12 negativos e 12 jornadas são catálogo de riscos a transformar em operações reais, podendo ser consolidados em menos execuções quando uma única operação provar múltiplas invariantes e nenhuma função deixar de ser coberta. Não repetir testes determinísticos se código/snapshot não mudou; repetir os de comportamento variável, concorrência e falha onde amostra única não basta, registrando razão, condições e frequências. Nenhum PASS por percentual de quantidade de arquivos.

### Isolamento, bindings e readback

Cada caso de execução recebe **somente**: `case_id`, pergunta sem resposta, tipo, `candidate_commit`, `source_commit`, owner esperado em forma de ID **quando não for gabarito factual**, limite de divulgação e instruções de retornar `{answer,epistemic_status,source_path,source_commit,source_blob_sha,source_excerpt_locator,read_operations,elapsed_if_observable}`. O avaliador separado faz comparação contextual com gabarito, verificando se **o trecho sustenta de fato** a conclusão e se o ator/tempo/escopo são legítimos. Autorrelato `pass` do executor não é evidência.

Negativos/mutações precisam de **payload executável isolado** (alteração deliberadamente inválida), HEAD e tree prévios, comando/operação realmente acionada, resposta do GitHub ou validador, HEAD/tree posteriores e diagnóstico. Exemplos sem escrita em master/campanha: ref descartável, dois commits filhos do mesmo parent, tentativa stale e readback; fonte/ID fictícios, mesma transação com payload conflitante, fonte não resolvida e erro de disclosure. Quando regra exigir bloquear antes de chamar Git, a evidência inclui diagnóstico do validador e confirmação remota de estado inalterado. **Nunca** simular ação e descrevê-la como Git remoto.

Comparar baseline e candidato com **mesma consulta, mesmo escopo temporal, mesma fonte de verdade e mesma janela de conhecimento**. C41 e C45 pertencem a snapshots diferentes; um valor correto no C41 não é resposta ao C45. Se migração substitui procedimento por decisão aceita, medir a **função preservada** em vez da assinatura do procedimento antigo. Registrar custo, chamadas, latência e bytes expostos por função/integração efetivamente medida; tokens/bytes HTTP reais Web não expostos são `NOT_OBSERVABLE` (DEC-19), nunca inventados. Preservar falhas e saídas de runs.

### Fronteira B versus C e critério de PASS

- **Executor mínimo B:** usar os quatro candidatos já existentes e funções de consulta/validação fora do runtime (por exemplo, scripts temporários de teste em sandbox), sem instalar roteador oficial, novo bootstrap, CI definitivo, handlers de cena ou contrato sucessor ativo. O fluxo efetivamente utilizado deve ler e retornar com evidência real; revisão independente e CI aplicável continuam gates de B, sem obrigação de dois canais.
- **C só depois de B05 PASS:** implementar gerador de catálogo, resolução, schemas ativos candidatos, transações e recuperação como código versionado da branch e rodar CI; sem ativar master/runtime. ZERO LEGADO completo é gate E e requisito implementado em C/D.
- **PASS crítico:** 0 falsos eventos, 0 novas decisões de PJ, 0 erros XP/FV, canon, segredos, owner/cursor, referência e recurso; **não críticos:** pelo menos baseline comparável, sem false CONFIRMED. O caso que falhar deve ser corrigido e repetido, com gabarito fonte **imutável**. CI necessária com `run_id`, commit, status, logs e verificações realmente concluídas.
- **DEC-25:** resultado de caso e recuperação provados automaticamente/externamente quando a função for determinística, e revisão contextual independente para semântica. Uma sessão de Web com respostas corretas não certifica confiabilidade generalizada; se a recuperação falhar, DEC-26 impõe `RECOVERY_FAILED` e handoff. **Até demonstrar B/C, a continuidade sem chat novo permanece condicional.**
- **Reprovação obrigatória:** qualquer teste crítico faltante, gabarito exposto ao executor, resposta sem fonte que sustente a afirmação, CI não executada, corrida simulada sem execução real ou ausência de evidência de leitura/escrita **não** vira PASS por exceção de telemetria. Não há promessa de detector semântico universal.

**Responsáveis:** A06 produz a seleção e contratos; B01 remapeia fontes e valida candidatos; B02/B03 executam recuperação factual e integração funcional; B04 exerce mutações/negativos/recuperação; B05 consolida evidência independente e gate; C01–C07 implementam; C08 revê C; D06/D07 audita cobertura; E03 decide ZERO LEGADO/ativação somente com autorização. Todos os outputs públicos PLAYER_SAFE.
