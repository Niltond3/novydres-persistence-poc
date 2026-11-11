---
id: arch-phase-a-following-phases
status: CANDIDATO_PENDENTE_APROVACAO
scope: NOVYDRES_GLOBAL
classification: PLAYER_SAFE
---
# Contratos executáveis e dependências B–E

## Regra de programa
Uma fase só começa após gate PASS e aprovação quando exigida; não iniciar B por mera presença deste texto. Todos os chats fazem leitura de .AGENT.md, .CONTEXTG.md, ADR-001, índice A e autoridade operacional mais recente validada, preservam master e matéria fechada, escrevem APENAS branch de design com commit + lease + readback. Ao encerrar, persistir relatório player-safe, último commit, evidências, pendências e handoff completo, sem depender de memória ou spoilers. O documento de comunicação ADR §8 aplica-se integralmente.

## B — Protótipo estritamente isolado
Entrada: aprovação explícita do gate A, validar HEADs atuais; reconciliar design que ficou atrás de master e todo novo ciclo/manifesto, sob snapshots exatos; registrar conflitos antes de tocar candidatos. Nunca copiar dados diretamente do master para um outro snapshot sem pin e aprovação.
Implementação: escolher 1 NPC, 1 trama, 1 história, 1 estado verdadeiros com registros representativos e sem expor spoilers; criar COPIAS candidatas no layout final numa branch de protótipo ou subtree isolada de design; não mover/alterar fontes operacionais. Cada exemplo deve conter owner, index, refs e provenance, conhecimento e correções. Sem eventos sintéticos tratados como fatos; fixtures artificiais rotuladas.
Testar: 30 consultas pareadas e negativos da suíte; rastrear duas ferramentas, hashes, custo de leitura, navegação e reconstrução. Certificar equivalência sem afirmar evento técnico novo se a fonte antiga não o suporta.
Gate B PASS: quatro casos têm mapping 100% de seus campos validados ou UNKNOWN preservado, sem upgrade de episteme, sem vazamento, sem mudança de master, baseline validada, readback Git e conflitos tratados por bloqueio/decisão; caso contrário B REMEDIATION.
Saída: relatório, mapas per-case, evidência e prompt de C; somente após aprovação pertinente.

## C — Ferramentas e segurança
Entrada: B PASS, master revisitado. Implementar schemas especializados, gerador catalogo determinístico, lint de IDs/relacionamentos/owner, detectores de mudanças em registros, validador de estado, sigilo, anti-legado, scripts Web/Codex e CI. Não ativar entradas candidatas no master.
Testar: runs reais com resultado consultável, fixtures adversariais, snapshot fixo/sha lease, concorrência stale HEAD, corrupção de blob, referência quebrada, conhecimento indevido, bytes externos e partial sync. Contrato de CLI e integração Web devem especificar entradas/saídas equivalentes; detectar limitação de API sem inventar capacidade.
Gate C PASS: executáveis e schemas têm testes reais aprovados para as duas rotas; checks de 100% de casos críticos; nenhuma lacuna bloqueante; readback. Sem CI comprovada = FAIL/NOT_EXECUTED.

## D — Migração integral de candidatos, ainda sem cutover
Entrada: C PASS e master atual pinado; congelar baseline de migração por commit imutável/tag auditável. Inventariar TODAS as entradas do snapshot, incluindo .github/workflows, originais, provas, mídia, fixtures, arquivos versionados, imports e dependências externas relevantes.
Transformação: atribuir cada origem a owner/destino ou classificação de fonte histórica arquivável por Git, com SHA e rationale; preservar literalmente o passado e decisões; registrar cada exceção/conflito/UNKNOWN sem inventar fatos; projetar estado/ciclo só após reconciliação. Nunca copiar retrospectivamente uma rolagem não auditada como RNG verificado. Calcular diff origem->destino, cobertura de todas as afirmações e refs. Produzir candidato de topologia final e testes.
Gate D PASS: inventário fechado sem input sem destino justificado, todos os vínculos e registros reconciliados, 0 perda/invenção, todos campos autoritativos equivalentes, apenas conflitos legitimamente não bloqueantes ou explicitamente aprovados; se violar cânone fechado, STOP. Ainda não promover master.

## E — Cutover atômico sem legado, absoluto
Entrada: D PASS + revisão independente + decisão expressa de política sucessora (G24/editorial/ADR), aprovação explícita de cutover, HEAD master revalidado; quaisquer novos commits exigem rebase sem retcon e nova prova.
Passos: construir árvore final sem nenhum caminho operacional antigo, reescrever workflows/imports/prompts/contratos ativos, garantir únicas entradas AGENTS.md/CONTEXT.md/catalogo.json, executar validador anti-legado em toda HEAD e suíte reprodutível, conferir mídia, controles e refs. Criar tag de segurança pré-cutover e plano de incidente aprovado; publicar um único commit final com parent esperado e expected_old_SHA; verificar ref/commit/árvore/blobs, rodar smoke test em snapshot promovido, checar CI. Não manter aliases/wrappers/symlinks/fallback/transitional routes depois da promoção.
Gate E PASS SOMENTE se ZERO legado e 100% equivalência/gates; qualquer caminho residual = FAIL e NÃO chamar a mudança de corte concluído. Falha antes da promoção não toca master. Falha pós-promoção: tratar como incidente de recuperação mediante instrução expressa, nunca fallback silencioso.

## Modelo de handoff de B (USAR SOMENTE APÓS aprovação explícita de A)
Missão: NOVYDRES MIGRAÇÃO FASE B — Protótipo, exclusivamente. Repositório Niltond3/novydres-persistence-poc; branch de design design/subject-oriented-migration. Primeiro consultar refs atuais; não presumir o SHA de A como o master atual. Ler ADR novydres/sistema/arquitetura/adr/001-subject-oriented.md; ler novydres/sistema/arquitetura/fase-a/index.md e todos os documentos vinculados; confirmar aprovação do jogador no registro auditável; resolver divergência design/master sem modificar master nem restaurar estado antigo. Ler .AGENT.md, .CONTEXTG.md e discovery do ciclo/manifesto vigentes. Protótipo restrito a COPIAS candidatas de 1 NPC, 1 trama, 1 história e 1 estado. Completar quadro de equivalência e fixture comparável Codex/Web. Não alterar eventos, decisões, ficha, cânone, runtime ou ciclos. Publicar somente novas evidências e candidatos na branch de design com commit protegido e readback. Encerrar em PASS/FAIL/BLOCKED/PENDING_APPROVAL; recomendar CONTINUAR NESTE CHAT ou ABRIR CHAT LIMPO; fornecer prompt de mesma fase caso falhe e de C apenas após PASS e autorização. PLAYER_SAFE; sem spoilers.
