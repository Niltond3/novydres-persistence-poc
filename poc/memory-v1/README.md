# POC — Memória Progressiva Contextual V1

Este diretório é **um experimento separado da CHRONICLE_001**. **Dados 100% sintéticos**, sem migração, sem alteração dos arquivos do Google Drive e sem mudança de G19/G24 ou DEC-CR-014.

## Componentes
- `LIVE.json`: checkpoint operacional atual, ficha, situação, restrições, últimos eventos e buffer de eventos pendentes de arquivamento.
- `SCENE_CONTEXT.md`: pacote contextual para a cena corrente, derivado de eventos e projeções; refeito somente ao mudar o contexto relevante.
- `HISTORY_INDEX.json`: índice resolutivo de personagens, lugares, arcos e lotes de eventos, com caminhos explícitos, IDs e regras de recuperação.
- `entities/` e `arcs/`: memória relacional/causal (projeções), sempre com referências aos eventos.
- `episodes/`: fonte histórica integral do exemplo, preservada em arquivo separado e em histórico de commits.
- `WEB_CONTRACT.md`: roteiro de uso no ChatGPT Web, sem serviços externos e sem automação de fundo.
- `TEST_PLAN.md`: critérios reproduzíveis antes de qualquer migração real.

## Objetivo de custo
- Mesmo chat + cena estável + estado/sha ainda disponíveis: **update_file + fetch_file = 2 chamadas** em turno comum com delta.
- Retomada sem contexto: buscar `LIVE.json` e `SCENE_CONTEXT.md`; carregar governança obrigatória quando aplicável.
- Mudança de cena: consultar HISTORY_INDEX, buscar somente entidades/arcos/fontes relevantes, reconstruir SCENE_CONTEXT; frequência variável.
- Rotação: commit atômico para arquivar evento(s), atualizar índice e LIVE; custo superior, raro.

Não pressupor cache persistente do modelo. Nunca continuar da memória do chat quando o checkpoint tiver ficado incerto.
