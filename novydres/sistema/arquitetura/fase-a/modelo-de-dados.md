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
