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

- **Imagem-mestre V1 imutável:** `novydres_imagem_mestre_v1.png`, 1448×1086; SHA256 `d36dc57d32d6874bd122316480432ca1ce4009a44a044b3c2e5815fc21dc947d`. **O mestre pode ser recuperado de fragmentos binários versionados em Git, sem gerar outra imagem**, via `reconstruct_assets.py`, ou de sua réplica em Library; SHA-256 é obrigatório.
- **M01:** delimitação de 1,0222% aprovada. **M01-V2 APROVADA PELO PROPRIETÁRIO em 18/11/2026**, após correção da silhueta/sombra residual. Candidato `novydres_M01_candidata_v2_sem_sombra.png`, SHA-256 `bb5c4a03bf65240e250e49504e6d281b6dc0b864eab16aa6a44e9b623cd26963`; zero pixels alterados fora da máscara. **O PNG M01-V2 aprovado pode ser reconstituído byte a byte pelos fragmentos binários Git**. O comparador HTML está na Library e pode ser regenerado pelo pipeline. Ver `masks/M01.json`.
- **M02:** máscara V3 (29.469 pixels) e resultado artístico V3 **APROVADOS em 18/11/2026**. PNG cumulativo SHA-256 `c118a0560e4adcaaede454b524d43bc3a4a94474dc01cfd17ceaea2963318e0b`. Zero diferenças fora da máscara. Recuperação binária Git por `reconstruct_m02_v3.py` + patch WebP sem perdas (ver assets.json). Nenhuma canonização automática.
- **Comparador:** versão anterior falhava no uso relatado pelo proprietário. Nova versão reconstruída e validada programaticamente em Chromium 1200px e 390px nos modos de mapa completo/detalhe, slider e lado-a-lado; **teste no dispositivo do proprietário pendente**. Se não abrir, não declarar gate concluído.

## Segurança editorial

Nenhuma edição raster transforma imagem em fonte canônica, altera `world-atlas-novydres` ou resolve GEOs. Não criar “handoff” de próxima MW com ponto aberto; apenas estado de retomada da mesma atividade. A aprovação da máscara ≠ aprovação da edição. Não mover estruturas não autorizadas. Não modificar `master` sem aprovação/integração.

## Arquivos raster persistidos e retomada sem chat (18/11/2026)

**Manifest oficial no Git:** `edicao-raster/assets.json` (SHA-256, nomes, caminhos persistentes e estados). Os cinco arquivos também estão na pasta persistente ChatGPT Library `/Novydres - Mapwork/edicao-raster`. **Mestre V1, M01-V2 e máscara M01 estão no Git como binários recuperáveis sem perda**: ver seção abaixo. Manifesto Git, e não memória de conversa, governa hashes, fontes e estados.

**M01-V2:** `APPROVED_BY_OWNER` em 18/11/2026. A estação histórica oeste foi aceita após retirada da sombra residual; fora da M01, zero pixels modificados. PNG aprovado `novydres_M01_candidata_v2_sem_sombra.png`, SHA-256 `bb5c4a03bf65240e250e49504e6d281b6dc0b864eab16aa6a44e9b623cd26963`. Não usar a candidata V1, nem exigir novo aceite da M01.

**Como retomar num chat limpo:** após bootstrap no Git, consultar `assets.json`; chamar `files.list` na pasta Library indicada e `files.materialize` (raw_file) para obter exatamente a master e a M01-V2, e conferir SHA-256 antes de qualquer operação. A imagem marcada M02 também está lá. **O arquivo de marcação não é a máscara aprovada.** A máscara M02V3 e a versão artística M02 V3 corrigida foram aprovadas pelo proprietário; esta última é agora a base cumulativa corrente, recuperável pelo Git e pela Library.

## Recuperação integral de PNGs a partir do Git (18/11/2026; regra vigente)

**Os binários mestre V1 e M01 V2 APROVADA ESTÃO persistidos no próprio GitHub** como fragmentos binários brutos sem perdas (cada um de até 150000 bytes), ordenados em `assets/master_v1/` (33 fragmentos) e `assets/m01_v2/` (26 fragmentos). A máscara M01 também foi publicada em `assets/M01_mask.png`. Não são PNGs individuais dentro do Git: o comando abaixo reconstrói exatamente os PNGs originais, com SHA-256 obrigatório. Esta seção **substitui afirmações históricas anteriores de ausência de binários no Git**.

Após checkout/obtenção dos arquivos do repositório:

`python novydres/cenario/atlas-novydres/cartografia/edicao-raster/reconstruct_assets.py --asset master_v1 --out MASTER.png`

`python novydres/cenario/atlas-novydres/cartografia/edicao-raster/reconstruct_assets.py --asset m01_v2 --out M01-V2.png`

O script recusa sobrescrever arquivo existente, verifica os SHA-1 dos fragmentos e confere o SHA-256 final. Consultar `assets/parts.json` e `assets.json`; em um chat sem acesso a clone/files Git binários, a pasta persistente ChatGPT Library `/Novydres - Mapwork/edicao-raster` permanece como réplica de recuperação, com mesmos SHA-256. A `M01-V2` já está aprovada e será a base operacional cumulativa para M02. A máscara M02V3 e a arte M02 V3 corrigida estão **APROVADAS**. A antiga candidata V2 foi rejeitada/substituída. O arquivo com marcação M02 existe na Library e não é uma máscara.

## M02V3 — máscara e arte aprovadas (18/11/2026)

A máscara extraída da pincelada branca do proprietário foi aprovada expressamente (`Aprovo`), com 29.469 pixels (1,874%) e SHA-256 `45203d53388c961cb1a81e593e29313b031a7b6a6f5110cb1e8a0a82230576d8`. A fonte estruturada é `masks/M02.json`, o PNG binário aprovado está na Library listada em `assets.json`. M01-V2 continua sendo a base operacional cumulativa imutável.

A candidata V2 foi rejeitada por corte de um edifício no limite leste. A versão V3 corrigida foi **APROVADA expressamente**: 24.902 pixels modificados dentro da máscara, zero fora, SHA-256 `c118a0560e4adcaaede454b524d43bc3a4a94474dc01cfd17ceaea2963318e0b`. PNG completo e comparador em Library; patch sem perdas e reconstrutor em Git. O último prédio termina inteiro antes da rua de conexão leste. Não canoniza a geografia.

## Recuperação Git do PNG M02 V3 aprovado

O binário `assets/m02_v3_approved/patch.webp` é um recorte **WebP lossless** de 342×111 pixels. Aplicado exclusivamente na máscara M02 V3 sobre a M01 V2 aprovada, reconstrói **byte a byte** `novydres_M02_V3_aprovada.png` SHA-256 `c118a0560e4adcaaede454b524d43bc3a4a94474dc01cfd17ceaea2963318e0b`. O arquivo PNG completo está também na Library (conforme `assets.json`).

```sh
python novydres/cenario/atlas-novydres/cartografia/edicao-raster/reconstruct_m02_v3.py --out M02-V3.png
```

Requer Pillow e os binários M01 V2 recuperáveis do Git pelo `reconstruct_assets.py`. O reconstrutor valida SHA-256 da base, patch, máscara e saída. **Aprovada a imagem ilustrativa**, não as hipóteses cartográficas que ela contenha.
