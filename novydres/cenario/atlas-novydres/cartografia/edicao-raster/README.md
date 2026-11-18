# NOVYDRES — Pipeline persistente de edição raster com máscaras (v1)

**Objeto:** imagem ilustrativa/isométrica de Novydres, separada da geografia canônica estruturada. O protocolo é operacional, não aprova posições, bairros, história ou outras definições do Atlas.

## Gatilho de retomada

Quando o proprietário disser **“vamos continuar a edição do mapa”**, com uma imagem marcada ou descrição da região:

1. **Bootstrap Git-native:** consultar HEAD atual de `master`; ler `novydres/AGENTS.md`, `CONTEXT.md` e `catalogo.json` no **mesmo SHA**; resolver `world-atlas-novydres`, `index.md`, ADR-002, PRD-ATLAS-001, `cartografia/guide.md` e este diretório. A branch de desenvolvimento não é fonte operacional antes de ser integrada a master.
2. **Confirmar base:** usar imagem enviada pelo usuário; verificar dimensão 1448×1086 e SHA-256 quando for V1. Não interpretar a imagem marcada como mestre; recuperar a versão sem marcações. Se for uma versão diferente, obter declaração explícita sobre qual base usar; nunca promover candidata automaticamente.
3. **Resolver máscara:** procurar `masks/MXX.json`; se nova, propor uma delimitação binária exata, com polígonos e exclusões, destacada sobre **mapa completo**. Não editar antes da aprovação específica da máscara.
4. **Execução local:** produzir candidata com ferramenta artística, sem assumir que ela obedeceu ao escopo; compor sobre uma cópia da base com `pipeline.py compose`, restringindo ao PNG da máscara aprovada; gerar relatório `verify`.
5. **Revisão semântica:** inspecionar encaixes de coberturas, sombras residuais/ghosting, continuidade das estradas, trilhos, perspectiva, bordas e edifícios protegidos. **Zero pixels alterados fora da máscara é necessário, mas NÃO suficiente.** Se houver falha visual, status `NEEDS_VISUAL_CORRECTION`, sem aprovação.
6. **Comparação obrigatória:** executar `pipeline.py compare`; entregar no chat **HTML interativo offline, funcional e verificado**, com mapa integral ANTES/DEPOIS por padrão, modos deslizar e lado-a-lado, mais prévia estática integral. Oferecer download direto no chat; **não enviar link GitHub como forma de visualizar**. Testar no Chromium desktop e mobile quando disponível, relatar limites se não houver navegador.
7. **Aceite e persistência:** só após aprovação explícita da candidata registrar nova revisão aprovada; manter mestre anterior e metadados de máscara/versionamento, readback remoto. **Se o binário aprovado não estiver persistido no repositório, declarar a lacuna e exigir sua recuperação por hash antes da próxima edição acumulativa.** Sem nova imagem, sem nova máscara ou sem aprovação, não afirmar que foi editado, aceito ou canonizado.

## Artefatos e comandos

`python pipeline.py mask --base MASTER.png --spec masks/M01.json --out M01-mask.png`

`python pipeline.py compose --base MASTER.png --candidate GERADA.png --mask M01-mask.png --out candidata.png`

`python pipeline.py verify --base MASTER.png --after candidata.png --mask M01-mask.png`

`python pipeline.py compare --base MASTER.png --after candidata.png --mask M01-mask.png --out comparador.html`

Dependência: Python 3 + Pillow. Os HTML são autocontidos com WebP embutido; seus previews podem usar compressão com perdas, mas PNG originais e verificação são sem perdas. Para aceitar, comparar pixel a pixel os PNG, não o HTML. Testes automatizados de controles no navegador e revisão visual são gates separados.

## Fonte e estados atuais (18/11/2026)

- **Imagem-mestre V1 imutável:** `novydres_imagem_mestre_v1.png`, 1448×1086; SHA256 `d36dc57d32d6874bd122316480432ca1ce4009a44a044b3c2e5815fc21dc947d`. **O binário mestre não está incluído neste pacote Git**; é obrigatório recuperar o arquivo original do usuário / anexo, verificar hash e jamais reconstruí-lo a partir de uma candidata ou de um PNG com anotações. O proprietário já declarou que pode enviar a versão do mapa na retomada.
- **M01:** delimitação de 1,0222% aprovada. **M01-V2 APROVADA PELO PROPRIETÁRIO em 18/11/2026**, após correção da silhueta/sombra residual. Candidato `novydres_M01_candidata_v2_sem_sombra.png`, SHA-256 `bb5c4a03bf65240e250e49504e6d281b6dc0b864eab16aa6a44e9b623cd26963`; zero pixels alterados fora da máscara. **O PNG aprovado e o comparador NÃO estão armazenados no GitHub**: para editar M02 sem perder M01, recuperar/anexar o PNG M01-V2 exato e validar hash. Ver `masks/M01.json`.
- **M02:** objetivo textual definido, delimitação pixel a pixel ainda NÃO aprovada; ver `masks/M02.json`. Próximo passo executável é gerar a prévia integral da máscara M02 a partir do arquivo M01-V2 recuperado e obter aprovação da máscara; não fazer edição artística de M02 antes da aprovação.
- **Comparador:** versão anterior falhava no uso relatado pelo proprietário. Nova versão reconstruída e validada programaticamente em Chromium 1200px e 390px nos modos de mapa completo/detalhe, slider e lado-a-lado; **teste no dispositivo do proprietário pendente**. Se não abrir, não declarar gate concluído.

## Segurança editorial

Nenhuma edição raster transforma imagem em fonte canônica, altera `world-atlas-novydres` ou resolve GEOs. Não criar “handoff” de próxima MW com ponto aberto; apenas estado de retomada da mesma atividade. A aprovação da máscara ≠ aprovação da edição. Não mover estruturas não autorizadas. Não modificar `master` sem aprovação/integração.

## Arquivos raster persistidos e retomada sem chat (18/11/2026)

**Manifest oficial no Git:** `edicao-raster/assets.json` (SHA-256, nomes, caminhos persistentes e estados). Os **5 binários de referência/artefatos** estão na pasta persistente da ChatGPT Library `/Novydres - Mapwork/edicao-raster`, não embutidos no Git. A integração atual não ofereceu envio binário PNG direto ao GitHub; não alegar que o PNG mora no repositório. O manifesto Git, e não memória de conversa, governa quais hashes, fontes e estados são válidos. Os cinco arquivos foram recuperados da Library e confrontados com os hashes locais.

**M01-V2:** `APPROVED_BY_OWNER` em 18/11/2026. A estação histórica oeste foi aceita após retirada da sombra residual; fora da M01, zero pixels modificados. PNG aprovado `novydres_M01_candidata_v2_sem_sombra.png`, SHA-256 `bb5c4a03bf65240e250e49504e6d281b6dc0b864eab16aa6a44e9b623cd26963`. Não usar a candidata V1, nem exigir novo aceite da M01.

**Como retomar num chat limpo:** após bootstrap no Git, consultar `assets.json`; chamar `files.list` na pasta Library indicada e `files.materialize` (raw_file) para obter exatamente a master e a M01-V2, e conferir SHA-256 antes de qualquer operação. A imagem marcada M02 também está lá. **O arquivo de marcação não é a máscara aprovada.** A máscara M02 continua pendente; primeiro prévia integral e aceite expresso, depois edição M02 sobre a M01-V2 aprovada. O mestre V1 fica imutável.
