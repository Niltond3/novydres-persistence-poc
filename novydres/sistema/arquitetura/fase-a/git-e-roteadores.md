---
id: arch-phase-a-git-and-routers
status: CANDIDATO_PENDENTE_APROVACAO
scope: NOVYDRES_GLOBAL
classification: PLAYER_SAFE
---
# Git-native, concorrência e roteadores Web/Codex

## Modelo de revisão e autoridade
A versão operacional é uma árvore de commit única; SHA do commit define snapshot e blob SHA define identidade de bytes. O catálogo, índices, projeções, árvore de assuntos e os metadados do commit integram UMA transação candidata. Nenhuma mudança de HEAD nem fonte autoritativa decorre da gravação de blob isolado. Git não fornece imutabilidade jurídica/absoluta: configurar branch protection/ruleset, impedir non-fast-forward/delete de arquivos de registros e preservar refs de checkpoints; o validador detecta violação, sem afirmar proteção que não foi instalada.

Escrita sob ADR será habilitada apenas após E e aprovação de sucessores. Não modificar o significado histórico de G24/DEC-CR-014 durante A–D; manter a antiga regra copy-on-write na operação corrente. O sucessor propõe que criação de novo commit com caminho corrente estável é o COW lógico, com commit predecessor recuperável. Os registros imutáveis permanecem arquivos distintos. Essa mudança precisa aprovação editorial/jogador documentada no cutover.

## Leitura idêntica por duas ferramentas
1. Fixar repo, branch permitida, HEAD SHA lido por ref. Se operação de runtime antes da E: usar discovery atual, nunca o layout de candidato.
2. Depois da E: abrir AGENTS.md e CONTEXT.md naquele commit; estes retornam catalogo.json, tipos e papéis. Resolver o subject ID no catálogo (fonte gerada), abrir seu index.md e somente as dependências declaradas.
3. Verificar path existente na árvore do commit e hashes dos documentos exigidos pelo assunto e status. Para informações sensíveis, consultar evento/decisão/verdade de origem, com classificação epistêmica, âmbito temporal, visibilidade e atribuição.
4. Se ID ambíguo, catálogo stale, SHA não encontrado, conflito de autoridades ou permissões insuficientes: BLOCKED com objeto e evidência, não preencher a lacuna com memória.
5. No handoff: fornecer commit completo, IDs, status, gate, procedimento de entrada e paths player-safe. Não copiar segredo nem esconder conflito.

Codex: leitura local de checkout em SHA fixo, parser JSON, busca no catálogo e no índice; validações reproduzíveis e diff exato. ChatGPT Web: conector GitHub fetch refs, trees (paginadas se necessário), fetch_file no SHA fixo, verificações por blob e escrita via create_blob + create_tree (base árvore correta) + create_commit(parent do HEAD esperado) + update_ref(expected_sha e force=false) + readback. Não depender de shell, clone, arquivos temporários ou memória entre chats para o fluxo Web. Se a ferramenta não permitir readback/exigir limitação, status NOT_PUBLISHED ou BLOCKED, nunca declarar commit verificado por inferência.

## Escrita segura (proposta futura)
1. Resolver owner, papel e permissão, ler HEAD esperado e as fontes que serão alteradas em um único SHA.
2. Checar precondições (gates de cena, aprovação, autoridade, autoria do PC, epistemic_status, IDs, antes/depois de recursos, conclusão G28, G26 buffer, sem retcon).
3. Compor delta mínimo. Se registro já existir, comparar byte SHA e conteúdo; se idêntico devolver idempotente, se divergente STOP_CONFLICT.
4. Inserir apenas novos arquivos de registro; atualizar somente documentos correntes do subject proprietário e derivados determinados (catálogo, estado, ciclo, ponteiros); nunca copiar toda a coleção por conveniência.
5. Regerar projeções do commit candidato, validar schemas, links, tipos, referências, segredos, escopo, regra de fonte, diff de eventos e a integridade dos registros históricos.
6. Criar blobs e árvore Git, commit com parent SHA lido; promover ref com expected_sha. Se lease falhar, reler HEAD, classificar conflito e NÃO repetir cegamente. Sem force push.
7. Readback ref, commit, parent, árvore e todos os blobs alterados; validar que se trata do snapshot promovido; distinguir COMMITTED de SNAPSHOT_SYNCED e anotar falhas.
8. Se publicação falhar para evento narrativo, preservar G26/G28 atuais; este documento não redefine buffer, turnos ou retomada. Mudança de cadência somente por autorização separada.

## Catálogo e cache
catalogo.json é determinístico: {schema_version, generated_from_tree, subjects: [{id,kind,owner,path,visibility,dependencies,source_ids}]}, ordenado por ID e sem texto de GM_HIDDEN. O gerador não lê memory de agente nem timestamps móveis; paths e relações resolvíveis são derivados de índices e arquivos. Em commit candidato: geração em duas passagens (scan e verificação), usando tree SHA sem auto-referência ou hash circular; usar content_index_sha do conjunto de fontes, não o SHA do commit que contém o catálogo. A CI recompõe e compara bytes; qualquer edição manual ou missing dependency falha. Cache é chaveado por commit SHA+subject ID+kind, invalidado quando HEAD muda ou mudou o blob; nunca cachear segredo numa resposta pública. Busca por ID aponta no máximo um owner ativo e retorna NOT_FOUND quando não cadastrado, não faz fuzzy fallback.

## Resiliência e migração
Sincronização entre branches é explícita: B começa de um snapshot novo de master, compara e reconcilia os dois commits divergentes observados ou posteriores, e registra alterações novas antes de prototipar. Evitar merge automático de estado operacional em design. Tags de cutover e pré-cutover servem só como provas históricas para recuperação autorizada de incidente, nunca como rota alternativa de runtime.
