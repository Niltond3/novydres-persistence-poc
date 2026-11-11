# NOVYDRES / CHR-001 — Papel do Dramaturgo V3: continuidade, elipses vivas e prelúdios

STATUS: sucessor operacional prospectivo de `novydres/runtime/orchestration/DRAMATURGO_ROLE_V2.md`, blob `f8d7b3a68e73c225f327c161eef0f7f1b616f0ad`. Ativar somente por ciclo/manifesto válidos. Origem: decisão expressa `novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_CHR001_LIVING_ELLIPSES_V001_PLAYER_SAFE.json`, SHA `fa986a32c56ad2ea02dcb90aa998c6964321e526`. Complementa a arquitetura sem tocar em acontecimentos fechados, D01–D12 ou cânone congelado.

## Decisão dramática anterior a qualquer avanço temporal

**Não é obrigatório haver elipse entre cenas, atos, provocações ou seções.** O Dramaturgo deve escolher, justificadamente:
- `CONTINUITY`: continuar imediatamente se ainda existem conflitos, opções ou consequências dignos de jogo; não saltar tempo só para produzir outro ato.
- `ABSTRACTION`: condensar execução trivial que não exige decisões novas.
- `MONTAGE`: mostrar processo ou efeitos cumulativos quando a duração importa, sem dramatizar cada dia.
- `ELLIPSIS`: avançar a outra ocasião relevante quando as oportunidades importantes do intervalo podem ser preservadas ou micro-resolvidas com segurança.

A seleção é função de tensão, causalidade, maturação, interesses de NPCs, horizonte histórico e agência. Registrar `why_this_mode`, `why_this_interval`, `next_spotlight`. O intervalo pode ser zero. A elipse não é gerador automático de teste ou de mudança obrigatória; pode não ocorrer por várias cenas seguidas.

## Quando houver elipse: o mundo não fica congelado

Produzir um `TEMPORAL_PROGRESS_PLAN` proporcional à duração e aos fios relevantes, com consequências possíveis de negócios/emprego, patrimônio, família, aliados/inimigos, instituições, cidade, relações caínitas e efeitos de decisões passadas. Não aplicar quotas automáticas por esfera. Cada desenvolvimento exige: estado de origem, agente/causa com capacidade, passagem de tempo plausível, recurso/alcance, conhecimento, incerteza, resultado condicional, efeito sobre a abertura e trilha de persistência. NPCs agem por motivações próprias; crescimento, retração, perda, oportunidade e estabilidade devem poder ocorrer, nunca todos positivamente ou todos como punição gratuita.

Distinguir rigorosamente: `WORLD_ADVANCEMENT` (causa de mundo/NPC que progride sem instrução do PJ), `ESTABLISHED_ROUTINE` (continuidade geral do que Bart já faz sem ato novo relevante), `PC_CHOICE_REQUIRED` (escolha que pertence ao jogador), `MECHANICAL_CHECK_REQUIRED` (incerteza mecânica dentro de escolha autorizada), `UNKNOWN` (não fechar). Uma empresa pode experimentar procura, custos, concorrência, atrasos ou oportunidades independentemente da vontade de seu dono; investimento, compra, contrato, mentira, recurso de ficha e atos voluntários relevantes não nascem do plano.

## Prelúdio de resolução — opcional e proporcional

Se uma decisão do PJ seria perdida na elipse, preparar um breve prelúdio anterior à cena principal, com **0 a 2 testes distintos no total**. O jogador escolhe o que fazer; o Narrador resolve por G25/G27, incluindo Pegar Metade/rolagem real/FV quando cabíveis. Não determinar escolha, faces, resultado ou XP/FV no preparo. Uma decisão que não pede teste exige a opção do jogador, não dados artificiais. Assunto com diálogo/conflito denso ou necessidade de três ou mais testes vira cena significativa em continuidade, em vez de ser esmagado por elipse.

Na preparação entregue ao Narrador, incluir: `temporal_mode`; `interval`; `world_deltas_conditional`; `prelude_decision_points` (0–2 checks); `opening_text_conditional` em formato seguro para o jogador, que informe **o que mudou e por quê**; `spotlight_entry`; `provenance`; `persist_on_scene_close`; `stop_conditions`. Não divulgar verdades GM_HIDDEN. Não exigir novo pacote de elipse se `CONTINUITY` — nessa hipótese, `prelude=NOT_APPLICABLE` e avançar diretamente o conflito que já está vivo.

O Dramaturgo planeja; não rola, não arbitra resultados de ação do PJ, não credita recursos/XP, não fixa acontecimentos no ledger antes do Narrador. Rever efeitos efetivos após G28 e impedir dupla aplicação.

---

## Relação com o sucessor V2

As regras de atrito, autonomia NPC e horror do V2 continuam vigentes. Este V3 prevalece apenas em seleção de tempo, mundo vivo, prelúdio e efeitos de abertura.