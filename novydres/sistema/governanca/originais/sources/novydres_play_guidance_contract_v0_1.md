---
document_id: novydres_play_guidance_contract
version: 0.1
status: candidate
date: 2026-08-05
scope: gap_arch_002_play_guidance_architecture
target_gap: GAP-ARCH-002
supersedes: null
depends_on:
  - novydres_editorial_governance_v1_0.md
  - skill_grill_me_v1_0.md
  - novydres_gap_registry_v0_2.json
  - novydres_next_gap_decision_v0_1.md
  - novydres_format_contract_v0_2.md
  - novydres_format_contract_v0_2_editorial_review_v0_1.md
  - novydres_standalone_rules_contract_v0_1.md
  - novydres_standalone_rules_editorial_review_v0_1.md
  - novydres_editorial_map_v0_8_step7.json
  - latest_valid_chapters_01_to_06
  - latest_available_dramatis_personae_material
related_decision_log: novydres_play_guidance_decisions_v0_1.md
---

# Novydres — Play Guidance Contract v0.1

## Purpose

Definir a arquitetura editorial de **“Jogando em Novydres”** como a camada que converte conhecimento do cenário em jogo efetivo de Vampire: The Masquerade 5th Edition.

A camada existe para ligar, de forma explícita e operacional:

**cenário → escolhas da mesa → posicionamento de personagens e coterie → criação → preparação do Narrador → pressões e situações → cenas → consequências → continuidade da crônica.**

Ela não existe para resumir o cenário, substituir as regras, armazenar segredos do Narrador ou escrever uma campanha.

## Gap Being Resolved

**GAP-ARCH-002 — Definir a seção/camada “Jogando em Novydres”.**

O gap existe porque o suplemento possui história, geografia, política, instituições, personagens, conflitos e mecânicas suficientes para sustentar jogo, mas não possui ainda uma superfície formalmente responsável por ensinar como esses elementos são combinados para produzir sessões e crônicas.

## Product Role

“Jogando em Novydres” é a **camada operacional de conversão do cenário em jogo**.

Sua responsabilidade autoritativa é responder:

- o que jogadores e coteries fazem em Novydres;
- quais escolhas de posicionamento precisam ser tomadas antes da criação e do início da crônica;
- como essas escolhas alimentam a criação de personagens;
- como o Narrador transforma esses outputs em pressões, relações, situações e consequências;
- como resultados mecânicos e narrativos retornam ao estado da crônica;
- como material de cenário já publicado é usado em jogo sem ser reimplementado.

## Primary Audiences

A camada possui **dupla audiência com responsabilidades distintas**.

### Jogadores / mesa

Precisam compreender:

- a proposta de jogo de Novydres;
- que tipos de decisões de inserção importam;
- como posicionar a coterie na cidade;
- como território, Raions, facções, instituições, poder, obrigações e relações afetam escolhas;
- quais outputs devem chegar à criação de personagem e coterie;
- como reconhecer oportunidades, custos e responsabilidades próprias do domínio.

### Narrador

Precisa compreender:

- como consumir os outputs definidos pela mesa;
- como selecionar pressões relevantes;
- como ativar facções, instituições, NPCs e conflitos;
- como transformar ações em respostas da cidade;
- como circular informação e rumores sem duplicar o capítulo de segredos;
- como manter consequências e estado de crônica entre sessões.

Nenhuma das audiências é secundária para a função do sistema, embora não recebam necessariamente o mesmo conteúdo.

## Editorial Form

A forma aprovada é **híbrida**:

1. **núcleo central identificável “Jogando em Novydres”** — fonte autoritativa do workflow operacional;
2. **interfaces distribuídas** nos capítulos relevantes — pontos de entrada, saída, referência ou aplicação que alimentam ou recebem dados do workflow.

O núcleo não deve ser desmontado em instruções dispersas, e as interfaces distribuídas não devem implementar versões concorrentes do mesmo processo.

## Position in Reading / Use Flow

O núcleo deve ser encontrado **depois do bloco principal de cenário e antes da criação/regras**.

Posição conceitual:

**entender Novydres → aprender a operar Novydres → posicionar a mesa → criar personagens/coterie → consultar/aplicar regras → retornar ao ciclo de jogo.**

Este contrato não fixa número final de capítulo, paginação ou ordem física exata em relação a futuras revisões do mapa editorial.

## Core User Journey

O workflow-base é um ciclo único compartilhado entre as duas audiências:

1. **Compreender a proposta de jogo** — temas, tensões e expectativas da experiência de Novydres.
2. **Posicionar a coterie** — definir inserção local, recém-chegada ou mista e relações relevantes com cidade, território e poder.
3. **Produzir inputs de criação** — registrar vínculos, tensões, interesses, obrigações e contexto que devem informar personagens e coterie.
4. **Executar criação mecânica em sua superfície autoritativa** — rápida ou completa/guiada.
5. **Retornar personagens/coterie ao workflow** — agora com elementos mecânicos e narrativos concretos.
6. **Narrador seleciona pressões** — escolhe quais conflitos, facções, instituições, NPCs e tensões devem responder ao estado criado.
7. **Preparar situações, não roteiros** — estabelecer forças em movimento, objetivos, informação disponível e consequências plausíveis.
8. **Jogar cenas** — aplicar cenário e regras por suas fontes autoritativas.
9. **Atualizar estado** — registrar mudanças em relações, território, Status, Prestações, pressões e demais elementos relevantes.
10. **Reiniciar o ciclo** — o novo estado se torna input para a próxima preparação.

O Narrador não fica limitado às escolhas dos jogadores: ameaças externas, agendas ocultas e forças independentes podem entrar no ciclo quando apropriado.

## Mandatory Information Families

### Player-safe / mesa

O núcleo deve, em implementação futura, cobrir no mínimo:

- proposta, temas e estilo de jogo em Novydres;
- o que uma coterie faz na cidade noite a noite;
- coteries locais, recém-chegadas e mistas como posições de jogo;
- inserção territorial e relação com Raions;
- posição diante da ordem política local;
- relações com facções, instituições e figuras de poder;
- caça e existência cotidiana como contexto de decisão, sem reimplementar regras;
- política, Status e Prestações como fontes de escolhas e consequências;
- Bairrismo e Marco Territorial como elementos de posicionamento quando aplicáveis, sem reproduzir sua implementação mecânica;
- rumores, informação e reputação como recursos de jogo em nível operacional;
- preparação de sessão zero e início de crônica em nível arquitetural;
- outputs que alimentam criação de personagens e coterie.

### Storyteller-facing / operação

O núcleo deve, em implementação futura, cobrir no mínimo:

- ingestão dos outputs produzidos pela mesa;
- seleção e priorização de pressões;
- ativação de conflitos/frentes relevantes;
- combinação de facções, instituições, NPCs e território;
- preparação orientada a situações;
- circulação operacional de rumores e informação;
- reação da cidade às ações da coterie;
- transformação de resultados em consequências persistentes;
- atualização do estado da crônica entre sessões;
- manutenção de múltiplas linhas de pressão sem construir uma campanha pré-escrita.

## Explicit Exclusions

“Jogando em Novydres” não deve:

- reescrever História, Atlas, Facções, Concílio, Fé ou Dramatis Personae;
- reproduzir entradas completas de Raions, instituições, facções ou NPCs;
- armazenar ou revelar sistematicamente Segredos do Narrador;
- resolver a arquitetura global player-facing versus Storyteller-facing;
- reproduzir regras completas de V5;
- criar versões simplificadas concorrentes de regras existentes;
- escrever o Capítulo 10;
- redesenhar mecânicas V5;
- fechar catálogos de opções;
- definir inventário oficial/homebrew;
- escrever campanhas, aventuras, atos, cenas, vilões, finais ou mini-crônicas;
- definir a sequência final de seções, textos finais, paginação ou word count;
- criar uma nova taxonomia completa de DEUs;
- implementar a futura criação guiada/jogada.

## Player-Safe Responsibilities

A superfície player-safe é responsável por **escolhas e expectativas**, não por revelar o backstage da crônica.

Ela deve permitir que jogadores tomem decisões significativas sobre:

- quem são na cidade;
- a quem devem algo;
- onde estão inseridos;
- o que desejam proteger, explorar ou conquistar;
- quais forças da cidade importam para sua coterie;
- quais tensões devem informar personagens e história compartilhada.

Informação necessária para essas escolhas deve vir das fontes player-safe autoritativas ou de síntese operacional mínima.

## Storyteller Responsibilities

A superfície do Narrador é responsável por **operação**, não por funcionar como repositório de segredos.

Ela ensina como:

- interpretar os outputs da mesa;
- selecionar material existente;
- montar pressões e situações;
- decidir quais forças reagem;
- transformar consequências em novo estado de jogo;
- consultar segredos quando necessário em seus lares autoritativos.

Ela pode referenciar material Storyteller-only, mas não assume sua propriedade editorial.

## Relationship with Setting Chapters

Capítulos de cenário permanecem fontes autoritativas sobre **o que Novydres é**.

“Jogando em Novydres” é fonte autoritativa sobre **como combinar esses elementos para produzir jogo**.

Regra de interação:

- cenário fornece fatos, entidades, relações, tensões e contexto;
- play guidance seleciona e encadeia esses elementos em workflows;
- quando precisar repetir contexto, usa apenas o mínimo operacional necessário;
- a referência completa retorna ao capítulo autoritativo.

Interfaces distribuídas podem indicar que determinado elemento produz um input para “Jogando em Novydres”, mas não devem recriar o workflow completo.

## Relationship with Character Creation

A criação de personagens já possui duas rotas compatíveis:

- **criação rápida**;
- **criação completa/guiada**.

“Jogando em Novydres” deve existir **antes da execução mecânica da criação** como fonte de inputs de posicionamento.

Inputs candidatos incluem, sem fixar ainda o formulário final:

- inserção local, recém-chegada ou mista;
- relação principal com território/Raion;
- posição frente à ordem política;
- vínculos ou tensões com facções/instituições;
- interesses, obrigações ou pressões relevantes;
- elementos de identidade compartilhada da coterie.

A superfície de criação permanece autoridade sobre todos os passos, opções e consequências mecânicas.

### Future complete/guided creation

O projeto deve preservar compatibilidade com uma futura proposta de **“criação jogada”** para o modo completo/guiado.

Essa futura experiência poderá construir não apenas ficha, mas também história/lore pessoal do personagem, vínculos, memória e história compartilhada da coterie.

O sistema de **Vampiro de Mil Anos / Thousand Year Old Vampire** foi registrado como **referência candidata de design**, não como solução aprovada ou adaptação fechada.

A arquitetura, workflow, adaptação, limites e integração mecânica dessa criação jogada exigem **grill e subagent próprios** quando esse trabalho for efetivamente aberto.

GAP-ARCH-002 apenas exige que nenhuma decisão presente inviabilize essa direção futura.

## Relationship with Standalone Rules

A fronteira é:

**regras respondem “como resolver mecanicamente”; Jogando em Novydres responde “quando isso entra no ciclo e o que fazer com o resultado”.**

Quando um workflow depende de uma regra, play guidance pode explicar:

- quando ela é acionada;
- por que importa naquele ponto;
- quais inputs ela recebe;
- quais outputs retornam ao ciclo;
- onde está a implementação autoritativa.

Não deve reproduzir a regra completa nem criar uma implementação resumida concorrente.

O modelo de fonte autoritativa única e superfícies derivadas do standalone-rules contract permanece vinculante.

## Relationship with Dramatis Personae

Dramatis Personae permanece autoridade sobre identidade, apresentação, relações, estatísticas e camadas de informação de personagens.

“Jogando em Novydres” usa NPCs como **peças operacionais do estado da cidade**:

- quem é ativado por uma escolha;
- quem reage a uma mudança;
- quem fornece pressão, informação, acesso ou oposição;
- quais relações existentes devem entrar em foco.

Não deve reproduzir perfis, fichas ou segredos completos.

## Relationship with DEUs

A arquitetura admite **DEUs derivadas apenas quando um workflow estável possui utilidade repetida à mesa**.

Princípio:

**núcleo = ensina e contextualiza; DEU = acelera execução já compreendida.**

Candidatos futuros podem incluir:

- orientação de sessão zero / posicionamento da coterie;
- resumo de outputs que alimentam criação;
- referência de preparação do Narrador;
- ciclo pressão → resposta → consequência.

Esses são candidatos funcionais, não novos tipos aprovados.

Quando uma família DEU existente já cobre a necessidade — por exemplo Raion — ela deve ser reutilizada em vez de criar superfície concorrente.

A criação de qualquer nova família formal exige decisão posterior própria.

As regras existentes de segurança física das DEUs permanecem intactas.

## Relationship with Campaign / Adventures

“Jogando em Novydres” deve estabelecer uma **interface editorial explícita** para campanhas e aventuras futuras.

Uma aventura poderá consumir outputs como:

- coterie posicionada;
- vínculos territoriais e sociais;
- relações/tensões com facções e instituições;
- NPCs ou fontes de informação já relevantes;
- estado corrente de pressões e consequências;
- procedimento estabelecido de reação da cidade.

A aventura é responsável por acrescentar conteúdo específico:

- situação;
- ameaças;
- objetivos;
- acontecimentos;
- cenas;
- antagonistas particulares;
- desenvolvimentos e possíveis desfechos.

Uma aventura pode sobrescrever inputs do workflow quando sua premissa exigir, desde que a substituição seja explícita.

“Jogando em Novydres” não contém premissas prontas, arcos, campanhas ou one-shots.

## Duplication and Cross-Reference Rules

1. Cada fato ou regra possui um lar autoritativo.
2. “Jogando em Novydres” pode sintetizar somente o mínimo necessário para manter o workflow legível.
3. Síntese operacional não pode se tornar segunda implementação completa.
4. Cross-references devem apontar para a autoridade original quando compreensão ou resolução completa for necessária.
5. Interfaces distribuídas podem produzir ou receber inputs, mas não duplicar o núcleo operacional.
6. DEUs são derivadas, não fontes concorrentes.
7. Storyteller Secrets permanecem fora da propriedade desta camada.

## Authoritative Information Ownership

### Autoridade de “Jogando em Novydres”

- workflow de conversão cenário → escolha → preparação → situação → consequência → continuidade;
- definição dos inputs/outputs entre mesa, criação, regras e Narrador;
- princípios de posicionamento da coterie;
- procedimentos editoriais de seleção e combinação de material em jogo;
- interface genérica com campanhas e aventuras.

### Não é autoridade sobre

- lore e fatos do cenário;
- estatísticas e perfis de NPCs;
- mecânicas V5 ou locais;
- catálogos de criação;
- segredos e verdade oculta;
- conteúdo específico de campanha/aventura;
- contratos globais de revelação.

## Entry / Exit Points

### Entrada principal

O leitor chega ao núcleo após ter recebido contexto suficiente do cenário principal para compreender cidade, poderes e tensões.

### Saída para criação

A mesa produz outputs de posicionamento que devem poder ser consumidos tanto pela criação rápida quanto pela criação completa/guiada.

### Retorno da criação

Personagens e coterie completos retornam com novos dados mecânicos e narrativos.

### Saída para preparação

O Narrador converte o estado atual em pressões e situações.

### Saída para regras

Quando resolução mecânica é necessária, o workflow aponta para a fonte autoritativa e recebe de volta o resultado.

### Saída para campanha/aventura

Materiais futuros podem consumir o estado produzido pelo workflow sem reensinar sua infraestrutura.

### Loop de continuidade

Consequências atualizam o estado e retornam como input para a próxima sessão.

## Dependencies

Dependências vinculantes:

- governança editorial e autoridade do chat principal;
- format contract v0.2 para arquitetura chapter-first, DEUs e segurança física;
- standalone rules contract para criação, regras e propriedade autoritativa;
- capítulos de cenário como fontes autoritativas de seus domínios;
- Dramatis Personae como fonte de NPCs;
- futuro GAP-ARCH-003 para arquitetura global de revelação;
- futuros trabalhos de criação para implementação detalhada das duas rotas;
- futuros gaps de campanha/aventura para conteúdo específico.

## Deferred Questions

Devem permanecer explicitamente abertos:

- número e posição final do capítulo no mapa editorial revisado;
- sequência exata de seções;
- redação final;
- perguntas concretas de sessão zero;
- formulário exato dos outputs de posicionamento;
- procedimento detalhado de preparação do Narrador;
- formato final de ferramentas de estado/pressão;
- contratos de novas famílias DEU, se necessárias;
- arquitetura global player-facing versus Storyteller-facing (GAP-ARCH-003);
- implementação da criação rápida;
- design da criação completa/guiada;
- design e validação da possível “criação jogada” inspirada em Vampiro de Mil Anos;
- adaptação mecânica/metodológica dessa referência;
- coterie-creation mechanical scope ainda deferido pelo standalone-rules review;
- escrita do Capítulo 10;
- campanhas e aventuras;
- paginação final e produção.

## Approved Decisions

- PG-001 — Função primária: camada operacional de conversão.
- PG-002 — Dupla audiência com responsabilidades distintas.
- PG-003 — Um workflow compartilhado; escolhas player-safe alimentam preparação do Narrador.
- PG-004 — Arquitetura híbrida: núcleo próprio + interfaces distribuídas.
- PG-005 — Núcleo após cenário principal e antes de criação/regras.
- PG-006 — Duas superfícies funcionais complementares; Storyteller-facing não é repositório de segredos.
- PG-007 — Ciclo completo de jogo em nível procedural, não enciclopédico.
- PG-008 — Posicionamento antes da criação como inputs formais editoriais; futura criação jogada preservada como direção candidata a ser resolvida separadamente.
- PG-009 — Contexto operacional mínimo + referência autoritativa para regras.
- PG-010 — DEUs apenas derivadas de workflows com utilidade repetida; nenhuma nova família aprovada aqui.
- PG-011 — Interface explícita com campanhas/aventuras sem escrever conteúdo de aventura.
- PG-012 — Fechar arquitetura agora; preservar implementação detalhada para grills/subagents especializados.

## Rejected Alternatives

Foram rejeitados como arquitetura principal:

- play guidance como simples resumo de ambientação;
- camada focada apenas em jogadores;
- camada focada apenas no Narrador;
- dois guias independentes sem workflow compartilhado;
- preparação totalmente pré-definida pelo Narrador como modelo obrigatório;
- capítulo único isolado sem interfaces distribuídas;
- camada totalmente distribuída sem núcleo próprio;
- núcleo colocado antes do cenário ou somente depois de todas as regras;
- duas entradas completas concorrentes;
- superfície única sem distinção funcional de audiência;
- terceira superfície autônoma apenas para continuidade;
- núcleo restrito ao início da crônica;
- manual operacional que reimplementa regras;
- integração apenas conceitual com criação;
- absorção do play guidance pelo capítulo de criação;
- simples apontamento de regras sem contexto de uso;
- versões próprias resumidas de regras;
- proibição total de DEUs de play guidance;
- transformação do núcleo inteiro em coleção de DEUs;
- compatibilidade apenas passiva com aventuras;
- inclusão de estruturas prontas de campanha;
- fechamento antecipado de toda implementação detalhada;
- arquitetura vaga delegada ao futuro escritor.

## Risks

### Risco: duplicação de cenário
Mitigação: síntese apenas operacional; autoridade permanece nos capítulos-fonte.

### Risco: segunda Rules Reference
Mitigação: explicar acionamento e retorno de regras, nunca reimplementá-las.

### Risco: vazamento de segredos
Mitigação: Storyteller-facing opera material e referencia segredos; não é o lar deles. GAP-ARCH-003 continua responsável pela arquitetura global.

### Risco: workflow burocrático
Mitigação: implementação futura deve testar se cada input realmente produz escolha, preparação ou consequência útil.

### Risco: criação guiada futura ficar engessada
Mitigação: este contrato fixa somente interface de inputs/outputs, não o método interno da criação.

### Risco: aventuras duplicarem onboarding e infraestrutura
Mitigação: contrato explícito de interface com outputs estáveis e possibilidade de override declarado.

### Risco: proliferação de DEUs
Mitigação: detachabilidade seletiva e necessidade demonstrada de uso repetido.

## Closure Assessment

Este contrato fornece a decisão arquitetural exigida para GAP-ARCH-002 ao definir:

- função;
- audiência;
- forma editorial;
- posição de leitura/uso;
- workflow central;
- famílias obrigatórias de informação;
- exclusões;
- responsabilidades player-safe e Storyteller-facing;
- propriedade autoritativa;
- relação com cenário, criação, regras, Dramatis Personae, DEUs e campanhas/aventuras;
- entradas e saídas;
- dependências e itens deliberadamente deferidos.

A arquitetura é suficientemente fechada para permitir que agentes futuros desenhem:

- a seção real “Jogando em Novydres”;
- integração de criação;
- ferramentas de preparação do Narrador;
- interfaces de campanha/aventura;

sem reabrir as decisões macroarquiteturais registradas aqui.

**Status deste artefato: `candidate`.**

A aprovação final e qualquer transição de status do Registry pertencem ao chat editorial principal. Este artefato não altera o Registry.