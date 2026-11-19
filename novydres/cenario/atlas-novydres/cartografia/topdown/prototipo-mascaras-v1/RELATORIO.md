# Novydres — protótipo de máscaras hierárquicas (candidato)

**Escopo:** Kingswell (região), `neighborhood-ksw-pilot-01`, lotes A e B, 7 edifícios (A1–A3, B1–B4). Não há obra sobre os 34 POIs.

**Fonte:** T03/U02 aprovada, SHA256 `9d55965f45181e3b943552e32df0e8ad41b63c8974ffd6e670f447ffd36eb9a0`, 1448×1086, conferido sem modificação.

## Prova efetiva

- Imagem completa U02 original comparada com etapa 2 (`comparacao_integral.png`).
- Zoom 16× do mesmo retângulo (`comparacao_bairro_zoom.png`), camadas de arquitetura com escala local 16×, sem girar o mapa.
- `overlay_lotes.png` contém sete edifícios sobre dois lotes; `overlay_microedicao.png` difere apenas no edifício B2.
- Pixels alterados no detalhe 16× na etapa de lotes: **212046**, com **zero fora das máscaras dos lotes**.
- Pixels alterados no detalhe 16× na microedição B2: **22498**, com **zero fora da máscara B2**.
- Pixels alterados na cidade original 1448×1086 pela implantação dos lotes: **865**, com **zero fora dos lotes**.
- Pixels alterados na cidade original 1448×1086 somente pela microedição B2: **108**, com **zero fora da máscara B2**.
- Todos os edifícios cabem integralmente nos pais; as máscaras dos dois lotes não se sobrepõem.

## Limitações honestas

Este protótipo **valida hierarquia, persistência de geometria, composição e isolamento de edição**, não qualidade arquitetônica final. As coberturas vetoriais ilustram volume em projeção de planta, mas não atingem a arte definitiva desejada. A U02 continua tendo 1448×1086 px; o detalhamento criado em 16× não recupera detalhes do raster de origem. Lotes são experimentais, não contornos cadastrais aprovados. Sem análise GIS completa. Nenhuma aprovação implícita de U03; nenhum cânone ou POI alterado.

**Estado: CANDIDATA, AGUARDANDO AVALIAÇÃO.**