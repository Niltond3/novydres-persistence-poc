# ADR-001 — sucessão operacional E02/E03

**Aprovação:** proprietário respondeu “aprovo” em 13/11/2026 à proposta E01, à promoção da árvore exata, sucessões operacionais, correção controlada dos gateways e recuperação de incidente. E02 promoveu tree `4e08b9e4559922f711669294718fbdc74780d9d8` no commit `74777a6328439eb02825cc09172fcb9244a1522f` com único parent `c9fcfc0c558cd17d58ec8c8272da3ed70182ff37`. Checkpoint `checkpoint/adr001-precutover-20261113` conserva a master antiga **somente para incidente**, nunca como fallback de runtime.

**Gatilho de eficácia:** E03_PASS documentado com CI/readback no HEAD final. E02/E03 não autorizam iniciar crônica, alterar fatos protegidos, XP/FV nem resolver `CONFLICT-001`, `CONFLICT-002` ou `CONFLICT-003B`.

## Autoridade única
Master atual por SHA é única referência operacional. Entradas: `AGENTS.md`, `CONTEXT.md`, `catalogo.json`, lidas no mesmo commit. Resolver ID exato e arquivos do subject proprietário; nenhuma rota antiga, alias, wrapper, redirecionamento ou fallback. SHAs, árvore candidata e checkpoints antigos são fontes para proveniência/incidente. O catálogo é derivado, sem duplicar verdade.

**Sucessões autorizadas:** G19/G23/G24 e DEC-CR-014 cedem ao Git-native com estado atual por assunto, texto histórico integral, correção explícita e histórico Git (DEC-16/23/24). G26/G28 e políticas editoriais pertinentes seguem DEC-18 e `novydres/sistema/narrativa/contrato.md`: condução proporcional, agência do PJ, NPCs autônomos, regras V5 vigentes e elipses facultativas. Não reintroduzir manifesto/ciclo como contrato ou fonte ativa.

## Uma transação por resposta futura autorizada
Fixar HEAD master e permissão. Selecionar assuntos por IDs, conferir owners, fonte e segredo. Preparar texto integral e mudanças materiais num **único conjunto de blobs**, com `tx_id` estável/fingerprint; não criar commit por microação nem buffer até fim da cena. Criar blobs/tree/commit com parent único no HEAD esperado, atualizar master com `expected_sha` e `force=false`, e fazer readback de ref, parent, tree, `tx_id` e blobs antes de entregar a narrativa.

Se ocorrer confirmação perdida, procurar o `tx_id` já publicado e comparar fingerprint e efeitos. Identidade igual: `NO_OP_VERIFIED`, sem reescrita. Divergência ou stale HEAD: STOP/RECONCILE, não retry cego. Nunca rerrolar, duplicar XP/FV, inventar estado ou declarar persistência sem readback. Provas remotas devem usar refs descartáveis, nunca dados reais da crônica.

## Sigilo, riscos e incidente
Distinguir conhecimento do agente, jogador, PJ e NPC; preparar oculto não é fato jogado. Rótulos textuais não são ACL externa. Preservar 38 escopos/47 registros, 44 tramas, C45 mortal e recursos sem nova operação.

119 sucessões comportamentais D05 seguem não certificadas; revisão D07 contextual por agente não é certificação humana, revisão V5 integral ou garantia de semântica futura. Preservar conflitos 001/002/003B, mídias opcionais e índice histórico parcial.

Falha após cutover: suspender ativação, preservar commit/refs e evidência, diagnosticar e solicitar decisão material de recuperação. Não restaurar master silenciosamente, não force-push, não usar fallback. A próxima cena depende de autorização própria, mesmo após E03_PASS.
