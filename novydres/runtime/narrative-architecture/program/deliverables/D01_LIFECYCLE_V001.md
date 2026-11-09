# NOVYDRES — D01 · Fluxos de autoria, estados e gates V001
STATUS: PLAYER_SAFE | PROPOSTO | NÃO OPERACIONAL. Não abre C06.

## 1. Pipeline
(1) READ_SOURCE: HEAD, ciclo maior numericamente, predecessor e SHAs de refs, LIVE, evento; registrar origem e lacunas. (2) HISTORIOGRAPHY: fatos jogados com provenance e author_known/UNKNOWN; nunca trocar índice derivado por evento técnico COMMITTED. (3) PLAN: crônica/marco/trama/stories/atores/pistas/relógios/consequências. (4) TRUTH_LOCK: se mistério significativo, definir em canal de acesso compatível verdade e variante antes da primeira pista. (5) REVIEW: autorizações e qualidade literária/técnica. (6) SCENE_PREFLIGHT: permissão operacional própria, sem decorrer da existência do plano. (7) NARRATE: só Narrador pode conduzir 1 cena, jogador controla PC. (8) G28_CLOSE: uma transação atômica, readback, handoff Dramaturgo. (9) DRAMATURGO_REVIEW: provocação completa frente ao último evento; só novo ciclo autorizado libera Narrador.
A sequência D01–D12 é projeto editorial em branch, **separada** da máquina de cena em master. Não há trabalho autônomo entre chats.

## 2. Gates ortogonais e donos
- SOURCE_INTEGRITY (auditor): refs do ciclo, versão, SHAs e last_event_id coincidem; divergência decisiva => STOP_CONFLICT, sem presunção de dados.
- AUTHORIAL_TRUTH_LOCKED (dramaturgo): LOCKED + versão/variante e fonte anteriores à primeira pista crítica; NOT_APPLICABLE em histórias sem mistério; FAIL não permite pista investigativa significativa.
- DRAMATURGO_READY (dramaturgo): plano completo, pressão independente, conflito real, saídas, suficiência D1, ritmo e horror; falha => REVISE.
- SCENE_READY (preflight Narrador): estado elegível, plano compatível com checkpoint, NPC knowledge, stakes, recusa/falha e pre-roll; falha => HOLD.
- PENDING_PLAYER_APPROVAL (jogador): retcon, promoção, mudança de congelado requer decisão expressa com ID; sem aprovação => nenhuma aplicação.
- READBACK_PASS (publicador): commit/lease/branch/blob SHA e dados relidos; erro => NOT_PUBLISHED / PENDING_PERSISTENCE.
- NARRATOR_PERMISSION (ciclo+entrada do jogador): READY_FOR_NARRATOR + revisão no mesmo event_id + SCENE_READY + consentimento de handoff + uma única cena. D01 PASS não concede permissão.
- D01_PROPOSAL_GATE (auditoria): proposta completa, compatível D1/D2/H, sem alteração do master e com sigilo; se FAIL => remediar D01, NÃO avançar D02.

## 3. Desvios e iniciativas
Recusa ou abandono: não obrigar retorno; pode fechar história e deixar trama viva sob ação de NPC. Falha: consequência com escala proporcional, alternativa legítima e estado rastreado. Sucesso antecipado: respeitar e adaptar outras oportunidades. Morte/saída de NPC: sua função pode cessar; não ressuscitar nem implantar substituto ad hoc. Relógios: tick somente por trigger causal, ator capaz, fonte e estado. Suspensão: exige motivo/owner/revisão, sem closure fictício.
Nova trama surgida em cena: o Narrador pode registrar evento local e THREAD; se passar a requerer verdade secreta, antagonista persistente ou culpado, marcar AUTHORIAL_REVIEW_REQUIRED e submeter ao Dramaturgo antes de transformar em PLOT. Reações improvisadas locais não são carta branca para retcon.
Offscreen: sem PC, o mundo pode continuar através de atores com capacidade e trigger estabelecidos; a ocorrência só entra no ledger quando evidência diegética/operacional puder ser registrada. Decurso de tempo administrativo não é fato.

## 4. Transições e critérios
PLOT DRAFT->LATENT->ACTIVE->ESCALATING, com possibilidade de ACTIVE<->SUSPENDED e terminal RESOLVED/FAILED/ABANDONED_WITH_CONSEQUENCES/RESOLVED_OFFSCREEN_WITH_EVIDENCE/SUPERSEDED_WITH_PROVENANCE; terminal é imutável como evidência e gera novo estado versionado se necessário. STORY DRAFT->ELIGIBLE->IN_PLAY->CLOSED_* ou SUSPENDED->IN_PLAY; não encadear cenas automaticamente.
MARCO possui funções D1 e fechamento apenas por Coverage+Coherence+Consequence, fonte, autoridade e pacote de consolidação, sem recompensa por evento inserido. D2 selection_method exige prova de RNG quando declarado D2_RNG_ELIGIBLE; CHR001_CURATED_SESSION é adaptação local, não equivalente.
Fase editorial Dxx PROPOSED->AUDITED->PASS/FAIL/PENDING_PLAYER_APPROVAL/STOP_CONFLICT; PASS libera apenas **mandato documental** Dxx+1; D12 só libera prompt Narrador com aprovação expressa, promoção permitida, READY_FOR_NARRATOR e readback operacional.
