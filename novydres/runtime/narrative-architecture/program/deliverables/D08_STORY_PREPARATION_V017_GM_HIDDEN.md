# CHR-001 — Preparação de histórias e cenas V017

**Versão:** V017. **Classificação:** GM_HIDDEN (agentes autorizados leem; relatório ao jogador não reproduz segredos).  
**Status:** copy-forward prospectivo; recusa, adiamento, falha recuperável, vitória mecânica e desvio fecham somente unidades locais e mantêm a rota pendente/quieta. `ALTERNATE` requer escolha explícita ou bloqueio irreversível comprovado; `INCOMPLETE` requer evidência reconciliada de impedimento material. `ST-C06-REENTRY` continua sem causa admitida em D04 V010; não há cena pronta, ativação runtime, SCENE_READY ou permissão ao Narrador.  
**Predecessor direto preservado:** `D08_STORY_PREPARATION_V016_GM_HIDDEN.md`, Git blob `3c9867f7e7ec08f91ef801c29d8844bde4790155`.  
**Baseline integrado:** `D06_CHRONICLE_BIBLE_V025.json`, Git blob `1ac6b9d8f64872bcf0526c32a926091b178b0c2e`; `D07_STORY_TRUTH_PACKAGE_V017_GM_HIDDEN.md`, Git blob `f138f205b18268614e6542f7d31640924c489b4b`; `D04_PLOT_ADMISSIONS_V010.json`, Git blob `260364032af2bd231b89c8fc7ac389f8543d4b79`; autorização vigente `PLAYER_DECISION_AGENT_ACCESS_V004.json`, Git blob `507eea0d797ddcafb0f19730c5dd20dd0d4594f1`. Predecessores permanecem no histórico; nenhuma ação ou resultado passado é alterado.

## Contrato comum de mesa

Os IDs de admissão D04 (`plot_id`) são distintos dos IDs de história (`story_id`, `ST-*`); qualquer ligação com uma unidade desta preparação é resolvida somente pelo `contract_ref` da admissão e seu fragmento `#ST-*`. Preservar o caminho/hash histórico citado por D04, sem tratar a versão apontada como dependência operacional vigente.

- Recuperar `CYCLE_V0034`, `LIVE_V038`, `HISTORY_INDEX_V038`, `state_v044`, `D06 V025`, `D07 V017`, fichas e ledger atuais antes de qualquer uso. C05 permanece a última seção jogada; C06 não começou; Bart está mortal e sem Abraço. Nenhuma cena já escrita de M3.01 muda esse estado.
- D04 V010 não admite causa para C06: o material abaixo preserva apenas o ponto de reentrada, sem história, local, agente ou objetivo novo. O arco de coerção com Kuthulun pertence a M3.02, uma história futura separada depois do encerramento de M3.01. Não usar a âncora de C06 para transformar Bart.
- M3.01 continua ativa; M3.02 não pode começar até que o encerramento de M3.01 e a transição sejam realmente registrados e autorizados. Se o prazo não couber na cronologia jogada, preservar a linha do tempo e rever o bloqueio com evidência; atraso por si só não fecha a rota, que permanece pendente/quieta se ainda recuperável.
- O Dossiê M3.01 V5 foi revisado até C04 e está stale perante C05; PT08 não é evento canônico e não aciona estas histórias. Revalidar qualquer uso futuro após reconciliação.
- Entrada de cena requer causa e escolha do jogador conforme cada contrato. Não puxar personagem para lugar, conversa ou luta por resumo, elipse ou conveniência.
- Cada teste anuncia pool, oposição, risco, regra, dados e recurso antes da resolução. Falha muda somente consequências preparadas; não substitui a investigação por porta fechada. Nunca manipular dados, assumir uso de FV, XP ou disciplina.
- Falar como NPCs em resposta ao que veem/sabem; nenhum diálogo, ação, sentimento ou decisão de Bart é obrigatório. NPCs não sabem segredo só por estarem no pacote. Família não aparece, escreve, responde, foge ou sofre dano sem evento jogado e evidência.
- Se o jogador examinar a caixa de C05, honrar sua ação sem inventar conteúdo. Registrar a nova ação e pausar somente a subinvestigação da caixa até fonte/decisão; a continuidade principal continua disponível por outra ação. A caixa não é um gate da história.
- Gatilhos de interrupção: conflito com fonte canônica; mecânica que não permita o ramo previsto; perda de consentimento/controle sobre protagonista; necessidade de registrar evento; ausência de gate operacional. Conservar a consequência e o estado observado; fechar apenas a unidade local quando houver evidência. Recusa, falha não letal, adiamento, demora ou desvio recuperável mantém a rota pendente/quieta. `ALTERNATE` exige escolha explícita ou resultado irreversível real, reconciliado e materialmente incompatível; `INCOMPLETE` exige evidência reconciliada do impedimento material.

## `ST-C06-REENTRY` — marco de continuidade sem cena pronta

**WHY_NOW e limite causal:** o único motivo atual para retornar é preservar a continuidade depois do encerramento G28 de C05. D04 V010 não admite causa para uma nova história C06. O marco operacional não produz conflito, agente, oferta, urgência nem mudança de local.

**Ponto exato de entrada:** Bart está dentro do próprio carro. A caixa cinza permanece fechada com barbante; conteúdo UNKNOWN. Não há destino, partida, viagem, decurso de tempo, chegada ou ação posterior confirmados. A primeira retomada autorizada deve recuperar somente esse estado e devolver em aberto a iniciativa ao jogador: o que Bart faz agora?

**Agentes e conhecimento:** nenhum NPC está presente, convocado ou em contato por força deste marco. Não se presume oficina, baia, cliente, telefonema, retorno ou presença de Milan, Niko, Daniel ou qualquer outro agente. Nenhum ledger de conhecimento muda. A eventual declaração do jogador sobre um plano ou destino é uma escolha atual; não deve ser narrada como viagem, chegada ou evento até que seja efetivamente jogada e autorizada.

**Stakes, escolhas e saída:** não há stakes de história ou decisão profissional preparados, porque não existe causa admitida para eles. Não oferecer menu de ações presumidas nem iniciar teste. Resolver apenas uma ação que o jogador efetivamente declare, com o estado e regras então válidos, sem pré-escrever a cena seguinte. Este marco sozinho nunca é `SCENE_READY`.

**Gate:** C06 só poderá voltar a ser preparado como história após uma causa sustentada por fonte aprovada, admissão explícita em D04, nova preparação e autorização. Um ciclo operacional não supre esses requisitos. Se a causa continuar indisponível, encaminhar M3.01 para `PROVOCATION_CLOSURE_PENDING` e aguardar escolha expressa do jogador segundo os gates de evidência e transição; não fabricar ponte, contato ou acontecimento.

## `ST-MEASURE-DISPOSITION` — peça curta, trama opcional

**Local/participantes:** bancada da Oficina; Bart, Niko e cliente só enquanto o pedido está aberto.

**Entrada:** somente quando um pedido atual de medição ou disposição documentada realmente se abrir. C06 não supre essa causa no estado atual; erro da régua não é automaticamente notado antes de inspeção ou falha física observável.

**Conflito e escolhas:** refazer com metal restante, pedir nova medida, explicar o atraso, entregar com risco explicitamente descrito, ou cancelar. Niko começa defensivo; se Bart mostra a régua contra padrão ou o corte curto, admite a pressa. Se acusado sem prova, pode encerrar conversa e pedir outra pessoa.

**Beats:** conferir régua; comparar projeto; decidir uso de material; comunicar cliente. Não exigir teste se há ferramenta adequada e tempo. Em falha, a peça continua não validada; não se narra quebra imediata sem teste/risco.

**Saídas:** peça corrigida e aceita; cliente retira o pedido; trabalho adiado com compromisso; ou cancelamento. Encerramento registrado com objeto e responsável. Sem efeito em Cainitas.

## `ST-VOLNAYA-BOUNDARY` — arquivo de índice, trama opcional

**Local/participantes:** balcão público do arquivo de Volnaya durante expediente; Bart; Jelena [NPC-CHR-001-JELENA-VOLNAYA]; outros atendentes só se o evento acioná-los.

**Entrada:** Bart deve trazer uma cópia ou escolher procurar o registro; sem isso, a escriturária não aparece na Oficina nem o índice se revela.

**Conflito/opções:** mostrar cópia, pedir correção, perguntar pelo número repetido, guardar a pista, sair ou acusar Jelena [NPC-CHR-001-JELENA-VOLNAYA]. Ela protege o emprego e quer comparar papel antes de responder. A cena não requer entrar em área restrita.

**Pistas:** (a) cópia carbono exibe número duplicado; (b) índice público confirma a duplicidade se for consultado; (c) Jelena explica o erro depois de confrontada com cópia. Com investigação cuidadosa, o campo que associa a transportadora ao Sistema Circulatório é visto literalmente. Ele prova somente a associação textual, sem rota ou explicação.

**Escalada:** se acusação, Jelena chama supervisora e atendimento termina; se a pergunta é precisa, ela deixa Bart comparar cópias; se Bart abandona, não há transmissão automática. Uma falha de teste não esconde a existência do documento que está visível; afeta interpretação ou tempo.

**Saídas:** obter e preservar a cópia, corrigir o índice, ser atendido sem prova, ou encerrar atendimento. A solução da duplicidade é local e rastreável. O que a transportadora faz além da associação permanece UNKNOWN e não trava outras cenas.

## `ST-GANGREL-ATTENTION` — conflito de rua com Gangrel

**Local:** beco lateral e faixa de descarga da Oficina, com saída para rua pública, caixa de ferramentas visível e passagem parcialmente bloqueada por peça longa.

**Entrada:** peça aguardando retirada e Rada usa a passagem naquela noite. Se a Oficina ou objeto não estiver no estado, usar alternativa: Rada observa a obstrução na próxima descarga real; sem descarga, não há contato. Rada não foi atraída por rumor sem fonte.

**Participantes:** Bart, Rada e Borislav. Nenhum outro Gangrel presente; Kuthulun está ausente.

**Objetivo/oposição:** Rada quer a passagem livre; Borislav procura uma reação de Bart; cada lado pode sair. A peça pode ser movida em equipe ou com equipamento; Borislav não recebe direito sobre ela.

**Beats/opções:** mover peça; pedir explicação; chamar Niko; negociar outra rota; recusar; ameaçar; lutar; encerrar. Borislav provoca apenas se Bart insiste em manter o bloqueio; Rada separa os dois se o confronto crescer e o corredor puder ser liberado.

**Conhecimento e relé:** Rada relata a Kuthulun pessoalmente no Pátio do Lastro na próxima reunião regular apenas se viu força extraordinária ou se recebeu de Bart pedido explícito para transmitir contato. O relatório nomeia somente observações. O atraso de reunião pode ser uma noite ou mais, conforme jogo, sem data fixa. Sem encontro, sem relatório; sem relatório/pedido transmitido, Kuthulun não sabe. Uma cena sem observação não cria decisão de convite. Se Rada recusar transmitir, registrar `REFUSED`, sem relatório, convite ou localização divulgada; se a reunião apenas atrasar, registrar `PENDING`, manter convite e divulgação como não emitidos enquanto não houver entrega. Os fatos anteriores nos ledgers de Bart e de cada NPC permanecem intactos. Só a entrega observada do relato pode alterar o conhecimento de Kuthulun, e apenas no conteúdo que a testemunha viu.

**Consequências/saídas:** passagem liberada; acordo; abandono; conflito físico com dano/resultado real; ou relato futuro documentado. O contato é encerrado quando Rada e Borislav saem ou quando Bart encerra. Se nenhum relé ocorrer, a história local fecha em quietude e o caminho ao convite não se abre automaticamente.

## `ST-KUTHULUN-PRECEDENCE` — apresentação breve

**Local:** área da báscula no pátio industrial aberto do Pátio do Lastro. As duas portas de pedestres do galpão e a abertura de carga são visíveis; o portão principal de veículos fica separado, voltado à estrada. Não há perímetro contínuo nem bloqueio de saídas. Participantes: Bart somente se comparecer, Kuthulun e Rada; Milena observa de longe se convocada, sem entrar.

**Crosswalk e pré-condições:** D04 V010 aponta diretamente `PLOT-KUTHULUN-COERCION` a `ST-KUTHULUN-COERCION`; esta unidade é seu pré-requisito procedimental condicional, sem admissão D04 própria. O gatilho amplo de D04 — premissa de conhecimento delimitada e/ou relatório com fonte e transferência registrados — só oferece uma base causal para uma possível ação futura. Após o encerramento autorizado de M3.01 e a transição válida a M3.02, é preciso que uma destas causas produza ação presente: (a) relatório realmente transmitido a Kuthulun; (b) pedido explícito de Bart realmente transmitido por Rada; ou (c) a premissa aprovada, sozinha, leva Kuthulun a decidir iniciar contato naquele momento. No ramo (c), a decisão e a instrução para Rada são ações prospectivas de Kuthulun e não são presumidas pelo gatilho. Em qualquer ramo, Rada precisa efetivamente entregar um primeiro cartão a Bart. Sem causa, ação ou entrega, não há história ou convite; Bart só chega se escolher comparecer.

**Função/conflito:** determinar se há interlocução e separar observação de rumor. Kuthulun pergunta por um fato que consta no relato disponível; Bart pode confirmar, contestar, mentir, calar, sair, pedir outra reunião ou recusar. Kuthulun sabe somente o que veio por uma transmissão registrada e a premissa delimitada aprovada; não recebe detalhes históricos adicionais por esta preparação. Ela controla o tempo da conversa e Rada trouxe o convite efetivamente entregue.

**Condicional dos NPCs:** se Bart contesta um relatório, Rada descreve somente o que observou e realmente transmitiu. Se ele se retira, ambos deixam o local. Se ele pede outra conversa e Kuthulun aceita, ela pode escolher mandar Rada levar um novo convite. Se ele não pede nem aceita, o fio pode encerrar. Nenhuma escolha de Kuthulun, Rada ou Bart é automática.

**Saídas/consequências:** conversa aceita; recusada; abandonada; novo convite futuro entregue; ou silêncio. A primeira entrega abre somente `ST-KUTHULUN-PRECEDENCE`. Um eventual convite para a história coerciva é um segundo ato, distinto, que só abre `ST-KUTHULUN-COERCION` depois de ser realmente entregue e de Bart escolher comparecer. Não registrar a presença de Bart por ausência nem iniciar coerção por causa do primeiro cartão.

## `ST-KUTHULUN-COERCION` — encontro de sete Gangrel, M3.02

**Local/circunstâncias:** área circular do galpão de pesagem no pátio industrial aberto do Pátio do Lastro; lâmpada industrial, ruído ocasional da estrada e campo de visão para as saídas. A porta oeste abre para o pátio; a porta leste abre para um caminho pedestre lateral; a abertura de carga dá para uma faixa de serviço. Essas três rotas são distintas e visíveis desde a área de confronto. O pátio não tem cerca contínua: há saídas pedestres laterais além do portão principal de veículos. Arvo observa somente esse portão, fora da linha das três rotas, e não as bloqueia automaticamente. Obstáculos, distâncias, visibilidade e posições reais são declarados antes de qualquer teste; nenhuma passagem secreta ou barreira nova surge durante a cena.

**Entrada:** somente depois de M3.01 encerrada pelo gate documental e de jogador do D06 V025, com transição autorizada e registrada, conclusão da história de precedência e entrega efetiva de um convite coercivo distinto. Bart escolhe se comparece. O gatilho amplo de D04 não substitui esses passos. Sem comparecimento, não há encontro nem captura ou perseguição fora de cena. O prazo autoral continua antes de 25/12/1970 sem dia inventado.

**Participantes:** Kuthulun no centro; Rada, Borislav, Vesna, Arvo, Milena e Danica, se todos constarem no estado de entrada; Bart diante dela se escolher comparecer. Arvo ocupa somente a posição visível junto ao portão principal, não uma saída do galpão. Sete Gangrel no desenho. Se uma ausência for estabelecida antes da cena, corrigir o elenco e a preparação, sem substituto silencioso.

**Conhecimento permitido:** Kuthulun sabe a premissa estrita autorizada pelo jogador e a variante aberta, além de qualquer fala ou transmissão efetivamente ocorrida. O pacote não cria relay histórico nem inventa quando ou como ela soube. Rada conhece somente observações e mensagens que realmente recebeu. Cada outro Gangrel sabe somente instruções que ouviu e o que vê ou ouve na cena. Nenhum NPC sabe paradeiro ou ações futuras da família sem fonte. A ameaça genérica sobre a família é uma tática verbal de coerção, não evidência de que Kuthulun ou o grupo conheçam nomes, relações, paradeiro, atos ou resposta de qualquer familiar. Ela não autoriza alterar os ledgers de conhecimento dos NPCs; registre apenas que a ameaça foi proferida. Fatos familiares e conhecimento do jogador/personagem ficam em seus próprios escopos.

**Função e conflito:** Kuthulun exige custódia e obediência. Não há acordo seguro de autonomia no encontro. Bart pode falar, calar, negociar, recusar, tentar qualquer saída física, lutar ou escolher outra ação. Recusa verbal, silêncio ou negociação sem submissão que o deixe no recinto é lida como não submissão. Kuthulun comunica que a recusa levará à morte e ameaça genericamente os vínculos que Bart tenta proteger. É a direção autoral do conflito, não prova de que ela sabe nomes, parentesco, endereço, paradeiro ou plano familiar; nenhum dano anterior é alegado. NPCs só podem agir sobre um alvo individualizado após fonte e transmissão em jogo.

**Escalada condicional:** Kuthulun começa sem ativar dons de sangue. Primeiro usa postura e combate físico; só escala para poder de sangue ou Disciplina se a ação de Bart e o estado mecânico justificarem. Garras Ferais e Blood Surge só entram se o perfil preparado no D07 V017, elegibilidade, custo de Rouse, Fome e regra vigente permitirem. BP2 é prospectivo e não estabelece compatibilidade de Geração; Generation permanece UNKNOWN. Antes de dados, reconciliar a ficha NPC, geração se houver fonte, Fome e custo; se não forem validados, não há rolagem. Blood Surge em BP2 adiciona +2 dados apenas quando uma ação elegível e custo declarado justificarem; efeitos de BP não dão bônus automático ao ataque físico das garras. Borislav avança somente por ordem ou gatilho definido; Vesna, Arvo e os demais só se movem ou agem a partir da posição declarada, conforme ação e regra. Milena registra o que presencia; Danica intervém por ferimentos observáveis dentro de seus recursos. Nenhum deles cancela a escolha de fuga nem determina sucesso.

**Beats e agência:** reconhecer acessos e posições; ouvir a exigência; decidir responder ou não; tomar ações sob risco; verificar cada resultado mecânico. Não há fala, ação ou sentimento obrigatório de Bart. O alvo autoral é Kuthulun derrotar Bart e forçar o Abraço perto da morte se ele permanecer e a resolução mecânica permitir; esse alvo nunca prevalece sobre uma vitória real de Bart ou outra resolução legal. Lutar ou fugir pode abrir saída física real, com chance e resultado incertos.

**Condições de saída:** fuga bem-sucedida fecha o conflito local por fuga; não há perseguição automática. A rota permanece pendente/quieta se o resultado ainda for recuperável; só escolha explícita ou bloqueio irreversível comprovado fundamenta saída de rota, conforme D09. Se Bart vence Kuthulun sob as regras aplicáveis, sua vitória é resultado canônico desta cena. Não há Abraço contra esse resultado. Primeiro se resolvem apenas as ações já em andamento e as respostas imediatas legalmente disponíveis; cada outro NPC decide individualmente conforme sua motivação, posição, conhecimento, recursos, ordens realmente recebidas e regras. Ninguém ataca, resgata, foge, persegue ou retaliará por automatismo, em uníssono ou fora de sua posição/turno. Se não houver ação imediata legal e motivada, a cena pode fechar após a vitória e a reconciliação do estado. Se algum outro conflito continua ativo, ele deve ser exposto e resolvido sob a mesma declaração prévia de posição, ação, pool, oposição, risco e consequência.

Se Kuthulun continua capaz de agir, o vencedor ainda não encerrou o conflito; seguir mecânicas e ações reais. Se ela está incapacitada, não pode agir até que as regras permitam. Se ela sofre Final Death, não há Abraço nem ressurreição. Uma vitória não garante que Bart esteja ileso, que os demais recuem ou que a saída fique segura; registrar apenas o que aconteceu. Antes de cada rolagem, declarar posições, ações, pool, oposição, risco e consequência para quem realmente age; os seis acompanhantes não imobilizam Bart nem fecham automaticamente as saídas. Resolver iniciativa, deslocamento, ataque e defesa conforme ficha/engine vigentes, sem poder gratuito ou bônus indevido. O Abraço só pode ocorrer se a sequência V5 vigente o permitir antes de Final Death, enquanto Bart ainda está em estado mortal/dying; aplicar drenagem e oferta de Vitae com o ledger real e sem inventar limiares, contagem de ações ou resultado. Nunca inferir Abraço por silêncio, cansaço ou consentimento presumido.

**Fechamento e consequência:** encerrar quando o resultado do conflito imediato estiver estável: fuga, interrupção real, incapacidade/derrota seguida das ações imediatas válidas, Abraço legal ou Final Death. Registrar somente posição, atos, falas, dano, recursos e resultado realmente resolvidos. A vitória de Bart fecha somente o conflito local e preserva dano, recursos, posições e demais consequências realmente ocorridas. Ela não fecha automaticamente a rota: resultado recuperável mantém pendência/quietude; se um fato irreversível materialmente bloquear o alvo, registrar a evidência e aplicar a revisão de D09. Nenhuma retaliação, resgate, nova convocação ou outra ação de NPC ocorre por automatismo. Nenhum resultado futuro — liderança, vingança, reconciliação, novo ataque ou resposta de outros Gangrel — é fixado aqui; cada ação posterior depende de agente capaz, motivação, conhecimento, oportunidade e causa. Nenhuma consequência retroage a M3.01.

## `ST-POST-EMBRACE` — agrupador, sem cena independente

Esta unidade apenas agrupa `ST-FIRST-NIGHTS`, `ST-GRIEF-AND-BOUNDARIES`, `ST-CAINITE-ENTRY` e `ST-ETHICAL-COST`. Ela não cria beat, evento, exigência de ordem ou cena própria; só fica disponível depois de Abraço realmente registrado.

## `ST-FIRST-NIGHTS` — primeira noite pós-transformação

**Local:** sala de manutenção fechada no Pátio do Lastro, colchão, água inutilizável para a fome, armário de primeiros socorros, recipiente lacrado de sangue animal com quantidade contada antes da cena.

**Entrada:** Abraço ocorrido e estado pós-evento validado; no primeiro período de vigília que o sistema confirmar. Sem evento, não existe. Participantes: Bart, Kuthulun, Danica e Ilja; qualquer ausência é resolvida pelo estado, não presumida.

**Função/conflito:** sobreviver à mudança e decidir se aceita abrigo, cuidado e fonte de sangue. Kuthulun mantém o recém-chegado dentro da própria custódia; Danica evita deterioração dentro de sua capacidade; Ilja deseja que sua rotina não seja interrompida.

**Opções/beats:** Bart pode aceitar ou rejeitar o local, pedir comida/sangue, examinar a sala, fugir, pedir espaço, convocar ajuda, ou não agir. Recurso alimentar é contabilizado e regra de sangue animal depende da ficha/BP real. Cuidado não cura fora da regra. Hunger/frenzy é uma resolução mecânica real, não montada para resultado dramático.

**Saída:** abrigo aceito, saída escolhida, fome resolvida por fonte efetivamente válida ou não resolvida. Persistir estado só após a cena. A cena termina quando decisão imediata de segurança/necessidade é tomada ou o jogador encerra.

## `ST-GRIEF-AND-BOUNDARIES` — relação humana sob perda

**Local:** sala de ferramentas da Oficina Krauser em horário sem clientes; porta de serviço e telefone ao alcance, sem indicar que alguém atende. Participantes: Bart e Ilja; Rada só se estiver registrada como presente. Nenhum familiar aparece automaticamente.

**Entrada:** semanas relativas após um Abraço real, depois que a primeira crise física terminou; Bart escolhe visitar a Oficina ou usar a sala como lugar de conversa. Se não escolhe, pode encerrar como não iniciado sem ser convocado por acaso.

**Conflito:** Ilja pede que Bart decida como proteger a vida anterior dos riscos noturnos; sente ressentimento por um recém-chegado receber a atenção de Kuthulun antes dele. Ilja não decide o acesso da família nem pode vetar Bart. Durante uma conversa iniciada ou aceita por Bart, Ilja pode oferecer a chave da porta de serviço; a transferência só ocorre se Bart aceitar, e a chave não garante entrada, passagem segura ou controle da porta. Sem conversa, sem oferta, diante de recusa ou se Ilja não estiver disponível, não se presume posse. Bart pode usar telefone, sair, pedir escolta, guardar um objeto escolhido por ele, confrontar Ilja, escolher não contatar ou definir outro limite; nenhuma dessas rotas depende da chave.

**Beats condicionais:** se Bart inicia ou aceita a conversa, Ilja pode oferecer a chave; registrar transferência somente se Bart a aceitar. Sem transferência, ele pode escolher telefone, porta pública, escolta ou outra ação. Ilja oferece suas informações de segurança; se Bart tenta contato, o Narrador verifica o canal real e o estado da família. Ninguém inventa resposta, localização ou decisão. Se a família não está disponível, registrar somente tentativa e canal, sem inferir sentimento. A tentativa recebe um registro separado (`tentado`, canal escolhido e resultado restrito a esta tentativa); não altera a identidade, localização, disponibilidade geral ou resposta familiar. Ausência de contato não significa rejeição nem decisão.

**Saídas/consequências:** limite definido pelo protagonista, contato efetivo, contato sem resposta documentada, ou retirada. Fechar a cena após um passo escolhido. O luto pertence ao personagem sem ser imposto como fala, monólogo ou sentimento obrigatório.




## `ST-CAINITE-ENTRY` — provação social e turno de vigia

**Local:** sala comum do Pátio do Lastro, quadro de turnos e dois bancos. Participantes: Bart, Kuthulun, Vesna, Ilja, Rada, Milena; Borislav pode observar sem votar.

**Entrada:** Abraço real e convite para o primeiro encontro formal; horário relativo após `ST-FIRST-NIGHTS`, nunca em M3.01.

**Conflito:** Vesna precisa atribuir um único turno de vigia a Bart ou a Ilja, o veterano que esperou por posição. O turno é limitado, tem horário e responsabilidade observáveis. Ilja quer reconhecimento e pode recusar ajudar; não sabotará automaticamente. Kuthulun pode sustentar ou rever sua ordem, conforme o que ocorreu.

**Escolhas:** aceitar, dividir, devolver, negociar outro turno, pedir assistência, recusar ou sair. Persuasão pode alterar proposta dentro de limites; uma falha não elimina todas as opções. Nenhuma rolagem determina valor social de Bart ou obriga obediência.

**Consequências/saída:** A aceitação encerra a unidade como `CLOSED_ACCEPTED`. A recusa encerra somente a unidade como `CLOSED_REFUSAL`; a rota fica pendente/quieta. O adiamento só fica como `PENDING_ONE_REOFFER` se esta preparação nomear agente responsável e gatilho relativo concreto; sem ambos, encerra a unidade como `CLOSED_DEFERRED`, mantendo a rota pendente/quieta. Pode haver uma única reoferta apenas se o gatilho nomeado ocorrer de fato; não há reoferta automática. Falha do gatilho, recusa ou novo adiamento fecha a unidade local, não a rota. Resultado irreversível real que, após reconciliação, materialmente bloqueie o alvo abre revisão finita; não fecha a rota por automatismo. `ALTERNATE` é registrado somente por escolha explícita do jogador; `INCOMPLETE` exige evidência reconciliada do impedimento material e a disposição do jogador conforme D09. Qualquer reabertura após encerramento exige causa independente já autorada e escolha do jogador.


#### Beat condicional: Ilja, chamado “O Retentor” nas apresentações

Na chegada às primeiras apresentações Cainitas em que Kuthulun está presente, Ilja pode cumprir o papel de anfitrião ou auxiliar de protocolo. Ele conhece a escolha recente de Kuthulun porque a presencia; não recebe por isso acesso às informações privadas de Bart. Sua frieza ou provocação social vem de ter esperado muito pelo próprio Abraço sem jamais receber uma promessa, enquanto Bart foi escolhido rapidamente. Ilja busca reconhecimento e posição; não age como assassino nem é a única via de entrada na sociedade. Bart pode responder, perguntar pela expectativa, recusar o teste de status, procurar outra apresentação ou deixar a provocação passar. Se Bart não o enfrentar, ele mantém a distância e a história continua por outras relações; se houver reconhecimento ou negociação, pode facilitar uma apresentação menor sem se tornar aliado automático. Não force fala, sentimento ou decisão de Bart.

## `ST-ETHICAL-COST` — inventário adulterado e promessa limitada, história opcional

**Local/participantes:** arquivo público de Volnaya durante o expediente e, se Bart aceitar conversar, sala comum do Pátio do Lastro. Bart, Vera, Kuthulun e a escriturária do inventário [NPC-CHR-001-INVENTORY-CLERK-VOLNAYA] podem estar presentes; nenhum precisa aparecer sem causa. Essa funcionária é distinta de Jelena [NPC-CHR-001-JELENA-VOLNAYA], que atua em `ST-VOLNAYA-BOUNDARY`; os ledgers, observações e transmissões são separados. A cópia de inventário associa uso noturno de um galpão ao grupo Gangrel e nomeia a funcionária responsável pelo livro, mas não contém dados familiares.

**Entrada e causa:** somente depois de um Abraço realmente registrado. Vera entrega uma notificação de consulta do arquivo a Bart e pede que ele ouça uma proposta. A história começa se Bart aceitar ouvir ou pedir a prova. Se a notificação não puder ser mostrada, a história fecha como oferta não verificada. Kuthulun só liga a proposta à família se Bart tiver dito, numa conversa jogada, que quer protegê-la; ninguém infere identidade, endereço ou resposta dos parentes.

**Conflito e escolhas:** Kuthulun quer reduzir a exposição da rotina do grupo e pede que Bart substitua uma folha por horário falso. A fraude pode transferir suspeita para a escriturária do inventário [NPC-CHR-001-INVENTORY-CLERK-VOLNAYA], que não conhece os Cainitas e só quer corrigir o inventário. Não usar conhecimento, observações ou histórico de Jelena [NPC-CHR-001-JELENA-VOLNAYA] nesta cena. Se Bart declarou preocupação familiar, Kuthulun oferece como contrapartida que o próprio grupo não procure nem contate a família enquanto a condição for respeitada. A promessa não cobre terceiros e não exige nomes ou paradeiro. Bart pode comparar os registros, falar com a funcionária, fazer ou recusar a troca, avisar o arquivo, pedir outra condição ou abandonar. Acesso e sucesso são estabelecidos pela ação e por teste apenas se houver risco mecânico real; falha não gera acusação ou dano automático.

**Conhecimento permitido e beats condicionais:** Vera conhece somente a notificação e a incumbência recebida. Kuthulun sabe apenas o que Bart revelou sobre a preocupação familiar. A escriturária do inventário [NPC-CHR-001-INVENTORY-CLERK-VOLNAYA] vê somente os documentos que lhe são mostrados; Jelena [NPC-CHR-001-JELENA-VOLNAYA] não participa nem transmite conhecimento para esta cena. A notificação prova a associação e o horário descritos, nada sobre rota, mecanismo, demais participantes ou familiares. Se Bart pedir prova, Vera mostra a cópia disponível; se questionar, a funcionária pode explicar duplicação ou fechar o atendimento conforme sua motivação. Se houver adulteração, registrar quem teve acesso, qual folha mudou e qual evidência ficou; nunca narrar sucesso automático. Se houver alerta, o arquivo abre revisão do registro. Recusa ou abandono encerra a oferta sem punição automática.

**Saídas e consequências:** (a) adulteração efetivamente realizada, com risco de suspeita para a escriturária e possível atraso em identificar a rotina; (b) recusa, registro permanece e Kuthulun pode retirar a promessa; (c) denúncia, registro entra em revisão e a rotina pode ficar mais exposta; (d) negociação alternativa ou abandono, sem alteração presumida. A saída se confirma pela escolha e resposta observada. Não se encena nem determina resposta familiar, não há contato automático e a trama opcional não bloqueia a criação guiada. Recusar ou abandonar fecha somente esta oferta opcional, preserva os registros e ledgers familiares e não bloqueia a revisão de graduação de 2010.

## `ST-2010-TRANSITION` — revisão final e entrada na crônica principal

**Local:** sala de arquivo emprestada no Pátio do Lastro, mesa, ficha atual, ledger de XP, índice de relações e lista de fios. Se o lugar não existir no estado de 2010, escolha apenas local já estabelecido naquele ano; a função da cena não depende do Pátio. Participantes: Bart e Narrador; um NPC participa somente se estiver ativo no estado daquela data.

**Entrada:** ano-base 2010 alcançado por passagem temporal autorizada/consentida e um pedido de revisão. Nenhum dia específico é inventado.

**Função/conflito:** reconciliar ficha real vs. ficha-alvo e determinar se criação guiada encerra. Bart pode avaliar objetivos, escolher oportunidade de desenvolvimento já preparada, deixar objetivo incompleto, encerrar sem entrar, ou escolher a crônica principal.

**Beats:** conferir história/jogadas; conferir XP ganho/gasto por comprovante; revisar relações sem completar respostas de ausentes; marcar cada trama fechada, abandonada, quieta ou carregada; revisar aderência ao alvo; perguntar se Bart deseja entrar em 2010. Não exigir rolagem nem resolver todo o cenário.

**Saída/critério:** `COMPLETE` somente se os critérios D09 forem evidenciados e Bart optar pela entrada. Um resultado irreversível que materialmente impeça o alvo abre revisão baseada em evidência, sem mudar o resultado. `ALTERNATE` somente se Bart escolher explicitamente essa saída após a revisão. `INCOMPLETE` somente com evidência reconciliada de impedimento material a requisito necessário e disposição conforme D09; ausência de prova, unidade recusada, atraso ou falha recuperável não bastam e deixam a rota pendente/quieta. Toda saída registra lista finita de lacunas; nenhuma fila infinita é criada.

## Controle de NPC e fonte

Para cada diálogo/ação, registrar `agent`, `source_event`, `content_scope`, `recipient`, `channel`, `time_relative` e `delivery_status`. Nenhuma transmissão é presumida. Os detalhes da Variante Aberta são lidos apenas do arquivo autorizado D12 V001 e nunca estendidos. O relatório PLAYER_SAFE só informa progresso, sem conteúdo deste pacote.


## Proveniência e versão

A cadeia histórica inclui `D08_STORY_PREPARATION_V008_GM_HIDDEN.md`; o predecessor direto é V013 conforme o cabeçalho. A ficha de conflito prospectiva e seus limites constam no D07 V015; BP2 não estabelece Geração.

## V008 — Salvaguardas e preparação condicional

**Versão:** V008. **Predecessor:** D08 V007. **Proveniência:** sucessor de preparação autoral prospectiva para fechar os bloqueios de transição e causalidade; não registra qualquer ação jogada.

- **Caixa do checkpoint:** a caixa permanece UNKNOWN e sem conteúdo inventado. A caixa não é uma gate para que Bart avance por outra prioridade; o Narrador não cria pistas para torná-la relevante.
- **Abandono da consulta documental:** Bart pode interromper e sair. O abandono encerra atendimento, sem transmissão automática ou relatório; o problema local pode permanecer sem correção e as outras histórias seguem sem retaliação automática por esse abandono. Nenhum NPC adquire conhecimento sem fonte e transmissão documentadas.
- **Recusa na entrada Cainita:** Bart pode recusar ou sair. Os NPCs respondem conforme objetivos e conhecimento próprios; nenhuma rolagem determina valor social, obediência ou sentimento. Nenhuma resposta força ingresso, permanência ou adesão do protagonista.

## Cross-story play contract anchor

<!-- D08-ADVERSARIAL-CONTRACT-ROOT -->

This anchor resolves cross-story adversarial tests against the complete playable preparation. Every required scene remains conditional on its entry state, player action, NPC knowledge, and an authorized cycle. Refusal, failure, deviation, early discovery, or abandonment must follow a prepared branch; none may silently mutate persistent state or imply that a scene was played. NPCs act only on knowledge they acquired, and mechanics resolve the actual outcome.


## Contratos preservados de V011 — cobertura de estado e proveniência de tentativas

A preparação V011 sucedeu V010; V012 preserva integralmente aquelas duas precisões e corrige os pins e identificadores acima. 

- Uma ameaça genérica à família é um ato de coerção, não prova de conhecimento sobre parentes específicos. O evento não altera nem amplia o ledger de conhecimento de nenhum NPC. A preparação e a auditoria devem comparar o mapa completo de conhecimento antes e depois, junto aos campos separados da ameaça.
- Uma tentativa de contato registra o canal que foi efetivamente escolhido no evento. O redutor não presume nem injeta um canal. O resultado é registrado em uma entrada própria de tentativa, sem substituir identidade, localização, resposta ou conhecimento anterior da família.

Estas regras são contratos de estado para preparação e teste; não registram tentativa, ameaça ou qualquer outro acontecimento no cânone jogado.

## Proveniência da sucessora V014

V014 deriva diretamente de D08 V013 (Git blob `d07d7d4a98337e34624ca1c0683b53f921e2039d`), conserva os contratos de conhecimento individual e usa D06 V020 apenas como baseline de autoria e D07 V014 como contrato direto; D06 V021 é a bíblia integrada posterior que consome esta preparação. O pin do baseline e o do contrato direto constam no cabeçalho. V003 era a autorização vigente naquele snapshot histórico e foi sucedida por V004; esta sucessora segue V004 como autoridade atual. O crosswalk com admissões D04 usa somente `contract_ref`; nenhuma identidade ou fato histórico é fundido por semelhança. A preparação não muda estado, não inicia C06 e não concede prontidão de cena.


## Rota de continuidade quando C06 não tem causa admitida (V015)

D04 V010 não admite causa para C06. Não existe oferta C06 válida no estado atual; ausência de oferta não é recusa. A retomada volta ao checkpoint C05-22 no carro, sem destino, partida, viagem ou tempo avançado, e entrega a próxima escolha ao jogador. Não iniciar cena de oficina nem introduzir cliente ou NPC para fabricar stakes.

Se o jogador escolher continuar, só usar unidades independentes que tenham causa própria e admissão válida. `ST-VOLNAYA-BOUNDARY` pode começar pela retomada voluntária do caminho documental existente. `ST-MEASURE-DISPOSITION` depende de um pedido atual ou disposição documentada efetivamente aberta. Ambas podem ficar quietas. Fios M3.01 não sobrevivem ao fechamento de M3.01 para serem reabertos depois; `ST-GANGREL-ATTENTION` pertence a M3.02 e exige transição autorizada e a causa local já preparada. Nenhum contato, observação, relé ou convite é presumido.

Sem causa admitida para C06, encaminhar a provocação a `PROVOCATION_CLOSURE_PENDING`; não inventar uma ponte ou cena. O jogador escolhe expressamente se continua por uma condição independente ou se aceita o fechamento alternativo, depois de reconciliados fatos e estado e satisfeitos os gates. Falha recuperável, recusa, desvio ou atraso preserva as consequências locais e mantém a rota pendente/quieta. Resultado irreversível que bloqueie materialmente requisito abre revisão; só uma escolha explícita pode encerrar a rota como `ALTERNATE`, e `INCOMPLETE` requer evidência reconciliada e disposição conforme D09. Nenhuma causa futura é inventada e transformação não é garantida.

## Saída quieta finita quando a rota não tem causa (V016)

Se não há causa admitida para C06, ou depois da transição válida não ocorre causa real para contato, nenhum cartão ou convite é entregue e nenhuma história M3.02 começa. A rota permanece pendente/quieta. Se o jogador preferir encerrar a criação guiada, ele pode escolher explicitamente a saída `ROUTE-QUIET-ALTERNATE-EXIT` definida em D06 V025: registrar `ALTERNATE` no último checkpoint reconciliado e listar condições do alvo e perguntas abertas. Isso encerra a rota editorial, não M3.01 na ficção; não cria cena, ciclo, evento, tempo decorrido, teste ou estado novo. Ausência não é recusa nem fracasso por si só; a escolha do jogador é necessária.

## Proveniência da sucessora V015

V015 deriva diretamente de D08 V014 (Git blob `1333384fb3b4bd36d8eac73dc519485452ce3017`), adota D06 V022 e D07 V015 como contratos integrados (pins registrados no cabeçalho) e preserva D04 V010 como fonte de admissão e segue PLAYER_DECISION_AGENT_ACCESS_V004 como autoridade vigente; V003 permanece somente na proveniência histórica de V014. A sucessora preserva o checkpoint C05-22, registra que D04 V010 não admite causa para C06 e troca a antiga preparação de cena por uma âncora sem stakes ou agentes. Nenhuma passagem de tempo, contato, chegada ou evento é criada; M3.01 permanece aberta até escolha explícita e gate válido.

## Proveniência da sucessora V016

V016 deriva diretamente de D08 V015 (Git blob `64768b468aacd35d4528a3b563142cd0588d6fa`), integra D06 V023 (Git blob `12f866dbd6595c71bd24f89e9ea6f65a16ced026`) e D07 V016 (Git blob `844398c7df3dbbd84ff77a1cb6edb7125aeedb56`), e preserva D04 V010 (Git blob `260364032af2bd231b89c8fc7ac389f8543d4b79`) e a autorização V004. A sucessora clarifica pré-requisito, gatilho e entrega distintos, e acrescenta uma saída local para vitória mecânica; não altera cânone, decisão, resultado jogado, gates de ativação ou checkpoint. Revisão independente D11 ainda necessária.



## Proveniência da sucessora V017

V017 deriva diretamente de D08 V016 (Git blob `3c9867f7e7ec08f91ef801c29d8844bde4790155`), integra D06 V025 (Git blob `1ac6b9d8f64872bcf0526c32a926091b178b0c2e`) e D07 V017 (Git blob `f138f205b18268614e6542f7d31640924c489b4b`), preserva D04 V010 (Git blob `260364032af2bd231b89c8fc7ac389f8543d4b79`) e a decisão V004 (Git blob `507eea0d797ddcafb0f19730c5dd20dd0d4594f1`). A única correção semântica prospectiva separa encerramento local da classificação de rota e exige escolha explícita ou evidência reconciliada de bloqueio irreversível; nenhuma decisão, cânone, evento, resultado passado ou gate operacional é alterado. D07_ACTIVATION_V002 permanece apenas acesso de agentes à versão V016; V017 não está ativado no runtime, não torna a cena pronta e não concede permissão ao Narrador. Revisão independente D11 ainda necessária.
