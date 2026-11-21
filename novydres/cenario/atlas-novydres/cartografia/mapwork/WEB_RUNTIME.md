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
   e `run_web(argv=[...], file_manifest=..., root=..., source_commit=...)`.
   O Python não tem conexão direta ao GitHub/Drive; ações remotas cabem ao agente.
4. Após cada ação, gravar/consultar recibos pelo conector e confirmar SHA
   por download. Para Git, usar escrita CAS com HEAD esperado, reler commit
   e blob e jamais descartar mudanças concorrentes. Drive armazena imagens;
   GitHub mantém links, hashes, estados, tentativas e checkpoints.
5. Em `FAIL`, executar `next_action` e repetir a entrada na mesma sessão;
   em interrupção operacional, persistir checkpoint e restaurar em novo chat.
   Não transferir erro técnico corrigível ao proprietário.

**Limite verificável:** SHA prova identidade dos bytes; um parecer vinculado
prova documentação de inspeção, não a veracidade da avaliação semântica da LLM.
Nunca declarar imagem, transferência, correção ou aceitação que não ocorreu.
