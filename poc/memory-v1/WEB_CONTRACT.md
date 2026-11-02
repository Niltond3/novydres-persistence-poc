# Contrato operacional experimental — ChatGPT Web (POC, não vigente)

## 0. Alcance
Esta especificação **não substitui** .AGENT.md V3, .CONTEXTG V2.0, DEC-CR-014, EVENT_PROTOCOL_V2 nem qualquer material CANÔNICO/FECHADO. Ela só poderá se tornar operacional para CHRONICLE_001 após autorização expressa e reconciliação da migração. Um usuário, uma sessão por vez; sem mecanismo de lock distribuído.

## 1. Bootstrap em conversa nova
1. Recuperar a governança válida e metadados de autoridade; não inferir que uma cópia no GitHub é aprovada porque existe.
2. Ler LIVE.json (estado, último event_id, sha, pending e apontador de cena).
3. Ler SCENE_CONTEXT.md se o apontador de contexto estiver ativo e a evidência/versão for coerente.
4. Se a cena, NPC, conflito ou promessa exigir mais contexto, ler HISTORY_INDEX e as memórias necessárias; para fatos sensíveis/ou contraditórios, abrir o evento original.
5. Verificar que o contexto está atualizado frente aos eventos do LIVE e que nenhuma lacuna causal relevante permanece. Se faltar prova: UNKNOWN / NEEDS_EVIDENCE; não inventar.

## 2. Contexto recuperado por relevância (sem ferramenta de busca externa)
A) Extrair entity_ids, location_ids, arc_ids, relação/tema e intenção do turno. B) Tomar o subconjunto de IDs no índice por correspondência explícita primeiro; aliases/tags apenas como fallback. C) Cobrir threads abertas, promessas e NPCs presentes. D) Abrir perfis/arcos por caminhos explícitos. E) Se uma afirmação for contestada ou de grande consequência, abrir a fonte integral citada. F) Preparar pacote SCENE_CONTEXT com fatos, claims, desconhecidos, causalidade, conhecimento por ator, refs de fontes e limites de agência.

A ausência de informação no índice **NÃO** prova que o fato não aconteceu: consultar arquivos originais ou marcar lacuna. Não confiar em code search do GitHub como índice primário; pode estar indisponível/desatualizada.

## 3. Turno normal
1. Usar LIVE da última verificação **somente se conteúdo e sha ainda presentes no contexto desta conversa**; se não, reler LIVE.
2. Classificar declaração/intenção/NPC_CLAIM/WORLD_EVENT/MECHANICAL_RESULT; distinguir conhecimento de cada ator.
3. Preparar delta + texto narrativo, sem responder ainda. IDs de evento estáveis, não duplicar; decisões do PJ exclusivas do jogador.
4. Gravar apenas LIVE.json via update_file com blob SHA da versão conhecida. O texto substitui o arquivo pequeno completo; Git guarda histórico em commits.
5. Conferir resposta e **fetch_file de readback** validando event_id, dados alterados e campos não afetados. Só depois narrar.
6. Se erro antes de confirmação, reler LIVE para identificar se event_id já está presente. Nunca rolar novamente por falha de persistência. Se persistir dúvida: PENDING_PERSISTENCE.

## 4. Rolagens e agência
Se existe uma escolha de FV pendente, gravar estado ROLL_PENDING com faces e decisão ainda aberta; não declarar efeito final antes de o jogador optar. Em novo turno, encerrar a rolagem sem gerar novos dados por causa de retry. Registrar faces, pool, dificuldade, modificadores, resultado, escolha do jogador, gasto e delta como registro operacional; **não promover retroativamente o CHRONICLE_STORE_V0_2 vazio a COMMITTED técnico**.

## 5. Transição de cena
1. Recuperar HISTORY_INDEX se não disponível na conversa; identificar temas, atores e consequências pendentes.
2. Buscar o mínimo suficiente para explicar conhecimento, causalidade, relações e obrigações.
3. Preparar SCENE_CONTEXT derivado com source_event_ids. Atualizar LIVE + SCENE_CONTEXT em **um commit Git atômico** (tree, commit, ref) e fazer readback dos caminhos relevantes.
4. Se rotações/histórico foram afetados, incluir lotes e índice no mesmo commit; verificação obrigatória antes de continuar.

## 6. Arquivamento
Gatilhos PROVISÓRIOS: LIVE >30 mil caracteres OU >20 eventos no buffer, além de fechamento de episódio. Salvar blocos integrais antes de retirá-los do buffer. Manter IDs estáveis e ordem; eventos corrigidos por CORRECTION, nunca apagados. Rotação: um commit com arquivo(s) de arquivo histórico + LIVE atualizado + HISTORY_INDEX atualizado, evitando janelas de sincronização parcial.

## 7. Erros e conflitos
Fato contraditório entre fontes => CONFLICT, registrar versões e pedir decisão se requerido por governança. Resumo não supera fonte verificada. Chat não tem relógio/cache confiável entre sessões; não assumir que o agente sempre lembrará regras ou dados. Segredos do narrador ficam fora do pacote visível ao jogador; a separação documental ajuda, mas por si só não assegura sigilo perfeito no mesmo modelo.

## 8. Proibição operacional
Não migrar CHRONICLE_001, não alterar Drive, não editar CANÔNICO/FECHADO ou APROVADO/CONGELADO, não promover esse contrato, não gerar eventos reais a partir das fixtures, não narrar pela POC.
