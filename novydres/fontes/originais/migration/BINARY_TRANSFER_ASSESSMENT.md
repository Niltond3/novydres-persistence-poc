# Avaliação de transferência binária — NOVYDRES

Em 02/11/2026, foram preservados **3 arquivos ZIP originais do Google Drive**, além de 6 arquivos brutos de código/texto: `novydres/migration/DRIVE_RAW_BLOB_AUDIT.md`. Para cada arquivo: baixar conteúdo original, gerar SHA-1 de objeto Git e SHA-256 sobre bytes locais, enviar blob base64 via GitHub, conferir SHA retornado e árvore commitada. Nove correspondências confirmadas.

**Separadamente**, os **19 ativos visuais históricos da Biblioteca** (MasterMap.png, `novydres-tiles.zip`, PNGs POI e referências) **NÃO** foram migrados. `files.materialize(raw_file)` retornou indisponibilidade de backing autorizado; imagem renderizada/preview não preserva bytes originais. Busca Google Drive não localizou cópias equivalentes confirmadas. Esses itens permanecem REFERENCED_ONLY_NOT_COPIED, com ID, nome e status histórico no catálogo.

Não declarar conclusão do domínio de cartografia ou ativos aprovados/congelados.
