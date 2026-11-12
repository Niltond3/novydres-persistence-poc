---
subject_id: architecture-adr001-implementation-plan
status: A_DESIGN_EXECUTION_PASS_B_PASS_SCOPED
visibility: PLAYER_SAFE
---
# Backlog integral — ADR-001

[Mandato, diagnóstico e entrevista](index.md). [Rastreabilidade dos requisitos](cobertura.md). **Baseline de elaboração:** as tarefas foram publicadas como planejadas; execução autorizada pelo jogador em 2026-11-12 para A–D somente na branch candidata. A01 encontra-se executada; tarefas seguintes seguem pendentes até prova e registro próprio. Trechos legados que falam de autorização somente documental descrevem a etapa de elaboração, anterior à nova autorização. A decomposição cobre A–E; Q-07 foi aceita condicionalmente como DEC-25: continuidade entre fases no Web exige controles automáticos e recuperação comprovados. Q-08 foi aceita como DEC-26 em 2026-11-12: risco residual aceito, com pausa da unidade afetada e renovação excepcional do chat se a recuperação falhar. Q-01–Q-06 estão aceitas (DEC-16/DEC-18/DEC-19/DEC-21–DEC-23), com a dispensa adicional de auditoria de rolagens em DEC-24; DEC-17 dá precedência às decisões da entrevista e DEC-20 exige revisar limites excessivos em todo o programa. A execução atual usa os critérios do backlog, sem habilitar runtime/cutover.

## Como executar futuramente

Cada tarefa usa o ADR, os documentos especializados de A e as evidências da dependência indicada. Ao iniciar, registrar snapshot de entrada, arquivos/donos afetados e autorização aplicável; ao encerrar, apontar saídas e evidência real, resultados, limitações e pendências. Usar um registro curto por tarefa neste backlog com links para testes existentes; não criar outro programa de relatórios por cena. Nunca guardar segredos nos resultados PLAYER_SAFE.

Aplicar DEC-17 e DEC-20 em todas as tarefas: responder primeiro pelas decisões já aceitas e modificar o desenho incompatível; só perguntar sobre escolhas residuais. Não criar aprovação repetida da mesma decisão. Examinar limites, quotas, formatos obrigatórios, aprovações e handoffs quanto à sua função e custo: retirar excessos já resolvidos pelas decisões anteriores; levar somente dúvidas materiais à entrevista. Documentar o tratamento na tarefa ou especificação afetada, sem registro adicional por regra. As saídas abaixo descrevem responsabilidades e destinos, sem exigir um novo documento para cada tópico. Reutilizar os arquivos especializados de A/B e scripts existentes quando corretos. Escolher a menor implementação que cumpra os contratos; nenhuma aplicação, serviço de agentes ou banco novo está implícito.

Dependência de gate significa PASS comprovado. Conforme DEC-22, após autorização futura de implementação do plano, A–D avançam sem nova confirmação apenas pela transição; registrar resultados revisáveis. Consultar o jogador para escolhas substantivas ainda abertas, mudanças de escopo/autoridade e cutover em E. Falhas impedem a transição e devem ser corrigidas no escopo autorizado. Autorização atual é documental. A aprovação histórica de A não aprova a emenda, sucessores operacionais, execução de C ou promoção em master. Os registros antigos de gate não são editados para aparentar progresso novo.

Sequência: `A01 → A02/A03/A04/A05 → A06 → A07 → B01 → B02/B03/B04 → B05 → C01–C07 → C08 → D01 → D02–D05 → D06 → D07 → E01 → E02 → E03`. As dependências precisas estão em cada tarefa; atividades da mesma fase podem compartilhar uma entrega sem perder seus critérios de conclusão.

## A — Consolidar a emenda e a especificação completa

### A01 — Reconciliar baselines, autoridade e alcance

- **Entrada/dependência:** ADR §§1–10, aprovação original de A, gate de B, master/design e programa narrativo D00–D12; nenhuma tarefa anterior.
- **Escopo/saída:** inventário inicial de consumidores e fontes por família, snapshots completos, divergências de branches, owners e políticas afetadas. Separar ativo/histórico/candidato e mapear o que de B precisa ser repetido. Não fazer merge indiscriminado nem inventário factual de segredos em documento público.
- **Conclusão:** toda família do mapa de A, inclusive raiz, `.github`, mídia e dependências externas controladas, tem responsável e tratamento proposto. Autoridade da ficha e janela temporal conferidas; conflitos listados. Descoberta de refs não é reconciliação completa nem conclusão desta tarefa.


#### Execução de A01 — 2026-11-12

- **Estado:** PASS de reconciliação estrutural/snapshots e autoridade de entrada; fase A ainda aberta. **Origem:** design `5b55c12f4d041187ee597eb786049e7dbe5a22fc`; master `c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura.
- **Saída/evidência:** adendo A01 em [auditoria-e-mapa.md](../fase-a/auditoria-e-mapa.md), com árvores Git não truncadas, `compare_commits`, 77/77 pins de caminho/blob C45 conferidos, owners por família, conflitos, mídia, ficha e janela temporal.
- **Limites:** nenhuma migração, cena, alteração de cânone, promoção de A ou CI presumida. Design permanece diferente de master (189 origens master-only); B continua `B_REMEDIATION_REQUIRED` e deve refazer provas relevantes. Capacidade de CI consultada, mas 0 runs/status no commit de entrada da candidata.
- **Publicação:** commit Git atômico e readback serão apontados pelo histórico da branch; este registro não se autocita com SHA circular. **Próxima:** A02; A03–A05 por dependências, A06 e A07 após suas provas.

### A02 — Fechar topologia, granularidade e modelo de informação

- **Depende de:** A01; aplicar Q-01 já aceita (DEC-16).
- **Escopo/saída:** revisar `fase-a/topologia-e-ownership.md`, `modelo-de-dados.md` e schemas candidatos: IDs, relações, índices por assunto, fronteiras global/local e campanha/suplemento, episteme, tempo, fonte e conhecimento por ator. Aplicar DEC-16 ao conteúdo estruturado e à prosa; definir limites de documento e registros adicionais somente por função necessária, conforme DEC-23/DEC-24. Os schemas existentes são baseline a adaptar: retirar obrigações de ledger universal, replay e auditoria por dado, sem reabrir escolhas aceitas. Arquivo opcional não vira formulário obrigatório por cena/beat/figurante.
- **Conclusão:** exemplos positivos e negativos permitem decidir o destino de cada tipo de informação sem duplicar donos. Incluir recuperação de um detalhe originalmente só na prosa, com fonte e conhecimento preservados, sem tratá-lo como evento novo nem ausência factual. Arquitetura por assunto funciona para cenário, personagem, crônica e sistema; nenhuma afirmação vira CONFIRMED ou conhecimento de NPC só porque o agente a leu. Não estabelecer ACL inexistente para segredos acessíveis ao agente.


#### Execução de A02 — 2026-11-12

- **Estado:** PASS de desenho candidato; entrada `783f8616d0f2e42f61f41a0be2a02b3f6258fa03`; runtime e master intactos.
- **Saída:** `fase-a/modelo-de-dados.md`, `topologia-e-ownership.md` e schemas `subject-candidate.schema.json` / `record-candidate.schema.json`. DEC-16/23/24 aplicadas: estrutura só para fatos duradouros, detalhe incidental na prosa, um owner, episteme/tempo/conhecimento por fonte, sem registro obrigatório de rolagem/replay.
- **Prova/limite:** JSON parseável, exemplos positivos/negativos no modelo; nenhum teste executado de instância, C01, Web/Codex ou CI. Não ativar os schemas nem promover dados.
- **Próximo elegível:** A03; A04/A05 conforme dependências.

### A03 — Especificar versões, imutabilidade e persistência

- **Depende de:** A01 e desenho compatível com A02; aplicar a cadência Q-02 já aceita (DEC-18). Aplicar DEC-23/DEC-24: sem reconstrução universal por eventos nem auditoria técnica por dado.
- **Escopo/saída:** contrato de nomes estáveis/Git, preservação do texto histórico, correção explícita, transação atômica, idempotência e estado atual por assunto. Registros adicionais só por função necessária; nenhuma obrigação de arquivo por evento/rolagem ou motor universal de replay. Mapear sucessores de G19/G23/G24, DEC-CR-014 e políticas editoriais quando afetadas; explicitar quais permanecem. Aplicar uma transação por resposta de jogo, publicada e verificada antes da entrega, com pausa em falha; definir retenção de originais, texto literal novo e limites do histórico não auditado. Não reabrir essa cadência.
- **Conclusão:** caminhos atuais não usam `_Vnnn` como mecanismo de revisão; um único dono por campo. Falha de escrita não confirma estado; risco entre gravações e recuperação definidos. Correção material não reescreve registro antigo. Proposta de sucessão e autoridade necessária identificadas, sem ativação.


#### Execução de A03 — 2026-11-12

- **Estado:** PASS de especificação candidata, sem sucessão ativada. **Entrada:** `582a627604b4350ec04a3573e272f28885a9e05d`.
- **Saída:** [git-e-roteadores.md](../fase-a/git-e-roteadores.md#a03--sucessão-de-persistência-histórico-e-falhas-2026-11-12) com mapa G19/G23/G24/DEC-CR-014/G26/G28, cadência DEC-18, retenção de prosa, correção explícita, `tx_id`, idempotência, lease/parent/readback e estados técnicos em confirmação perdida.
- **Limites:** Git-native no caminho estável ainda é somente desenho e exige sucessores/autorização de política em E; não testados cenário concorrente e recuperação de confirmação perdida (B04/C03). Nenhuma cena, evento, XP/FV, master ou runtime alterado.
- **Próximas tarefas elegíveis:** A04/A05; A06 após ambas e A07 após A01–A06.

### A04 — Consolidar condução narrativa e criação guiada

- **Depende de:** A01; compatibilidade com A02/A03.
- **Escopo/saída:** contrato candidato em `sistema/narrativa`, exceções de CHR-001 e mapa IMP-01–IMP-15. Integrar DEC-01–DEC-15: funções no mesmo chat, preparação proporcional, texto integral, intenções, elipses, drama jogado, NPCs com interesses, stakes e verdades de mistérios. Conferir a ficha inteira e a progressão até 2010 contra regras/recursos, sem cena por ponto. Aplicar DEC-24: nas rolagens, preservar desenrolar narrativo e efeitos materiais, sem persistir faces, reproduzir o cálculo ou certificar RNG.
- **Conclusão:** cada procedimento mantido, simplificado ou retirado tem destino e função preservada. Sem revisão obrigatória por cena, disposição numérica, roteiro obrigatório de beats ou imunidade automática da família no desenho sucessor. Não inventar XP, eventos futuros consumados ou risco incompatível com os destinos fixos.


#### Execução de A04 — 2026-11-12

- **Estado:** PASS de especificação narrativa candidata com **PENDING_EVIDENCE** de certificação V5/2010, sem alteração operacional. **Entrada:** `39da97c260c7a25d432de990b7fdd7342a7b8156`.
- **Saída:** [simplificacao-narrativa/desenho.md](../simplificacao-narrativa/desenho.md#a04--condução-e-criação-guiada-contrato-sucessor-2026-11-12-candidato), DEC-01–15 e IMP-01–IMP-15 reconciliados; exemplos concretos de elipse, agência, oposição social, stakes, mistério, correções, horror e persistência.
- **Prova:** quatro fontes mecânicas/estado foram confrontadas no master `c9fcfc0`: alvo aprovado integral versus aquisições parciais, 675 XP equivalentes ≠ crédito gastável, mortalidade/cursor e convenção de testes provisórios. Core Rulebook V5 integral e certificação de custos/idiomas/poderes/Touchstones seguem pendentes; não promover destino futuro a fato atual.
- **Próximo:** A06 (A02–A05 agora documentalmente cumpridas), A07 após critérios/revisão, sem dispensar os bloqueios mecânicos pertinentes em B/C/D.

### A05 — Especificar contratos reais de leitura e escrita no fluxo adotado

- **Depende de:** A01; A02/A03 para fechar o contrato.
- **Escopo/saída:** revisar `fase-a/git-e-roteadores.md`: descoberta das três entradas, lookup exato por ID, leitura por snapshot, catálogo gerado e hash sem circularidade, invalidação de cache, CAS, parent esperado, readback e erros. Conferir capacidades e limites das ferramentas disponíveis sem efetuar mutações nesta etapa documental. Não presumir shell ou API no Web. Especificar DEC-25 no contrato existente: entrada/checkpoint por commit, fontes decisivas, recuperação de divergência e evidência externa de conclusão. Verificar ações reais de leitura, escrita e acompanhamento de CI, sem assumir equivalência entre o ambiente Codex e o Web.
- **Conclusão:** contratos de entrada/saída, erro e retomada no fluxo efetivamente adotado, sem exigir duplicação por canal, NOT_FOUND explícito, sem fallback fuzzy ou overwrite silencioso. Capacidade de proteção de refs, CI e sandbox classificada como comprovada ou pendência concreta; limitações não viram garantias. O contrato distingue sinal objetivo de erro de comparação semântica assistida; aplicar DEC-26 à recuperação, ao risco residual e à renovação excepcional, sem dispensar a prova de DEC-25.


#### Execução de A05 — 2026-11-12

- **Estado:** PASS de contrato de interfaces e levantamento de capacidade; **não** comprova controle DEC-25 nem equivalência Codex/Web. **Entrada:** `0298e4837bf9a304857837c5639b2c74fc5a729b`.
- **Saída:** [git-e-roteadores.md](../fase-a/git-e-roteadores.md#a05--contratos-webcodex-e-continuidade-com-prova-de-capacidade-2026-11-12) define `resolve/read_selected/commit_transaction/resume`, saídas, diagnósticos, recuperação, autoria, fallback proibido e checkpoints.
- **Evidências:** Web GitHub fetch por ref, blobs, comparação, criação de tree/commit, atualização com `expected_sha` e readback A01–A03 reais. API de consulta CI existe, mas em `0298e48` retornou **0 runs, 0 check-runs, 0 statuses**. Sem shell/Codex executado; stale/ref remota e falha de confirmação ainda não provocadas em sandbox. Tokens/bytes Web `NOT_OBSERVABLE` (DEC-19).
- **Próximo:** A04 pendente; A06 requer A04 e A02/A03/A05. DEC-25 depende B/C e DEC-26 mantém parada/renovação excepcional.

### A06 — Fechar critérios, gabaritos e fronteira B/C

- **Depende de:** A02–A05; aplicar Q-03/Q-04 já aceitas (DEC-19/DEC-21).
- **Escopo/saída:** revisar `fase-a/validacao-e-metricas.md` e contratos de B: casos com IDs, fontes, gabarito separado, bindings executáveis, isolamento, observabilidade, comparação antes/depois e revisão editorial independente. Definir quais ferramentas mínimas permitem provar B sem antecipar C. Aplicar DEC-21: dimensionar a suíte por riscos, preservando casos críticos e falhas históricas. Mapear funções/casos/provas, rotas reais necessárias ao fluxo de uso e amostragem de comportamento variável, concorrência e falhas; justificar seleção, reutilização e repetições, sem quotas de 30/12/12 ou três rodadas obrigatórias. Não usar volume nem uma única resposta correta como prova de confiabilidade. Aplicar NOT_OBSERVABLE somente aos contadores Web abrangidos por DEC-19. Incorporar os casos DEC-25 de fonte inexistente/insuficiente, decisão superada, falsa conclusão, checkpoint divergente e recuperação no mesmo chat; reutilizar casos pertinentes e declarar limites de detecção, sem novo programa ou quota de testes.
- **Conclusão:** cada critério possui prova, responsável e reprovação definidos. Preservar a classificação crítico/não crítico e a precisão exigida: críticos sem divergência; não críticos ao menos equivalentes à baseline comparável, sem false CONFIRMED. A quota e a contagem histórica de 30/30 não são critério futuro; falhas factuais conhecidas continuam exigindo correção e nova evidência, sem apagamento ou reclassificação oportunista. Ausência de telemetria/teste não equivale a PASS; qualidade de escrita não se mede por palavras-chave. Matriz de cobertura completa, incluindo controles DEC-25 com executor/resultado externo e comparação contextual; não tratar autorrelato PASS como comprovação.


#### Execução de A06 — 2026-11-12

- **Estado:** PASS de matriz de provas, sem execução de B/C. **Entrada:** `b22f03e7190e4bed39cdf6b1dce7b123a40aff01`.
- **Saída:** [validacao-e-metricas.md](../fase-a/validacao-e-metricas.md#a06--cobertura-por-risco-gabarito-isolado-e-fronteira-de-execução-2026-11-12) inclui matriz risco→executor/oráculo/reprovação, casos B-Q/N/M existentes, isolamento de gabarito, operações negativas reais, revisão semântica, DEC-25/26 e critério de CI.
- **Prova:** relidos os 30 B-Q, 12 B-N, 12 B-M, seis refs de quatro assuntos, resultados históricos e gate B; B-Q29/Q30 permanecem falhas históricas obrigatórias até correção. Os fixtures misturam pergunta/gabarito e precisam de projeção sem resposta ao executor; predicados locais e mutações simuladas não são testes remotos.
- **Limite:** nenhum teste B/C passou nesta tarefa; `B_REMEDIATION_REQUIRED` e faltas de CI/execução Codex e Web intactas. Próximo: A07, preservando aprovação antiga.

### A07 — Revisar a emenda e registrar decisão de desenho

- **Depende de:** A01–A06.
- **Escopo/saída:** diff consolidado revisável, decisões da entrevista e impacto sobre A/B; registrar a consolidação das escolhas já aceitas e obter decisão somente sobre questões residuais, sem substituir a aprovação histórica. Distinguir aprovação de desenho, de sucessores operacionais e de cutover. Aplicar DEC-22 ao regime futuro de transições A–D, sem confundir essa escolha documental com autorização de execução atual. Aplicar DEC-25 e DEC-26 já aceitas, mantendo a condição de prova Web antes de dispensar a troca por fase e a pausa/renovação excepcional quando a recuperação falhar.
- **Conclusão:** escolhas aceitas incorporadas sem pedido repetido de aceitação; nenhum trade-off bloqueante escondido em tarefa técnica; baseline e critérios aceitos para retomar B. Somente decisão substantiva realmente pendente mantém PENDING_APPROVAL para o escopo afetado. Critério técnico incompleto exige remediação; não pedir confirmação apenas para iniciar a próxima fase já autorizada no plano.


#### Execução de A07 e gate de desenho — 2026-11-12

- **Estado:** `A_DESIGN_EXECUTION_PASS` com aprovação operacional em E **não concedida**; A01–A06 conferidos por diff GitHub e checkpoints. **Entrada:** `c8b282a4984851bd166b89af7d6b264c04dea87e`; `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura e idêntico à entrada.
- **Saída:** [fases-b-e.md](../fase-a/fases-b-e.md#a07--revisão-consolidada-da-emenda-e-decisão-de-desenho-execução-2026-11-12) e [cobertura.md](cobertura.md#execução-de-a01a07--evidência-de-desenho-2026-11-12). Seis commits/9 paths `sistema/arquitetura/`, nenhum dado narrativo alterado. Aprovação histórica de A e gate B inalterados.
- **Critérios:** DEC-01–DEC-26 incorporadas sem reabrir Q-01–Q-08; sucessores editoriais e ativação somente E; B precisa corrigir falhas 51/90, B-Q29/Q30, Web, CI, stale remoto, isolamento do gabarito e inconsistência C41/C45 antes de PASS.
- **Próxima elegível:** B01, apenas protótipo isolado, depois B02/B03/B04 e gate B05; C não liberada. Controle DEC-25 em Web não comprovado — manter checkpoint/handoff e DEC-26 para renovação excepcional. **Nenhuma cena, cutover ou runtime.**

## B — Remediar e comprovar o protótipo isolado

### B01 — Reconciliar os quatro casos e seus mapas

- **Depende de:** A07 e mandato pertinente de B.
- **Escopo/saída:** revalidar fontes atuais e os candidatos existentes: um NPC (identidade global e contexto local), uma trama, uma história e um estado. Ajustar ao modelo/contrato revisados com mapa campo a campo, fontes pinadas, relações e UNKNOWN preservados. Exercícios narrativos adicionais são fixtures fictícias, não expansão da migração.
- **Conclusão:** 100% dos campos dos casos têm equivalência ou transformação justificada; nenhuma cópia vira autoridade operacional. Texto histórico não vira ledger auditado, segredo não vaza e master não muda.

### B02 — Recuperação factual com prova por caso

- **Depende de:** B01 e contratos executáveis de A06.
- **Escopo/saída:** corrigir causas das falhas registradas, inclusive Q29/Q30, e executar ou aproveitar, quando ainda válida, a prova dos casos comparáveis de recuperação definidos em A06 no fluxo adotado, com repetição justificada conforme DEC-21, baseline/candidato com contexto controlado. Guardar pergunta, resposta, fonte/trecho localizado, leitura e métrica observável por operação; não fornecer o gabarito ao executor.
- **Conclusão:** precisão, referências, recursos e conhecimento atendem os critérios acordados. Agregados antigos 51/90 ou citações sem localização não substituem evidência individual; resultados ausentes permanecem não executados.

### B03 — Validar recuperação e integração na rota de uso

- **Depende de:** B01 e A05/A06; Q-03 aceita como DEC-19.
- **Escopo/saída:** casos comparáveis de recuperação definidos em A06, com amostragem justificada conforme DEC-21, por ferramenta realmente disponível no Web, com snapshot, consultas, respostas e fontes verificáveis. Preservar isolamento do gabarito e registrar métricas expostas; aplicar a exceção estrita DEC-19 de observabilidade, sem dispensar operações nem fontes.
- **Conclusão:** revisão independente consegue conferir os resultados por caso. Autorrelato não é evidência. Não duplicar teste somente por trocar de produto; exigir prova adicional quando o uso real do conector, a integração, o contrato ou o comportamento diferir materialmente do já testado. Demonstrar a sequência DEC-25 na rota Web: recuperar tarefa/fontes, detectar divergência observável e retomar no mesmo chat a partir de checkpoint/evidência verificáveis.

### B04 — Executar negativos, mutações e concorrência no sandbox

- **Depende de:** B01 e A05/A06.
- **Escopo/saída:** materializar os casos negativos e jornadas que cobrem os riscos definidos em A06, reutilizando fixtures pertinentes com dados/IDs reais e substituindo placeholders. Executar nas rotas reais aplicáveis; repetir conforme variabilidade, concorrência e falhas, sem quotas fixas (DEC-21). Provar autoria, episteme, sigilo, recursos, idempotência, correção, stale SHA e falha parcial. Corrida remota usa ref descartável autorizada, nunca master nem campanha.
- **Conclusão:** operações realmente executadas têm entrada, tentativa, rejeição/resultado, SHA e readback; controles negativos deixam o alvo inalterado. CAS local não prova CAS remoto; atualização remota sem disputa não prova rejeição stale. Executor mínimo de B permanece limitado aos testes, sem ativar ferramentas finais. Exercitar a recuperação DEC-25 e a detecção de conclusão sem prova; documentar também erros semânticos não detectados, sem anunciá-los como impossíveis.

### B05 — Consolidar gate B com evidência atual

- **Depende de:** B02–B04.
- **Escopo/saída:** comparar baseline, equivalência, precisão, custo/latência observáveis e resultados negativos; obter a execução CI aplicável às verificações do protótipo com run ID e commit. Revisar exceções aprovadas, relações fora do escopo e diffs de master.
- **Conclusão:** todos os requisitos de B comprovados ou B continua em remediação. Evidência de CI não executada, métricas inventadas e casos faltantes impedem PASS. No plano futuramente autorizado, PASS comprovado libera C conforme DEC-22, sem nova confirmação apenas pela fase; não há promoção operacional.

#### Retomada B02–B05 — checkpoint 2026-11-12 (Web)

- Refs e cinco commits históricos conferidos; runs CI `43155672041` e `43155927667` em sucesso. B01 continua PASS histórico C41, master C45. B02 sem Codex real. B03: nova auditoria de 30 pins/localizadores e oito recursos críticos iguais, **não** avaliação semântica independente. B04: commit vencedor real e runner sintético CI; erro remoto sem classe stale demonstrada, testes reais de ID duplicado/conflitante e perda de confirmação pendentes. B05 `B_REMEDIATION_REQUIRED`, C bloqueada, DEC-25 `PARTIAL_OBSERVED_NOT_CERTIFIED`.
- Evidências consolidadas nos arquivos existentes `../fase-b/resultado-testes.json#b03_locator_followup_2026_11_12` e `../fase-b/gate-e-readback.json#b05_followup_2026_11_12`. Próxima elegível: revisão semântica independente e integração B04 com rota efetiva, sem substituir essas provas por simulação.

## C — Construir e verificar as ferramentas finais

### C01 — Implementar schemas e validações de informação

- **Depende de:** B05 PASS, entrada pertinente de C e A02.
- **Escopo/saída:** schemas especializados e validações V01–V04 para tipos efetivamente usados, IDs, relações, owner, tempo, episteme, proveniência e conhecimento. Reutilizar código adequado existente; não criar campos/arquivos sem função demonstrada. Retirar dos schemas antigos exigências de ledger universal, replay e registros/faces por rolagem (DEC-23/DEC-24).
- **Conclusão:** fixtures válidas passam; conflitos de dono, fontes inválidas, ID ambíguo e promoção indevida falham com diagnóstico acionável. Texto livre preserva seus bytes e não é convertido em estrutura inventada.

#### Execução de C01 — 2026-11-12 (implementação candidata; CI ainda não concluída neste registro)

- **Tarefa/snapshot:** C01, design `53b15fd93e2db27419c10876757ca41e91d93889`; master somente leitura `c9fcfc0c558cd17d58ec8c8272da3ed70182ff37`. B05 corrente `B_PASS_SCOPED` com as limitações históricas preservadas; C41 é snapshot dos exemplos, C45 é cursor operacional diferente.
- **Saída:** novos schemas especializados de relação/conhecimento/checkpoint junto aos dois schemas existentes de A02; implementação V01–V04 em `novydres/scripts/validar-assuntos.mjs`, suíte de mutações em `testar-validacao-assuntos.test.mjs` e workflow candidato `adr001-phase-c-candidate.yml`. Nenhum destes é entrada operacional de mesa.
- **Prova real inicial:** HEADs e cinco blobs históricos verificados pelo conector GitHub; arquivos V56/C41 ausentes da árvore candidata, mas fixados em `master@c26c0fbf15fff6c817182c06e6208e302b954f3a` com SHA conferido. Os testes de validação ainda exigem execução no Actions; fonte por commit/caminho/blob é distinta de fallback operacional.
- **DEC-20/21/23/24/27:** somente tipos efetivamente presentes nos casos C41; sem ledger universal, replay, arquivos por rolagem, quota de repetição ou executor Codex duplicado. Casos negativos dirigidos a owner, colisão, fonte, relação, episteme, conhecimento, recursos e promoção.
- **Limites/risco:** a relação externa ainda não migrada é relatada como DEFERRED, não como resolvida; comportamento narrativo e fontes semânticas não são certificados por schema; CI pendente, logo C01 não pode ser declarada PASS definitivo nesta anotação.
- **Próxima elegível:** concluir execução/readback do CI e registrar resultado em C01; somente depois C02 e, quando permitido pelas dependências, C03–C08. Sem runtime, cenas, master ou E02.


#### C01 — validação remota concluída e prova B04 complementar (2026-11-12)

- **Estado corrente de C01:** `C01_PASS_SCOPED`, sem ativação ou certificação da árvore completa. Os resultados `CI_PENDING` e `FAIL` acima são checkpoints anteriores, agora sucedidos pela prova direcionada sem apagamento. Snapshot de implementação `0333527625a49a1dd07c24793d096327fa66c65f`, correção `4d5c4e47eb7127ab19c66b4660de1727dcb9456c`, com master fixado somente para leitura em `c9fcfc0c558cd17d58ec8c8272da3ed70182ff37`.
- **CI real C01:** Actions run `43231562541` falhou na primeira versão por colisão aparente entre `assunto.json` e `atual.json` do mesmo sujeito e referência C41 ausente na HEAD candidata. Corrigido por validação da identidade compartilhada e fonte histórica pinada por commit/caminho/blob. Run `43231879039`, job `131229022999`, commit `4d5c4e47eb7127ab19c66b4660de1727dcb9456c`: `completed/success`, **13/13 testes**, 11 arquivos verificados, 5 subjects, 0 erros. Resultado externo lido no GitHub, não simulação local declarada como CI.
- **Correção de prova B04 sem alterar gate histórico:** runs remotos `43228359079` e `43231561927` falharam após corrida de escritores ao comparar HEAD remoto imediatamente, com refs descartáveis limpas. Após inspecionar logs, commit `7fea555e8df0d42c3af7a7b502a39af8d835aba1` exige duas leituras remotas estáveis concordantes, em janela finita, sem dispensar a asserção e sem novos testes nos dois canais; restringiu também gatilhos documentais redundantes. Actions run `43232582512`, job `131231505127`, `completed/success`: publicação remota em ref descartável, um escritor vencedor, duplicata NO_OP, conflito impedido, recuperação de confirmação suprimida, rejeição `stale info` via transporte Git e limpeza confirmada. O diagnóstico HTTP 422 permanece genérico. Scorer B03 determinístico passou; revisão contextual anterior não é refeita nem atribuída a este CI.
- **Limitações DEC-20/21/25/26/27:** `pc-bartholomeu-krauser` continua vínculo externo `DEFERRED`, a fatia C41 não foi atualizada para cursor operacional C45, a existência de blob não certifica verdade semântica, cenas de teste não certificam runtime, não houve falha real de rede induzida nem medição de tokens Web/bytes HTTP wire. Os dois FAIL e o PASS dirigido da corrida permanecem rastreáveis; a estabilização de leitura não demonstra ausência universal de intermitência. Não há reivindicação de ZERO LEGADO ou sucessão de política operacional.
- **Readback/continuação:** commit e ref da branch confirmados após as publicações de C01 e B04; fechar C01 no seu escopo com provas reais acima. **Próxima elegível: C02**, condicionada aos seus critérios e A05. C03/C08 e D dependem das suas provas; E01 só após D07, apresentação de entrega para aprovação expressa; E02 permanece proibida.

### C02 — Implementar catálogo e recuperação por assunto

- **Depende de:** C01 e A05.
- **Escopo/saída:** geração determinística, lookup por ID e leitura seletiva no fluxo efetivamente usado, índices/relacionamentos derivados, hashes sem autorreferência e cache por snapshot. As três entradas finais localizam o contrato; README não vira quarto bootstrap.
- **Conclusão:** mesmos inputs geram mesmos bytes; alterações invalidam o que precisam invalidar, todos os destinos resolvem e NOT_FOUND não consulta rota antiga. V03/V09 comprovados na rota aplicável.

#### C02 — Implementação candidata e prova em andamento (2026-11-12)

- **Tarefa/entrada:** C02, snapshot `design@a0430cf15b0c0715e9572954dbf320c97374bfa8`; `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura. C01 `PASS_SCOPED` confirmado por CI `43231879039`; A05 especifica SHA de commit, ID exato, índice derivado e ausência de fallback.
- **Implementação:** `novydres/scripts/catalogo-assuntos.mjs` gera/verifica `novydres/catalogo.json` a partir dos `assunto.json` candidatos reais e seus arquivos/índices, produz dependências inversas e `content_index_sha` Git dos pares caminho/blob ordenados (sem hash do commit/catálogo no próprio catálogo); lookup exato, restrição de divulgação, cache de metadados por snapshot e leitura seletiva de blobs com `git show <commit>:<path>`/verificação de SHA. `AGENTS.md` e `CONTEXT.md` novos são entradas explicitamente candidatas, **não** ativação da mesa.
- **Prova preparada:** 5 assuntos / 16 arquivos da árvore Git candidata não truncada; índices e `assunto.json` existentes; test suite `testar-catalogo-assuntos.test.mjs` cobre V03/V09, determinismo de bytes, inversos, mudança de conteúdo, ID/owner, restrição por papel, snapshot antigo, catálogo forjado, refs ausentes e rejeição de caminhos não declarados. Integração à CI de C01, sem workflow por teste ou executor Codex obrigatório.
- **Limites/DEC-20/21/25/27:** escopo somente cinco subjects C41, não catálogo global completo; o elo externo `pc-bartholomeu-krauser` permanece `DEFERRED`, não resolvido; origens históricas não viram fallback; tags `SYSTEM_AUDIT` restringem divulgação, mas não são ACL Git. Não se presume equivalência a C45 nem ausência universal de erros semânticos.
- **Estado/proxima ação:** implementação preparada, **CI C02 ainda não executada** neste checkpoint. Publicar com expected SHA, reler commit/blobs, inspecionar CI real e registrar resultado na própria C02 antes de permitir C03/C06. Não fazer merge, cutover ou cena.


#### C02 — Fechamento verificável (2026-11-12)

- **Estado:** `C02_PASS_SCOPED`, não operacional. A primeira publicação `d1651727ca1600d859c92216d123ddd3fd87e1b0` falhou no Actions `43234885147` por rejeitar um `owner_scope` igual ao próprio diretório; causa corrigida em `1e9eaf25a8f78e0dd94f0d8d59b746cf134a8028`, sem alterar os dados.
- **Evidência externa de execução:** Actions `43235094545`, job `131240227058`, commit corrigido: `completed/success`. Verificador de catálogo `ok=true`, 5 assuntos, 16 arquivos, `content_index_sha=fa13e82dcdd09afec0bd8bad5004b7caa744a0df`, bytes gerados iguais aos publicados; **15/15** testes V03/V09 e **13/13** testes C01 regressivos. Provas incluem leitura real de blobs por `git show` em commit pinado, correlação do catálogo com dados, cache por snapshot, invalidação por mudança de bytes, rejeição de ID aproximado, collisions, refs/targets indevidos, papéis sem permissão e catálogo de outro SHA.
- **Readback Web/GitHub:** ref de design e commit exatos confirmados, com `catalogo.json@2d77610ebf825eab42370b0b9cfe8787ab9e822b`, `perfil.json@17a353ccbda595b99fbf909b7ecd9d91b0e723d9` e `conhecimento.json@64af21e9ca4c0ea625af3f7f7b3a93b7a241073e`; os dois últimos SHA coincidem com a lista no catálogo. `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` sem alteração.
- **DEC-20/21/27 e limites:** reutilizada CI de C01, sem prova duplicada Codex. Catálogo tem somente os cinco subjects da fatia histórica C41, não representa toda a árvore ou o cursor master C45; vínculo externo `pc-bartholomeu-krauser` continua `DEFERRED`. Histórico, cenas, fontes ocultas e ausência universal de erro semântico não foram certificados; nenhuma transação de mesa, runtime ou cutover.
- **Próxima elegível:** `C03` (transações Git atômicas) e `C06` (auditoria de fontes/legado) após C02, respeitando suas dependências; `C04/C05/C07/C08` aguardam os antecessores.

### C03 — Implementar gravação atômica e histórico preservado

- **Depende de:** C01/C02 e A03/A05.
- **Escopo/saída:** transação dos donos afetados, texto histórico preservado, correção explícita, identidade mínima de transação, idempotência, expected SHA/parent, proteção de ref e readback. Estado corrente é editável com revisão; não exigir registro próprio por evento/rolagem ou certificado RNG. Exercitar stale update, repetição de ID, concorrência, blob corrompido e interrupções em sandbox. A transação da resposta reúne texto/deltas; nenhum texto ficcional é entregue antes do readback.
- **Conclusão:** V05/V10 passam com rejeições comprovadas, sem sobrescrita/perda silenciosa; estado COMMITTED distinto de sincronização parcial. Provar também publicação concluída com confirmação perdida: recuperação encontra a mesma transação, sem duplicar texto, deltas ou consequências e sem rerrolar. Restrições administrativas efetivamente disponíveis conferidas; proteção não comprovada não é anunciada.

#### C03 — Implementação isolada e prova pendente (2026-11-12)

- **Entrada:** `design@7fcc60a9b6dd1848ecd3afc5258ca0cec2a636b7`; `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura. C01/C02 PASS_SCOPED verificados; A03/A05 governam transações e recuperação.
- **Saída:** candidato `novydres/scripts/transacao-git.mjs`, testes `testar-transacao-git.test.mjs` e workflow isolado C03. A implementação exige ref `test/adr001-c03-*`, alteração simultânea somente de texto/JSON em `tmp/adr001-c03/*`, `expected_head`, `tx_id`, fingerprint de conteúdo, commit filho do esperado, `force=false` e readback de commit/tree/blobs. Identidade de transação fica no trailer Git, sem ledger universal nem auditoria de faces.
- **Prova preparada:** GitHub Actions em ref descartável, com publicação real, duas alterações atômicas, duplicação NO_OP, mesmo ID divergente STOP_CONFLICT, stale, concorrência, commit não promovido, confirmação deliberadamente suprimida após publicação e verificação negativa de blob. A mutação de blob é teste de diagnóstico, não corrupção real; a perda é de confirmação simulada no cliente, não pane de rede injetada.
- **Limite:** `NOT_TESTED` neste checkpoint; nada da crônica, `master`, canon ou runtime é editável por esse executor. Integração final com owners/autoridades, controle de sigilo e política operacional de E depende de C04/C05/C07/D/E. Não declarar C03 PASS antes de Actions e readback.
- **Próximo:** conferir diff, publicar somente em design, executar CI remoto, recuperar provas e registrar resultado em C03; C04 permanece dependente de C03 PASS.


#### C03 — Fechamento verificável do mecanismo isolado (2026-11-12)

- **Estado:** `C03_PASS_SCOPED` com implementação não operacional em `design@5f1c15dde738ecc7983ef994f9115212e1c00829`. `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura e sem alteração. A03/A05 e a prova de C02 seguem fontes fixadas.
- **Evidência real:** GitHub Actions `43236381679`, job `131244735495`, `completed/success`, teste remoto V05/V10 `1/1` cenário composto com múltiplas invariantes. Na ref descartável `test/adr001-c03-43236381679-1`, uma transação publicou **dois blobs** no mesmo commit `f942ac1610a6a9ee8a2a97af949f35b064695ffa`, com pai exato `5f1c15dde738ecc7983ef994f9115212e1c00829`, tree/blobs relidos; duplicata `NO_OP_VERIFIED`, mesmo ID divergente `STOP_CONFLICT_SAME_ID`, stale `STALE_HEAD_PRECHECK`, dois escritores com único vencedor `cd15dff384253cebddd8bc1999c141caf17f1a84` e perdedor `STOP_CONFLICT_STALE_REMOTE`. Criar objeto sem promover manteve ref; leitura adversarial detectou `READBACK_BLOB_MISMATCH`. Supressão de ACK **após publicação real** foi recuperada por `NO_OP_VERIFIED` sem duplicar. Limpeza da ref confirmada por leitura 404.
- **Contrato/DEC-20/23/24/27:** apenas texto/estado TEST_ONLY em `tmp/adr001-c03/*`, fingerprint e `tx_id` em trailer Git, sem ledger universal, arquivo por rolagem, reconstrução por replay, cenas, mutação de fichas ou Codex duplicado. Operações Git efetivamente executadas no Actions, auditadas também pelo readback Web do commit/arquivos.
- **Limitações explícitas:** cliente restringe escrita a ref/paths artificiais; integração com owners, políticas sucessoras, segredo editorial e real runtime ainda não comprovada (C04/C05/C07/D/E). Perda de ACK foi induzida pelo cliente, **não** queda real da rede; erro de blob foi injeção adversarial de expectativa e não corrupção de objeto Git. `force:false` e rejeição remota na ref descartável foram comprovados, sem afirmar ruleset administrativo instalado ou proteção universal. Não ativar em master.
- **Próximas elegíveis:** C04 (estado atual e retomada) e C06 (auditoria de fontes/legado); depois C05/C07/C08 conforme dependências. Gate C geral permanece aberto; E01 continua dependente de D07 PASS e aprovação expressa antes de E02.

### C04 — Implementar estado atual e retomada fiel

- **Depende de:** C03 e A02/A03.
- **Escopo/saída:** estado atual por assunto com dono único, recursos/ficha, última intenção, cursor e conhecimento situado, vinculado às fontes pertinentes. Preservar lacunas históricas e acesso ao texto literal sem repetir toda a crônica na entrada. Conciliar inconsistências pelas fontes; sem exigir reconstrução universal por eventos ou auditoria de rolagens.
- **Conclusão:** V06/V07: consistência e recuperação em contexto renovado mantêm os mesmos saldos, consequências materiais e ponto de retomada, sem rerrolar ou restaurar recursos antigos. Nenhuma prova técnica de RNG é exigida ou inventada. Escrita falha não é apresentada como atualização confirmada. Checkpoint de tarefa/fase suporta continuidade no mesmo chat e handoff quando necessário, sem outro arquivo por verificação.

#### C04 — Implementação candidata; CI remoto pendente (2026-11-12)

- **Entrada:** `design@7a332796496a487677f040a26422a42e742f0de5`; `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura; C03 `PASS_SCOPED`, A02/A03 consultados. Não interpretar fonte histórica C41 como cursor C45.
- **Implementação não operacional:** `novydres/scripts/retomar-estado.mjs` relê `catalogo.json` no commit candidato, owner do checkpoint, dados de história/trama/conhecimento situados e fontes históricas pinadas `CYCLE_V0041`, `LIVE_v038` e texto literal. Confere recursos/ficha por aritmética e por fonte, materialidade, cursor, autoria, grau epistêmico, intenção ainda não recebida, não realização de fatos futuros, ausência de ledger técnico inventado e divergência temporal declarada. O retorno é mínimo, com localizadores, não entrega cena ou texto oculto. Retomada com HEAD divergente, fonte ausente/errada ou escrita não confirmada bloqueia.
- **Prova preparada:** `testar-retomada-estado.test.mjs` cobre V06/V07 com run isolado do estado candidato, repetição em nova invocação e mutações adversariais de recursos, fontes, cursor, obrigações, texto, conhecimento, confirmação e erro de HEAD. Reutiliza workflow de validação C existente, sem criar manifestos por cena/rolagem, replay universal, RNG e sem alterar o arquivo histórico `estado/atual.json`.
- **Limites:** `CI_PENDING` neste checkpoint; não há reconciliação C41→C45 nem reivindicação de prontidão para narrar. Fonte existente sustentar conclusão é revisão semântica separada, não decidida apenas por SHA. Prova de continuidade entre chats de DEC-25 é parcial: recuperação técnica reproduzível não verifica a memória/contexto de um modelo.
- **Próximo:** publicar diff com lease; rodar CI, conferir readback remoto, registrar C04 conforme resultados. Dependente C05 não liberado antes de C04 PASS_SCOPED.

#### C04 — Validação remota concluída (2026-11-12)

- **Estado:** `C04_PASS_SCOPED` exclusivamente para amostra histórica C41. Publicação `design@0ca990cd83283ebdeb5483a6632056c5932f59b4`, `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura. O checkpoint `CI_PENDING` acima é histórico, não apagado.
- **Prova executada:** GitHub Actions `43237946940`, job `131250285182`, `completed/success`. V06/V07 `15/15` testes específicos e `28/28` regressões C01/C02; comando standalone `retomar-estado.mjs` retornou `CANDIDATE_HISTORICAL_ONLY` no snapshot do run, fonte `c26c0fbf15fff6c817182c06e6208e302b954f3a` e 8 marcadores textuais. O validador consultou blobs Git históricamente pinados e rejeitou recursos/cursor divergentes, fontes inválidas, evento futuro, alegação reclassificada, uso do snapshot como operacional e falta de confirmação de escrita.
- **Restrições:** nenhum replay universal, auditoria RNG, atualização dos 5 assuntos, prova de que C41 coincide com C45, nem equivalência contextual irrestrita. Caso de alegação semanticamente errada porém estruturalmente válida foi isolado como risco de revisão contextual; hash não comprova verdade factual. Retomada técnica em nova invocação é determinística, mas não garante memória de modelo ou ausência de alucinação.
- **Dependências:** C05 agora elegível após C02–C04/A04; C06 permanece elegível independentemente. C07/C08 e D aguardam provas. Continuar sem ativar mesa.

### C05 — Integrar contrato de mesa e preparação proporcional

- **Depende de:** C02–C04 e A04.
- **Escopo/saída:** ferramentas e entradas aplicam o contrato candidato e as exceções locais, sem validadores/workflows novos por cena. Exercícios de narração isolados cobrem NPCs, concessões, rotina, intenções, prioridades, perdas/ganhos e mistério, conforme matriz IMP-01–IMP-15.
- **Conclusão:** revisão contextual da escrita, separada da integridade mecânica, verifica a função das regras retiradas. Nenhuma fixture cria fatos da campanha; sem quota de dano/recusa ou suposição de que um checklist torna a narrativa boa. Integrar também continuidade das tarefas A–E no Web (DEC-25), sem confundir esse procedimento de implementação com exigências adicionais por cena.

#### C05 — Contrato consolidado e revisão contextual reaproveitada (2026-11-12; CI pendente)

- **Entrada:** `design@748f803891a7a9ab36d39e1c46f62f43351dcec8`; `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura. Dependências C02/C03/C04 `PASS_SCOPED`, desenho A04 `simplificacao-narrativa/desenho.md` e ADR §11 DEC-01–27 lidos.
- **Implementação candidata não operacional:** `novydres/sistema/narrativa/contrato.md` consolida responsabilidades de narração/dramaturgia sem handoff por cena, autonomia causal NPC, sucesso social limitado mas efetivo, elipse opcional, prioridades em saltos relevantes, mistério com verdade fixada antes da pista, consequências e recursos sem novas obrigações de RNG/ledger. `novydres/CONTEXT.md` aponta o contrato, sem quarto bootstrap; novo subject `chr001-table-config` em `cronicas/CHR-001/configuracao/` (assunto/index/config), com owner único, `SYSTEM_AUDIT`, refs A04/ADR pinadas, fontes mecânicas/exceções **não inferidas**, e sem cena/ativação. Catálogo `novydres/catalogo.json` regenerado para **6 assuntos, 19 arquivos**, com índice SHA sem autorreferência; os 5 protótipos C41 mantêm bytes e limites históricos.
- **Exercícios e prova preparada:** `revisar-conducao-candidata.mjs` é diagnóstico **opcional de fixtures**, não geração de texto, gate de cena ou validador de qualidade literária. `testar-conducao-candidata.test.mjs` verifica seleção do contrato/configuração via catálogo, invariantes de agência, interesse, concessão, elipse, mistério, correção, persistência/recuperação, fontes e riscos. Reutilizar **sem reescrever** N-01–N-08/N-06-RESULT de `fase-b/resultado-testes.json` e revisão contextual em `fase-b/gate-e-readback.json`: N-06 inicial insuficiente e continuação com consequência preservada; revisor anterior foi de outra conversa, **não cego**; nenhum caso da campanha foi criado. Separar CI de formato/risco da revisão semântica; teste não certifica jogo real.
- **Limites/estado:** `C05_CI_PENDING`; manter gates mecânicos V5, variantes editoriais e compatibilidade C41→C45 para D/C07. DEC-25 controles de recuperação de implantação não se tornam novo requisito por cena. CI C01/C02/C04/C06 existente foi estendida, sem workflow dedicado por cena. Nenhuma autoridade de `master` ou da crônica alterada.
- **Próxima:** publicar com expected SHA/readback, testar no Actions e registrar resultado; C07 depende de C05 comprovada.

#### C05 — Fechamento com CI e revisão contextual anterior (2026-11-12)

- **Estado:** `C05_PASS_SCOPED` para contrato e configuração candidata, jamais execução de cena. Commit `47d6cd7d1a5d9e58e600d7db0bee045711795c09`; `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura.
- **Prova externa GitHub:** Actions `43249190298`, job `131290018740`, `completed/success`, **9/9** testes IMP-01/02/04–11 + **13/13** C01, **15/15** C02, **15/15** C04 e **11/11** C06. Gerador do catálogo byte-a-byte passou com seis subjects e 19 arquivos; os owners C41 históricos permanecem sem alteração de bytes. Readback de ref e blobs do catálogo `b0f60c3513644011118a1ff15fa9f6a18892653f` e configuração `79a17a901f644d2dd72227a5c215116f013ff34c` realizado.
- **Revisão contextual reaproveitada, não refeita como nova revisão cega:** saída N-01–N-08/N-06-RESULT em `fase-b/resultado-testes.json#narrative_exercises_2026_11_12`, com revisor em outra conversa conforme `fase-b/gate-e-readback.json#b05_independent_session_contextual_review_2026_11_12`. N-06 inicial `INSUFFICIENT` continua histórico, superado apenas pela continuação artificial. A avaliação separada não foi cega e não representa prova de prosa em jogo real; testes de código não pontuam qualidade literária.
- **Escopo e pendências:** contrato único em `sistema/narrativa/contrato.md` localizável por `CONTEXT.md` e assunto privado de configuração; `AGENTS.md/CONTEXT.md/catalogo.json` continuam apenas três entradas candidatas. Configuração declara exceções mecânicas V5 pendentes de checagem autoritativa; não altera G19/G23/G24/G26/G28 operacionais. A varredura C06 no commit contou 922 blobs e manteve 835 caminhos legados, cinco consumidores antigos e cinco originais visuais pendentes como riscos explícitos. Não afirmar `ZERO_LEGADO`, equivalência C41→C45, revisão semântica independente C07 ou DEC-25 universal.
- **Próxima elegível:** C07 para integração de CI, métricas observáveis e revisão de risco sobre o fluxo efetivo. C08/D ainda dependem da prova de C07.

### C06 — Implementar auditoria de fontes e detector de legado

- **Depende de:** C01/C02 e inventário de A01.
- **Escopo/saída:** V08/V11/V12 sobre toda árvore: código, JSON, prosa operacional, URLs, CI, symlinks, aliases, wrappers e fallbacks. Distinguir citação de proveniência de rota executável por regra verificável; conferir localização/direitos de mídia sem inventar hashes.
- **Conclusão:** resíduos operacionais e vazamentos nas fixtures são detectados, sem exclusão genérica de diretórios/documentação. Aprovar candidato isolado não significa que toda branch pré-cutover esteja ZERO LEGADO. Git histórico não vira fallback no HEAD.

#### C06 — Implementação pré-cutover e prova a executar (2026-11-12)

- **Entrada:** `design@f5a18cf499bc9cc936697f8a2ad82fdb29076d9c`, `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura; C01/C02 e A01 confirmados.
- **Implementação:** `novydres/scripts/auditar-legado-e-fontes.mjs` enumera todos os blobs da árvore Git, symlinks, raízes antigas, textos, código/config/CI, scripts e entradas candidatas; distingue citação histórica de uso executável e checa os pinos do catálogo. O registo V2 de ativos visuais é inspecionado sem download e sem inventar SHA externo. Testes em `testar-auditoria-legado.test.mjs` cobrem import/fallback, symlink, proveniência, metadados públicos, mídia e exigência de ZERO LEGADO em HEAD final.
- **Lacunas registradas:** fonte visual V2 possui 19 itens, 14 originais vinculados no Drive e 5 pendentes; 0 hashes externos verificados. A HEAD pré-cutover ainda contém caminhos legados e decisões editoriais pendentes. O resultado positivo da ferramenta é `C06_CANDIDATE_AUDIT_EXECUTED_WITH_LEGACY_PENDING`; a mesma árvore em `ZERO_LEGACY_FINAL` deve retornar `ZERO_LEGACY_BLOCKED`. Não tratar PASS da ferramenta como gate E.
- **Limite:** `CI_PENDING`; scanner de padrões não é parser AST universal nem auditoria semântica de segredos, direitos, permissões ou mídia externa. Não mutar canon, histórico, master, fixtures ou fontes Drive. Próxima prova: Actions real e readback do commit; revisão contextual e D exigem completar inventário e migração.

#### C06 — Auditoria remota executada, gate final corretamente bloqueado (2026-11-12)

- **Estado:** `C06_PASS_SCOPED` para a implementação/detecção da auditoria **não operacional**, não equivale a ZERO LEGADO. Implementação `2f8177877857cc3fe0c7cf7143b68da5dc76b8f4`, correção do falso negativo em `require('../runtime/...')` no commit `4ce3d2c6d058f565b3f926a877323facfff8a315`.
- **Provas GitHub Actions:** run `43239329003` falhou na primeira tentativa pelo limite de palavra da expressão regular que omitia imports relativos `require()`; mantido histórico. Run `43239520057`, job `131255831594`, `completed/success`: **11/11** testes V08/V11/V12, **15/15** C04, **15/15** C02 e **13/13** C01; auditoria standalone da mesma HEAD passou com `C06_CANDIDATE_AUDIT_EXECUTED_WITH_LEGACY_PENDING`. Exposição de segredo testada por metadados e caminhos; sem declaração de auditoria semântica universal.
- **Achados sem supressão:** árvore completa examinada `916/916` blobs: `835` caminhos/arquivos antigos (pré-cutover), `5` consumidores legados em código/config identificados e classificados como pendência, `539` arquivos textuais com menções legadas, nenhum symlink Git nesta HEAD, `19` ativos visuais de integridade SHA externa não verificada e `5` originais pendentes no Drive, `0` nomes de fonte oculta detectados nos pontos de entrada candidatos. O modo `ZERO_LEGACY_FINAL` sobre esta árvore é corretamente `ZERO_LEGACY_BLOCKED`. Contagens são diagnóstico e snapshot, não certificação de ausência de vazamento contextual, direitos/licença ou prontidão de cutover.
- **Limite:** scanner de padrões sintáticos e paths; revisão independente/AST efetivo de todos os consumers e bytes externos das mídias permanecem pendentes para C07/D/E. C06 comprova que o bloqueio é observável, não que a migração de toda a árvore tenha sido concluída. Preserve A01 e dados históricos sem apagar `835` caminhos para reduzir número.
- **Próximas elegíveis:** C05 (contrato de mesa/ensaio proporcional); depois C07, C08, D conforme dependências e provas; nenhuma escrita em master ou runtime.

### C07 — Integrar CI, fluxo de uso e regressões de produção

- **Depende de:** C01–C06.
- **Escopo/saída:** scripts e workflows finais, contratos das rotas efetivamente usadas, suíte crítica, erros de integração e métricas comparáveis e revisão independente de sigilo/escrita. Adaptar ou retirar workflows específicos antigos no candidato final; manter as provas necessárias.
- **Conclusão:** runs reais com commit e resultados reproduzíveis nas integrações efetivamente utilizadas; custo e p95 julgados pelos critérios de A06, exceções expressas. Teste de texto/palavra-chave não substitui cenário narrado nem demonstra ausência de vazamento contextual. Provar os controles DEC-25 com resultados externos recuperáveis no Web e falhas induzidas/recuperação; revisão semântica registra limites e falhas que escapam. Sem evidência real, a condição da dispensa de chat por fase permanece não demonstrada.

#### C07 — Integração de risco e métrica real de navegação (2026-11-12; CI pendente)

- **Base:** `design@f84a7e018dd86775bab0ef28795bb00b1d7ef65d`, `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura; C01–C06 `PASS_SCOPED`. Reutilizar prova real C03 de concorrência/idempotência do Actions `43236381679` sem refazer a corrida só para obter outra contagem (DEC-21/27).
- **Implementação integrada:** `novydres/scripts/testar-fluxo-integrado.test.mjs` liga catálogo, ID exato, configuração privada, checkpoint C41, controle de conhecimento, revisão narrativa fictícia anterior, `STOP` de publicação não confirmada, fingerprint/transação limitada a ref de teste e auditoria V08/V11/V12 de toda HEAD. A CI existente de C01/C02/C04/C05/C06 executa também C07, sem workflow por cena. Não há chamada de transação operacional nem nova cena.
- **Métrica real Web/GitHub — escopo C41 histórico e mesma informação de recursos:** snapshots `c26c0fbf15fff6c817182c06e6208e302b954f3a` (um LIVE histórico) e `f84a7e018dd86775bab0ef28795bb00b1d7ef65d` (catálogo + checkpoint candidato). Cinco pares sequenciais, com duas leituras do candidato em paralelo dentro de cada par. Baseline amostras ms `[411,516,497,653,433]`, p50 `497`, p95 nearest-rank `653`; candidato frio `[757,516,494,960,513]`, p50 `516`, p95 `960`. **Regressão fria de p95 ~47%, não esconder.** Respostas medidas em caracteres `24.539` contra `8.505`, não HTTP wire bytes nem tokens reais.
- **Investigação e cache:** a consulta fria faz **duas chamadas** em vez de uma, explicando custo adicional possível; catálogo já fixado no snapshot permite uma leitura seletiva subsequente. Cinco amostras quentes ms `[485,678,521,663,528]`, p50 `528`, p95 `678` (não inclui fetch inicial do catálogo); p95 quente ~3,8% acima do baseline frio, mas amostras pequenas e condições distintas. Registrar ambos, não tratá-los como equivalentes, nem inferir melhoria geral. Tokens Web e bytes HTTP wire: `NOT_OBSERVABLE` conforme DEC-19. Necessário retestar em D/E com cursor operacional atualizado e uso de sessão real, especialmente se a latência afetar experiência; DEC-22 não impõe nova consulta por porcentagem técnica isolada.
- **Revisão e riscos não comprovados:** revisão contextual narrativa anterior em outra conversa foi independente da autoria, **não cega**; não houve nova revisão independente do contrato C05, da semântica de sigilo em C07 nem dos limites da escrita em produção. Cinco workflows `novydres-*` antigos continuam na candidata e dependem de migração/retirada em D05; não removê-los antes de resolver suas dependências. ZERO LEGADO permanece BLOCKED com 835 caminhos antigos e cinco mídias originais pendentes, o que não impede um teste honesto do auditor C06, mas impede D/E.
- **Estado:** `C07_CI_PENDING_REVIEW_REQUIRED`. Após CI, readback e conferência externa, marcar `C07_PASS` somente com revisão proporcional de sigilo/escrita e integração suficiente, não pela palavra PASS no log; sem isso, C08/D bloqueados. Não ativar mesa.

#### C07 — Execução técnica remota concluída; revisão independente pendente (2026-11-12)

- **Status corrente:** `C07_TECH_PASS_REVIEW_REQUIRED`, **NÃO** `C07_PASS` e não autoriza C08/D. Histórico `CI_PENDING` acima permanece sem reescrita. Implementação commit `563fd0f4323b59950d3db41f4254b97fda684842` (design), `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura. A CI já integra todos os módulos C01/C02/C04/C05/C06 e C07 sem duplicar a prova C03 isolada.
- **Prova externa:** Actions `43250381801`, job `131294242995`, `completed/success`: **9/9** testes de fluxo C07, **9/9** C05, **13/13** C01, **15/15** C02, **15/15** C04, **11/11** C06, `72/72` testes no total. C03 permanece prova real da ref descartável no Actions `43236381679` com um vencedor remoto, conflito/stale e perda de confirmação simulada no cliente. Nenhum caso da campanha foi alterado.
- **Execução integrada verificada:** consulta por subject e commit exato; configuração privada `chr001-table-config`, `READBACK` do catálogo, limite PLAYER/AUDITOR, estado C41 com histórico pinado, `PENDING_PERSISTENCE` e `HEAD_DIFFERENT` distintos de confirmação; auditor de todos os blobs. Benchmark local Actions Node 22 no commit C07: cinco consultas seletivas, dez `git show` no total, p50 `25,65 ms`, p95 nearest-rank `26,68 ms`. **NÃO comparável** à latência do conector Web; nunca usar como melhora geral. HTTP wire bytes/tokens Web `NOT_OBSERVABLE`.
- **Limitações e pendências reais:** Web frio p95 `960 ms` contra `653 ms` na origem (mais duas chamadas versus uma), quente p95 `678 ms` excluindo fetch inicial; investigação registrada acima, sem esconder regressão. Varredura do commit C07: `923` blobs, `835` rotas/pastas legadas e `5` consumidores de código/config ainda a retirar em D05, `5` originais visuais faltantes, 19 SHA externos não verificados; E ZERO LEGADO corretamente bloqueado. Os exercícios N-01–N-08/N-06-RESULT tiveram revisão anterior separada não cega; novo contrato/roteadores/risco de sigilo contextual e política de escrita exigem **revisão independente ainda não realizada**. Falha semântica intencionalmente válida ao lint ficou exposta, não ocultada.
- **Decisão de gate:** `C07_REVIEW_REQUIRED` por critério já existente, sem reduzir escopo para PASS. Revisão independente proporcional deve ler a branch fixada e fontes sem depender da autocrítica, examinar política de divulgação, rótulos epistêmicos/atores, persistência/recuperação e pelo menos casos que possam passar tecnicamente mas falhar semanticamente; registrar constatações no backlog/arquivos atuais. C08 permanece bloqueado até a conclusão e readback desse exame. Nenhuma fase D iniciada.

#### C07 — Endurecimento de sigilo e checkpoint de revisão pendente (2026-11-12)

- **Defeito identificado no exame adversarial interno:** `resolveSubject`/`readSelected` em `catalogo-assuntos.mjs` assumiam papel `AUDITOR` em chamadas sem `role`; apesar de testes anteriores aprovados, era um padrão permissivo. Corrigido no commit `01ee96aa78cd2c9d8b9b1d1ddaad966838ff387d`: omissão de papel resulta em `ROLE_NOT_AUTHORIZED`, sem qualquer leitura privada implícita. Acrescentado negativo V04, sem alterações nas cinco fontes C41 ou no sexto subject candidato.
- **Regressão externa reexecutada:** GitHub Actions `43251191127`, job `131297111798`, `completed/success` no commit corrigido: **73/73 testes** somando C01 `13`, C02 `16`, C04 `15`, C05 `9`, C06 `11`, C07 `9`. C03 mantém Actions remoto `43236381679` válido porque código/transação isolada não mudou. Benchmark local novo `6,27`/p95 `7,69 ms` é variável e **não comparável** com medição Web p95 frio `960 ms`; não o usar para apagar regressão fria.
- **Sem independência declarada:** análise de risco acima feita pelo próprio executor, não substitui revisor separado da implementação C05/C07, divulgação, escrita/rollback e cenário semanticamente enganoso. Este remédio melhora o controle mas não encerra gate: `C07_TECH_PASS_REVIEW_REQUIRED`; `C08_NOT_ELIGIBLE`, `D_NOT_STARTED`, `E_NOT_AUTHORIZED`. A revisão necessária pode ser feita em outra conversa ChatGPT Web com conector GitHub **somente leitura**, usando commits e casos já fixados, registrando falhas sem expor segredos. Nenhum ritual de chat limpo é imposto às etapas sem essa necessidade de independência.
- **Estado de fontes:** `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura; auditoria de legado, originais Drive pendentes, conflitos editoriais e revisão completa de D não solucionados nem dispensados. Nenhuma cena, merge ou cutover.

#### C07 — Auditoria adversarial de consistência HEAD/checkout (2026-11-12; CI pendente)

- **Base antes da proposta:** `design@9cff3e9b7f2a2f0317dc35a4d12007cf42d37ac9`; `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura; CI `43251191127` sucessor C07 técnico `73/73` em código anterior. Revisão independente exigida permanece `PENDING`.
- **Vulnerabilidade encontrada na própria ferramenta:** `auditar-legado-e-fontes.mjs` enumerava caminhos/SHA da árvore Git **HEAD**, mas lia o conteúdo de texto e o registro de mídia via `readFileSync` na área de trabalho mutável. Um checkout não limpo, arquivo substituído ou symlink poderia mascarar o conteúdo realmente publicado e induzir uma conclusão falsa de V08/V11/V12. Embora a Action verificada usasse checkout limpo, não equivale à garantia de auditoria do snapshot prometida.
- **Correção proposta:** ler cada texto diretamente do blob Git `git cat-file blob <sha>` apontado por `git ls-tree <commit>`, verificar SHA Git dos bytes, usar registro de mídia do mesmo commit, comparar `expected_head` e `HEAD` antes/depois e inspecionar link simbólico como objeto, nunca seguir seu destino. Assim não misturar paths de HEAD com conteúdo do checkout. Acrescentar teste com repositório Git **TEST_ONLY** temporário: checkout adulterado não cobre segredo publicado; arquivo local não commitado não produz falso positivo; symlink não é dereferenciado; expected SHA stale bloqueia. Nenhum arquivo canônico/operacional será alterado.
- **Status:** `C07_HEAD_AUDIT_REMEDIATION_CI_PENDING`. Após CI real e readback, manter o requisito de revisão **independente** de escrita/sigilo e falhas semânticas; não declarar C07 integral, C08 ou D PASS por correção técnica.

#### C07 — Correção adicional de cache não confiável (2026-11-12; CI pendente)

- **Evidência já confirmada de HEAD:** Actions `43253243005`, job `131304482007`, `completed/success` em `design@62b8112156fb581319be4313765ce87e76dea9b9`: **74/74** testes; auditor lê exclusivamente objetos Git pinados, não checkout mutável, e teste negativo usa repositório Git TEST_ONLY temporário com conteúdo local trocado, referência GM_HIDDEN commitada e symlink; os três comportamentos foram detectados sem seguir symlink. A ferramenta confirma HEAD de 923 blobs e mantém 835 resíduos legados e 5 mídias pendentes como diagnóstico, não Zero Legado.
- **Outro defeito técnico descoberto:** `catalogo-assuntos.mjs#resolveSubject` acessava `cache.get` antes de checar autorização de `role=PLAYER`; um cache Map injetado manualmente com chave correspondente podia devolver metadados restritos e influenciar a leitura selecionada, embora a rota usual não construísse esse cache adulterado. Não supor que cache de chamador é confiável. A proposta inverte a ordem: autorização/owner/arquivo derivado sempre conferidos contra catálogo de snapshot antes de retornar cache; entrada envenenada retorna `CACHE_INTEGRITY`; `PLAYER` restrito recebe `DISCLOSURE_DENIED`. Acrescentados negativos de payload e ponteiro arbitrário, sem modificar dados da crônica.
- **Status da proposta:** `C07_CACHE_REMEDIATION_CI_PENDING`. Após publicação/CI, registrar resultado no backlog. Revisor independente de C05/C07 (sigilo contextual, escrita, rollback, prosa e falsos positivos semânticos) continua **NÃO EXECUTADO**; portanto `C07_TECH_PASS_REVIEW_REQUIRED`, `C08_NOT_ELIGIBLE`, `D_NOT_STARTED`. Não conceder PASS por mudança de critérios nem autorizar cutover.

#### C07 — Duas remediações de segurança confirmadas; escopo da revisão externa (2026-11-12)

- **Status técnico consolidado:** `C07_TECH_PASS_REVIEW_REQUIRED`. Remediação auditor HEAD: commit `62b8112156fb581319be4313765ce87e76dea9b9`, Actions `43253243005`/job `131304482007` `completed/success` **74/74** (C01 13, C02 16, C04 15, C05 9, C06 12, C07 9). Teste de checkout adulterado, HEAD com segredo e symlink aprovados; auditor agora consulta cada blob Git exato, não o working tree. Histórico de C06 com validação por WT é superado apenas no código, não apagado.
- **Segunda remediação:** commit `6077480e64ca3b02d1cb8ffd586c0df2c0ec64c2`, Actions `43253732882`/job `131306246632` `completed/success` **76/76** (C01 13, C02 18, C04 15, C05 9, C06 12, C07 9). O resolvedor agora autoriza antes do cache e verifica o conteúdo cacheado contra os metadados oficiais; negativos comprovam `DISCLOSURE_DENIED` para `PLAYER` com cache envenenado e `CACHE_INTEGRITY` para ponteiro/owner fraudado. Os 5 assuntos históricos C41, configuração C05, crônica, contratos e master não sofreram alteração.
- **Revisão independente AINDA NÃO EXECUTADA (gate C07):** outro revisor/contexto deve ler **código/fonte diretamente**, sem tratar o presente backlog ou autocrítica como gabarito, em `design@6077480e64ca3b02d1cb8ffd586c0df2c0ec64c2`, `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura. Fontes e código essenciais: `novydres/scripts/catalogo-assuntos.mjs`, `transacao-git.mjs`, `retomar-estado.mjs`, `auditar-legado-e-fontes.mjs`, `revisar-conducao-candidata.mjs`, `testar-fluxo-integrado.test.mjs`, `novydres/sistema/narrativa/contrato.md`, `novydres/cronicas/CHR-001/configuracao/configuracao.json`, A04 `simplificacao-narrativa/desenho.md`, ADR-001 §11, A06 `validacao-e-metricas.md`, B05 `gate-e-readback.json`. Verificar por exemplo: role fornecida pelo chamador **não** equivale a autenticação Git; divulgação de nomes de assuntos/paths privados em `catalogo.json`; noção de proveniência não é prova semântica nem conhecimento do ator; transação C03 restringe-se a ref TEST_ONLY; V08/V12 scanner não é AST nem auditoria universal de prosa/URLs; explicação de falha de escrita, readback e duplicação; padrões semanticamente falsos que passam lints; possíveis regressões de tipagem/schema; testes de narrativa são TEST_ONLY, revisão B05 anterior não cega. Avaliar contraprovas e impacto real, não inventar cenas/segredos. Relatar `PASS_SCOPED` ou `REMEDIATION_REQUIRED` com evidências; não criar novos critérios nem dispensar existentes.
- **Pendências e ordem:** `C08_NOT_ELIGIBLE` e `D_NOT_STARTED` até conclusão publicada da revisão independente de C07 e fechamento posterior de C08. Master, runtime e material CANÔNICO/FECHADO intocados; `ZERO_LEGACY_FINAL` continua BLOCKED pelos 835 caminhos antigos, cinco consumidores/config e cinco visuais pendentes (contagens do snapshot candidato anterior; reconferir em D). C07 não comprova controle de autenticação remota pelo marcador `role` nem ausência de segredos semânticos. Sem autorização de E e sem cutover.

### C08 — Revisar e encerrar gate C

- **Depende de:** C07.
- **Escopo/saída:** conferir V01–V12, contratos implementados, regressões, limitações e readback. Relacionar cada requisito à prova, sem declarar equivalência integral ainda não migrada.
- **Conclusão:** C PASS apenas sem lacuna bloqueante, com CI e rota funcional aplicável comprovada; no plano futuramente autorizado, seguir para D conforme DEC-22, sem nova confirmação apenas pela fase. Runtime antigo continua operacional até E.

## D — Migrar toda a árvore candidata

### D01 — Fixar snapshot e fechar inventário por origem

- **Depende de:** C08 PASS e entrada pertinente de D.
- **Escopo/saída:** revalidar master, fixar baseline e inventariar TODAS as entradas e dependências controladas. Mapa por caminho/SHA, autoridade, owner, informação, destino/retirada, transformação, conhecimento/visibilidade, conflitos e prova. Incluir raiz, `.github`, binários, mídia, fontes, ferramentas, planos e fixtures.
- **Conclusão:** denominador reproduzível do inventário, sem exclusões arbitrárias nem número histórico de arquivos tratado como cobertura atual. Escopo externo é o efetivamente referenciado/controlado; não mover todo o acervo do diretório pai.

### D02 — Migrar governança, fontes e mídia

- **Depende de:** D01.
- **Escopo/saída:** políticas e decisões com sucessão explícita, proveniência, originais/documentos autoritativos, registros de fontes e mídia. Respeitar congelamento e maturidade editorial. Original cuja autoridade/localização é Drive permanece lá conforme política; metadados verificáveis no destino correto, sem cópia binária indiscriminada.
- **Conclusão:** decisões/approvals preservadas; conflitos conhecidos das fontes, variantes de NPC e mídia pendente resolvidos ou classificados legitimamente não bloqueantes. Arquivar revisão no Git não elimina uma fonte atual necessária.

### D03 — Migrar cenário e identidades globais

- **Depende de:** D01 e destinos de D02 necessários às fontes.
- **Escopo/saída:** `cenario/`, regras/sistema e `personagens/` globais: lore, organizações, lugares, história, fichas, fontes e relações por assunto. Separar perfil global de relação/conhecimento local. Não promover invenção de campanha ao suplemento por mover arquivo.
- **Conclusão:** informação autoritativa, episteme, fontes e relações equivalentes; owner único e vínculos resolvidos. Divergências editoriais não harmonizadas silenciosamente; sem diretório obrigatório vazio.

### D04 — Migrar crônicas, história, preparação e estado

- **Depende de:** D01, identidades/fontes necessárias de D02/D03.
- **Escopo/saída:** todas as crônicas do snapshot, não só os quatro exemplos: texto disponível, episódios, cenas, tramas, elenco/conhecimento, segredos, registros, correções, recursos, ficha-alvo, estado e ponto de retomada. Separar preparação futura de fato jogado e prosa antiga de transcrição inexistente. Preservar fontes existentes sem recriar ledger de eventos, faces ou trilha RNG dispensados por DEC-23/DEC-24.
- **Conclusão:** nenhum fato, escolha, recurso ou texto necessário perdido; nenhuma cena, rolagem ou elipse inventada. Estado atual reconciliado, limites de conhecimento preservados e âncoras guiadas intactas. Apenas mover pastas não conclui a migração semântica.

### D05 — Migrar consumidores e retirar procedimentos substituídos

- **Depende de:** D01 e interfaces/destinos definidos em D02–D04.
- **Escopo/saída:** contratos, bootstrap, scripts, schemas, imports, automações, workflows, documentação corrente e dependências externas operacionais. Aplicar sucessores narrativos/governança e retirar nomes versionados, caminhos antigos e cadeias de adendos do candidato final. Dar destino ao POC e às provas úteis; adaptar também este plano e seus links quando deixarem de ser correntes. Migrar o checkpoint/handoff e o procedimento DEC-25 sem reintroduzir troca obrigatória por fase ou autoavaliação apresentada como detector universal.
- **Conclusão:** um único fluxo operacional na árvore final; apenas `AGENTS.md`, `CONTEXT.md` e `catalogo.json` como entradas. Nenhum alias/arquivo morto/fallback como compatibilidade. Histórico necessário preservado como fonte nova ou Git, conforme o mapa.

### D06 — Provar cobertura, equivalência e prontidão da árvore final

- **Depende de:** D02–D05.
- **Escopo/saída:** executar ferramentas de C no candidato completo e comparar origem/destino por informação; testar consistência e retomada do estado, consultas, escrita, sigilo, fontes, mídia e scanner integral. Conferir cada entrada do inventário e cada requisito da matriz, inclusive mudanças deliberadas de procedimento aprovadas.
- **Conclusão:** 100% de origens tratadas, vínculos resolvidos e invariantes preservados, sem conflito bloqueante, falso CONFIRMED ou fonte sem destino. ZERO LEGADO comprovado na árvore candidata exata, não apenas num subtree selecionado. Preparar evidência e diff para E.

### D07 — Revisar independentemente e encerrar gate D

- **Depende de:** D06.
- **Escopo/saída:** revisão independente de equivalência, escrita, sigilo, sucessores e plano de promoção/incidente. Corrigir falhas no candidato e repetir somente provas afetadas; reconciliar qualquer drift antes de encerrar.
- **Conclusão:** D PASS com revisão identificável, pendências não bloqueantes justificadas e snapshot de candidato exato. Não ativar a migração; apresentar a entrega concreta em E01 para aprovação expressa de cutover. Escolhas de política já aceitas não são perguntadas novamente; mudanças substantivas residuais devem ser resolvidas.

## E — Promover e encerrar todo o ADR

### E01 — Preparar promoção final e obter autorização específica

- **Depende de:** D07 PASS.
- **Escopo/saída:** redescobrir master e candidato, reconciliar commits novos com nova prova, apresentar diff final e políticas sucessoras, tag/checkpoint pré-cutover e plano de incidente. Confirmar proteção de ref e condições de promoção. Obter decisão expressa de cutover e das sucessões necessárias, se ainda não aprovadas.
- **Conclusão:** árvore completa revisável, expected parent/SHA e aprovações inequívocas para esse escopo; nenhuma mudança pendente escondida. Sem autorização, não promover. Nova divergência material exige revalidar, não forçar atualização.

### E02 — Promover atomicamente e verificar a publicação

- **Depende de:** E01 concluída com autorização pertinente.
- **Escopo/saída:** criar checkpoint/tag conforme plano autorizado e promover a árvore final num único commit com parent esperado e proteção contra stale SHA. Remover rotas antigas no mesmo corte; verificar ref, commit, árvore e blobs publicados.
- **Conclusão:** HEAD remoto exato corresponde ao candidato aprovado, sem legado operacional ou mistura de snapshots. Falha antes da promoção mantém baseline; falha depois inicia procedimento de incidente com preservação dos novos registros, sem retorno silencioso. Não iniciar cena.

### E03 — Verificar o HEAD promovido e encerrar integralmente o ADR

- **Depende de:** E02.
- **Escopo/saída:** CI real no commit promovido, smoke tests de leitura/escrita/retomada no fluxo de uso efetivo em ambiente seguro, revisão de sigilo e scanner de toda HEAD/dependências controladas. Atualizar matriz com evidência definitiva, documentação corrente e estado final dos gates; manter barreira anti-regressão para commits seguintes.
- **Conclusão:** todos os requisitos do ADR e sucessores aprovados implementados, migração completa, versões via Git, ZERO LEGADO e equivalência comprovados; nenhuma pendência bloqueante transferida a uma futura tarefa. Só então E PASS/ADR IMPLEMENTADO. Se houver falha, programa não encerrado. Isso não autoriza cena nem certifica eficácia narrativa ainda não observada em jogo.

## Registro de execução

Nenhuma tarefa concluída por esta elaboração documental. Registrar futuramente sob o ID correspondente: estado, snapshot, saídas, evidências, limites e decisão de gate quando aplicável. Não criar T31 de “terminar a migração” depois de E03; qualquer descoberta obrigatória deve entrar no escopo e impedir o encerramento até ser resolvida.

### B01–B05 — Checkpoint de execução (2026-11-12; ChatGPT Web/GitHub)

- B01 **PASS_SCOPED_HISTORICAL** — 4 assuntos, 7 grupos de mapeamento e fontes fixas, delta C41→C45 declarado; `fase-b/matriz-equivalencia.json`.
- B02 **CODEX_NOT_EXECUTED** — ferramenta não disponível; preservar 51/90 e B-Q29/30, sem PASS substituto.
- B03 **PASS_SCOPED_AUTO_GRADING** — 30/30, snapshot pinado, localizadores por caso; falta revisão semântica independente; `fase-b/resultado-testes.json`.
- B04 **PARTIAL** — 12 negativos + 12 jornadas + 7 guardas sintéticas em CI real 43155672041 (`success`); 2 recusas 404 reais; corrida remota com vencedor único e falha concorrente sem motivo de stale classificado. Confirmação perdida simulada apenas localmente. Ref de teste não apagada.
- B05 **B_REMEDIATION_REQUIRED** — `fase-b/gate-e-readback.json#b05_consolidation_2026_11_12`; Codex, revisão independente e diagnósticos/stale remotos pendentes. DEC-25 parcial e DEC-26 em unidade bloqueada; C01 não liberada. `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura. Próxima tarefa elegível: B02 com Codex real, revisão B03, complementação B04 e reavaliação B05.


### B02–B05 — checkpoint Codex real (2026-11-12; evidência pronta para publicação)

- B02: 30 casos executados por Codex CLI real. Revisão independente: 17/30 na rodada inicial; 13 afirmações genéricas de proveniência falharam. Após corrigir apenas o prompt, os 13 casos afetados passaram em nova execução e revisão independente; cobertura efetiva 30/30, incluindo B-Q26/B-Q29/B-Q30. Causa das falhas históricas Q29/Q30 segue indeterminada; respostas antigas ausentes. `fase-b/resultado-testes.json#b02_codex_real_2026_11_12`.
- B03 antigo: `RAW_RESPONSES_UNAVAILABLE_FOR_INDEPENDENT_REVIEW`; não reconstruído. B04 permanece parcial. Probe remoto `expected_sha` recebeu erro GraphQL genérico; ref de design e `master` permaneceram iguais, então stale SHA não foi comprovado. Runner CI é isolado/sintético; não existe rota real para idempotência, conflito de ID, guards ou recuperação após perda de confirmação.
- B05 `B_REMEDIATION_REQUIRED`; commit `b73eb073` e cinco blobs lidos de volta; CI 43212545361/job 131163549104 passou no commit publicado. Respostas Web originais continuam indisponíveis para revisão independente; DEC-25 parcial e DEC-26 restrita a essa unidade. C bloqueada. Próximo: recuperar respostas Web originais se existir cópia e reavaliar B05; testes de rota B04 dependem de rota real existente. Não iniciar C.

### Retomada DEC-27 — execução funcional e evidências B (2026-11-12)

- **Regra vigente:** decisão nova do jogador revoga a exigência de provar duas interfaces. B02 independente 30/30 no snapshot histórico pode ser reaproveitada; as falhas anteriores permanecem históricas. B03 preserva a rodada Web nova `00d1633` e a retestagem `c8afeab`, com conferência determinística 6/6 no CI `43221036507`; revisão independente das respostas novas continua pendente.
- **B04 real:** executor mínimo no Actions em ref `test/adr001-b04-ci-*` descarta dados artificiais após execução. Run `43220528637`: publicação/readback, idempotência, conflito de ID, duas escritas concorrentes e um vencedor, confirmação suprimida recuperada, dez guardas e `stale info` explícito em Git transport; REST 422 genérico não certifica rejeição nativa por SHA. Não houve injeção de falha de rede real. DEC-25 prova guardas específicos e recuperação no mesmo chat, não detector universal.
- **Narrativa:** oito cenas artificiais congeladas e consequência ficcional adicional; autocrítica N-06 registrada; falta avaliação editorial independente. Métrica nova de leitura REST pareada foi implementada; p95 histórico Web continua ausente, sem extrapolação.
- **B05:** `B_REMEDIATION_REQUIRED` até revisar semanticamente respostas novas/cenas por avaliador independente, conferir métricas e último CI. Próxima unidade elegível: revisão independente focada + ajuste dos casos que falharem, depois B05; **não iniciar C**. Não há requisito de Codex adicional só por nome de canal. Fonte de verdade: `fase-b/gate-e-readback.json#b05_dec27_current`.

**Readback técnico adicional do checkpoint DEC-27:** Actions `43221967102` e `43222461058` concluídos com PASS, cobrindo código atual do executor/scorer. A amostra comparável restrita a REST registrou p50 198 ms (12 leituras fonte) versus 187 ms (12 leituras candidato), corpos JSON distintos e p95 histórico NOT_OBSERVABLE/NOT_REPORTED. Isso não remove as duas revisões contextuais independentes pendentes em B05. A próxima tarefa elegível continua revisão independente focalizada, não C01.


### B05 — Revisão contextual cruzada delimitada (2026-11-12)

Uma nova conversa Web conferiu separadamente as fontes Git fixadas de B-Q01/B-Q11/B-Q21/B-Q26/B-Q29/B-Q30 e avaliou o conteúdo narrado de N-01 a N-08 e N-06-RESULT. Os três pedidos factuais inicialmente incompletos só contam após reteste congelado. N-06 inicial continua INSUFFICIENT, com consequência causal na continuação fictícia. Evidência por caso: `fase-b/gate-e-readback.json#b05_independent_session_contextual_review_2026_11_12`. A conversa revisora teve acesso à autoavaliação anterior: **não se certifica revisão cega**. B05 permanece `B_REMEDIATION_REQUIRED`; a próxima unidade é revisão cega com prompts e fontes congelados antes da autoavaliação, correção das falhas e nova decisão B05. Nenhuma prova histórica foi reclassificada, e nenhuma alteração de runtime/campanha ocorreu.


### Reavaliação do gate B05 — 2026-11-12

A revisão factual e narrativa registrada em `fase-b/gate-e-readback.json#b05_independent_session_contextual_review_2026_11_12` ocorreu em conversa ChatGPT Web separada da produção dos exercícios. O revisor viu a autoavaliação anterior: a revisão não foi cega e esse risco de ancoragem fica explícito. Os critérios aceitos exigem revisão contextual independente, mas não cegamento; portanto a limitação não cria um bloqueio adicional.

B-Q01/Q11/Q21/Q26/Q29/Q30 foram conferidas contra fontes fixadas, preservando as respostas iniciais incompletas e os retestes. N-01–N-08 e N-06-RESULT receberam avaliação contextual; a insuficiência inicial de N-06 continua registrada. Os exercícios são TEST_ONLY, não certificam cenas de runtime. Respostas Web antigas indisponíveis permanecem sem revisão. Com a evidência B02–B04, os controles DEC-25 no escopo testado, os limites aceitos por DEC-19/DEC-26 e o CI `43223477154` concluído com sucesso, **B05 passa como B_PASS_SCOPED**.

A condição do gate para C01 está atendida, mas esta alteração documental não inicia a implementação nem autoriza cutover. Quando o trabalho for iniciado pelo prompt acordado, C01 é a próxima unidade elegível e deve atualizar a leitura das fontes atuais, preservando a diferença entre o snapshot C41 e o cursor operacional C45.

### C07 — Revisão independente inicial de código e contratos (2026-11-12; antes da reconciliação com checkpoints)

- **Snapshot examinado diretamente:** `design@96bb6a7d95a2f1c82b9b528ab70d410fb5b0e8c7`; `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` somente leitura. Exame dos cinco módulos C02–C06, C07 integrado, contrato C05, configuração local e workflows; decisões §11, A04/A06 como critério, não conclusão histórica como gabarito. Esta revisão não comprova ausência universal de erros semânticos.
- **Defeito efetivo RI-01 (divulgação contextual):** um assunto `PLAYER_SAFE` podia devolver `dependencies` contendo um `subject_id` `SYSTEM_AUDIT`, lista completa de `source_ids` e o `assunto.json` com referências internas pela API de `resolveSubject/readSelected(role=PLAYER)`. `DISCLOSURE_DENIED` de leitura direta do assunto privado não bastava. Corrigir metadados retornados ao PLAYER e negar leitura do manifesto técnico nesse papel, preservando resolução completa para AUDITOR.
- **Defeito efetivo RI-02 (gate final de mídia):** `auditRepository(mode=ZERO_LEGACY_FINAL)` exigia ler o registro `novydres/migration/VISUAL_ASSET_REGISTRY_V2.json`, cujo próprio caminho é legado proibido pelo gate. Depois da remoção legítima em D, a auditoria passaria a lançar `MEDIA_REGISTRY_INVALID` mesmo com fonte nova migrada; e `auditTree(...,mediaRegistry=null)` podia tratar ausência de mídia como prova vazia. Corrigir consulta final para `novydres/fontes/registro.json` pinado no HEAD futuro, sem fallback, e retornar bloqueio explícito se ainda ausente. Esse caminho é destino de contrato para D02, não criação/ativação prematura.
- **Riscos ainda abertos:** `role` é parâmetro declarado pelo chamador, não identidade autenticada; o catálogo bruto no repositório pode conter nomes de assuntos restritos e nunca deve ser enviado como resposta pública; arquivos estruturados `PLAYER_SAFE` requerem inspeção semântica antes da divulgação; o mecanismo C03 existe somente na ref TEST_ONLY, não oferece transação de produção; os false positives estruturais de `examineFictionalFrame` são explicitamente reproduzíveis. A auditoria é regex/paths, não AST, nem validação dos bytes de mídia externa.
- **Classificações:** RI-01 e RI-02 são defeitos demonstrados pelo fluxo/código; falta de autenticação do chamador e semântica de prosa são riscos de integração e limites de escopo, não falhas corrigíveis por renomear PASS. Os bytes HTTP/tokens e a qualidade real da narração continuam `NOT_OBSERVABLE`/não demonstrados nesta prova. Não avançar gates sem CI real, readback e reavaliação.

### C07 — Resultado da remediação e gate revisado (2026-11-12)

- **Revisão independente:** código e contratos do commit `96bb6a7d95a2f1c82b9b528ab70d410fb5b0e8c7` avaliados diretamente; só depois conferidas decisões, checkpoints históricos B/C e seus limites. RI-01 e RI-02 identificados nesta revisão, não aprovados por autoavaliação. Os contraexemplos não reescrevem os 76/76 testes históricos.
- **Correção atômica na design:** commit `3108fabeec604c3f7273928bf996221551f23d9d`, árvore `3e7835324776e1afa35aa3aea7ca24b34951cd89`, pai `96bb6a7d95a2f1c82b9b528ab70d410fb5b0e8c7`, seis blobs lidos por SHA e HEAD remoto confirmado. RI-01 filtra dependências privadas, source IDs e manifesto técnico quando `role=PLAYER`; RI-02 exige mídia migrada no modo final e nega sucesso quando falta. Nenhuma alteração de dados canônicos, estado operacional, config da crônica, C03 ou `master`.
- **CI remoto novo:** Actions `43260930785`, job `131331696750`, `completed/success` no commit: C01 `13/13`; C02 `19/19`; C04 `15/15`; C06 `13/13`; C05 `9/9`; C07 `10/10`; total **79/79, zero falhas**. Regressoes de RI-01/RI-02 executadas em GitHub Actions, não em execução local simulada. C03 não mudou: reutilizada prova remota real `43236381679`/job `131244735495`, `completed/success`, com ref descartável, dois escritores/um vencedor, readback, idempotência, conflito, confirmação perdida e cleanup confirmado (DEC-21/27).
- **Contraprovas semânticas e de fonte:** um `reported_fact` inventado sem fonte passa pelo lint `examineFictionalFrame`, portanto a ferramenta NÃO certifica a prosa; conteúdo ficcional N-01–N-08 e N-06-RESULT manteve avaliação contextual anterior separada, não cega, com N-06 inicial insuficiente e continuação revisada. A revisão de código confirmou que `retomar-estado.mjs` confere C41 histórico, pins e recursos mas não certifica equivalência ao cursor corrente C45; `continuationDecision` exige evidência fornecida, não autentica sozinho uma transação. O contrato C05 respeita DEC-01–27 em desenho, sem prova de comportamento narrativo em jogo.
- **Métricas/limites:** consulta Web fria anteriormente medida p95 960 ms contra 653 ms na origem (regressão investigada, duas leituras vs uma); quente p95 678 ms sem fetch inicial e NÃO equivalente ao frio; microbenchmark Node22 Actions no commit atual não substitui métricas Web. Tokens e bytes HTTP `NOT_OBSERVABLE` (DEC-19). Auditoria C06 agora leu `923/923` blobs do HEAD, `0` symlinks, `835` caminhos legados, `5` consumidores antigos, `5` originais visuais pendentes, `19` SHA externos não verificados; `ZERO_LEGACY_BLOCKED` permanece verdadeiro. AST/prosa integral/mídia externa e autenticação de papéis não foram demonstradas.
- **Decisão:** `C07_PASS_SCOPED` para as funções candidatas testadas, inclusive revisão independente e CI externo. Isso **não** significa `ZERO_LEGACY_PASS`, `RUNTIME_CERTIFIED`, autenticação de `role` contra GitHub, proteção contra todos os vazamentos contextuais ou que um caso estruturalmente válido seja narrativamente verdadeiro. DEC-26 aceita o risco semântico residual, não autoriza uso operacional. C08 passa a ser elegível.

### C08 — Revisão de fechamento do gate C (2026-11-12)

- **Prova examinada:** commit `3108fabeec604c3f7273928bf996221551f23d9d`, seis blobs remotos verificados e CI `43260930785`/job `131331696750` de 79/79; C03 permanece na prova `43236381679` sem mudança de implementação. O catálogo e os conteúdos da amostra ficam pinados à mesma HEAD; não comparar C41 histórico com C45 atual como se fossem mesma fonte.
- **Matriz V01–V12:** V01/V02 (schema/ownership), V03/V04 (fontes/visibilidade) na suíte C01+C02, incluindo negativo de metadados; V05/V10 (atomicidade, história, lease, confirmação e readback) em C03 remoto TEST_ONLY; V06/V07 (estado, autoria, cursor e recuperação) em C04; V08 (bloqueio de divulgação e análise independente contextual delimitada) em C02/C06/C07 e revisão presente; V09 (catálogo/hash/cache) em C02; V11 (localizador e integridade da mídia, prova de pendências e fail-closed no modo final) em C06; V12 (detector da árvore inteira, paths e consumidores) em C06. V08/V11/V12 NÃO são certificação universal: análise AST de todos os consumidores, inspeção semântica integral, bytes externos de mídia e ZERO LEGADO pertencem à prova final de D/E.
- **Conflitos e pendências preservados:** 835 caminhos legados e cinco consumidores permanecem para D05; cinco originais e 19 verificações externas para D02/D06; matriz integral owner/destino/source e conciliação C41↔cursor atual para D01–D04; acesso ao catálogo bruto e marcadores de papel não substituem isolamento de divulgação. Nenhuma aprovação congelada foi reinterpretada.
- **Decisão:** `C08_PASS_SCOPED` — fase C concluída somente no escopo candidato não operacional, sem elevar provas estruturais a verdade semântica e sem dispensar verificações D06/D07/E03. Conforme DEC-22/27, D01 torna-se elegível; E02, runtime e cenas continuam bloqueados.

### D01 — Abertura de inventário de origem e divergência (2026-11-12; em execução)

- **Snapshot fixado para levantamento (não promoção):** candidata `3108fabeec604c3f7273928bf996221551f23d9d` / árvore `3e7835324776e1afa35aa3aea7ca24b34951cd89`; `master` somente leitura `c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` / árvore `4894bebafcc872dcd7c772ea4d34e5d54079b810`. Ambas as árvores Git recursivas vieram completas (`truncated=false`), sem symlinks: design `923` blobs e `100` diretórios; master `1029` blobs e `81` diretórios. As árvores Git vinculam cada caminho ao respectivo blob SHA para reconciliação; contagens não substituem a matriz editorial.
- **Divergência verificável:** `compare master...design` devolveu `diverged`, `ahead=71`, `behind=28`, merge-base `cb9aa9e422fb0327e04e9eb0929e4ab678785405`. Não resetar, não promover automaticamente versões de `master`, não pressupor que os 1029 blobs são subconjunto da design. C41 amostral permanece distinto de C45/estado operacional mais novo; redescobrir autoridade por objeto e contrato ao mapear.
- **Escopo inventariado sintaticamente:** Git tree enumera `.github`, bootstrap, `chronicles`, `runtime`, `governance`, `migration`, `systems`, `world`, `poc`, novos `cronicas/personagens/sistema/scripts`, mídia e documentação. C06 tem `923/923` objetos blob escaneados. **Ainda não existe mapa concluído de 100% dos owners, destinos, classificações, direitos e decisões editoriais por fonte.** O gate D01 permanece `D01_IN_PROGRESS`, não PASS.
- **Próxima ação D01:** reconciliar os 28 commits de master ausentes na linha da design, mapear por caminho/SHA os proprietários, classificações, destinos e conflitos, atualizar o inventário existente sem fabricar status de aprovação nem alterar arquivos fechados; D02–D07 bloqueadas até prova D01. Não fazer cutover ou execução de cena.

### D01 — Inventário estrutural fixado com prova automatizada (2026-11-12; CI PENDENTE)

- **Base read-only verificada antes da escrita:** `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` (árvore `4894bebafcc872dcd7c772ea4d34e5d54079b810`), candidata `design@5a88739f1ca4c6758697aa597e4e591f298262d6` (árvore `5d81d3b011fd74415c3916200fda9ed2af84701f`). Git trees recursivas não truncadas, nenhum symlink; leitura de objetos, sem shell local/sem Codex.
- **Artefato D01 único e restrito a agentes:** `sistema/arquitetura/fase-d/inventario-origens.json` com `SYSTEM_AUDIT_NOT_PLAYER_REPORT`. Enumera exatamente **1029 blobs** por path+SHA+mode do `master`, 83 paths exclusivos da candidata, caminhos/SHA correspondentes 839 idênticos, 1 divergente, 189 ausentes do layout candidato. Destino e owner são `PROPOSTOS` por família, com `NOT_AUDITED_BY_PATH_INDEX` e `PENDING_FIELD_REVIEW` em cada origem. Nenhuma classificação por nome vira aprovação, nenhum segredo é reproduzido no relatório público.
- **Fontes controladas externas:** 193 entradas da fonte `migration/INVENTORY.json` pinada no master, `discovery_status=PARTIAL`; 19 registros de mídia de `migration/VISUAL_ASSET_REGISTRY_V2.json`, cinco originais pendentes e 19 SHA externos não verificados. O inventário preserva IDs e rótulos de governança apenas como metadados herdados, sem apresentar esses rótulos como veredito. Essas contagens não são somadas aos blobs: fontes externas podem referir cópias Git.
- **Âncora operacional para reconciliação (sem ativação):** `CYCLE_V0045.json` (C45) aponta a `MANIFEST_V63.json`; 77 pins de caminhos/objetos e o predecessor imediato conferidos contra a árvore Git do `master` (77/77). Isso não afirma que toda cadeia de precedentes ou os documentos em si estão semanticamente validados. A candidata de B/C baseada em C41 não se torna o cursor corrente por esta verificação.
- **Regressões preparadas:** `scripts/verificar-inventario-d01.mjs` compara todos os paths/SHA/mode com `git ls-tree` de ambos os commits imutáveis, reconcilia refs externas e pinos de C45. `scripts/testar-inventario-d01.test.mjs` injeta omissão, duplicação, hash trocado, relacionamento de branch inventado, fonte externa adulterada, mídia falsamente verificada, alteração de pins e liberação prematura do gate. Workflow existente C/D recebe verificação e negativos; commit/CI/readback ainda requeridos.
- **Limites:** D01 permanece `D01_IN_PROGRESS`, não concluído por enumerar blobs. Estão pendentes autoridade e destino **por conteúdo**, visibilidade/episteme por campo, dependências/imports, classificação de 193 fontes externas e conflitos CONFLICT-001/002/003/003B onde aplicáveis; 189 ausências precisam decisão explícita sobre sucessão ou preservação no Git. Não migrar arquivos operacionais, não editar congelados, não criar histórias, não mover `master`.

### D01 — Impacto de C45 na candidata (2026-11-12; CI de incremento pendente)

- A comparação do manifesto pinado por C45 contém 77 referências ao todo, mas **73 caminhos únicos** (quatro referências reiteradas). Entre os 73, **53 caminhos de fontes operacionais pinadas não existem no mesmo path da candidata** e 20 estão presentes com blob idêntico. Essa distinção importa: `77` referências não são 77 documentos distintos e ausência no candidato não significa perda em `master`.
- O inventário D01 agora marca cada origem pinada pela autoridade de C45 e sua relação com a branch candidata; o verificador e teste adversarial recusam reclassificar uma fonte operacional ausente como se fosse presente. Fica proibido projetar a amostra C41 como substituta do estado corrente C45.
- Os registros externos permanecem `PARTIAL`: 151 cópias textuais verificadas segundo inventário histórico, 19 fontes referenciadas não copiadas, 14 pastas enumeradas e 9 objetos brutos Git, sem transformar essas etiquetas legadas em veredito editorial novo. 33 entradas não têm destino de arquivo Git no inventário porque são referências ou pastas, não necessariamente perda.
- **Gate permanece `D01_IN_PROGRESS`** até conciliar conteúdo/autoridade/destino e dependências por fonte. D02 ainda bloqueada; nenhum material CANÔNICO/FECHADO ou APROVADO/CONGELADO foi alterado.

### D01 — Readback e resultado técnico remoto (2026-11-12)

- **Publicação estrutural inicial:** commit `8a9e2225be6b94f82f7bc636981c45d4d5d254a9`, pai `5a88739f1ca4c6758697aa597e4e591f298262d6`, GitHub Actions `43264183220`/job `131343188345`, `completed/success`: 79 testes existentes + 11 D01 = **90/90**. Verificador retornou `D01_STRUCTURE_VERIFIED_EDITORIAL_PENDING`, com 1029/1029 entradas master, 923 blobs de candidata, 193 registros externos, 19 mídias, 77 pins (com repetições).
- **Incremento de risco C45:** commit `efa80f3f85e2cb0c8974a10457f13e183a27beda`, pai `8a9e2225be6b94f82f7bc636981c45d4d5d254a9`; GitHub Actions `43264824193`/job `131345478525`, `completed/success`: C01 13, C02 19, C04 15, C06 13, C05 9, C07 10, D01 **12/12**; total **91/91**, zero falhas. A saída agregada do verificador fixou `cycle_pins=77`, `cycle_unique_pinned_paths=73`, `cycle_pins_missing_candidate=53`, `cycle_pins_same_candidate=20`, `editorial_approval=NOT_PROVEN`.
- **Leitura de confirmação:** blobs das implementações e do inventário deverão ser confrontados com a árvore do commit publicado; este checkpoint não é um teste novo de CI nem recategoriza resultados históricos. A diferença `master`/candidata segue real e o snapshot master permanece imutável como referência; nenhuma alteração foi enviada ao master.
- **GATE:** `D01_IN_PROGRESS`; cobertura de objetos Git e registros de origem está tecnicamente verificada, mas owner/destino definitivo, status editorial, conhecimento por campo, direitos de mídia, importações e conflitos permanecem pendentes. Próxima unidade elegível: **D01 — reconciliar inicialmente os 53 pins únicos de C45 sem caminho equivalente, depois completar a matriz de autoridade para as 1029 origens e 193 registros externos**. D02/E02 não liberadas.

### D01 — Leitura estrutural de 53/53 fontes operacionais C45 ausentes (2026-11-12; CI pendente)

- **Referência imutável:** `master@c9fcfc0c558cd17d58ec8c8272da3ed70182ff37`, somente leitura; candidata de base `design@f3e84585a9d4761370de6631552a49382dc5e4f6`. A inspeção pelo GitHub Fetch ocorreu em cinco lotes; 53 arquivos de `master` foram abertos por caminho exato e cada SHA do conteúdo foi conferido com a árvore de origem. Também se verificou que nenhum dos 53 SHAs aparece no conjunto completo de blobs da candidata com outro nome.
- **Ampliação do artefato único D01:** `sistema/arquitetura/fase-d/inventario-origens.json` contém, em cada um desses 53 registros, formato, extensão, total de unidades de código UTF-16, chaves top-level JSON, metadados de classificação/status declarados na fonte e contagem de títulos de Markdown, sem reproduzir texto ficcional ou detalhes ocultos em relatórios PLAYER_SAFE. Abrange **29 JSON, 14 Markdown, 4 Python, 4 JavaScript e 2 texto**.
- **Triagem de ownership proposta, não aprovada:** 28 fontes locais de `cronicas/CHR-001`, 15 contratos gerais em `sistema/narrativa`, oito validadores/testes em `scripts` e dois casos de divisão de responsabilidade (personagem/estado; bootstrap/instância). Diferencia fios abertos de conhecimento dos NPCs e separa segredos da trama de registros públicos. Isso é roteamento para revisão, **não** juízo editorial por campo.
- **Prova automatizada preparada:** `scripts/verificar-inventario-d01.mjs` passa a reler os 53 conteúdos do commit master via `git show` e comparar exatamente a estrutura publicada, além da cobertura e dos pins já verificados. Impede destino legado, aprovação presumida, omissão de inspeção e troca de destino entre fios/conhecimento. `scripts/testar-inventario-d01.test.mjs` adiciona seis testes adversariais; o workflow existente permanece a superfície de CI Web/GitHub, sem teste equivalente no Codex.
- **Limite de significado:** o conteúdo foi inspecionado apenas para metadados estruturais. `editorial_review=PENDING`, `epistemic_and_visibility_review=PENDING`, `content_equivalence_to_target=NOT_PROVEN`, `target_materialized_in_candidate=false`. A próxima parte de D01 deve conciliar semântica e autoridade por fonte, incluindo todas as demais entradas Git e externas; D02 **NÃO** foi iniciada. Não há alteração de material fechado, cânone, cenas, `master` ou runtime.

### D01 — Falha de teste novo e remediação localizada (2026-11-12; rerun pendente)

- Primeiro CI da leitura estrutural: Actions `43273777415`/job `131376653294`, **FAIL**. O verificador de inventário e leitura dos 53 conteúdos concluiu `success`; C01/C02/C04/C06/C05/C07 passaram. D01 teve `17/18`: o teste adversarial sobre `OPEN_THREADS` buscava a primeira ocorrência histórica no inventário (sem metadados C45), provocando `TypeError` antes de chamar o validador. Falha de **seleção da fixture**, não aprovação da prova integral nem evidência de perda de fonte. Registro histórico não foi reescrito.
- Correção proposta no próprio teste: selecionar a ocorrência com `c45_content_reconciliation` antes de aplicar mutação; somar dois negativos de ownership (conhecimento local separado de fios; pacote GM restrito fora do estado público). **20 casos** D01 previstos para nova execução real.
- O gate permanece `D01_IN_PROGRESS` até novo CI bem-sucedido, readback e reconciliação editorial. Nenhuma alteração em conteúdo de `master`, fontes operacionais ou material CANÔNICO/FECHADO.

### D01 — CI final do incremento de triagem e decisão (2026-11-12)

- **Rerun real concluído:** Actions `43274055416`, job `131377633252`, HEAD `9e5cf67f5f7eff217ff3ccc93ee5788bad543181`, estado `completed/success`. Blocos de teste C01 13/13, C02 19/19, C04 15/15, C06 13/13, C05 9/9, C07 10/10 e D01 **20/20**; total **99/99**, zero falhas. O CI executou `git show` de todos os 53 pins operacionais ausentes, conferiu chaves/status/formato contra o inventário e executou adversariais de owner/sigilo. A falha histórica `43273777415` (fixture histórica incorreta) permanece documentada, não apagada.
- **Resultado técnico verificado:** `D01_STRUCTURE_VERIFIED_EDITORIAL_PENDING`: 1029 blobs no snapshot master, 923 no snapshot candidato original, 839 hashes iguais no mesmo path, 1 path divergente, 189 entradas master sem mesmo path candidato, 83 entradas exclusivas candidatas; C45 com 77 referências / 73 caminhos únicos, dos quais 53 sem caminho candidato e 53/53 inspecionados por estrutura. Fontes externas: 193 registros históricos com descoberta `PARTIAL`; 19 ativos de mídia, cinco originais pendentes e 19 SHA externos não conferidos.
- **Marcadores de sigilo:** dos 53, 36 não apresentam declaração top-level de `classification`, `visibility` ou `spoiler_class`; cinco possuem marcador de classificação apenas no nome sem declaração top-level. **Nenhuma dessas ausências é prova de conteúdo público**. Escopo real, conhecimento de ator e possíveis referências na prosa ainda exigem revisão contextual.
- **Gate:** `D01_IN_PROGRESS`, com incremento de integridade aprovado no escopo técnico testado; **D02–D07 não iniciadas** por esta prova e E/cutover sem autorização. Próxima unidade: conciliação substantiva e destino final por fonte/owner (primeiro conjunto C45), além dos 136 paths master ausentes mas não pinados pelo ciclo, 839 objetos compartilhados e 1 divergente, fontes externas e conflitos. As versões históricas e o conteúdo CANÔNICO/FECHADO não foram editados.
