# Plano de testes — POC Memória Contextual V1

## Critérios de aceitação (a verificar, NÃO comprovados apenas por criar arquivos)
1. O índice encontra os caminhos corretos para Ivo, Vale, bomba, alarme e promessa, sem abrir todos os históricos.
2. A reconstrução de SCENE_CONTEXT distingue uma declaração, uma alegação e um evento observado; testa também o desconhecimento de Ivo.
3. O índice e as projeções têm referências válidas para todos os eventos citados.
4. Uma conversa nova recupera LIVE e contexto e identifica a decisão pendente sem continuar a cena.
5. Um turno estável pode gravar apenas LIVE + 1 readback, com integridade e estado anterior recuperável.
6. Uma mudança de cena publica LIVE e SCENE_CONTEXT juntos; uma rotação publica LIVE, índice e arquivo histórico juntos.
7. Simular erro antes de publicar branch e retry idempotente, sem duplicar eventos nem reexecutar rolagens.
8. Simular 20+ turnos em **nova execução de teste**, medir número de chamadas, tamanho de payload, tempo, taxa de falha e memória recuperada.
9. Testar `NEEDS_EVIDENCE` para afirmação ausente, contradição e alegação não confirmada.
10. Validar que POC não escreve em Drive nem contém fatos de CHRONICLE_001.

## Checklists de consultas determinísticas
- Consulta: 'Ivo perguntou sobre a bomba' => HISTORY_INDEX.entities.npc-ivo + arcs.arc-pump + events batch, SCENE_CONTEXT atual.
- Consulta: 'Vale comprovou segurança?' => NÃO: SIM-M001-E002 = NPC_CLAIM, UNVERIFIED.
- Consulta: 'Ivo leu relatório?' => UNKNOWN; ele ouviu uma alegação, não confirmou leitura.
- Consulta: 'Íris assinou?' => UNKNOWN; não declarar conclusão/assinatura.
- Consulta: 'A causa do alarme é confirmada?' => UNKNOWN, houve WORLD_EVENT de alarme sem causa conhecida.

## Nota
O evento SIM-M001-E004 termina aguardando a resposta da jogadora. A especificação testa recuperação, nunca autoriza criar resposta da jogadora ou iniciar partida real.
