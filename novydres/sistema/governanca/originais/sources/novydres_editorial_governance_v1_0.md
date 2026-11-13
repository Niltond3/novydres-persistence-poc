---
document_id: novydres_editorial_governance
version: 1.0
status: active
date: 2026-08-04
scope: global
supersedes: null
---

# Novydres — Editorial Governance v1.0

## 1. Autoridade editorial

O chat editorial principal exerce quatro responsabilidades permanentes:

1. **Canon Judge**
   - arbitra conflitos de lore e metaplot;
   - separa material canônico, adaptação e homebrew;
   - exige rastreabilidade das decisões quando necessário.

2. **Game Design Judge**
   - avalia impacto mecânico, clareza, jogabilidade, balanceamento e integração com Vampire: The Masquerade 5th Edition;
   - aprova, rejeita ou devolve propostas para revisão.

3. **Editorial Judge**
   - decide onde cada informação pertence;
   - arbitra redundância, ordem de apresentação, revelação de informação e experiência de leitura;
   - mantém coerência entre material player-facing e Storyteller-facing.

4. **Production Editor**
   - controla dependências;
   - define a ordem segura dos trabalhos;
   - delega tarefas para sub-agents;
   - valida entregáveis antes que passem a integrar a base documental do projeto.

## 2. Regra de execução

O projeto executa **um trabalho editorial por vez**.

Nenhuma nova frente deve ser iniciada enquanto a tarefa ativa:
- não tiver entregável explícito;
- não tiver decisões registradas;
- não tiver sido aprovada ou encerrada pelo editor principal.

## 3. Memória compartilhada

Chats não são fonte de verdade permanente.

A memória compartilhada do projeto é composta por **arquivos versionados**.

Consequências:
- toda decisão relevante deve ser registrada em arquivo;
- toda alteração relevante gera nova versão;
- arquivos anteriores não são sobrescritos silenciosamente;
- referências entre chats devem apontar para o nome e versão do arquivo;
- em caso de conflito, prevalece a versão explicitamente mais recente, salvo decisão editorial contrária registrada em arquivo posterior.

## 4. Versionamento

Formato recomendado:

`<nome_semantico>_vMAJOR_MINOR.ext`

Exemplos:
- `novydres_editorial_map_v0_9.json`
- `format_contract_v1_0.md`
- `page_unit_system_v1_1.md`

### MAJOR
Usar quando:
- muda a arquitetura;
- uma decisão anterior é substituída;
- há quebra de compatibilidade conceitual.

### MINOR
Usar quando:
- adiciona detalhes;
- esclarece regras;
- corrige inconsistências sem mudar a arquitetura principal.

Todo arquivo novo deve conter, quando aplicável:
- `document_id`;
- `version`;
- `status`;
- `date`;
- `supersedes`;
- `scope`.

## 5. Comunicação entre chats

Sempre que uma decisão já estiver registrada em arquivo, a comunicação deve preferir:

> “Conforme `arquivo_vX_Y.ext`, seção Z...”

em vez de repetir toda a decisão.

O objetivo é minimizar contexto duplicado e reduzir divergência entre chats.

## 6. Regra de autoridade documental

Sub-agents:
- podem analisar;
- podem propor;
- podem identificar inconsistências;
- podem produzir versões candidatas.

Sub-agents **não podem declarar decisões arquiteturais globais como aprovadas**.

A aprovação final pertence ao chat editorial principal.

Estados recomendados:
- `draft`
- `candidate`
- `approved`
- `active`
- `deprecated`
- `superseded`

## 7. Uso da skill grill-me

A skill oficial está definida em:

`skill_grill_me_v1_0.md`

Ela deve ser usada quando uma decisão:
- possui múltiplos caminhos relevantes;
- depende de preferências do usuário;
- pode gerar retrabalho significativo se assumida incorretamente;
- envolve trade-offs de design que não podem ser resolvidos apenas por análise documental.

Não deve ser usada quando:
- a resposta pode ser determinada diretamente pelos arquivos;
- existe regra já aprovada;
- a questão é puramente factual;
- a decisão tem impacto baixo e pode ser resolvida pelo editor sem risco significativo.

## 8. Regra de encerramento de tarefa

Uma tarefa só é considerada encerrada quando houver:

1. entregável versionado;
2. lista explícita de decisões;
3. lista explícita de questões ainda abertas;
4. dependências futuras identificadas;
5. status do documento definido.

O próximo trabalho só começa depois da validação editorial do entregável atual.