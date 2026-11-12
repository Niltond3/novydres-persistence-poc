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
