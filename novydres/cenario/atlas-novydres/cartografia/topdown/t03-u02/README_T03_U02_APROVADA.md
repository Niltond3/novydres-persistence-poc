# NOVYDRES MAPWORK — T03 / U02 aprovada com ressalva

**Estado:** `CLOSED_FOR_VISUAL_WORKING_BASE` — decisão explícita do proprietário em 19/11/2026. **Não é canonização de limites oficiais, infraestrutura GIS, domínio político ou relevo original.**

## Base recuperável

- T02: relevo top-down usado na U01 (imagem-fonte preservada).
- T03/U01 V2: urbanização aprovada (mantida byte a byte).
- T03/U02: infraestrutura e conexões aprovada para continuidade visual (mantida byte a byte).
- Arte Gótico-Punk V1 continua sendo a referência visual canônica histórica, não sobrescrita.
- Todos os arquivos originais, comparadores U01/U02, máscaras, relatório e scripts seguem no pacote versionado por fragmentos binários Git.

Recuperação: `python reconstruct_topdown.py --out /pasta/saida`; exige Python 3 + zstd. O reconstrutor confere SHA256 do arquivo comprimido e de **cada arquivo**. Consulte `topdown_assets_manifest.json`.

## Dados verificados da U02

- Base U01 V2 SHA256: `f17cdcdaec1fa4d9e096fc458a883378a0b9cd82f7b88af4759e1ad8900149de`.
- Resultado U02 SHA256: `9d55965f45181e3b943552e32df0e8ad41b63c8974ffd6e670f447ffd36eb9a0`.
- Máscara U02 SHA256: `b5939602b2a41d673fe6c75ca36fd438bca34c923f5796aec267799e5f53b9a5`.
- Resolução: 1448×1086; 533.702 pixels efetivamente alterados, zero fora dos 533.874 pixels da máscara de composição.
- **Não** foram executadas validações GIS/topológicas de estradas, ferrovias, ilhas ou contornos dentro da máscara.

## Ressalva do proprietário, vigente a partir da U03

- Trocar as localizações de **Vasyl Bay** e **New London** no planejamento das regiões: o envelope físico anteriormente associado a Vasyl Bay passa a ser tratado como New London; o envelope anteriormente associado a New London passa a representar Vasyl Bay.
- A estação norte de passageiros **POI 34** continua na mesma localização física que a U02 exibe, ficando **dentro de New London** no planejamento a partir da U03.
- A identidade **POI 21 — Estação Sul de Carga/Pátio Ferroviário** segue ratificada; não ressuscitar POI 35.
- Não mudar imagens U01/U02 retroativamente; não deslocar construções automaticamente.
- Os outros POIs relacionados às regiões trocadas devem ser reavaliados antes de ajustar rótulos/posições.
- O GEO-013.1 atualmente registra a parada internacional de passageiros em **Sulfok**; a nova decisão visual põe o POI 34 em **New London**. A divergência geográfica é explícita e precisa de reconciliação formal; não declarar silenciosamente que o fato antigo deixou de valer.

A ressalva detalhada e a prova de proveniência estão em `u03_remapeamento_zonas.json` e `topdown_approval_state.json`.