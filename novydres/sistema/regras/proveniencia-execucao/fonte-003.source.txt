# NOVYDRES / CHR-001 — AUDITORIA DE GOVERNANÇA PARA EXECUÇÃO DE CENAS V1
Data: 2026-11-03. Escopo: novos contratos locais de execução, somente ChatGPT Web + conector GitHub.
Baseline auditado: master 78c1524307197f73db44f9f0faedd3c6df89ecdb.
Status: AUDITORIA DOCUMENTAL; sem evento narrativo, compra ou recuperação.

## Fontes examinadas (não substituir por versões históricas)
- novydres/.AGENT.md e novydres/.CONTEXTG.md: guardrails G01–G24, agência, hierarquia, copy-on-write; checkpoints antigos são históricos.
- novydres/migration/MIG-DEC-002_GITHUB_PRIMARY_ACTIVATION_V1.md: GitHub é fonte textual primária; Drive textual inativo.
- novydres/runtime/GITHUB_PRIMARY_CONTRACT_V4.md: bootstrap e regras locais posteriores, incluindo G25–G27.
- novydres/governance/decisions/DECISIONS_STATE_V9.source.txt: DEC-CR-014/015/016/017/018/019/020.
- novydres/runtime/PRE_ROLL_TAKE_HALF_GATE_V1.md: G25 obrigatório antes de RNG.
- novydres/runtime/NARRATOR_LED_ADJUDICATION_G27_V1.md: narrador estipula testes; não delega cálculos ao jogador.
- novydres/runtime/G28_SCENE_END_BATCH_AND_DYNAMIC_CONFLICT_V1.md: batch de um commit ao final da cena; buffer cronológico efêmero; G26 no erro.
- novydres/governance/protocols/EVENT_PROTOCOL_V5.source.txt: T01–T12, autoria, proveniência, causalidade e limites de automação.
- novydres/systems/v5/MOTOR_MECANICO_V5_V1_1.source.txt: FV, RNG, oposição, motores e caveats.
- novydres/chronicles/CHR-001/character/MECHANICAL_GUIDED_CREATION_RULES_PROVENANCE_V3.json: pools provisórios versus adquiridos; Briga(Agarrar) local e limitada.
- novydres/MANIFEST_V14.json: ponteiros operacionais correntes.
- novydres/chronicles/CHR-001/LIVE_v012.json, HISTORY_INDEX_v012.json, episodes/M2.03_v017.source.txt, character/state_v018.source.txt, knowledge/NPC_KNOWLEDGE_PROVENANCE_V2.json e OPEN_THREADS_V2.json: fato e checkpoint.

## Matriz de precedência
1. Cânone fechado / ficha-alvo aprovada congelada: INALTERÁVEL sem instrução explícita.
2. Decisões do jogador e contratos vigentes G23/G24/G25/G26/G27/G28.
3. Fontes e eventos confirmados com proveniência, decisões e ledger técnico quando auditado.
4. Projeções atuais LIVE, índice, estado do personagem, índice de NPC; distinção entre evidência e hipótese.
5. Diário histórico e memórias de conversa; não suplantam correções posteriores.

## Conflitos aparentes resolvidos por decisão já vigente, NÃO por nova exceção
- G19 antigo pede persistência pré-resposta, G26 permite backlog após erro, G28 posterior fixa a CADÊNCIA da gravação no fim da CENA. Este pacote implementa G28 sem gravação por turno; continua obrigatório readback antes de declarar persistência.
- .AGENT/.CONTEXTG carregam checkpoints M1 e Drive; MIG-DEC-002 e MANIFEST_V14 supersedem destino e checkpoints. Não reabrir M1 nem M2.03.
- Ficha TARGET não equivale à ficha COMPRADA. DEC-CR-019 somente autoriza Briga (Agarrar) temporariamente no escopo expresso. M2.03.119 teve exceção de Ofícios no teste já aceito, PENDING_RULE_AUDIT, não novo precedente global.
- RNG em chat com faces transcritas não vira ferramenta verificada; manter UNVERIFIED_CHAT_PRESENTATION.
- Recompensa da provocação longa até 30 libera CREDITO DE COMPRA, não XP total; avaliação/lançamento somente na transição autorizada. FV no início real de nova sessão; não no fechamento.
- Uma mudança de chat NÃO é uma mudança de sessão ou recuperação de FV.

## Travas no ponto de implantação
- M2.03 CLOSED: checkpoint M2.03.126; M2 ACTIVE_AWAITING_NEXT_PROVOCATION; M2.04 NOT_STARTED.
- PJ mortal, fim dos anos 1970, em casa; sem Abraço nem crônica 2010.
- XP total519, gasto170, restante349, crédito disponível20; FV máxima provisória6, dano superficial5, agravado0, disponível1.
- Mikahel Touchstone e Convicção literal preservados; Sara e Mary preservadas.
- NPC Nadezhda aprende apenas primeiro nome em M2.03.124; antes disso uso do nome foi erro de narrador. Homem ferido e paramédicos não possuem conhecimento comprovado do nome.
- Ficha aprovada imutável: novydres/chronicles/CHR-001/character/TARGET_SHEET_V2_APPROVED.json, SHA f8b62bf74f4f5f937a0f0d3b3462263d4a9d186c.

## Escopo permitido desta implementação
Criar contratos/schemas/provas de regressão/manifesto V15 somente por novos caminhos. Nenhuma decisão DEC anterior reescrita. Sem comprar XP, conceder crédito, restaurar FV, abrir M2.04, fazer rolagem real, alterar NPC ou fechar pendência histórica. Na primeira transição efetiva exigir solicitação e verificação de estado atual. Contratos procedimentais não são um serviço autônomo nem substituem a validação executável de dados quando disponível.
