---
document_id: novydres_character_creation_power_envelope
version: 0.1.1
status: candidate_for_senior_editor_revalidation
date: 2026-08-13
workstream: character_creation_novydres_architecture
execution_node: B
scope: character_power_envelope_for_pc_and_npc_creation
owns:
  - CHAR-CREATE-Q-017
  - CHAR-CREATE-Q-018
  - CHAR-CREATE-Q-019
  - CHAR-CREATE-Q-020
  - CHAR-CREATE-Q-021
  - CHAR-CREATE-Q-022
  - CHAR-CREATE-Q-023
  - CHAR-CREATE-Q-024
  - CHAR-CREATE-Q-025
  - CHAR-CREATE-Q-026
  - CHAR-CREATE-Q-027
  - CHAR-CREATE-Q-028
depends_on:
  - novydres_master_senior_editor_prompt_v1_2.md
  - novydres_prompt_reuse_contract_v0_1.md
  - novydres_character_creation_novydres_architecture_audit_v0_1_3.md
  - novydres_character_creation_architecture_decision_inventory_v0_1_2.md
  - novydres_character_creation_core_v5_baseline_v0_1.md
  - novydres_character_creation_specialist_a_decisions_v0_1.md
  - novydres_npc_power_scale_citywide_v0_1_1.md
  - novydres_npc_power_scale_citywide_decisions_v0_1.md
  - 07_personagens/iskander_yasupov_v0_9.md
  - 07_personagens/madame_zoya_v0_9.md
supersedes: novydres_character_creation_power_envelope_v0_1.md
final_verdict: READY_FOR_DOWNSTREAM_DESIGN_WITH_EXPLICIT_DEFERMENTS
patch_scope: ledger_provenance_and_downstream_interface_separation_only
no_substantive_rule_change: true
decision_authority: unchanged_CHAR-B-001_through_CHAR-B-025
---

# Character Power Envelope — Novydres

## A. Função

Este artefato define o envelope de potência de criação consumido por todas as construções de personagem em Novydres.

Ele converte o `npc_power_scale_citywide` em uma arquitetura de criação aplicável tanto a PJs quanto a NPCs sem transformar controles demográficos de cenário em proibições automáticas para PJs.

Ele não define:

- um terceiro modo de criação;
- a sequência completa de criação;
- o conteúdo narrativo das provocações;
- catálogos de Disciplinas, poderes, rituais, Méritos, Falhas ou Backgrounds;
- Status, Dignitas, facções, território ou Marco Territorial;
- a apresentação publicada dos envelopes;
- nomes públicos definitivos para os perfis internos.

Existem exatamente dois modos de criação:

1. `Rápido`;
2. `Guiado`.

Ambos usam o mesmo modelo de legalidade e o mesmo Power Envelope autorizado.

## B. Invariantes

1. `QUICK ⊆ GUIDED ⊆ COMMON LEGALITY MODEL`.
2. Rápido e Guiado não possuem limites de poder diferentes por serem modos diferentes.
3. Idade informa plausibilidade; não concede pontos, XP, Geração, Potência de Sangue, Disciplinas, Backgrounds ou ativos.
4. Geração é genealógica, nunca proxy cronológico.
5. Blood Potency deriva de limites de Geração + envelope autorizado + trajetória validada.
6. Tempo cria oportunidade; não cria mastery automaticamente.
7. Disciplines são auditadas por Depth, Breadth, Mastery Load e Power Density.
8. Poder institucional, histórico e social permanece separado de poder sobrenatural pessoal.
9. Fraquezas, perdas e complicações nunca compram poder.
10. Raridade não é orçamento numérico; acumula-se qualitativamente em significado.
11. A demografia de Novydres informa plausibilidade e impacto, mas não cria quotas de personagem.
12. O Power Envelope é definido antes da ficha e auditado depois dela.
13. Na criação Guiada, o envelope funciona como guardrail vivo durante a storyline de provocações.
14. História nunca funciona como XP retroativo.

## C. Estrutura interna de perfis

B usa três perfis ordinários reutilizáveis. Seus identificadores atuais são estritamente internos e provisórios:

- `Baseline`;
- `Established`;
- `Advanced`.

Esses nomes NÃO são terminologia publicada aprovada.

### C.1 Relação com criação padrão

- Perfil 1 (`Baseline`) é a referência ordinária de criação de PJ quando a premissa da crônica não especifica potência diferente.
- Perfil 2 (`Established`) suporta personagens já estabelecidos e crônicas de potência intermediária.
- Perfil 3 (`Advanced`) suporta criação de alta potência e personagens muito desenvolvidos.

A crônica autoriza o espaço de potência; a trajetória determina como o personagem ocupa esse espaço.

Nenhum perfil é sinônimo de Neófito, Ancilla, Ancião ou qualquer estrato cronológico/social.

Um Ancilla pode ocupar qualquer dos três perfis. Um Neófito pode ocupar perfil superior quando a premissa autorizar e a causalidade sustentar. Um Ancião não recebe Perfil 3 automaticamente.

## D. Matriz híbrida dos perfis ordinários

A matriz combina intervalos concretos onde números são operacionalmente necessários e estados qualitativos onde a excepcionalidade depende da composição.

| Eixo | Perfil 1 — identificador interno `Baseline` | Perfil 2 — identificador interno `Established` | Perfil 3 — identificador interno `Advanced` |
|---|---|---|---|
| Geração ordinariamente esperada | 12ª–16ª | 10ª–13ª | 8ª–11ª |
| BP ordinário | 1–2 | 2–3 | 3–4 |
| Discipline Depth ordinário | 1–2 | 2–3 | 3–4 |
| Depth excepcional autorizável | 3 focal | 4 focal | 5 material |
| Discipline Breadth ordinária | 1–2 | 2–3 | 3–4 |
| Breadth acima do ordinário | 3 justificável | 4 autorizável | 5 sob auditoria |
| Mastery Load | nenhum pico 4–5 esperado | um pico alto pode existir como exceção focal | múltiplos picos possíveis sob audit, nunca automáticos |
| Power Density esperada | Standard | Standard–Expanded | Expanded–High |
| Mechanical Load esperado | Lean–Focused | Focused–Broad | Broad–Dense |
| Exceptional State | incomum | possível | possível, mas nunca automático |

A sobreposição é intencional. A coluna não concede automaticamente tudo nela contido e não representa pacote de benefícios.

### D.1 Sinais fora do espaço ordinário

São sinais fortes para revisão excepcional, não ilegalidade automática:

- 7ª Geração ou inferior;
- BP muito alto para o perfil ou saturação do teto permitido pela Geração;
- múltiplas Disciplines em 5;
- `Power Density = Exceptional`;
- `Mechanical Load = Saturated`;
- composições equivalentes de picos máximos ou raridades.

## E. Relação idade/estrato ↔ envelope

O estrato cronológico/social cria expectativa e teste de coerência, nunca entitlement mecânico.

O perfil é autorizado pela premissa da crônica, função do personagem e potência inicial desejada. A idade e a trajetória validam plausibilidade.

Consequências:

- personagem antigo pode ocupar envelope baixo por Torpor, perda, isolamento, acesso limitado ou trajetória equivalente;
- personagem jovem pode ocupar envelope superior quando a premissa permitir e a trajetória excepcional sustentar;
- idade não converte-se em XP retrospectivo;
- Methuselah não constitui perfil ordinário automático.

## F. Geração na criação

1. Se Sire e/ou Geração do Sire são conhecidos, a Geração do personagem é derivada pela genealogia aplicável.
2. Se a linhagem concreta ainda não estiver definida, o envelope autoriza uma faixa admissível e a Geração pode ser escolhida provisoriamente dentro dela.
3. Geração provisória cria obrigação downstream de compatibilidade genealógica final.
4. Geração abaixo da expectativa ordinária do perfil não é automaticamente ilegal, mas acrescenta rarity debt e pode exigir autorização excepcional.
5. Played History ou storyline de provocações pode explicar como a linhagem entrou na trajetória; não pode alterar retrospectivamente a Geração para obter vantagem.

## G. Blood Potency inicial

Fluxo normativo:

`Generation hard bounds → Profile envelope → Trajectory validation → Final BP`

- Geração sempre impõe os limites rígidos.
- O perfil estabelece a faixa ordinariamente autorizada.
- A trajetória pré-crônica sustenta o valor final.
- Idade só é evidência de oportunidade; nunca fórmula.
- Atingir o teto de BP permitido pela Geração acrescenta rarity debt independente.
- BP fora da faixa ordinária do perfil exige tratamento excepcional.

## H. Torpor e trajetória de BP

Torpor funciona como modificador qualitativo da trajetória, não como fórmula temporal.

Regra central:

> Torpor altera a plausibilidade da trajetória; não calcula o resultado mecânico.

Assim:

- períodos materiais de Torpor podem justificar BP menor que o esperado pela idade;
- vida majoritariamente ativa pode tornar BP muito baixo mais excepcional;
- despertar recente pode explicar defasagem entre idade, agência e potência atual;
- Torpor não reduz Geração;
- Torpor não remove automaticamente Disciplines;
- Torpor não gera créditos mecânicos;
- nenhum cálculo de anos ativos determina BP.

## I. Discipline Depth

Cada perfil possui:

1. faixa ordinária de Depth;
2. teto excepcional autorizável;
3. Mastery Load auditado separadamente.

Regra central:

> Depth mede quão alto o personagem chegou; Mastery Load mede quantas vezes ele chegou alto.

Uma Discipline muito alta não autoriza automaticamente várias outras altas. Múltiplos ratings 4–5 aumentam rarity debt mesmo no Perfil 3.

## J. Discipline Breadth

Cada perfil possui:

1. faixa ordinária de Disciplines materialmente desenvolvidas;
2. faixa acima do ordinário que exige justificativa;
3. limite excepcional autorizável.

Breadth elevada deve ser auditada junto com:

- quantidade de Disciplines de clã;
- quantidade out-of-clan;
- Depth;
- Mastery Load;
- Power Density;
- caminhos de aquisição.

Quantidade de Disciplines é apenas o primeiro sinal; excepcionalidade depende da composição.

## K. Power Density

Power Density permanece eixo independente.

Estados internos:

- `Standard` — normalmente não gera dívida própria relevante;
- `Expanded` — exige trajetória aquisitiva coerente;
- `High` — exige autorização e aumenta claramente rarity debt;
- `Exceptional` — excepcionalidade material com revisão explícita.

Foco pode explicar concentração, mas não funciona como pagamento por poder.

Alta Density combinada com alta Breadth, Depth e Mastery Load aumenta fortemente a excepcionalidade composta.

## L. Prova causal para aquisições raras/out-of-clan

Aquisições fora do ordinário usam prova causal estruturada proporcional à raridade.

Quando aplicável, registrar:

- `Fonte`;
- `Acesso`;
- `Oportunidade`;
- `Sustentação`;
- `Custo/Obrigação/Consequência`;
- `Compatibilidade Mecânica`.

Escalonamento:

- aquisição ordinária → evidência mínima;
- out-of-clan plausível → ao menos fonte + acesso;
- raro/restrito/Amalgam incomum → contexto mais concreto;
- singular/excepcional → história específica + autorização.

Played History/provocações podem fornecer a evidência, mas não criam entitlement.

## M. Mechanical Load Audit

Estados internos:

`Lean → Focused → Broad → Dense → Saturated`

Validação em dois pontos:

### M.1 Pré-ficha / pré-alocação

- definir o Power Envelope autorizado;
- registrar expectativa de Mechanical Load;
- identificar excepcionalidades previstas.

### M.2 Pós-ficha / pós-alocação

- auditar o Mechanical Load real;
- comparar com o envelope;
- revisar stacking de raridades;
- reclassificar quando necessário.

Subida material exige uma das seguintes respostas:

- justificativa;
- ajuste;
- autorização superior;
- `Exceptional Start`;
- `Declared Outlier`.

Regra central:

> O envelope é definido antes; a ficha prova depois se ficou dentro dele.

## N. Rarity Debt e excepcionalidade composta

Rarity debt é qualitativa e cumulativa.

A auditoria faz três perguntas:

1. `Excepcionalidade individual` — o elemento está dentro, acima ou fora da expectativa do perfil?
2. `Composição` — quantos eixos excepcionalmente altos coexistem e se reforçam?
3. `Impacto` — a combinação altera plausibilidade, papel na crônica ou posição relativa na cidade?

Estados internos:

- `ordinário`;
- `justificativa requerida`;
- `excepcionalidade concentrada`;
- `excepcionalidade composta`;
- `dominante/outlier`.

Fraquezas não pagam rarity debt. Especialização pode explicar concentração sem anulá-la. Justificativas individuais não impedem stacking coletivo.

Regra central:

> Raridade não é somada em pontos; ela é acumulada em significado.

## O. Exceptional Start e Declared Outlier

A fronteira acima do Perfil 3 usa dois estados distintos.

### O.1 Exceptional Start

Ultrapassa materialmente o Perfil 3, mas ainda pode existir dentro da escala normal da crônica.

Exige:

- autorização explícita;
- causalidade documentada;
- rarity debt reconhecida;
- Mechanical Load audit;
- avaliação de impacto na crônica.

Pode decorrer de pico extremo isolado, algumas excepcionalidades compostas, Geração muito rara, BP excepcional, concentração elevada de Disciplines ou Asset Portfolio extraordinário.

### O.2 Declared Outlier

Reservado para combinações que distorcem a escala ordinária.

Gatilhos qualitativos incluem:

- composite exception `Dominant`;
- vários picos máximos simultâneos;
- combinação rara de Geração + BP + Depth + Breadth + Density;
- `Mechanical Load = Saturated`;
- impacto que exige tratamento especial na calibração citywide;
- equivalentes funcionais de Methuselah/figura singular.

Regra:

> Todo outlier é excepcional; nem toda exceção é outlier.

Esses estados não são quarto perfil nem terceiro modo de criação.

## P. Backgrounds e Asset Portfolio

B audita a excepcionalidade e causalidade do portfólio sem definir a arquitetura social/política/territorial.

Dimensões de auditoria:

- Source;
- Control;
- Access;
- Mobilization;
- Maintenance;
- Dependency;
- Exposure.

Distinguir ainda:

- ativo pessoal;
- institucional;
- delegado;
- temporário.

A legalidade dos Backgrounds permanece com A. Status, Dignitas, facção, território e relações correlatas permanecem com C ou autoridade própria.

Idade não concede portfólio automaticamente.

## Q. PCs versus raridade demográfica

Raridade demográfica do cenário gera dívida de explicação e sinal de validação, não proibição automática nem quota.

Para PJs:

1. o traço deve ser mecanicamente legal;
2. deve caber no envelope ou receber exceção;
3. deve possuir causalidade suficiente;
4. raridades múltiplas acumulam rarity debt;
5. a premissa da crônica pode restringir exceções sem transformar isso em regra demográfica universal;
6. o PJ não ocupa uma “vaga” na pirâmide populacional;
7. combinações extremas podem exigir `Declared Outlier` e revisão de impacto citywide.

## R. Beckoning como derived flag

Beckoning é consequência derivada da configuração final, não variável usada para comprar ou limitar o personagem.

Depois de Geração e BP finais, registrar:

- `Beckoning relevance = not ordinarily eligible | eligible`;
- quando aplicável, `Intensity = latent | whisper | call | imperative` segundo a regra local vigente.

Esse registro:

- não concede nem remove pontos;
- não proíbe o personagem;
- não altera o perfil;
- não é calculado por idade;
- não afirma automaticamente que o Beckoning está manifestado em cena;
- apenas sinaliza relevância para a regra apropriada.

## S. Provocações na criação Guiada

A criação Guiada usa uma premissa de RPG solo inspirada em `Vampiro de Mil Anos`.

Perguntas, gateways e mecânicas devem alimentar desde o início uma storyline de provocações que termine em personagem conciso, causalmente coerente e compatível com Novydres.

Uma provocação pode produzir:

- ganho;
- perda;
- troca;
- transformação;
- acesso;
- obrigação;
- condição;
- consequência puramente narrativa.

Uma provocação pode ainda registrar um parágrafo de histórico e/ou alterar características como Atributos, Habilidades, Especialidades, Backgrounds/Antecedentes, Disciplines/Powers, Humanity, Blood Potency e outras opções legalmente suportadas.

Toda alteração mecânica passa por:

`legalidade → causalidade → aquisição → espaço no envelope → rarity → demografia → registro`

Se ultrapassar materialmente o envelope, o sistema deve:

- converter o resultado;
- limitar o resultado;
- substituir a consequência mecânica;
- elevar formalmente o perfil por gateway, se autorizado;
- entrar em `Exceptional Start`, se autorizado;
- ou manter somente o efeito narrativo.

Perdas e complicações não pagam matematicamente por ganhos.

## T. Envelope dinâmico controlado

A criação Guiada começa com uma premissa de potência autorizada que define o envelope inicial.

Fluxo:

`Premissa inicial → Envelope autorizado → Provocações → Gateway de reavaliação, se necessário → Envelope final`

Mudança de perfil nunca ocorre silenciosamente nem por soma automática de provocações.

O gateway pode:

- manter o perfil e converter/limitar resultados;
- elevar formalmente ao perfil seguinte, se a premissa permitir;
- entrar em `Exceptional Start`;
- preservar efeito narrativo sem conceder alteração mecânica.

## U. Gatilhos de gateway

Gateway de reavaliação é disparado por mudança material de estado, não por toda alteração de ficha.

Gatilhos incluem:

- ultrapassar faixa ordinária;
- alcançar teto excepcional;
- aumentar Mastery Load;
- elevar Power Density;
- introduzir aquisição rara/out-of-clan material;
- subir Mechanical Load de categoria;
- adicionar Asset/Background excepcional;
- fazer raridades previamente aceitáveis passarem a `Composite` ou `Dominant`.

Regra central:

> Gateway é acionado por mudança de classe qualitativa de poder ou excepcionalidade.

## V. Demografia como contexto ativo

A demografia de Novydres atua durante a storyline como contexto de plausibilidade e no final como auditoria.

Pode informar:

- raridade de Geração;
- prevalência relativa de estratos;
- posição territorial/social;
- acesso a linhagens;
- concentração de poder;
- disponibilidade de instituições;
- raridade de práticas, mentores e recursos;
- posição relativa na população Cainita.

Isso influencia quais provocações são plausíveis, quais exigem causalidade adicional, quais geram rarity debt ou consequências sociais e quais podem exigir excepcionalidade formal.

Auditoria final de fit demográfico:

- `demograficamente ordinário`;
- `demograficamente incomum, mas coerente`;
- `excepcional e justificado`;
- `outlier com impacto citywide`.

A demografia nunca funciona como quota numérica de personagem.

## W. Contrato B → D1/D2

B define o que a storyline precisa preservar; D1/D2 definem como a storyline produz isso.

### W.1 Estado atual obrigatório

A implementação da criação Guiada deve poder representar:

- envelope autorizado;
- Geração;
- BP;
- Depth;
- Breadth;
- Mastery Load;
- Power Density;
- Mechanical Load;
- rarity debt;
- exceptional state;
- demography state.

### W.2 Evento de provocação

Eventos podem produzir:

- ganho;
- perda;
- troca;
- transformação;
- acesso;
- obrigação;
- condição;
- efeito narrativo.

### W.3 Validação obrigatória

Cada consequência material deve respeitar:

- legalidade;
- causalidade;
- aquisição;
- envelope;
- rarity;
- demografia.

### W.4 Gateway

Quando materialmente acionado, pode:

- aceitar;
- converter;
- limitar;
- substituir;
- elevar perfil;
- elevar para `Exceptional Start`;
- manter apenas efeito narrativo.

### W.5 Finalização

A finalização deve executar:

- post-sheet audit;
- Mechanical Load;
- composição de rarity debt;
- fit demográfico;
- Beckoning derived flag;
- blockers/dependencies restantes.

B não define número, ordem, texto ou estrutura literária das provocações.

## X. Iskander Yasupov e Madame Zoya — real testing profiles

Iskander e Zoya são perfis reais de teste progressivo da arquitetura.

Nesta fase:

- nenhuma ficha é editada;
- nenhum valor ausente é inventado;
- nenhum perfil final é congelado;
- ambos permanecem sujeitos a targeted mechanical revalidation.

### X.1 Iskander Yasupov

Testa principalmente a faixa superior de poder pessoal.

Dados atuais relevantes:

- Gangrel;
- 8ª Geração;
- BP 4;
- Abraço c. 1794;
- Xerife;
- Sire Kuthulun.

Leitura B:

- 8ª Geração entra na expectativa superior do Perfil 3, mas permanece rara citywide;
- BP 4 cabe ordinariamente no Perfil 3;
- cargo de Xerife não concede BP, Depth, Breadth ou mastery;
- Depth/Breadth/Density/Load completos devem ser auditados na targeted revalidation;
- a ficha final pode permanecer Perfil 3 ou subir para `Exceptional Start`;
- 8ª Geração + BP 4, isoladamente, não o transforma em outlier.

### X.2 Madame Zoya

Testa principalmente a independência entre poder sobrenatural e poder institucional/social.

Dados atuais relevantes:

- Nosferatu;
- 11ª Geração;
- BP 2;
- Abraço em 1918;
- Harpia Maior + Chanceler;
- forte concentração de arquivos, precedentes, intermediários, segredos e memória institucional.

Leitura B:

- 11ª Geração é compatível com mais de um perfil;
- BP 2 não exige classificação sobrenatural alta;
- idade não exige BP maior;
- múltiplos cargos não acumulam automaticamente potência pessoal;
- seu Asset Portfolio e Historical Reach podem ser extraordinários sem inflar Disciplines/BP;
- rituais exclusivos não resolvidos permanecem dependências e não podem ser inferidos.

### X.3 Teste end-to-end futuro

Quando o capítulo de criação estiver efetivamente construído, Iskander e Zoya devem ser submetidos ao mesmo procedimento oferecido no suplemento.

O teste deve responder:

> É possível chegar de forma legítima, reproduzível e auditável a personagens como estes usando a criação publicada?

Eles não são templates ou caps normativos; são stress tests reais do sistema.

## Y. Closure matrix — CHAR-CREATE-Q-017–028

| Question | Closure | Basis B |
|---|---|---|
| `CHAR-CREATE-Q-017` Standard PC starting power envelope | CLOSED | `CHAR-B-001`, `002`, `014`, `015`, `024` |
| `CHAR-CREATE-Q-018` Ancilla/older-PC creation envelope | CLOSED | `CHAR-B-002`, `014`, `015`, `016`, `024` |
| `CHAR-CREATE-Q-019` Generation choice/derivation | CLOSED | `CHAR-B-003`, `013`, `015` |
| `CHAR-CREATE-Q-020` Starting Blood Potency | CLOSED | `CHAR-B-004`, `005`, `015` |
| `CHAR-CREATE-Q-021` Torpor impact on pre-chronicle BP trajectory | CLOSED | `CHAR-B-005` |
| `CHAR-CREATE-Q-022` Discipline Depth starting envelope | CLOSED | `CHAR-B-006`, `015` |
| `CHAR-CREATE-Q-023` Discipline Breadth starting envelope | CLOSED | `CHAR-B-007`, `015` |
| `CHAR-CREATE-Q-024` Power Density / extra-power handling | CLOSED | `CHAR-B-008`, `011`, `015` |
| `CHAR-CREATE-Q-025` Rare/out-of-clan acquisition proof standard | CLOSED | `CHAR-B-009`, `011`, `019` |
| `CHAR-CREATE-Q-026` Mechanical Load validation point | CLOSED | `CHAR-B-010`, `011`, `019`, `021` |
| `CHAR-CREATE-Q-027` Exceptional Background/Asset envelope | CLOSED | `CHAR-B-012`, `011`, `022` |
| `CHAR-CREATE-Q-028` PC exception handling vs citywide rarity | CLOSED | `CHAR-B-013`, `016`, `022` |

## Z. Downstream interfaces, deferments and blockers

### Z.1 B → D1/D2 — Played History Core / Finalization & Integration

Consume:

- matriz híbrida de envelopes;
- envelope dinâmico controlado;
- contratos de estado/evento/validação/gateway/finalização;
- regra de provocações como causalidade, nunca XP farm;
- fit demográfico como contexto ativo;
- proof standard para aquisições raras.

Não reinterpretar:

- idade como orçamento;
- modo Guiado como modo mais poderoso;
- perdas como pagamento mecânico;
- demografia como quota.

Este contrato permanece clericalmente sincronizado com `W. Contrato B → D1/D2`; nenhuma nova decisão de Played History é criada por este patch.

### Z.2 B → G — Quick Creation Interface

G deve consumir apenas os outputs já aprovados de B necessários ao modo `Rápido`:

- um Power Envelope autorizado conforme a premissa da crônica;
- a mesma ontologia comum de potência aplicável a PJs e NPCs;
- o mesmo modelo de envelope usado por `Guiado`;
- nenhuma potência adicional ou reduzida em razão da brevidade procedimental;
- validação pré-ficha e pós-ficha do envelope;
- Geração sob regra genealógica e faixas autorizadas;
- Blood Potency pelo pipeline `Generation hard bounds → Profile envelope → Trajectory validation → Final BP`;
- Discipline Depth, Breadth, Mastery Load e Power Density dentro dos limites e estados aprovados;
- rarity debt qualitativa e cumulativa;
- Mechanical Load Audit;
- gates de `Exceptional Start` e `Declared Outlier`;
- Beckoning como estado derivado pós-Geração/BP quando relevante.

B não define o procedimento de Quick, seus atalhos, sua ordem de escolhas ou defaults não previamente aprovados.

### Z.3 B → H — Guided Creation Interface

H deve consumir:

- o mesmo Power Envelope autorizado aplicável ao modo `Rápido`;
- paridade de potência: `Guiado` não recebe mais poder bruto por ser mais longo;
- provocações capazes de alterar estado narrativo ou mecânico somente sob o envelope autorizado;
- legalidade e causalidade de cada consequência material;
- prova de aquisição quando aplicável;
- rarity debt e fit demográfico como validações ativas;
- Mechanical Load durante a trajetória e na auditoria final;
- gateway explícito quando houver escalada material de classe de poder ou excepcionalidade;
- conversão, limitação, substituição, elevação formal autorizada ou preservação apenas narrativa quando o envelope seria excedido;
- auditoria final do envelope, incluindo composição de raridade e Beckoning derived flag.

B não define prompts, número/ordem de eventos, sequência concreta de provocações ou o engine final de Played History.

### Z.4 B → I — NPC Application & Depth Profiles Interface

I deve preservar:

- a mesma ontologia comum de potência para PJs e NPCs;
- exatamente os dois modos `Rápido` e `Guiado`; não existe terceiro modo de criação para NPCs;
- profundidade de perfil/apresentação de NPC não concede potência adicional;
- classes de apresentação como principal, secundário, lendário e dependente permanecem separadas do envelope diegético real;
- I pode selecionar/consumir o envelope autorizado apropriado segundo papel e premissa, sem redefinir as faixas de B;
- rarity debt, `Exceptional Start` e `Declared Outlier` continuam aplicáveis;
- um perfil simplificado ou mecanicamente incompleto não implica que o personagem seja menos poderoso no mundo;
- dependências mecânicas não resolvidas permanecem explícitas e não podem ser preenchidas por inferência;
- Iskander e Zoya permanecem stress tests progressivos, não templates ou hard caps.

B não define os depth profiles de I, sua taxonomia operacional ou seu protocolo completo de apresentação.

### Z.5 B → K — Final Integration Requirements

K deve rejeitar qualquer integração downstream que viole as invariantes aprovadas de B:

- ontologia comum de potência para PJs e NPCs;
- exatamente dois modos de criação: `Rápido` e `Guiado`;
- idade não concede entitlement automático de poder;
- Geração permanece genealógica;
- Blood Potency preserva `Generation hard bounds → Profile envelope → Trajectory validation → Final BP`;
- Discipline Depth e Breadth permanecem eixos distintos;
- Mastery Load e Power Density permanecem preservados;
- Mechanical Load Audit permanece qualitativo e em dois pontos;
- rarity debt permanece qualitativa/cumulativa, nunca orçamento numérico;
- `Exceptional Start` e `Declared Outlier` permanecem gates separados do perfil ordinário;
- paridade entre Quick/Guided permanece obrigatória;
- poder político/social/institucional não se converte automaticamente em poder sobrenatural pessoal;
- Beckoning permanece derived flag pós-Geração/BP, não moeda ou gate de compra;
- nomes públicos dos perfis e exposição ao jogador/Narrador permanecem deferidos até resolução aprovada por especialista downstream competente;
- forma publicada das provocações e gateways permanece deferida.

K não recebe autoridade de B para inventar novas regras; sua função é integrar e detectar drift.

### Z.6 Retro triggers

Nenhum retro trigger obrigatório para Capítulos 01–06 é criado por B neste momento.

Se a futura apresentação publicada exigir redistribuição estrutural de regras já fechadas em capítulos anteriores, aplicar a política vigente de dependência retroativa/memória viva; isso não é inferido antecipadamente por B.

### Z.7 Blockers

Nenhum blocker arquitetural permanece em `CHAR-CREATE-Q-017–028`.

Dependências downstream permanecem deliberadamente abertas:

- design detalhado das provocações;
- apresentação pública dos envelopes;
- revalidação end-to-end Iskander/Zoya;
- mecânicas ainda não resolvidas nos perfis existentes;
- agentes posteriores D1/D2/G/H/I/K conforme DAG vigente.

## Final readiness verdict

**READY FOR DOWNSTREAM DESIGN WITH EXPLICIT DEFERMENTS**

`CHAR-CREATE-Q-017–028 = CLOSED`

B está arquiteturalmente fechado sob invariantes + auditabilidade. Os deferimentos de publicação e design narrativo não constituem pendência de B enquanto preservarem as regras aqui consolidadas.