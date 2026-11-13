# CHR-001 / Ativação controlada do módulo de predisposição V1
STATUS: STAGED, IMPLEMENTAÇÃO DISPONÍVEL; NÃO ATIVADO NO CICLO V0012.
Checkpoint inspecionado: master 3eecfad9f33965ea8a3106d5a069673d04712f2e, CYCLE_V0012 READY_FOR_NARRATOR, C14 CLOSED, C15 NOT_STARTED; LIVE_v027, episódio M2.04_v013 e dossiê V7 permanecem intocados.

## Motivo do gate
O esquema CYCLE_SCHEMA_V1 declara refs com additionalProperties=false e o validador permite transições Narrador/Dramaturgo específicas. Um commit técnico não é uma revisão do Dramaturgo, não é uma cena, não pode avançar o CYCLE e não pode modificar o LIVE corrente. Não inserir refs.social à força em V0012 nem criar ciclo falso. O módulo novo é funcional e testável isoladamente, mas a régua fica inativa até promoção prospectiva e verificável.

## Caminho seguro de ativação
1. Permitir C15 somente com ciclo vigente V0012 e suas regras existentes; não impor régua em cena que já foi autorizada. Não iniciar C15 como parte da instalação.
2. Quando C15 for encerrada e o Narrador executar seu G28, na MESMA transação atômica de encerramento poderá produzir STATE_V002.json (ou sucessor COW, somente se houver base social efetivamente avaliada e auditável), LIVE sucessor com campo opcional `npc_disposition_state_ref:{path,blob_sha}`, e CYCLE sucessor SCENE_COMMITTED/READY_FOR_DRAMATURGO. O campo adicional fica exclusivamente no LIVE; o CYCLE_V1 preserva exatamente o contrato de refs. Reconciliar SHAs antes de atualizar HEAD e fazer readback.
3. O Narrador não deve retroagir estados de humor a C15. A versão ativa pode iniciar com perfis prospectivos e mood_window=null. `activation_event_id` pode usar o último evento real da cena encerrada como marco administrativo de vigência futura, sem atribuir um evento emocional fictício.
4. O Dramaturgo da transição seguinte lê STATE vigente, contrato local e fatos da última cena; reavalia integralmente M2.04 e emite ciclo válido READY_FOR_NARRATOR ou fechamento, sem revelar GM_HIDDEN. Só após isso a PRÓXIMA cena pode usar a régua.
5. Em caso de conflito com o esquema LIVE, a governança ou com o handoff, bloquear a ativação e manter módulo STAGED; nunca editar históricos/canônicos ou criar commit administrativo que pareça cena fictícia.

## Auditoria do estado na ativação
- `status` troca de STAGED para ACTIVE somente em novo STATE_VNNN; `previous_version` aponta para anterior.
- `activation_event_id` deve ser evento real no episódio da transição; humor das interações anteriores não é inventado.
- LIVE de ciclo sucessor aponta caminho e Git blob SHA do STATE novo; validação Node `VALIDATOR_V1.mjs` confere âncora histórica, ponteiro ativo e faixas.
- Os perfis iniciais de Mary, Mikahel, Pavel e Anna são hipóteses editoriais limitadas por eventos existentes, não mudanças na narrativa. O Dramaturgo pode revisá-los prospectivamente se houver fonte incompatível.
- Sem ajustes automáticos a XP/FV, relacionamento persistente ou poderes.

## Operação e falhas
Apenas GitHub como fonte operacional, COW obrigatório, um commit por transição e readback HEAD/arquivo/SHA. Em G26 PENDING manter buffer no chat e NÃO passar handoff de novo chat até gravar e verificar. Na ausência de RNG verificável, mood_window method=NEUTRAL_FALLBACK, não fingir dados.
