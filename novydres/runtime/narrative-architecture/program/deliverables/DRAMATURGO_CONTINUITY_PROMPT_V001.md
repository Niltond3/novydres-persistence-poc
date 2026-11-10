# Briefing ao Dramaturgo — continuidade de Bartholomeu Krauser (CHR-001)

## Escopo deste pedido

Planeje a continuidade de Bartholomeu a partir do checkpoint aberto de M3.01. Entregue uma proposta de fases, conflitos, preparação causal, transição para o Abraço e consequências familiares, sociais e Cainitas. Isto é planejamento documental. **Não escreva uma cena, diálogo ou prompt de Narrador; não inicie ciclo de Narrador; não peça nem alegue permissão de cena.**

Use as fontes candidatas abaixo apenas para planejamento. Elas não foram promovidas a fontes operacionais. Não acesse, cite, resuma, infira nem revele conteúdo secreto. Se qualquer elo depender de uma verdade oculta, marque-o como bloqueado e proponha somente uma alternativa aberta compatível, sem preencher a lacuna por invenção.

## Fontes verificadas

Os hashes abaixo são Git blob SHA-1. O HEAD documental de entrada foi `3101f183c456a3cf0f188dd2a70ca50e3290092f`; o HEAD de `master` lido foi `735fe5d52e2761c4d492fe873a4b6bbcce17654a`.

| Papel | Caminho e versão | Blob SHA-1 |
|---|---|---|
| Fonte candidata de M3.01, preserva C01–C05 e retima o período | `novydres/runtime/narrative-architecture/program/deliverables/source-candidates/M3.01_v006.source.txt` | `8b72355fb8242b4d35994bc76ced8af1811b85cf` |
| Estado candidato limitado, sem reinterpretação de v043 | `novydres/runtime/narrative-architecture/program/deliverables/source-candidates/state_v044.source.txt` | `6dad4e47da3eeb9f59380e895eeebf15894ab785` |
| Reconciliação de fontes e proveniência | `novydres/runtime/narrative-architecture/program/deliverables/D06_SOURCE_RECONCILIATION_V001.json` | `201b223ccb88e07a308c6c5c06ec5fab037acdc0` |
| Cursor operacional lido em `master` | `novydres/MANIFEST_V47.json` | `6d00581981b406ec30bd0138928248965b083cc7` |
| Checkpoint aberto: C05 fechado, C06 não iniciado, Bart mortal, Abraço não ocorrido | `novydres/chronicles/CHR-001/orchestration/CYCLE_V0033.json` | `51afa7fa15ba7dc49a863dfe6f6bb0c539014a6a` |
| Estado aberto corroborador | `novydres/chronicles/CHR-001/LIVE_v037.json` | `3c51465d548484f0bbf5a42cd7d6611f0b3bb85e` |
| Índice do evento e das fontes correntes | `novydres/chronicles/CHR-001/HISTORY_INDEX_v037.json` | `80e73aa4204c8844ff8e7dfa8a7bd3193586bbbf` |
| Limites de conhecimento de Mary e do homem ferido | `novydres/chronicles/CHR-001/knowledge/NPC_KNOWLEDGE_PROVENANCE_V21.json` | `679298fec1da012572f25cfd9b9ae0a37df8586a` |
| Senhora futura escolhida pelo jogador | `novydres/chronicles/CHR-001/character/FUTURE_SIRE_PLAYER_SELECTION_V1.json` | `046e275386e48924a404ce5f8fc5f96839cbcdc4` |
| Vocabulário aberto da linhagem Gangrel urbana | `novydres/world/lineages/GANGREL_URBANO_NOVYDRES_V1.md` | `4129858b8cc1d360189df7bf34c2be8adaac769b` |

Registro de integração D12 usado para checar gates: `HANDOFF_D12_V001.json` (blob `c08c91ddf19d63e44e60d3b2448e212b00141b64`), `AUDIT_D12_V001.json` (`67aed57c8dbf4ed4c24dabddd33c8b35716bed3c`) e `D12_RELEASE_CANDIDATE_V001.json` (`0e1d89d8b303305bddc6d6a877ba95b4b8c6eb6c`). Última revisão prévia, V004: `HANDOFF_D12_V004.json` (`be4a3d4b499ce643f51a346baeaf6d39ec4ecde0`), `AUDIT_D12_V004.json` (`bdb5b7a6a9995104f093d19a2096726aef2e6204`), `D12_RELEASE_CANDIDATE_V004.json` (`a1e9179c801ab2784ee9eb9ff97faa69377f4ce7`) e `D12_VALIDATE_V004.py` (`198108985e7fdc6853bf12526981a903ba8d95dd`, 62/62 verificações na execução reproduzida). Os registros locais históricos lidos foram `execution-manifest.json` (SHA-256 `0286dad22a87a973de539d9ce95670983e283dba600f94069ae49cd058731d47`) e `CHR001_D05-D12_RUN_STATE.json` (SHA-256 `87249ad00b4e7ada06b841067cca8c520aeea89a860a5ac6016bbde19c252816`). São trilha de execução, não canon diegético.

## Cronologia e limites documentais

- A reconciliação de ponteiro confirmou `MANIFEST_V47` → `CYCLE_V0033`. O campo `MANIFEST_V46` dentro do ciclo é referência histórica. O ciclo aponta DRAMATURGO, com C05 fechado e C06 ainda não iniciado.
- A fonte v005 de M3.01 dizia “fim dos anos 1970”. A cópia candidata v006 preserva os acontecimentos e a ordem de C01–C05, situando M3.01 inteiramente antes de 1970. Bartholomeu permanece mortal em todas essas cenas; nenhum Abraço aconteceu nelas.
- O alvo autoral aprovado é um Abraço forçado por Kuthulun antes de 25/12/1970, contra a vontade de Bartholomeu. É alvo futuro, não evento estabelecido. Datas civis exatas, intervalos entre conflitos e data do Abraço continuam desconhecidos.
- A referência chamada `state_v043.source.txt`, blob `46612796f44c9b75cbd7ab43854dcec33283804a`, começa como STATE v019 / M2.03 e contém marcadores explícitos até v041 / M3.01 C03; não traz checkpoint formal v042/v043 nem estado formal de C05. Não trate seu conteúdo antigo como o estado atual. O candidato state_v044 recupera apenas o checkpoint que CYCLE_V0033, LIVE_v037 e HISTORY_INDEX_v037 corroboram.
- Uma nota de C03.15 em v005 invocava princípios norte-americanos de proteção ocupacional “dos anos 1970”. v006 marca a base temporal/legal como anomalia não verificada, sem substituí-la por uma afirmação histórica. Não use essa nota como fundamento dramático.
- O identificador de evento contendo `2026` é identificador de persistência; não determina data diegética.

## Fatos estabelecidos, direção autoral e incógnitas

**Estabelecido nas fontes abertas:** Kuthulun, “A Lua de Sangue”, é a Senhora futura selecionada pelo jogador. Bartholomeu Krauser é mortal no checkpoint, é marido de Mary Krauser e pai de Mikahel e Sara. A linhagem Gangrel é um plano futuro, não uma revelação já feita a Bartholomeu. O índice de conhecimento registra que Mary viu documentos/informações sobre a Volnaya e ouviu a versão de Bartholomeu sobre a transportadora e sobre ferir um homem e levá-lo ao hospital. O índice também registra que esse homem reapareceu depois com os dois braços; não estabelece que Mary saiba dessa reaparição.

**Direção autoral do jogador, a preservar como proposta e não como evento/canon independente:** tratar Kuthulun como Anciã Gangrel da cidade, com reputação de nunca ter perdido luta desde quando era viva; a cultura Gangrel local valoriza força de combate e tem caráter militar; rumores de um mortal que enfrenta Cainitas desarmado despertam atenção; a transportadora se liga ao Sistema Circulatório, rede secreta Ventrue que fornece sangue a quem pode pagar; Kuthulun sabe que Bartholomeu viu e contou fatos que ameaçam a segurança da sociedade, inclusive o que Mary sabe sobre a transportadora e sobre a luta com o homem que perdeu um braço e sobreviveu; o Abraço ocorre após derrota imposta quando ele está perto da morte, sem depender de desejo ou consentimento.

As fontes consultadas confirmam a identidade futura de Kuthulun, mas **não confirmam independentemente** a reputação de invencibilidade, o título/cargo de Anciã, o rótulo de Primogênita, a cultura militar de toda a cidade, a ligação da transportadora ao Sistema Circulatório nem o alcance exato do conhecimento de Mary ou de Kuthulun. A fonte de linhagem aberta sustenta adaptação Gangrel urbana à confrontação, não todas essas afirmações. Preserve-as como direção autoral; desenhe apenas os elos de aquisição que possam ser sustentados por informação aberta.

**Desconhecido ou não estabelecido:** datas civis; ritmo e ordem dos conflitos futuros; como rumores circulam; como Kuthulun obtém informações; se Mary conhece o retorno do homem com os dois braços; como Bartholomeu descobre a conexão de transporte e sangue; local, duração e resultado de eventuais tentativas de fuga; estado posterior da família, dos lacaios e das relações Cainitas. Não converta nenhuma dessas lacunas em fato preexistente.

## Trabalho solicitado

Proponha uma continuidade em fases, com encadeamento causal, ritmo e espaço entre os acontecimentos:

1. **Preparação gradual:** parta do checkpoint documentado. Proponha um ou dois conflitos adicionais com Cainitas antes do Abraço, incluindo pelo menos um Gangrel. Mostre como a reputação de Bartholomeu se forma por consequências observáveis e por relatos cuja circulação seja plausível; não faça todos os Gangrel saberem o mesmo sem uma rota de informação.
2. **Transportadora e informação:** desenhe uma trilha aberta, gradual e verificável que permita revelar a conexão com o Sistema Circulatório como parte da direção autoral. Separe o que Bartholomeu vê, o que Mary ouviu, o que terceiros alegam e o que poderia ser corroborado. Se a conexão depender de conteúdo secreto, pare nesse elo e marque-o bloqueado; não acesse nem revele a verdade oculta.
3. **Pressão e confronto candidato:** preserve a imagem concebida pelo jogador de aproximadamente sete ou oito Gangrel, Kuthulun no centro e Bartholomeu diante dela. Ela considera a exposição de informações — inclusive o que a esposa sabe — uma ameaça à segurança da sociedade. A moldura é coerciva, sem saída segura: lutar, talvez abrir uma chance de fuga limitada, ou recusar e enfrentar morte/ameaça à família. Kuthulun pode começar sem dons de sangue e escalá-los se necessário; Bartholomeu não tem como vencê-la. Ela o derrota e o Abraça quando ele está perto da morte. Não transforme resistência em consentimento nem dê a Bartholomeu vitória sobre Kuthulun.
4. **Consequências e continuidade:** reserve tempo narrativo depois do Abraço para a ira e o luto por perder a vida familiar, a ameaça ou separação dos vínculos humanos, a inveja/ressentimento de lacaios que esperaram pelo Abraço, as provações de posição e pertencimento Cainitas, e a adaptação ao novo estado. Desenvolva a aprendizagem de que ele não resolve tudo sozinho e talvez precise aceitar atos que rejeita para proteger a família. Não determine automaticamente sobrevivência, destino familiar, cargo, poderes, relações, lealdades ou aceitação social.
5. **Calendário:** proponha janelas e espaçamento que caibam no objetivo de Abraço forçado antes de 25/12/1970 e deixem espaço real para drama familiar, ingresso e adaptação Cainita. Marque cada data proposta como nova proposta, não como fonte histórica. M3.01 permanece todo antes de 1970 e Bartholomeu mortal durante todo o ciclo.

## Formato da resposta

Entregue: (a) fases em ordem com finalidade dramática; (b) por fase, conflito/pressão, causa, informação disponível e consequência; (c) trilha de rumor e descoberta, identificando emissor, receptor e grau de certeza; (d) janela temporal proposta, com incertezas explicitadas; (e) consequências humanas e Cainitas a explorar; (f) lista final de dependências bloqueadas e fatos que exigiriam nova evidência/decisão autoral.

Não escreva prosa de cena, falas, rolagens, transcrição nem conteúdo de Narrador. Não altere o checkpoint operacional, não comece C06, não ative D07, não promova nada a `master` e não confunda `READY_FOR_DRAMATURGO` com `SCENE_READY` ou `NARRATOR_PERMISSION`. Este briefing não concede permissão para cena.
