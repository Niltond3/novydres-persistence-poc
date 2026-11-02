# NOVYDRES — Relatório de validação parcial (lote consolidado de 02/11/2026)

Classificação: **MIGRATION_IN_PROGRESS**. Cutover operacional: **NÃO**.

## Integridade de preservação
- Inventário com **190 registros**: 148 fontes textuais copiadas e comparadas exatamente ao texto retornado da fonte; 9 arquivos brutos do Drive copiados com SHA de blob Git idêntico ao SHA calculado dos bytes originais (3 ZIP e 6 arquivos de código/texto); 14 pastas de Drive enumeradas; **19 arquivos visuais da Biblioteca apenas catalogados e pendentes**.
- A árvore Git foi recuperada e todos os nove caminhos brutos apontam para os mesmos SHA verificados.
- 45 arquivos sob `poc/` conservam os mesmos caminhos e SHA que o commit inicial observado: POC não alterada.
- 57/57 referências textuais/JSON do catálogo histórico da Biblioteca foram preservadas; isso não implica que a Biblioteca inteira foi descoberta.
- 0 documentos Google Docs nativos foram transferidos com todos os estilos, objetos, imagens e comentários originais.

## Crônica CHR-001
- Documentos integrais de episódio M2.03 v008, character state v008, diário legado e versões históricas preservados como **texto integral extraído**, com readback.
- `LIVE.json` contém último evento `CHR001-M203-CHANGING-CLOTHES-20261102-001`, cena M2.03.073 e recursos XP 519/170/349, crédito20; FV 6/5/0/1, sem nova rolagem.
- Reconciliação parcial da ficha confirmada no diário: sete atributos alocados, quatro perícias alocadas, custo 125+45=170 XP. Duas Touchstones históricas **Sara e Mary**; elegibilidade em 2010 ainda desconhecida.
- Índice de M1: 27 marcos, 26 entidades, 12 relações, 10 locais (75 localizadores) derivados da projeção provisória antiga, sem caráter de ledger.
- Índice de M2: 87 identificadores (174 ocorrências) com referência e posição em dois textos-fonte. Identificadores de eventos e rolagens não são prova de origem RNG nem `COMMITTED` técnico.
- Todos os caminhos do LIVE, do índice e dos subíndices testados existem na árvore Git. Os SHA das fontes do índice M2 conferem. O estado candidato permanece expressamente **INATIVO**.
- **Retomada narrativa bloqueada** até auditoria e decisão de migração formal, em respeito a G19/G23.

## Restrições
- 19 PNG/ZIP de cartografia e POI na Biblioteca permanecem sem cópia de bytes originais; não são os três ZIP de código histórico do Drive que passaram por transferência.
- Conflitos de autoridade editorial/POI e de completude da ficha e conhecimentos dos NPCs ainda exigem evidência.
- Nenhuma migração do ledger técnico vazio para eventos supostamente auditados, nenhum retcon, nenhuma edição de CANÔNICO/FECHADO ou APROVADO/CONGELADO.
- O Drive permanece fonte operacional e acervo original; GitHub é arquivo migrado e projeção candidata.
