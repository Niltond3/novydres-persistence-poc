---
subject_id: architecture-adr001-implementation-plan
status: MODELO_DE_INICIO_NAO_EXECUTADO
visibility: PLAYER_SAFE
---
# Prompt de início — ChatGPT Web

Texto para o jogador copiar em um novo chat com a conexão GitHub disponível. A autorização de execução contida no prompt passa a valer quando o jogador o enviar; salvar ou publicar este modelo não inicia A01 nem autoriza cutover. O HEAD exato deve ser recuperado na abertura, sem pin circular ao próprio commit deste arquivo.

```text
Retome NOVYDRES no repositório https://github.com/Niltond3/novydres-persistence-poc, branch `design/subject-oriented-migration`.

Autorizo iniciar a execução do plano integral do ADR-001, começando por A01 e avançando nas tarefas elegíveis de A–D conforme suas dependências e critérios comprovados. Essa autorização inclui alterações, commits e publicação na branch candidata; não inclui cutover em master, ativação do novo runtime ou cenas. E01 deve preparar uma entrega concreta para minha aprovação expressa antes de E02.

Leia nesta ordem, recuperando os arquivos reais da branch:
1. Instruções de agentes aplicáveis e entradas de autoridade pertinentes. Distinga contratos operacionais antigos do desenho sucessor, sem ativar este último antecipadamente.
2. `novydres/sistema/arquitetura/adr/001-subject-oriented.md`, especialmente §§11–12 e DEC-01–DEC-26.
3. `novydres/sistema/arquitetura/plano-integral/index.md`, `tarefas.md` e `cobertura.md`.
4. Os documentos especializados de `fase-a/` e as evidências de `fase-b/` necessárias à tarefa atual. Use `simplificacao-narrativa/` para contexto e impactos.

Antes de editar, confirme repositório, branch, HEAD e capacidades reais da conexão: leitura por ref/SHA, escrita na branch, publicação, readback e acesso aos resultados de CI quando exigidos. Não presuma shell, API, escrita ou CI disponíveis. Se uma capacidade faltar, registre o bloqueio específico e prossiga apenas no trabalho independente possível; entregue eventual proposta/diff sem alegar persistência ou conclusão inexistentes. Não exponha credenciais.

Comece A01 reconciliando o HEAD de design, o master atual e as fontes exigidas pela tarefa. Os SHAs nos documentos são snapshots históricos; não combine seus estados nem faça merge indiscriminado. A aprovação original de A é apenas de desenho; B permanece `B_REMEDIATION_REQUIRED`, não concluída por este planejamento. Os testes antigos não comprovam as alterações novas.

As decisões da entrevista precedem o ADR original. Aplique-as diretamente, sem reabrir Q-01–Q-08 ou pedir confirmação apenas por tarefa/fase. Simplifique limites excessivos já resolvidos por essas decisões. Se surgir escolha substantiva nova, consulte primeiro as fontes e então faça uma pergunta por vez, no output normal, usando Grill with Docs se disponível; recomende uma opção e explique sua consequência. Não crie burocracia ou componentes sem função necessária.

Execute o escopo e os critérios de cada tarefa, preservando trabalho alheio, fatos jogados, fontes, cânone fechado e distinções de conhecimento. Preparação não é acontecimento. Não narre, role dados, avance CHR-001 ou altere recursos do personagem.

Registre progresso curto sob o ID no backlog existente: estado, snapshot, saídas, evidências reais, limitações e próxima tarefa elegível. Confirme a publicação por leitura do commit/arquivos; autorrelato PASS não é prova externa. Não crie arquivo por teste nem reexecute verificações idênticas sem motivo.

A continuidade no mesmo chat depende dos controles de DEC-25 ainda por comprovar no Web. Preserve checkpoints desde A; não considere essa condição satisfeita por seguir este prompt. Conforme DEC-26, recupere divergências pelas fontes e retome quando resolvidas; se não recuperar uma base confiável, pause a unidade afetada e entregue handoff para outro chat. Sem promessa de detecção universal ou execução ilimitada.

Inicie agora pela verificação de acesso e A01. Informe brevemente o que foi confirmado e faça o trabalho possível, sem parar apenas para apresentar um plano.
```
