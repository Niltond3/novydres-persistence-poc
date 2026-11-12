# NOVYDRES — MANDATO DRAMATURGO D01 V1
Status: PLAYER_SAFE / EXECUÇÃO PROPOSTA EM BRANCH DE DESIGN / NÃO É ORDEM DE NARRAÇÃO.
Objetivo: estabelecer contratos de arquitetura reutilizáveis para qualquer crônica NOVYDRES (criação guiada, crônica completa, side quest), sem ainda inventar culpados, lore secreto ou desfechos de Bartholomeu.

## Preflight obrigatório
GitHub repo Niltond3/novydres-persistence-poc, master: redescobrir HEAD e maior CYCLE verificado, latest LIVE/HISTORY_INDEX, character, atlas, 44 threads e dossiês; ler .AGENT.md, .CONTEXTG.md e governança/contratos.
Documentos de entrada:
- novydres/runtime/narrative-architecture/program/ARCHITECTURE_PLAN_V1.md
- novydres/runtime/narrative-architecture/program/PROGRAM_RUNBOOK_V1.md
- novydres/runtime/narrative-architecture/program/D01_MANDATE_V1.md (este)
- novydres/runtime/narrative-architecture/NARRATIVE_ATLAS_CONTRACT_V1.md
- novydres/runtime/provocation-prep/DRAMATURGO_CONTRACT_V3.md
- novydres/runtime/provocation-prep/LONGITUDINAL_PROGRESS_GATE_V1.md
- novydres/runtime/orchestration/ORCHESTRATION_CONTRACT_V1.md e DRAMATURGO_ROLE_V1/V2
- novydres/chronicles/CHR-001/preparations/global/CH00..CH07
- novydres/chronicles/CHR-001/narrative-atlas/ATLAS_SNAPSHOT_V001.json e COVERAGE_REPORT_V002.json
- novydres/chronicles/CHR-001/knowledge/OPEN_THREADS_V23.json (ou sucessor autenticado).
Os PDFs oficiais são fontes externas no Drive, links preservados no ARCHITECTURE_PLAN; não precisam ser copiados ao GitHub.

## Escopo D01
1. Desenhar ontologia CRONICLE / MARCO / STORY-PROVOCATION / PLOT / SCENE / BEAT / THREAD / NPC / SOURCE / CLUE / CLOCK / OUTCOME / PLAYER_KNOWLEDGE e relacionamentos; diferenciar hierarquia de grafo de tramas transversais.
2. Definir fluxos de criação, revisão, encerramento, suspensão, conexão entre tramas, início de arco emergente durante cena e prevenção de estagnação.
3. Propor esquemas para bible/plot/story/scene/beat/ledger/handoff: campos required, enums, ids, provenance, state machine e classification.
4. Definir gates separados DRAMATURGO_READY, SCENE_READY, AUTHORIAL_TRUTH_LOCKED, PENDING_PLAYER_APPROVAL, READBACK_PASS e NARRATOR_PERMISSION, sem violar ciclo narrativo.
5. Definir política de segredo e separação GM vs PLAYER_SAFE; o dono do repo privado pode ler arquivos, portanto secret GM exige canal que ofereça proteção real se quiser isolamento técnico, não só label.
6. Definir retcons: GAP/INTERPRETATION/RETCON_SOFT/RETCON_HARD/CANON_CONFLICT, assinaturas de aprovação e caminhos para atualizar sem sobrescrever original.
7. Definir qualidade literária: horror gótico-punk, NPC autonomia, estruturação de cenas sem scripting de decisões PC; avaliação literária e técnica distintas.
8. Definir template de entregas de D02 e a lógica de handoff incremental até D12/Narrador; preservar compatibilidade com G28, COW, D1/D2/H e eventos passados.

## Proibições
- NÃO narrar C06 ou qualquer cena; NÃO abrir 2010.
- NÃO dar XP/FV, mudar estado do personagem, NPC knowledge vigente, LIVE, ciclo, manifesto ou qualquer episódio fechado.
- NÃO definir ou expor verdades ocultas de Volnaya, caixa, Abraço, sire ou outras tramas; D01 é engenharia de contratos.
- NÃO editar contrato APROVADO/CONGELADO ou CANÔNICO/FECHADO, não presumir autoridade para aprovar retcon.
- NÃO publicar material GM_HIDDEN em relatório ao jogador nem no prompt/handoff público.
- NÃO alterar master para tornar proposta norma ativa.

## Entregas esperadas
No branch de design (criar por exemplo design/chr001-narrative-program a partir de master validado, ou usar ramo já existente com readback): contratos propostos e versão de ontologia + auditoria de compatibilidade; exemplos apenas fictícios, sem spoilers de CHR-001; AUDIT_D01_V001.json, HANDOFF_D01_V001.json PLAYER_SAFE, NEXT_PROMPT_D02_V001.md completo, com links/SHAs reais depois de commit.
Antes de escrever verificar se já existe fase D01 para evitar duplicação; se existir, auditar, comparar e produzir versão nova em vez de sobrescrever.

## Critérios de aceitação
Campos essenciais suficientes para autoria e conclusão; distinção clara de cronologia/árvore/grafo; mistério não improvisado por Narrador; recusa, fracasso e autonomia NPC representáveis; sigilo sem ilusões de ACL; ZERO alteração no cânone; protocolo de retcon com consentimento; handoff D02 independente de memória de chat. Se FAIL, publicar remediação e pedir decisão, não fingir D02 pronto.

## Saída obrigatória ao usuário, sem spoiler
Resumo da arquitetura, documentos no GitHub por links, HEAD verificado e resultados de gates, conflitos sem conteúdo secreto; um PROMPT D02 pronto para colar em CHAT LIMPO (usar WritingBlock se disponível). O prompt D02 referencia todos os artefatos D01 versionados e AUDIT/hand-off e exige o mesmo padrão até D12. Se gate bloqueado, fornecer prompt de REMEDIAÇÃO D01, não pular.
