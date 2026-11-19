# NOVYDRES MAPWORK — T03/U03 · candidata para avaliação

**Estado:** `CANDIDATE_AWAITING_OWNER_APPROVAL`, sem fechamento, sem canonização e sem avanço a U04.

## Fonte e remapeamento

- `master` no bootstrap: `432609e642c6569da6a64e302dc8272dd4b4a47f`.
- U02 aprovada e imutável: `9d55965f45181e3b943552e32df0e8ad41b63c8974ffd6e670f447ffd36eb9a0`, 1448×1086.
- U03 candidata PNG: `3fae4c251e09651994c4da43e8f61967193b655abf39f983eabccff2c7ad96b1`.
- Vasyl Bay e New London trocam **identidade visual regional** a partir de U03: antigo envelope Vasyl Bay = New London; antigo envelope New London = Vasyl Bay. Não há traslado de construções nem alteração de limites administrativos.
- POI 34 — Estação Norte de Passageiros, permanece fisicamente como na U02; sua zona de planejamento U03 é New London. POI 21 preservado como Estação Sul de Carga/Pátio Ferroviário, sem resolver raion definitivo; POI 35 permanece aposentado.

## Alterações visuais efetivadas

- Detalhamento conservador de materiais e microcoberturas de edifícios existentes nas ROIs de **New London** (neoclássico), **Vasyl Bay** (religioso/universitário), **Dunwich** (termal/turístico), **Bukovie** (aristocrático/financeiro), **Alexandria** (monumental clássico), **Crisol** (institucional fortificado), **Levi** (institucional/científico), **Sulfok** (fabril/operário), **Kingswell** (histórico/degradado) e **Drevnigrad** (gótico industrial).
- O trabalho restringe-se a modulação discreta da textura de telhados e pequenos traços arquitetônicos de cobertura. **Não há ainda um redesenho profundo de quadras nem implantação de edifícios individualizados**, como o objetivo artístico completo pede. Este limite deve ser avaliado expressamente pelo proprietário; não tratar como satisfação integral da intervenção 2.
- Não foram criados nem movidos os 34 POIs. Conflitos de identidade e posição de 6–12 estão inventariados em `T03_U03_pois_reconciliacao.json`.

## Validação proporcional

- Mesmo enquadramento e resolução dos dois rasters; fonte U02 não regravada.
- 387566 pixels modificados, 0 alterações fora das ROIs classificadas de telhado por limiar de textura.
- Fora das ROIs, inclusive corredores ferroviários protegidos, igualdade de pixels demonstrada.
- Nenhum rótulo, ícone, legenda, vetor de limites ou reconfiguração administrativa adicionado ao mapa.
- **Não verificado:** classificação semântica 100% correta de todos os telhados, detalhe individual de quadras, persistência topológica de vias locais e contornos GIS, visualização no navegador do proprietário, adequação artística plena.

## Conflitos e ressalvas

1. GEO-013.1 associa passageiros internacionais a Sulfok; a U03 visual reserva POI 34 em New London, conforme decisão explícita. O Atlas permanece intacto, reconciliação futura necessária.
2. Os envelopes propostos no Inventário V3 foram calculados sobre uma ilustração anterior, sem registro cadastral transferível à U02 top-down. ROIs desta edição são **zonas visuais conservadoras** e não polígonos administrativos ou máscaras aprovadas.
3. Os POIs 6–9 (antigo New London) e 10–12 (antigo Vasyl Bay) exigem conciliação de função, região e lote antes de U04; sem movimento automático.
4. Não houve revisão independente pixel a pixel de ruas locais e edifícios específicos, apenas verificação automatizada de escopo do procedimento.

## Recuperação

- Rodar `python reconstruct_u03.py --out T03_U03_candidata.png`, usando os oito `parts/part-*.b64`, restaurando byte a byte o PNG com SHA conhecido.
- O arquivo `build_u03.py` documenta as ROIs e permite regenerar a candidata **a partir do arquivo U02 original** e do Inventário V3 aprovado; requer Pillow, NumPy e OpenCV.
- `make_comparator.py` gera um HTML independente do GitHub a partir dos PNGs U02/U03; a visualização é entregue ao proprietário diretamente no ChatGPT, não por link GitHub.

**Nenhum fechamento ou handoff para U04 foi autorizado.**