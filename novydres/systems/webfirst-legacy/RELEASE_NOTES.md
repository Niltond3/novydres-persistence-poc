# RELEASE V0.2 — CHATGPT WEB / GOOGLE DRIVE

- Sistema de arquivo canônico do cenário: **não alterado**.
- Governança narrativa `.AGENT.md` V1: **não alterada**.
- Substitui a decisão anterior de manter banco SQLite local como fonte persistente.
- Fonte única da crônica: Google Doc JSON `CHRONICLE_STORE_V0_2`, leitura e gravação com CAS de revisão.
- Motor Python sem acesso à rede, executável em ambiente transitório mediante ferramentas.
- Eventos encadeados por hash, `before/after`, `PLAYER_DECLARATION` literal e referência de origem.
- Rolagens devem ser precedidas de commit da especificação; dados são gerados aleatoriamente via `secrets.SystemRandom` e auditados via cadeia de hashes.
- Testes: 24/24 locais e CAS real de Google Docs em sandbox.
- Problemas conhecidos: nenhum gateway automático de execução de código a partir do Google Drive; ChatGPT deve buscar e executar explicitamente o motor; validação semântica/identidade e proteção contra edição administrativa não garantidas.
- Próximo marco: importação/validação da ficha com canon atual e fluxo de ponta a ponta de rolagem para personagem real (sem atos fictícios).
