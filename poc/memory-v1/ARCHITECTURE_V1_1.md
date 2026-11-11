# NOVYDRES — Proposta de Memória Progressiva Contextual V1.1 (POC)

Status: **EXPERIMENTAL / NÃO OPERACIONAL PARA CHRONICLE_001**. Nenhuma mudança foi feita em Drive, em contratos de governança nem em arquivos canônicos.

## Decisão técnica candidata
A memória contextual da **cena atual** passa a morar **dentro do LIVE.json**, em `scene.context_packet`. A separação entre "memória ativa" e "contexto da cena" continua sendo **lógica**, mas não precisa impor uma segunda gravação física a cada transição. O arquivo `SCENE_CONTEXT.md` torna-se exportação derivada opcional para auditoria e handoff; não integra o ciclo crítico normal nem supera LIVE ou eventos históricos.

Manter uma cópia corrente de SCENE_CONTEXT.md **e** o mesmo contexto em LIVE como duas fontes equivalentes provocaria divergência; por isso a única projeção de cena operacional candidata será LIVE.scene.context_packet.

## Objetivos mensuráveis
- Turno comum no ChatGPT Web, com conteúdo íntegro e blob SHA do LIVE ainda disponíveis: **1 update_file + 1 fetch_file de readback**. Não eliminar readback; se o conteúdo/SHA não estiver íntegro no contexto, fazer leitura inicial.
- Mudança de cena sem entidade/relacionamento novo: **recuperar índice/fontes relevantes quando necessário**, montar novo context_packet dentro do LIVE, **1 update_file + 1 fetch_file**, não gravar índice só para repetir o ID da cena.
- Alteração relevante do grafo, nascimento de arco, correção factual ou rotação: commit Git multi-arquivo por árvore, commit e update_ref, seguido de readback dos caminhos afetados (custo maior e deliberado).
- Bootstrap em conversa nova: recuperar governança de fonte autorizada e LIVE; buscar índice e memórias conforme mudanças de cena, entidades/threads/links relevantes. Não prometer cache entre conversas.
- Evento histórico completo: buffer enquanto não arquivado; após rotação, arquivo histórico integral + índice de faixa sequencial. Nunca depender somente de Git diffs/commits para reconstrução.
- Rotação experimental se LIVE >30 mil caracteres ou buffer >20 eventos; guardar inteiro e validar antes de retirar qualquer entrada.

## Estrutura candidata
```text
CHR-001/
├── LIVE.json                  # Estado + pacote de cena + buffer + evento ativo
├── HISTORY_INDEX.json         # Index esparso de fatos, relações, arcos e batches
├── governance/                # REFERÊNCIAS/APROVAÇÕES, jamais alteração tácita de cânone
├── entities/                  # Projeções por entidade, com refs
├── arcs/                      # Causalidade, promessas, consequências, conhecimento
├── episodes/                  # Eventos arquivados íntegros e versionados
└── exports/SCENE_CONTEXT.md   # Opcional, snapshot derivado; pode estar atrasado
```

## Contrato do pacote contextual embutido (exemplo de schema)
```json
{
  "scene": {
    "scene_id": "SC-EXAMPLE",
    "context_packet": {
      "built_from_event_id": "EVENT-ID",
      "location": "location-id",
      "participants": ["entity-id"],
      "confirmed_facts": [{"text":"...", "source_event_ids":["..."]}],
      "npc_claims": [{"text":"...", "claimant":"...", "source_event_ids":["..."], "verified":false}],
      "actor_knowledge": [{"entity_id":"...", "knows_event_ids":["..."], "unknowns":["..."]}],
      "latent_obligations": [{"thread_id":"...", "source_event_ids":["..."]}],
      "unresolved": ["..."],
      "source_refs": ["..."],
      "context_status": "EVIDENCE_BACKED"
    }
  }
}
```

## Algoritmo de recuperação
1. Verificar LIVE e sua versão. Para a mesma cena, usar pacote já verificado.
2. Se mudar localização, ator, relação, ameaça ou arco, identificar entidades, fios causais pendentes, **promessas latentes**, testemunhas e conhecimento restrito.
3. Ler HISTORY_INDEX somente quando não está em contexto ou quando os caminhos relevantes não estão no pacote ativo. Primeira correspondência por entity_id, scene_id e arc_id; aliases/tags são recuperação secundária.
4. Selecionar perfis/arcos, sem escanear toda a história. Quando o detalhe for decisivo, abrir evento original em buffer ou arquivo histórico (por event_id/faixa); resumos nunca são prova suficiente.
5. Montar novo context_packet com proveniência. Ausência no índice NÃO equivale a ausência no mundo; registrar NEEDS_EVIDENCE ou ler fonte adicional.
6. Narrar somente depois de commit + readback confirmado para qualquer novo delta, conforme G19 após eventual migração aprovada.
7. Se entidade nova aparece em LIVE antes do próximo arquivamento do índice, registrar `pending_index_updates` no próprio LIVE para não criar falso negativo. Esses campos serão consolidados em commit multi-arquivo.
8. Não atualizar `HISTORY_INDEX.active_scene` em todo corte: a cena vigente é exclusivamente LIVE.scene.scene_id. Índice apenas armazena relações estáveis e ponteiros de histórico.

## Política de conhecimento e causalidade
- `PLAYER_DECLARATION` ≠ ação automaticamente resolvida; `PLAYER_INTENT` ≠ êxito.
- `NPC_CLAIM` ≠ fato do mundo; rumor mantido com autor e origem.
- NPC só conhece o que presenciou, lhe foi comunicado ou foi demonstrado por evento fundamentado.
- Ouvinte que recebe uma declaração sobre promessa antiga não passa a ter presenciado a promessa original.
- NPC possui agência e não recebe script fechado de comportamento por sua ficha.
- Inconsistências entre contrato canônico, decisões, eventos e projeções = CONFLICT/NEEDS_EVIDENCE, não retcon.
- Segredos do narrador não devem ser incluídos inadvertidamente em pacote que o jogador receberá integralmente.

## Operações e limites
A API GitHub contents `update_file` substitui o texto inteiro do LIVE. O modelo deve verificar integralidade estrutural antes de gravar; não reconstituir por memória quando a fonte já se perdeu. O SHA protege a substituição contra usar blob errado e o readback verifica conteúdo, mas **o GitHub não impede erro de narrativa ou um resumo omitir informação**. Confiabilidade semântica exige testes e revisão humana.

Git versiona tudo: a recomendação NÃO é copiar LIVE_vNNN em cada turno. Histórico é commit + arquivos de eventos imutáveis por procedimento, não por garantia automática da interface.

## Governança
A DEC-CR-014 continua **APROVADA** para a crônica em Drive. Esta arquitetura requer decisão explícita nova para promover persistência Git. G19, G23 e proteção CANÔNICO/FECHADO/APROVADO/CONGELADO não são relaxados. Ledger técnico histórico vazio permanece não migrado até reconciliação independente.

## Critérios ainda pendentes
Teste de novo chat REAL no ChatGPT Web; auditoria semântica com cenas livres e múltiplos NPCs; simulação de erro real de rede/timeout (em vez de apenas interrupção controlada); benchmarking de 30k caracteres e transformação integral do LIVE; corpus de história real reconciliado sem invenção.
