---
document_id: novydres_revelation_architecture_decisions
version: 0.1
status: candidate
date: 2026-08-05
scope: gap_arch_003_grill_decision_log
target_gap: GAP-ARCH-003
supersedes: null
contract: novydres_revelation_architecture_contract_v0_1.md
---

# Novydres — Revelation Architecture Decisions v0.1

## Purpose

Registrar de forma auditável as decisões tomadas no grill de GAP-ARCH-003.

O grill foi encerrado após **12 perguntas substantivas**, sem segunda rodada, com saturação arquitetural suficiente para produzir o contrato candidato.

---

## RA-001 — Modelo global de audiência

**Question:** Quais classes mínimas de acesso do leitor devem existir?

**Approved answer:** Três classes ortogonais ao conhecimento ficcional: `player_safe`, `storyteller_operational`, `storyteller_secret`.

**Recommendation:** Opção 2.

**Rationale:** Reader Access precisa responder quem pode ler, sem confundir isso com o que um personagem sabe. Também preserva a decisão já estabelecida em Play Guidance de que Storyteller-facing não é sinônimo de segredo.

**Rejected alternatives:** duas classes apenas; taxonomia extensa misturando mortal/Cainita/facção com segurança editorial.

**Consequence:** acesso do leitor e conhecimento de personagem passam a ser dimensões independentes.

**Affected artifacts/dependencies:** Play Guidance; DEUs; Dramatis Personae; Loresheets; Chapter 13; adventures.

---

## RA-002 — Vocabulário de Character Knowledge

**Question:** Qual deve ser a granularidade mínima do conhecimento ficcional?

**Approved answer:** `public`, `cainite_common`, `conditional`, `unknown`.

**Recommendation:** Opção 2.

**User addendum:** a sintaxe exata de publicação não deve transformar esses códigos em badges repetitivos e visualmente cansativos.

**Rationale:** O vocabulário pequeno cobre alcance ficcional sem proliferar estados para cada clã, facção, cargo ou Loresheet.

**Rejected alternatives:** `common/restricted` apenas; taxonomia extensa por origem de acesso.

**Consequence:** `conditional` usa gate separado quando necessário; os códigos são semânticos, não necessariamente visuais.

**Affected artifacts/dependencies:** character creation; Loresheets; factions; NPCs; onboarding.

---

## RA-003 — Sintaxe de publicação de Character Knowledge

**Question:** Como os estados de Character Knowledge aparecem na publicação?

**Approved answer:** Contexto por padrão + sinalização somente quando há mudança relevante.

**Recommendation:** Opção 2.

**Rationale:** A classificação deve permanecer auditável internamente sem dominar o layout.

**Rejected alternatives:** badge obrigatório em toda ocorrência; forma visual fixa por estado.

**Consequence:** seções podem estabelecer baseline; desvios relevantes são publicados preferencialmente em linguagem natural.

**Affected artifacts/dependencies:** frontmatter; parser; Atlas; Dramatis Personae; Loresheets; layout editorial.

---

## RA-004 — Modelo interno de verdade

**Question:** Qual o menor vocabulário útil de truth states?

**Approved answer:** `established`, `disputed`, `partial`, `false`, `unresolved`.

**Recommendation:** Opção 2.

**User correction/addendum:** esses estados devem ser internos e, no máximo, explicitados em superfícies autorizadas do Narrador. Marcar algo como falso ou verdadeiro para jogadores destrói peso narrativo e enfraquece red herrings.

**Rationale:** separa verdade objetiva de circulação, acesso e apresentação.

**Rejected alternatives:** `fact/uncertain/secret`; vocabulário extenso que mistura rumor, propaganda, verdade e acesso.

**Consequence:** truth state não pode funcionar como certificado player-facing de confiabilidade.

**Affected artifacts/dependencies:** rumor system; Chapter 13; continuity audit; adventures.

---

## RA-005 — Voz epistemicamente situada

**Question:** Até onde o player-facing deve evitar voz onisciente?

**Approved answer:** Perspectiva in-fiction generalizada, sem transformar toda informação em módulo formal de rumor.

**Recommendation:** Opção 2.

**Rationale:** A publicação deve evitar denunciar segredos pela diferença de tom entre fatos “confirmados” e informações duvidosas.

**Rejected alternatives:** incerteza somente para itens sensíveis; tratar todo lore como rumor formal.

**Consequence:** registros, tradição, consenso, versão oficial e outras fontes in-fiction podem sustentar tanto verdades quanto red herrings.

**Affected artifacts/dependencies:** Chapters 01–07; Atlas; history; institutions; Dramatis Personae.

---

## RA-006 — Truth ownership

**Question:** Onde vive a resolução objetiva de rumores e claims incertos?

**Approved answer:** Um único authoritative truth home, com destino contextual.

**Recommendation:** Opção 2.

**Rationale:** Evita versões concorrentes sem inflar Chapter 13 com cada rumor.

**Rejected alternatives:** todo rumor resolvido em Chapter 13; resolver somente quando entrar em jogo.

**Consequence:** global secret → Chapter 13; adventure secret → adventure; non-secret authority → thematic source; undecided → `unresolved`.

**Affected artifacts/dependencies:** Chapter 13; adventures; rumors; NPCs; Loresheets.

---

## RA-007 — Papel das Loresheets

**Question:** Até onde Loresheets podem revelar verdade?

**Approved answer:** Revelação progressiva, mas sem autoridade final por padrão.

**Recommendation:** Opção 2.

**Rationale:** Permite progressão epistemológica sem fragmentar a verdade autoritativa.

**Rejected alternatives:** Loresheets nunca revelam verdades; Loresheets como repositórios completos de verdade.

**Consequence:** uma Loresheet pode aproximar, confirmar ou revelar informação, mas deriva do truth home quando ele existe fora dela.

**Affected artifacts/dependencies:** Loresheet architecture; character creation; Chapter 13; progressive discovery.

---

## RA-008 — Semântica dos marcadores sobrescritos

**Question:** O que significam `²` e `³`?

**Approved answer:** A premissa da pergunta foi rejeitada. Todos os marcadores sobrescritos são apenas contadores locais de referências.

**User correction:** a primeira referência é `¹`, a segunda `²`, a terceira `³`, a quarta `⁴` e assim por diante. Nenhum número define pipeline, audiência ou capítulo específico.

**Recommendation after correction:** ratificar a semântica ordinal pura.

**Rationale:** A referência impressa serve para localizar a nota correspondente; semântica de segurança e destino pertence ao link/metadata.

**Rejected alternatives:** `²` como player-permissible; `³` como Storyteller secret; números como tipo de capítulo.

**Consequence:** rodapé resolve a referência conceitualmente como `Capítulo: Título geral, página`.

**Affected artifacts/dependencies:** all chapters; footnotes; parser; DEUs; navigation.

---

## RA-009 — Obrigatoriedade de cross-reference

**Question:** Quando uma referência é obrigatória?

**Approved answer:** Quando preserva ownership, segurança ou operação.

**Recommendation:** Opção 2.

**Rationale:** Nem toda leitura adicional merece nota, mas dependências arquiteturais precisam ser rastreáveis.

**Rejected alternatives:** referenciar toda dependência; remover a maior parte das referências da publicação.

**Consequence:** referência é mandatória quando a omissão criaria falsa autoridade local, esconderia fronteira de acesso ou quebraria dependência operacional.

**Affected artifacts/dependencies:** DEUs; rules; Play Guidance; Chapter 13; Loresheets; NPC profiles.

---

## RA-010 — Duplicação

**Question:** Quanto conteúdo pode ser repetido entre superfícies?

**Approved answer:** Restatement funcional mínimo, sem duplicação de autoridade.

**Recommendation:** Opção 2.

**Rationale:** Uma unidade destacável precisa de contexto local, mas cópias extensas geram drift.

**Rejected alternatives:** proibição quase total de duplicação; duplicação livre desde que consistente.

**Consequence:** repetir contexto suficiente para operar, nunca autoridade suficiente para competir.

**Affected artifacts/dependencies:** DEUs; Play Guidance; Loresheets; Dramatis Personae; adventures.

---

## RA-011 — Segurança física e `dual_use`

**Question:** Como `dual_use` deve funcionar na segurança física de DEUs?

**Approved answer:** O usuário rejeitou a necessidade da categoria.

**User decision:** `dual_use` é redundante porque `player_safe` já especifica livre circulação; utilidade operacional não constitui categoria de segurança.

**Additional mandatory instruction:** o uso e a menção de `dual_use` devem ser **retroativamente removidos** do projeto.

**Rationale:** Qualquer conteúdo pode ser útil a Narrador e jogadores; isso não altera quem pode lê-lo ou manuseá-lo.

**Rejected alternatives:** misturar player-safe na frente e secret no verso; manter `dual_use` como terceira classe; depender de alerta gráfico.

**Consequence:** 
- `dual_use` torna-se valor obsoleto;
- deve ser removido de metadata, documentação e exemplos;
- unidade manipulável por jogadores precisa ser inteiramente player-safe;
- material secreto deve ser fisicamente separável.

**Affected artifacts/dependencies:** format contract maintenance; DEU declarations; NPC dossiers; handouts; future templates; validation pipeline.

---

## RA-012 — Segurança de navegação digital

**Question:** Metadados de navegação pertencem ao spoiler envelope?

**Approved answer:** Sim.

**Recommendation:** Opção 2.

**Rationale:** bookmarks, TOC, índice e títulos podem revelar respostas sem o jogador abrir a página secreta.

**Rejected alternatives:** proteger apenas o corpo; exigir agora PDFs totalmente separados de player/ST.

**Consequence:** títulos e metadata devem identificar o assunto sem revelar a resposta; implementação técnica fica downstream.

**Affected artifacts/dependencies:** Chapter 13; adventures; PDF pipeline; bookmarks; TOC; index; cross-reference labels.

---

# Approved Decisions

RA-001 a RA-012 estão incorporadas em `novydres_revelation_architecture_contract_v0_1.md`.

# Rejected Alternatives

As alternativas materialmente rejeitadas estão registradas em cada decisão.

# Deferred Questions

- conteúdo real de Chapter 13;
- respostas reais de segredos;
- resolução de rumores específicos;
- mecânicas exatas de Loresheets;
- parser/frontmatter final;
- implementação automatizada de validação;
- pipeline PDF;
- adventure format;
- final player/ST packaging.

A remoção retroativa de `dual_use` **não é uma pergunta deferida**; é uma decisão aprovada cuja migração deve ser executada em workstream autorizado.

# Closure Record

O grill atingiu **12/12 perguntas substantivas** e alcançou saturação arquitetural.

Não há segunda rodada autorizada ou necessária neste momento.

O resultado é candidato e deve retornar ao chat editorial principal para julgamento.

Este decision log não atualiza o Gap Registry e não marca GAP-ARCH-003 como resolved.