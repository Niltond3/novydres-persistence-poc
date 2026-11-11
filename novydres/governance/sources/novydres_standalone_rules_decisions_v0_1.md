---
document_id: novydres_standalone_rules_decisions
version: 0.1
status: candidate
date: 2026-08-04
scope: gap_arch_001_decision_log
target_gap: GAP-ARCH-001
contract:
  - novydres_standalone_rules_contract_v0_1.md
depends_on:
  - novydres_editorial_governance_v1_0.md
  - skill_grill_me_v1_0.md
  - novydres_gap_registry_v0_1.json
  - novydres_gap_registry_decisions_v0_1.md
  - novydres_editorial_map_v0_8_step7.json
  - novydres_format_contract_v0_2.md
---

# Novydres Standalone Rules Decisions v0.1

## Purpose

Registro auditável das decisões tomadas durante o grill de GAP-ARCH-001.

Este arquivo registra decisões arquiteturais. Ele não aprova o contrato, não altera o Registry e não resolve individualmente mecânicas ou fontes.

---

## SR-001 — Definição normativa de standalone

**Pergunta**  
Qual definição de standalone deve governar Novydres by Night?

**Resposta aprovada**  
Opção 2 — standalone operacional completo, com ressalva de catálogo amplo.

Um grupo com apenas Novydres deve conseguir criar qualquer personagem suportado e conduzir uma crônica normal de V5 em Novydres sem consultar outro livro para descobrir como uma mecânica necessária funciona.

Além do core necessário, Disciplinas, Méritos, Falhas, Vantagens, a massiva maioria dos Tipos de Predador e Especializações devem formar um conjunto amplo, cobrindo as publicações V5 admitidas e homebrews selecionados.

**Recomendação dada**  
Opção 2.

**Rationale**  
Compatibiliza a promessa standalone do mapa editorial com a integração entre criação e catálogo mecânico, sem exigir reprodução indiscriminada de todo conteúdo V5.

**Alternativas materialmente rejeitadas**
- Opção 1: standalone de sessão, permitindo dependência externa durante criação.
- Opção 3: standalone enciclopédico irrestrito.

**Consequência contratual**
- Seções 3, 5, 6, 7 e 8.
- Dependência externa é proibida para opções publicadas como suportadas.
- Catálogo amplo é obrigação editorial distinta do core mínimo.

**Fontes/dependências afetadas**
- novydres_editorial_map_v0_8_step7.json
- GAP-ARCH-001

---

## SR-002 — Classes normativas de inclusão

**Pergunta**  
Como classificar a profundidade de cobertura de cada regra ou opção?

**Resposta aprovada**  
Seis classes:
- `FULL_RULE`
- `FULL_OPTION`
- `ADAPTED_RULE`
- `OPERATIONAL_SUMMARY`
- `QUICK_REFERENCE`
- `EXTERNAL_OR_EXCLUDED`

**Recomendação dada**  
Aprovar as seis classes.

**Rationale**  
Distingue regra estrutural, opção de catálogo, adaptação, resumo e lookup sem criar burocracia excessiva.

**Alternativas materialmente rejeitadas**
- Classificação mais simples sem distinção entre regra e opção.
- Taxonomia excessivamente granular.

**Consequência contratual**
- Seção 4.
- Base para a Dependency Matrix.

**Fontes/dependências afetadas**
- GAP-ARCH-001
- novydres_format_contract_v0_2.md

---

## SR-003 — Core universal + fechamento de dependências

**Pergunta**  
Como determinar quais mecânicas são obrigatórias?

**Resposta aprovada**  
Opção 2 — core universal explícito + fechamento transitivo de dependências.

**Recomendação dada**  
Opção 2.

**Rationale**  
Uma lista fixa envelhece e pode deixar opções publicadas quebradas. O fechamento de dependências garante completude operacional.

**Alternativas materialmente rejeitadas**
- Opção 1: lista fixa fechada.
- Opção 3: inclusão automática de todo subsistema presente nas fontes admitidas.

**Consequência contratual**
- Seção 5.
- Nenhuma `FULL_OPTION` pode depender exclusivamente de fonte externa.

**Fontes/dependências afetadas**
- GAP-ARCH-001
- Capítulo 10
- catálogos mecânicos
- regras locais

---

## SR-004 — Arquitetura da criação de personagens

**Pergunta**  
Qual escopo de criação deve ser suportado?

**Resposta aprovada**  
Opção 2 — criação completa/guiada + criação rápida compatível.

**Recomendação dada**  
Opção 2.

**Rationale**  
Mantém onboarding completo e uma rota acelerada sem criar sistemas paralelos.

**Alternativas materialmente rejeitadas**
- Opção 1: apenas criação tradicional completa.
- Opção 3: múltiplos métodos independentes.

**Consequência contratual**
- Seções 6 e 17.
- Criação é autoritativa no procedimento, não nos catálogos individuais.
- Criação rápida não pode divergir mecanicamente.

**Fontes/dependências afetadas**
- novydres_editorial_map_v0_8_step7.json
- material legado de criação
- Capítulo 10

---

## SR-005 — Política de Disciplinas e Poderes

**Pergunta**  
Como organizar o catálogo amplo de Disciplinas/Poderes?

**Resposta aprovada**  
Opção 2 — catálogo consolidado e normalizado por estrutura mecânica, não por publicação.

**Recomendação dada**  
Opção 2.

**Rationale**  
Facilita consulta, elimina duplicação e permite consolidar revisões preservando proveniência.

**Alternativas materialmente rejeitadas**
- Opção 1: catálogo por publicação.
- Opção 3: catálogo oficial consolidado e homebrew em seção paralela.

**Consequência contratual**
- Seção 7.
- Cada poder admitido é `FULL_OPTION`.
- Revisões e duplicatas devem ser normalizadas.
- Homebrew deve ser explicitamente identificado.

**Fontes/dependências afetadas**
- inventário futuro de fontes V5
- catálogo de Disciplinas/Poderes
- homebrews selecionados

---

## SR-006 — Vantagens, Antecedentes, Méritos, Falhas e Especializações

**Pergunta**  
Qual fronteira deve governar esses catálogos?

**Resposta aprovada**  
Opção 2 — superset oficial consolidado + homebrew curado, com exclusões justificadas.

Exclusão objetiva somente por:
1. obsolescência/substituição;
2. incompatibilidade estrutural real;
3. duplicação mecânica efetiva.

Especializações são abrangentes, mas não uma lista universal fechada.

**Recomendação dada**  
Opção 2.

**Rationale**  
Preserva o objetivo de referência ampla sem transformar preferência temática em corte arbitrário.

**Alternativas materialmente rejeitadas**
- Opção 1: seleção temática Novydres.
- Opção 3: reprodução integral por fonte, inclusive redundâncias.

**Consequência contratual**
- Seção 8.
- Ausência de opção oficial válida exige justificativa objetiva.

**Fontes/dependências afetadas**
- inventário futuro de fontes
- catálogos de Advantages/Backgrounds/Merits/Flaws
- Especializações
- homebrews selecionados

---

## SR-007 — Profundidade dos sistemas de resolução

**Pergunta**  
Quanto do motor geral de V5 deve ser `FULL_RULE`?

**Resposta aprovada**  
Opção 2 — motor ordinário completo.

**Recomendação dada**  
Opção 2.

**Rationale**  
Standalone exige que o Narrador consiga resolver ações físicas, mentais e sociais sem conhecimento prévio do livro-base.

**Alternativas materialmente rejeitadas**
- Opção 1: motor mínimo.
- Opção 3: todas as variantes e subsistemas opcionais integralmente.

**Consequência contratual**
- Seção 9.
- Conflito social deve ter profundidade operacional adequada ao foco político de Novydres.

**Fontes/dependências afetadas**
- Capítulo 10
- Status
- Prestações
- conflitos sociais e físicos

---

## SR-008 — Sistemas vampíricos específicos

**Pergunta**  
Qual profundidade aplicar à condição vampírica estrutural?

**Resposta aprovada**  
Opção 2 — condição vampírica estrutural completa como `FULL_RULE`.

**Recomendação dada**  
Opção 2.

**Rationale**  
Baixa frequência não torna diablerie, torpor, Blood Bond ou vulnerabilidades menos fundamentais quando ocorrem.

**Alternativas materialmente rejeitadas**
- Opção 1: somente sistemas frequentes completos.
- Opção 3: todo subsistema vampírico de toda fonte admitida automaticamente completo.

**Consequência contratual**
- Seção 10.
- Qualquer Clã suportado deve ser mecanicamente completo dentro do produto.

**Fontes/dependências afetadas**
- catálogo de Clãs
- criação
- regras vampíricas
- Capítulo 10

---

## SR-009 — Relação entre baseline e regras próprias de Novydres

**Pergunta**  
Como uma adaptação local deve declarar sua relação com V5?

**Resposta aprovada**  
Opção 2 — quatro relações normativas:
- `REPLACEMENT`
- `EXTENSION`
- `EXCEPTION`
- `NEW_SUBSYSTEM`

**Recomendação dada**  
Opção 2.

**Rationale**  
“House rule” é insuficiente para declarar precedência, escopo e dependência.

**Alternativas materialmente rejeitadas**
- Opção 1: apenas oficial vs house rule.
- Opção 3: relação livre definida caso a caso sem taxonomia.

**Consequência contratual**
- Seções 11 e 13.
- Divergência material nunca pode existir silenciosamente.

**Fontes/dependências afetadas**
- Bairrismo
- Marco Territorial
- Status
- Prestações
- demais mecânicas locais

---

## SR-010 — Admissão de publicações oficiais V5

**Pergunta**  
Como definir quais publicações integram o corpus?

**Resposta aprovada**  
Opção 2 — política ampla + inventário versionado.

Estados de fonte:
- `ADMITTED`
- `SUPERSEDED`
- `PARTIAL`
- `EXCLUDED`

**Recomendação dada**  
Opção 2.

**Rationale**  
Mantém a intenção de cobertura ampla sem fazer novas publicações alterarem silenciosamente uma edição vigente.

**Alternativas materialmente rejeitadas**
- Opção 1: lista fechada dentro do contrato.
- Opção 3: admissão automática de qualquer nova publicação oficial.

**Consequência contratual**
- Seção 12.
- Inventário nominal é artefato futuro separado.
- Exclusões devem ser justificadas.

**Fontes/dependências afetadas**
- todas as fontes V5
- inventário futuro de fontes
- catálogos consolidados

---

## SR-011 — Fonte autoritativa e duplicação

**Pergunta**  
Como tratar uma mesma regra quando aparece em múltiplas superfícies?

**Resposta aprovada**  
Opção 2 — uma única fonte explicativa autoritativa + superfícies derivadas.

**Recomendação dada**  
Opção 2.

**Rationale**  
Reduz divergência entre criação, capítulo, catálogo, apêndice e DEU e é compatível com o contrato de formato.

**Alternativas materialmente rejeitadas**
- Opção 1: duplicação completa por conveniência.
- Opção 3: centralização obrigatória de toda regra no Capítulo 10.

**Consequência contratual**
- Seções 14 e 15.
- Conteúdo completo repetido deveria ser derivado da mesma fonte estruturada quando possível.

**Fontes/dependências afetadas**
- novydres_format_contract_v0_2.md
- Capítulo 10
- capítulos temáticos
- apêndices
- DEUs

---

## SR-012 — Responsabilidades entre superfícies editoriais

**Pergunta**  
Como dividir regras entre Capítulo 10, criação, capítulos temáticos, apêndices e DEUs?

**Resposta aprovada**  
Opção 2 — responsabilidades funcionais distribuídas.

**Recomendação dada**  
Opção 2.

**Rationale**  
Permite que o Capítulo 10 concentre core e catálogos sem arrancar regras contextuais de capítulos próprios e sem transformar apêndices/DEUs em fontes concorrentes.

**Alternativas materialmente rejeitadas**
- Opção 1: toda mecânica centralizada no Capítulo 10.
- Opção 3: capítulos autossuficientes por duplicação.

**Consequência contratual**
- Seções 16 a 19.
- Capítulo 10: core + criação + catálogos sistêmicos.
- Capítulos temáticos: regras contextuais autoritativas.
- Apêndices: lookup derivado.
- DEUs: superfícies derivadas destacáveis.
- Contrato informacional exato da Rules Reference DEU permanece deferred.

**Fontes/dependências afetadas**
- novydres_editorial_map_v0_8_step7.json
- novydres_format_contract_v0_2.md
- Capítulo 10
- Apêndices
- capítulos temáticos
- DEUs

---

# Approved Decisions

As decisões SR-001 a SR-012 foram explicitamente aprovadas pelo usuário durante o grill.

# Rejected Alternatives

Alternativas materialmente rejeitadas estão registradas em cada decisão. Em termos consolidados, foram rejeitadas:

- dependência externa para criação suportada;
- standalone puramente enciclopédico e irrestrito;
- taxonomia insuficiente de inclusão;
- core baseado apenas em lista fixa;
- criação rápida mecanicamente independente;
- catálogo mecânico organizado por livro;
- seleção temática restritiva das grandes famílias de opções;
- motor ordinário reduzido;
- condição vampírica estrutural resumida por baixa frequência;
- house rules sem relação formal com baseline;
- admissão automática e silenciosa de novas fontes;
- duplicação independente de regras;
- centralização absoluta de toda mecânica no Capítulo 10;
- autossuficiência de capítulos baseada em repetição integral.

# Deferred Questions

Permanecem deliberadamente deferidos:

- inventário nominal completo das fontes V5;
- homebrews concretamente selecionados;
- classificação individual de regras locais;
- lista final de Clãs/categorias suportadas;
- resolução individual de conflitos entre versões oficiais;
- implementação técnica da fonte estruturada única;
- informação exata de Rules Reference DEU;
- escrita/paginação do Capítulo 10;
- escrita/paginação dos Apêndices;
- inclusão individual de coterie creation.

Esses pontos não impedem o fechamento arquitetural porque os critérios para resolvê-los já estão definidos.

# Implementation Consequences

A implementação posterior deverá ser capaz de:

1. construir uma matriz auditável por família/regra;
2. identificar dependências transitivas;
3. manter inventário versionado de fontes;
4. consolidar duplicatas e revisões;
5. registrar proveniência oficial/homebrew;
6. registrar adaptação e precedência;
7. apontar uma fonte autoritativa por regra;
8. derivar criação, apêndices e DEUs sem criar cópias concorrentes;
9. testar se qualquer opção publicada funciona sem livro externo.

# Closure Assessment

O grill atingiu saturação arquitetural suficiente para GAP-ARCH-001.

As decisões aprovadas cobrem:

- definição de standalone;
- classes de inclusão;
- core mecânico obrigatório;
- fechamento de dependências;
- criação;
- Disciplinas/Poderes;
- Advantages/Backgrounds/Merits/Flaws;
- Especializações;
- resolução geral;
- condição vampírica;
- adaptações locais;
- política de fontes;
- autoridade/duplicação;
- Capítulo 10;
- apêndices;
- DEUs.

Nenhuma decisão restante é necessária para formular o contrato arquitetural candidato.

**READY_FOR_EDITORIAL_CLOSURE_REVIEW**