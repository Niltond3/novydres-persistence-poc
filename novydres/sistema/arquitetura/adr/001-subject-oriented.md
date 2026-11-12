---
adr_id: ADR-001
titulo: Arquitetura por assuntos, caminhos estáveis e versionamento Git
status: APROVADO_PARA_DESENHO_NAO_OPERACIONAL
decidido_em: 2026-11-11
escopo: NOVYDRES_GLOBAL
branch_de_trabalho: design/subject-oriented-migration
autoridade: decisao_expressa_do_jogador_para_formalizar_o_ADR
cutover: NAO_AUTORIZADO_POR_ESTE_ADR
spoilers: PLAYER_SAFE
---

# ADR-001 — Arquitetura por assunto para NOVYDRES

## 1. Decisão e limites

Adotar **Subject-Oriented Vertical Slices**, adaptadas a conhecimento literário, regras e estado de RPG, como arquitetura-alvo de NOVYDRES.

**Precedência de desenho (DEC-17):** as decisões da entrevista de simplificação, tomadas antes de integrar o ADR ao plano de tarefas, prevalecem sobre o texto anterior deste ADR e sua especificação de A. Usá-las para resolver questões e adaptar o desenho; não pedir novamente uma escolha já aceita só porque o ADR diverge. As decisões posteriores expressas do jogador, como DEC-16, integram essa orientação. A distinção abaixo entre desenho e operação não dá ao contrato antigo poder de veto sobre o desenho novo: a implantação continua sendo trabalho futuro autorizado separadamente.

Decisões aceitas pelo jogador:
- assuntos e subassuntos agrupam arquivos com responsabilidade coesa, escopo finito e fonte autoritativa;
- nomes e caminhos correntes são estáveis; o **Git** versiona as revisões, sem famílias de arquivos de revisão `_V001`, `_V002` etc.;
- texto jogado, decisões e autorizações preservam sua fonte histórica, com correções explícitas; o estado atual por assunto é atualizado com revisão Git e proveniência, sem obrigação de reconstrução universal por eventos nem registro de cada dado (DEC-16/DEC-23/DEC-24);
- um índice navegável permite recuperação seletiva por papel, assunto e IDs;
- o programa possui **cinco fases A–E**, planejadas para ChatGPT Web com acesso ao GitHub; continuar no mesmo chat depende dos controles automáticos e de recuperação de DEC-25, sem troca obrigatória apenas pela fase;
- a **fase E exige ZERO rotas legadas na árvore operacional final**, sem aliases, wrappers, symlinks de compatibilidade, redirects ou fallback de leitura/escrita;
- quantidade total de arquivos não é métrica de sucesso.

**Este ADR não modifica a autoridade vigente.** Até o cutover formal, prevalecem os contratos aprovados de G19/G23/G24, DEC-CR-014, governança editorial, ciclo, manifesto e seus pins. A migração não autoriza retcon, narrativa, XP/FV, mudanças de ficha, nem edição silenciosa de material CANÔNICO/FECHADO ou APROVADO/CONGELADO. Alterações de política exigem documentos sucessores, prova de compatibilidade e aprovação própria. O desenho pode evoluir por decisão registrada; nunca se torna operacional por simples existência deste arquivo.

## 2. Problema observado

Na revisão de referência do `master` em `cb9aa9e422fb0327e04e9eb0929e4ab678785405`, a árvore continha 841 arquivos; 690 caminhos combinavam com convenções de revisão no nome. Esses números são **diagnóstico de descoberta**, não objetivo, meta, linha de corte nem medida de sucesso.

Sintomas concretos: arquivos históricos competindo pela descoberta do vigente, dupla versão Git/nome, gateways com checkpoints obsoletos, necessidade de conciliar manifestos, ciclos, SHAs e versões em muitas leituras, risco de compor informações de revisões diferentes.

Não concluir que um arquivo antigo é inválido só pelo nome; demonstrar autoridade e papel de cada fonte na fase A. Nenhuma informação validada pode ser descartada por conveniência estrutural.

## 3. Arquitetura-alvo de referência

```text
novydres/
  AGENTS.md                  # poucas regras invioláveis + como descobrir o vigente
  CONTEXT.md                 # índice inicial curto, sem checkpoint narrativo fixo
  catalogo.json              # índice GERADO de subjects, paths, IDs e papéis
  cenario/                   # geografia, história, política, organizações, relações globais
  personagens/               # identidades e atributos persistentes das entidades
  cronicas/                  # bíblias, tramas, histórias, cenas, eventos, estado de campanha
  sistema/                   # regras, políticas, governança, arquitetura e orquestração
    arquitetura/adr/
      001-subject-oriented.md
  scripts/                   # catálogo, validação, testes, migração e CI
  fontes/                    # fontes primárias, direitos, procedência e acervo referencial
```

Os nomes acima são o desenho inicial para a fase A, não exigência de criar pastas vazias. Diretórios e arquivos seguem `lowercase-kebab-case`, IDs estáveis e nomes sem sufixo de revisão. **V5** como edição do jogo e **CHR-001** como identificador semântico NÃO são sufixos de revisão de documentos.

Cada assunto tem um `index.md` breve com: ID, tipo, escopo, proprietário do dado, arquivos disponíveis, links a outros assuntos, fontes, conhecimento permitido e caminhos de validação. Modelos de arquivos são definidos por **tipo** (ex.: personagem, organização, trama), opcionais quando irrelevantes; nunca inventar conteúdo ou criar arquivos vazios apenas para simetria.

Exemplo ilustrativo, sem fato narrativo:
```text
personagens/npc-0042/
  index.md
  perfil.md
  objetivos.md
  afiliacoes.yaml
  relacoes.yaml
```

**Fronteira de propriedade:** identidade global de NPC em `personagens/`; conhecimento, estados e ações em uma campanha em `cronicas/<id>/`; regra em `sistema/`; realidade e estrutura social global em `cenario/`. Relações têm ID, direção, proveniência e único proprietário; índices inversos são derivados, não cópias concorrentes. Referências cruzadas usam IDs, não duplicação textual da mesma verdade.

## 4. Representação, verdade e sigilo

- Prosa humana: Markdown legível sem renderizador proprietário; dados normalizados quando apropriado: JSON/YAML validado.
- Estruturar fatos duradouros com efeito sobre estado, recursos, relações, conhecimento, pistas, decisões ou compromissos, conforme DEC-16. Esses dados contêm `subject_id`, estado epistêmico quando aplicável (`CONFIRMED`, `NPC_CLAIM`, `GM_PREPARED`, `CONDITIONAL`, `UNKNOWN`), fonte/evento/decisão rastreável e âmbito temporal. Não exigir assertion, ID ou arquivo próprio para cada frase ou detalhe incidental.
- Preservar detalhes incidentais no texto integral, recuperável por cena/trecho. Se um detalhe adquirir importância posterior, consultar a fonte e então representá-lo estruturalmente, com proveniência e conhecimento situado; não inventar que ocorreu agora, ampliar quem o conhece ou reescrever a fonte. Ausência em dados estruturados não prova ausência na ficção.
- Separar `AGENT_KNOWLEDGE`, `PLAYER_KNOWLEDGE`, `PC_KNOWLEDGE`, `NPC_KNOWLEDGE`. Agentes autorizados podem ler material oculto; **sigilo é de DIVULGAÇÃO ao jogador**, não proibição de acesso pelo Dramaturgo/Narrador/auditores.
- Informação secreta não aparece em prompts de handoff, títulos, commits e relatórios voltados ao jogador. Acesso técnico real depende de permissões externas; rótulos não são ACL.
- Documentação e estado corrente podem ser editados com revisão Git, fonte e correção explícita quando necessária. Preservar o texto jogado e a fonte histórica das decisões/aprovações, sem retcon silencioso. Conforme DEC-23, estado atual por assunto, texto integral e histórico Git substituem o ledger universal de eventos e o motor de replay; catálogo e índices continuam derivados. Registros estruturados adicionais só existem por função demonstrada, não por obrigação de duplicar toda mudança de estado. Conforme DEC-24, persistir o desenrolar narrativo e seus efeitos materiais é suficiente para as rolagens: não exigir faces individuais, registro próprio por teste ou prova técnica de aleatoriedade. Essa dispensa de auditoria não revoga as regras V5 e os testes aplicáveis já aceitos.

## 5. Leitura, escrita e concorrência

**Leitura (Codex ou ChatGPT Web):** (1) identificar projeto, papel e commit autorizado; (2) abrir `AGENTS.md` e `CONTEXT.md` curtos; (3) pesquisar `catalogo.json` por ID/tipo; (4) abrir `index.md` da fatia; (5) ler apenas os documentos e dependências pertinentes; (6) validar fatos importantes por fonte e estado epistêmico. Não carregar o repositório inteiro por padrão.

**Snapshot consistente:** uma operação usa um commit Git identificado; não misturar arquivos de HEADs distintos. `main/master` só é referência operacional após o cutover; candidatos em branch de migração não são autoridade de narração.

**Escrita:** validar versão esperada, autoridades e invariantes; aplicar delta apenas ao subject proprietário; executar schemas/testes e auditoria de referências; commit atômico protegido por SHA anterior; readback do commit e dos artefatos. Em conflito concorrente: bloquear e reconciliar explicitamente; nunca sobrescrever por conveniência.

**Cadência da mesa (DEC-18):** reunir o texto integral e as mudanças materiais de cada resposta de jogo em uma única transação atômica, com publicação e readback antes de entregar a resposta. Não criar commit por microação ou teste nem adiar a gravação até o fim da cena. A verificação acrescenta espera por resposta, aceita pelo jogador. Se falhar a persistência, pausar a continuação ficcional até recuperar/verificar a transação, informar a pendência e preservar escolhas e resultados; não rerrolar, recriar acontecimentos nem apresentar escrita pendente como confirmada. Falha de confirmação após possível publicação exige verificar o commit existente antes de tentar novamente. Esta cadência é o desenho a implementar; não ativa a mesa durante a etapa documental.

**Navegação:** catálogo derivado e gerado em CI; índice não deve criar outra fonte de verdade. Os roteadores para Codex e Web resolvem o mesmo ID, caminho e commit, ainda que usem ferramentas diferentes. Nunca depender de memória entre chats.

## 6. Requisito absoluto do cutover: ZERO LEGADO

Na **árvore do commit operacional final**, para todos os artefatos sob escopo NOVYDRES e suas automações:

1. Todos os arquivos e diretórios operacionais devem seguir a nova topologia; **nenhum caminho antigo subsiste**, inclusive em pastas `legacy`, `archive` ou cópias de compatibilidade no HEAD.
2. Nenhum manifesto, índice, schema, teste, script, workflow, importação, prompt, gateway ou contrato ativo pode resolver/usar uma rota antiga; **zero alias, redirect, symlink ou fallback**.
3. Nenhuma referência operacional pode depender de fontes removidas ou de um `_Vnnn` antigo como versão corrente. Referências a fontes primárias externas podem existir como **proveniência**, nunca como recuperação operacional alternativa.
4. `AGENTS.md`, `CONTEXT.md` e o catálogo são as únicas portas de entrada correntes; não há bootstrap por arquivo antigo. Deve haver uma única autoridade corrente por fato/estado.
5. Testes de CI inspecionam **caminhos reais**, referências resolvíveis e strings relevantes (incluindo texto, JSON, scripts e workflows), impedindo ressurreição de dependências antigas em commits futuros.
6. O auditor precisa produzir uma **prova reproduzível de cobertura e ausência de legado no HEAD**, não apenas um relatório de sucesso; qualquer referência não migrada bloqueia PASS.
7. Históricos de commits/tags Git anteriores ao cutover continuam preservados para auditoria e recuperação em caso de incidente; **não** são rotas de fallback do runtime. Mapas históricos detalhados podem ser recuperados por commit/tag de migração, sem manter caminhos operacionais antigos em documentos correntes.

`ZERO LEGADO` aqui significa zero **na árvore e em todas as dependências controladas por este repositório no HEAD promovido**. Links ou caches de serviços externos fora do controle do repositório precisam ser inventariados como dependências e migrados/retirados antes do cutover quando forem operacionais; não alegar garantia universal sobre sistemas externos não inspecionados.

A fase E é **FAIL** se qualquer rota legada operacional for encontrada. Não existem exceções, período de compatibilidade pós-cutover nem mecanismo de migração parcial denominado PASS.

## 7. Programa faseado e gates

| Fase | Continuidade no Web | Entrega mínima e gate |
|---|---|---|
| **A — Arquitetura** | Condicionada a DEC-25 | Spec de subjects/tipos, ownership, padrões, ontologia, IDs, leitura/escrita, ADRs complementares/decisões necessárias, plano de equivalência, inventário de fronteiras e mapa de migração; teste de viabilidade e consolidação do desenho autorizado antes de B, conforme DEC-22. NÃO migrar dados. |
| **B — Protótipo** | Mesmo chat elegível por DEC-25 | Migrar **cópias candidatas** de 1 NPC, 1 trama, 1 história e 1 estado; comparar recuperações, conhecimento e autoridade; sem ativar. |
| **C — Ferramentas** | Mesmo chat elegível por DEC-25 | Catálogo gerado, roteamento, lints, schemas, prova de referências, testes Web/Codex e simulação de cutover. |
| **D — Migração** | Mesmo chat elegível; subfases possíveis | Migrar integralmente assuntos, fatos, regras, eventos, aprovações, segredos, vínculos e dependências, com equivalência comprovada; sem promover runtime incompleto. |
| **E — Cutover** | Mesmo chat elegível; revisão independente preservada | Aprovação expressa, execução atômica controlada, eliminação de todo caminho/dependência operacional antigo do HEAD, CI anti-legado, testes regressivos, leitura de confirmação e liberação da nova entrada única. |

São **cinco fases**, **não uma quota de chats**. Q-07 foi aceita condicionalmente como DEC-25: trocar de fase não exige chat limpo se os controles automáticos e a recuperação no Web estiverem comprovados. Uma fase grande pode continuar em novos chats com checkpoint persistido. Isso não promete execução indefinida ou detecção completa de alucinações; o risco residual e a exceção de parada seguem DEC-26, aceita em 2026-11-12. A fase seguinte começa **somente quando o gate anterior estiver PASS**. DEC-22 define o regime futuro: após autorização de implementação do plano, A–D avançam pelos critérios comprovados, sem nova confirmação apenas por trocar de fase. Consultar o jogador para decisão substantiva não resolvida ou mudança de escopo/autoridade; E mantém aprovação expressa de cutover. A autorização atual continua sendo somente documental. Cada fase usa branch de proposta, não altera conteúdo congelado e não avança/narra CHR-001.

Métrica de sucesso: precisão e rastreabilidade dos fatos, ausência de conflitos/retcons e spoilers, recuperação correta por Codex/Web, custo real de leitura (tokens, leituras e chamadas), custo de escrita e mudanças propagadas, testes de jornada e zero dependências legadas. Quantidade de arquivos é **estatística apenas**, nunca gate ou meta. Comparar a mesma suíte de tarefas antes/depois, sem inventar ganho percentual.

## 8. Protocolo de comunicação obrigatório para QUALQUER AGENTE OPERACIONAL

**Regra de concisão:** respostas objetivas, sem relatórios prolixos, repetições de todo o histórico ou revelações narrativas. Handoff público apenas PLAYER_SAFE. A troca de chat deixa de ser ritual por fase; registrar checkpoint curto nas conclusões de tarefas/fases e explicar a troca somente quando necessária à retomada ou revisão independente. A continuidade depende da comprovação de DEC-25, com os limites aceitos em DEC-26.

Formato de encerramento (até 6 linhas/bullets, salvo pedido explícito):
1. **Estado:** `PASS / FAIL / BLOCKED / PENDING_APPROVAL`, fase e resumo de uma frase.
2. **Git:** branch, commit real, readback e arquivos principais (links).
3. **Pendência:** somente decisão indispensável do jogador ou `nenhuma`.
4. **Recomendação:** `CONTINUAR NESTE CHAT` ou `ABRIR CHAT LIMPO`, com motivo curto.
5. **Próxima ação:** se basta resposta simples, dizer expressamente `RESPONDA AQUI: [pergunta objetiva]` e **não gerar prompt**; se novo chat é necessário, fornecer **um prompt completo**, pronto para colar, ancorado nos arquivos/commits verificados.
6. Se o agente não conseguiu persistir ou verificar, declarar `NOT_PUBLISHED` e não avançar etapa.

**Pause para decisão** somente quando houver escolha substantiva ainda não resolvida, mudança de escopo/autoridade ou cutover que exija aprovação. Uma falha técnica impede avançar, mas deve ser corrigida dentro do escopo autorizado sem pedir aprovação para cada tentativa. A conclusão comprovada de A–D não exige confirmação adicional apenas pela transição (DEC-22); não presumir autorização inicial de execução nem autorização de cutover pelo silêncio. Continuar no mesmo chat quando os controles de DEC-25 permitirem; uma nova fase, isoladamente, não exige outro chat. Recomendar renovação quando a recuperação do contexto falhar ou a revisão independente exigir separação. O agente pode recomendar **continuar a mesma fase** em chat limpo se necessário; nunca promover PASS artificial para cumprir a meta de cinco chats. O agente deve explicar se a interação requerida é resposta curta ou execução nova.

O documento de navegação final `AGENTS.md` e os contratos de cada papel devem **herdar esta política** durante A–E, de forma rastreável, sem alterarem a governança antiga antes da promoção autorizada.

## 9. Salvaguardas e rollback

- A baseline anterior e seu commit permanecem intactos. Nada do layout candidato tem autoridade antes da fase E.
- Não se retifica cânone, conhecimento de NPC, eventos, XP/FV, nem resultado de uma cena durante a migração.
- O gate de cutover checa: integridade histórica (100% dos fatos autorizados), contratos/decisões vigentes, consistência do estado e retomada fiel, coerência de fontes, qualidade de escrita, sigilo, testes de ferramentas, CI anti-legado e versão única de runtime.
- Em falha pré-cutover: preservar baseline vigente e corrigir candidato. Em falha após promoção: recuperação por commit/tag de emergência exige nova decisão explícita e é procedimento de incidente, não fallback operacional cotidiano.
- Todos os conflitos de fontes têm ID/proveniência e decisão separada; UNKNOWN legítimo permanece UNKNOWN.

## 10. Perguntas técnicas reservadas à fase A

A especificação deve fundamentar, sem presumir: granularidade máxima dos documentos; formato dos vínculos canônicos; catálogo estático/gerado e regras de invalidação; organização mínima dos registros necessários, conforme DEC-23/DEC-24; mapeamento autoritativo de lore, materiais binários e fontes externas; desempenho do Web connector para commits em lote; política de sigilo das saídas; estratégia de regressão e aprovação do cutover. Divergências com DEC-CR-014 e governança editorial precisam de proposta de decisão expressa, sem resolver conflito por interpretação.

**Gates de ADR:** iniciativa de desenho autorizada; migração de dados NÃO INICIADA; substituição do runtime NÃO AUTORIZADA; narrador e estado narrativo INALTERADOS.

## 11. Revisão do harness narrativo

Registros em 2026-11-11 e 2026-11-12, PLAYER_SAFE. As diretrizes abaixo foram confirmadas pelo jogador na entrevista que motivou esta revisão. **O desenho de implementação é candidato; não altera contratos ativos, aprova gates A–E ou autoriza cutover.** O ADR continua sendo o ADR-001, na branch `design/subject-oriented-migration`; não se cria um programa arquitetural concorrente.

As escolhas substantivas já aceitas orientam a revisão do ADR e não aguardam nova aprovação de conteúdo. Se uma exigência anterior conflitar com elas, modificar o texto de desenho e registrar a correspondência; nova pergunta só se restar uma escolha não resolvida. Preservar aprovações e evidências históricas como eram, sem tratá-las como autorização operacional do desenho revisado.

O objetivo prioritário é jogar uma crônica solo com continuidade, surpresa e poucas interrupções. Harness reutilizável e suplemento standalone continuam possíveis no mesmo repositório, com autoridades distintas. O diagnóstico é que a arquitetura acumulou procedimentos sem demonstrar benefício narrativo equivalente. Há instruções já existentes que proíbem exatamente falhas relatadas: rotina sem propósito, simpatia convertida em cooperação e cortes sem continuidade. Acrescentar outra proibição não demonstra resolver essas falhas.

### Diretrizes confirmadas

| ID | Decisão |
|---|---|
| DEC-01 | A prioridade é a experiência solo. Reutilização do harness e suplemento continuam no escopo do repositório, com autoridades separadas. |
| DEC-02 | A plataforma são chats com acesso ao repositório. Dramaturgia e narração podem acontecer no mesmo chat; termina a obrigação de trocar de chat e revisar toda a provocação após cada cena. Revisão independente pode ser usada quando útil. |
| DEC-03 | A IA pode criar NPCs, motivos, segredos e consequências e mudar o planejamento prospectivo, respeitando fatos estabelecidos, limites do cenário e decisões do jogador. |
| DEC-04 | Nesta criação guiada, tornar-se vampiro Gangrel, receber o Abraço antes do final de 1970 e chegar a Novydres em 2010 com a ficha-alvo inteira são obrigatórios. O percurso permanece aberto. Isso não define os limites de uma futura crônica aberta. |
| DEC-05 | Experiências, treinamento, montagens e elipses podem sustentar consolidação mecânica por marcos. Cada ponto da ficha não exige uma cena própria. Elegibilidade, custos e recursos continuam sujeitos às regras e decisões aplicáveis. |
| DEC-06 | Preservar integralmente o texto das novas cenas como histórico, manter estado atual curto e consultar fontes antigas conforme necessário. Resumos históricos existentes não passam a ser transcrições literais. |
| DEC-07 | O narrador pode resolver passos rotineiros implicados na intenção clara do jogador até o próximo obstáculo ou escolha relevante. Não escolhe emoções, compromissos nem soluções do protagonista. |
| DEC-08 | Avanços substanciais de tempo exigem antes as prioridades do personagem. O mundo pode agir no intervalo; intenções relevantes pendentes não podem desaparecer no corte. |
| DEC-09 | O drama deve ser jogado: perdas e conquistas substanciais na vida do personagem exigem cenas. A elipse para nesses acontecimentos; a evolução mecânica gradual pode ser consolidada conforme DEC-05. |
| DEC-10 | A proteção dos destinos obrigatórios de Bartholomeu não se estende automaticamente à família. Consequências exigem causalidade; não há punição ou sofrimento obrigatório. |
| DEC-11 | A verdade central de um mistério deve estar fixada privadamente antes de pistas significativas. Descoberta e desfechos permanecem abertos; detalhes secundários podem emergir coerentemente. |
| DEC-12 | Retirar o cálculo numérico de disposição dos NPCs, preservando a função que motivou sua criação. Simpatia não equivale a concessão: objetivos, poder, limites, memória e interesses institucionais governam as respostas. A substituição precisa ser verificada em narração. |
| DEC-13 | Em testes sociais, esclarecer a concessão em disputa e os riscos quando houver ambiguidade, sem revelar intenções ocultas. O sucesso conquista o combinado e não converte automaticamente o adversário em aliado. |
| DEC-14 | Erros pequenos de continuidade podem ser corrigidos explicitamente de imediato. Mudanças que afetem escolhas, pistas, custos ou resultados anteriores exigem participação do jogador antes de correção retroativa. |
| DEC-15 | O tom desejado é horror pessoal, social e político gótico-punk, com instituições exploratórias e autopreservadoras. Afeto, solidariedade e vitórias continuam possíveis; hostilidade automática também é uma falha. |
| DEC-16 | Estruturar fatos duradouros com efeito sobre estado, recursos, relações, conhecimento, pistas, decisões ou compromissos. Detalhes incidentais permanecem na prosa integral e são consultados quando necessários; não há registro individual obrigatório por detalhe narrado. Q-01 aceita pelo jogador em 2026-11-11. |
| DEC-17 | As decisões da entrevista anteriores à integração do ADR nas tarefas de simplificação e melhoria precedem o ADR. Elas devem fundamentar respostas e mudanças no próprio ADR, sem reabrir escolhas resolvidas. Diretriz expressa do jogador em 2026-11-11; aplica-se a todo o restante do desenho e planejamento. |
| DEC-18 | Persistir texto e mudanças de cada resposta de jogo numa única gravação atômica verificada antes da entrega, sem commits por microação e sem buffer até o fim da cena. O jogador aceita a espera por resposta e a pausa da continuação em caso de falha até recuperar a persistência. Preservar escolhas/resultados e evitar duplicação na retomada. Q-02 aceita por resposta direta “aceito” em 2026-11-11. |
| DEC-19 | Aceitar a exceção de observabilidade somente para tokens reais e bytes HTTP que o ChatGPT Web não exponha. Registrar NOT_OBSERVABLE, sem estimativas apresentadas como medição real; manter respostas, fontes, operações reais e demais métricas observáveis por caso. A exceção não cobre falhas factuais, execução ausente, integridade ou CI. Q-03 aceita expressamente em 2026-11-11. |
| DEC-20 | Remover limites e guardrails excessivos. Quando as decisões anteriores já determinarem a simplificação, aplicá-la ao desenho e documentar sua razão sem pedir aceitação novamente. Quando não bastarem para decidir o que é excessivo, levar o caso concreto à entrevista Grill with Docs, com recomendação e consequências, uma pergunta por vez. Esta diretriz vale para todo o ADR e suas tarefas, sem autorizar implementação nesta etapa documental. |
| DEC-21 | Substituir quotas fixas de consultas, negativos, jornadas e rodadas por cobertura de riscos e funções. Preservar os casos críticos e as falhas anteriores, provar os dois canais e concentrar repetições em comportamento variável, concorrência e falhas. Verificações determinísticas não precisam de repetição idêntica sem mudança relevante. Justificar a cobertura e registrar evidência; menos amostras podem deixar passar falhas intermitentes. Q-04 aceita por resposta direta “aceito” em 2026-11-11. |
| DEC-22 | Na implementação futura, uma vez autorizado o plano, permitir avanço entre A–D quando os critérios estiverem comprovados, sem nova confirmação apenas pela transição. Manter resultados revisáveis por fase e consultar o jogador para decisões substantivas ainda abertas, mudanças de escopo/autoridade e aprovação expressa do cutover em E. Falhas técnicas exigem correção antes de avançar; não são dispensadas por aprovação. Q-05 aceita por resposta direta “aceito” em 2026-11-11; esta aceitação define o plano, sem autorizar execução agora. |
| DEC-23 | Manter estado atual por assunto, texto integral e histórico Git; retirar a obrigação geral de reconstruir o estado por replay de eventos estruturados. Registros adicionais só quando necessários à função de auditoria, decisões, correções e identificação de transações, com o limite de rolagens da DEC-24. Preservar atomicidade/readback por resposta, proveniência, idempotência e ausência de retcon. Inconsistências podem exigir conciliação de fontes; não se promete reconstrução automática universal. Q-06 aceita expressamente em 2026-11-11. |
| DEC-24 | Para rolagens, o desenrolar narrativo e seus efeitos materiais são suficientes. Não exigir garantia técnica do resultado de cada dado, persistência das faces, trilha RNG, seed ou arquivo por rolagem. Registrar no estado as consequências relevantes de recursos/ficha/conhecimento, conforme DEC-16, sem reproduzir o cálculo do teste. Não inventar prova aleatória nem rerrolar para preencher auditoria. Diretriz adicional expressa do jogador em 2026-11-11; os registros históricos existentes não são apagados por esta dispensa prospectiva. |
| DEC-25 | Q-07 aceita condicionalmente em 2026-11-11: executar as fases no ChatGPT Web com acesso ao GitHub, sem exigir chat limpo a cada fase, desde que existam controles automáticos para prevenir/detectar divergências e recuperar a continuidade. Preservar checkpoint e handoff recuperáveis, fontes verificáveis e revisão independente. A05/A06 e B/C devem especificar e comprovar esses controles na rota Web real antes de considerar a condição satisfeita. Aceitação não comprova sua eficácia nem autoriza execução agora. Não interpretar a condição como promessa de detectar toda alucinação ou de execução ininterrupta ilimitada; esses limites seguem DEC-26. |
| DEC-26 | Q-08 aceita por resposta direta “Aceito” em 2026-11-12: aceitar o risco residual de erros semânticos não detectados. Manter revisão independente nos pontos previstos e continuar no mesmo chat enquanto a base verificável for confiável. Diante de divergência, recuperar pelas fontes e retomar; se a recuperação não restabelecer fonte/estado confiável, pausar a unidade afetada e fornecer handoff para renovação excepcional do chat. Tarefas independentes podem continuar conforme suas dependências. Não prometer detecção universal, início autônomo de novo chat ou execução ilimitada. Esta aceitação resolve a política de exceção; não comprova os controles de DEC-25 nem autoriza implementação agora. |

Fonte: escolhas confirmadas nesta conversa; síntese, não transcrição literal nem acontecimento ficcional. O desenho deve preservar restrições anteriores mais específicas até conferir sua autoridade; o limite público de 1970 não afrouxa silenciosamente outra janela já aprovada.

### Integração proposta às fases A–E

O pacote [simplificação narrativa](../simplificacao-narrativa/index.md) contém contexto e impactos; suas tarefas integram o [backlog integral](../plano-integral/tarefas.md). É uma **emenda candidata ao desenho da fase A**, a confrontar com os resultados já existentes de B. A aprovação original de A permanece histórica; não se estende automaticamente a esta emenda. B continua `B_REMEDIATION_REQUIRED`; C não está liberada.

A equivalência dos §§6–9 preserva fatos, decisões, regras mecânicas, recursos, conhecimento e fontes. **Essa preservação é distinta da substituição deliberada de procedimentos**: trocas obrigatórias de chat por cena, cálculo de disposição, herança de adendos e gates específicos por cena. As mudanças já decididas devem ser incorporadas ao desenho com mapa de sucessão e verificação da função preservada, sem pedir nova aceitação da mesma escolha. Uma mudança de política ainda não decidida continua exigindo decisão própria. Documentar os sucessores para a implantação futura não ativa o desenho durante esta etapa documental.

Permanece o requisito ZERO LEGADO em E. Não haverá piloto operacional com duas rotas concorrentes, arquivos antigos deixados no HEAD sob rótulo de arquivo morto ou fallback cotidiano. Antes de E: exercícios isolados, sem efeitos na campanha. Depois de E e de autorização própria de cena: avaliação em jogo real. O histórico Git preserva as fontes retiradas da árvore final. Recuperação após promoção segue o procedimento de incidente do §9.

A continuidade entre fases A–E passa a seguir a aceitação condicionada de DEC-25; DEC-02 trata da mesa habitual. A especificação dos controles está em [validação e métricas](../fase-a/validacao-e-metricas.md#continuidade-no-chatgpt-web--condição-de-dec-25). O regime de aprovação entre fases segue DEC-22, preservando a revisão independente exigida em E. DEC-18 resolve a cadência: agrupar por resposta, antes da entrega, em vez de adiar até o fim da cena. Mapear G19/G24/G26/G28 e sucessores para esse desenho, sem pedir nova aceitação da escolha nem ativar candidatos antes da implantação autorizada.

### Consequências e limites

Aplicar DEC-20 como revisão transversal, não como nova camada de gates: para cada exigência questionada, registrar no próprio documento ou tarefa o problema que atende, a decisão pertinente e o tratamento (manter, simplificar, substituir ou retirar). Não criar formulário ou arquivo por guardrail. Duplicações e procedimentos contrariados pelas escolhas aceitas são retirados do desenho; perdas ou riscos ainda não discutidos vão para a entrevista. Não presumir que todas as proteções são necessárias nem que todas foram dispensadas. DEC-21 resolve Q-04: a suíte passa a ser dimensionada por riscos e funções, sem a quota fixa anterior. DEC-22 resolve Q-05 para a implementação futura, sem autorização atual de execução. DEC-23/DEC-24 resolvem Q-06 e dispensam a auditoria por dado. DEC-25 registra Q-07 como aceitação condicionada à prevenção/detecção automática e recuperação no Web; a condição depende de prova futura, não de autorrelato. DEC-26 resolve Q-08: o risco residual é aceito; se a recuperação não restabelecer uma base verificável, pausar a unidade afetada e fornecer handoff para renovação excepcional do chat. Tarefas independentes podem continuar conforme suas dependências.

Menos verificações podem deixar passar erros; mais verificações consomem contexto e podem interromper o jogo. Não há comparação empírica que estabeleça a causa das falhas ou prove ganho de criatividade. Mantêm-se descoberta inequívoca, persistência verificável, distinção entre preparo e fato, conhecimento situado e sigilo de divulgação. Autorrevisão não é auditoria independente; PASS estrutural não certifica narrativa.

Esta entrega registra escolhas e prepara trabalho revisável. Não inicia migração de dados, fase C, deleção de arquivos existentes ou cenas. [Tarefas integrais](../plano-integral/tarefas.md) definem dependências, escopo e evidência sem presumir avanço de gate.

## 12. Decomposição integral para implementação posterior

Mandato confirmado pelo jogador em 2026-11-11: o plano deve abranger **todo o ADR-001**, não somente a simplificação narrativa, e não está limitado a dez tarefas. Ao concluir sua última tarefa, devem estar implementados A–E, a migração integral, os nomes estáveis com histórico Git, a arquitetura por assunto e o encerramento ZERO LEGADO no HEAD promovido. O plano não inclui escrever conteúdo inédito de todo o suplemento; inclui migrar seu conteúdo existente e preservar suas autoridades e capacidade de evolução.

O [plano integral](../plano-integral/index.md) concentra análise crítica, decisões da entrevista, [backlog único](../plano-integral/tarefas.md) e [matriz de cobertura](../plano-integral/cobertura.md). Substitui o recorte anterior T01–T10 da parcela narrativa. As tarefas estão planejadas, não executadas. As oito questões registradas da entrevista estão resolvidas; detalhamento técnico e comprovação permanecem nas tarefas A01–A06 e nas fases posteriores. Não há declaração de execução nem aprovação adicional de gate. A última tarefa só encerra o programa com prova de todos os requisitos, sem transferir migração ou ferramentas obrigatórias a uma etapa futura.

Esta etapa é **somente documental e de análise**. A aprovação histórica de A e a remediação existente de B permanecem registradas como ocorreram. Aplicar as decisões já documentadas sobre granularidade, persistência e observabilidade sem pedir nova aceitação. Somente escolhas substantivas ainda não resolvidas ou mudanças de escopo/autoridade exigem nova decisão; não há exceções operacionais por omissão. Nenhum cutover, publicação, cena ou alteração de estado é autorizado por esta seção.
