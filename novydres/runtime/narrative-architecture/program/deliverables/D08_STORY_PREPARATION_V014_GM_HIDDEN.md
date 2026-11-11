# CHR-001 — Preparação de histórias e cenas V014

**Versão:** V014. **Classificação:** GM_HIDDEN (agentes autorizados leem; relatório ao jogador não reproduz segredos).  
**Status:** preparação autoral concreta; não é SCENE_READY, não inicia C06 e não concede permissão ao Narrador.  
**Predecessor direto preservado:** `D08_STORY_PREPARATION_V013_GM_HIDDEN.md`, Git blob `d07d7d4a98337e34624ca1c0683b53f921e2039d`.  
**Baseline de autoria:** `D06_CHRONICLE_BIBLE_V020.json`, Git blob `554dd17fae38d30ef1e320df5a6882cbe2544520` (snapshot anterior à integração V021); `D07_STORY_TRUTH_PACKAGE_V014_GM_HIDDEN.md`, Git blob `69c3be7f74f28e38933c7d1d8f35234d5e431164`; `D04_PLOT_ADMISSIONS_V010.json`, Git blob `260364032af2bd231b89c8fc7ac389f8543d4b79`; autorização vigente `PLAYER_DECISION_AGENT_ACCESS_V003.json`, Git blob `9526af065467588c4c8ce5cb0013d199868542a1`. Predecessores permanecem no histórico; esta sucessora incorpora o crosswalk por `contract_ref`, as identidades NPC estáveis e os ramos de acesso condicional sem alterar material jogado.

## Contrato comum de mesa

Os IDs de admissão D04 (`plot_id`) são distintos dos IDs de história (`story_id`, `ST-*`); qualquer ligação com uma unidade desta preparação é resolvida somente pelo `contract_ref` da admissão e seu fragmento `#ST-*`. Preservar o caminho/hash histórico citado por D04, sem tratar a versão apontada como dependência operacional vigente.

- Recuperar `CYCLE_V0034`, `LIVE_V038`, `HISTORY_INDEX_V038`, `state_v044`, `D06 V021`, `D07 V014`, fichas e ledger atuais antes de qualquer uso. C05 permanece a última seção jogada; C06 não começou; Bart está mortal e sem Abraço. Nenhuma cena já escrita de M3.01 muda esse estado.
- M3.01 C06 tem preparação candidata própria. O arco de coerção com Kuthulun pertence a M3.02, uma história futura separada depois do encerramento de M3.01. Não usar C06 para transformar Bart.
- M3.01 continua ativa; M3.02 não pode começar até que o encerramento de M3.01 e a transição sejam realmente registrados e autorizados. Se o prazo não couber na cronologia jogada, manter o alvo não alcançado/alternativo.
- O Dossiê M3.01 V5 foi revisado até C04 e está stale perante C05; PT08 não é evento canônico e não aciona estas histórias. Revalidar qualquer uso futuro após reconciliação.
- Entrada de cena requer causa e escolha do jogador conforme cada contrato. Não puxar personagem para lugar, conversa ou luta por resumo, elipse ou conveniência.
- Cada teste anuncia pool, oposição, risco, regra, dados e recurso antes da resolução. Falha muda somente consequências preparadas; não substitui a investigação por porta fechada. Nunca manipular dados, assumir uso de FV, XP ou disciplina.
- Falar como NPCs em resposta ao que veem/sabem; nenhum diálogo, ação, sentimento ou decisão de Bart é obrigatório. NPCs não sabem segredo só por estarem no pacote. Família não aparece, escreve, responde, foge ou sofre dano sem evento jogado e evidência.
- Se o jogador examinar a caixa de C05, honrar sua ação sem inventar conteúdo. Registrar a nova ação e pausar somente a subinvestigação da caixa até fonte/decisão; a continuidade principal continua disponível por outra ação. A caixa não é um gate da história.
- Gatilhos de interrupção: conflito com fonte canônica; mecânica que não permita o ramo previsto; perda de consentimento/controle sobre protagonista; necessidade de registrar evento; ausência de gate operacional. Fechar como alternativa/incompleto em vez de criar fato.

## `ST-C06-REENTRY` — retorno à Oficina, candidato M3.01 C06

**Local/circunstâncias:** baia alugada da Oficina Krauser, bancada e entrada lateral. É o próximo turno de trabalho que vier a ser autorizado; nenhuma passagem de tempo é presumida. Milan Varga chega em seu sedã usado com chiado ao dar partida e luz de carga intermitente. Uma inspeção inicial mostra correia do alternador ressecada e trincada; a peça correta não está no estoque. Ele pede avaliação e orçamento antes de autorizar qualquer serviço, pois precisa do carro para um turno de entregas no período seguinte.

**Participantes possíveis:** Bart e Milan. Niko só pode entrar se o ledger do momento disser que está trabalhando e Bart decidir delegar algo. Nenhum Gangrel ou familiar está presente. Outros NPCs só aparecem se seu estado reconciliado justificar.

**Entrada/pré-condições:** C06 precisa ser iniciado por ciclo autorizado; recuperar o último estado e o papel de cada personagem antes da abertura. Enquanto o cursor mantiver C06 não iniciado, isto é preparação escrita, não acontecimento. A caixa permanece desconhecida e não é necessária. Não introduzir Kuthulun, a transportadora, o Sistema Circulatório ou o Abraço.

**Função dramática e conflito:** reabrir a iniciativa por meio de uma escolha profissional concreta: quanto examinar, o que cobrar, como descrever o risco, e se o trabalho é possível no prazo. Milan quer mobilidade e custo controlável; Bart segue o código profissional de cobrar por todo serviço, só fazer trabalho pedido e informar defeitos. A peça ausente impede prometer reparo imediato. A pressão é de tempo e dinheiro, sem antagonista oculto.

**Conhecimento na entrada:** Bart observa o carro, o sintoma e a condição visível da correia; ainda não sabe se há falha adicional. Milan conhece o sintoma e o turno de trabalho que pretende cumprir; não conhece o diagnóstico de Bart. Niko, se presente, conhece somente o que observou ou ouviu. Nenhum participante sabe algo sobre a caixa ou sobre Cainitas por esta situação.

**Beats condicionais e escolhas:**  
1. Milan descreve o chiado e a luz intermitente, pede um orçamento e pergunta se um ajuste rápido basta. Bart pode atender, limitar a inspeção, explicar o escopo e o preço, recusar ou encerrar.  
2. Se Bart examina o conjunto, pode confirmar visualmente a correia trincada e avaliar o tensionamento; qualquer teste de motor ou inspeção adicional ocorre apenas se escolhido, com risco e pool anunciados antes.  
3. Bart pode explicar a diferença entre ajuste provisório e substituição correta, cobrar avaliação, cotar peça e mão de obra, recomendar retorno após obter a peça, oferecer outra alternativa ou não recomendar circulação até a condição ser corrigida. O texto não fixa preço, reparo, autorização ou teste.  
4. Milan pode aceitar a avaliação, pedir escopo menor, adiar, retirar o carro, pedir tempo para decidir, ou aceitar retorno depois. Se ele contestar preço ou recomendação, Bart pode esclarecer ou encerrar; não há obrigação de acordo.  
5. Se Bart pergunta por acontecimentos desde a última cena, cada personagem responde somente pela própria experiência. Não preencher elipses. Se Bart examina a caixa, honrar a ação sem inventar conteúdo.

**Falha, recusa e desvio:** nenhuma rolagem é obrigatória para inspeção simples feita com ferramentas adequadas. Se uma ação arriscada falha, aplicar apenas o efeito declarado antes dos dados; a causa pode permanecer desconhecida e o cliente ainda pode escolher orçamento, adiamento ou retirada. Se Bart recusa atendimento ou abandona, Milan leva o carro e a interação fecha sem punição automática. Uma ação inesperada é respondida a partir do que Milan conhece e pode fazer; o Narrador não a converte em investigação ou confronto Cainita.

**Consequências imediatas e saídas:** orçamento entregue e aceito/recusado; avaliação paga conforme preço realmente informado e aceito; reparo autorizado e concluído apenas se a peça, tempo e trabalho de fato permitirem; retorno combinado; carro retirado; ou cena encerrada sem serviço. Registrar pedido, consentimento, preço, autorização, observações e estado do veículo somente pelo que foi jogado. C06 pode fechar depois que Bart escolhe próximo passo e o ledger registra o resultado. Nenhum destino do carro, pagamento ou seguimento ocorre fora de cena.

**Critério de saída:** existe decisão profissional observável ou o jogador encerra/abandona a interação. O fio fecha localmente mesmo se nenhuma reparação ocorrer. Falha não cancela C06 nem exige outra provocação. O conteúdo autoral está preparado; isso não é SCENE_READY, não inicia C06 e não concede permissão ao Narrador.

## `ST-MEASURE-DISPOSITION` — peça curta, trama opcional

**Local/participantes:** bancada da Oficina; Bart, Niko e cliente só enquanto o pedido está aberto.

**Entrada:** peça precisa ser inspecionada em C06 ou visita posterior; erro da régua não é automaticamente notado antes de inspeção ou falha física observável.

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

**Pré-condições:** Rada entregou em mãos cartão de Kuthulun após relé válido ou após solicitação direta de Bart. O cartão contém local e uma janela relativa, sem endereço familiar. Sem cartão, sem cena. Bart escolhe aceitar, recusar ou ignorar.

**Função/conflito:** determinar se há interlocução e separar observação de rumor. Kuthulun pergunta por um fato que consta no relato; Bart pode confirmar, contestar, mentir, calar, sair ou pedir outra reunião. Kuthulun sabe somente o que Rada relatou e o conhecimento limitado pela variante aberta. Ela não ameaça nem tenta capturar nesta primeira aproximação.

**Condicional dos NPCs:** se Bart contesta o relatório, Rada descreve somente o que viu. Se ele se retira, ambos deixam o local. Se ele pede nova conversa, Kuthulun pode aceitar e manda Rada levar convite futuro. Se não pedir e não aceitar, o fio pode encerrar.

**Saídas/consequências:** conversa aceita; recusada; abandonada; convite futuro entregue; ou silêncio. Somente a entrega efetiva abre ST-KUTHULUN-COERCION. Não registrar a presença de Bart por ausência.

## `ST-KUTHULUN-COERCION` — encontro de sete Gangrel, M3.02

**Local/circunstâncias:** área circular do galpão de pesagem no pátio industrial aberto do Pátio do Lastro; lâmpada industrial, ruído ocasional da estrada e campo de visão para as saídas. A porta oeste abre para o pátio; a porta leste abre para um caminho pedestre lateral; a abertura de carga dá para uma faixa de serviço. Essas três rotas são distintas e visíveis desde a área de confronto. O pátio não tem cerca contínua: há saídas pedestres laterais além do portão principal de veículos. Arvo observa somente esse portão, fora da linha das três rotas, e não as bloqueia automaticamente. Obstáculos, distâncias, visibilidade e posições reais são declarados antes de qualquer teste; nenhuma passagem secreta ou barreira nova surge durante a cena.

**Entrada:** somente depois de M3.01 encerrada pelo gate documental e de jogador do D06 V021, com transição autorizada e registrada, convite entregue por causa verificável e Bart escolher comparecer. Sem comparecimento, não há encontro nem captura ou perseguição fora de cena. O prazo autoral continua antes de 25/12/1970 sem dia inventado.

**Participantes:** Kuthulun no centro; Rada, Borislav, Vesna, Arvo, Milena e Danica, se todos constarem no estado de entrada; Bart diante dela se escolher comparecer. Arvo ocupa somente a posição visível junto ao portão principal, não uma saída do galpão. Sete Gangrel no desenho. Se uma ausência for estabelecida antes da cena, corrigir o elenco e a preparação, sem substituto silencioso.

**Conhecimento permitido:** Kuthulun sabe a premissa estrita autorizada pelo jogador e a variante aberta, além de qualquer fala ou transmissão efetivamente ocorrida. O pacote não cria relay histórico nem inventa quando ou como ela soube. Rada conhece somente observações e mensagens que realmente recebeu. Cada outro Gangrel sabe somente instruções que ouviu e o que vê ou ouve na cena. Nenhum NPC sabe paradeiro ou ações futuras da família sem fonte. A ameaça genérica sobre a família é uma tática verbal de coerção, não evidência de que Kuthulun ou o grupo conheçam nomes, relações, paradeiro, atos ou resposta de qualquer familiar. Ela não autoriza alterar os ledgers de conhecimento dos NPCs; registre apenas que a ameaça foi proferida. Fatos familiares e conhecimento do jogador/personagem ficam em seus próprios escopos.

**Função e conflito:** Kuthulun exige custódia e obediência. Não há acordo seguro de autonomia no encontro. Bart pode falar, calar, negociar, recusar, tentar qualquer saída física, lutar ou escolher outra ação. Recusa verbal, silêncio ou negociação sem submissão que o deixe no recinto é lida como não submissão. Kuthulun comunica que a recusa levará à morte e ameaça genericamente os vínculos que Bart tenta proteger. É a direção autoral do conflito, não prova de que ela sabe nomes, parentesco, endereço, paradeiro ou plano familiar; nenhum dano anterior é alegado. NPCs só podem agir sobre um alvo individualizado após fonte e transmissão em jogo.

**Escalada condicional:** Kuthulun começa sem ativar dons de sangue. Primeiro usa postura e combate físico; só escala para poder de sangue ou Disciplina se a ação de Bart e o estado mecânico justificarem. Garras Ferais e Blood Surge só entram se o perfil preparado no D07 V014, elegibilidade, custo de Rouse, Fome e regra vigente permitirem. BP2 é prospectivo e não estabelece compatibilidade de Geração; Generation permanece UNKNOWN. Antes de dados, reconciliar a ficha NPC, geração se houver fonte, Fome e custo; se não forem validados, não há rolagem. Blood Surge em BP2 adiciona +2 dados apenas quando uma ação elegível e custo declarado justificarem; efeitos de BP não dão bônus automático ao ataque físico das garras. Borislav avança somente por ordem ou gatilho definido; Vesna, Arvo e os demais só se movem ou agem a partir da posição declarada, conforme ação e regra. Milena registra o que presencia; Danica intervém por ferimentos observáveis dentro de seus recursos. Nenhum deles cancela a escolha de fuga nem determina sucesso.

**Beats e agência:** reconhecer os acessos e as posições; ouvir a exigência; decidir responder ou não; tomar ações sob risco; verificar cada resultado mecânico; encerrar apenas por fuga, interrupção, derrota, incapacidade ou resultado legal de Abraço. Não há fala, ação ou sentimento obrigatório de Bart. O alvo autoral é Kuthulun derrotar Bart e forçar o Abraço perto da morte se ele permanecer e a resolução mecânica permitir. Não há ramo preparado em que Bart derrote Kuthulun, mas ação, dados e regras continuam válidos. Fugir ou lutar pode abrir uma saída física real, com chance e resultado incertos.

**Condições de saída:** fuga bem-sucedida encerra a história como rota coerciva falhada; a matilha não inicia perseguição automática. Se Bart fica e é derrotado, recusa ou passividade não oferecem saída segura: Kuthulun continua a coerção até interrupção por causa concreta ou até um ramo mecânico válido. Antes de cada rolagem, o Narrador declara posição, ação, pool, oposição, risco e consequência de cada participante que agir; seis acompanhantes não imobilizam Bart nem fecham automaticamente as três saídas. Resolver deslocamento, iniciativa, ataques e defesas segundo a ficha/engine vigentes, sem poder gratuito ou bônus indevido. O alvo é iniciar o Abraço contra a vontade enquanto Bart ainda estiver em estado mortal/dying e antes de Final Death, usando a sequência V5 vigente de drenagem e oferta da Vitae de Kuthulun, conforme o ledger real. Não inventar limiar, número de ações ou resultado de rolagem. Se Final Death ocorrer primeiro, não há Abraço ou ressurreição; fechar como divergência. Abraço só entra no ledger depois de execução legal real, nunca por silêncio, cansaço ou consentimento presumido. Se a mecânica impedir o alvo, prevalece a regra, sem fraude ou rerrolagem compulsória.

**Fechamento e consequência:** registrar somente posição, atos, falas, dano e resultado realmente resolvidos. Sobrevivência, morte, fuga e Abraço não são garantidos pelo documento. O grupo pode continuar suas rotinas independentemente; não age contra a família sem conhecimento e fonte jogados. A história fecha no desfecho observado e não produz alteração retroativa em M3.01.

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

**Consequências/saída:** A aceitação encerra a unidade como `CLOSED_ACCEPTED`. A recusa encerra a unidade como `CLOSED_REFUSAL` e registra a rota como alternativa/incompleta, sem convite automático, repetição ou avanço de rota. O adiamento só fica como `PENDING_ONE_REOFFER` se esta preparação nomear um agente responsável e um gatilho relativo concreto; sem ambos, encerra como `CLOSED_DEFERRED`. Pode haver uma única reoferta; falha do gatilho, recusa ou novo adiamento encerra a unidade. Qualquer reabertura após encerramento exige causa independente e escolha do jogador.


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

**Saída/critério:** `COMPLETE` se os critérios D09 forem evidenciados e Bart optar pela entrada; `ALTERNATE` se houver um desvio intencional que ainda sustente a ficha/entrada; `INCOMPLETE` se condição necessária não ocorreu ou falta evidência. Toda saída registra uma lista finita de lacunas; nenhuma fila infinita é criada.

## Controle de NPC e fonte

Para cada diálogo/ação, registrar `agent`, `source_event`, `content_scope`, `recipient`, `channel`, `time_relative` e `delivery_status`. Nenhuma transmissão é presumida. Os detalhes da Variante Aberta são lidos apenas do arquivo autorizado D12 V001 e nunca estendidos. O relatório PLAYER_SAFE só informa progresso, sem conteúdo deste pacote.


## Proveniência e versão

A cadeia histórica inclui `D08_STORY_PREPARATION_V008_GM_HIDDEN.md`; o predecessor direto é V013 conforme o cabeçalho. A ficha de conflito prospectiva e seus limites constam no D07 V014; BP2 não estabelece Geração.

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

V014 deriva diretamente de D08 V013 (Git blob `d07d7d4a98337e34624ca1c0683b53f921e2039d`), conserva os contratos de conhecimento individual e usa D06 V020 apenas como baseline de autoria e D07 V014 como contrato direto; D06 V021 é a bíblia integrada posterior que consome esta preparação. O pin do baseline e o do contrato direto constam no cabeçalho. A decisão V003 é a autorização atual; V001/V002 ficam apenas como histórico. O crosswalk com admissões D04 usa somente `contract_ref`; nenhuma identidade ou fato histórico é fundido por semelhança. A preparação não muda estado, não inicia C06 e não concede prontidão de cena.
