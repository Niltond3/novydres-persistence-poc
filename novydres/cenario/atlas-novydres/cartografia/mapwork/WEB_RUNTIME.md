# Executor ChatGPT Web

O adaptador `scripts/web_bridge.py:run_web` somente verifica o transporte
de código e invoca **em processo** `scripts/pipeline.py:main` sem terminal,
Git CLI ou rede Python. Não executa geração de imagens nem possui decisões
urbanísticas próprias.

1. Pelo conector GitHub, recuperar HEAD, árvore/blobs e contratos operacionais.
   O HEAD da branch é referência de implementação, `master` é fonte de cânone.
2. Pelo conector Google Drive, recuperar cache de código, U02 e arquivos de
   candidatas em `NOVYDRES_MAPWORK_ASSETS`; verificar SHA-256 local,
   Git blob SHA e que o cache corresponde à árvore efetivamente lida no GitHub.
   Cache divergente deve ser reconstruído; nunca usado como autoridade.
3. Materializar no Python os bytes reais; usar `web_bridge.verify_files`
   e `run_web(argv=[...], file_manifest=..., root=..., source_commit=..., remote_blobs=...)`.
   `remote_blobs` é mapa independente `caminho → Git blob SHA` da árvore do
   commit lida **pelo conector GitHub**; não aceitar cópia dos SHA do próprio
   manifesto como prova de origem. Todos os `.py` locais, inclusive transitivos,
   devem estar presentes e verificados. Recusar módulos Python pré-carregados
   sem selo da mesma revisão e ZIP com arquivo faltante, extra ou duplicado.
   O Python não tem conexão direta ao GitHub/Drive; ações remotas cabem ao agente.
4. Autonomia Web: passar --host-branch, --host-head inicial e
   --host-journal-path=sessions/<arquivo>.json, deixando
   web_bridge injetar --source-commit. Seguir SYNC_PENDING_JOURNAL,
   COMPLETE_OPERATION, SYNC_COMPLETED_JOURNAL e ACK_COMPLETE, conforme
   PIPELINE.md. O host usa o conector GitHub com CAS e GET de ref, commit,
   tree e blob; imagens passam pelo Google Drive e GET de bytes.
5. Na retomada reler journal GitHub, operação original e artefatos por
   GET independente. Não reiniciar uma operação com novo ID. FAIL corrigível
   exige correção material e reentrada na mesma pipeline; sem canonização.

**Limite verificável:** SHA prova identidade dos bytes; um parecer vinculado
prova documentação de inspeção, não a veracidade da avaliação semântica da LLM.
Nunca declarar imagem, transferência, correção ou aceitação que não ocorreu.

## Retomada fria obrigatória

Uma cópia local de `sessions/*.json` **não** é prova de sincronização. Em
outro processo ChatGPT Web, obtenha novamente pelo conector GitHub a ref da
branch, o commit que escreveu o journal, seu pai, sua árvore, o Git blob
exatamente em `sessions/...` e os bytes desse blob. Materialize o journal
em caminho novo e o GET em **outro** arquivo. Verifique também a árvore de
código no `source_commit` fixado na sessão e todo artefato anterior por GET
de GitHub/Drive, em arquivos distintos dos locais. Não herde os caminhos
absolutos `/mnt/data` da sessão antiga.

Passe `--host-recovery <arquivo.json>` junto da chamada normal, sem trocar
`--host-head` inicial pelo HEAD novo. O arquivo é materializado pelo host:

```json
{
  "schema": "NOVYDRES_MAPWORK_COLD_RECOVERY",
  "branch": "<branch-fixada>",
  "journal_repo_path": "sessions/<journal>.json",
  "source_commit": "<commit-fixado-da-implementacao>",
  "initial_head": "<HEAD-original-da-sessao>",
  "journal_readback_path": "<arquivo-distinto-de-GET-do-GitHub>",
  "journal_commit": {
    "branch": "<branch-fixada>",
    "repo_path": "sessions/<journal>.json",
    "head": "<commit-que-gravou-journal>",
    "ref_head": "<commit-que-gravou-journal>",
    "commit_sha": "<commit-que-gravou-journal>",
    "commit_parent": "<lease-da-ultima-operacao>",
    "tree_blob_sha": "<blob-da-arvore-do-commit>",
    "blob_sha": "<blob-do-journal>"
  },
  "current_ref_head": "<HEAD-atual-obtido-por-GET>",
  "head_chain": [],
  "artifact_readbacks": []
}
```

`head_chain` lista os commits efetivamente inspecionados entre o commit do
journal e o HEAD atual, na ordem: `{parent, head, commit_sha,
journal_blob_sha}`. A cadeia precisa preservar o blob do journal.
`artifact_readbacks` precisa cobrir **todos** os artefatos concluídos,
com `{original_path, materialized_path, readback_path, provider, remote_id,
sha256}`. Cada readback é um GET real separado; uma resposta de upload não
pode preencher o campo. O módulo valida bytes, hash, vínculos e cadeia;
a autenticidade das chamadas é responsabilidade do host conectado.

Se `head_chain` não estiver vazia, a pipeline devolve
`RECONCILE_RECOVERED_REMOTE_WRITES` sem repetir upload/ação. A
reconciliação de uploads já realizados aceita `COMPLETE_OPERATION` do
`operation_id` original **somente** quando todo `head_chain[]` atribui
cada commit àquela operação e confronta `{parent, head, files}` com
`result.github_commits[]`, além dos bytes baixados dos provedores.
Em caso de conflito de autoria, rejeite o recibo: um commit concorrente
não pode ser apropriado como execução da operação. Com journal PENDING e HEAD ainda no seu commit, a resposta é
`EXECUTE_RECOVERED_PENDING_OPERATION`: reutilize `operation_id` e
`pending_sync` do commit verificado. Com journal COMPLETED e confirmação
ainda pendente, `ACK_RECOVERED_COMPLETED_JOURNAL`: faça os GETs finais e
confirme, sem escrever segundo commit de conclusão.

Os caminhos históricos continuam inalterados no journal hash-chain;
`artifact_readbacks` remapeia apenas argumentos referenciados por bytes
reverificados. Diretórios ou caminhos sem artefato verificável continuam
bloqueados até reconstrução explícita, nunca substituição automática.

O transporte real GitHub Actions ZIP → conector Google Drive → GET do Drive
foi demonstrado em `sessions/host-io-transport-evidence.json`. Esse ZIP
é apenas um cache técnico opcional: **GitHub Actions não é requisito de
execução**. O teste não constitui demonstração de imagem nativa, classificação
visual, nem conclusão do ciclo autônomo.

## Conversão operacional do retorno de conectores

Após cada operação externa do ChatGPT Web, usar
`web_bridge.materialize_host_exchange(operation=..., pending_sync=...,
provider_results=..., github_commits=..., arg_updates=..., output_path=...)`
para montar automaticamente o JSON de `--host-exchange`. O mesmo
`operation_id` emitido pela entrada canônica deve ser mantido. O adaptador
é **puro**: não chama conectores e não cria uma pipeline alternativa.

Cada `provider_results[]` recebe `provider`, `path` (bytes originais),
`readback_path` (outro arquivo produzido por um GET real),
`upload` (resposta do provedor), `readback` (metadados do GET) e
`kind` opcional. GitHub exige também `repo_path`, `upload.sha` e
`readback.sha`. Drive exige `upload.success=true`,
`upload.id=readback.id`. O adaptador extrai `remote_id`,
Git blob e SHA-256 dos bytes reais em vez de aceitar hashes de recibos
montados à mão. Geração exige PNG verdadeiro e inspeção visual separada;
o controlador original faz as demais verificações.

**Prova de transporte real:** a geração nativa produziu
`mapwork-noncanon-native-io-test-20261121.png` (1536×1024,
3.727.755 bytes, SHA-256
`c00f079f312be5b987f24a3546df9ca73e761273975ca3dbbff0ff7baf7166cd`);
o conector Google Drive aceitou o arquivo
`1oC3mcjsYmQzqdAa3--rqfNDOCYlPCxf2` e um GET independente
materializou bytes idênticos. Foi montada e validada no controlador uma
troca técnica contendo esta imagem e um parecer visual FAIL vinculado ao
mesmo hash, armazenado em
`sessions/agent3-native-image-review.json`. A troca foi um
**ensaio de transporte**, não um journal CAS remoto concluído nem um
aceite de INF-01. Não imputar a este ensaio a passagem de gates.
A pesquisa técnica em duas fontes reais está em
`sessions/agent3-technical-research.json`, sem efeito editorial.

Esta sessão não demonstrou retomada em outra conversa nem execução
completa de pesquisa → classificação → topologia → geração → reprovação
→ correção → replanejamento → aceite. Não transferir ao Agente 4
enquanto esses passos não ocorrerem no próprio controlador com
recibos de ferramentas reais e nova evidência material.

## Troca controlada da revisão executável durante ensaio sintético

Um journal recuperado preserva seu `source_commit` histórico. Quando há nova
implementação da pipeline, `web_bridge.run_web` exige verificação completa dos
Git blobs na **revisão executável nova** e rejeita divergência da referência
do journal por padrão. A exceção restringe-se a `--synthetic-trial` com
`--host-recovery` e `--host-runtime-upgrade-proof`; não é permitida com U02,
renderizador canônico, `--execute`, assets ou zona real.

O host deve consultar separadamente a comparação GitHub entre a revisão
histórica e a revisão executável e persistir a prova:

```json
{
  "schema": "NOVYDRES_MAPWORK_SYNTHETIC_RUNTIME_UPGRADE",
  "test_only": true,
  "journal_sha256": "<sha256-do-journal-existente>",
  "journal_source_commit": "<commit-historico-imutavel>",
  "runtime_source_commit": "<commit-novo-verificado>",
  "branch": "<branch-do-journal>",
  "journal_repo_path": "sessions/<journal>.json",
  "github_compare": {
    "base": "<commit-historico-imutavel>",
    "head": "<commit-novo-verificado>",
    "status": "ahead",
    "ahead_by": 1
  }
}
```

`ahead_by` precisa refletir a leitura real do conector GitHub. Este JSON não
substitui essa leitura nem validação dos blobs; só vincula os resultados ao
mesmo journal e à fixture sintética. A referência histórica e os
`operation_id` não são alterados. A troca da implementação não valida,
conclui ou repete a operação pendente por si só.

## Geração nativa com referência realmente visível

O Web host entrega PNGs materializados por GETs do Google Drive ao ChatGPT
Images **como entradas visuais**, não somente como caminhos, URLs, hashes ou
visualizações anteriores. Para operações nativas a troca contém seis
artefatos: `reference-image`, `edit-mask`, `image` (saída bruta),
`composed-image` (saída mascarada), `native-edit-handoff` e
`visual-review`. O `web_bridge.materialize_host_exchange` transporta
todos esses tipos por bytes locais e readback, sem simular conectores.

`native_generation.verify_handoff` valida a identidade da referência,
máscara, pedido, `generation_id` da resposta real, arquivos e observação
`visual_input_evidence`. O ChatGPT Web não oferece os campos internos
`dispatch.attached_inputs` nem um parâmetro programático de máscara
equivalente ao da API; não os invente. O `visual_input_evidence` é uma
atestação do host, não um selo criptográfico de anexo. Na ausência de entrada
real, a operação permanece `PENDING` por bloqueio de capacidade.

A composição é determinística e independente da geração; nunca escalar
automaticamente resultado desalinhado. O código verifica também os pixels
externos e o conteúdo recomposto relido do Drive. A avaliação semântica
permanece tarefa do agente, com imagens acessíveis e observações concretas.
O `edit_op` da ferramenta não determina PASS/FAIL por si só. Não se completa
uma operação somente porque o CI, o checksum ou um relatório visual disse
`PASS` sem vínculo com a imagem corrigida. O journal não é reescrito.

Os comandos de preparação, máscara de reparo e composição continuam
subetapas da entrada `scripts/pipeline.py run`: não há pipeline paralela,
API externa nem necessidade de GitHub Actions para execução no Web.
