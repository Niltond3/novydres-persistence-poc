---
document_id: novydres_character_creation_specialist_b_decisions
version: 0.1.1
status: candidate_for_senior_editor_revalidation
date: 2026-08-13
workstream: character_creation_novydres_architecture
execution_node: B
scope: specialist_b_grill_decision_log
owns:
  - CHAR-B-001
  - CHAR-B-002
  - CHAR-B-003
  - CHAR-B-004
  - CHAR-B-005
  - CHAR-B-006
  - CHAR-B-007
  - CHAR-B-008
  - CHAR-B-009
  - CHAR-B-010
  - CHAR-B-011
  - CHAR-B-012
  - CHAR-B-013
  - CHAR-B-014
  - CHAR-B-015
  - CHAR-B-016
  - CHAR-B-017
  - CHAR-B-018
  - CHAR-B-019
  - CHAR-B-020
  - CHAR-B-021
  - CHAR-B-022
  - CHAR-B-023
  - CHAR-B-024
  - CHAR-B-025
depends_on:
  - novydres_character_creation_power_envelope_v0_1.md
  - novydres_character_creation_architecture_decision_inventory_v0_1_2.md
  - novydres_character_creation_specialist_a_decisions_v0_1.md
  - novydres_npc_power_scale_citywide_v0_1_1.md
  - novydres_npc_power_scale_citywide_decisions_v0_1.md
supersedes: novydres_character_creation_specialist_b_decisions_v0_1.md
final_verdict: READY_FOR_DOWNSTREAM_DESIGN_WITH_EXPLICIT_DEFERMENTS
patch_scope: decision_ledger_provenance_auditability_only
no_substantive_rule_change: true
decision_authority: unchanged_CHAR-B-001_through_CHAR-B-025
---

# Specialist B — Decision Log

## 1. Function

Registro consolidado das decisões materiais aprovadas no grill do Specialist B — Character Power Envelope.

Este documento registra decisões; a definição normativa consolidada vive em `novydres_character_creation_power_envelope_v0_1.md`.

## 2. Approved decisions

| ID | Decision | Status |
|---|---|---|
| `CHAR-B-001` | Três perfis ordinários reutilizáveis; excepcional/outlier como overlay/classificação, nunca quarto perfil | APPROVED |
| `CHAR-B-002` | Idade/estrato cria expectativa e teste de coerência; nunca entitlement mecânico | APPROVED |
| `CHAR-B-003` | Geração derivada genealogicamente quando possível; faixa provisória por envelope quando linhagem ainda não definida | APPROVED |
| `CHAR-B-004` | `Generation hard bounds → Profile envelope → Trajectory validation → Final BP` | APPROVED |
| `CHAR-B-005` | Torpor altera plausibilidade da trajetória de BP; não calcula BP | APPROVED |
| `CHAR-B-006` | Depth usa faixa ordinária + teto excepcional; Mastery Load separado | APPROVED |
| `CHAR-B-007` | Breadth usa faixa ordinária + excepcionalidade progressiva por composição | APPROVED |
| `CHAR-B-008` | Power Density é eixo independente com expectativa por perfil | APPROVED |
| `CHAR-B-009` | Aquisição rara/out-of-clan exige prova causal estruturada proporcional à raridade | APPROVED |
| `CHAR-B-010` | Mechanical Load validado pré-ficha e pós-ficha | APPROVED |
| `CHAR-B-011` | Rarity debt qualitativa cumulativa; individual → composição → impacto | APPROVED |
| `CHAR-B-012` | B audita excepcionalidade/causalidade de Asset Portfolio sem definir autoridade social/política | APPROVED |
| `CHAR-B-013` | Raridade demográfica gera explicação, não proibição/quotas de PJ | APPROVED |
| `CHAR-B-014` | Matriz híbrida: intervalos concretos + estados qualitativos; nomes/apresentação pública deferidos | APPROVED WITH DEFERMENT |
| `CHAR-B-015` | Valores concretos sobrepostos para os três perfis ordinários | APPROVED |
| `CHAR-B-016` | Escada `perfil ordinário → Exceptional Start → Declared Outlier` | APPROVED |
| `CHAR-B-017` | Iskander/Zoya como real testing profiles progressivos, sem congelar classificação final | APPROVED WITH EXTENSION |
| `CHAR-B-018` | Beckoning como derived flag pós-Geração/BP; adendo global de storyline de provocações | APPROVED WITH GLOBAL ADDENDUM |
| `CHAR-B-019` | Provocações podem alterar ficha dentro de envelope dinâmico controlado | APPROVED |
| `CHAR-B-020` | Envelope inicial autorizado + evolução somente por gateway explícito | APPROVED |
| `CHAR-B-021` | Gateway dispara por mudança material de classe de poder/excepcionalidade | APPROVED |
| `CHAR-B-022` | Demografia atua como contexto ativo nas provocações + auditoria final | APPROVED |
| `CHAR-B-023` | B entrega contrato operacional de integração narrativa a D1/D2 | APPROVED |
| `CHAR-B-024` | Perfil 1 é default; Perfis 2/3 dependem da premissa da crônica, não da idade | APPROVED |
| `CHAR-B-025` | B fecha `Q-017–028` e registra deferimentos; verdict READY FOR DOWNSTREAM DESIGN WITH EXPLICIT DEFERMENTS | APPROVED |

## 2.1 Canonical provenance mapping — CHAR-B-001–025

**Preservation statement:** `CHAR-B-001–025 UNCHANGED`.

This matrix is additive audit metadata. It does not replace the approved decision text or the closure matrix.

| Decision ID | CHAR-CREATE-Q IDs | Upstream authority | Relevant NPC-POWER IDs | Downstream consumers | Status |
|---|---|---|---|---|---|
| `CHAR-B-001` | Q-017, Q-018, Q-028 | Specialist A common-model/two-mode baseline; Power Scale envelope/outlier framework | 038, 075, 099 | G — Quick Creation; H — Guided Creation; I — NPC Creation Application & Depth Profiles; K — Final Integration | APPROVED / UNCHANGED |
| `CHAR-B-002` | Q-017, Q-018 | Power Scale chronological-stratum and no-retrospective-XP invariants | 002, 004, 075, 076, 100 | D1 — Played History Core; D2 — Played History Finalization / Integration; G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-003` | Q-019 | Specialist A required final Generation field; Power Scale genealogical Generation / lineage causality | 004, 005, 067, 099 | D1; D2; G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-004` | Q-020 | Specialist A required final BP field; Power Scale BP architecture | 007, 008 | D1; D2; G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-005` | Q-020, Q-021 | Power Scale BP trajectory + Torpor + no retrospective XP | 007, 043, 100 | D1; D2; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-006` | Q-022 | Power Scale Discipline architecture and soft benchmarks | 009, 010, 102 | G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-007` | Q-023 | Power Scale Discipline architecture, acquisition path and soft benchmarks | 009, 010, 011, 102 | G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-008` | Q-024 | Power Scale extra-power rule, Power Density and composite-exception audit | 011, 012, 040, 102 | D1; D2; G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-009` | Q-025 | Specialist A legality/acquisition-context interface; Power Scale causal acquisition | 011, 039, 049, 067, 068 | D1; D2; G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-010` | Q-026 | Power Scale two-pass Power Envelope / Mechanical Load / closure-by-auditability | 055, 102, 106 | D1; D2; G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-011` | Q-024, Q-025, Q-026, Q-027, Q-028 | Power Scale explanatory debt, composite exceptions and citywide exception audit | 039, 040, 072, 073, 103 | D1; D2; G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-012` | Q-027 | Specialist A Background legality boundary; Power Scale personal/institutional separation and Asset Portfolio | 013, 059, 097 | D1; D2; G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-013` | Q-019, Q-028 | Power Scale shared PC/NPC causality with setting-side population controls | 005, 038, 039, 072, 073, 074, 075, 099 | G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-014` | Q-017, Q-018, Q-020, Q-022, Q-023, Q-024, Q-026 | Specialist A common legality/two-mode baseline; Power Scale relative-envelope framework; user-approved publication deferment | 075, 099, 102 | G; H; I; K | APPROVED WITH DEFERMENT / UNCHANGED |
| `CHAR-B-015` | Q-017, Q-018, Q-019, Q-020, Q-022, Q-023, Q-024, Q-026 | Power Scale Generation/BP/Discipline/ordinary-population benchmarks; Specialist A common model | 004, 005, 007, 008, 009, 010, 011, 012, 074, 075, 099, 102 | G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-016` | Q-018, Q-026, Q-028 | Power Scale Declared Outlier, explanatory debt and composite-exception framework | 038, 039, 040, 072, 073, 102 | G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-017` | Q-017, Q-018, Q-028 | Existing Iskander/Zoya canonical profiles; Power Scale benchmark/revalidation policy; `Unknown stays Unknown` | 054, 077, 094, 095, 101 | I; K | APPROVED WITH EXTENSION / UNCHANGED |
| `CHAR-B-018` | Q-020, Q-028 | Power Scale Beckoning derivation; architecture-audit Played History inspiration; user-approved global provocation addendum | 018, 019, 021, 039, 100 | D1; D2; H; I; K | APPROVED WITH GLOBAL ADDENDUM / UNCHANGED |
| `CHAR-B-019` | Q-025, Q-026 | Specialist A legality interface; approved B provocation addendum; Power Scale causality/no-XP/load invariants | 039, 100, 102, 103 | D1; D2; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-020` | Q-017, Q-018, Q-026 | Approved B envelope/provocation architecture; Power Scale two-pass envelope and no-retrospective-XP | 039, 055, 100, 102 | D1; D2; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-021` | Q-026 | Approved B gateway architecture; Power Scale composite-exception and Mechanical Load gates | 040, 055, 102 | D1; D2; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-022` | Q-027, Q-028 | Power Scale demographics, exception-density and shared-PC/NPC invariants | 033, 039, 041, 056, 063, 072, 073, 074, 075, 099, 106 | D1; D2; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-023` | Q-017–Q-028 | Approved CHAR-B-001–022; architecture-audit D1/D2 dependency contract | 039, 055, 099, 100, 102 | D1 — Played History Core; D2 — Played History Finalization / Integration; K | APPROVED / UNCHANGED |
| `CHAR-B-024` | Q-017, Q-018 | Specialist A common model/mode parity; Power Scale relative envelopes + shared PC/NPC causality + no retrospective XP | 075, 099, 100 | G; H; I; K | APPROVED / UNCHANGED |
| `CHAR-B-025` | Q-017–Q-028 | Editorial governance; approved CHAR-B-001–024; Power Scale integration-contract and closure criteria | 093, 106 | D1; D2; G; H; I; K | APPROVED / UNCHANGED |

### 2.2 Provenance validation

- `CHAR-B` decisions expected: **25**
- decisions mapped: **25**
- missing decision IDs: **0**
- duplicate decision IDs: **0**
- no sequential decision beyond `CHAR-B-025` is instantiated
- mappings without a `CHAR-CREATE-Q-*`: **0**
- mappings without upstream authority: **0**
- mappings without downstream consumer or explicit none: **0**
- invented `NPC-POWER-*` provenance: **0**
- substantive decision changes: **0**

## 3. Decision details

### CHAR-B-001 — Arquitetura de perfis reutilizáveis

**Decisão:** três perfis ordinários internos + estado excepcional separado.

**Regra:**

- `Envelope Profile = Baseline | Established | Advanced` como identificadores internos provisórios;
- excepcional/outlier não é perfil, nível ou modo;
- perfis configuram múltiplos eixos, não orçamento universal;
- NPCs podem ocupar menos que o envelope;
- elder não implica Advanced; Advanced não implica elder.

**Deferimento:** nomes publicados melhores, em português, serão definidos apenas no grill de redação/apresentação do capítulo.

### CHAR-B-002 — Relação idade/estrato ↔ perfil

**Decisão:** idade informa plausibilidade, trajetória explica aquisição e o perfil autorizado limita a construção.

Personagens velhos podem ocupar envelopes baixos; personagens jovens podem ocupar envelopes superiores se a premissa e causalidade sustentarem. Não há age→power automático.

### CHAR-B-003 — Geração

**Decisão:** derivação genealógica primeiro; escolha provisória dentro da faixa do envelope quando a linhagem ainda não estiver definida.

Toda Geração provisória cria dívida de compatibilidade genealógica downstream. Baixa Geração fora da expectativa ordinária gera rarity debt e pode exigir exceção.

### CHAR-B-004 — Blood Potency inicial

**Decisão:**

`Generation hard bounds → Profile envelope → Trajectory validation → Final BP`

A faixa do perfil é subordinada à Geração; trajetória sustenta o valor; teto de Geração aumenta rarity debt; idade nunca calcula BP.

### CHAR-B-005 — Torpor

**Decisão:** Torpor é modificador qualitativo da trajetória de BP.

Não existe `anos ativos → BP`. Torpor não reduz Geração, não remove automaticamente Disciplines e não gera créditos mecânicos.

### CHAR-B-006 — Discipline Depth

**Decisão:** cada perfil usa faixa ordinária + teto excepcional; Mastery Load separado.

**Regra:** Depth mede quão alto chegou; Mastery Load mede quantas vezes chegou alto.

### CHAR-B-007 — Discipline Breadth

**Decisão:** faixa ordinária + faixa acima do ordinário com justificativa + limite excepcional autorizável.

Auditar junto com clan/out-of-clan, Depth, Mastery Load, Power Density e aquisição.

### CHAR-B-008 — Power Density

**Decisão:** eixo independente com estados `Standard | Expanded | High | Exceptional`.

- Standard: ordinário;
- Expanded: trajetória coerente;
- High: autorização + rarity debt claro;
- Exceptional: excepcionalidade material com revisão explícita.

Foco explica concentração; não compra poder.

### CHAR-B-009 — Prova causal de aquisição

**Decisão:** prova proporcional à raridade.

Campos quando aplicáveis:

- Fonte;
- Acesso;
- Oportunidade;
- Sustentação;
- Custo/Obrigação/Consequência;
- Compatibilidade Mecânica.

Played History/provocações podem preencher a prova; não geram entitlement.

### CHAR-B-010 — Mechanical Load

**Decisão:** audit em dois pontos.

1. pré-ficha: envelope + expectativa + excepcionalidades previstas;
2. pós-ficha: load real + stacking + aderência.

Subida material exige ajuste, justificativa, autorização ou excepcionalidade formal.

### CHAR-B-011 — Rarity Debt

**Decisão:** rarity debt qualitativa e cumulativa.

Perguntas:

1. excepcionalidade individual;
2. composição;
3. impacto.

Estados: ordinário; justificativa requerida; concentrada; composta; dominante/outlier.

Fraquezas não pagam poder.

### CHAR-B-012 — Backgrounds/Assets

**Decisão:** B audita o portfólio, não a autoridade social/política.

Dimensões: Source, Control, Access, Mobilization, Maintenance, Dependency, Exposure.

Distinguir pessoal, institucional, delegado e temporário.

### CHAR-B-013 — PJs e demografia

**Decisão:** raridade demográfica cria dívida de explicação e validation signal, não quota.

PJs compartilham causalidade do mundo, mas não ocupam “vagas” populacionais. Premissa de crônica pode limitar exceções localmente.

### CHAR-B-014 — Matriz híbrida

**Decisão:** usar números onde operacionalmente necessários e estados qualitativos onde a composição importa.

**Ressalva aprovada:**

- nomes ingleses são internos/provisórios;
- nomes públicos serão decididos no grill de escrita do capítulo;
- também será decidido depois se a matriz/perfis serão expostos ao jogador, apresentados indiretamente ou mantidos apenas para Narrador/editorial.

### CHAR-B-015 — Valores concretos dos perfis

**Perfil 1**

- Gen 12ª–16ª;
- BP 1–2;
- Depth 1–2; Depth 3 focal excepcional;
- Breadth 1–2; Breadth 3 justificável;
- Mastery Load sem pico 4–5 esperado;
- Density Standard;
- Load Lean–Focused.

**Perfil 2**

- Gen 10ª–13ª;
- BP 2–3;
- Depth 2–3; Depth 4 focal excepcional;
- Breadth 2–3; Breadth 4 autorizável;
- Mastery Load com um pico elevado como expectativa excepcional;
- Density Standard–Expanded;
- Load Focused–Broad.

**Perfil 3**

- Gen 8ª–11ª;
- BP 3–4;
- Depth 3–4; Depth 5 possível, mas material;
- Breadth 3–4; Breadth 5 autorizável sob audit;
- múltiplos picos possíveis, nunca automáticos;
- Density Expanded–High;
- Load Broad–Dense.

Sinais como 7ª Gen ou inferior, múltiplas Disciplines 5, Exceptional Density ou Saturated Load entram no regime excepcional, não em ilegalidade automática.

### CHAR-B-016 — Exceptional Start / Declared Outlier

**Decisão:** duas etapas acima do espaço ordinário.

`Exceptional Start` exige autorização, causalidade, rarity debt, load audit e impacto.

`Declared Outlier` é reservado a combinações dominantes que distorcem a escala ordinária.

Todo outlier é excepcional; nem toda exceção é outlier.

### CHAR-B-017 — Iskander/Zoya como real testing profiles

**Decisão:** ambos são stress tests progressivos e, quando o capítulo estiver construído, devem ser executados end-to-end pelo mesmo procedimento publicado.

- Iskander testa faixa superior de poder pessoal.
- Zoya testa separação entre poder sobrenatural e institucional/social.

Nenhuma classificação final é congelada nesta fase.

### CHAR-B-018 — Beckoning + adendo global de provocações

**Decisão principal:** Beckoning é derived flag pós-Geração/BP, sem custo, proibição ou alteração de perfil.

**Adendo global aprovado:** criação Guiada usa premissa solo inspirada em `Vampiro de Mil Anos`; efeitos narrativos com consequência mecânica aparecem como provocações registráveis em histórico e/ou ficha.

Toda pergunta, gateway e mecânica deve alimentar uma storyline que termine em personagem coeso, compatível com sua proposta e com Novydres.

### CHAR-B-019 — Provocações e envelope

**Decisão:** provocações podem gerar ganho, perda, troca, transformação, acesso, obrigação, condição ou efeito narrativo e alterar a ficha, mas sempre sob guardrail vivo.

Fluxo de validação:

`legalidade → causalidade → envelope → rarity → demografia → registro`

Ultrapassagem material exige conversão, limitação, substituição, exceção formal ou preservação apenas narrativa. Perdas não pagam por poder.

### CHAR-B-020 — Momento do envelope

**Decisão:** começar com envelope inicial autorizado e permitir evolução apenas por gateway explícito.

`Premissa inicial → Envelope autorizado → Provocações → Gateway → Envelope final`

Mudança de perfil nunca é silenciosa nem automática.

### CHAR-B-021 — Gatilhos de gateway

**Decisão:** gateway dispara por mudança material em qualquer eixo ou na composição.

Inclui:

- ultrapassar faixa ordinária;
- atingir teto excepcional;
- elevar Mastery Load/Density/Load;
- aquisição rara/out-of-clan material;
- Asset/Background excepcional;
- evolução para Composite/Dominant.

### CHAR-B-022 — Demografia durante a storyline

**Decisão:** demografia é contexto ativo das provocações + auditoria final.

Estados finais:

- demograficamente ordinário;
- incomum, mas coerente;
- excepcional e justificado;
- outlier com impacto citywide.

Nunca é quota.

### CHAR-B-023 — Contrato B→D1/D2

**Decisão:** entregar protocolo conceitual com:

- estado atual;
- eventos de provocação;
- validações;
- gateway;
- finalização.

B define o que a storyline preserva; D1/D2 definem como ela produz isso.

### CHAR-B-024 — Default e crônicas avançadas

**Decisão:** Perfil 1 é default quando a crônica não especifica outro envelope; Perfis 2 e 3 dependem da premissa da crônica.

A idade não determina perfil. Rápido/Guiado compartilham o mesmo perfil autorizado.

### CHAR-B-025 — Fechamento

**Decisão:** Specialist B fecha arquiteturalmente.

- `CHAR-CREATE-Q-017–028 = CLOSED`;
- matriz fechada;
- excepcionalidade/outlier fechados;
- integração com provocações fechada no nível de contrato;
- Iskander/Zoya mantidos como testing profiles;
- nomes públicos dos perfis deferidos;
- exposição jogador/Narrador deferida;
- desenho concreto das provocações deferido.

Esses deferimentos não reabrem B automaticamente salvo contradição posterior com suas invariantes.

**Verdict:** `READY FOR DOWNSTREAM DESIGN WITH EXPLICIT DEFERMENTS`.

## 4. Closure matrix

| Question | Status | Approved basis |
|---|---|---|
| `CHAR-CREATE-Q-017` | CLOSED | B-001, B-002, B-014, B-015, B-024 |
| `CHAR-CREATE-Q-018` | CLOSED | B-002, B-014, B-015, B-016, B-024 |
| `CHAR-CREATE-Q-019` | CLOSED | B-003, B-013, B-015 |
| `CHAR-CREATE-Q-020` | CLOSED | B-004, B-005, B-015 |
| `CHAR-CREATE-Q-021` | CLOSED | B-005 |
| `CHAR-CREATE-Q-022` | CLOSED | B-006, B-015 |
| `CHAR-CREATE-Q-023` | CLOSED | B-007, B-015 |
| `CHAR-CREATE-Q-024` | CLOSED | B-008, B-011, B-015 |
| `CHAR-CREATE-Q-025` | CLOSED | B-009, B-011, B-019 |
| `CHAR-CREATE-Q-026` | CLOSED | B-010, B-011, B-019, B-021 |
| `CHAR-CREATE-Q-027` | CLOSED | B-012, B-011, B-022 |
| `CHAR-CREATE-Q-028` | CLOSED | B-013, B-016, B-022 |

## 5. Deferred decisions — explicitly not B blockers

1. nomes públicos definitivos dos perfis;
2. exposição integral, parcial/indireta ou exclusiva ao Narrador/editorial;
3. estrutura e redação concreta das provocações;
4. quantidade/ordem de gateways na experiência publicada;
5. classificação final de Iskander/Zoya após teste end-to-end.

## 5.1 Corrective-patch preservation

`CHAR-B-001–025 UNCHANGED`

`CHAR-CREATE-Q-017–028 CLOSED`

The provenance matrix is additive and does not reclassify, reopen or materially reword any approved decision.

## 6. Final verdict

**READY FOR DOWNSTREAM DESIGN WITH EXPLICIT DEFERMENTS**

`CHAR-CREATE-Q-017–028 = CLOSED`