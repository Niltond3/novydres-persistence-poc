---
document_id: novydres_standalone_rules_contract
version: 0.1
status: candidate
date: 2026-08-04
scope: standalone_v5_rules_architecture
closes_candidate:
  - GAP-ARCH-001
depends_on:
  - novydres_editorial_governance_v1_0.md
  - novydres_gap_registry_v0_1.json
  - novydres_editorial_map_v0_8_step7.json
  - novydres_format_contract_v0_2.md
decision_log:
  - novydres_standalone_rules_decisions_v0_1.md
---

# Novydres Standalone Rules Contract v0.1

## 1. Purpose

Este contrato define a arquitetura normativa pela qual **Novydres by Night** deve ser jogável sem acesso direto aos livros-base de Vampire: The Masquerade 5th Edition, preservando ao mesmo tempo um catálogo mecânico amplo e consolidado.

Este documento não escreve o Capítulo 10, não redefine mecânicas individuais e não fixa layouts de DEU. Ele estabelece critérios auditáveis de inclusão, profundidade, dependência, adaptação, autoridade e distribuição editorial das regras.

## 2. Status and Authority

- Status: `candidate`.
- O chat editorial principal permanece a autoridade final para aprovação.
- Este contrato MUST NOT, por si só, alterar o status de GAP-ARCH-001 no Registry.
- Versões mais recentes explicitamente aprovadas dos arquivos de governança e arquitetura prevalecem em caso de conflito.
- Regras específicas já aprovadas em seus capítulos autoritativos MUST NOT ser silenciosamente substituídas por este contrato.

## 3. Definition of Standalone

Novydres adota o modelo de **standalone operacional completo**.

Um grupo que possua apenas Novydres by Night MUST conseguir:

1. criar do zero qualquer personagem explicitamente suportado pelo suplemento;
2. compreender e executar o motor ordinário de V5;
3. resolver a condição vampírica estrutural;
4. utilizar qualquer opção mecânica publicada no suplemento;
5. conduzir uma crônica normal em Novydres sem consultar outra publicação para descobrir como uma mecânica necessária funciona.

Referências externas MAY existir para proveniência, expansão e leitura adicional, mas MUST NOT ser dependência operacional de uma regra ou opção publicada como suportada.

Standalone não significa reprodução enciclopédica indiscriminada de toda a linha V5. Entretanto, famílias de catálogo explicitamente abrangentes neste contrato possuem cobertura deliberadamente superior ao mínimo necessário para uma crônica ordinária.

## 4. Rules Inclusion Classification

Toda família, regra ou opção mecânica auditada SHOULD receber uma das seguintes classes de tratamento:

### 4.1 `FULL_RULE`

Regra ou subsistema explicado de forma autocontida e operacionalmente completa.

Uso típico:
- motor básico;
- sistemas vampíricos estruturais;
- procedimentos gerais;
- regras necessárias ao jogo continuado.

### 4.2 `FULL_OPTION`

Entrada mecânica selecionável apresentada com todos os elementos necessários para escolhê-la e utilizá-la, sem repetir os sistemas gerais dos quais depende.

Uso típico:
- Poder de Disciplina;
- Mérito;
- Falha;
- Vantagem;
- Antecedente;
- Tipo de Predador;
- opção equivalente de catálogo.

### 4.3 `ADAPTED_RULE`

Regra cuja forma em Novydres altera, estende, excepciona ou cria uma relação formal com o baseline V5.

A entrada MUST declarar sua relação conforme a Seção 13.

### 4.4 `OPERATIONAL_SUMMARY`

Resumo suficiente para resolver o escopo explicitamente coberto, sem reproduzir toda a profundidade, variantes, aconselhamento ou exemplos do material-fonte.

`OPERATIONAL_SUMMARY` MUST NOT ser usado quando a omissão de detalhes impedir o funcionamento de uma opção ou de uma situação estrutural coberta pelo suplemento.

### 4.5 `QUICK_REFERENCE`

Superfície abreviada de consulta.

MUST apontar para uma fonte autoritativa interna ou ser derivada dela.
MUST NOT ser a única definição de uma regra obrigatória ao standalone.

### 4.6 `EXTERNAL_OR_EXCLUDED`

Material não necessário ao funcionamento de nenhuma promessa operacional do suplemento e não admitido no corpus efetivo da edição.

Uma dependência necessária a uma opção publicada MUST NOT receber esta classificação.

## 5. Mandatory Mechanical Core

Novydres MUST manter dois conjuntos complementares:

### 5.1 Core universal obrigatório

O core universal MUST conter como `FULL_RULE`, no mínimo, o motor necessário para:

- composição de pools;
- dificuldades;
- sucessos e margem;
- testes simples;
- testes opostos;
- críticos;
- Messy Critical;
- falha;
- Bestial Failure;
- modificadores e penalidades;
- re-rolls e uso geral de Willpower;
- resolução física, mental e social ordinária;
- conflitos;
- dano superficial e agravado;
- Health;
- Willpower;
- impairment/incapacitação e recuperação;
- progressão/XP na profundidade necessária ao jogo continuado;
- Hunger;
- Rouse Checks;
- Blood Surge;
- Blood Potency;
- Humanity;
- Stains e Remorse;
- Frenzy;
- Compulsions;
- funcionamento geral de Disciplines;
- funcionamento geral de Advantages;
- Predator Type;
- criação de personagem e valores derivados.

### 5.2 Core condicional obrigatório

Novydres MUST aplicar **fechamento transitivo de dependências**.

Se uma regra, opção, personagem suportado, procedimento, subsistema ou adaptação publicada depender de outra mecânica para ser escolhida, criada, interpretada ou resolvida corretamente, a dependência também MUST receber tratamento interno suficiente.

Nenhuma `FULL_OPTION` MAY terminar em dependência exclusivamente externa.

## 6. Character Creation Contract

Novydres MUST fornecer duas rotas compatíveis:

1. **criação completa/guiada**;
2. **criação rápida**.

A criação rápida MUST ser uma interface acelerada sobre a mesma arquitetura mecânica da criação completa e MUST NOT introduzir um segundo sistema incompatível.

A criação completa/guiada MUST fornecer todos os procedimentos necessários para criar qualquer personagem suportado, incluindo, conforme aplicável:

- conceito;
- Ambição;
- Desejo;
- categoria/clã de personagem;
- geração;
- Blood Potency inicial;
- Atributos;
- Habilidades;
- Especializações;
- Disciplinas e Poderes iniciais;
- Advantages;
- Backgrounds;
- Merits;
- Flaws;
- Predator Type;
- Humanity;
- Convictions;
- Touchstones;
- Health;
- Willpower;
- Hunger inicial;
- Resonance quando mecanicamente necessária;
- aplicações de regras próprias de Novydres exigidas na criação.

O fluxo de criação MUST explicar **quando e como escolher/aplicar** uma opção, mas SHOULD referenciar o catálogo autoritativo em vez de duplicar integralmente cada entrada.

## 7. Disciplines and Powers Policy

Novydres MUST manter um **catálogo consolidado e normalizado** de Disciplinas e Poderes.

### 7.1 Cobertura

O catálogo MUST:

- consolidar as Disciplinas e Poderes oficiais presentes nas fontes V5 admitidas;
- admitir homebrews selecionados pelo processo editorial;
- organizar o conteúdo por estrutura mecânica, não por livro de origem;
- tratar cada poder admitido como `FULL_OPTION`.

### 7.2 Integridade operacional

Cada poder MUST conter, diretamente ou por dependência interna resolvida:

- nível;
- pré-requisitos;
- requisitos de Disciplina;
- Amalgam quando aplicável;
- custo;
- pool;
- oposição/dificuldade;
- duração;
- efeito;
- limitações;
- demais elementos necessários à operação.

### 7.3 Consolidação

Duplicatas, reimpressões e revisões MUST ser normalizadas em uma única entrada autoritativa quando forem a mesma opção mecânica.

Erratas e revisões oficiais posteriores SHOULD prevalecer sobre redações oficiais anteriores, salvo adaptação explicitamente aprovada de Novydres.

Homebrew MUST ser identificado como não oficial e MUST NOT substituir silenciosamente material oficial.

## 8. Advantages / Backgrounds / Merits / Flaws Policy

Novydres MUST adotar um **superset oficial consolidado + homebrews curados** para:

- Advantages;
- Backgrounds;
- Merits;
- Flaws;
- famílias mecânicas equivalentes;
- Especializações.

### 8.1 Presunção de inclusão

Uma opção oficial pertencente a uma fonte admitida SHOULD ser incluída.

Sua ausência MUST possuir justificativa objetiva baseada em pelo menos um dos critérios:

1. obsolescência ou substituição oficial;
2. incompatibilidade estrutural real com o produto;
3. duplicação mecânica efetiva.

Preferência temática, por si só, MUST NOT ser usada como justificativa para remover uma opção oficial válida do catálogo abrangente.

### 8.2 Especializações

Novydres MUST consolidar especializações oficialmente publicadas nas fontes admitidas e SHOULD fornecer vocabulário adicional próprio.

A lista de Especializações MUST ser tratada como expansível, não como lista universal fechada.

O produto MUST explicar os critérios para uma Especialização válida.

### 8.3 Homebrew

Entradas homebrew MUST registrar:

- natureza `homebrew`;
- fonte/autoria quando identificável;
- se usada sem alteração ou adaptada;
- pré-requisitos específicos de Novydres quando existirem.

## 9. Core Resolution Systems

Os sistemas ordinários de resolução MUST ser `FULL_RULE`.

Isto inclui resolução:

- física;
- mental;
- social.

Novydres MUST permitir que um Narrador transforme intenção ficcional em procedimento mecânico sem pressupor conhecimento prévio do livro-base.

Variantes opcionais, procedimentos raros não estruturais, aconselhamento extenso e exemplos adicionais MAY receber `OPERATIONAL_SUMMARY`, desde que o fechamento de dependências não exija cobertura superior.

Conflito social MUST receber profundidade operacional compatível com o foco político do cenário e com sistemas locais como Status e Prestações.

## 10. Vampire-Specific Systems

A condição vampírica estrutural MUST ser coberta como `FULL_RULE`, mesmo quando determinada ocorrência seja rara.

Isto inclui, conforme aplicável ao baseline admitido:

- Hunger e Hunger Dice;
- Rouse Checks;
- Blood Surge;
- Blood Potency;
- alimentação e saciedade;
- categorias/qualidades de sangue necessárias ao sistema;
- Resonance;
- Dyscrasia quando aplicável;
- Humanity;
- Convictions;
- Touchstones;
- Stains;
- Remorse;
- Frenzy;
- Compulsions;
- Banes das opções de Clã suportadas;
- Clan Compulsions das opções suportadas;
- Blood Bond;
- ghouls quando exigidos pelas opções publicadas;
- torpor;
- despertar do torpor;
- Final Death;
- diablerie;
- geração quando mecanicamente relevante;
- exposição ao sol;
- fogo;
- demais vulnerabilidades vampíricas universais necessárias ao jogo normal.

Baixa frequência MUST NOT, sozinha, justificar uma dependência externa.

Qualquer Clã admitido como opção jogável MUST ser mecanicamente operável sem consulta externa.

## 11. Novydres-Specific Mechanics Policy

Mecânicas próprias de Novydres MUST ser classificadas arquiteturalmente sem serem redesenhadas por este contrato.

Cada uma MUST:

- declarar sua relação com o baseline;
- declarar dependências;
- declarar localização autoritativa;
- declarar precedência;
- evitar divergência silenciosa.

Bairrismo, Marco Territorial, Status, Prestações e outras regras locais já aprovadas MUST ser preservadas em suas fontes autoritativas e posteriormente classificadas segundo este contrato.

A classificação individual dessas mecânicas é trabalho de implementação/auditoria e não requisito para alterar suas decisões materiais durante GAP-ARCH-001.

## 12. Official Sourcebook Admission Policy

Novydres adota política de **admissão ampla com inventário versionado**.

### 12.1 Política geral

Material mecânico oficialmente publicado para V5 é presumidamente elegível para consolidação.

A edição MUST manter um inventário versionado das fontes efetivamente avaliadas.

Cada fonte SHOULD possuir um estado entre:

- `ADMITTED`;
- `SUPERSEDED`;
- `PARTIAL`;
- `EXCLUDED`.

### 12.2 Significado dos estados

`ADMITTED`: a fonte integra o corpus mecânico relevante.

`SUPERSEDED`: a versão/fonte foi substituída por revisão, errata ou publicação posterior.

`PARTIAL`: somente famílias ou elementos especificados foram admitidos.

`EXCLUDED`: a fonte não integra o corpus, com justificativa registrada.

### 12.3 Novas publicações

Nova publicação oficial V5 MUST NOT alterar silenciosamente uma edição vigente de Novydres.

Ela MUST passar por revisão de admissão antes de modificar inventário ou catálogo.

### 12.4 Fontes especializadas

Cenários, crônicas, livros regionais, suplementos de facção e outras publicações oficiais MAY contribuir opções mecânicas ao corpus, mesmo quando regras não sejam seu foco primário.

## 13. Adaptation and Override Rules

Toda regra própria ou divergente de Novydres MUST declarar uma relação primária:

### `REPLACEMENT`

Substitui uma regra baseline dentro de escopo declarado.

Novydres prevalece no escopo da substituição.

### `EXTENSION`

Mantém o baseline válido e adiciona procedimentos, efeitos ou possibilidades.

### `EXCEPTION`

Mantém o baseline em geral, mas altera seu funcionamento sob condições explicitamente delimitadas.

### `NEW_SUBSYSTEM`

Introduz uma camada mecânica própria sem substituir diretamente um subsistema baseline equivalente.

### 13.1 Registro mínimo de adaptação

Cada `ADAPTED_RULE` MUST registrar:

- família/regra baseline afetada, se houver;
- relação primária;
- escopo;
- parte do baseline que permanece válida;
- precedência;
- dependências;
- localização autoritativa.

Na ausência de declaração explícita de adaptação, MUST ser presumido o baseline consolidado admitido pelo projeto.

## 14. Authoritative Rule Location Policy

Cada regra ou opção mecânica MUST possuir **uma única localização explicativa autoritativa** no produto.

A casa autoritativa MAY estar:

- no Capítulo 10;
- em capítulo temático;
- em catálogo especializado;
- em outro arquivo explicitamente designado.

A escolha MUST seguir função editorial e contexto, não uma regra de centralização absoluta.

Mecânicas cujo significado depende fortemente do contexto MAY permanecer autoritativas em capítulos temáticos.

## 15. Duplication and Cross-Reference Policy

Superfícies secundárias MAY conter:

- resumos;
- tabelas;
- lembretes;
- aplicações contextuais;
- referências cruzadas;
- quick reference.

Elas MUST NOT criar uma segunda implementação editorial independente da mesma regra.

Quando conteúdo completo precisar aparecer em múltiplas superfícies, SHOULD ser derivado de uma mesma fonte estruturada/autoritativa, evitando manutenção manual concorrente.

Referência interna SHOULD preferir localização estável e terminologia consistente.

Referência externa MUST NOT ser necessária para operar uma promessa mecânica do produto.

## 16. Chapter 10 Responsibilities

O Capítulo 10, **Regras do Sangue e da Cidade**, é responsável pelo núcleo sistêmico e pelo fluxo mecânico central do suplemento.

Ele MUST abrigar ou coordenar:

- motor geral standalone;
- condição vampírica estrutural;
- procedimentos gerais reutilizáveis;
- criação completa/guiada;
- criação rápida compatível;
- catálogos mecânicos cuja casa natural seja sistêmica;
- referências internas para regras autoritativas mantidas fora dele.

Ele SHOULD organizar o ensino de modo compatível com o fluxo gradual de criação de personagem.

O Capítulo 10 MUST NOT absorver automaticamente toda mecânica contextual do livro.

## 17. Character Creation Responsibilities

A criação é a superfície autoritativa do **procedimento de criação**, não uma duplicata de todos os catálogos.

Ela MUST:

- ordenar escolhas;
- explicar pré-condições;
- calcular valores derivados;
- apontar para opções autoritativas;
- garantir que ambas as rotas de criação cheguem a personagens mecanicamente compatíveis;
- aplicar dependências internas sem exigir livro externo.

Ela MUST NOT manter versões paralelas e divergentes de Powers, Merits, Flaws, Advantages, Predator Types ou outras opções.

## 18. Appendix / Quick-Reference Responsibilities

Apêndices e referências rápidas são superfícies de **lookup derivado**.

Eles MAY conter:

- tabelas;
- índices;
- matrizes;
- resumos;
- listas consolidadas;
- fluxos;
- referências cruzadas;
- quick-reference sheets.

Eles MUST ser construídos a partir de regras maduras.

Uma regra obrigatória ao standalone MUST NOT existir apenas em apêndice, exceto quando o conteúdo for intrinsecamente de consulta e a explicação autoritativa necessária estiver estabelecida em outra superfície interna.

## 19. Rules Reference DEU Relationship

DEUs de regras são superfícies derivadas e destacáveis.

Elas MAY:

- resumir uma fatia operacional coerente;
- reunir tabela e framing local;
- funcionar isoladamente dentro dos limites previstos pelo contrato de formato.

Elas MUST NOT:

- redefinir autoridade mecânica;
- criar variante acidental;
- duplicar integralmente capítulos apenas para obter independência;
- forçar uma família complexa inteira em uma única unidade.

Uma família complexa MAY requerer múltiplas DEUs.

O contrato exato de informação da Rules Reference DEU permanece **deferred** e MUST NOT ser silenciosamente resolvido por GAP-ARCH-001.

## 20. Dependency Matrix

A auditoria futura de cada família ou regra SHOULD registrar, no mínimo:

| Campo | Obrigatório |
|---|---|
| `rule_family` / identificador | MUST |
| necessária por Novydres? | MUST |
| necessária ao standalone ordinário? | MUST |
| dependências | MUST |
| tratamento de inclusão | MUST |
| localização explicativa autoritativa | MUST |
| superfícies abreviadas/cross-reference | SHOULD |
| modificada por Novydres? | MUST |
| tipo de adaptação, se aplicável | MUST |
| fonte baseline/proveniência | MUST |
| estado da fonte | SHOULD |
| pode o produto funcionar se omitida? | MUST |
| justificativa de exclusão, se aplicável | MUST |

### 20.1 Regra de fechamento

Se `pode o produto funcionar se omitida? = não`, a regra MUST NOT ser `EXTERNAL_OR_EXCLUDED`.

Se qualquer opção publicada falhar sem a regra, o tratamento MUST ser elevado até o nível necessário para eliminar a dependência externa.

## 21. Explicit Exclusions

Este contrato MUST NOT ser interpretado como autorização para:

- escrever o Capítulo 10 completo;
- redesenhar mecânicas V5;
- redesenhar regras locais já aprovadas;
- definir o layout final de DEUs;
- alterar a arquitetura geral do formato;
- criar novos Clãs;
- criar novas Disciplinas;
- criar NPCs;
- alterar lore;
- definir campanhas;
- aprovar homebrews individuais;
- escolher a lista concreta final de fontes oficiais;
- alterar o Registry;
- marcar GAP-ARCH-001 como `resolved`;
- selecionar o próximo gap.

## 22. Deferred Questions

As seguintes questões são deliberadamente deferidas porque não impedem o fechamento arquitetural:

1. inventário nominal completo de publicações oficiais V5 e estado de cada uma;
2. lista nominal de homebrews selecionados;
3. classificação individual de cada regra local de Novydres como `REPLACEMENT`, `EXTENSION`, `EXCEPTION` ou `NEW_SUBSYSTEM`;
4. lista concreta final de Clãs e demais categorias de personagem suportadas;
5. tratamento individual de opções oficialmente revisadas ou contraditórias;
6. taxonomia técnica final dos arquivos-fontes estruturados usados para gerar múltiplas superfícies;
7. contrato informacional exato das Rules Reference DEUs;
8. conteúdo final e paginação do Capítulo 10;
9. conteúdo final dos Apêndices;
10. classificação final de coterie creation: se o produto a prometer como parte da criação suportada, ela MUST receber cobertura interna suficiente pelo fechamento de dependências.

Nenhuma dessas questões altera a definição de standalone, as classes de inclusão ou a política de dependências aqui aprovadas.

## 23. Risks

### 23.1 Rules expansion pressure

O catálogo abrangente pode pressionar volume e manutenção.

Mitigação:
- consolidação;
- normalização;
- fonte autoritativa única;
- derivação de superfícies;
- exclusões justificadas apenas por critérios objetivos.

### 23.2 Source drift

Novas publicações V5 podem alterar o corpus.

Mitigação:
- inventário versionado;
- revisão explícita de admissão;
- ausência de atualização automática silenciosa.

### 23.3 Duplicate-rule divergence

Criação, capítulos, apêndices e DEUs podem divergir.

Mitigação:
- localização autoritativa única;
- superfícies derivadas;
- cross-reference estável.

### 23.4 Hidden external dependency

Uma opção aparentemente completa pode depender de mecânica ausente.

Mitigação:
- fechamento transitivo de dependências;
- matriz auditável por família/regra.

### 23.5 Homebrew provenance confusion

Material não oficial pode ser confundido com material V5 oficial.

Mitigação:
- metadados explícitos de proveniência;
- proibição de substituição silenciosa.

### 23.6 Local-rule precedence ambiguity

House rules podem conflitar com baseline sem precedência clara.

Mitigação:
- relações normativas `REPLACEMENT`, `EXTENSION`, `EXCEPTION`, `NEW_SUBSYSTEM`.

## 24. Closure Test for GAP-ARCH-001

GAP-ARCH-001 pode ser considerado candidato a fechamento editorial quando o chat editorial principal confirmar que este contrato fornece evidência versionada suficiente para:

- enumerar o core mecânico obrigatório;
- estabelecer fechamento de dependências;
- definir classes de inclusão/exclusão;
- definir a política de catálogos amplos;
- definir a política de fontes oficiais e homebrew;
- definir adaptações e precedência;
- definir uma fonte autoritativa por regra;
- separar responsabilidades entre Capítulo 10, criação, capítulos temáticos, apêndices e DEUs;
- permitir auditoria objetiva de qualquer família mecânica.

### Closure Evidence

> Contrato versionado aprovado que enumere o core obrigatório, critérios de inclusão/exclusão, política de adaptações locais e relação com criação/apêndices.

### Registry Handoff

Se e somente se o chat editorial principal aprovar uma versão deste contrato como evidência de fechamento, uma atualização futura e separada do Registry SHOULD:

- alterar GAP-ARCH-001 para `resolved`;
- apontar `resolution_source` para o contrato aprovado;
- registrar histórico de auditoria compacto;
- reavaliar os gaps bloqueados por GAP-ARCH-001.

Este documento MUST NOT executar essa mutação.

**READY_FOR_EDITORIAL_CLOSURE_REVIEW**