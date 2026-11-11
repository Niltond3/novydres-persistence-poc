# NOVYDRES · CHR-001 · DRAMATURGO — SOMENTE RECONCILIAÇÃO DE PERSISTÊNCIA G28
**Status do handoff:** RESTRICTED_RECONCILIATION_ONLY; **não é** READY_FOR_DRAMATURGO operacional enquanto master não promover C44.
**Repositório:** `Niltond3/novydres-persistence-poc`, via GitHub no ChatGPT Web.
**Fonte operacional atual master:** `27652bc35755086ebbbdfd9749cb521e3e76c517`, ciclo C43, manifesto V58 (verificar HEAD real antes de agir).
**Branch candidata:** `scene/chr001-m302-c01-g28-20261111`; redescobrir HEAD atual em vez de presumir SHA, pois há adendo de feedback após o candidato inicial `d7c883758d7fcb7fb03b6f97f3d3698ed9c58420`.

## Missão autorizada

1. Ler .AGENT.md, .CONTEXTG.md e gateways operacionais V4/V3, depois C43/V58 em master e C44/V59 na candidata. Conferir HEADs, predecessor, source HEAD e SHA de todos os 6 refs operacionais, arquitetura, manifesto e 43 predecessores, incluindo as regras de temporalidade V2.
2. Auditar o G28 M3.02.C01 (5 marcos): abertura já apresentada, ação única de mover a viga fora da passagem, reação verbal da mulher, desengajamento voluntário do PJ, fechamento. Não duplicar entrada repetida do jogador. Preservar data civil desconhecida em 1970, uma noite relativa, caixa Y.B. ainda de situação atual desconhecida, Mary sem conversa comprovada, propriedade da viga UNKNOWN, oficina pequena alugada. Não inventar novos eventos.
3. Conferir explicitamente 44 fios, status mortal e Embrace não ocorrido, XP total 675/spent 270/remaining 405/credit 0 e FV máximo 6/superficial 2/disponível 4. Sem delta mecânico, sem testes e sem vitória ou XP inventados.
4. Ler e preservar o comentário do jogador `novydres/chronicles/CHR-001/feedback/PLAYER_COMMENT_M302_C01_IMMERSION_V1_PLAYER_SAFE.md` e o gate de imersão `novydres/runtime/scene-execution/NARRATIVE_IMMERSION_GATE_V1.md`; aplicar a correção para orientações futuras. Não editar material CANÔNICO/FECHADO ou APROVADO/CONGELADO.
5. Executar validadores V18 de ciclo, schema e negativos e o CI do **SHA candidato exato**. Um V17/V16 PASS histórico não equivale ao PASS do novo SHA. Os runs da versão anterior estavam `queued` com zero jobs; se continuar assim, **BLOCKED_PENDING_CI**, sem alegar sucesso.
6. Só após PASS integral verificável promover commit candidato para `master` via atualização protegida de ref `expected_sha` igual ao HEAD conferido, sem `force`; depois readback do novo master, ciclo/manifesto e fontes, confirmando estado final.
7. Após persistência concluída, encerrar missão e informar ao jogador HEAD, resultado e handoff separado para Dramaturgo de revisão. **Não executar revisão dramática prospectiva da provocação neste procedimento.**

## Restrições

NÃO narrar, rolar, atribuir ações, executar C02, preparar novo dossier de C02, abrir nova provocação, tratar candidato como master, mudar cânone, resolver conflito silenciosamente ou revelar GM_HIDDEN. Não pedir ao jogador para repetir sua escolha. C02 permanece NOT_STARTED e o Narrador não recebe permissão até um futuro ciclo revisado.

## Handoff posterior

Somente depois de C44/V59 oficialmente publicados e verificados, o Dramaturgo operacional poderá reavaliar M3.02 após C01 e produzir novo ciclo prospectivo sem cena automática.
