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
