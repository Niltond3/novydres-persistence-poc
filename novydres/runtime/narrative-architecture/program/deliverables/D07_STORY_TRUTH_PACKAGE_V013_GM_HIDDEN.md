# CHR-001 — Contratos de trama e verdade autoral V013

**Versão:** V013. **Classificação editorial:** GM_HIDDEN (acesso integral de agentes autorizados; não divulgar ao jogador).  
**Status:** contratos autorais completos; nenhuma cena está ativada e nenhum evento prospectivo está registrado como ocorrido.  
**Autoridade vigente:** PLAYER_DECISION_AGENT_ACCESS_V003, Git blob `9526af065467588c4c8ce5cb0013d199868542a1`; autoria prospectiva delegada, cânone confirmado congelado.  
**Predecessor direto preservado:** D07_STORY_TRUTH_PACKAGE_V012_GM_HIDDEN.md, Git blob `430220d0e147d67646c51befc9831a8ba4159072`. V011 e versões anteriores permanecem no histórico; V013 corrige o crosswalk entre namespaces, explicita a entrega condicional de uma chave e fixa identidades NPC distintas com IDs estáveis. **Dependências vigentes:** D06_CHRONICLE_BIBLE_V019.json, Git blob `85d6a8f37e3fb4e2fd7559b3d1965e4fcc2c5296`; D04_PLOT_ADMISSIONS_V009.json, Git blob `0e34b4ab4287cb929d7146808510c562ccdd7d54`; decisão PLAYER_DECISION_AGENT_ACCESS_V003.json, Git blob `9526af065467588c4c8ce5cb0013d199868542a1`. A auditoria mecânica V5 de V011 continua aplicável.

## Registro canônico de unidades

Os `ST-*` abaixo são IDs de unidades de história compartilhados entre D06, D07, D08 e D09. D04 mantém um namespace distinto de admissão (`plot_id`, por exemplo `PLOT-*`); um `plot_id` nunca é um `story_id`, mesmo quando os rótulos parecem relacionados. O crosswalk ocorre exclusivamente pelo `contract_ref` da admissão: usar o fragmento `#ST-*` para localizar a unidade atual correspondente, preservando o caminho e o hash históricos que o próprio D04 registrou. Em D04 V009 esses caminhos ainda apontam ao predecessor D07 V011; eles não transformam V011 na autoridade vigente nem autorizam associação por semelhança nominal. `ST-POST-EMBRACE` é um agrupador editorial, não um evento nem uma história autônoma. `ST-2010-TRANSITION` é o ID único para a revisão de 2010.

| ID | Janela/episódio | Natureza |
|---|---|---|
| `ST-C06-REENTRY` | M3.01 | required-for-return; prepared prospectively; not scene-ready |
| `ST-MEASURE-DISPOSITION` | M3.01 | optional; authored prospectively |
| `ST-VOLNAYA-BOUNDARY` | M3.01 | optional; authored prospectively; contains a new, conditional evidence path |
| `ST-GANGREL-ATTENTION` | M3.02 | required-on-target-route; authored prospectively |
| `ST-KUTHULUN-PRECEDENCE` | M3.02 | required-on-target-route; authored prospectively |
| `ST-KUTHULUN-COERCION` | M3.02 | target-on-route; authorial target; never a past event |
| `ST-POST-EMBRACE` | M4 | umbrella; umbrella only; contains four child story units |
| `ST-FIRST-NIGHTS` | M4 | required-on-target-route; authored prospectively; conditional on an actual Embrace |
| `ST-GRIEF-AND-BOUNDARIES` | M4 | required-on-target-route; authored prospectively; conditional on an actual Embrace |
| `ST-CAINITE-ENTRY` | M4 | required-on-target-route; authored prospectively; conditional on an actual Embrace |
| `ST-ETHICAL-COST` | M4 | optional; authored prospectively; conditional on an actual Embrace |
| `ST-2010-TRANSITION` | M5 | required-for-graduation-review; authored prospectively |


## 1. Cânone, autoria prospectiva e quatro níveis de conhecimento

**Fatos de fonte:** C05 está fechado; C06 não começou; Bartholomeu continua mortal e sem Abraço. As seções já existentes de M3.01 permanecem mortais. M3.02 é uma história futura separada, proposta para depois do encerramento efetivo de M3.01; nenhuma parte da transformação entra em M3.01. A esposa e os filhos existem conforme as fontes; respostas, paradeiro, conhecimento e decisões futuras deles permanecem não escritos.

**Limite da transição:** M3.01 continua operacionalmente ativa, e C06 ainda é a próxima seção planejada. A preparação de M3.02 só poderá entrar em jogo depois de M3.01 ser encerrada por jogo e a transição ser autorizada e registrada. Se a cronologia efetivamente jogada deixar o prazo impossível, a meta de Abraço fica não alcançada/alternativa; não se comprime o jogo nem se declara encerramento retroativo.

**Direção autoral aprovada:** Kuthulun é a futura Senhora Gangrel escolhida; a cultura local valoriza combate; sua reputação de nunca ter perdido desde quando era viva é direção do jogador. O rumor sobre um mortal que encara Cainitas desarmado pode atrair atenção, se uma observação e um relé causal realmente ocorrerem. A cena-alvo contém sete Gangrel, Kuthulun no centro e Bart diante dela. O confronto é coercivo e não oferece convivência segura sob custódia; lutar ou fugir pode criar chance real, incerta, de escapar. O alvo autoral, se Bart permanecer e a resolução permitir, é Kuthulun derrotá-lo e forçar o Abraço perto da morte, contra a vontade dele. Esse alvo não substitui ações do jogador, rolagens ou regras. Kuthulun começa sem dons de sangue e pode escalá-los conforme a necessidade mecânica.

**Variante aberta, limite literal:** a transportadora se liga ao Sistema Circulatório; Kuthulun sabe o que Mary sabe sobre a transportadora e a luta com o homem que perdeu um braço e sobreviveu. Este contrato não define o conteúdo exato desse conhecimento, como/quando Mary soube ou contou, rota, mecanismo, participantes, pagamentos ou qualquer outra verdade preexistente. Uma pista criada abaixo é um novo acontecimento futuro, condicional e observável; nunca deve ser apresentada como memória anterior de Mary ou Kuthulun.

**Direção autoral sobre conhecimento de Kuthulun:** a direção expressa do jogador autoriza tratá-la, no confronto futuro, como sabendo que Bart viu e contou coisas comprometedoras, incluindo apenas o âmbito delimitado pela variante aberta. Isso é uma premissa prospectiva fornecida pelo jogador, não um novo evento histórico nem licença para inventar destinatário, data, método, detalhes ou conteúdo adicional. Separadamente, qualquer relatório de Rada só entra no conhecimento de Kuthulun se a transmissão ocorrer em jogo.

**Níveis:** AGENT_KNOWLEDGE inclui este pacote; PLAYER_KNOWLEDGE exclui os segredos ainda não revelados; PC_KNOWLEDGE inclui apenas evidência realmente obtida por Bart; NPC_KNOWLEDGE inclui apenas fontes efetivamente recebidas por cada NPC. O Narrador não transfere conhecimento entre níveis sem uma cena/relé registrado.

**Desconhecidos protegidos:** conteúdo da caixa de C05; datas e espaçamentos exatos; estado interno e respostas futuras da família; conhecimento de cada NPC além do ledger individual; qualquer detalhe anterior não autorizado da transportadora. A caixa de C05 não é necessária para resolver ou avançar as histórias preparadas. Se Bart a examinar, a ação é respeitada; o conteúdo não é inventado por este pacote e não bloqueia a rota principal.

**Preparação histórica não revalidada:** `M3.01_DOSSIER_V5.json` foi revisado apenas até C04 e está stale perante o checkpoint C05. PT08 permanece preparação prospectiva não canônica, não evento e não causa para a coerção. Este pacote não usa PT08 como gatilho, evidência ou conhecimento; qualquer uso futuro exige reconciliação contra o estado então vigente.

## 2. Agentes, objetivos, recursos, limites e oposição

Todos os perfis abaixo são NPCs novos ou perfis prospectivos. As motivações descrevem a autoria futura; nenhum NPC age antes de existir uma causa e uma cena. A ordem de entrada é condicional.

| Agente | Objetivo/motivação | Recursos | Limites e oposição |
|---|---|---|---|
| **Kuthulun** | Conter uma ameaça de exposição e avaliar uma força que a cultura Gangrel valoriza; vê conversão como domínio/custódia, não como presente. A reputação de combate é direção do jogador, não prova universal de invencibilidade. | Autoridade pessoal perante seis Gangrel; escolha de escalada física e dons válidos; reputação local. | Só sabe o que fontes identificadas lhe transmitem e o limite da variante aberta; não lê mentes, não localiza Bart automaticamente, não controla a família e não pode falsificar dados. Pode perder posição política se sua coerção expuser o grupo. |
| **Rada, batedora Gangrel** | Manter desobstruído um corredor noturno que usa e impedir que confrontos mortais atraiam atenção pública. | Observação direta na rua da Oficina; bilhete e deslocamento a pé; fala pessoal com Kuthulun em encontro regular. | Não presencia ações dentro de casas; não sabe do que não observou; relatório é uma decisão sua, com conteúdo limitado ao evento; pode recusar ou atrasar o recado. |
| **Borislav, desafiante jovem** | Provar que mortais não devem impor termos à matilha e recuperar prestígio após uma disputa de rota. | Força física, provocação verbal e presença local. | Não tem autoridade para Abraçar, decidir política ou ir atrás da família; Kuthulun pode interrompê-lo; não conhece o conteúdo da variante. |
| **Vesna, guardiã de protocolo** | Manter a reunião coerente com a autoridade de Kuthulun e evitar que um encontro público vire caos. | Conhece o procedimento interno do grupo; controla ordem de fala e registro de decisões que presencia. | Não pode converter protocolo em consentimento, impedir uma fuga por decreto ou falar pela família. |
| **Arvo, observador da entrada principal** | Evitar entrada acidental de mortais e perceber quem chega pela entrada de veículos voltada à estrada. | Uma posição junto à entrada principal do pátio aberto. | Observa somente essa entrada; não controla as saídas pedestres laterais nem as aberturas internas do galpão, não fecha rotas e não persegue fora do local; não tem conhecimento independente sobre Bart. |
| **Milena, observadora** | Registrar quem iniciou cada ato e impedir que Borislav reescreva a história do grupo. | Testemunho presencial e caderno próprio. | Registra apenas o que vê/ouve; pode contestar a narrativa de Kuthulun, mas não muda resultados. |
| **Danica, tratadora de feridos** | Reduzir risco de morte irreversível depois do confronto, sem desfazer a decisão de Kuthulun. | Kit de primeiros socorros e experiência de campo. | Não garante sobrevivência nem Abraço; não transforma um resultado letal em sucesso; não atua como médica onisciente. |
| **Milan Varga, cliente prospectivo** | Conseguir avaliação honesta e manter seu sedã disponível para trabalho sem aceitar custo que não autorizou. | Carro, escolha sobre o orçamento e possibilidade de retirar ou retornar. | Não conhece sociedade Cainita; não autoriza reparo antes do preço; sua urgência não obriga Bart. |
| **Niko, ajudante da Oficina** | Entregar trabalho correto e conservar o emprego. | Acesso ao banco de trabalho e à régua usada em cada peça. | Não conhece sociedade Cainita; erro de medida é dele apenas se a cena o estabelecer; pode corrigir uma peça, não resolver mistérios externos. |
| **Jelena [NPC-CHR-001-JELENA-VOLNAYA], escriturária de Volnaya** | Corrigir uma cópia duplicada sem ser responsabilizada por um arquivo mal indexado. | Índice local, cópia carbono e horário de expediente. | Não controla a transportadora, não conhece seus trajetos ou membros; só responde ao documento que lhe é mostrado e pode encerrar atendimento. |
| **Escriturária do inventário [NPC-CHR-001-INVENTORY-CLERK-VOLNAYA]** | Corrigir o registro de turno sem assumir responsabilidade por rotinas que não conhece. | Livro de inventário e expediente do arquivo. | É uma pessoa distinta de Jelena; só responde ao registro que lhe é mostrado e não conhece o grupo Cainita ou a família de Bart sem fonte. |
| **Ilja, lacaio veterano e chamado “O Retentor” nas apresentações** | Proteger a rotina da casa Gangrel e ressentir-se de ter esperado muito tempo pelo próprio Abraço e reconhecimento enquanto um recém-chegado recebe atenção. | Ghoul veterano a serviço de Kuthulun; conhece turnos, etiqueta e apresentações; pode retirar cooperação voluntária e expressar juízo social dentro do grupo. | Kuthulun nunca lhe prometeu Abraço; não comanda Gangrel, não decide a entrada de Bart, não conhece a família ou detalhes da transportadora sem fonte e não pode impor ação ao protagonista. |
| **Mary, Mikahel e Sara** | Objetivos próprios ainda não especificados. | Somente recursos e conhecimento que fontes futuras ou cenas efetivamente registrarem. | Nenhum texto prescreve sua reação, fala, conhecimento futuro, localização ou escolha. Não são instrumentos automáticos de ameaça. |

**Identidade resolvida:** “O Retentor” é o título social de Ilja, não uma segunda pessoa. As referências a Ilja e ao Retentor neste pacote usam o mesmo agente, ledger de conhecimento, história e consequências.

### Perfil mecânico prospectivo de Kuthulun — pronto para uso futuro, sem fixar Geração

Este perfil é preparação autoral nova para a história futura, autorizada pelo jogador. Ele não atualiza as fontes históricas nem entra no estado presente. **Geração permanece UNKNOWN**: a escolha da futura Senhora e a linhagem Gangrel local não autorizam deduzi-la. Não há inferência de Geração a partir de BP, idade, cargo ou reputação.

Perfil de conflito: Força 5, Destreza 4, Vigor 5; Carisma 3, Manipulação 3, Autocontrole 4; Inteligência 3, Raciocínio 4, Determinação 4. Briga 5, Atletismo 4, Prontidão 4, Intimidação 5, Liderança 3, Sobrevivência 5. Vitalidade 8 e Força de Vontade 8. Pool físico de ataque desarmado: 10 dados antes de modificadores; todo pool de oposição é declarado junto da ação, antes da rolagem.

Potência de Sangue preparada: 2. Esse número é uma escolha autoral independente; não prova, fixa nem demonstra compatibilidade com qualquer Geração, que permanece UNKNOWN. Antes de usar a ficha em rolagens, validar a combinação com a ficha NPC vigente, a Geração quando for conhecida por fonte válida e a regra V5 então aplicável. Pela tabela corrigida oficial, BP2 dá Blood Surge +2 dados; repara 2 pontos de dano superficial por Rouse Check; concede +1 dado a testes de poderes de Disciplina; permite rerrolagem de Rouse Check apenas para poderes de nível 1; bane severity 2; sangue animal e ensacado saciam metade da Fome. A Fome é estado de cena, não valor fixo: recuperar do ledger NPC vigente ou resolver antes de qualquer Rouse Check. Disciplina preparada: Proteanismo 2, Garras Ferais. Kuthulun começa com disciplinas desativadas. Ativação exige ação, custo, Rouse Check, estado de Fome e regra vigente; nenhum poder é gratuito. O bônus de BP a testes de poderes não se aplica automaticamente a ataques físicos feitos com garras.

A ficha só vale para M3.02 depois dos gates de episódio e de autorização; uma fonte validada posterior prevalece e exige revalidação. Antes de dados, declarar ação, pool, oposição, risco e consequência; usar a engine vigente sem manipulação. O alvo autoral é Kuthulun derrotar Bart se ele permanecer, mas isso é objetivo dramático, não resultado assegurado: qualquer sucesso mecânico de fuga, interrupção ou outro resultado legal prevalece e encerra a rota como alternativa/incompleta, sem Abraço presumido. Referência de regra: tabela corrigida oficial da Renegade, https://renegadegamestudios.com/content/File%20Storage%20for%20site/VTM/BloodPotencyTable.pdf.

## 3. Contratos de história

Cada contrato fecha seu motivo, verdade, agentes, pistas, ramos e encerramento local. Uma pista que não for obtida permanece não conhecida; isso não impede o restante da crônica.

### `ST-C06-REENTRY` — retomada de M3.01, ainda sem cena pronta

**Origem/verdade:** a história devolve a iniciativa depois de C05 por meio de um pedido comum de manutenção automotiva, compatível com o código profissional confirmado de Bart. Não preenche o conteúdo da caixa, a elipse anterior nem qualquer fato passado. Não introduz Cainitas nem Abraço.

**Situação autoral futura:** Milan Varga chega à baia alugada com um sedã usado que chia ao dar partida e cuja luz de carga acende de modo intermitente. A correia do alternador está ressecada e trincada; não há correia correta no estoque. Milan precisa do carro para um turno de entregas no período seguinte e pede primeiro avaliação e orçamento; pergunta se um ajuste rápido bastaria. Ele não autoriza desmontagem, peça ou reparo sem ouvir o preço. Sua urgência é econômica e prática, não uma ameaça nem um segredo.

**Agentes e recursos:** Milan quer uma resposta honesta e uma opção que caiba no que pode pagar; dispõe do carro e pode aceitar, adiar ou retirar. Bart decide se atende, quanto cobra pelo trabalho solicitado, o que examina e que opções explica. Niko só participa se o estado vigente o estabelecer em serviço e Bart lhe delegar algo; nenhum beat depende da presença dele. Não há outro cliente ou observador necessário.

**Oposição e pistas:** o tempo até o próximo turno de Milan, a falta da peça correta e o limite entre orçamento, ajuste provisório e reparo concluído. O ruído, a luz e o estado da correia são observáveis na entrada; a causa de qualquer falha adicional não é presumida. Uma inspeção visual pode bastar para justificar a recomendação. Teste mecânico só ocorre se Bart escolher e declarar risco, pool e consequência. Não há pista sobre a caixa ou a transportadora.

**Fechos:** avaliação e orçamento entregues; reparo autorizado e concluído apenas se houver peça, tempo e trabalho efetivamente realizados; serviço agendado; recomendação recusada; carro retirado; ou conversa encerrada. O cliente pode adiar sem punição automática. Registrar somente o serviço, preço, autorização e condição realmente escolhidos. Falha de teste não inventa acidente nem impede outra opção. Não há relé a Kuthulun nesta história.

<a id="ST-MEASURE-DISPOSITION"></a>
### `ST-MEASURE-DISPOSITION` — erro de medida, trama opcional

**Verdade de bastidores:** Niko corta uma braçadeira de aço alguns milímetros curta após usar uma régua empenada. É erro de pressa, não sabotagem e não pista Cainita. A peça curta não é entregue ao cliente sem que Bart escolha como tratá-la.

**Agentes/oposição:** Niko quer conservar o emprego e esconder o erro; o cliente deseja a peça no prazo; Bart pode medir, pedir explicação, refazer, usar a peça com risco declarado ou suspender a entrega. Recursos: bancada, régua, metal restante, recibo de encomenda. Limitação: não há material ilimitado; o cliente pode recusar novo atraso.

**Pistas/descoberta:** medir a régua contra um padrão independente; comparar o corte e o pedido; ou ouvir Niko se ele decidir falar. Nenhum teste é obrigatório: inspeção cuidadosa ou pergunta direta podem bastar. Falha pode não localizar a causa, mas o defeito físico permanece verificável.

**Escalada e consequência:** cliente aguarda ou retira o pedido; Niko enfrenta correção ou perda de confiança. Sem dano pessoal automático. Bart pode deixar o serviço e fechar o fio.

**Encerramento:** peça corrigida e aceita, pedido cancelado, peça marcada para reaproveitamento, ou questão abandonada com custo conhecido. Não liga por si só à rede secreta nem a qualquer Cainita.

<a id="ST-VOLNAYA-BOUNDARY"></a>
### `ST-VOLNAYA-BOUNDARY` — índice duplicado e alcance limitado da prova, opcional

**Verdade de bastidores:** uma cópia de índice da escriturária Jelena [NPC-CHR-001-JELENA-VOLNAYA] recebeu o mesmo número de fólio duas vezes por erro de transcrição; ela reteve o segundo papel para não ser culpada pelo índice. O papel novo que pode surgir numa investigação futura contém um campo nominal que associa a transportadora ao **Sistema Circulatório**. Isso é uma pista prospectiva, e somente prova textual dessa associação. Não revela rota, método, financiador, quantidade, calendário, outros participantes ou o conteúdo anterior da conversa de Mary.

**Agentes/oposição:** Jelena quer corrigir o próprio registro sem acusação; Rada pode passar diante do balcão como visitante, mas não tem autoridade arquivística. O obstáculo é expediente, papelada e a escolha de Bart de mostrar uma cópia. A escriturária não entrega outros registros sem causa e não conhece a política da transportadora.

**Pistas alternativas:** a cópia carboneada com número repetido; uma segunda conferência no índice público local; ou a explicação de Jelena depois que Bart aponta a duplicidade. Nenhuma requer reler material sigiloso ou invocar conhecimento de Kuthulun. Descoberta antecipada do campo fecha o mistério local diretamente; não acrescenta detalhes além do campo.

**Escalada:** se Bart pressionar, Jelena pode encerrar o atendimento; se fizer acusação, ela chama um superior do arquivo. Se não investigar, o papel fica no índice e a história termina silenciosamente. Nenhum agente recebe o resultado sem transmissão observável.

**Encerramento:** cópia corrigida e observada, pista nominal obtida, atendimento encerrado sem prova, ou desistência. A solução do duplicado fica fechada; o que o Sistema Circulatório faz além da associação impressa permanece fora do contrato e não é uma investigação ativa.

<a id="ST-GANGREL-ATTENTION"></a>
### `ST-GANGREL-ATTENTION` — disputa de passagem, primeiro conflito Cainita

**Origem/gatilho:** numa noite posterior à retomada, uma peça longa aguarda retirada no beco lateral da Oficina. Rada chega por causa do bloqueio de um corredor de passagem que ela realmente usa. Borislav, acompanhando-a, interpreta qualquer exigência de Bart para permanecer como desafio. O conflito começa por circulação da rua, não por boato onisciente.

**Verdade/objetivo:** Rada quer liberar a passagem e ir embora; Borislav quer provocar uma demonstração de força; Kuthulun não está presente. Bart pode mover a peça, discutir, pedir ajuda ao cliente, recusar, ameaçar, enfrentar ou encerrar a conversa. Nada presume luta.

**Observação e relé causal:** Rada e Borislav veem somente o que acontece no beco. Se Bart confrontar Borislav desarmado e a ação demonstrar capacidade extraordinária, Rada escolhe reportar, por sua função de batedora e por temer que o próximo encontro seja mais perigoso. Ela leva o relato pessoalmente a Kuthulun no Pátio do Lastro, na próxima reunião regular do grupo. Conteúdo permitido: local, conduta vista, presença/ausência de arma e resultado observável; não inclui causa que não viu, conteúdo de C05, família ou detalhes da transportadora. O relato pode atrasar; o atraso é registrado. Se não houver demonstração, Rada relata apenas a obstrução, sem rumor de combate.

**Descoberta alternativa:** Bart pode pedir a Rada que marque uma conversa; ela diz que pode transmitir o pedido, sem prometer resposta. Se ela não transmite, nenhum convite existe. Não há testemunha invisível, rede telepática nem contato de seguimento automático.

**Consequências/fecho:** passagem liberada, disputa encerrada, confronto interrompido ou Bart afastado. Se houver lesão, aplicar a mecânica e registrar dano real. A história termina após a saída dos dois Gangrel e um relato de quem realmente decidiu transmiti-lo. Se não houver contato/relé, a rota de K permanece quieta; não se inventa atenção.

### `ST-KUTHULUN-PRECEDENCE` — primeira aproximação, antes da coerção

**Gatilho:** Kuthulun recebe o relato limitado de Rada ou Bart originou pedido de apresentação e Rada confirma a transmissão. Ela decide testar a fonte antes de abrir reunião maior. Rada entrega pessoalmente à Oficina um cartão com local e janela relativos no Pátio do Lastro; não procura Bart em casa nem o captura. Se nenhum cartão é entregue, esta história não começa.

**Local/participantes:** galpão aberto do Pátio do Lastro, com Kuthulun e Rada; Milena pode observar da área de ferramentas, sem entrar no diálogo. Bart chega apenas se escolher. A reunião é audível a terceiros próximos e não presume segredo perfeito.

**Conflito/escolhas:** Kuthulun pergunta pelo evento que gerou o contato e quer decidir se Bart é uma exposição ou um interlocutor. Pode ouvir, contestar, mentir, sair, solicitar nova conversa ou recusar. Bart observa que Kuthulun controla o tempo da conversa e que Rada trouxe o convite; não tem como saber o que K recebeu além do conteúdo relatado.

**Oposição/escalada:** se Bart acusa Rada ou Kuthulun, Rada esclarece somente seu próprio relatório; Kuthulun pode encerrar. Se ele abandona o encontro, ninguém o segue. Se aceita conversa futura, Kuthulun envia uma resposta explícita por Rada. A ordem não contém ameaça contra a família nem exigência de conversão.

**Fecho:** reunião concluída, recusada, abandonada ou sem resposta posterior. Um próximo encontro só existe se convite/resposta efetivamente chega e Bart decide comparecer. O fio sobre a segurança do grupo permanece aberto.

<a id="ST-KUTHULUN-COERCION"></a>
### `ST-KUTHULUN-COERCION` — encontro de sete Gangrel e alvo de transformação futura

**Causa e presença:** somente se o contato anterior produziu convite entregue por Rada, ou Bart solicitou e recebeu uma apresentação. Rada retorna à Oficina e entrega pessoalmente um cartão para o Pátio do Lastro. Bart escolhe se vai. Sem comparecimento, não há encontro nem captura fora de cena; a rota fecha como não realizada/alternativa.

**Local e formação:** galpão de pesagem desativado num pátio industrial aberto, sem perímetro fechado. Duas portas de pedestres e a abertura de carga ficam visíveis; cada uma leva a uma rota física distinta para fora do galpão, e as saídas laterais do pátio não são fechadas. Arvo observa a entrada principal de veículos junto à estrada; essa posição não bloqueia as três rotas nem cria captura automática. Sete Gangrel: Kuthulun no centro; Rada, Borislav, Vesna, Arvo, Milena e Danica em posições reconhecíveis. Bart fica diante dela ao aceitar o convite. Linhas de visão, obstáculos e posições são declarados antes de testes; nenhum acesso secreto surge durante a cena.

**Verdade e motivação:** Kuthulun age conforme a direção autoral do jogador e o conhecimento estritamente delimitado pela variante aberta: considera comprometedor o que sabe e quer conter uma exposição. A preparação não inventa como, quando ou por quem ela soube; qualquer dado além desse limite depende de fala ou transmissão efetiva. Rada pode acrescentar apenas observações que realmente relatar. Ela valoriza a força de Bart como combatente, mas seu interesse é posse/controle, não convite romântico nem presente. Seu código de custódia é que uma ameaça deve ser incorporada ou removida; ela não tem poder de localizar pessoas que Bart protege nem de cumprir uma ameaça fora do alcance que efetivamente conhece. O grupo discorda sobre a maneira: Borislav quer luta imediata; Vesna quer uma ordem observável; Milena quer registrar a origem dos fatos.

**Escolha coerciva no encontro:** Kuthulun exige custódia e submissão à sua autoridade; não oferece via segura de convivência independente e o Abraço não depende do desejo ou consentimento de Bart. Recusa verbal, silêncio, negociação sem submissão ou outra resposta que o deixe no local conta como não submissão. Kuthulun comunica que a recusa termina em morte e ameaça genericamente os vínculos que Bart tenta proteger. A ameaça faz parte da direção autoral futura, mas não demonstra que ela conhece nomes, parentesco, endereço, paradeiro ou planos de qualquer familiar; ela não descreve dano já feito e não pode agir sobre alvos que não localizou. Lutar ou fugir abre possibilidade real, mas não garantida, de escapar. Se Bart permanece sob controle do grupo, Kuthulun começa sem dons de sangue e escala força física e dons legalmente disponíveis conforme necessário, buscando derrotá-lo e deixá-lo perto da morte; ela o Abraça contra a vontade somente se a sequência mecânica vigente ainda permitir. Bart não tem rota de vitória sobre Kuthulun no desenho autoral, mas o Narrador não falsifica rolagens, dano ou incapacidade.

**Limites mecânicos e sequência:** antes de qualquer rolagem, declarar ação, posição, pool, oposição, risco, regra e consequências possíveis para cada participante que efetivamente agir; resolver iniciativa e deslocamentos conforme a engine vigente. Não presumir que seis acompanhantes imobilizam Bart, bloqueiam todas as saídas ou agem em uníssono. A fuga exige testes e resposta NPCs apenas se suas posições, ações e recursos permitirem. Não garantir fuga, derrota, morte, sobrevivência ou Abraço contra a resolução real. O alvo é que, se Bart permanecer e for derrotado, Kuthulun inicie o Abraço enquanto ele ainda estiver em estado mortal/dying e antes de Final Death: executar então a sequência exigida pela regra V5 vigente, incluindo drenagem e oferta da Vitae de Kuthulun, usando o estado e ledger efetivos. Este texto não inventa limite de Vitalidade, contagem de ações/rolagens nem limiar de “perto da morte”. Se Final Death ocorrer primeiro, ou a sequência não for legal, não há Abraço nem ressurreição; fechar como alternativa divergente. Se Bart escapa, a rota coerciva falha e só se aplicam consequências observadas; não há perseguição automática. Só registrar transformação como evento futuro após resolução real, com consentimento=false e proveniência.

**Fecho e condição temporal:** concluído com fuga, interrupção, resultado letal sem Abraço, Abraço forçado mecanicamente válido, ou recusa/ausência antes de entrar. Permanecer no local depois de recusar não gera saída segura implícita; é o ramo de coerção descrito acima. A meta autoral é que o último ramo aconteça após o encerramento de M3.01 e antes de 25/12/1970. Não fixar uma data. Se o tempo jogado tornar o prazo impossível, registrar desvio; não comprimir luto ou mudar datas já jogadas.

<a id="ST-POST-EMBRACE"></a>
### `ST-POST-EMBRACE` — agrupador editorial

Contém `ST-FIRST-NIGHTS`, `ST-GRIEF-AND-BOUNDARIES`, `ST-CAINITE-ENTRY` e `ST-ETHICAL-COST`. Só é percorrido depois de um Abraço realmente registrado. Não cria evento, cena, estado ou data. A sequência padrão dá noites para sobrevivência, depois semanas/meses para luto e adaptação; cada cena pode ser jogada em ordem alternativa se a causalidade permitir. A história de Kuthulun não decide a reação da família.

### `ST-FIRST-NIGHTS` — sobrevivência e primeiro custo

**Verdade:** a nova condição traz fome e sentidos difíceis; o grupo tem uma sala de manutenção no Pátio do Lastro e um pequeno estoque de sangue animal fechado, cuja quantidade é contada ao abrir. Danica quer evitar que Bart fuja ferido; Kuthulun quer mantê-lo vivo por sua própria decisão, não por benevolência.

**Opções/risco:** Bart pode aceitar a sala, sair, pedir sangue, recusar alimentação ou exigir distância. O Narrador usa a ficha real pós-Abraço e a regra atual para determinar se o sangue animal reduz Fome conforme BP; não garante efeito nem reduz Fome automaticamente. Sem alimento, efeitos de fome/frenesi seguem a regra, sem forçar uma escolha narrativa. Danica presta somente cuidados que a regra e seu kit permitem.

**Fecho:** permaneça sob cuidado, saia, aceite fonte válida ou escolha não se alimentar. Registrar Fome/dano apenas com mecânica e evento real. Nada sobre Mary ou filhos é comunicado automaticamente.

### `ST-GRIEF-AND-BOUNDARIES` — perda da vida familiar

**Verdade prospectiva e condicional:** quando Bart escolhe iniciar ou aceitar a conversa, Ilja pode oferecer a chave da porta de serviço da Oficina, ainda sob controle Cainita; Bart só a recebe se aceitar. A posse da chave não garante entrada, passagem segura ou controle da porta. Se Bart recusar, não houver conversa, ou Ilja não estiver disponível no estado da cena, nenhuma transferência ocorre; telefone, porta pública, pedido de escolta e outras ações escolhidas continuam alternativas reais. Ilja cobra que Bart defina um limite de contato com a vida anterior e ressente ter esperado anos por reconhecimento, sem querer negociar privilégios pelo recém-chegado. Não existe carta, telefonema ou ação de família predeterminada.

**Local/participantes:** sala de ferramentas superior da Oficina, em horário fechado; Bart, Ilja e, se presente por decisão/estado, Rada. A porta pública e um telefone ficam visíveis, sem indicar que alguém atende.

**Conflito/escolhas:** Bart pode proteger um objeto que ele próprio trouxer, pedir escolta, tentar ir até a família, usar o telefone, recusar contato ou confrontar Ilja. Ilja explica riscos que ele realmente conhece; não inventa ameaça já executada. Se Bart tenta contato, preparar a interação a partir da decisão e do estado da família então conhecido, sem fala/resposta predeterminada. A família pode não estar disponível; isso é uma contingência, não rejeição presumida.

**Consequências/fecho:** o limite escolhido fica registrado como intenção do protagonista somente se ele o disser/agir; resposta familiar só entra por cena real. O fio fecha quando Bart escolhe uma ação ou escolhe não agir e registra o custo vivido por ele, sem exigir resolução da família.




### `ST-CAINITE-ENTRY` — provação social e ressentimento

**Verdade:** no primeiro encontro formal de grupo após o Abraço, Vesna exige que a nova cria responda a uma disputa simples de prioridade: uma tarefa de vigia e um turno de recurso só podem ser atribuídos a uma pessoa. Ilja foi o mais antigo na fila e acredita que Kuthulun o contornou. Não há punição escondida automática; o conflito é status e confiança.

**Local/participantes:** sala comum do Pátio do Lastro, com Kuthulun, Vesna, Ilja, Rada e Milena; Borislav pode assistir sem voto. Entrada condicionada a um Abraço real e a convite/convocação documentada.

**Escolhas e comportamento:** Bart pode aceitar a tarefa, negociar divisão, devolver o turno a Ilja, pedir justificativa ou recusar. Ilja argumenta com exemplos de sua espera, pode reter cooperação pessoal, mas não fala por todos. Vesna lê os critérios e registra o resultado. Kuthulun pode defender sua escolha ou permitir que a disputa continue. Nenhuma rolagem substitui a decisão.

**Fecho:** tarefa aceita, repartida, recusada ou adiada com responsável identificado. O grupo atualiza confiança somente conforme ações observadas. Bart pode pedir ajuda para a tarefa; receber ajuda demonstra interdependência sem impor sentimento ou consentimento.


#### Espera pelo próprio Abraço

Ilja, chamado “O Retentor” nas apresentações, é um ghoul veterano a serviço de Kuthulun. Ele permaneceu ao lado dela por muito tempo e esperou que a lealdade lhe rendesse o próprio Abraço, sem que Kuthulun jamais lhe fizesse essa promessa. Quando Bart recebe prioridade, Ilja sente que foi ultrapassado. Busca reconhecimento e acesso; sua influência limita-se à etiqueta, às apresentações e ao acesso social de sua função. Não comanda Gangrel, não decide a entrada de Bart, não quer matá-lo e não conhece detalhes sobre a família ou a transportadora sem fonte adquirida. Pode guardar ressentimento, aceitar um reconhecimento franco ou recuar se Bart não entrar no jogo de status; nenhuma resposta resolve a trajetória sozinha.

## `ST-ETHICAL-COST` — inventário adulterado e promessa limitada, história opcional

**Origem e verdade de bastidores:** depois de um Abraço real, Kuthulun recebe de Vera, mensageira Gangrel, uma notificação do arquivo público de Volnaya: uma cópia de inventário associa o uso noturno de um galpão ao grupo. A cópia não contém nomes ou dados de parentes. A funcionária de turno [NPC-CHR-001-INVENTORY-CLERK-VOLNAYA] não causou o uso do galpão nem conhece o grupo; seu nome aparece como responsável pelo livro. Ela é uma NPC distinta de Jelena [NPC-CHR-001-JELENA-VOLNAYA], da trama `ST-VOLNAYA-BOUNDARY`; nenhuma identidade, observação, relação ou transmissão é fundida entre elas. Kuthulun quer impedir que uma consulta futura identifique a rotina do grupo, e pede a Bart que troque uma folha de inventário por uma cópia com um horário diferente. A troca é fraude documental, cria risco concreto de responsabilização para a escriturária e não apaga o original do arquivo. Vera comunica o pedido a Bart em cena; não existe cópia, investigação ou conhecimento anterior presumido.

**Agentes, objetivos, recursos e limites:** Kuthulun quer reduzir uma exposição operacional do grupo sem prometer controle sobre terceiros. Vera transporta a cópia de notificação e só sabe o conteúdo que recebeu. A escriturária [NPC-CHR-001-INVENTORY-CLERK-VOLNAYA] quer conservar o emprego e corrigir o inventário quando informada, mas não tem autoridade sobre o grupo Cainita. Bart tem a cópia que lhe for mostrada e pode pedir prova, comparar registros, falar com a escriturária ou encerrar a conversa. Ninguém sabe quem são ou onde estão os familiares de Bart por causa deste contrato.

**Gatilho causal e pressão familiar:** a história só é oferecida se Bart, em conversa anterior jogada, disser a Kuthulun que quer proteger a família, ou se ele trouxer essa preocupação à conversa com Vera. Se isso ocorrer, Kuthulun pode oferecer uma promessa estreita: seu próprio grupo não procurará nem contatará familiares de Bart enquanto a promessa for respeitada. Ela condiciona a promessa à discrição sobre o grupo e pede a troca fraudulenta. Isso cria a escolha entre aceitar um ato que pode prejudicar uma pessoa inocente para obter um limite de conduta do grupo que o Abraçou, ou recusar e preservar o registro. A promessa não é segurança contra terceiros, não exige que Bart revele identidades ou localização e não muda o que a família sabe ou faz. Se Bart não revelar essa preocupação, a tarefa pode ser apresentada como proteção do grupo, sem barganha familiar.

**Pistas e meios de descoberta:** notificação de consulta ao inventário; conferência da cópia com o livro em expediente; pergunta direta à escriturária; ou recusa de Vera em fornecer prova. A descoberta antecipada da folha confirma somente o horário e a associação textual. Nenhuma dessas vias revela rota, mecanismo, outros participantes ou resposta da família. Sem prova disponível, a história fecha como oferta não verificada, sem exigir investigação posterior.

**Escalada e oposição:** Vera pode pedir uma resposta e aguardar até o fim do expediente; a escriturária pode encerrar atendimento se pressionada; Kuthulun pode manter ou retirar sua promessa em resposta à conduta observada, sem transformar recusa em ameaça automática. Alterar a folha sem acesso real ao arquivo não tem sucesso presumido. Uma falha não cria acusação nem dano à família. Abandono encerra o encontro e conserva o estado documental conhecido.

**Consequências e condições de encerramento:** (a) Bart aceita e a folha é alterada somente se a ação e o acesso forem estabelecidos; a escriturária corre o risco definido pela evidência, não uma punição automática; (b) ele recusa e a promessa pode ser retirada, mas não há retaliação automática; (c) ele alerta o arquivo, que inicia uma revisão do inventário e pode tornar a rotina Cainita mais visível; (d) ele pede outra condição ou abandona, encerrando a oferta sem resolver o registro. Fecho local é comprovado pela escolha, resposta observada e estado do documento; não há cadeia obrigatória de investigação. A trama é opcional, não protege automaticamente a família e não bloqueia a conclusão em 2010.

<a id="ST-2010-TRANSITION"></a>
### `ST-2010-TRANSITION` — conclusão finita da criação guiada

**Verdade:** a criação não precisa resolver todas as tramas; seu propósito é revisar o personagem e oferecer entrada real na crônica principal em 2010. O conflito é a diferença possível entre ficha-alvo, estado jogado e fios ainda abertos.

**Agentes/recursos:** Bart e Narrador; ficha atual, ledger de XP, histórico reconciliado, lista de estados e autorizações. Um membro Cainita da rede só participa se seu status em 2010 estiver então estabelecido; não se presume que qualquer NPC sobreviveu, permaneceu ou mudou de posição.

**Pistas/opções:** conferir cada campo por evidência; mostrar ao jogador objetivos concluídos, pendentes ou não escolhidos; escolher uma última oportunidade de desenvolvimento já autorizada ou encerrar com desenvolvimento parcial; entrar na crônica principal, prolongar por escolha explícita com objetivo e critério, ou parar a criação como incompleta. Sem rolagem obrigatória.

**Fecho:** transição concluída quando estado, ficha, XP, relações e fios são reconciliados e o jogador escolhe entrar em 2010; alternativa documentada se não entrar. A história não cria pontos, XP, recursos, datas ou parentesco. Encerramento independente de todas as tramas opcionais.

## 4. Encerramento transversal e proveniência

Uma trama encerra quando a condição local acima é comprovada por evento registrado, escolha explícita, saída/recusa ou fechamento em quietude. “Não encontrada” é válido; “o Narrador inventará depois” não é. A ausência de pista não se torna conhecimento. Falha de investigação não bloqueia a história principal.

**Proveniência vigente:** a autorização de autoria e acesso dos agentes vem de `novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_AGENT_ACCESS_V003.json` (Git blob `9526af065467588c4c8ce5cb0013d199868542a1`); V001/V002 são apenas predecessores históricos. V013 deriva diretamente de D07 V012 (blob registrado no cabeçalho), usa D06 V019 como bíblia vigente e D04 V009 como fonte de `contract_ref`; nenhuma versão histórica de D04/D07 ganha autoridade atual por ser mencionada em referência antiga. A decisão V003 autoriza autoria prospectiva, não retcon. O crosswalk preserva os `plot_id` próprios de D04 e liga unidades somente pelo fragmento `#ST-*` em `contract_ref`. Nenhuma cena, estado ou consequência passada é alterada. Conteúdo prospectivo segue sujeito à revisão adversarial D11. A aprovação de preparação não abre C06 nem inicia uma cena.


## Proveniência mecânica V5

A preparação prospectiva usa a tabela corrigida oficial de Blood Potency publicada pela Renegade: [V5 Blood Potency Correction](https://renegadegamestudios.com/content/File%20Storage%20for%20site/VTM/BloodPotencyTable.pdf). O perfil autoral deste pacote escolhe Blood Potency 2 como valor independente e mantém Generation UNKNOWN; a tabela só valida os efeitos associados ao BP escolhido. Ela não prova geração, idade ou status histórico. Rouse Checks, Hunger, poderes e pools dependem do estado e das regras vigentes no momento futuro de jogo. O perfil não atualiza a ficha atual nem autoriza uma cena.


## Contratos preservados de V011 — encerramento M3.01, custo opcional e perfil mecânico

**Versão de origem:** V011. **Sucessora atual:** V012; predecessor direto e blob SHA-1 registrados no cabeçalho. **Proveniência:** autoria prospectiva autorizada pela decisão V003, sem transformar UNKNOWN histórico em fato; nenhuma cena, estado, morte ou Abraço é registrado por este texto.

- Se Bart sair durante a primeira conversa, a conversa local se encerra. O NPC não aprende informação adicional; não procura Bart em casa nem o captura, e não inicia perseguição. Não há novo contato sem causa e transmissão já estabelecidas no contrato aplicável.
- Se uma rolagem real produzir estado incompatível com o final-alvo autoral, prevalece a mecânica: não falsificar morte ou Abraço; classificar a rota como divergente e encerrar o trajeto dessa forma. Não há rerrolagem compulsória, fraude de resultado ou ressurreição narrativa.

## Cross-story contract anchor

<!-- D07-ADVERSARIAL-CONTRACT-ROOT -->

This anchor resolves cross-story adversarial tests against the full truth package. Each test must still cite a concrete pass criterion and the reducer must satisfy its declared assertions. Agent knowledge does not become PC or NPC knowledge; only reconciled canon and the bounded approved variant may supply historical facts; prospective truth never rewrites a played event. No prepared outcome overrides player action or applicable V5 resolution.
