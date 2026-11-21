# Mapwork V3.3 — executor ChatGPT Web, mesmo pipeline

**Status:** mecanismo Web de transporte/execução validado; produção artística E2E **ainda BLOQUEADA**. Nenhum PASS de infraestrutura, nenhum lote/POI, nenhuma mudança do cânone ou U02.

## Autoridades e ferramentas

- **GitHub:** fonte única de código, Markdown, decisões, checkpoints e hashes dos arquivos versionados. O `master` é autoridade do cânone; esta branch contém implementação *candidata*.
- **Google Drive:** fonte dos bytes privados (U02, imagens, máscaras, assets, snapshots de transporte). O snapshot de código no Drive é **cache**, nunca fonte de verdade; comparar o Git blob SHA de **cada arquivo** com o tree do commit remoto antes da execução. Se um único blob divergir, `BLOCKED`; refazer materialização pelo conector, nunca substituir código silenciosamente.
- **Python executável no ChatGPT Web:** apenas validações/detecção/composição locais, sem CLI, `git clone`, `subprocess` ou internet no interpretador.
- **Agente:** interpretação de Markdown, pesquisa e revisão efetiva das imagens usando pixels visíveis. O script não pode decidir estética nem inventar prova de invocação de ferramenta.

## Entrada canônica

O único motor permanece `scripts/pipeline.py` (no diretório `novydres/cenario/atlas-novydres/cartografia/mapwork-v3`). `scripts/v33_web_bridge.py` é **adaptador de transporte**, não uma segunda pipeline: `run_web` chama **a mesma `pipeline.main(['run',...])` dentro do processo Python**.

Em um chat limpo, sem terminal:

1. Ler este arquivo, `AGENT.md`, `PIPELINE.md`, `docs/infra-acceptance-v33.md`, `config.json`, `world-state.json` e o checkpoint mais recente pelo GitHub; recuperar `master` para autoridades canônicas. Confirmar HEAD e `git/trees/<sha>?recursive=1` pelo conector GitHub.
2. Pelo conector Google Drive, baixar o cache `mapwork-v33-web-runtime-source.zip` do diretório `NOVYDRES_MAPWORK_V3_ASSETS`; isso cria um arquivo real montado no runtime. Extrair no Python usando `v33_web_bridge.extract_verified_zip` ou a API padrão `zipfile`, jamais executar shell. Carregar `bundle-manifest.json`; verificar SHA-256 de todos os arquivos **e** o Git blob SHA de todos contra a árvore atual. Em caso de atualização de código, reconstruir o cache a partir dos arquivos atuais do GitHub via conector, e conferir novamente; não confiar no cache desatualizado.
3. Pelo Google Drive recuperar `U02_APPROVED_REFERENCE.png` com ID `1PrfWEcD07Gz5eX5r2qKGaRlecixVKh6r`: SHA-256 `9d55965f45181e3b943552e32df0e8ad41b63c8974ffd6e670f447ffd36eb9a0`, 1448×1086. Verificar bytes reais com Python/Pillow. Recuperar máscaras e assets necessários pelo ID e SHA; arquivos de retorno da ferramenta têm que aparecer no diretório de trabalho.
4. Realizar de verdade GitHub read/write readback, pesquisa Web e entrega de arquivo; gerar `capabilities.json` com `proof.local_path`, `proof.sha256` e, para Github, `proof.blob_sha`/`commit_sha`/`readback`. **A estrutura JSON por si só NÃO autentica a chamada remota:** host deve confrontar a resposta real dos conectores. Não declarar capacidades futuras de imagem como disponíveis sem gerar e reabrir pixels.
5. No Python, importar `scripts/v33_web_bridge.py` e chamar `run_web(argv=["--intent", ... , "--scope-index", ..., "--capabilities", ..., "--research-file", ..., "--decisions-file", ..., "--inventory-file", ..., "--acceptance-ledger", ..., "--reference", <caminho U02 real>, "--checkpoint", ...], file_manifest=<manifest verificado>, root=<mapwork-v3 extraído>, source_commit=<SHA do snapshot também verificado pelo GitHub>)`. **Nunca chamar outra pipeline**. O argumento `--district kingswell` sem intent serve somente como diagnóstico compatível legado.
6. Ler o JSON retornado. `PASS`: exclusivamente gate com provas técnicas válidas e aprovação semântica vinculada; `FAIL`: candidata inválida/obsoleta/fraudulenta, corrigir e validar de novo; `BLOCKED`: pré-requisito/capacidade/candidato legítimo ausente; `CHECKPOINT`: somente progresso, não aprovação; `READY_FOR_OWNER_REVIEW`: revisão final requerida, não publicação. Nenhuma saída da execução Web autoriza alteração canônica por si.
7. Na infraestrutura, respeitar a ordem `INF-01..INF-07` + `URB-08`. Cada candidata tem PNG integral, máscara binária, geometria estruturada, SHA de U02, SHA do estágio anterior, auditoria matemática independente e observações visuais regionais ligadas ao hash dos pixels reais. Texto `PASS` do agente sem bytes/observações => `FAIL`. Cruzamentos, níveis e modais precisam coexistir em rede cumulativa. Repetição sem progresso => replanejar. Não avançar lotes nem POIs sem aprovação integral das etapas previstas.
8. Persistir tentativa e checkpoint no GitHub com compare-and-swap e readback do blob; armazenar PNGs/máscaras/tiles no Google Drive e reabrir para conferir SHA; registrar IDs de Drive reais nos recibos. Interrupção: recuperar último checkpoint e comparar os hashes de todas as entradas. Divergência => revalidar, nunca marcar PASS por relato antigo.
9. Fazer inspeção visual real e separada do código; o script comprova que as observações se vinculam à imagem, mas **não pode provar criptograficamente que o modelo examinou semanticamente a imagem**. Isso continua dever do agente; uma verificação semântica independente pode ser necessária para homologação. A publicação de arte requer ANTES/DEPOIS real, aprovação explícita e readback.

## Evidências deste corte

- Repositório: auditoria `WEB_EXECUTION_AUDIT_20261120.md` e código/testes em branch candidata.
- Python no chat, sem shell: 10 blobs Git verificados, execução da entrada oficial com U02 montada, resultado `BLOCKED` em `INF-01`, `allows_lots:false`, nenhuma edição canônica.
- Transferência Google Drive → Python e Python → Google Drive → Python: U02, máscara de diagnóstico e sobreposição R2 com SHA idênticos. O diagnóstico R2 tem 98 vias, **não** possui topologia auditável completa e não é arte aprovada.
- Rodada diagnóstica INF-01: candidata 1 `FAIL` por cruzamento não tipado; candidata 2 corrige esse erro matemático em recorte mínimo, mas segue `FAIL` sem cobertura visual/urbana suficiente; hash falso e relatório visual sem regiões => `FAIL`. Essas tentativas são **isoladas** e não entram no ledger canônico.
- Suíte completa em GitHub Actions: verificar a execução mais recente na HEAD da branch; testes locais e Actions não substituem ensaio real de arte nativa/compositor.

**Limites não superados:** sem prova de transferência dos bytes de imagem **gerada nativamente** para o compositor de tiles; sem execução de composição artística integral aprovada/retomada após troca de chat; sem garantia criptográfica de que o agente realizou uma avaliação semântica real. Permanecem `BLOCKED`, não `PASS`.
