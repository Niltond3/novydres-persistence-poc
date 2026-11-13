# NOVYDRES · ADR-001 · E01 — proposta de cutover para aprovação · 2026-11-13

**Estado: E01_PREPARATION_COMPLETE_PENDING_OWNER_APPROVAL.** Esta proposta é PLAYER_SAFE, não operacional e não concede E02/E03. D07 recebeu revisão contextual de agente em sessão distinta; consulte `../fase-d/revisao-contextual-d07-2026-11-13.md`.

## Snapshots e decisão

- Candidata examinada antes de publicar este relatório: branch `design/subject-oriented-migration`, HEAD `57c6ca324911da96cbadf6b701b2c8aa42c997ed`, tree `94453cddee9a636871a4b6080a61640dba18f4ad`.
- Baseline master somente leitura: HEAD `c9fcfc0c558cd17d58ec8c8272da3ed70182ff37`, tree `4894bebafcc872dcd7c772ea4d34e5d54079b810`.
- Comparação GitHub antes do registro E01: `diverged`, 170 commits à frente/28 atrás; a listagem de arquivos do compare tem limite de página, não é auditoria completa do diff. A árvore Git recursiva candidata é não truncada. **Não efetuar merge automático, rebase silencioso ou restauração da árvore antiga.**
- O commit documental que publica E01 muda o HEAD/tree da branch, mas não o código/runtime validado. **Para E02, usar EXCLUSIVAMENTE o HEAD e a tree finais confirmados por readback remoto e reproduzidos no handoff, nunca inferir a referência da linha anterior como HEAD final.** Se houver novo commit, reavaliar mudanças materiais.

## Evidências aceitas para a proposta

- A: `A_DESIGN_EXECUTION_PASS` (A01–A07).
- B: `B_PASS_SCOPED` conforme DEC-27; não duas rotas Web/Codex obrigatórias.
- C: `C08_PASS_SCOPED`, catálogo, validador, fluxo seguro e provas reais no GitHub.
- D: D01–D03 concluídas; D04/D05 `PASS` por risco explicitamente aceito; D06 `PASS` técnico pelo run **43364072558** (dois jobs SUCCESS); D04/D05 regressão **43364329372** SUCCESS; D07 `PASS_ESCOPADO` após parecer por agente e confronto direto de fontes. Sem alegar 119 equivalências comportamentais certificadas.
- Cobertura: 1.029 origens classificadas; 438 fontes históricas D04 e 399 origens D05; 153 subjects; 38 atores, 47 conhecimentos, 44 threads. C45 preservado (C01 fechado/C02 não iniciado), XP/FV e fronteira de conhecimento. Scanners e árvore Git demonstram 0 caminhos legados operacionais e 0 symlinks na candidata; não garantem ausência de dependência fora do repositório.
- ADR-001 essencial: nomes estáveis Git/owner por assunto, catálogo derivado por snapshot, separação epistêmica e de divulgação, histórico literal protegido, transação atômica CAS/tx_id/readback, recuperação sem rerrolar, um runtime proposto com entrada `AGENTS.md → CONTEXT.md → catalogo.json`, sem alias/redirect/fallback. A qualidade de jogo real somente pode ser verificada após promoção autorizada.

## Plano de E02 — somente depois de aprovação explícita

1. Reconsultar HEADs e trees de `master` e candidata, verificar que a master continua na baseline autorizada; se divergir, **bloquear**, reconciliar diferenças por fonte/autoridade e repetir apenas regressões afetadas. Conferir delta desde a revisão D07, os documentos sucessores, guardrails de sigilo, scanner `--final`, catálogo `--check` e CI ainda válidos.
2. Formalizar no ato de aprovação a sucessão operacional Git-native de G19/G23/G24 e DEC-CR-014/editorial pertinente para a arquitetura ADR-001, DEC-18 (G26/G28), com uma transação por resposta de jogo, publicação+readback antes da entrega e pausa em falha. Preservar textos históricos e não tocar CANÔNICO/FECHADO ou APROVADO/CONGELADO. Não selecionar CONFLICT-001/002/003B sem fonte/decisão; se qualquer um for material ao novo runtime, requer decisão específica antes de E02.
3. Criar e verificar um checkpoint remoto imutável de referência à master pré-corte (por exemplo ref de segurança `checkpoint/adr001-precutover-20261113` apontando ao SHA antigo; sem force), registrando seu SHA. Esse checkpoint é para incidente, **nunca fallback corrente**.
4. Construir **um** novo commit de promoção na master: `tree = tree exata da candidata aprovada` e `parent = SHA atual de master aprovado`; manter arquivo/estado histórico do Git, não mesclar paths antigos. Atualizar `master` com `expected_sha = master anterior` e `force=false`. Se a lease falhar, não retry cego: ler e reconciliar.
5. Fazer readback remoto de ref, parent, commit e tree (comparar exatamente com a candidata), conferir os três gateways, resolução de IDs, ausência de caminhos/consumidores legados e invariantes C45. Só registrar `E02_PASS` após confirmação inequívoca. Não narrar ou iniciar C02.

## E03 e plano de incidente

- Após E02 comprovado: CI real no HEAD master promovido; scanner de **toda árvore** e referências operacionais controladas; catálogo e schemas; testes negativos de PLAYER/segredo e UNKNOWN, recuperação C45, XP/FV, 44 threads, três gateways e 9 grupos de funções por cenários críticos; smoke de transação em destino descartável, sem campanha real. Prova negativa de stale HEAD, idempotência/readback e nenhuma rota legada. A liberação final só se dá após `E03_PASS`; nenhum atalho para retomar a cena.
- Falha **antes** da troca da ref: master não muda, candidato permanece; sanar na candidata e rever diff. Falha **após** troca: suspender runtime/narrativa, preservar commit promovido e diagnóstico, comparar estado e, se necessário, solicitar decisão expressa de recuperação (commit corretivo ou retorno controlado). Nunca `force-push` ou voltar silenciosamente ao legado.
- Limitações aceitas: 119 comportamentos históricos não certificados individualmente; índice histórico não exaustivo; 5 mídias opcionais dispensadas e dependências externas não certificadas universalmente; revisão D07 por agente, não humana/cega; funcionalidade narrativa pós-E02 depende de smoke E03. Conflitos editoriais 001/002/003B não resolvidos por conveniência. Se algum desses itens se tornar essencial ao runtime, bloquear a transição afetada até decisão.

## Decisão solicitada ao proprietário

**Aprovar ou rejeitar E02** para promover a árvore candidata exata e ativar as políticas sucessoras descritas, com uma única autoridade Git-native e ZERO LEGADO. E03 só será executada após E02 efetivamente verificada. Aprovação não autoriza mudar fatos, inventar XP/FV, iniciar cenas nem suprimir conflitos materiais. Resposta inequívoca sugerida: **“Aprovo o cutover E02 conforme a proposta E01, inclusive as sucessões operacionais e o plano de contingência; preservar conflitos editoriais não resolvidos.”**

