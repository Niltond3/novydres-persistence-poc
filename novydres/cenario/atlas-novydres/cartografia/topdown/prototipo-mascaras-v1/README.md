# Novydres — prova de máscaras hierárquicas V1

Experimento **não canônico** autorizado pela aceitação de um protótipo: uma região (Kingswell), um bairro, dois lotes, sete prédios. A U02 (SHA-256 fixado) permanece imutável.

## Executar

1. Instalar as dependências de `requirements.txt`.
2. Obter o PNG aprovado U02 (1448×1086) do pacote persistido `topdown/t03-u02`, sem modificá-lo.
3. `python render.py --base /caminho/T03_U02_aprovada.png`
4. Conferir `validacao.json`, abrir `comparador_interativo.html` ou `comparacao_microedicao_zoom.png`.

## Camadas

`geometria.json` contém a árvore cidade > região > bairro > lote > edifício; estradas, rios, ferrovia e bonde são camadas independentes protegidas. `overlay_lotes.png` detalha apenas dois lotes. `overlay_microedicao.png` altera apenas o telhado de `b2`; todas as demais regiões permanecem idênticas ao primeiro estágio.

As coordenadas são uma **proposta técnica experimental sobre o raster U02**, não loteamento cadastral. O render testa as máscaras e o isolamento, não certifica qualidade artística, infraestrutura vetorial nem resolução de toda a cidade. Não fechar U03 nem canonizar a partir deste experimento sem novo aceite.