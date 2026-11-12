---
subject_id: architecture-adr001-implementation-plan
status: RASTREABILIDADE_PLANEJADA_NAO_COMPROVADA
visibility: PLAYER_SAFE
---
# Cobertura integral e prova de conclusão

Esta matriz vincula requisitos a tarefas e evidências esperadas. **Não é relatório de PASS.** Ao executar, substituir a expectativa por links ao snapshot, testes e revisão reais; requisito sem prova impede encerrar sua fase. [Backlog](tarefas.md), [decisões abertas e fontes](index.md).

## ADR-001 e especificação de A

| Obrigação/fonte | Tarefas responsáveis | Prova necessária para encerrar |
|---|---|---|
| §§1–3: vertical slices por assunto; cenário, personagens, crônicas, sistema, scripts e fontes | A01–A02, C01–C02, D01–D05 | Mapa integral por assunto/owner, destinos e consultas reais sem duplicação de autoridade. |
| §§1, 3, 6: nomes estáveis, revisões Git, três entradas únicas | A03, A05, C02–C03, D05, E02–E03 | Tree final, catálogo reproduzível, referências e histórico recuperável; nenhum `_Vnnn` como revisão corrente. Edição V5 e citações históricas não são revisões físicas. |
| §4: episteme, fontes, tempo e conhecimento situado | A02, B01–B04, C01, C04, D02–D04 | Equivalência por campo, testes de claims/UNKNOWN/futuro/conhecimento indevido e revisão contextual. |
| §§4–5: histórico preservado, estado atual, correções e transações | A03, A05, B04, C03–C04, D04, D06 | Preservação de fontes históricas e correção explícita; estado atual consistente e retomada fiel, sem ledger universal, replay obrigatório ou auditoria por dado (DEC-23/DEC-24). Uma transação verificada antes de cada resposta; falhas/idempotência/CAS e recuperação após confirmação perdida comprovadas. |
| §5: lookup seletivo por ID, catálogo/cache, commit fixo e readback | A05, B02–B04, C02–C03, C07, E03 | Contrato do fluxo realmente adotado executado, sem fuzzy fallback; hashes e leitura posterior do commit/blobs. |
| §6: ZERO LEGADO em toda HEAD e consumidores controlados | A01, C06, D01, D05–D06, E02–E03 | Scanner integral e revisão de imports/config/prompts/CI/URLs/aliases/symlinks, sem exclusão genérica de documentação ou acervo. |
| §7: A–E, métricas e gates comprovados | A06–A07, B05, C08, D07, E01–E03 | Autorização inicial do plano e resultados revisáveis por fase; transições A–D por critérios comprovados conforme DEC-22, decisões substantivas residuais e aprovação expressa de cutover em E; falhas antigas não convertidas em PASS. |
| §§7–8/11, DEC-25: continuidade condicionada no Web com GitHub | A05–A07, B03–B04, C04–C05/C07, D05/D07 | Fontes e snapshot conferidos, checkpoint recuperável, validações/resultados externos consultáveis e casos reais de divergência/retomada no mesmo chat. Aplicar DEC-26 aos limites semânticos, à recuperação e à pausa/renovação excepcional; declarar capacidades ausentes e demonstrar a condição em B/C antes de dispensar troca por fase. Não certificar ausência de alucinação. |
| §8: comunicação, persistência e handoff sem promoção fictícia | A03–A07 e tarefas de gate | Status, branch/SHA/readback, pendência e próxima unidade claros; NOT_PUBLISHED quando cabível; sem criar nova burocracia por cena. |
| §9: equivalência, limites de autoridade, revisão independente e incidente | A01–A04, C07, D02–D07, E01–E03 | Sem perda/retcon, sem upgrade de autoridade; revisão independente; checkpoint, promoção autorizada e plano de incidente. |
| §10: granularidade, vínculos, registros necessários, mídia, desempenho Web, sigilo e conflitos de políticas | A02–A06, B03–B04, C03, C06–C07, D02 | Decisões fundamentadas e capacidades demonstradas; Q-01 aplicada conforme DEC-16; Q-02 aplicada conforme DEC-18; Q-03 aplicada conforme DEC-19; revisão de guardrails conforme DEC-20, com Q-04 aceita como DEC-21 e transições futuras conforme DEC-22; Q-06 aceita como DEC-23/DEC-24. Q-07 aceita condicionalmente como DEC-25; Q-08 aceita como DEC-26: risco residual e pausa/renovação excepcional quando a recuperação falhar. |
| §§1/4/11: DEC-01–DEC-27, granularidade, precedência e simplificação | A04, B01/B04, C05/C07, D04–D05, E03 | Decisões da entrevista prevalecem no desenho; estrutura só para fatos duradouros, recuperação da prosa com fonte; contrato consolidado, exercícios narrados e revisão de escrita; nenhuma cena fictícia promovida à campanha. Eficácia em jogo não inferida do scanner. |
| §12: backlog único até implantação completa, sem limite de dez tarefas | A01–E03 | Esta matriz preenchida com evidência definitiva no HEAD promovido, sem obrigação restante escondida como pós-migração. |
| A/topologia: identidade global versus contexto local e proprietário único | A02, C01–C02, D03–D04 | Uma identidade, relações locais por escopo, sem cópias concorrentes de ficha/estado. |
| A/auditoria: todas as origens, fontes conflitantes e mídia externa | A01, D01–D02, D06 | SHA/categoria/destino/prova por origem; conflitos conhecidos tratados; originais externos preservados conforme política, sem hashes inventados. |
| A/git: proteção administrativa e rotas de leitura/escrita aplicáveis viáveis | A05, B04, C03/C07, E01–E03 | Capacidade observada, conflito stale rejeitado em sandbox, permissões/ref/parent conferidos, CI com run ID. |
| A/validação: precisão/custo/latência e suíte pareada | A06, B02–B05, C07, D06, E03 | Cobertura de riscos/casos/provas e amostragem justificada conforme DEC-21; casos críticos e falhas históricas preservados, determinísticos sem repetição redundante e rotas reais do fluxo adotado comprovadas. Aplicar DEC-19 a métricas indisponíveis, com baseline comparável nos campos observáveis. Sem dispensar provas de precisão e integridade. |

## Validadores V01–V12 de A

| Validador | Implementação | Prova integrada |
|---|---|---|
| V01 schema | C01 | C07, D06, E03 |
| V02 IDs/namespace/owner | C01 | C07, D06, E03 |
| V03 relações/referências/fontes | C01–C02 | C07, D06, E03 |
| V04 autoridade/episteme/visibilidade | C01, C04 | C07 + revisão contextual, D06–D07, E03 |
| V05 histórico/correção/idempotência | C03 | B04 como prova preliminar; C07, D06, E03 |
| V06 estado atual/recursos/retomada | C04 | C07, D04/D06, E03 |
| V07 continuidade/autoria/cursor/snapshot | C04–C05 | C07, D04–D06, E03 |
| V08 divulgação/sigilo | C06–C07 | Negativos + revisão contextual independente em C07, D07 e E03 |
| V09 catálogo/determinismo/hash | C02 | C07, D06, E03 |
| V10 Git/lease/parent/readback | C03 | B04 como prova preliminar; C07, E01–E03 |
| V11 fontes/mídia/direitos/localização | C06 | D02/D06, E03 |
| V12 ZERO LEGADO | C06 | D05–D07 na árvore final candidata, E03 na HEAD promovida |

## Cobertura da revisão narrativa

| Impactos no [desenho narrativo](../simplificacao-narrativa/desenho.md) | Tarefas |
|---|---|
| IMP-01/IMP-02: orquestração, entrada, contexto e sucessões | A01/A03–A05, C02–C05, D05 |
| IMP-03/IMP-04: conhecimento, estado e memória | A02–A03, B01–B04, C01–C04, D04 |
| IMP-05/IMP-06: NPCs e stakes sociais | A04, B01/B04, C05/C07, D04–D05 |
| IMP-07/IMP-08/IMP-09: preparo, ficha/progressão e verdade | A04, B01/B04, C04–C05, D04 |
| IMP-10/IMP-11: tempo, continuidade e alcance dos testes | A04/A06, C05/C07, D04/D06, E03 |
| IMP-12/IMP-13/IMP-14: CI, programa antigo e resíduos | A01, C06–C07, D01/D05–D07, E03 |
| IMP-15: campanha, harness e suplemento no mesmo repositório | A02/A04, C01–C02, D02–D05 |

Todo IMP precisa de fonte/destino e função preservada; não implica preservar o procedimento antigo. DEC-01–DEC-27 não são reabertas pela decomposição; o desenho anterior é adaptado às escolhas aceitas. Avaliação em jogo posterior a E observa NPCs, continuidade, ritmo e carga operacional sem forçar acontecimentos, e pode motivar correções no sistema já migrado. Esse acompanhamento não esconde trabalho técnico obrigatório de E nem autoriza iniciar a crônica.

## Execução de A01–A07 — evidência de desenho (2026-11-12)

`A_DESIGN_EXECUTION_PASS` está descrito em [fases-b-e.md](../fase-a/fases-b-e.md#a07--revisão-consolidada-da-emenda-e-decisão-de-desenho-execução-2026-11-12). Comparação confirmada de `5b55c12f4d041187ee597eb786049e7dbe5a22fc` até `c8b282a4984851bd166b89af7d6b264c04dea87e`: seis commits, nove caminhos alterados **apenas em `sistema/arquitetura`**, sem fonte narrativa ou master tocada. O relatório de A01 inclui a árvore e pins; A02 produz limites de dono e schemas candidatos; A03/A05 definem escrita/continuidade, A04 define contrato narrativo/ficcional, A06 especifica riscos e provas B/C.

Esta é prova de **desenho/persistência da documentação**, não da migração integral. Os validadores V01–V12, a integração funcional efetiva, o CI, a concorrência remota e ZERO LEGADO seguem **NOT_EXECUTED**. O gate B existente continua `B_REMEDIATION_REQUIRED`. O Core Rulebook V5 integral e a certificação final da ficha-alvo 2010 permanecem `PENDING_EVIDENCE`, não são pré-condições para o escopo isolado B que não reescreve a ficha. Mídia externa e conflitos editoriais ficam como dependências de D/E. Antes de E, nenhuma entrada candidata é ativada; aprovação histórica A está preservada.

A execução A–D foi autorizada pelo jogador em 2026-11-12; E ainda exige autorização expressa. Passar de A a B é permitido somente com checkpoint e autorização já registrados; **não** presume dispensada a troca de chat por DEC-25, cuja prova fica em B/C e cuja exceção de recuperação está em DEC-26.

## Provas por função e risco — DEC-27, execução de B (2026-11-12)

Este checkpoint é prospectivo e não altera os vereditos históricos. `B_REMEDIATION_REQUIRED` continua até encerramento independente.

| Função / risco | Prova real publicada | Estado e limite |
|---|---|---|
| Recuperação factual, fonte, conhecimento e recursos | B02 30/30 efetivos com revisão independente histórica; B03 seis respostas Web congeladas, três incompletas e três retestadas; CI `43221036507` | PASS determinístico 6/6 efetivos; revisão semântica independente da nova rodada ainda pendente; C41 não igual a C45 |
| Persistência, idempotência, concorrência e falhas | Actions `43220528637` e `43221036507`, ref descartável, HEAD/commit/blob readback, prova de `stale info` explícito | PASS_SCOPED no executor de B; REST 422 genérico distinto de rejeição por lease; perda de resposta de rede não injetada |
| Autoridade/DEC-25/DEC-26 | Dez negativos ligados a fontes/ref reais, checkpoint e prova Git; leitura da DEC-27 vigente adicionada para CI | Proteções delimitadas; nenhuma certificação de detecção semântica geral |
| NPCs, social, intenção, ritmo, prioridades, drama, mistério e sigilo | Oito outputs TEST_ONLY, N-06 resultado fictício adicional, avaliação contextual interna registrada | Revisão editorial **independente PENDING**; não substituída por scanner/CI |
| Métricas/custo | Telemetria real de chamadas e tempos REST Actions, coleta pareada nova implementada | Web tokens e bytes HTTP não observáveis (DEC-19); p95 histórico não medido e não inferido; comparar somente mesmo escopo |
| Gate e cutover | `fase-b/gate-e-readback.json#b05_dec27_current` | `B_REMEDIATION_REQUIRED`; C bloqueada e E exige autorização própria |
