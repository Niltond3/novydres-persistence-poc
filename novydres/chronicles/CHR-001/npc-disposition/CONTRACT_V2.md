# CHR-001 / NPC DISPOSITION — CONTRACT V2: AUTONOMIA, ATRITO E ASSIMETRIA
STATUS: ATIVO PROSPECTIVAMENTE APÓS PUBLICAÇÃO ATÔMICA COM MANIFEST_V42 + CYCLE_V0020. Escopo ESTRITAMENTE CHR-001; substitui somente o preflight interpretativo de CONTRACT_V1.md, sem alterar fórmula, dados, precedência, cenas fechadas ou cânone. Fonte: instrução do jogador sobre excesso de NPCs solícitos antes do fechamento M2; exemplo C14 e avaliação do mundo gótico-punk.
PRECEDÊNCIA: .AGENT/.CONTEXTG, G23/G24, cânone/congelados, CONTRACT_V1 (H/B/pressões/limites), NPC_KNOWLEDGE_GATE, G25/G27/G28 e ORCHESTRATION_CONTRACT_V1. A antiga ativação em C15 não retroage a C14. Se houver conflito, não harmonizar silenciosamente.

## Defeito corrigido
Em EVALUATOR_V1.mjs, `expression = score<=-2 ? negative_expression : positive_expression`: para -1, 0 e +1 selecionava POSITIVE. O EVALUATOR_V2.mjs passa a usar NEGATIVE para -5..-2, NEUTRAL_ROLE_DRIVEN para -1..+1 e POSITIVE somente para +2..+5. Perfil ausente produz UNPROFILED/UNKNOWN, jamais score=0 usado como prova de cordialidade. Humor ainda requer janela temporal e duas faces d3 verificáveis quando sem causa conhecida; se RNG indisponível, fallback 0 IDENTIFICADO, não alegria simulada.

## Hard gate: resposta NPC significativa
ANTES de narrar fala/decisão com impacto sobre liberdade, cooperação, dinheiro, trabalho, informação, segurança ou relações, identificar internamente:
1. OBJETIVO próprio: o que esse NPC quer AQUI, independentemente de Bartolomeu? Não usar 'ajudar o protagonista' como motivo.
2. CARGO e PODER: quem pode autorizá-lo, puni-lo, pagar-lhe, substituí-lo, denunciá-lo ou constrangê-lo?
3. RISCO/CUSTO de consentir: que prazo, carreira, prestígio, reputação, salário, segurança, segredo ou recurso a concessão sacrifica? Se não custa nada, documentar por que é trivial.
4. LIMITES e conhecimento: quais regras institucionais, compromissos, traços e proveniências fazem sentido? Conhecimento UNKNOWN não vira certeza ou falsa ignorância.
5. HUMOR + VÍNCULO: obter pontuação pela regra V1/V2 quando há dados; usar personalidade e contexto também. Estado sem perfil não justifica fala positiva/negativa automática.
6. DECISÃO AUTÔNOMA: cooperar, negar, protelar, impor condição, exigir contrapartida, ceder por medo, mentir segundo conhecimento, encaminhar, barganhar ou reagir de outro modo causal. NÃO decidir somente pelo valor de P. Registrar consequência possível e relação de poder, sem garantir fracasso/sucesso.

## Padrão de conduta e fricção
- Predisposição alta expressa abertura à CONVERSA, não licença de abandonar trabalho, ignorar procedimento, revelar informação, perdoar, confiar ou concordar. Um aliado pode dizer NÃO com carinho, um chefe pode achar Bart útil e ameaçá-lo se ele faltar.
- Predisposição baixa pode ser hostilidade verbal, silêncio, rigidez, burocracia, ironia, manipulação, mau humor, cansaço ou rejeição. Ninguém precisa ser vilão declaradamente grosseiro.
- Neutro é NEUTRO, não abraço emocional: falar pouco, desviar o tema, manter distância, negociar, exigir documentação, avaliar risco ou agir profissionalmente, segundo perfil. Neutralidade não obriga indiferença.
- Personagens são imperfeitos e inconsistentes: orgulho, oportunismo, covardia, crueldade, preconceitos, exaustão, ingenuidade, autocontrole falho e interesses materiais são POSSIBILIDADES causais, não rótulos sorteados. Não transformar todos em psicólogos maduros, protetores e terapeutas morais.
- Não recompensar sistematicamente a intenção boa de Bart com validação emocional, obediência ou perdão. Seu porte e sua violência podem provocar defesa, medo, rancor, humilhação e reação institucional; nunca isentá-lo de consequência por protagonismo.
- NPC institucional pode obedecer regulamento injusto por conveniência, medo de perder emprego, crença ou ganho. Integridade e simpatia são possíveis, mas têm preço, limites e posicionamentos conflitantes.
- Não criar obstáculo FORÇADO nem recusa automática: decidir por agência, contexto, disposição, testemunhas, riscos e fatos documentados. Variar pessoas e circunstâncias. Não mudar relação permanente B apenas por um dia ruim.

## Exemplo de regressão C14 — NÃO É RETCON
C14.04 historicamente: Pavel ofereceu cobertura e Andreyev aceitou a ida imediata de Bart à escola. Fica fechado. Em situação FUTURA comparável, o Narrador deve verificar prazo/crise, quem pode dispensá-lo, custo de remanejamento e incentivos de Pavel/Andreyev. Negar saída, conceder licença condicional, descontar horas ou ajudar com risco pessoal são alternativas plausíveis; 'família primeiro, vá em paz' não é resposta automática nem proibida. Se faltar ao trabalho, o PJ escolhe; advertência/retaliação só com agente competente e fatos causais.

## Sem burocracia de contexto
Para figurante de uma interação: estado mental MÍNIMO efêmero (função + objetivo + risco/limite + atitude), sem criar arquivo persistente de cada transeunte. Para recorrente: armazenar somente perfil/pressões duradouros quando eventos sustentarem. Em G28, persistir deltas materiais por CENA; não batidas, não conversa cordial trivial. Sem perfil, caracterizar minimamente por função e evidência, sem inventar conhecimento/parentesco/segredo.
