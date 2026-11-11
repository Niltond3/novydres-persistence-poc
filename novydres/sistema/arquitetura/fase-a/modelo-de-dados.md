---
id: arch-phase-a-data-model
status: CANDIDATO_PENDENTE_APROVACAO
scope: NOVYDRES_GLOBAL
classification: PLAYER_SAFE
---
# Modelo de dados e ontologia verificável (candidato)

## Entidades e vínculos
Subject: {subject_id, kind, owner_scope, status, visibility, source_refs[], source_assertions[], related_subject_ids[], schema_version}. Tipos: world-location, history-topic, organization, lineage, character, chronicle, story, plot, thread, episode, scene, beat, event, roll, decision, approval, correction, source, orchestration-cycle. Um subject pode ter documentos opcionais; não exigir placeholders para tipo sem dados.

Chaves de referência: ref por {id, kind, scope, source_commit?}; normalizar para ID em índices e conteúdo. Relações: {relation_id, from_subject_id, to_subject_id, predicate, owner_subject_id, scope, valid_from?, valid_to?, source_record_ids[], epistemic_status, visibility}. relation_id, direcionalidade, âmbito, tempo e dono obrigatórios. Inversa derivada; grau de confiança não autoriza mesclar NPCs homônimos.

Afirmação substantiva: {assertion_id, subject_id, field, value, epistemic_status, attribution_actor_id?, evidence_refs[], valid_time, recorded_time?, visibility, owner_scope}. Status: CONFIRMED, NPC_CLAIM, GM_PREPARED, CONDITIONAL, UNKNOWN; categorias de evento ainda distinguem PLAYER_DECLARATION, PLAYER_INTENT, NPC_ACTION, WORLD_EVENT, GM_PROPOSAL, CANON_SOURCE, MECHANICAL_RESULT. UNKNOWN não vira false, e ausência de registro não vira UNKNOWN estabelecido.

Conhecimento separado: AGENT_KNOWLEDGE (material acessível a agentes com função), PLAYER_KNOWLEDGE (revelado ao usuário), PC_KNOWLEDGE (visto pelo PJ), NPC_KNOWLEDGE (por indivíduo e tempo); cada item tem assertion_id, actor_id, as_of_event_id e evidence/ref. Acesso de agente não implica divulgação ao jogador, nem conhecimento ficcional de personagem. Visibility inclui PLAYER_SAFE, PC_KNOWN, NPC_BELIEF, GM_HIDDEN, SYSTEM_AUDIT; classificações são filtros editoriais, NÃO controle de acesso Git.

## Hierarquia narrativa e estados
- chronicle contém story, plot/thread e episode; episode agrupa scene; scene pode referenciar beat condicional. A cena não define retroativamente uma ação de personagem.
- plot/thread pode cruzar episódios, tem proprietário de assunto, estado com evidência, restrições e dependências; fechada uma cena, o fio pode continuar aberto.
- event refere chronicle_id, scene_id, actor_id, source_type, original_declaration_quote quando existir, source_message_ref quando existente, event_time ou UNKNOWN, location_id ou UNKNOWN, causal_event_ids, record IDs de rolls, deltas, visibility, estado de persistência.
- roll é registro imutável por roll_id: faces transcritas, método de geração e auditabilidade separada. CHAT_UNVERIFIED não equivale a RNG_VERIFIED; jamais rerrolar para melhorar auditoria.
- decision e approval preservam autoridade, escopo, data, conteúdo exato/autorização, predecessores e efeito prospectivo. Mudança de política cria sucessor sem editar prova antiga.
- correction aponta target_record_id e justificativa, com before/after sem adulterar fonte antiga. Eventos nunca são silently rewritten.
- estado/atual.json é materialização por commit de event IDs confirmados + correções aplicáveis e approved decisions; guarda checkpoint, recursos, version pin e projection_source_commit. Se irreconciliável -> BLOCKED_CONFLICT, não atualizar silently.

## Registro físico Git-native
Cada evento, rolagem, decisão, aprovação ou correção tem arquivo único em registros/<classe>/<id-normalizado>.json. ID estável e global dentro de seu namespace; preservar IDs históricos originais como source_id e seu SHA de fonte, sem criar alias executável. Para novos IDs: prefixo evt/roll/dec/app/corr + identificador único; checagem de unicidade do catálogo. Registros são INSERT-ONLY após COMMITTED; correções são arquivos novos referenciando o anterior. Antes de concluir COMMITTED verificar a árvore Git publicada e readback; um arquivo preparado mas não promovido não é COMMITTED. Política de append-only exige diff e branch protection, não é garantia física infalível contra administrador reescrever Git.

História textual literal, quando prova primária, deve ser preservada sem reinterpretação em fontes/ (cópia textual de proveniência) ou pela própria história Git; converter narrativa em eventos técnicos exige evidência real e revisão, nunca inferir que um resumo é ledger válido. Um arquivo histórico repetido com conteúdo parcialmente distinto precisa de classificação: histórico preservado, autoritativo, duplicado equivalente ou CONFLICT, com SHA. Linhagem entre apresentações deve ser rastreável.

## Schemas e normalização
Os dois JSON Schema candidatos ao lado especificam envelopes mínimos. Na C completar schemas específicos (event/roll/decision/approval/correction/chronicle/relation/knowledge/manifest/cycle), validate referential integrity e compatibilidade de tipos; não instalar como runtime na A. Em schema_version incompatível, migração explícita antes de usar; não aplicar coercion automática.
