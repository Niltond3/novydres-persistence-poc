# CHR-001 — Mandato para próxima execução aplicável do Dramaturgo / Atlas V1
Status: SOLICITAÇÃO AUTORAL DO JOGADOR registrada em 2026-11-08; PLANO EM FILA, NÃO EXECUTADO. Não substitui a sequência de papéis nem confere direito de alterar material congelado.
Origem: pedido para reconstruir histórias antigas, mapear cada NPC tocado por Bartholomeu, estado e relações entre NPCs, construir tramas independentes e reutilizar a história para narrativas solo paralelas.

## Ao ser invocado novamente
1. Redescobrir HEAD, CYCLE de maior sequência, manifesto, .AGENT/.CONTEXTG e verificar LIVE, blob SHAs, last_event_id, role, arquivos históricos e governança. Não assumir que CYCLE_V0030 e C04 ainda são atuais.
2. Ler ANTES de produzir um novo dossiê: CH07_PLANO_ATLAS_NARRATIVO_RETROATIVO_V1.md, NARRATIVE_ATLAS_CONTRACT_V1.md, ATLAS_SNAPSHOT_SCHEMA_V1.json e ATLAS_BACKFILL_QUEUE_V1.json. Consolidar retroativamente provas M1 até último evento real do checkpoint.
3. Executar as etapas do CH07 com escrita COW em arquivos novos, começando por fontes, cartões de eventos, censo total, estados, grafo, tramas, diagramas e seeds. Publicar relatório honesto de cobertura e fila V2; cada campo factual precisa de evidência. Se não completar, marcar PARTIAL e explicar precisamente o que falta. Não se declarar uma auditoria completa sem ser.
4. Separar planejamento original de Dramaturgo, execução Narrador, declarações jogador, reivindicações NPC e reconstrução retroativa; mapear autoria ORIGINAL somente comprovada. Não consolidar histórias independentes numa conspiração inventada.
5. Preservar integralmente M1/M2 CLOSED e cenas fechadas de M3. Nenhuma cena é aberta, nenhuma rolagem ou XP/FV acontece, nenhum passado é reescrito. Se a execução for documental e o ciclo ainda pedir NARRADOR, não fabricar PLAN_REVISED nem mudar o next_role para DRAMATURGO.
6. Quando o cursor exigir legitimamente o Dramaturgo, revalidar provocação contra eventos e atlas. Se integração permanente precisar de novos contratos/manifesto/ciclo, propor e ativar apenas segundo protocolo de versionamento/autoridade, sem mutação in-place. Separar transação administrativa do ciclo narrativo sempre que forem escopos distintos.
7. No retorno, relatar arquivos, SHA/commit, cobertura, GAP/CONFLICT, o que é jogador-safe e o que não é, e um handoff compatível com o estado real do ciclo; jamais spoilers de GM em resposta pública.

## Prioridade exigida
P0: prova e cronologia; P1: NPCs tocados, estado e relações dirigidas; P2: arcos passados e iniciativas autônomas; P3: diagramas; P4: seeds de histórias solo; P5: integração durável e testes. Se o volume exigir etapas múltiplas, publicar checkpoints auditáveis e permanecer com mandado OPEN até cobertura validada.

## Prompt para um próximo chat do Dramaturgo
NOVYDRES CHR-001 · DRAMATURGO — EXECUTAR MANDATO DO ATLAS NARRATIVO.
Repositório Niltond3/novydres-persistence-poc, master. Descubra HEAD e ciclo vigente, leia .AGENT.md e .CONTEXTG.md e os contratos atuais. Execute o mandato novydres/chronicles/CHR-001/admin/NEXT_DRAMATURGO_ATLAS_MANDATE_V1.md e o plano CH07 de reconstrução retroativa, incluindo eventos M1–M3, TODOS NPCs tocados por Bartholomeu, estados, relações dirigidas Bart↔NPC e NPC↔NPC, tramas autônomas, diagramas e pacotes de solo derivado. Use somente fontes, distinga jogado/preparado/alegado/desconhecido, publique resultados versionados COW com commit/readback e relatório de cobertura. Não altere cenas fechadas, cânone, XP/FV, não narre e respeite o next_role efetivo e o ciclo vigente.