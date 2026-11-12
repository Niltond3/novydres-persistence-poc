---
id: arch-phase-a-data-model
status: CANDIDATO_PENDENTE_APROVACAO
scope: NOVYDRES_GLOBAL
classification: PLAYER_SAFE
---
# Modelo de dados e ontologia verificável (candidato)

## Orientação da revisão
Revisado documentalmente em 2026-11-11 conforme [ADR-001 §11, DEC-16/DEC-17/DEC-23/DEC-24](../adr/001-subject-oriented.md#11-revisão-do-harness-narrativo). As decisões aceitas na entrevista precedem a formulação anterior deste modelo; esta revisão não reescreve a aprovação histórica de A nem ativa schemas ou candidatos de B.

## Limite entre prosa e dados estruturados
Exigir representação estruturada para fatos duradouros que afetem estado, recursos, relações, conhecimento, pistas, decisões ou compromissos. Detalhes incidentais permanecem no texto integral recuperável da cena; não recebem obrigatoriamente assertion, evento, subject ou arquivo próprio. A classificação depende do efeito na ficção, não de uma quota de registros.

Se um detalhe incidental se tornar relevante, recuperar o trecho original e registrar sua fonte, tempo e quem efetivamente poderia conhecê-lo antes de utilizá-lo como dado estruturado. Isso registra um fato já narrado, não um acontecimento novo nem um retcon. Se a fonte for ambígua, preservar a incerteza e aplicar a regra de correção material; não completar o passado por inferência. Ausência no índice estruturado não prova que algo não aconteceu. Não normalizar retrospectivamente toda a prosa para executar essa recuperação.

## Entidades e vínculos
Subject: {subject_id, kind, owner_scope, status, visibility, source_refs[], source_assertions[], related_subject_ids[], schema_version}. Tipos: world-location, history-topic, organization, lineage, character, chronicle, story, plot, thread, episode, scene, beat, event, decision, approval, correction, source, orchestration-cycle. Um subject pode ter documentos opcionais; não exigir placeholders para tipo sem dados.

Chaves de referência: ref por {id, kind, scope, source_commit?}; normalizar para ID em índices e conteúdo. Relações: {relation_id, from_subject_id, to_subject_id, predicate, owner_subject_id, scope, valid_from?, valid_to?, source_record_ids[], epistemic_status, visibility}. relation_id, direcionalidade, âmbito, tempo e dono obrigatórios. Inversa derivada; grau de confiança não autoriza mesclar NPCs homônimos.

Afirmação estruturada, quando exigida pelo limite acima: {assertion_id, subject_id, field, value, epistemic_status, attribution_actor_id?, evidence_refs[], valid_time, recorded_time?, visibility, owner_scope}. O envelope não é obrigação por frase da narrativa. Status: CONFIRMED, NPC_CLAIM, GM_PREPARED, CONDITIONAL, UNKNOWN; categorias de evento ainda distinguem PLAYER_DECLARATION, PLAYER_INTENT, NPC_ACTION, WORLD_EVENT, GM_PROPOSAL, CANON_SOURCE, MECHANICAL_RESULT. UNKNOWN não vira false, e ausência de registro não vira UNKNOWN estabelecido.

Conhecimento separado: AGENT_KNOWLEDGE (material acessível a agentes com função), PLAYER_KNOWLEDGE (revelado ao usuário), PC_KNOWLEDGE (visto pelo PJ), NPC_KNOWLEDGE (por indivíduo e tempo); cada item tem assertion_id, actor_id, as_of_source_ref e evidence/ref. Acesso de agente não implica divulgação ao jogador, nem conhecimento ficcional de personagem. Visibility inclui PLAYER_SAFE, PC_KNOWN, NPC_BELIEF, GM_HIDDEN, SYSTEM_AUDIT; classificações são filtros editoriais, NÃO controle de acesso Git.

## Hierarquia narrativa e estado atual
- chronicle, story, plot/thread, episode e scene organizam o conteúdo quando úteis; scene pode referenciar beat condicional. Não criar unidade ou arquivo vazio para completar a hierarquia.
- plot/thread pode cruzar episódios, tem dono, estado com fonte e dependências relevantes; o fechamento de uma cena não encerra automaticamente um fio.
- Fato narrado é recuperável pelo texto da cena/trecho e commit. Um registro adicional de evento só existe quando tiver função concreta; não é requisito para atualizar relações, conhecimento, pistas ou intenções.
- estado/atual.json, ou documento equivalente do assunto proprietário, é o estado corrente autoritativo, atualizado na mesma transação do texto e dos efeitos materiais. Contém o mínimo para retomar: situação, tempo conhecido, recursos/ficha, última intenção e pendências relevantes; dados de outros donos são referenciados. Não é projeção obrigatória de um ledger universal nem depende de motor de replay.
- decisões e aprovações preservam autoridade, escopo, conteúdo e fonte histórica. Correção explícita aponta para o registro ou trecho afetado, com motivo e efeito, conforme DEC-14. Não precisa de um arquivo por correção se a referência e a rastreabilidade forem preservadas.
- Em inconsistência material, conciliar estado, texto e histórico Git antes de confirmar a informação; não fabricar o elo ausente nem reescrever o passado silenciosamente. Recuperação técnica preserva os fatos posteriores já jogados, sem restaurar recursos antigos por conveniência.

## Rolagens: consequência suficiente
DEC-24 dispensa faces individuais, pool transcrito, seed, trilha RNG e registro técnico por rolagem. Para persistência, basta o que aconteceu na ficção e os efeitos materiais correspondentes. Exemplo de fixture, sem evento de campanha: uma tentativa frustrada deixa o personagem ferido e sob suspeita; registrar a consequência e o estado pertinente, sem a sequência de dados que a produziu.

Não se exige reconstituir nem certificar retrospectivamente testes. As regras V5, stakes e adjudicação já aceitos continuam aplicáveis; a dispensa é de auditoria/persistência dos dados, sem nova exceção mecânica implícita. Resultados históricos já registrados permanecem como fontes, sem exigir nova estrutura nem alegar verificação aleatória ausente. Nunca rerrolar para completar um registro ou para recuperar uma gravação.

## Registro físico Git-native
Nomes correntes estáveis e revisão pelo Git. Não impor arquivo por evento, dado ou mudança de estado. A02 define a organização por coesão e recuperação; registros adicionais de decisão, aprovação, correção ou transação só existem quando necessários, com fonte/identidade suficiente para referência e idempotência. Índices e catálogo são derivados, sem segundo dono do estado.

O texto jogado e as fontes históricas permanecem preservados; correções são explícitas. COMMITTED exige publicação e readback da transação: arquivo preparado não comprova persistência. A implementação define o mínimo necessário para reconhecer uma transação já aplicada e recuperar confirmação perdida, sem recriar um ledger narrativo completo. Proteções Git não são garantia física absoluta contra um administrador reescrever o histórico.

História textual literal não é reconstruída a partir de resumo. Um arquivo histórico com variante de conteúdo exige classificação de autoridade/conflito e proveniência; não produzir evento técnico ou prova RNG para preencher lacuna. A migração preserva fontes, não exige converter todo o passado em eventos.

## Schemas e normalização
Os dois JSON Schema existentes ao lado são candidatos da baseline anterior, ainda não atualizados por esta revisão documental. A02/C01 devem adequar apenas os formatos efetivamente usados: assuntos, estado, relações/conhecimento e identificação de transações quando necessária. Retirar exigências herdadas de ledger universal, replay e roll por dado. Não criar schema por cena, beat ou teste sem função demonstrada. Validar referências e tipos sem coerção silenciosa. Nenhum schema é instalado ou ativado nesta etapa.

## A02 — Execução de desenho (2026-11-12; NÃO OPERACIONAL)

Fontes: ADR-001 DEC-16/17/23/24; A01 em `auditoria-e-mapa.md`. Estes limites substituem a parte excessiva do envelope anterior **somente no candidato**, sem alterar master, cânone ou fatos. Os schemas JSON adjacentes foram ajustados; validação real em B/C continua pendente.

| Classe de informação | Proprietário e representação mínima | Proibição |
|---|---|---|
| Identidade global de NPC | `personagens/{id}`, proveniência e status editorial | Duplicar perfil em cada crônica ou promover NPC_CLAIM a fato global |
| Conhecimento, relação e ação local | `cronicas/{id}/elenco/{npc-id}` ou seu assunto proprietário; ator, fonte, tempo e estado epistêmico | Atribuir conhecimento a outro NPC ou ao PJ só porque o agente leu a fonte |
| Mundo, organizações e regras | `cenario/`, `sistema/regras/` e decisões editoriais autorizadas | Promover material `candidate`/homebrew a cânone por renomeação |
| Preparo e evento futuro | `cronicas/{id}/tramas`/`preparacao`, `GM_PREPARED` ou `CONDITIONAL` | Tratar preparação como cena jogada, resultado ou XP concedido |
| Estado, recursos, escolhas e pistas duráveis | Texto integral e delta no único owner correspondente, com proveniência | Criar arquivo por dado/rolagem/beat ou ledger/replay universal |
| Detalhe incidental | Prosa integral recuperável pelo path + commit + localização textual | Exigir assertion/arquivo por frase, ou inferir ausência do fato por ausência de campo |
| Decisão, aprovação ou correção | Registro referenciável apenas quando necessário, com autoridade/efeito/fonte | Sobrescrever originais, dispensar autoria ou inventar hashes |
| Índices, catálogos e espelhos | Derivados determinísticos por snapshot | Fonte de verdade concorrente |
| Mídia e fontes externas | Link/ID, direitos e integridade observada em `fontes/` | Presumir bytes ou SHA externo não verificável |

**Granularidade:** uma fatia existe quando há assunto real e recuperação seletiva útil. `index.md` e arquivos por tipo são opcionais segundo necessidade, nunca um formulário completo por NPC, cena, beat ou teste. O limite de documento é sua coesão e custo de recuperar um fato, sem quota fixa de linhas/tokens. Relações usam ID, direção, âmbito temporal, owner e fonte; inversas são derivadas. Campos globais e locais não têm segundo dono. `schema_version` é formato, não revisão; o commit Git versiona documentos correntes. A ausência de `source_refs` no envelope vazio é sintaticamente aceita, mas **fatos duradouros CONFIRMED exigem fonte localizável** pela validação semântica de C01; uma fonte externa sem hash usa ID/URL e integridade desconhecida.

**Casos para C01/B (fixtures abstratas, não acontecimentos de CHR-001):**
1. Positivo — uma cena fictícia contém um símbolo no casaco apenas na prosa. Quando virar pista durável, a consulta localiza o trecho original por path/commit; a anotação posterior preserva quem realmente o viu e não cria acontecimento retroativo.
2. Positivo — uma alegação feita por NPC em crônica permanece `NPC_CLAIM` e conhecida somente por fontes/ouvintes comprovados, enquanto o perfil global do NPC continua independente.
3. Positivo — um acontecimento preparado continua `GM_PREPARED` até fonte de realização; eventual recusa do PJ não vira execução implícita.
4. Negativo — rejeitar converter hipótese, claim, simulação ou capítulo `candidate` em `CONFIRMED` ou APROVADO sem fonte decisória.
5. Negativo — rejeitar conhecimento telepático entre membros de organização e duplicação de owner de relação/recurso.
6. Negativo — ausência no estado exige busca na prosa, jamais resposta conclusiva de que o detalhe não ocorreu.
7. Negativo — não exigir `ROLL`, faces, seed, replay ou auditoria RNG para aceitar consequências materiais preservadas; não apagar fontes históricas de teste.
8. Negativo — fonte não localizada retorna `NOT_FOUND`/`UNKNOWN`, sem fallback fuzzy ou SHA fabricado.

**Limite de prova A02:** exemplos classificam fronteiras e ambos os schemas candidatos são JSON válido. Ainda não foram executados testes de instância, recuperação Web/Codex, CI nem equivalência factual integral. A02 não substitui C01/C02.
