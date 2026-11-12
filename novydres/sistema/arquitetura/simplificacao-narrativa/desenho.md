---
subject_id: architecture-narrative-simplification
status: EMENDA_CANDIDATA_NAO_OPERACIONAL
visibility: PLAYER_SAFE
---
# Desenho e matriz de corte — Harness narrativo

PLAYER_SAFE. Arquitetura proposta, não operacional. Decisões confirmadas: [ADR-001, seção 11](../adr/001-subject-oriented.md#11-revisão-do-harness-narrativo). Bases e limites: [contexto](contexto.md). Execução: [backlog integral](../plano-integral/tarefas.md).

As decisões aceitas da entrevista precedem o desenho anterior do ADR (DEC-17). Este desenho deve ser ajustado a elas sem nova aceitação do mesmo conteúdo. Conforme DEC-16, detalhes incidentais permanecem na prosa; só fatos com efeito duradouro exigem representação estruturada própria, com fonte e conhecimento situado preservados.

## Estrutura pretendida

| Responsabilidade | Conteúdo mínimo | Limite |
|---|---|---|
| Cânone e suplemento | Referências autorizadas do cenário, mecânicas e decisões editoriais. | A campanha produz fatos locais; promoção ao suplemento exige decisão editorial própria. |
| Condução | Um contrato de mesa consolidado e um ponto de entrada que o localize. | Sem herança obrigatória de dezenas de adendos para entender a regra vigente. |
| Estado atual | Um checkpoint autoritativo: posição/tempo conhecido, última intenção relevante, recursos, vínculos/pressões atuais e pendências. | Fichas ou registros especializados só por função necessária, com dono de cada campo definido; sem cópias equivalentes concorrentes ou ledger universal de eventos (DEC-23). |
| Memória histórica | Texto integral das novas cenas, fontes históricas preservadas e índice suficiente para recuperar o episódio necessário. | Resumo serve à navegação; fato decisivo duvidoso exige fonte. Não reconstruir diálogo antigo como transcrição. |
| Preparação privada | Verdades fixadas dos mistérios, objetivos e limites dos agentes, pressões e oportunidades relevantes. | Preparar situações e causas; falas, soluções e sequência de cenas permanecem abertas. |

São responsabilidades lógicas, não cinco novos sistemas ou formatos obrigatórios. Preferir adaptar arquivos existentes; não promover o POC de memória por conveniência.

### Encaixe na topologia aprovada para desenho

| Conteúdo | Dono/destino candidato no ADR-001 |
|---|---|
| Contrato geral de condução e funções | `novydres/sistema/narrativa/`; configuração e exceções da mesa em `cronicas/CHR-001/configuracao.json`, referenciadas por ID. |
| Cenário e suplemento | `novydres/cenario/`, `fontes/` e políticas editoriais em `sistema/governanca/`; sem duplicar o cânone dentro da crônica. |
| Checkpoint e recursos locais | `novydres/cronicas/CHR-001/estado/atual.json` e respectivos donos especializados; entrada aponta para esse estado, não o copia. |
| Texto jogado e provas | `cronicas/CHR-001/cenas/`, `episodios/` e `registros/`; resumo e catálogo são derivados. |
| Preparo e conhecimento situado | `cronicas/CHR-001/preparacao/`, `tramas/`, `elenco/`; identidade global em `personagens/`, sem copiar o conhecimento local. |
| Ferramentas de integridade | `novydres/scripts/`; CI em `.github/workflows/`. |

Os caminhos são slots da topologia de A, não ordem para criar todos os diretórios. `AGENTS.md`, `CONTEXT.md` e catálogo continuam as entradas únicas previstas em E. O “contrato consolidado” é uma fonte normativa localizada por essas entradas, não uma quarta porta concorrente. Nenhum destino candidato é criado ou ativado por este documento.

DEC-25 trata separadamente da execução da migração A–E no ChatGPT Web com GitHub: retirar a troca automática por fase depende de controles automáticos e recuperação comprovados em B/C, conforme [validação e métricas](../fase-a/validacao-e-metricas.md#continuidade-no-chatgpt-web--condição-de-dec-25). Checkpoint curto reaproveita o progresso existente; não há detector universal comprovado. DEC-26 aceita o risco residual e a renovação excepcional do chat se a recuperação não restabelecer uma base verificável, com pausa da unidade afetada. Isso não cria procedimento novo por cena.

Dramaturgo e Narrador são funções exercíveis no mesmo chat. A preparação privada é revista quando mudam fatos, escolhas ou condições importantes. A revisão de outro agente/chat é indicada para um conflito persistente, incoerência importante ou avaliação independente solicitada; não constitui etapa automática de todo encerramento.

## Procedimento habitual proposto

1. **Retomada:** descobrir a entrada vigente e o checkpoint confirmado. Recuperar apenas as fontes pertinentes; consulta ampla quando houver lacuna decisiva, mudança material ou renovação de contexto.
2. **Condução:** apresentar uma situação significativa e reagir às escolhas. Resolver rotina já implicada na intenção sem pedir microautorizações. Testar quando existir incerteza relevante e consequência; esclarecer stakes ambíguos antes da rolagem. Manter adjudicação e testes V5 aplicáveis; persistir desenrolar narrativo e efeitos materiais, sem faces, cálculo reproduzível ou certificado RNG (DEC-24).
3. **Tempo:** para um salto substancial, obter prioridades; considerar vínculos, objetos, compromissos e conflitos relevantes. Fazer o mundo avançar segundo causas. Jogar perdas/conquistas substanciais; não resolvê-las em prelúdios de testes ou fatos consumados. Afeto e cenas de respiro podem ter valor dramático.
4. **Persistência:** conforme DEC-18, reunir texto integral e deltas materiais de cada resposta numa única transação, publicada e verificada antes da entrega. Sem commit por microação/teste e sem adiar até o fim da cena. O jogador aceita a espera dessa verificação e a pausa da continuação em falha. Recuperar a transação antes de repetir uma publicação de resultado incerto; não rerrolar ou duplicar efeitos. A retomada por outro chat depende de estado efetivamente recuperável.
5. **Replanejamento:** ajustar prospectivamente quando o jogo exigir. Manter verdades de mistérios já estabelecidas e consequências anteriores. Novas ideias não exigem dossiê completo nem aprovação do jogador, exceto quando alteram seus limites ou escolhas protegidas.

As âncoras da criação guiada limitam os desfechos possíveis: não apresentar morte definitiva antes de 2010 como risco aberto enquanto essa chegada for obrigatória. Custos, perdas e o caminho até os destinos continuam em disputa; a família não recebe a mesma proteção. Nenhum acontecimento futuro é obrigatório apenas por constar do preparo.

A concessão social conquistada permanece válida mesmo se o NPC continuar contrário ao protagonista. NPCs podem mentir, resistir, ajudar ou negociar conforme suas condições; nenhuma dessas respostas é obrigatória só para marcar tom. A preocupação é agência sustentada, não uma quantidade de negativas.

## Matriz de intervenção

As referências indicam famílias concretas a revisar, não autorização genérica de apagar diretórios. Versões remotas são as observadas no contexto e precisam ser redescobertas em A01.

| ID | Alvo e problema | Ação proposta | Função preservada / critério | Tarefas |
|---|---|---|---|---|
| IMP-01 | `runtime/orchestration/ORCHESTRATION_CONTRACT_V1/V2` locais, sucessão até V19 remota e handoffs por papel. | Modificar o fluxo; excluir a troca obrigatória e revisão integral a cada cena. | Continuidade, preparação suficiente e persistência continuam; o jogador não transporta prompts entre papéis por obrigação. | A03–A05, C02–C05, D05 |
| IMP-02 | `.AGENT.md`, entradas versionadas, `.CONTEXTG*`, `START_HERE*` e D10 role adapters. | Simplificar para uma entrada curta que aponte a regra e o estado vigentes; eliminar checkpoints concorrentes na entrada. | Estado atual localizável sem deduzir autoridade pela maior versão de qualquer documento. | A02/A05, C02/C04, D05 |
| IMP-03 | `chronicles/CHR-001/orchestration/CYCLE_V*`, `MANIFEST_V*`, schemas e validadores acoplados. | Modificar descoberta e publicação; usar a autoridade corrente prevista em A, sem novo manifesto/schema/contrato por mudança ordinária de cena. | Escrita consistente e detecção de divergência; fatos e registros migrados, versões históricas recuperáveis no Git. | A03/A05, C03–C04, D04–D05 |
| IMP-04 | `LIVE_v*`, `character/state_v*`, `HISTORY_INDEX_v*`, `knowledge/*` e fontes de episódios. | Simplificar o estado atual, mapear dono de cada dado e atualizar somente deltas pertinentes; retirar replay universal e auditoria de rolagens (DEC-23/DEC-24). | Texto e recursos não se perdem; conhecimento de PC/NPC continua distinguido. Consulta à fonte substitui inferência por resumo. | A02–A03, B01, C04, D04 |
| IMP-05 | `npc-disposition/CONTRACT_V*`, `EVALUATOR_V*`, estados e workflows dependentes. | Modificar para caracterização e memória; excluir fórmula, sorteio de humor e escore como obrigação ativa. | Interesses resistem à cordialidade e vínculos não se apagam. Exercícios antes de E, avaliação real depois; não manter a fórmula antiga como fallback operacional. | A04, B01/B04, C05/C07, D04–D05, E03; acompanhamento após E |
| IMP-06 | `narrative-tone/*`, gates de imersão e instruções equivalentes nos papéis/preparo. | Simplificar no contrato de condução, preservando apenas responsabilidades distintas. | Horror aparece em relações, poder e consequências; sem checklist de horror em toda cena ou punição automática de vitória. | A04, C05/C07, D05 |
| IMP-07 | Contratos D01 e preparo D08 de trama/história/cena/beat, dossiês e sidecars. | Modificar exigência de preenchimento: usar organização proporcional ao conflito, cenas/beats como ferramentas opcionais. | Causas, agentes, alternativas e possibilidades de encerramento inteligíveis. Não preparar cada movimento ou bloquear uma reação por falta de formulário. | A02/A04, B01, C05, D04 |
| IMP-08 | D06/D09, ficha-alvo aprovada, progressão e políticas de XP. | Modificar o enquadramento dos destinos e consolidar progresso por marcos compatíveis com as regras. | Ficha inteira obrigatória em 2010, trajetória jogável e finita, recursos auditáveis. Não exigir uma cena por ponto nem conceder XP inventado. | A04, C04–C05, D04 |
| IMP-09 | D07 e fronteiras de conhecimento. | Preservar verdades centrais estabelecidas; simplificar preparo futuro e autorizar criação coerente no mesmo chat. | Pistas não são justificadas por trocar retrospectivamente a verdade. Segredos não aparecem em relatório ao jogador. | A02/A04, B01/B04, C05/C07, D04 |
| IMP-10 | `PACING_TEMPORAL_FRAMING_V3`, `ELLIPSIS_PRELUDE_PROTOCOL_V1` e `TEMPORAL_TRANSITION_*` remotos. | Modificar: prioridades antes de saltos substanciais; substituir inventário obrigatório de todos os fios por revisão dos afetados com recuperação adicional quando necessária. | Nenhuma intenção relevante sumida nem drama substancial comprimido. O prelúdio atual já é opcional: não tratar limite de testes ou mudanças como quota ou substituto de cena. | A04, C04–C05, D04 |
| IMP-11 | D10/D11, testes de reducer e matrizes de aprovação. | Modificar alcance declarado; separar verificação de integridade/recursos de observação do comportamento narrado. | PASS técnico não é certificado literário nem autorização para uma cena. | A06, C05/C07, D06, E03; acompanhamento após E |
| IMP-12 | `.github/workflows/novydres-*`, inclusive gates remotos específicos de M3.02. | Simplificar a CI para integridade do mecanismo vigente e regressões relevantes; retirar snapshots históricos da condição normal de jogar. | Mudanças de software continuam testadas; cada cena nova não exige um workflow e uma família de schemas próprios. | C06–C07, D05, E03 |
| IMP-13 | Programa D00–D12 e relatórios/handoffs antigos. | Excluir a obrigação de reexecutar toda a sequência; manter evidência e aproveitar conteúdo necessário. | A revisão tem correspondência por fase e não apaga autoria nem confunde preparo com evento. | A01/A04, D01/D05, E03 |
| IMP-14 | POC, exportações, cópias intermediárias e testes antigos sem consumidor ativo. | Em D, atribuir destino ou retirada justificada a cada origem; em E, retirar as rotas antigas do HEAD, inclusive POC/arquivo morto. | Fatos e fontes necessários têm destino; redundâncias têm Git, origem e recuperação comprovados. Nenhuma deleção executada agora. | A01, C06, D01/D05–D07, E03 |
| IMP-15 | Mistura entre campanha, criação guiada, harness genérico e suplemento. | Modificar navegação e fronteiras de autoridade, sem separar repositórios obrigatoriamente. | A crônica carrega suas exceções locais; o suplemento mantém suas fontes e decisões próprias. | A02/A04, C01–C02, D02–D05 |

### Integração com as fases A–E do ADR

| Fase | Parcela desta revisão | Condição de passagem |
|---|---|---|
| A — emenda de desenho | A01–A07: baseline, sucessores propostos, responsabilidades e casos afetados. | Consolidar escolhas aceitas e resolver somente decisões substantivas residuais; no plano futuramente autorizado, avançar por critérios comprovados (DEC-22), sem reescrever aprovação histórica. |
| B — protótipo/remediação | B01–B05: testar o desenho nos quatro exemplos isolados já previstos e exercícios fictícios de condução. | Resolver B_REMEDIATION_REQUIRED; manter precisão/recuperação e evidência Web/Codex. Não dispensar falhas por trocar o fluxo. |
| C — ferramentas | C01–C08: implementar e verificar o mecanismo mínimo e os sucessores compatíveis. | B PASS e autorização inicial do plano; sem nova confirmação apenas pela transição (DEC-22), com critérios de C comprovados. |
| D — migração candidata | D01–D07: aplicar a topologia e os contratos a todo o snapshot, com mapa de informação preservada e procedimentos substituídos. | C PASS; inventário integral, equivalência e conflitos resolvidos. |
| E — cutover | E01–E03: revisão independente, autorização e um único HEAD sem legado. | D PASS; política sucessora aprovada, CI, promoção protegida e readback. |
| Após E | Avaliação em jogo quando autorizada e ajustes delimitados; não é tarefa restante de implantação do ADR. | Não é gate retroativo de equivalência; eficácia narrativa permanece uma avaliação própria. |

Os quatro casos de B não autorizam ampliar o protótipo B para uma migração integral. Um contrato sucessor candidato pode mudar comportamento pretendido, mas não legitima perda factual. A validação deve distinguir equivalência da informação, mudança deliberada de procedimento e eventual mudança de regra que ainda exija decisão própria.

## Integração com D00–D12

| Fases existentes | Aproveitar | Revisar neste corte |
|---|---|---|
| D00–D01 | Diagnóstico, distinções úteis e limites de autoria. | Ontologia não impõe contrato/arquivo para toda unidade narrativa; substituir o desenho operacional. |
| D02–D03 | Fontes históricas, identidades, relações e conhecimento individual. | Recuperação sob demanda e estado atual enxuto; não repetir a historiografia inteira para retomar jogo. |
| D04–D05 | Classificação de conflitos, consequências e decisões materiais pendentes. | Separar mistério/conflito ativo de detalhe incidental; revisão de trama não exige encerrar todos os fios. |
| D06–D09 | Direção até 2010, verdades fixadas, situações aproveitáveis, ficha e progressão. | Adaptar às decisões DEC-03–DEC-11, preservando fontes e restrições aprovadas. Nenhum evento futuro vira obrigatório só porque foi preparado. |
| D10 | Regras de integridade e conhecimento, componentes úteis. | Implementar o formato mínimo escolhido; retirar validação específica por cena do fluxo ordinário. |
| D11 | Casos negativos e falhas que possam voltar a ocorrer. | Manter sua alegação de alcance limitada; adicionar avaliação de narração e recuperação em novo chat. |
| D12 | Disciplina de publicação verificável e preservação de autoridade. | Uma migração delimitada; depois persistência normal. Sem transformar a mesa em repetição de uma release de arquitetura. |

## Estratégia de migração

1. Concluir A01–A07 confrontando as três linhagens e o gate de B. Não transplantar uma branch inteira para `master`.
2. Concluir B no seu escopo isolado; só depois executar ferramentas em C e migração integral em D. Preparação nunca vira evento jogado por migração.
3. Verificar recuperação, recursos, conhecimento, falha de escrita e compatibilidade com a ficha-alvo. Exercícios ficam fora da campanha; documentos públicos não carregam segredos.
4. Apresentar em E uma árvore completa revisável: ponto de retomada, entradas, fontes migradas, procedimentos sucessores, retirada de caminhos antigos e provas. A mudança exige autorização expressa e não inicia uma cena.
5. Após E, avaliar condução real quando autorizada. Não reintroduzir caminhos antigos por compatibilidade para corrigir uma falha narrativa.

Antes de E, a baseline operacional permanece intacta. Depois da promoção, uma falha é incidente: preservar novos registros e obter a decisão de recuperação prevista no ADR §9, sem fallback silencioso. Corrigir o mecanismo não permite voltar a história, repetir resultados ou restaurar recursos antigos.

## Verificação e conclusão

| Caso | Resultado a observar |
|---|---|
| NPC cordial com interesse contrário ao pedido | Sustenta seu interesse ou concede por motivo plausível; simpatia não determina cooperação. |
| Vitória social | Entrega a concessão combinada; preserva a agenda própria do NPC, sem retirar o ganho por punição automática. |
| Intenção relevante pendente | A intenção é desenvolvida ou interrompida por uma causa jogável; não desaparece num corte editorial. |
| Trabalho e deslocamento rotineiros | Compressão até a próxima situação relevante, sem série de testes de manutenção sem consequência significativa. |
| Salto substancial | Prioridades antes do avanço; consequências proporcionais e mundo em movimento. Perdas/conquistas substanciais jogadas. |
| Família ameaçada | Possibilidade causal de consequência, sem blindagem automática e sem dano obrigatório. |
| Mistério | Verdade fixada antes da pista; recusa/falha mudam descoberta e consequências sem trocar retroativamente o núcleo. |
| Nova conversa ou recuperação após falha | Retoma o mesmo fato, recursos, intenção e limites de conhecimento; nenhuma escrita pendente vira confirmação. |
| Progresso até 2010 | Ficha e âncoras conferidas em revisões por marcos, sem prolongar rotina para justificar cada ponto. |

Os primeiros testes desses casos são exercícios identificados como tais, não eventos da campanha nem prova de sucesso futuro. A validação narrativa depende de jogo real e avaliação do jogador. Não impor número fixo de cenas, conflitos, recusas ou perdas para alcançar PASS.

O cutover arquitetural só termina com E PASS e ZERO LEGADO conforme o ADR, além das funções preservadas e da ausência de troca obrigatória de chat ou disposição numérica no fluxo. Fontes históricas retiradas são recuperáveis por Git; não permanecem em rotas antigas no HEAD. A eficácia narrativa é avaliada em acompanhamento posterior a E, com falhas e limites explícitos; não se deduz de E PASS nem exige forçar acontecimentos em jogo.
