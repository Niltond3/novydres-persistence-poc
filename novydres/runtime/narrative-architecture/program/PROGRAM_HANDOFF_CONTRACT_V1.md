# NOVYDRES — CONTRATO DE HANDOFF INCREMENTAL V1
Status: PLAYER_SAFE, regras de coordenação D01–D12. Aplicado por mandato do usuário, mas não altera orquestração vigente nem documentos congelados.

## Resultado obrigatório de cada chat Dnn
1. Exato branch/repo HEAD antes/depois, commit SHA REAL, ciclo ativo de master e event_id verificáveis; reler todos após publicação. Se sem commit: NOT_PUBLISHED.
2. Arquivos PROPOSTOS publicados no branch de design: paths + blob SHA, versões e fontes; identificar trabalho feito, não feito, conflitos, testes de schema/semântica e limitações.
3. Controle de aprovação: PASS/FAIL/PENDING_PLAYER_APPROVAL/STOP_CONFLICT; retcon precisa consentimento com ID, nunca inferido por iniciar próximo chat.
4. Handoff estruturado + PROMPT Dnn+1 completo no GitHub. PROMPT não deve depender de memória do chat, usar caminhos exatos (sem corpo secreto), papel, regras de escopo e critério de saída.
5. Resposta pública apresenta resultado sem spoilers + PROMPT pronto. Se gate FAIL, entregar REMEDIATION_PROMPT da fase atual, não emitir Dnn+1 como READY.
6. D12: somente gerar prompt NARRADOR quando os requisitos de ciclo READY_FOR_NARRATOR E autorização de cena existirem. Na ausência disso, gerar REMEDIATION_PROMPT ou aprovação de integração, sem liberação fictícia.

## Modelo de estado legível por máquina
{ "program_id":"NOVYDRES_NARRATIVE_D00_D12_V1", "phase":"D01", "status":"PASS|FAIL|PENDING_PLAYER_APPROVAL|STOP_CONFLICT", "repository":"Niltond3/novydres-persistence-poc", "design_branch":"...", "design_head_sha":"...", "master_head_sha_at_review":"...", "cycle":{"path":"...", "blob_sha":"...", "next_role":"..."}, "inputs":[{"path":"...", "blob_sha":"..."}], "outputs":[{"path":"...", "blob_sha":"...", "status":"PROPOSED"}], "tests":[{"id":"...", "result":"PASS|FAIL|N_A"}], "unresolved":[{"id":"...", "type":"GAP|CONFLICT|PLAYER_DECISION", "public_label":"sem spoiler"}], "next_prompt_path":"...","next_phase":"D02", "spoiler_class":"PLAYER_SAFE" }
Nenhum SHA placeholder deve aparecer como se fosse validado. No prompt público, não enumerar planos ocultos concretos; citar apenas paths opacos/manifesto de baixo risco e invariantes.

## Separação de funções
Dramaturgo autor: planejamento e validação, nunca interpretar fala do jogador nem rolar.
Narrador: somente depois do gate, conduz uma cena com NPCs autônomos e escolhas livres, sem criar verdade secreta a posteriori.
Jogador: decisões de PJ, aprovações explícitas de retcon, contrato e promoção.

## Riscos e bloqueios
D00 não congelou arquitetura. D01 não pode declarar master vigente; D02 não pode converter hipótese passada em fato; D07 não pode inventar autor original; D11 deve ser adversarial, independente. D12 precisa readback e aprovação. Qualquer desvio interrompe handoff até remediação.
