# NOVYDRES — gateway Git-native (ADR-001)

**E02 aprovado pelo proprietário em 13/11/2026 e publicado em master.** A eficácia operacional exige E03_PASS verificável em `sistema/arquitetura/fase-e/execucao-e03.json`. Mesmo após E03_PASS, **não iniciar a crônica, cenas, rolagens ou efeitos de XP/FV sem uma instrução própria do jogador**.

## Uma entrada e um snapshot
1. Consultar o HEAD remoto atual de `master`. Ler `novydres/AGENTS.md`, `novydres/CONTEXT.md` e `novydres/catalogo.json` **desse mesmo SHA**; são as únicas três entradas correntes.
2. Resolver `subject_id` exato no catálogo, validar owner, `index.md`, caminhos, hashes e dependências do mesmo commit. `NOT_FOUND` ou bloqueio explícito em falta de autoridade, fonte ou acesso. Não buscar por aproximação.
3. Branch candidata, checkpoint pré-cutover e SHAs antigos servem à proveniência/auditoria ou recuperação de incidente, **nunca** como rota operacional, alias, wrapper, redirect ou fallback. Sem bootstraps por ciclos/manifestos antigos.

## Sigilo e estados
Acesso técnico do agente não é permissão de divulgação. Separar AGENT/PLAYER/PC/NPC, `CONFIRMED`, `NPC_CLAIM`, `GM_PREPARED`, `CONDITIONAL`, `UNKNOWN`. Restringir divulgação conforme papel e fonte; catálogo bruto e metadados restritos não são respostas públicas. Rótulos não constituem ACL externa.

O cursor C45 pertence ao assunto `chr001-state-checkpoint` em `cronicas/CHR-001/estado/recuperacao-c45.json`. C41 em `atual.json` é fixture histórica, não cursor. Nenhuma preparação vira evento jogado. Não modificar material CANÔNICO/FECHADO ou APROVADO/CONGELADO sem ordem específica; preservar `CONFLICT-001/002/003B` sem escolha silenciosa.

## Contratos e persistência
A sucessão autorizada está em `sistema/arquitetura/fase-e/sucessao-operacional.md`; o contrato editorial aprovado está em `sistema/narrativa/contrato.md`. Em jogo **futuramente autorizado**, cada resposta usa uma única transação Git-native atômica que inclui prosa integral e efeitos materiais com `tx_id`, CAS/`expected_sha`, `force=false`, confirmação remota de ref/parent/tree/blobs **antes da entrega**. Em confirmação perdida, verificar transação existente antes de tentar de novo; nunca duplicar, rerrolar ou confirmar escrita pendente.

As 119 sucessões D05 ainda não certificadas individualmente são risco residual aceito, não equivalência provada. Falha material suspende a função afetada e exige o plano de incidente. Nenhum fallback legado.
