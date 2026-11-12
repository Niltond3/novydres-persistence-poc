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

## Leitura idêntica por duas ferramentas
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
