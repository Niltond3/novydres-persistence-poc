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

Decisões aceitas pelo jogador:
- assuntos e subassuntos agrupam arquivos com responsabilidade coesa, escopo finito e fonte autoritativa;
- nomes e caminhos correntes são estáveis; o **Git** versiona as revisões, sem famílias de arquivos de revisão \`_V001\`, \`_V002\` etc.;
- fatos jogados, rolagens, decisões e autorizações permanecem em **registros imutáveis**, distintos das projeções atuais;
- um índice navegável permite recuperação seletiva por papel, assunto e IDs;
- o programa possui **cinco fases A–E**, inicialmente um chat Web por fase, com subfases se a segurança exigir;
- a **fase E exige ZERO rotas legadas na árvore operacional final**, sem aliases, wrappers, symlinks de compatibilidade, redirects ou fallback de leitura/escrita;
- quantidade total de arquivos não é métrica de sucesso.

**Este ADR não modifica a autoridade vigente.** Até o cutover formal, prevalecem os contratos aprovados de G19/G23/G24, DEC-CR-014, governança editorial, ciclo, manifesto e seus pins. A migração não autoriza retcon, narrativa, XP/FV, mudanças de ficha, nem edição silenciosa de material CANÔNICO/FECHADO ou APROVADO/CONGELADO. Alterações de política exigem documentos sucessores, prova de compatibilidade e aprovação própria. O desenho pode evoluir por decisão registrada; nunca se torna operacional por simples existência deste arquivo.

## 2. Problema observado

Na revisão de referência do \`master\` em \`cb9aa9e422fb0327e04e9eb0929e4ab678785405\`, a árvore continha 841 arquivos; 690 caminhos combinavam com convenções de revisão no nome. Esses números são **diagnóstico de descoberta**, não objetivo, meta, linha de corte nem medida de sucesso.

Sintomas concretos: arquivos históricos competindo pela descoberta do vigente, dupla versão Git/nome, gateways com checkpoints obsoletos, necessidade de conciliar manifestos, ciclos, SHAs e versões em muitas leituras, risco de compor informações de revisões diferentes.

Não concluir que um arquivo antigo é inválido só pelo nome; demonstrar autoridade e papel de cada fonte na fase A. Nenhuma informação validada pode ser descartada por conveniência estrutural.

## 3. Arquitetura-alvo de referência

\`\`\`text
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
\`\`\`

Os nomes acima são o desenho inicial para a fase A, não exigência de criar pastas vazias. Diretórios e arquivos seguem \`lowercase-kebab-case\`, IDs estáveis e nomes sem sufixo de revisão. **V5** como edição do jogo e **CHR-001** como identificador semântico NÃO são sufixos de revisão de documentos.

Cada assunto tem um \`index.md\` breve com: ID, tipo, escopo, proprietário do dado, arquivos disponíveis, links a outros assuntos, fontes, conhecimento permitido e caminhos de validação. Modelos de arquivos são definidos por **tipo** (ex.: personagem, organização, trama), opcionais quando irrelevantes; nunca inventar conteúdo ou criar arquivos vazios apenas para simetria.

Exemplo ilustrativo, sem fato narrativo:
\`\`\`text
personagens/npc-0042/
  index.md
  perfil.md
  objetivos.md
  afiliacoes.yaml
  relacoes.yaml
\`\`\`

**Fronteira de propriedade:** identidade global de NPC em \`personagens/\`; conhecimento, estados e ações em uma campanha em \`cronicas/<id>/\`; regra em \`sistema/\`; realidade e estrutura social global em \`cenario/\`. Relações têm ID, direção, proveniência e único proprietário; índices inversos são derivados, não cópias concorrentes. Referências cruzadas usam IDs, não duplicação textual da mesma verdade.

## 4. Representação, verdade e sigilo

- Prosa humana: Markdown legível sem renderizador proprietário; dados normalizados quando apropriado: JSON/YAML validado.
- Informação substantiva contém \`subject_id\`, estado epistêmico quando aplicável (\`CONFIRMED\`, \`NPC_CLAIM\`, \`GM_PREPARED\`, \`CONDITIONAL\`, \`UNKNOWN\`), fonte/evento/decisão rastreável e âmbito temporal. Não converter hipótese em fato.
- Separar \`AGENT_KNOWLEDGE\`, \`PLAYER_KNOWLEDGE\`, \`PC_KNOWLEDGE\`, \`NPC_KNOWLEDGE\`. Agentes autorizados podem ler material oculto; **sigilo é de DIVULGAÇÃO ao jogador**, não proibição de acesso pelo Dramaturgo/Narrador/auditores.
- Informação secreta não aparece em prompts de handoff, títulos, commits e relatórios voltados ao jogador. Acesso técnico real depende de permissões externas; rótulos não são ACL.
- Documentação corrente pode ser editada com revisão Git; fatos jogados, rolagens, decisões e aprovações usam registros append-only com IDs imutáveis e provas de commit. Projeções como \`estado/atual.json\` são regeneráveis/conciliáveis, não concorrentes dos eventos.

## 5. Leitura, escrita e concorrência

**Leitura (Codex ou ChatGPT Web):** (1) identificar projeto, papel e commit autorizado; (2) abrir \`AGENTS.md\` e \`CONTEXT.md\` curtos; (3) pesquisar \`catalogo.json\` por ID/tipo; (4) abrir \`index.md\` da fatia; (5) ler apenas os documentos e dependências pertinentes; (6) validar fatos importantes por fonte e estado epistêmico. Não carregar o repositório inteiro por padrão.

**Snapshot consistente:** uma operação usa um commit Git identificado; não misturar arquivos de HEADs distintos. \`main/master\` só é referência operacional após o cutover; candidatos em branch de migração não são autoridade de narração.

**Escrita:** validar versão esperada, autoridades e invariantes; aplicar delta apenas ao subject proprietário; executar schemas/testes e auditoria de referências; commit atômico protegido por SHA anterior; readback do commit e dos artefatos. Em conflito concorrente: bloquear e reconciliar explicitamente; nunca sobrescrever por conveniência.

**Navegação:** catálogo derivado e gerado em CI; índice não deve criar outra fonte de verdade. Os roteadores para Codex e Web resolvem o mesmo ID, caminho e commit, ainda que usem ferramentas diferentes. Nunca depender de memória entre chats.

## 6. Requisito absoluto do cutover: ZERO LEGADO

Na **árvore do commit operacional final**, para todos os artefatos sob escopo NOVYDRES e suas automações:

1. Todos os arquivos e diretórios operacionais devem seguir a nova topologia; **nenhum caminho antigo subsiste**, inclusive em pastas \`legacy\`, \`archive\` ou cópias de compatibilidade no HEAD.
2. Nenhum manifesto, índice, schema, teste, script, workflow, importação, prompt, gateway ou contrato ativo pode resolver/usar uma rota antiga; **zero alias, redirect, symlink ou fallback**.
3. Nenhuma referência operacional pode depender de fontes removidas ou de um \`_Vnnn\` antigo como versão corrente. Referências a fontes primárias externas podem existir como **proveniência**, nunca como recuperação operacional alternativa.
4. \`AGENTS.md\`, \`CONTEXT.md\` e o catálogo são as únicas portas de entrada correntes; não há bootstrap por arquivo antigo. Deve haver uma única autoridade corrente por fato/estado.
5. Testes de CI inspecionam **caminhos reais**, referências resolvíveis e strings relevantes (incluindo texto, JSON, scripts e workflows), impedindo ressurreição de dependências antigas em commits futuros.
6. O auditor precisa produzir uma **prova reproduzível de cobertura e ausência de legado no HEAD**, não apenas um relatório de sucesso; qualquer referência não migrada bloqueia PASS.
7. Históricos de commits/tags Git anteriores ao cutover continuam preservados para auditoria e recuperação em caso de incidente; **não** são rotas de fallback do runtime. Mapas históricos detalhados podem ser recuperados por commit/tag de migração, sem manter caminhos operacionais antigos em documentos correntes.

\`ZERO LEGADO\` aqui significa zero **na árvore e em todas as dependências controladas por este repositório no HEAD promovido**. Links ou caches de serviços externos fora do controle do repositório precisam ser inventariados como dependências e migrados/retirados antes do cutover quando forem operacionais; não alegar garantia universal sobre sistemas externos não inspecionados.

A fase E é **FAIL** se qualquer rota legada operacional for encontrada. Não existem exceções, período de compatibilidade pós-cutover nem mecanismo de migração parcial denominado PASS.

## 7. Programa faseado e gates

| Fase | Um chat principal | Entrega mínima e gate |
|---|---|---|
| **A — Arquitetura** | Chat limpo A | Spec de subjects/tipos, ownership, padrões, ontologia, IDs, leitura/escrita, ADRs complementares/decisões necessárias, plano de equivalência, inventário de fronteiras e mapa de migração; teste de viabilidade e aprovação de desenho antes de B. NÃO migrar dados. |
| **B — Protótipo** | Chat limpo B | Migrar **cópias candidatas** de 1 NPC, 1 trama, 1 história e 1 estado; comparar recuperações, conhecimento e autoridade; sem ativar. |
| **C — Ferramentas** | Chat limpo C | Catálogo gerado, roteamento, lints, schemas, prova de referências, testes Web/Codex e simulação de cutover. |
| **D — Migração** | Chat limpo D (subfases possíveis) | Migrar integralmente assuntos, fatos, regras, eventos, aprovações, segredos, vínculos e dependências, com equivalência comprovada; sem promover runtime incompleto. |
| **E — Cutover** | Chat limpo E | Aprovação expressa, execução atômica controlada, eliminação de todo caminho/dependência operacional antigo do HEAD, CI anti-legado, testes regressivos, leitura de confirmação e liberação da nova entrada única. |

São **cinco fases**, **não garantia de cinco interações**. Uma fase grande pode continuar em novos chats com checkpoint persistido. O próximo chat começa da fase seguinte **somente quando o gate anterior estiver PASS**. Cada fase usa branch de proposta, não altera conteúdo congelado e não avança/narra CHR-001.

Métrica de sucesso: precisão e rastreabilidade dos fatos, ausência de conflitos/retcons e spoilers, recuperação correta por Codex/Web, custo real de leitura (tokens, leituras e chamadas), custo de escrita e mudanças propagadas, testes de jornada e zero dependências legadas. Quantidade de arquivos é **estatística apenas**, nunca gate ou meta. Comparar a mesma suíte de tarefas antes/depois, sem inventar ganho percentual.

## 8. Protocolo de comunicação obrigatório para QUALQUER AGENTE OPERACIONAL

**Regra de concisão:** respostas objetivas, sem relatórios prolixos, repetições de todo o histórico ou revelações narrativas. Handoff público apenas PLAYER_SAFE. A decisão sobre seguir no chat atual ou abrir chat limpo é **obrigatória** sempre que a etapa terminar ou precisar da intervenção do jogador.

Formato de encerramento (até 6 linhas/bullets, salvo pedido explícito):
1. **Estado:** \`PASS / FAIL / BLOCKED / PENDING_APPROVAL\`, fase e resumo de uma frase.
2. **Git:** branch, commit real, readback e arquivos principais (links).
3. **Pendência:** somente decisão indispensável do jogador ou \`nenhuma\`.
4. **Recomendação:** \`CONTINUAR NESTE CHAT\` ou \`ABRIR CHAT LIMPO\`, com motivo curto.
5. **Próxima ação:** se basta resposta simples, dizer expressamente \`RESPONDA AQUI: [pergunta objetiva]\` e **não gerar prompt**; se novo chat é necessário, fornecer **um prompt completo**, pronto para colar, ancorado nos arquivos/commits verificados.
6. Se o agente não conseguiu persistir ou verificar, declarar \`NOT_PUBLISHED\` e não avançar etapa.

**Pause** depois de gate ou bloqueio que exija aprovação; não presumir que silêncio do usuário é autorização. Preferir continuar no mesmo chat para uma resposta decisória simples; recomendar chat limpo para nova fase, contexto saturado ou revisão independente. O agente pode recomendar **continuar a mesma fase** em chat limpo se necessário; nunca promover PASS artificial para cumprir a meta de cinco chats. O agente deve explicar se a interação requerida é resposta curta ou execução nova.

O documento de navegação final \`AGENTS.md\` e os contratos de cada papel devem **herdar esta política** durante A–E, de forma rastreável, sem alterarem a governança antiga antes da promoção autorizada.

## 9. Salvaguardas e rollback

- A baseline anterior e seu commit permanecem intactos. Nada do layout candidato tem autoridade antes da fase E.
- Não se retifica cânone, conhecimento de NPC, eventos, XP/FV, nem resultado de uma cena durante a migração.
- O gate de cutover checa: integridade histórica (100% dos fatos autorizados), contratos/decisões vigentes, reconstrução de estado, coerência de fontes, qualidade de escrita, sigilo, testes de ferramentas, CI anti-legado e versão única de runtime.
- Em falha pré-cutover: preservar baseline vigente e corrigir candidato. Em falha após promoção: recuperação por commit/tag de emergência exige nova decisão explícita e é procedimento de incidente, não fallback operacional cotidiano.
- Todos os conflitos de fontes têm ID/proveniência e decisão separada; UNKNOWN legítimo permanece UNKNOWN.

## 10. Perguntas técnicas reservadas à fase A

A especificação deve fundamentar, sem presumir: granularidade máxima dos documentos; formato dos vínculos canônicos; catálogo estático/gerado e regras de invalidação; desenho físico do ledger imutável; mapeamento autoritativo de lore, materiais binários e fontes externas; desempenho do Web connector para commits em lote; política de sigilo das saídas; estratégia de regressão e aprovação do cutover. Divergências com DEC-CR-014 e governança editorial precisam de proposta de decisão expressa, sem resolver conflito por interpretação.

**Gates de ADR:** iniciativa de desenho autorizada; migração de dados NÃO INICIADA; substituição do runtime NÃO AUTORIZADA; narrador e estado narrativo INALTERADOS.
