# NOVYDRES CHR-001 · DRAMATURGO — FASE D06

## Retomada verificada

Repositório: https://github.com/Niltond3/novydres-persistence-poc
Branch: design/chr001-narrative-program-d01 (somente propostas documentais).
HEAD-base verificado na entrada D05: 6cf1434147527a2d6fd7892ee4538670ad0dad7a. Revalide o HEAD remoto antes de trabalhar e continue sobre a ponta atual sem sobrescrever commits concorrentes.
Ciclo de leitura: CYCLE_V0033.json, blob 51afa7fa15ba7dc49a863dfe6f6bb0c539014a6a; last_event_id CHR001-M301-C05-22-20261109-001. C05 está fechado, C06 não iniciado, protagonista mortal e Abraço não ocorrido. O manifesto V46 diverge dos ponteiros do ciclo; não resolver nem alterar essa divergência.

## Base D05

Gate D05: conteúdo PASS_WITH_UNKNOWN; fase ainda PENDING_READBACK. Comece D06 somente depois de o manifesto local registrar o push e o readback integral de D05. Leia os artefatos D05 V001, AUDIT_D05_V001 e HANDOFF_D05_V001 no diretório deliverables; valide seus blobs no HEAD atual. O handoff D05 mantém o ponteiro operacional, o isolamento de segredos e a promoção pendentes. Se o manifesto local não registrar readback integral, não avance.

## Mandato

Proponha a bíblia estrutural global CHR-001 do passado mortal até o horizonte de 2010: questão dramática, escopo, funções M1–M5, suficiência e encerramentos, transformações possíveis, dependências, custos, alternativas e critérios de continuidade. Respeite fatos fechados e lacunas de D02–D05. Trate 2010 como horizonte documental, não como evento garantido. Não imponha trajetória, não antecipe Abraço, não conceda recursos, não escreva cena futura nem altere estado operacional.

## Guardrails

- Preserve todas as incertezas de D02 V011, os limites epistemológicos D03 e as classificações editoriais D04.
- Não infira causalidade, conhecimento de NPC, identidade ou aceitação de oferta.
- Não promova propostas a cânone ou contrato operacional.
- Não inclua verdades secretas no repositório; não há segregação GM_HIDDEN comprovada.
- Não narre nem autorize C06.

## Saída e validação

Crie novos artefatos D06 V001, AUDIT_D06_V001.json, HANDOFF_D06_V001.json e NEXT_PROMPT_D07_V001.md em deliverables/. Rode validações estruturais e revisão adversarial; declare PASS_WITH_UNKNOWN ou bloqueio com razões verificáveis. Publique somente na branch documental após inspeção de escopo, fetch, push normal e readback integral. Mantenha master e arquivos canônicos intocados.
