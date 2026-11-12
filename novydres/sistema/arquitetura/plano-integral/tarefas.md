---
subject_id: architecture-adr001-implementation-plan
status: EXECUCAO_EM_CURSO_A01_A03_A05_PASS_A04_NEXT
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

### A05 — Especificar contratos reais de leitura e escrita Codex/Web

- **Depende de:** A01; A02/A03 para fechar o contrato.
- **Escopo/saída:** revisar `fase-a/git-e-roteadores.md`: descoberta das três entradas, lookup exato por ID, leitura por snapshot, catálogo gerado e hash sem circularidade, invalidação de cache, CAS, parent esperado, readback e erros. Conferir capacidades e limites das ferramentas disponíveis sem efetuar mutações nesta etapa documental. Não presumir shell ou API no Web. Especificar DEC-25 no contrato existente: entrada/checkpoint por commit, fontes decisivas, recuperação de divergência e evidência externa de conclusão. Verificar ações reais de leitura, escrita e acompanhamento de CI, sem assumir equivalência entre o ambiente Codex e o Web.
- **Conclusão:** contratos de entrada/saída, erro e retomada equivalentes nos dois canais, NOT_FOUND explícito, sem fallback fuzzy ou overwrite silencioso. Capacidade de proteção de refs, CI e sandbox classificada como comprovada ou pendência concreta; limitações não viram garantias. O contrato distingue sinal objetivo de erro de comparação semântica assistida; aplicar DEC-26 à recuperação, ao risco residual e à renovação excepcional, sem dispensar a prova de DEC-25.


#### Execução de A05 — 2026-11-12

- **Estado:** PASS de contrato de interfaces e levantamento de capacidade; **não** comprova controle DEC-25 nem equivalência Codex/Web. **Entrada:** `0298e4837bf9a304857837c5639b2c74fc5a729b`.
- **Saída:** [git-e-roteadores.md](../fase-a/git-e-roteadores.md#a05--contratos-webcodex-e-continuidade-com-prova-de-capacidade-2026-11-12) define `resolve/read_selected/commit_transaction/resume`, saídas, diagnósticos, recuperação, autoria, fallback proibido e checkpoints.
- **Evidências:** Web GitHub fetch por ref, blobs, comparação, criação de tree/commit, atualização com `expected_sha` e readback A01–A03 reais. API de consulta CI existe, mas em `0298e48` retornou **0 runs, 0 check-runs, 0 statuses**. Sem shell/Codex executado; stale/ref remota e falha de confirmação ainda não provocadas em sandbox. Tokens/bytes Web `NOT_OBSERVABLE` (DEC-19).
- **Próximo:** A04 pendente; A06 requer A04 e A02/A03/A05. DEC-25 depende B/C e DEC-26 mantém parada/renovação excepcional.

### A06 — Fechar critérios, gabaritos e fronteira B/C

- **Depende de:** A02–A05; aplicar Q-03/Q-04 já aceitas (DEC-19/DEC-21).
- **Escopo/saída:** revisar `fase-a/validacao-e-metricas.md` e contratos de B: casos com IDs, fontes, gabarito separado, bindings executáveis, isolamento, observabilidade, comparação antes/depois e revisão editorial independente. Definir quais ferramentas mínimas permitem provar B sem antecipar C. Aplicar DEC-21: dimensionar a suíte por riscos, preservando casos críticos e falhas históricas. Mapear funções/casos/provas, rotas reais dos dois canais e amostragem de comportamento variável, concorrência e falhas; justificar seleção, reutilização e repetições, sem quotas de 30/12/12 ou três rodadas obrigatórias. Não usar volume nem uma única resposta correta como prova de confiabilidade. Aplicar NOT_OBSERVABLE somente aos contadores Web abrangidos por DEC-19. Incorporar os casos DEC-25 de fonte inexistente/insuficiente, decisão superada, falsa conclusão, checkpoint divergente e recuperação no mesmo chat; reutilizar casos pertinentes e declarar limites de detecção, sem novo programa ou quota de testes.
- **Conclusão:** cada critério possui prova, responsável e reprovação definidos. Preservar a classificação crítico/não crítico e a precisão exigida: críticos sem divergência; não críticos ao menos equivalentes à baseline comparável, sem false CONFIRMED. A quota e a contagem histórica de 30/30 não são critério futuro; falhas factuais conhecidas continuam exigindo correção e nova evidência, sem apagamento ou reclassificação oportunista. Ausência de telemetria/teste não equivale a PASS; qualidade de escrita não se mede por palavras-chave. Matriz de cobertura completa, incluindo controles DEC-25 com executor/resultado externo e comparação contextual; não tratar autorrelato PASS como comprovação.

### A07 — Revisar a emenda e registrar decisão de desenho

- **Depende de:** A01–A06.
- **Escopo/saída:** diff consolidado revisável, decisões da entrevista e impacto sobre A/B; registrar a consolidação das escolhas já aceitas e obter decisão somente sobre questões residuais, sem substituir a aprovação histórica. Distinguir aprovação de desenho, de sucessores operacionais e de cutover. Aplicar DEC-22 ao regime futuro de transições A–D, sem confundir essa escolha documental com autorização de execução atual. Aplicar DEC-25 e DEC-26 já aceitas, mantendo a condição de prova Web antes de dispensar a troca por fase e a pausa/renovação excepcional quando a recuperação falhar.
- **Conclusão:** escolhas aceitas incorporadas sem pedido repetido de aceitação; nenhum trade-off bloqueante escondido em tarefa técnica; baseline e critérios aceitos para retomar B. Somente decisão substantiva realmente pendente mantém PENDING_APPROVAL para o escopo afetado. Critério técnico incompleto exige remediação; não pedir confirmação apenas para iniciar a próxima fase já autorizada no plano.

## B — Remediar e comprovar o protótipo isolado

### B01 — Reconciliar os quatro casos e seus mapas

- **Depende de:** A07 e mandato pertinente de B.
- **Escopo/saída:** revalidar fontes atuais e os candidatos existentes: um NPC (identidade global e contexto local), uma trama, uma história e um estado. Ajustar ao modelo/contrato revisados com mapa campo a campo, fontes pinadas, relações e UNKNOWN preservados. Exercícios narrativos adicionais são fixtures fictícias, não expansão da migração.
- **Conclusão:** 100% dos campos dos casos têm equivalência ou transformação justificada; nenhuma cópia vira autoridade operacional. Texto histórico não vira ledger auditado, segredo não vaza e master não muda.

### B02 — Reexecutar recuperação Codex com prova por caso

- **Depende de:** B01 e contratos executáveis de A06.
- **Escopo/saída:** corrigir causas das falhas registradas, inclusive Q29/Q30, e executar no canal Codex os casos comparáveis de recuperação definidos em A06, com repetição justificada conforme DEC-21, baseline/candidato com contexto controlado. Guardar pergunta, resposta, fonte/trecho localizado, leitura e métrica observável por operação; não fornecer o gabarito ao executor.
- **Conclusão:** precisão, referências, recursos e conhecimento atendem os critérios acordados. Agregados antigos 51/90 ou citações sem localização não substituem evidência individual; resultados ausentes permanecem não executados.

### B03 — Executar recuperação real no ChatGPT Web

- **Depende de:** B01 e A05/A06; Q-03 aceita como DEC-19.
- **Escopo/saída:** casos comparáveis de recuperação definidos em A06, com amostragem justificada conforme DEC-21, por ferramenta realmente disponível no Web, com snapshot, consultas, respostas e fontes verificáveis. Preservar isolamento do gabarito e registrar métricas expostas; aplicar a exceção estrita DEC-19 de observabilidade, sem dispensar operações nem fontes.
- **Conclusão:** revisão independente consegue conferir os resultados por caso. Autorrelato de execução ou um run Codex não é evidência Web; limitação de acesso é pendência, não simulação aprovada. Demonstrar a sequência DEC-25 na rota Web: recuperar tarefa/fontes, detectar divergência observável e retomar no mesmo chat a partir de checkpoint/evidência verificáveis.

### B04 — Executar negativos, mutações e concorrência no sandbox

- **Depende de:** B01 e A05/A06.
- **Escopo/saída:** materializar os casos negativos e jornadas que cobrem os riscos definidos em A06, reutilizando fixtures pertinentes com dados/IDs reais e substituindo placeholders. Executar nas rotas reais aplicáveis; repetir conforme variabilidade, concorrência e falhas, sem quotas fixas (DEC-21). Provar autoria, episteme, sigilo, recursos, idempotência, correção, stale SHA e falha parcial. Corrida remota usa ref descartável autorizada, nunca master nem campanha.
- **Conclusão:** operações realmente executadas têm entrada, tentativa, rejeição/resultado, SHA e readback; controles negativos deixam o alvo inalterado. CAS local não prova CAS remoto; atualização remota sem disputa não prova rejeição stale. Executor mínimo de B permanece limitado aos testes, sem ativar ferramentas finais. Exercitar a recuperação DEC-25 e a detecção de conclusão sem prova; documentar também erros semânticos não detectados, sem anunciá-los como impossíveis.

### B05 — Consolidar gate B com evidência atual

- **Depende de:** B02–B04.
- **Escopo/saída:** comparar baseline, equivalência, precisão, custo/latência observáveis e resultados negativos; obter a execução CI aplicável às verificações do protótipo com run ID e commit. Revisar exceções aprovadas, relações fora do escopo e diffs de master.
- **Conclusão:** todos os requisitos de B comprovados ou B continua em remediação. Evidência de CI não executada, métricas inventadas e casos faltantes impedem PASS. No plano futuramente autorizado, PASS comprovado libera C conforme DEC-22, sem nova confirmação apenas pela fase; não há promoção operacional.

## C — Construir e verificar as ferramentas finais

### C01 — Implementar schemas e validações de informação

- **Depende de:** B05 PASS, entrada pertinente de C e A02.
- **Escopo/saída:** schemas especializados e validações V01–V04 para tipos efetivamente usados, IDs, relações, owner, tempo, episteme, proveniência e conhecimento. Reutilizar código adequado existente; não criar campos/arquivos sem função demonstrada. Retirar dos schemas antigos exigências de ledger universal, replay e registros/faces por rolagem (DEC-23/DEC-24).
- **Conclusão:** fixtures válidas passam; conflitos de dono, fontes inválidas, ID ambíguo e promoção indevida falham com diagnóstico acionável. Texto livre preserva seus bytes e não é convertido em estrutura inventada.

### C02 — Implementar catálogo e recuperação por assunto

- **Depende de:** C01 e A05.
- **Escopo/saída:** geração determinística, lookup por ID e leitura seletiva em Codex/Web, índices/relacionamentos derivados, hashes sem autorreferência e cache por snapshot. As três entradas finais localizam o contrato; README não vira quarto bootstrap.
- **Conclusão:** mesmos inputs geram mesmos bytes; alterações invalidam o que precisam invalidar, todos os destinos resolvem e NOT_FOUND não consulta rota antiga. V03/V09 comprovados nas duas rotas.

### C03 — Implementar gravação atômica e histórico preservado

- **Depende de:** C01/C02 e A03/A05.
- **Escopo/saída:** transação dos donos afetados, texto histórico preservado, correção explícita, identidade mínima de transação, idempotência, expected SHA/parent, proteção de ref e readback. Estado corrente é editável com revisão; não exigir registro próprio por evento/rolagem ou certificado RNG. Exercitar stale update, repetição de ID, concorrência, blob corrompido e interrupções em sandbox. A transação da resposta reúne texto/deltas; nenhum texto ficcional é entregue antes do readback.
- **Conclusão:** V05/V10 passam com rejeições comprovadas, sem sobrescrita/perda silenciosa; estado COMMITTED distinto de sincronização parcial. Provar também publicação concluída com confirmação perdida: recuperação encontra a mesma transação, sem duplicar texto, deltas ou consequências e sem rerrolar. Restrições administrativas efetivamente disponíveis conferidas; proteção não comprovada não é anunciada.

### C04 — Implementar estado atual e retomada fiel

- **Depende de:** C03 e A02/A03.
- **Escopo/saída:** estado atual por assunto com dono único, recursos/ficha, última intenção, cursor e conhecimento situado, vinculado às fontes pertinentes. Preservar lacunas históricas e acesso ao texto literal sem repetir toda a crônica na entrada. Conciliar inconsistências pelas fontes; sem exigir reconstrução universal por eventos ou auditoria de rolagens.
- **Conclusão:** V06/V07: consistência e recuperação em contexto renovado mantêm os mesmos saldos, consequências materiais e ponto de retomada, sem rerrolar ou restaurar recursos antigos. Nenhuma prova técnica de RNG é exigida ou inventada. Escrita falha não é apresentada como atualização confirmada. Checkpoint de tarefa/fase suporta continuidade no mesmo chat e handoff quando necessário, sem outro arquivo por verificação.

### C05 — Integrar contrato de mesa e preparação proporcional

- **Depende de:** C02–C04 e A04.
- **Escopo/saída:** ferramentas e entradas aplicam o contrato candidato e as exceções locais, sem validadores/workflows novos por cena. Exercícios de narração isolados cobrem NPCs, concessões, rotina, intenções, prioridades, perdas/ganhos e mistério, conforme matriz IMP-01–IMP-15.
- **Conclusão:** revisão contextual da escrita, separada da integridade mecânica, verifica a função das regras retiradas. Nenhuma fixture cria fatos da campanha; sem quota de dano/recusa ou suposição de que um checklist torna a narrativa boa. Integrar também continuidade das tarefas A–E no Web (DEC-25), sem confundir esse procedimento de implementação com exigências adicionais por cena.

### C06 — Implementar auditoria de fontes e detector de legado

- **Depende de:** C01/C02 e inventário de A01.
- **Escopo/saída:** V08/V11/V12 sobre toda árvore: código, JSON, prosa operacional, URLs, CI, symlinks, aliases, wrappers e fallbacks. Distinguir citação de proveniência de rota executável por regra verificável; conferir localização/direitos de mídia sem inventar hashes.
- **Conclusão:** resíduos operacionais e vazamentos nas fixtures são detectados, sem exclusão genérica de diretórios/documentação. Aprovar candidato isolado não significa que toda branch pré-cutover esteja ZERO LEGADO. Git histórico não vira fallback no HEAD.

### C07 — Integrar CI, dois canais e regressões de produção

- **Depende de:** C01–C06.
- **Escopo/saída:** scripts e workflows finais, contratos Web/Codex equivalentes, suíte crítica, erros de integração, métricas pareadas e revisão independente de sigilo/escrita. Adaptar ou retirar workflows específicos antigos no candidato final; manter as provas necessárias.
- **Conclusão:** runs reais com commit e resultados reproduzíveis em ambos os canais; custo e p95 julgados pelos critérios de A06, exceções expressas. Teste de texto/palavra-chave não substitui cenário narrado nem demonstra ausência de vazamento contextual. Provar os controles DEC-25 com resultados externos recuperáveis no Web e falhas induzidas/recuperação; revisão semântica registra limites e falhas que escapam. Sem evidência real, a condição da dispensa de chat por fase permanece não demonstrada.

### C08 — Revisar e encerrar gate C

- **Depende de:** C07.
- **Escopo/saída:** conferir V01–V12, contratos implementados, regressões, limitações e readback. Relacionar cada requisito à prova, sem declarar equivalência integral ainda não migrada.
- **Conclusão:** C PASS apenas sem lacuna bloqueante, com CI e duas rotas comprovadas; no plano futuramente autorizado, seguir para D conforme DEC-22, sem nova confirmação apenas pela fase. Runtime antigo continua operacional até E.

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
- **Escopo/saída:** CI real no commit promovido, smoke tests de leitura/escrita/retomada nas duas rotas em ambiente seguro, revisão de sigilo e scanner de toda HEAD/dependências controladas. Atualizar matriz com evidência definitiva, documentação corrente e estado final dos gates; manter barreira anti-regressão para commits seguintes.
- **Conclusão:** todos os requisitos do ADR e sucessores aprovados implementados, migração completa, versões via Git, ZERO LEGADO e equivalência comprovados; nenhuma pendência bloqueante transferida a uma futura tarefa. Só então E PASS/ADR IMPLEMENTADO. Se houver falha, programa não encerrado. Isso não autoriza cena nem certifica eficácia narrativa ainda não observada em jogo.

## Registro de execução

Nenhuma tarefa concluída por esta elaboração documental. Registrar futuramente sob o ID correspondente: estado, snapshot, saídas, evidências, limites e decisão de gate quando aplicável. Não criar T31 de “terminar a migração” depois de E03; qualquer descoberta obrigatória deve entrar no escopo e impedir o encerramento até ser resolvida.
