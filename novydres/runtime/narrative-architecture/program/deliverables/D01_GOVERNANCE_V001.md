# NOVYDRES — D01 · Autoridade, autoria, proveniência, sigilo e retcon V001
STATUS: PLAYER_SAFE | PROPOSTO | SEM MUTAÇÃO DE CÂNONE.

## Precedência e responsabilidades
CANÔNICO/FECHADO e APROVADO/CONGELADO prevalecem; .AGENT/.CONTEXTG e decisões vigentes, D1/D2/H, G19–G28, contratos locais e de orquestração conforme autoridade própria. Propostas D01–D12 são camada editorial subordinada, nunca vigência implícita. Ciclo numericamente mais recente e validado é cursor narrativo; manifesto é fonte normativa e pode preservar checkpoints históricos. Divergências devem ser **registradas** e escaladas, nunca reparadas silenciosamente.
Dramaturgo cria proposta e checa coerência global, agentes, pistas, custos, lock e revisão após cena; Narrador adjudica sob preparação aprovada e vive o mundo, mas não decide PC nem inventa solução de mistério; jogador detém ações/interioridade do protagonista e aprova retcons/promoções; editor/governança arbitram mudanças normativas.

## Proveniência por afirmação
record_kind = CANON_EVENT / PLAYER_DECLARATION / NPC_CLAIM / NARRATOR_ADJUDICATION / CANON_SOURCE / GM_PREPARED / GM_LOCKED_TRUTH / CONDITIONAL / EDITORIAL_RECONSTRUCTION / NEW_AUTHORIAL_DESIGN_POST_HOC / PROPOSED_RETCON / UNKNOWN.
original_author = PLAYER / NARRATOR / DRAMATURGO / SHARED_EMERGENT / AUTHOR_UNKNOWN.
fact_status = CONFIRMED / CLAIMED / PROPOSED / CONDITIONAL / UNKNOWN / CONFLICT.
Campos: source_path + blob_sha + anchor/event_id, as_of, diegetic_time_or_UNKNOWN, generated_at, authored_before_event_or_UNKNOWN. Autoria UNKNOWN não vira autoria da IA por conveniência. GM_PLAN não vira CANON_EVENT por estar no GitHub; testemunho NPC_CLAIM não vira verdade objetiva; silêncio não equivale a falso; atlas derivado e índice parcial não são ledger técnico COMMITTED.
Conhecimento requer owner_id, aquisição demonstrável, checkpoint e epistemic_status. Relações são dirigidas, com fonte por aresta, e permitem B=UNKNOWN; humor H e P permanecem sob seu contrato.

## Retcons como proposta, nunca execução automática
GAP_FILL_PROSPECTIVE: preencher espaço futuro sem reescrever passado. INTERPRETATION: leitura alternativa explicitamente baseada em fonte, sem nova ocorrência. RETCON_SOFT: modificação de fato/implicação consolidada; consentimento expresso. RETCON_HARD: substituição de evento fechado; consentimento expresso e análise de efeitos. CANON_CONFLICT: choque de autoridade, bloco de promoção.
Registro obrigatório: change_id, affected_paths/event_refs, before_claim, after_proposal, sources, temporal_cascade, npc_knowledge_impact, mechanical_impact, alternatives, approval_required, approval_decision_id, status. SOFT/HARD necessitam decisão positiva inequívoca antes de aplicar, por COW e readback; nada in-place, nada de aprovação inferida por silêncio ou início do próximo chat. Não editar documento congelado sem ordem expressa do proprietário e autoridade competente.

## Sigilo e segurança
PLAYER_SAFE é a única classificação publicada na resposta do jogador; GM_HIDDEN é informação de bastidor; MIXED_REQUIRES_DERIVATION exige extração segura. IDs opacos, estado, SHA e rótulos administrativos são aceitáveis; não mostrar identidade oculta, solução, motivação secreta, escolhas futuras ou um título de arquivo revelador. Os nomes D01 são neutros.
Repositório privado **não** impede o proprietário de abrir seu conteúdo; pasta "GM" e classificação editorial não são ACL. Se sigilo real do próprio jogador for indispensável, exigir armazenamento com credenciais realmente separadas **antes de persistir segredos**. D01 não grava segredos, e D07 não pode marcar AUTHORIAL_TRUTH_LOCKED de investigação jogável usando só placeholder sem lock protegido e verificável.
Commit, README, PR, diagrams, prompt, handoff e saída pública passam por revisão de spoiler; contagem/IDs não podem codificar segredos descobríveis.

## Qualidade e testes
QC_TECH: links tipados/evidência, status, source hashes, truth_lock, duas rotas independentes de pistas críticas, NPC epistemology, clock causal, terminais, COW, gates. QC_LIT: horror gótico-punk com atrito social, autonomia NPC, agência PC, custos coerentes, contraste humano, densidade e elipses relevantes. Validação automática não substitui editor.
Alarme de estagnação inicia REVISÃO editorial, não um ataque criado para o PJ. Retcon e suspense não servem para encobrir uma falta de objetivo ou terminal verificável.
