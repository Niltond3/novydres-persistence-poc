# Agente Mapwork — inicialização

1. Ler `novydres/AGENTS.md` e recuperar HEAD, cânone, estado e referências
   pela integração GitHub. O cânone e a U02 são imutáveis sem decisão explícita.
2. Ler `PIPELINE.md` e `WEB_RUNTIME.md`. Carregar somente os critérios
   da etapa atual em `docs/infra-acceptance.md` e `VISUAL_REVIEW_PROTOCOL.md`.
3. Chamar exclusivamente `scripts/pipeline.py run`, diretamente ou por
   `scripts/web_bridge.py:run_web`. Seguir `next_action` até aceite verificável
   ou impedimento legítimo, persistindo cada candidata.
4. Pesquisar analogias reais, preservar decisões aprovadas, perguntar apenas
   a respeito de novos elementos/conflitos editoriais e da composição final.
5. Não falsificar ferramentas, imagens, auditorias ou estado. GitHub guarda
   código, decisões e checkpoints; Drive guarda bytes de imagens e artefatos.

A transição para geração depende dos aceites auditados INF-01 a URB-08,
com hash do contrato Markdown, ledger e checkpoint reconciliados.
Referências visuais e aprovações históricas da U02 não são gates operacionais.
