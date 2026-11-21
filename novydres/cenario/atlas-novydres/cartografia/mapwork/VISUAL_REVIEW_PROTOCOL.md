# Revisão visual independente do controle matemático

O agente deve realmente **abrir** a imagem integral e recortes críticos;
comparar U02, geometria, máscara autorizada, quadrantes e zonas adjacentes.
O validador comprova os bytes/hashes e a vinculação do relatório, jamais
substitui o julgamento semântico.

## Infraestrutura (INF-01 a URB-08)

Conferir visualmente cada um dos quatro critérios da etapa definidos em
`docs/infra-acceptance.md`, cruzamentos, níveis, travessias, conectividade,
faixas de proteção, modal, continuidade bilateral, cobertura sem buracos e
restrições aprovadas. Associar cada critério a recorte real via `bbox` e
SHA-256 de seus pixels e descrever motivo específico para FAIL ou PASS.
Regenerar a geometria **e** prévia ao corrigir; vincular o relatório aos SHA.

## Imagens por unidade

Gerar pela ferramenta nativa do agente, **sem API própria**, materializar o
arquivo, máscara e plano. Conferir máscara e pegada, estrutura urbana, acessos,
fronteiras de N/S/L/O com cada vizinho, leitura micro→macro e macro→micro.
Recibos incluem SHA da imagem, máscara, U02, plano e cada vizinho. Falha
invalida a unidade e suas dependentes; retornar para correção e nova geração
segundo a política única de `PIPELINE.md`. Não usar limite isolado de três
tentativas que marque uma unidade como terminada.

## Composição

Compor tiles sem modificar pixels fora de máscaras e sem alterar U02; abrir
ovamente overviews e tiles integrais ANTES/DEPOIS. Conferir identidade da
região, conectores, máscaras, transporte e micro↔macro. O relatório global
inclui `tiles_sha256`, `before_sha256`, `after_sha256`, `reference_sha256`,
`image_receipts_sha256` e as unidades examinadas. O aceite técnico apenas
libera revisão do proprietário: não publica cânone automaticamente.
