# Ensaio de carga — 26 turnos sintéticos

Somente POC; absolutamente nenhum evento de Bartholomeu/CHR-001.

O fixture inicia no evento 004 de um histórico sintético, depois registra 26 eventos numerados 005–030. Cenário de teste: galpão, casa, retorno ao galpão; promessa feita a Leta; declaração de Vale continua NPC_CLAIM, causa do alarme continua UNKNOWN; rolagem usa faces fixas de teste, não RNG.

Critérios: leitura/gravação/readback no mesmo chat; scene packets em transições e arquivo de eventos por rotação >20; bootstrap sem memória de conversação, recuperar compromisso latente de seq13 ao retornar no seq21; falha pós-commit ainda não publicado; medição de chamadas de produção separada de chamadas do harness. Contratos de Drive permanecem vigentes para CHR-001.
