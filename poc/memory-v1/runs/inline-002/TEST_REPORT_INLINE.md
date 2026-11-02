# POC V1.1 — Relatório de contexto embutido

**STATUS:** Aprovado como teste técnico sintético, NÃO autorizado para CHRONICLE_001.

## Fixture e proveniência
Criado fork de ensaio `inline-002` a partir do snapshot sintético `load-001` seq030. Histórico anterior é preservado em arquivos POC referenciados por `HISTORY_INDEX.json` e `scene.context_packet.source_refs`. O índice do fork removeu `active_scene`; o `LIVE.scene.scene_id` é a única fonte de cena atual. `SCENE_CONTEXT.md` não é necessário neste fork.

## Resultado
- 3 eventos sintéticos novos (031, 032, 033), **3/3 commits publicados com readback**.
- 2 transições de cena (031 galpão → casa, 033 casa → galpão) em que **o único arquivo escrito foi LIVE.json**; cada transição exigiu `1 update_file + 1 fetch_file` no caminho de gravação e conferência. Não houve alteração de HISTORY_INDEX.
- 1 turno sem transição (032), mesmo custo de escrita+verificação.
- O pacote embutido incluiu lembrança da promessa antiga seq013, desconhecimento original de Ivo, NPC_CLAIM de Vale ainda não verificada e questão do alarme ainda em aberto.
- Em um ensaio de leitura isolada do estado, **uma leitura de LIVE** trouxe o contexto de cena, a pendência, as referências de história e as restrições narrativas. **Essa leitura não substitui consulta à governança nem prova o conteúdo integral do arquivo histórico.**
- O último LIVE ficou com ~13.031 caracteres (dentro do limite experimental de 30 mil).

## Custo comparado, somente para uma transição SEM mudança do índice
V1 (load-001) atualizava `LIVE`, `HISTORY_INDEX` e `SCENE_CONTEXT`: `create_tree + create_commit + update_ref + 3 fetch_file` = **6 chamadas críticas**; leituras preparatórias de HEAD/tree e recuperação excluídas.
V1.1 inline escreve só LIVE com contexto embutido: `update_file + fetch_file` = **2 chamadas críticas**; recuperação eventual de entidades, arcos e evidências é adicional.
Assim, duas transições testadas economizaram **4 chamadas críticas cada**, mas isso NÃO é garantia para cenas que alteram índices ou exigem fontes complexas.

## Limitações
Teste operado por script com dados sintéticos. Não houve narração autônoma, chat realmente novo, erro real de rede, disputa de concorrência nem migração de dados reais. Ler o LIVE sozinho não basta para todo encontro: se a cena exigir nuances não presentes no pacote, buscar INDEX/entidade/arco/fonte original.

## Próximo gate recomendado
1. Validação adversarial de coerência narrada com contexto insuficiente: forçar NEEDS_EVIDENCE, nunca inventar.
2. Ensaio de retomada em conversa realmente nova.
3. Auditoria de proveniência e inventário do Drive antes de qualquer importação real.
4. Formalizar aprovação específica de alteração da DEC-CR-014; preservar G19/G23, cânone e documentos congelados.
