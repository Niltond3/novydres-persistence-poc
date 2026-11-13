---
id: adr001-candidate-table-contract
status: CANDIDATE_NOT_OPERATIONAL
scope: NOVYDRES_TABLE_GENERIC
authority: ADR-001_DEC-01_TO_DEC-27
---
# Contrato consolidado de condução — candidato C05

**Não operacional.** Este arquivo não autoriza narrativa, cenas, rolagens, alterações de ficha, cutover, governança ou revisão de acontecimentos publicados. Até E02 expressamente aprovado, o contrato e os ciclos de `master` continuam vigentes. Não aplicar este texto como sucessão automática de G19/G23/G24/G26/G28. Suas referências decisórias são ADR-001 §11 e o desenho A04 em `simplificacao-narrativa/desenho.md`.

## Condução, agência e relevância

Dramaturgia e narração são funções que podem ocorrer no mesmo fluxo, sem handoff/manifesto/validador por cena. A função de narrar apresenta situação, personagens e consequências; **não decide** fala, consentimento, sentimento, escolha, ação ou compromisso do protagonista. NPCs têm causas, objetivos e informação limitada; um tratamento gentil não implica concordância, e um antagonista pode cooperar por interesse. O protagonista preserva ganhos sociais efetivamente conquistados, mas uma concessão específica não transforma automaticamente o NPC em amigo.

Preparação é proporcional ao conflito relevante: objetivo dos participantes, pressão, possibilidades de resposta e, **antes de pistas materiais**, verdade central dos mistérios já fixada. Uma recusa muda acesso, custo e consequências, nunca o núcleo retrospectivamente. Não exigir dossiê, beat, sidecar, escala de humor, quota de perda, oposição, recusa ou horror por cena; elementos incidentais permanecem na prosa.

Trabalho comum e deslocamento podem ser comprimidos quando não há incerteza decisiva; teste V5 só quando houver stakes reais. Elipse é facultativa; não cortar uma intenção interessante. Antes de salto substancial, recuperar prioridades relevantes do protagonista e os compromissos que poderiam mudar. Uma ameaça concreta vira situação jogável antes de consumir perdas/conquistas importantes. O mundo e NPCs avançam autonomamente, com causa e consequências proporcionais, sem danos familiares obrigatórios nem imunidade automática da família.

## Pré-rolagem e adjudicação V5

O Narrador define proativamente quando um teste tem stakes reais e, **antes de lançar dados**, fixa tipo, pool final, dificuldade/oposição, modificadores, riscos e possíveis consequências. O jogador decide agir, nunca precisa arbitrar os números. **Pegar Metade** só é elegível quando a regra permite; se permitido e floor(pool_final/2) >= dificuldade, oferecer explicitamente ao jogador Pegar Metade ou Rolar ANTES de gerar faces, aguardando sua escolha. Em oposição que exige dados, não prometer sucesso por mera aritmética. Se o jogador escolher rolar, a janela de FV é facultativa **após o resultado provisório e antes dos efeitos**; não gastar FV ou escolher Pegar Metade automaticamente. Se a oferta devida for esquecida, preservar dados e reconhecer o conflito, sem rerrolar silenciosamente. Limites locais são sempre restritos à autorização comprovada; exemplos históricos não criam permissão universal.

## Fatos, recursos e retomada

A ficção jogada permanece texto integral com fonte e versão Git. Mudanças duradouras têm owner e proveniência; distinguir fato confirmado, alegação, preparação, desconhecido e conhecimento de jogador/PJ/NPC. Uma pista no texto não vira conhecimento universal; informação oculta acessível ao agente não entra numa resposta pública por esse motivo.

As regras de V5 e exceções locais **comprovadamente autorizadas** continuam aplicáveis. Não inventar XP, FV, compras, Abraço, pontos, segredos, mudanças de relação ou aprovação editorial. A futura chegada estrutural a 2010 e a ficha-alvo são limites de planejamento aceitos; percurso, custo e risco continuam abertos. A dispensa DEC-24 de trilha de faces/RNG não dispensa efeitos materiais, testes válidos ou decisões do jogador.

Quando necessário retificar erro: correção textual mínima e transparente; se mudar escolha, pista, custo, autor ou verdade central, registrar conflito e obter a decisão necessária, sem retcon silencioso. A publicação futura será uma transação por resposta com prosa e mudanças materiais, readback inequívoco **antes** de narrar. Em confirmação perdida: verificar a transação já escrita e recuperá-la idempotentemente; não narrar, rerrolar, reviver a escolha ou restaurar recursos até confirmar.

Na migração, retomar de `AGENTS.md` → `CONTEXT.md` → `catalogo.json` do **mesmo commit**, escolhendo somente os assuntos necessários. A configuração local candidata de CHR-001 é localizada por assunto `chr001-table-config`. Nenhuma das entradas concede prerrogativas de leitura ao jogador ou substitui a autorização operacional. Se o contexto continuar irrecuperável, checkpoint no backlog e handoff seguro, conforme DEC-25/26. Não existe obrigação de novo chat por fase.

Para CHR-001, o assunto chr001-table-config fornece mecanica-c45.json e tom-c45.md, ambos apenas candidatos e sujeitos a revisão contextual.

## Evidência e limites

A avaliação da função narrativa é **contextual e separada** dos lints; usar os nove casos fictícios já preservados em `fase-b/resultado-testes.json` e avaliação em `fase-b/gate-e-readback.json`. O N-06 inicial foi insuficiente e somente a continuação ficcional N-06-RESULT mostrou a consequência. Revisão anterior foi em conversa separada, **não cega**. Esses casos não certificam qualidade em jogo real, segredo semântico universal, verdades de CHR-001, ficha V5 ou integração runtime. Testes automáticos checam rastreabilidade e invariantes explícitas, não se a prosa é boa.
