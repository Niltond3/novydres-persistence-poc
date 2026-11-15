---
document_id: CONTRATO-PROPAGACAO-ATLAS
status: EMENDA_APROVADA_2026_11_15
subject_id: world-atlas-novydres
visibility: PLAYER_SAFE
source_snapshot: 7ce8e88c122a5d80879e30a23b1f3be159cac727
created_on: 2026-11-14
---

# Contrato de fechamento e propagação canônica — Atlas

## 1. Regra: zero autoridade operacional concorrente

**Uma decisão não é canônica quando só recebe um número de ticket, um OK textual ou uma nova geometria.**

O estado `CLOSED_CANON` requer simultaneamente:

1. Resolução substantiva por aprovação expressa do proprietário, com escolha final, escopo e data/ano de vigência.
2. Registro do fato no **assunto proprietário**, com ID estável, fonte da aprovação, estado epistêmico adequado e geometria quando aplicável.
3. Reconciliação do **universo de consumidores pertinentes**: referências de sujeitos relacionados, mapas, listas, entidades, índices e versões pública/restrita. Uma projeção nunca vira verdade separada.
4. Prova negativa: **nenhuma fonte vigente e operacional** responde com valor incompatível para o mesmo atributo, lugar e período.
5. Validação do impacto em episódios/eventos: acontecimentos jogados não podem ser retificados ou divulgados sem autorização separada.
6. Um commit Git atômico do pacote lógico (ou pacote coordenado que não exponha estado canônico intermediário incoerente), aplicado com parent esperado, `force=false`, e readback de ref/tree/blobs. Se depender de material alheio não autorizado, a decisão fica `APPROVED_PENDING_PROPAGATION`, não `CLOSED_CANON`.
7. Build/checks e exportações derivadas geradas ou marcadas como pendentes; falha material bloqueia fechamento.

**Emenda do proprietário (15/11/2026):** nenhuma versão editorial obsoleta pode permanecer nos arquivos correntes depois do fechamento. Remover documentos substituídos do HEAD, eliminar referências correntes e manter o histórico anterior somente em commits Git. A proposta vigente para fatos não aprovados também deve ser única. Se ainda houver dependência quebrada ou conflito operacional, o status é `APPROVED_PENDING_PROPAGATION`, jamais `CLOSED_CANON`.

## 2. Ciclo formal de cada GEO

`OPEN_EVIDENCE` → `RECOMMENDED` → `OWNER_APPROVED` → `PROPAGATING` → `CLOSED_CANON`.

Estados alternativos: `BLOCKED_CONFLICT`, `REOPENED`, `REJECTED`. Não confundir este fluxo editorial com o `CONFIRMED/NPC_CLAIM/GM_PREPARED/CONDITIONAL/UNKNOWN` do conhecimento do mundo; são dimensões separadas.

Pacote mínimo de decisão:
- ID GEO, pergunta, alternativas, resposta aprovada em termos inequívocos, definição de 2010 e demais períodos;
- fontes/linhas comparadas e motivo de precedência; escopo de público/privado;
- lista calculada e revista de entidades próprias e consumidores;
- diff de arquivos, testes, resultado do verificador de autoridade e SHA de commit publicado;
- estado `CLOSED_CANON` **somente após readback e prova de não concorrência ativa**.

## 3. Matriz de proprietários e propagação

| Tipo de alteração | Fonte autoritativa a atualizar | Referências/consumidores a reconciliar | Não editar sem autorização específica |
|---|---|---|---|
| Extensão, costa, hidrografia, Ermo, redes e geometrias | `cenario/atlas-novydres/cartografia/` | `atlas-novydres/index.md`, raions, POIs, mapas técnicos, atlas público, scripts/índice | Cenas históricas ou conhecimento situado |
| Limite, nome, função e população do raion | `cenario/geografia/district-*/` + geometria referencial do Atlas | Os nove raions, lugares internos, política, transportes, resumos e visualizações | Fontes obsoletas retiradas da árvore corrente; histórico apenas no Git |
| Identidade/nome/função de instituição/POI | `cenario/lugares/poi-XX/` (ou novo assunto adequado) | Registro do Atlas por ID, raion, redes, legenda, atividades do operador, visão pública/privada | Fatos ficcionais fechados em crônica |
| Organização, domínio, seita, pacto, influência territorial | `cenario/politica-global/` ou `cenario/organizacoes/<id>/` conforme owner | Raion, indicadores territoriais, atlas de domínio, NPCs envolvidos e direitos de acesso | Arquivos de lore histórico literal |
| Identidade/status duradouro e poder de NPC global | `personagens/<subject_id>/` | Organizações, influência por território, lugares, atlas restrito, índices | Atos/estados de campanha pertencentes à crônica |
| Ação, posição, conhecimento e hipótese surgidos em cena | `cronicas/CHR-001/` no assunto apropriado | Projeção temporal compatível, referências geográficas se aprovadas, mapa conforme visibilidade | Reinterpretação retroativa da prosa ou revelação de segredos |
| Conceitos e regras de cartografia | `cenario/atlas-novydres/cartografia/`; ADR para decisão arquitetural | Schemas/validadores/testes, índice/catalogo derivados, renderizações | Gateway de runtime sem necessidade e autorização |
| Nome, fonte e exposição de camadas públicas | Dado no owner + estilo/manifest de exportação | Site, SVG/PNG/PDF, arquivos cacheados/publicados | Informações `SYSTEM_AUDIT` ou de narrador em saída pública |

**Catalogação:** `novydres/catalogo.json` é gerado, não uma segunda autoridade. O índice de dependentes explícitos de `world-atlas-novydres` contém os nove `district-*` e os 32 `poi-*`. Mas o inventário textual de relações indiretas entre histórias, organizações, NPCs e bibliografia também deve ser revisado.

## 4. Validação material exigida

A validação atual do repositório possui `novydres/scripts/validar-assuntos.mjs` e `catalogo-assuntos.mjs`, e workflows do ADR-001; **não está comprovado** que eles validem geometrias ou todos os consumidores semânticos. Não atribuir-lhes competência inexistente.

Antes do primeiro fechamento real, implementar/validar conforme necessário:

- `canon-one-owner`: um atributo/escopo/período possui um único owner e sua fonte vigente;
- `refs-resolvable`: ids de raion, POI, organização, NPC, lugar, linha, estação e geometria resolvem;
- `active-source-coherence`: documentos operacionais correntes não discordam do fato fechado;
- `topology-networks`: estradas, ferrovia, metrô, acessos e hidrografia coerentes; viadutos não viram entroncamentos falsos;
- `facility-coverage`: instalações referidas por legenda ocupam posição e possuem acessos/capacidade adequada à escala;
- `scenario-temporal`: eventos históricos e estado narrativo preservados;
- `disclosure`: saída pública sem informação restrita, incluindo nomes e limites de influência;
- `render-equivalence`: cada tile ou zoom usa as mesmas feições/IDs, não outra imagem independente.

A verificação deve ser **orientada a falhas materiais**, não cria gate artificial por quantidade de arquivos.

## 4.1 Aplicação da fonte única ao Atlas

`atlas-proposta.md` é a única proposta corrente para os nove raions e 32 POIs. `populacao-2010.json` é a única fonte do censo municipal de 2010. `localizacao-geral-2010.json` é a única fonte da região geral aprovada. Cópias substituídas do Atlas e seus índices de custódia foram retirados do HEAD; os 41 assuntos associados possuem uma única projeção da proposta. Os verificadores devem auditar origem antiga somente pelo commit histórico, nunca exigir cópias obsoletas no HEAD.

## 5. Critério de prontidão para geração de imagens

Para cada região e escala da imagem final:

- decisões substantivas relevantes `CLOSED_CANON`;
- geometrias, redes principais e instituições correspondentes aprovadas;
- sem conflitos de autoridade ativa;
- áreas sem dados classificadas explicitamente como `não renderizar` ou detalhe procedural sob regra aprovada;
- saída pública/restrita aprovada;
- ferramenta gera mapa técnico determinístico que pode ser auditado por entidade e posição.

Até esses itens: **não** produzir imagens finais nem se valer de imagens anteriores para preencher lacunas. Protótipos técnicos sintéticos podem servir para testar pipeline e não são cânone.

## 6. Fontes nucleares e evidência de precedência

- `novydres/AGENTS.md`, `CONTEXT.md`, `catalogo.json` em `7ce8e88c122a5d80879e30a23b1f3be159cac727`.
- Atlas histórico `cenario/atlas-novydres/atlas-proposta.md`, `atlas-proposta.md` e `registro.json`.
- `cenario/geografia/district-*/conteudo.json`; `cenario/lugares/poi-*/conteudo.json`.
- `cenario/politica-global/fonte-001..003.source.md`; `cenario/historia-global/fonte-001..002.source.md`.
- `cenario/organizacoes/escala-de-poder/`; `personagens/` e `cronicas/` por dependência situacional.
- PRD e ADR-002 aprovados **para planejamento** na branch documental, não como licença para resolver fatos de lore.

**Estado desta versão:** proposta de governança suplementar. Não modifica ADR-001 nem canoniza geografia.
