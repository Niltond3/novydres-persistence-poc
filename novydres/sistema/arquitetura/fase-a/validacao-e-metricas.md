---
id: arch-phase-a-validation
status: CANDIDATO_PENDENTE_APROVACAO
scope: NOVYDRES_GLOBAL
classification: PLAYER_SAFE
---
# Validadores, regressão e cutover ZERO LEGADO

Emendas documentais em 2026-11-11 e 2026-11-12: aplicar DEC-16–DEC-26 do [ADR-001 §11](../adr/001-subject-oriented.md#11-revisão-do-harness-narrativo). DEC-19 aceita a exceção estrita de métricas Web; DEC-20 exige revisão dos limites excessivos. DEC-21 aceita a substituição das quotas fixas por cobertura de riscos, detalhada abaixo e no [plano integral](../plano-integral/index.md); não reescrever as evidências anteriores. DEC-23/DEC-24 substituem ledger/replay universal e auditoria de faces por estado atual, texto integral, Git e efeitos materiais. Nenhum teste ou gate é executado por esta emenda.

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

**Limites de automação.** Os scripts/CI precisam executar fora do raciocínio livre do chat e produzir resultados recuperáveis pela integração disponível. A05 verifica acesso real a refs/arquivos por SHA, escrita autorizada, disparo ou acompanhamento de CI e leitura dos resultados; não presume que qualquer conexão GitHub ofereça essas ações. B usa o executor mínimo isolado, C entrega a ferramenta final. Se um controle exigido não puder ser executado/observado no Web, registrar a lacuna: simulação Codex não satisfaz a condição. Nenhuma API nova, serviço permanente ou segundo agente obrigatório por tarefa está implícito.

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
- Executar testes determinísticos uma vez por versão relevante; repetir após mudança que invalide a prova. Compartilhar evidência apenas quando a implementação e o contrato testados forem os mesmos. Exercitar as rotas reais de leitura/escrita e os riscos próprios de Codex e Web; resultado de um canal não comprova o outro.
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
C: validadores/roteadores executados com testes negativos em dois canais, sem regressão de integridade.
D: cobertura de todas as fontes com provas de equivalência e owners; sem silenciar conflitos.
E: auditoria final ZERO LEGADO + testes + aprovação + promoção atômica; FAIL absoluto se sobrar rota antiga.
