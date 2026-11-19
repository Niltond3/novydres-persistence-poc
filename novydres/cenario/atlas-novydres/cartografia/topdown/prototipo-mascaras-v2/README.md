# Novydres Mapwork — POC de máscaras hierárquicas V2

**Status: CANDIDATA — AGUARDANDO REVISÃO VISUAL.** A POC V1 foi aprovada como mecanismo; a V2 aplica três ajustes: edifícios individuais, projeção local oblíqua 2.5D e regras operacionais para agentes. A U02 e a POC V1 não foram editadas.

## Estrutura

- `geometria_v2.json`: árvore da cidade até os sete prédios e coordenadas experimentais.
- `assets/buildings/a1.png` ... `b4.png`: **sete PNGs transparentes independentes**. `b2_cobre.png` é a variante editada de B2.
- `assets/masks/*.png`: máscaras binárias estáveis de cada prédio, no mesmo `bbox` local de seu asset.
- `manifest.json`: cada ID, pai, máscara, SHA-256, posição e ordem de desenho.
- `render_v2.py`: renderizador, compositor, testes e comparadores reproduzíveis.
- `validacao_v2.json`: resultados mensuráveis da última composição.
- `AGENT_RULES.md`: as regras que o agente deve seguir **antes de qualquer alteração**.

## Executar

Requer Python 3.11+, `Pillow`, `NumPy`, `Shapely` (ver `requirements.txt`). Obtenha o PNG U02 aprovado (1448×1086) a partir do pacote de restauração da U02, e confirme seu SHA-256 antes de continuar.

```bash
pip install -r requirements.txt
python render_v2.py --base /caminho/T03_U02_aprovada.png --init-assets
python render_v2.py --base /caminho/T03_U02_aprovada.png --edit-b2
python render_v2.py --base /caminho/T03_U02_aprovada.png
```

**Fluxo de trabalho:** `--init-assets` cria os sete assets apenas na implantação inicial. `--edit-b2` altera somente a variante do edifício B2 e recompõe; os outros assets não são regravados. Sem flags, apenas carrega os assets existentes, compõe e testa. Você também pode editar manualmente qualquer outro `assets/buildings/<id>.png`, desde que mantenha o mesmo tamanho, a mesma máscara e o encaixe; execute depois sem flags.

## Ver a proposta

Abra `comparador_interativo_v2.html` para alternar entre mapa integral e zoom 16×, implantação e edição B2. Alternativas estáticas: `comparacao_integral_v2.png`, `comparacao_arquitetura_v2.png` e `comparacao_microedicao_v2.png`.

## Limite explícito

A geometria dos lotes é **experimental**. A projeção oblíqua dentro de footprints fixos é uma **convenção ilustrativa 2.5D** (telhado mais estreito que a base para exibir duas fachadas), e não altitude, perspectiva física calibrada ou CAD. O raster original tem 1448×1086: não se recuperam detalhes perdidos apenas ampliando. Nenhum limite administrativo ou POI foi modificado. A POC V2 não aprova a arquitetura de Novydres inteira.
