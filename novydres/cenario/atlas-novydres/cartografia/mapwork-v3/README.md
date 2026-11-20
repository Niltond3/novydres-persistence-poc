# Novydres Mapwork V3 — infraestrutura de composição e arquitetura urbana V3.1 (não canônica)

**Propósito:** gerar arte 2D por lote (edifício individual só por exceção), compor mosaicos globais em alta resolução, preservar escala U02, checar conectores e entregar comparação ANTES/DEPOIS completa. Este pacote **não** gera arte com IA por conta própria: o agente no ChatGPT pesquisa, chama ferramenta de imagem quando autorizado, baixa e envia assets via Google Drive, confere o readback, atualiza manifestos no GitHub e só então usa o compositor local.

## Regras inegociáveis

1. Bootstrap em um único SHA de `master`: `novydres/AGENTS.md`, `CONTEXT.md`, `catalogo.json`, ADR-002, PRD-ATLAS-001 e `cartografia/guide.md`; nunca substituir as fontes por resumo de chat.
2. Referência aprovada U02 (SHA-256 `9d55965f45181e3b943552e32df0e8ad41b63c8974ffd6e670f447ffd36eb9a0`), 1448×1086. Suas coordenadas são unidades abstratas, não metros.
3. Escala detalhada única: 64 px por pixel U02, tiles 512×512. Não renderizar o atlas inteiro em uma bitmap monolítica. A qualidade final vem de novos assets, não da interpolação da U02.
4. Lote com máscara total e bleed ≤ 1,5 unidade U02. Edifícios especiais têm asset separado. Elementos de lotes são desenhados em 2D top-down consistente com a U02, não extrusão mecânica 3D.
5. Conectores espaciais de zonas adjacentes devem ter os mesmos ID, categoria, coordenadas, largura e perfil. Estradas/trilhos/rios têm definição global; nunca redesenhar a autoridade independentemente em cada lado. O teste semântico não substitui inspeção visual das costuras.
6. Editar uma região não altera zonas aprovadas nem promove cânone. `last_approved_global_release` aponta só para versão aprovada; candidato nunca atualiza esse ponteiro automaticamente.
7. Toda entrega visual exige mapa ANTES/DEPOIS integral e zoom, com HTML acessível pelo chat, não GitHub como canal visual. O comparador é um HTML autocontido que carrega os tiles relevantes; avaliar limite de tamanho para zonas grandes.
8. Assets e máscaras PNG ficam privados no Google Drive. Git guarda esquemas, estados, IDs do Drive, SHA256 e scripts; não guarda imagens produzidas no V3. GitHub Actions não acessa a sessão autenticada do Google Drive do ChatGPT.

## Instalação no executor local do agente

```bash
python -m pip install -r novydres/cenario/atlas-novydres/cartografia/mapwork-v3/requirements.txt
python -m pytest -q novydres/cenario/atlas-novydres/cartografia/mapwork-v3/tests
```

## Comandos

```bash
python scripts/mapwork.py audit
python scripts/mapwork.py next --zone zones/cidade-velha/zone.json
python scripts/mapwork.py validate --zones zones/area-a/zone.json zones/area-b/zone.json --assets /working/assets --base /working/U02.png --strict
python scripts/mapwork.py render --zones zones/area-a/zone.json zones/area-b/zone.json --assets /working/assets --base /working/U02.png --out /working/tiles-candidate
python scripts/mapwork.py compare --before /working/tiles-approved --after /working/tiles-candidate --base /working/U02.png --out /working/comparacao.html
```

Execute da pasta `mapwork-v3/`. `--before` pode ser omitido apenas na primeira versão, quando a U02 aprovada é a referência visual completa. Quando houver uma release, o agente deve baixar os tiles aprovados do Drive para montar a visão anterior. O manifesto `tiles.json` contém hashes e coordenadas; ao fazer upload de cada tile, preencher seu `drive_file_id` e confirmar metadados no Drive antes da publicação.

## Limites honestos

- GitHub Actions valida contratos, fixtures, IDs, geometria e testes. Não consegue confirmar bytes privados do Drive sem credencial Google própria. Integridade dos PNGs da release é verificada pelo executor com bytes baixados da conta conectada e SHA256. Não alegar que apenas um SHA em JSON prova disponibilidade real do arquivo.
- A escala física, altura de pavimentos e limites exatos da Cidade Velha ainda precisam de decisão. A camada de base U02 ampliada ainda será baixa resolução fora das regiões substituídas.
- O HTML embute tiles PNG em base64. Em zonas grandes, dividir entrega por conjunto de tiles/trechos inspecionáveis; manter mapa integral como visão de contexto. Não prometer um único arquivo leve para milhares de tiles.
- O presente pacote prova o mecanismo com fixtures sintéticas, **não a geração artística real da Cidade Velha**.


## V3.1 — Transporte estrutura os lotes

Um **lote urbano** é um quarteirão/quadrante delimitado por vias, linhas ferroviárias ao nível do solo, água e outras barreiras urbanas. Dentro do lote distribuem-se edifícios, fábricas, pátios e POIs. Uma `work_unit` é apenas uma parcela operacional de geração/máscara e pode haver muitas work units no mesmo lote. A contagem de lotes é derivada da malha, não escolhida como 14 por antecedência.

A camada `scripts/urban_architecture.py` define rede global de ruas/avenidas/expressas, trevos, viadutos, cruzamentos, ferrovias, ramais, bondes e hidrografia, verificando níveis, conectividade, classificação territorial 100%, morfologia por uso/altura, formação de quarteirões e distribuição exata dos pixels editáveis nas work units. O motor preserva a autoridade da U02, separa cruzamentos reais de passagens elevadas e exige máscaras e costuras bilaterais antes da geração de arte. Consulte `architecture-v3-1-transport.md`.

**Kingswell:** U02_KW_SKETCH_02 aprovado no nível **macro**; a rede real da U02 e a classificação integral ainda não foram extraídas. Os 14 retângulos históricos são janelas candidatas cobrindo 16,32% do polígono total, não lotes da cidade. Testes sintéticos da arquitetura não comprovam que Kingswell esteja pronto para arte.
