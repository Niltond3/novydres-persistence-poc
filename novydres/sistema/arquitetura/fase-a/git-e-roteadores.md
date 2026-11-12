---
id: arch-phase-a-git-and-routers
status: CANDIDATO_PENDENTE_APROVACAO
scope: NOVYDRES_GLOBAL
classification: PLAYER_SAFE
---
# Git-native, concorrência e roteadores Web/Codex

Revisão documental em 2026-11-11: [ADR-001 DEC-17/DEC-18](../adr/001-subject-oriented.md#11-revisão-do-harness-narrativo) orienta o desenho abaixo. As decisões aceitas da entrevista precedem sua formulação original; a operação vigente e os registros históricos de aprovação não são alterados nesta etapa.

## Modelo de revisão e autoridade
A versão operacional é uma árvore de commit única; SHA do commit define snapshot e blob SHA define identidade de bytes. O catálogo, índices, estado corrente, árvore de assuntos e os metadados do commit integram UMA transação candidata. Nenhuma mudança de HEAD nem fonte autoritativa decorre da gravação de blob isolado. Git não fornece imutabilidade jurídica/absoluta: configurar branch protection/ruleset, impedir non-fast-forward e alterações não autorizadas das fontes históricas e preservar refs de checkpoints; o validador detecta violação, sem afirmar proteção que não foi instalada.

Escrita sob ADR será habilitada apenas após E e aprovação de sucessores. Não modificar o significado histórico de G24/DEC-CR-014 durante A–D; manter a antiga regra copy-on-write na operação corrente. O sucessor propõe que criação de novo commit com caminho corrente estável é o COW lógico, com commit predecessor recuperável. Conforme DEC-23/DEC-24, preservar fontes históricas sem exigir arquivo por evento/rolagem ou ledger universal; estado corrente recebe revisões Git. Essa mudança precisa aprovação editorial/jogador documentada no cutover.

## Leitura consistente por ferramentas efetivamente utilizadas
1. Fixar repo, branch permitida, HEAD SHA lido por ref. Se operação de runtime antes da E: usar discovery atual, nunca o layout de candidato.
2. Depois da E: abrir AGENTS.md e CONTEXT.md naquele commit; estes retornam catalogo.json, tipos e papéis. Resolver o subject ID no catálogo (fonte gerada), abrir seu index.md e somente as dependências declaradas.
3. Verificar path existente na árvore do commit e hashes dos documentos exigidos pelo assunto e status. Para informações sensíveis, consultar evento/decisão/verdade de origem, com classificação epistêmica, âmbito temporal, visibilidade e atribuição.
4. Se ID ambíguo, catálogo stale, SHA não encontrado, conflito de autoridades ou permissões insuficientes: BLOCKED com objeto e evidência, não preencher a lacuna com memória.
5. No handoff: fornecer commit completo, IDs, status, gate, procedimento de entrada e paths player-safe. Não copiar segredo nem esconder conflito.

Codex: leitura local de checkout em SHA fixo, parser JSON, busca no catálogo e no índice; validações reproduzíveis e diff exato. ChatGPT Web: conector GitHub fetch refs, trees (paginadas se necessário), fetch_file no SHA fixo, verificações por blob e escrita via create_blob + create_tree (base árvore correta) + create_commit(parent do HEAD esperado) + update_ref(expected_sha e force=false) + readback. Não depender de shell, clone, arquivos temporários ou memória entre chats para o fluxo Web. Se a ferramenta não permitir readback/exigir limitação, status NOT_PUBLISHED ou BLOCKED, nunca declarar commit verificado por inferência.

## Continuidade entre tarefas e fases no Web

DEC-25 condiciona a retirada do chat limpo por fase a controles automáticos comprovados na rota real. Aplicar [continuidade e recuperação](validacao-e-metricas.md#continuidade-no-chatgpt-web--condição-de-dec-25): checkpoint curto no progresso existente, reconciliação com HEAD, fontes decisivas consultadas, validações externas e conclusão vinculada à evidência. Ao detectar divergência, recuperar fontes e corrigir no mesmo chat antes de avançar a unidade dependente. A05 deve verificar quais ações a integração GitHub realmente expõe, inclusive CI; não inferir capacidade Web a partir deste ambiente Codex. DEC-26 aceita o risco residual e define a pausa/renovação excepcional se a recuperação falhar; isso não comprova detector completo nem continuidade ilimitada.

## Escrita segura (proposta futura)
Na mesa, a unidade da transação é a resposta de jogo: texto integral e deltas materiais correspondentes publicados juntos e verificados antes da entrega. Não criar commits intermediários por movimento/teste nem guardar texto entregue somente num buffer de cena. A latência dessa verificação foi aceita em DEC-18. A transação pode alterar os donos e derivados efetivamente afetados, sem cópias concorrentes de estado. Preparação oculta permanece separada do texto destinado ao jogador.

1. Resolver owner, papel e permissão, ler HEAD esperado e as fontes que serão alteradas em um único SHA.
2. Checar precondições do contrato sucessor (permissão efetiva para jogar, autoridade, autoria do PC, epistemic_status, IDs, antes/depois de recursos e ausência de retcon). DEC-02 não admite nova aprovação por cena como rotina; DEC-18 não admite buffer até seu encerramento. Mapear a função preservada de G26/G28 sem reinserir exigências antigas incompatíveis.
3. Compor delta mínimo e identificar a transação. Se já aplicada, conferir o conteúdo/efeito e devolver idempotente; divergência sob o mesmo identificador é STOP_CONFLICT. A identificação não exige evento por ação ou dado.
4. Acrescentar texto ao histórico e atualizar os documentos correntes dos assuntos proprietários e derivados efetivamente afetados. Criar registro adicional só por função necessária; não inserir um arquivo por rolagem ou mudança de relação. Nunca copiar toda a coleção por conveniência.
5. Atualizar índices/catálogo afetados; validar schemas efetivamente usados, referências, segredos, escopo, fontes, consistência de recursos e integridade do texto histórico. Não executar replay universal nem exigir faces dos dados; conferir consequências e estado correspondente (DEC-23/DEC-24).
6. Criar blobs e árvore Git, commit com parent SHA lido; promover ref com expected_sha. Se lease falhar, reler HEAD, classificar conflito e NÃO repetir cegamente. Sem force push.
7. Readback ref, commit, parent, árvore e todos os blobs alterados; validar que se trata do snapshot promovido; distinguir COMMITTED de SNAPSHOT_SYNCED e anotar falhas.
8. Só entregar a resposta de jogo após publicação e readback. Em falha, pausar a continuação ficcional e informar a pendência técnica; não apresentar o texto ainda não persistido como acontecimento confirmado. Se o resultado da publicação for incerto, verificar ref/commit/blobs e o identificador da transação antes de repetir. Retomar da última transação comprovada, preservando escolhas e resultados já existentes, sem rerrolar nem duplicar efeitos. DEC-18 já decide essa cadência; sua implementação futura não está autorizada por esta edição documental.

## Catálogo e cache
catalogo.json é determinístico: {schema_version, generated_from_tree, subjects: [{id,kind,owner,path,visibility,dependencies,source_ids}]}, ordenado por ID e sem texto de GM_HIDDEN. O gerador não lê memory de agente nem timestamps móveis; paths e relações resolvíveis são derivados de índices e arquivos. Em commit candidato: geração em duas passagens (scan e verificação), usando tree SHA sem auto-referência ou hash circular; usar content_index_sha do conjunto de fontes, não o SHA do commit que contém o catálogo. A CI recompõe e compara bytes; qualquer edição manual ou missing dependency falha. Cache é chaveado por commit SHA+subject ID+kind, invalidado quando HEAD muda ou mudou o blob; nunca cachear segredo numa resposta pública. Busca por ID aponta no máximo um owner ativo e retorna NOT_FOUND quando não cadastrado, não faz fuzzy fallback.

## Resiliência e migração
Sincronização entre branches é explícita: B começa de um snapshot novo de master, compara e reconcilia os dois commits divergentes observados ou posteriores, e registra alterações novas antes de prototipar. Evitar merge automático de estado operacional em design. Tags de cutover e pré-cutover servem só como provas históricas para recuperação autorizada de incidente, nunca como rota alternativa de runtime.

## A03 — Sucessão de persistência, histórico e falhas (2026-11-12)

**Estado:** desenho candidato completo para A03; **NÃO OPERACIONAL**. Entrada em `582a627604b4350ec04a3573e272f28885a9e05d`, com A01/A02 já registrados. Este contrato aplica DEC-18/23/24 ao modelo A02, preserva a hierarquia editorial e não faz nenhum write de crônica, cânone, `master` ou runtime. A03 não testa CAS concorrente nem perda de confirmação; essas provas cabem a B04/C03.

### Mapa explícito de sucessão — apenas após aprovação e E

| Regra vigente / fonte | Função que fica preservada | Mudança proposta no sucessor | Limite de autoridade |
|---|---|---|---|
| G19 (inclusive sua sucessão vigente) | Fonte, autoria, delta e readback antes de dizer COMMITTED | **Uma transação verificada por resposta de jogo** em vez de gravações por microação ou somente ao fim da cena, DEC-18 | A fase A não altera G19 em produção |
| G23 e editoração v1.0 | Cânone congelado, prioridade, conflitos e decisão editorial | Mantidos em substância; caminhos estáveis Git não promovem automaticamente `candidate` | Sucessor de política editorial exige aprovação própria |
| G24 / DEC-CR-014 copy-on-write | Histórico intocado, revisões recuperáveis, sem retcon silencioso | Revisão Git de **mesmo caminho corrente** em commit novo; bytes antigos continuam no commit pai/tag | Sem reescrever arquivos canônicos/fechados; não ativar antes de E |
| G26 / DEC-CR-016 (persistência não bloqueante) | Guardar escolhas, estados, autoria e evitar perda/duplicação | **Substituir** continuidade narrativa com buffer não publicado por pausa técnica em falha de transação, DEC-18; recuperação da mesma transação antes de qualquer continuação | G26 permanece vigente no runtime atual; nenhuma narrativa é afetada aqui |
| G28 / DEC-CR-020 (batch ao fim da cena) | Uma transação coerente; consequência, risco, resolução dinâmica e limite de ação do PJ | Trocar **somente a cadência de escrita** para uma transação por resposta; não exigir commit por teste/microação nem novo documento por cena | G28 continua vigente até o cutover autorizado |
| Registros de rolagem/ledger histórico | Consequência, proveniência e coerência mecânica do estado | Sem evento universal, replay obrigatório, face, seed, RNG ou arquivo por dado no sucessor, DEC-23/24 | G25 e as regras V5 de adjudicação continuam; não reexecutar rolagens antigas |
| Ciclos, manifestos e bootstrap atual | Autoridade de estado, origem, permissão de Narrador e retomada | Estado corrente por assunto, fontes Git e três entradas `AGENTS.md`, `CONTEXT.md`, `catalogo.json` após E | Ciclos atuais continuam únicos válidos em master até E |

### Contrato de transação e idempotência — para C03 implementar

**Unidade:** uma resposta ficcional autorizada, composta de texto integral + efeitos materiais e intenções/recursos/conhecimento nos respectivos **owners** + derivados necessários. A preparação prévia e o texto ainda não publicado **não** são eventos jogados. Não incluir resultado de um teste anterior já aplicado, nem antecipar resposta seguinte. Nenhum arquivo extra é obrigatório por evento, turno, teste ou rolagem.

1. **Ler** um commit `base_head` autorizado; verificar papel, documento/owner, versão, fontes decisivas, eventuais aprovações e cursor. Classificar decisões e fatos versus alegações e preparo. Se desconhecidos, bloquear a unidade, sem inferir.
2. **Identificar** transação por `tx_id` estável no checkpoint/metadata de efeito (ou registro mínimo apenas se necessário), e fingerprint determinístico do mesmo conjunto texto+efeitos; o formato final não pode introduzir ledger narrativo por reflexo. Recuperar `tx_id` existente antes de tentar escrever. Mesmo `tx_id` com payload diferente é `STOP_CONFLICT`.
3. **Preparar** deltas somente nos owners afetados; anexar texto original com fonte, manter correção material explícita ligada ao trecho/campo anterior e ao motivo. Atribuição e status epistêmico não se elevam por mera persistência. Gerar apenas derivados afetados, conforme A02.
4. **Validar** mecanicamente campos, IDs, referências, autorização, precedência editorial, fontes, visibilidade, coerência de recursos e continuidade. Preservar texto histórico. Um validador de formato não substitui revisão semântica nem aprovações pendentes.
5. **Publicar atomicamente** blobs e uma única tree Git, commit cujo **pai é `base_head`**, e mover exclusivamente a ref permitida com `expected_sha=base_head`, `force=false`. Criar blob/tree/commit sem mover a ref significa **NÃO PUBLICADO**. Sem fallback Drive, sobrescrita forçada ou atualização do master por rotina.
6. **Reler** ref, parent do commit, tree e blobs correspondentes e comparar `tx_id`, texto e efeitos, além de sigilo. Só `CONFIRMED` após a confirmação remota inequívoca. A resposta de jogo só então pode ser entregue.
7. **Em falha ou confirmação perdida**, congelar a continuação ficcional e classificar `PENDING_PERSISTENCE`; primeiro recuperar ref/commits/owners e comparar `tx_id`/fingerprint. Se o commit foi publicado, confirmar a transação **existente**, sem duplicá-la. Se não foi publicado, reconciliar com novos commits remotos antes de qualquer nova tentativa. Nunca rerrolar, atribuir nova decisão ao PJ ou restaurar recursos por conveniência.

**Estados técnicos possíveis:** `PREPARED_LOCAL` (nenhum efeito operacional), `COMMIT_OBJECT_CREATED_UNPUBLISHED` (objetos órfãos possíveis), `REF_UPDATED_READBACK_PENDING` (não declarar confirmado), `CONFIRMED` (ref+commit+owners efetivamente verificados), `STOP_CONFLICT` (mesmo ID/delta divergente, owner/fonte conflitante ou lease concorrente), `PENDING_PERSISTENCE` (não existe prova de confirmação suficiente para entregar a ficção). O rótulo nunca substitui a leitura real do repositório.

### Exercícios negativos exigidos na implementação

- **Stale lease remoto:** dois escritores iniciam do mesmo parent numa ref descartável; só um pode promover. O segundo deve receber rejeição e preservar seu delta para reconciliação. `update_ref` sem disputa prova somente sucesso normal, não rejeição.
- **Confirmação perdida:** o servidor publicou, mas a resposta de confirmação se perdeu; recuperação encontra `tx_id` e os exatos efeitos já vigentes, sem segundo commit narrativo.
- **Mesmo ID, outro conteúdo:** corrigir a intenção do jogador em uma tentativa não autorizada deve parar, não sobrescrever texto.
- **Preparo versus acontecimento:** referência `GM_PREPARED` ou cena não iniciada não gera evento, XP ou conhecimento por mudança de arquivo.
- **Rollback incidental:** editar estado atual não pode apagar texto histórico, mudar aprovação ou desfazer recursos sem correção identificável.
- **Blob e tree não promovidos:** criá-los não equivale a escrita no HEAD. Falha ou versão divergente exige readback antes de qualquer novo commit.
- **Fato só na prosa:** buscar fonte original e materializar consequência somente ao ganhar relevância (A02), com conhecimento/tempo conservados.
- **Fonte externa sem integridade:** não inventar hash para arquivos do Drive, nem reclassificar canon por arquivo copiado.

### Separação entre história, estado e revisão

- **História literal:** preservar fontes jogadas e decisões anteriores; conteúdo existente não é sintetizado como transcrição ausente. Referência histórica pode apontar a commit antigo, jamais virar rota operacional de fallback após E.
- **Estado corrente:** só o owner do campo guarda a situação atual; não depende de replay de eventos; discrepância entre ele e a prosa pede reconciliação auditável de fontes, sem harmonização silenciosa.
- **Correções:** manter marcador identificável no owner/registros necessários que explica fonte, escopo, decisão, efeito e anterioridade; não editar o texto histórico para parecer que sempre esteve corrigido.
- **Sucessões:** propostas de G19/G23/G24/G26/G28, contrato Git e governança editorial precisam de política sucessora expressamente autorizada antes de operação; A03 define consequências, não as aprova nem congela.

**Provas desta etapa:** alterações documentais verificadas no GitHub por SHA/bytes, sem ativação. **Não provados:** endpoint remoto rejeitar stale, recuperação pós-perda de confirmação, performance por resposta, sigilo contextual e compatibilidade executada Web/Codex; mantidos como deveres de B04/C03/C07. Próximas A04 e A05; A06 depende das duas.

## A05 — Contratos Web/Codex e continuidade com prova de capacidade (2026-11-12)

**Estado:** A05 especificação concluída, implementação/ensaios C e B ainda não. Entrada `0298e4837bf9a304857837c5639b2c74fc5a729b` no mesmo ramo candidato. Os comportamentos testados abaixo são resultados reais do **ChatGPT Web + conector GitHub desta execução**; não são atribuídos ao Codex. A continuidade por fase de DEC-25 continua condicionada a prova B/C, e DEC-26 exige handoff quando a base não puder ser reconciliada.

### Interface lógica única (sem exigir tecnologia idêntica)

`resolve(subject_id, revision, role, purpose)`: entrada `{repo,branch,expected_head?,commit_sha,subject_id,role,visibility_ceiling}`. Fixar ref no início, ler **somente** `AGENTS.md`, `CONTEXT.md`, `catalogo.json` após E (antes de E: bootstrap pinado operacional antigo para a mesa; em A–D: documentação candidata explicitamente selecionada). Procurar subject ID por igualdade exata no catálogo daquela árvore, um owner; retornar `{snapshot_sha,subject_id,owner_path,files:[{path,blob_sha}],source_locators,epistemic_scope}`. Em `NOT_FOUND` ou ID ambíguo: erro explícito, sem aproximação, Git histórico como fallback ou inventar fonte.

`read_selected(snapshot_sha, paths[], actor_scope)`: conferir cada path contra a tree do **mesmo commit**, blob correspondente e fonte/tempo/ator, aplicar política de **divulgação** adequada à resposta. Acesso técnico a GM_HIDDEN por papel autorizado não significa que esse conteúdo deve ir a um output público. Conteúdo não localizado ou não sustentado: `UNKNOWN`/`NOT_FOUND`, nunca `CONFIRMED`.

`commit_transaction(expected_head,tx_id,changes[],authority)`: preparar deltas em owners existentes, verificar autorização+schema+fonte e `tx_id`; publicar **uma tree e um commit** cujo pai é `expected_head`; `update_ref(expected_sha=expected_head, force=false)`; recuperar ref/commit/tree/changed blobs e reconciliar `tx_id` e efeitos. Retornar `{status,commit_sha,tree_sha,base_head,changed_blobs,readback}` apenas se a publicação foi confirmada; resultados incertos retornam `PENDING_PERSISTENCE`. Nunca ocultar o fato de que create_blob/tree/commit sem update_ref não publicou a branch.

`resume(checkpoint)`: `{task_id,branch,source_commit,source_refs,decisions_applied,outputs,tests,limit,next_step}` é registro no backlog existente, não substituto da consulta Git. Readback da ref atual e referências; `HEAD_DIFFERENT` requer comparação/reconciliação e reprova afirmações de conclusão stale. Caso divergência sem base confiável, pausar apenas a unidade afetada e fornecer handoff PLAYER_SAFE (DEC-26). Evitar refazer etapas já confirmadas ou reabrir decisões aceitas.

### Mapeamento por canal e capacidades verificadas

| Capacidade | ChatGPT Web nesta execução | Codex | Prova / cautela |
|---|---|---|---|
| Repositório privado e identidade | **COMPROVADO:** `get_repo`, `get_user_login`, `pull=true`, `push=true`; ref design lida | **NÃO EXERCITADO** neste canal | Permissão do repo não certifica proteção administrativa efetiva de branch |
| Leitura fixada por SHA, diretório/tree e blob | **COMPROVADO:** `fetch_file(ref=SHA)`, REST `/git/trees/{sha}?recursive=1` não truncada, blob hash, `compare_commits` | **NÃO EXERCITADO** | Para árvore grande, paginar/inventariar se a resposta truncar; validar path e hash |
| Escrita múltipla atômica e readback | **COMPROVADO no ramo autorizado:** `create_blob`, `create_tree(base_tree_sha)`, `create_commit(parent_sha)`, `update_ref(expected_sha,force=false)` e readback; commits A01–A03 | **NÃO EXERCITADO** | Sucesso sem disputa não prova rejeição de SHA stale; B04 deve provar isso em ref descartável |
| Consulta de CI/Actions | **COMPROVADA API GET:** consultas a `/actions/runs`, `/commits/{sha}/check-runs`, statuses e acesso a jobs/logs pela integração | **NÃO EXERCITADO** | No commit de entrada de A05, `0298e48`, **0 workflow runs, 0 check-runs e 0 statuses** retornados; CI do plano não foi executado |
| Disparo/edição de workflow, shell/clone local ou métricas HTTP/tokens | **NÃO COMPROVADO:** não há ferramenta GitHub de execução de shell nem autorização de presumir disparo manual de workflow; contadores HTTP/tokens não expostos por esse conector | **NÃO EXERCITADO** | Em Web `NOT_OBSERVABLE` só para bytes HTTP/tokens reais conforme DEC-19. CI pode ocorrer via workflow GitHub após commit, mas não afirmar que ocorreu sem run ID |
| Proteção de branch e concorrência | `expected_sha` aplicado em updates normais; proteção admin/ruleset ainda não inspecionada nem rejeição negativa executada | **NÃO EXERCITADO** | B04/C03 devem testar stale ref, confirmação perdida e corrida em sandbox; E verifica ruleset real |

**Regra vigente após DEC-27:** testar ID/commit/fonte, erro/stop e readback no fluxo realmente destinado ao uso. A tabela acima preserva o levantamento histórico por produto, mas não cria dois gates. Evidência anterior continua válida quando código, fontes, contrato e integração relevante não mudaram; prova extra de Codex ou Web somente por diferença concreta. Não usar memória de chat como autoridade nem misturar refs de master e design.

### Diagnósticos observáveis e reação

| Código | Condição | Ação |
|---|---|---|
| `NOT_FOUND` | ID/path não localizado no snapshot fixo | Parar consulta afetada e informar ausência; sem fuzzy fallback |
| `STALE_HEAD` | Branch HEAD mudou antes de publicar | Não promover; reler, comparar e reconciliar explicitamente |
| `HASH_MISMATCH` | Path existe mas blob difere do pin | Bloquear fato/etapa afetados; recuperação pela fonte correta |
| `AUTHORITY_CONFLICT` | Dois owners ou canon/política divergentes | Registrar CONFLICT, nenhuma fusão silenciosa |
| `KNOWLEDGE_LEAK_RISK` | Informação de agente não autorizada para divulgação | Bloquear output público e rever escopo/ator |
| `UNVERIFIED_WRITE` | Falha de atualização/readback ou resposta perdida | Consultar branch/commit/tx antes de repetir; `PENDING_PERSISTENCE` |
| `EVIDENCE_MISSING` | PASS alegado sem CI/commit/readback quando exigido | Gate não passa; manter dependentes bloqueados |
| `RECOVERY_FAILED` | Fontes ou checkpoint incoerentes após tentativa explícita | Pausar unidade, handoff com refs e limites (DEC-26) |

### Checkpoint e condição de DEC-25

Ao começar cada tarefa, **automaticamente onde possível**: (1) fetch HEAD, (2) recuperar linha da tarefa/backlog e decisões DEC pertinentes, (3) ler fontes exatas e validar SHA, (4) checar dependências/gates, (5) antes de escrever repetir HEAD/lease, (6) após escrever fazer readback de HEAD, commit/parent, blobs, status e CI quando exigido, (7) registrar checkpoint curto. Os passos objetivamente verificáveis podem virar validadores em C; a presente execução é ferramenta-orquestrada e **não certifica um detector semântico universal**. B03/B04/C07 devem demonstrar falha induzida: fonte inexistente, fonte presente que não sustenta conclusão, decisão antiga, checkpoint stale, falsa conclusão e recuperação na mesma conversa; incluir caso estruturalmente válido mas semanticamente falso. Comparação não deve expor informações GM_HIDDEN no relatório.

**Limites atuais:** o Web já prova escrita/readback de documentação candidata. Nenhuma prova aqui demonstra recuperação de erro injetado, resiliência em sessão longa, medição de tokens ou equivalência com Codex. Portanto **DEC-25 AINDA NÃO SATISFEITA** para dispensar troca de chat por fase. Se o chat perder contexto recuperável, DEC-26 prevalece. A05 não concede PASS a B/C nem cutover.
