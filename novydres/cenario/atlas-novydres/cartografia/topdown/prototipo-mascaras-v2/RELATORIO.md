# Novydres — Validação POC V2

**Situação:** candidata, aguardando avaliação visual do proprietário. **Não** é canonização da U03 nem dos lotes/edifícios.

## Implementação

POC V1 e U02 preservadas. Setor teste: Kingswell; um bairro experimental, dois lotes, sete edifícios A1–A3, B1–B4. Cada edifício tem PNG RGBA e máscara binária **próprios**, separados do lote e da cidade. Implantação e microedição são compostas a partir desses assets individuais.

A cidade continua top-down; os prédios mostram fachadas sul/leste e coberturas em uma **perspectiva oblíqua ilustrativa uniforme**, sem câmera 3D. É um contrato 2.5D, não uma reconstrução de alturas reais. A iluminação de cobertura é consistente, com fachadas detalhadas e janelas.

## Testes

Consulte `validacao_v2.json` para números reproduzíveis. Foi verificado:

- SHA-256 da U02 original e resolução 1448×1086.
- Todos os sete edifícios dentro dos lotes e máscaras não sobrepostas.
- Alteração de implantação apenas nos dois lotes.
- Alteração do B2 apenas dentro da própria máscara, no detalhe 16× e no mapa original.
- **Sete edições sintéticas isoladas** (uma em cada prédio), sem alterações fora das máscaras correspondentes.
- Edição física do PNG alternativo de B2 sem regravar os outros sete PNGs ou suas máscaras.

## Ressalvas

Os footprints herdados da POC V1 são **áreas experimentais**, não lotes cadastrados. A U02 de 1448×1086 permanece pixelada no zoom 16×; o detalhamento vetorial local não aumenta a informação original. As edificações produzidas ilustram um método, não são arte arquitetônica final aprovada. Não há levantamento GIS/topológico nem validação da versão U03 inteira. Os 34 POIs continuam reservados. Necessária revisão visual pelo proprietário.
