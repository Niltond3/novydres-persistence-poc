# NOVYDRES — PROGRAMA MULTI-DRAMATURGO D00–D12 V1
Status: PLAYER_SAFE / COORDENAÇÃO DE PROJETO / NÃO ALTERA O CICLO NARRATIVO.
Fonte: ARCHITECTURE_PLAN_V1.md. Entrada do usuário: cada fase em CHAT LIMPO com mandato no GitHub; deve terminar com PROMPT da fase seguinte, sem spoilers.

## Protocolo geral de execução
1. Repositório privado Niltond3/novydres-persistence-poc. A conexão GitHub deve estar disponível com permissão de leitura para auditoria e de escrita apenas se o usuário autorizar a fase. LER master HEAD atual via API, verificar branch e ciclo mais recente NUMÉRICO. LER novydres/.AGENT.md e .CONTEXTG.md e contratos relevantes. Não confiar em HEAD de um prompt antigo.
2. Ler este programa, ARCHITECTURE_PLAN_V1.md, mandate da fase e entregáveis da fase anterior. Em descompasso, STOP_CONFLICT. C05 está CLOSED no marco de base e C06 não pode começar só porque o programa foi escrito.
3. Escrever em BRANCH DE DESIGN isolado, não em master, a menos que uma fase autorize explicitamente promoção. Novos arquivos com versão e hash; arquivos anteriores APROVADOS/CONGELADOS e CANÔNICOS/FECHADOS permanecem inalterados. COW em todas as revisões; sem atualização retroativa silenciosa.
4. Em cada fase produzir: (a) entregas versionadas; (b) AUDIT com fontes, hashes, decisões, lacunas; (c) PHASE_HANDOFF_Dxx_Vnn.json e sua vista PLAYER_SAFE; (d) prompt pronto de Dxx+1 numa nova conversa. O prompt deve apontar para o HEAD/branch VERIFIED após readback. Não incluir segredo na resposta.
5. Se um gate FAIL ou há autorização necessária, produzir PENDING_APPROVAL / REMEDIATION_PROMPT; NÃO emitir prompt que presuma que a próxima fase está desbloqueada. O jogador decide de forma explícita. A sequência D01→D12 é uma disciplina, não um bypass de aprovação.
6. Publicação: transação de commit atômico por conjunto de documentos correlatos, atualizar branch com expected_sha, readback de todas as fontes e do estado; sem alegar sucesso antes da verificação. Se não for possível escrever, apresentar um pacote legível e declarar NOT_PUBLISHED sem inventar SHA.
7. A cada resposta pública exibir APENAS paths PLAYER_SAFE, IDs, checksums, escopo, status, decisões que dependam do jogador (sem descrever segredo), e o prompt. Secretos não aparecem em título, commit, README, handoff, diff nem prompt. O repositório ser private não protege um segredo de seu próprio dono: manter segregação de apresentação, e avaliar separação de acesso efetiva antes de persistir material GM_HIDDEN.
8. Não gerar material futuro repetindo cenas fechadas nem conceder XP/FV. Nenhuma fase sozinha narra C06 ou abre 2010. Somente D12 passa um prompt para NARRADOR após validação do ciclo e autorização expressa.

## Fases e critérios de saída
D00: analisar seis obras oficiais e lacunas GitHub — ARCHITECTURE_PLAN_V1, PROGRAM_RUNBOOK, D01_MANDATE.
D01: modelar a ontologia e interfaces CRONICA/MARCO/HISTORIA/TRAMA/CENA/BEAT/FIO/NPC/CLUE/CLOCK/OUTCOME/KNOWLEDGE e casos de encerramento; produzir contratos PROPOSTOS, regras de sigilo e de decisão sobre lacuna/retcon, mapa de governança; sem escrever novas verdades de trama; gate = compatibilidade com D1/D2/H e agência + proteção de sigilo.
D02: historiografia com last_event_id, M1..M3 C05; grafos retrospectivos, autoria documentada ou UNKNOWN, inventário de fontes auditadas; gate = sem inventar fato nem atribuir intenção original.
D03: agentes/NPCs, estados por checkpoint, grafo dirigido e conhecimento; gate = 0 telepatia NPC, 0 fusões de alias sem prova.
D04: classificação de tramas: grandes, médias, pequenas, incidentais; mapear todos os 44 fios baseline após C05 sem presumir que sejam todos arcos; gate = todo fio tem owner/classificação/risco/gatilho ou GAP explícito.
D05: gap/retcon candidates com classificação e propostas, NUNCA aplicar retcon sem consentimento; gate = cada conflito material vira pergunta de aprovação. Sem consentimento, seguir apenas ao que não depende da correção, com pendência formal.
D06: bíblia macro de Bartholomeu, M1–M5 e ponte pós Abraço até 2010, objetivos e calendários flexíveis com check de suficiência; gate = transformação oferecida com liberdade e tempo plausível.
D07: contratos para tramas significativas, inclusive investigação Volnaya; verdade GM_LOCKED definida ou variante escolhida antes de novas pistas, agentes, múltiplos resultados, provados por source/proposta; gate = nenhum mistério jogável depende de inventar resposta ad hoc.
D08: engenharia de histórias, provocações, atos internos, cenas e beats condicionais, sem reescrever C01–C05; gate = introdução e encerramento local mesmo se arco transversal continuar.
D09: alinhar progressão V5, necessidade de experiência vampírica, Marcos D1 e 2010, sem XP/FV fictício; gate = plano executável e concluível sem plot armor ou sorte artificial.
D10: schemas/versionamento/validadores/role adapters; testes de ponta a ponta; gate = Narrador só executa conteúdo prévalidado, emergências vão ao Dramaturgo; contratos congelados intactos.
D11: auditoria independente adversarial: recusa PJ, falha, morte NPC, pista encontrada cedo, mistério reconfigurado, estagnação, contato sobrenatural, conflitos de precedência, retcon sem aprovação, vazamento; gate = PASS editorial e técnico ou remediação.
D12: revisão final, APROVAÇÃO DO JOGADOR, promoção versionada dos contratos/planejamentos permitidos, readback HEAD/ciclo, prompt de retomada NARRADOR condicionado a READY_FOR_NARRATOR e autorização de cena; gate = nenhum spoil público, nenhuma mudança em evento fechado sem retcon aprovado.

## Nomenclatura e handoffs
Usar pasta novydres/runtime/narrative-architecture/program/deliverables/ em branch design para D01–D12 com D01_..._V001.ext, AUDIT_D01_V001.json, HANDOFF_D01_V001.json, NEXT_PROMPT_D02_V001.md (PUBLIC_SAFE) e links SHAs exatos. D12/NARRADOR apenas depois de gate e revisão.
O próximo prompt se apresenta 'NOVYDRES CHR-001 · DRAMATURGO — FASE Dnn' e contém: repositório, branch, HEAD verificado e fallback para HEAD atual, last approved checkpoint, base doc, todos os paths e SHA, mandato, proibições, deliverables, validação, regras de segurança, saída handoff Dnn+1.
Se fase >10 sessões, usar subfases D04-a/b sem incrementar Dxx até gate PASS.

## Regras de aprovação e segurança
- D01–D04: alterações só PROPOSTAS, não promover a vigência.
- D05: retcon = apenas proposta; qualquer alteração de fato fechado exige decisão player com ID e registro.
- D06/D07: segredos podem ser projetados somente em local com política de acesso compatível; não despejar no chat público.
- D08–D11: documento editorial sem autoria do jogador nem alteração de estado mecânico.
- D12: escrever master/manifesto/ciclo somente após autorização expressa, sem violar orquestração. Se não há autorização, conclusão = READY_FOR_APPROVAL, não READY_FOR_NARRATOR.
