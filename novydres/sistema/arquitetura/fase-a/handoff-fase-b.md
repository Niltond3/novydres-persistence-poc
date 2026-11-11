---
id: arch-phase-b-handoff
status: PHASE_A_APPROVED_PHASE_B_NOT_STARTED
classification: PLAYER_SAFE
phase: A
source_approval: novydres/sistema/arquitetura/fase-a/aprovacao.json
---
# NOVYDRES — Handoff da Fase A para B

A arquitetura da Fase A do ADR-001 foi **aprovada expressamente pelo jogador em 2026-11-11** com a declaração literal "Aprovo a arquitetura". O escopo é desenho: não há cutover, nenhuma alteração do runtime, nenhuma política substituída em master e nenhuma narrativa alterada.

## Baseline comprovada no handoff
- Repositório: `Niltond3/novydres-persistence-poc`
- Design: `design/subject-oriented-migration`; commit aprovado de especificação: `401d5706ef9f4967efc5d300652fd77d4edb3dae`.
- Master observada no momento da aprovação: `1af5e5549120be66115bc8c8c4c61d0ea3d7a3f2`, **não é pin duradouro**. O HEAD já avançou desde a auditoria A (que viu `44b5c2348ccd3bb2ea5edaaa918f2f55b197321b`). Abrir B com re-leitura de HEADs e detectar qualquer outra mudança.
- Approval status source: `novydres/sistema/arquitetura/fase-a/aprovacao.json`; o arquivo histórico `decisoes-e-gate.json` preserva o estado ANTERIOR à aprovação, não é uma negativa atual.
- ADR aprovado para desenho: `novydres/sistema/arquitetura/adr/001-subject-oriented.md`.
- Pacote integral de A: `novydres/sistema/arquitetura/fase-a/index.md` e todas suas dependências, incluindo esquemas candidatos e matriz de conflitos.
- Não presumir que CYCLE_V0038 / MANIFEST_V53 continuam sendo atuais: a descoberta operacional sempre usa highest **valid** ciclo + manifesto + pins exatos.

## Prompt completo de execução para chat limpo — utilizar após encerrar este chat

# NOVYDRES — MIGRAÇÃO ARQUITETURAL · FASE B (PROTÓTIPO)

**Missão:** Executar exclusivamente FASE B — protótipo isolado por assuntos, sem migração operacional. A Fase A está APPROVED_FOR_DESIGN_ONLY; sua aprovação consta em `novydres/sistema/arquitetura/fase-a/aprovacao.json` e readback Git da branch de design.

**Repositório:** `Niltond3/novydres-persistence-poc`. **Branch de design:** `design/subject-oriented-migration`. Branch operacional `master` estritamente somente leitura. Ler os HEADs atuais antes de qualquer decisão; `401d5706ef9f4967efc5d300652fd77d4edb3dae` é o commit de arquitetura aprovada, e `1af5e5549120be66115bc8c8c4c61d0ea3d7a3f2` é apenas a master observada no handoff.

**Fontes obrigatórias:** `novydres/sistema/arquitetura/adr/001-subject-oriented.md`; `novydres/sistema/arquitetura/fase-a/index.md`, `novydres/sistema/arquitetura/fase-a/topologia-e-ownership.md`, `novydres/sistema/arquitetura/fase-a/modelo-de-dados.md`, `novydres/sistema/arquitetura/fase-a/git-e-roteadores.md`, `novydres/sistema/arquitetura/fase-a/auditoria-e-mapa.md`, `novydres/sistema/arquitetura/fase-a/validacao-e-metricas.md`, `novydres/sistema/arquitetura/fase-a/fases-b-e.md`, `novydres/sistema/arquitetura/fase-a/decisoes-e-gate.json` (histórico), `novydres/sistema/arquitetura/fase-a/aprovacao.json`, `novydres/sistema/arquitetura/fase-a/handoff-fase-b.md` e os dois schemas candidatos. Ler também `novydres/.AGENT.md`, `novydres/.CONTEXTG.md` e validar o mecanismo corrente de autoridade por ciclo, manifesto e hashes, sem inferir uma versão pela numeração de arquivo isolado.

**Primeiro gate:** Reconciliar explicitamente a divergência entre design e master, incluindo commits publicados depois de A, sem merge cego, sem alteração de master e sem fazer pins de snapshots mistos. Registrar cada conflito necessário. Não permitir que o branch antigo retroceda eventos, ciclos, gates ou estado.

**Execução:** Criar somente cópias candidatas de 1 NPC, 1 trama, 1 história e 1 estado usando os novos assuntos, index, IDs e referências. Provar source→target, owner único, status epistêmico e temporal, sigilo, links, correções, recursos e estado. Nunca inventar roll/evento técnico a partir de resumo. Material POC sintético é fixture rotulada, não fato jogado. Preservar mídia externa conforme política vigente. Sem editar CANÔNICO/FECHADO, APROVADO/CONGELADO, ficha, eventos, rolamentos, XP/FV, ciclo ou preparação operacional.

**Validação:** Suíte pareada e negativa conforme `validacao-e-metricas.md`; capturar precisão, cobertura, tokens efetivos, chamadas, bytes, p50/p95, navegação, estado e concorrência para Codex e ChatGPT Web. Se alguma métrica ou teste não for possível, registrar NOT_EXECUTED sem inventar PASS. Quantidade de arquivos não é métrica de sucesso. Assegurar que quatro casos tenham equivalência comprovada ou UNKNOWN/GAP honestamente rotulado; nenhum vazamento ou mudança de master.

**Persistência:** Trabalhar somente em design; novos entregáveis Git-versionados, commit atômico com parent esperado e promoção protegida; readback de ref/commit/árvore/blobs. Salvar relatório, evidências, conflitos, gate e handoff completo no GitHub, sem depender da memória do chat. Não avançar automaticamente para C.

**Saída curta, PLAYER_SAFE:** Informar estado PASS/FAIL/BLOCKED/PENDING_APPROVAL, commits e readback, pendências, recomendação exata CONTINUAR NESTE CHAT ou ABRIR CHAT LIMPO. Se só falta decisão, RESPONDA AQUI; se chat novo, fornecer prompt pronto; com FAIL, prompt da própria B, não de C. Sem spoilers. Pausar ao concluir.

**Proibições absolutas:** nenhuma alteração operacional; nenhum cutover; não criar aliases, redirects, compatibilidade permanente; não iniciar cena; não usar conteúdo GM_HIDDEN na resposta pública; não declarar versão do manifesto/ciclo válida sem validação. A política Git-native permanece proposta até aprovação específica de sucessor e E.

## Gate de entrada
FASE A: PASS_APPROVED. FASE B: NOT_STARTED. Ao iniciar B, tratar a reconciliação de HEADs/authority e os testes Web/Codex como tarefas a EXECUTAR, não como resultados já verificados.
