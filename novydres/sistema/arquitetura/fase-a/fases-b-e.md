---
id: arch-phase-a-following-phases
status: CANDIDATO_PENDENTE_APROVACAO
scope: NOVYDRES_GLOBAL
classification: PLAYER_SAFE
---
# Contratos executáveis e dependências B–E

Emenda documental: DEC-23/DEC-24 substituem replay universal e trilha de dados por estado atual, texto integral e histórico Git, mantendo consequências e recursos. DEC-19/DEC-21 do ADR substituem as exigências antigas de telemetria Web indisponível e quotas fixas de testes. Aplicar a suíte por riscos em [validação e métricas](validacao-e-metricas.md); evidências históricas não mudam. DEC-22 resolve Q-05 do [plano integral](../plano-integral/index.md): depois de autorização futura do plano, A–D avançam por critérios comprovados, sem confirmação apenas pela transição. Decisões substantivas, mudanças de escopo/autoridade e cutover em E continuam exigindo decisão pertinente. Nenhum avanço está autorizado nesta etapa documental.

## Regra de programa
Uma fase só começa após gate PASS e dentro da autorização inicial do plano (DEC-22); não iniciar B por mera presença deste texto. Todos os chats fazem leitura de .AGENT.md, .CONTEXTG.md, ADR-001, índice A e autoridade operacional mais recente validada, preservam master e matéria fechada, escrevem APENAS branch de design com commit + lease + readback. Ao encerrar, persistir relatório player-safe, último commit, evidências, pendências e handoff completo, sem depender de memória ou spoilers. O documento de comunicação ADR §8 aplica-se integralmente. DEC-25 permite continuidade entre fases no mesmo chat somente com os controles automáticos e a recuperação Web comprovados em [validação e métricas](validacao-e-metricas.md#continuidade-no-chatgpt-web--condição-de-dec-25); manter checkpoint e revisão independente, sem novo handoff obrigatório apenas pela fase. DEC-26 aceita o risco residual e define a pausa da unidade afetada e a renovação excepcional do chat se a recuperação falhar.

## B — Protótipo estritamente isolado
Entrada: A PASS e implementação do plano autorizada, sem nova confirmação apenas pela fase (DEC-22); validar HEADs atuais; reconciliar design que ficou atrás de master e todo novo ciclo/manifesto, sob snapshots exatos; registrar conflitos antes de tocar candidatos. Cópias candidatas precisam de pin e estar no escopo autorizado do protótipo; não exigir aprovação por cópia já prevista no plano.
Implementação: escolher 1 NPC, 1 trama, 1 história, 1 estado verdadeiros com registros representativos e sem expor spoilers; criar COPIAS candidatas no layout final numa branch de protótipo ou subtree isolada de design; não mover/alterar fontes operacionais. Cada exemplo deve conter owner, index, refs e provenance, conhecimento e correções. Sem eventos sintéticos tratados como fatos; fixtures artificiais rotuladas.
Testar também os casos de divergência, conclusão sem evidência e recuperação no mesmo chat de DEC-25, na rota Web real; não declarar cumprida a condição de continuidade sem essa prova. Testar: recuperação pareada, negativos e jornadas conforme cobertura de riscos e amostragem definida em A06, sem quota fixa de consultas/rodadas; rastrear as ferramentas efetivamente utilizadas, hashes, custo de leitura, navegação, consistência do estado e retomada. Certificar equivalência sem afirmar evento técnico novo se a fonte antiga não o suporta.
Gate B PASS: quatro casos têm mapping 100% de seus campos validados ou UNKNOWN preservado, sem upgrade de episteme, sem vazamento, sem mudança de master, baseline validada, readback Git e conflitos tratados por bloqueio/decisão; caso contrário B REMEDIATION.
Saída: relatório, mapas per-case e evidência revisáveis. B PASS permite seguir para C no escopo do plano futuramente autorizado (DEC-22); gerar handoff apenas quando necessário à continuidade.

## C — Ferramentas e segurança
Entrada: B PASS, master revisitado. Implementar schemas especializados, gerador catalogo determinístico, lint de IDs/relacionamentos/owner, detectores de mudanças em registros, validador de estado, sigilo, anti-legado, scripts do fluxo de uso e CI. Não ativar entradas candidatas no master.
Testar: runs reais com resultado consultável, fixtures adversariais, snapshot fixo/sha lease, concorrência stale HEAD, corrupção de blob, referência quebrada, conhecimento indevido, bytes externos e partial sync. Contratos dos executores efetivamente adotados devem especificar entradas/saídas verificáveis; detectar limitação de API sem inventar capacidade.
Gate C PASS: executáveis e schemas têm testes reais aprovados na rota usada; checks de 100% de casos críticos; nenhuma lacuna bloqueante; readback. Sem CI comprovada = FAIL/NOT_EXECUTED.

## D — Migração integral de candidatos, ainda sem cutover
Entrada: C PASS e master atual pinado; congelar baseline de migração por commit imutável/tag auditável. Inventariar TODAS as entradas do snapshot, incluindo .github/workflows, originais, provas, mídia, fixtures, arquivos versionados, imports e dependências externas relevantes.
Transformação: atribuir cada origem a owner/destino ou classificação de fonte histórica arquivável por Git, com SHA e rationale; preservar literalmente o passado e decisões; registrar cada exceção/conflito/UNKNOWN sem inventar fatos; conciliar estado/ciclo com suas fontes. Conforme DEC-23/DEC-24, não exigir conversão do histórico para ledger, replay universal ou auditoria por dado. Preservar fontes antigas sem inventar certificado RNG. Calcular diff origem->destino, cobertura de todas as afirmações e refs. Produzir candidato de topologia final e testes.
Gate D PASS: inventário fechado sem input sem destino justificado, todos os vínculos e registros reconciliados, 0 perda/invenção, todos campos autoritativos equivalentes, apenas conflitos legitimamente não bloqueantes ou explicitamente aprovados; se violar cânone fechado, STOP. Ainda não promover master.

## E — Cutover atômico sem legado, absoluto
Entrada: D PASS + revisão independente + decisão expressa de política sucessora (G24/editorial/ADR), aprovação explícita de cutover, HEAD master revalidado; quaisquer novos commits exigem rebase sem retcon e nova prova.
Passos: construir árvore final sem nenhum caminho operacional antigo, reescrever workflows/imports/prompts/contratos ativos, garantir únicas entradas AGENTS.md/CONTEXT.md/catalogo.json, executar validador anti-legado em toda HEAD e suíte reprodutível, conferir mídia, controles e refs. Criar tag de segurança pré-cutover e plano de incidente aprovado; publicar um único commit final com parent esperado e expected_old_SHA; verificar ref/commit/árvore/blobs, rodar smoke test em snapshot promovido, checar CI. Não manter aliases/wrappers/symlinks/fallback/transitional routes depois da promoção.
Gate E PASS SOMENTE se ZERO legado e 100% equivalência/gates; qualquer caminho residual = FAIL e NÃO chamar a mudança de corte concluído. Falha antes da promoção não toca master. Falha pós-promoção: tratar como incidente de recuperação mediante instrução expressa, nunca fallback silencioso.

## Modelo de handoff de B (somente no plano autorizado, com A PASS)
Missão: NOVYDRES MIGRAÇÃO FASE B — Protótipo, exclusivamente. Repositório Niltond3/novydres-persistence-poc; branch de design design/subject-oriented-migration. Primeiro consultar refs atuais; não presumir o SHA de A como o master atual. Ler ADR novydres/sistema/arquitetura/adr/001-subject-oriented.md; ler novydres/sistema/arquitetura/fase-a/index.md e todos os documentos vinculados; confirmar autorização de implementação do plano e A PASS no registro auditável, sem exigir nova aceitação apenas pela fase; resolver divergência design/master sem modificar master nem restaurar estado antigo. Ler .AGENT.md, .CONTEXTG.md e discovery do ciclo/manifesto vigentes. Protótipo restrito a COPIAS candidatas de 1 NPC, 1 trama, 1 história e 1 estado. Completar quadro de equivalência e fixture comparável por função e risco. Não alterar eventos, decisões, ficha, cânone, runtime ou ciclos. Publicar somente novas evidências e candidatos na branch de design com commit protegido e readback. Encerrar em PASS/FAIL/BLOCKED/PENDING_APPROVAL; recomendar CONTINUAR NESTE CHAT ou ABRIR CHAT LIMPO; fornecer prompt de mesma fase caso falhe e de C apenas após PASS e dentro da autorização inicial do plano (DEC-22). PLAYER_SAFE; sem spoilers.

## A07 — Revisão consolidada da emenda e decisão de desenho (execução 2026-11-12)

**Veredito revisável:** `A_DESIGN_EXECUTION_PASS` para A01–A07, **somente desenho em branch candidata**. O mandato direto do jogador em 2026-11-12 autoriza A–D e commits, enquanto E/master/ativação/runtime e cenas continuam expressamente sem autorização. DEC-22 permite iniciar B conforme dependências provadas, sem nova confirmação só pela fase. A prova de controles DEC-25 **ainda está pendente** e esta decisão não dispensa handoff/renovação excepcional (DEC-26). Aprovação histórica `fase-a/aprovacao.json` e `fase-a/decisoes-e-gate.json` permanecem **literalmente imutáveis como registros de sua data**, não reclassificados retroativamente.

### Comparação do início até A06

- **Baseline de execução design:** `5b55c12f4d041187ee597eb786049e7dbe5a22fc`; **HEAD de revisão A07:** `c8b282a4984851bd166b89af7d6b264c04dea87e` (tree `6d84346ff6038abe51d15bdeb72c86bd7bbced75`). Comparação GitHub: **6 commits à frente, 0 atrás**, em 9 arquivos alterados, **0 fora** do prefixo `novydres/sistema/arquitetura/`. Nenhuma origem de protótipo B, crônica, fonte histórica, cânone, regra ativa ou workflow foi alterada nessa série.
- **master** na revisão: `c9fcfc0c558cd17d58ec8c8272da3ed70182ff37` (tree `4894bebafcc872dcd7c772ea4d34e5d54079b810`), idêntico ao snapshot da entrada. No ramo candidato, gate histórico B `gate-e-readback.json`, blob `433b2d4b321a49aeeedf48c5b3a48f4914753423`, permanece `B_REMEDIATION_REQUIRED`; C não liberada.
- Commits e entregas: A01 `783f8616d0f2e42f61f41a0be2a02b3f6258fa03` (autoridade/árvores/9 famílias); A02 `582a627604b4350ec04a3573e272f28885a9e05d` (owners, prosa/estrutura, 2 schemas candidatos); A03 `0298e4837bf9a304857837c5639b2c74fc5a729b` (G19/G23/G24/G26/G28 e transação DEC-18); A05 `39da97c260c7a25d432de990b7fdd7342a7b8156` (interfaces, evidência Web GitHub); A04 `b22f03e7190e4bed39cdf6b1dce7b123a40aff01` (DEC-01–15, IMP-01–15, ficha/rumo, lacunas V5); A06 `c8b282a4984851bd166b89af7d6b264c04dea87e` (gabarito isolado, riscos, executor mínimo e B/C).
- Cada publicação acima teve `expected_sha` e readback de HEAD e blob. **Não** houve execução de benchmark/CI, validador de schema de instância, roteador final ou teste de casos adversariais; isso é prova documental, não da implementação.

### Matriz DEC e mudança de obrigação

| Decisões / origem | Efeito no desenho após A01–A06 | Evidência e futuro gate |
|---|---|---|
| DEC-01–15/17 | Condução solo prioritária, mesmo chat para papéis, NPCs com autonomia, preparo proporcional, elipse opcional, 1970/2010 e justiça social, tom e correções | `simplificacao-narrativa/desenho.md`, A04; testar em B/C com revisão contextual |
| DEC-16/23/24 | Dados só para durável, texto incidental íntegro, estado por owner, sem ledger/replay/face obrigatórios | `fase-a/modelo-de-dados.md`, `topologia-e-ownership.md` e 2 schemas; C01/C04 |
| DEC-18 | Escrita/resposta atômica antes da entrega, pausa se falhar; G26/G28 só substituídos após E | `fase-a/git-e-roteadores.md`, A03; B04/C03 |
| DEC-19/21 | Métrica Web parcial `NOT_OBSERVABLE` para tokens/bytes HTTP; suíte por risco, falhas históricas preservadas | `fase-a/validacao-e-metricas.md`, A06; B02–B05 |
| DEC-20 | Retirar guardrails repetitivos sem perder autorização, história, agente, conhecimento e efeito | A02–A06 e IMP map; C05/C07 |
| DEC-22 | Autorização direta A–D recebida em 2026-11-12, transições por gates técnicos | Este A07 e backlog; B começa sem nova aprovação ritual |
| DEC-25/26 | Web/GitHub com controles demonstrados e recuperação; pausa/renovação excepcional quando falhar | A05/A06 **definiram mas não provaram** detector/retomada; B03/B04 e C04/C07 obrigatórios |

### Questões e limitações não resolvidas por A07

1. **ARCH-A-001 / RA-02:** conflito entre G24/DEC-CR-014 e nomes estáveis Git: requer sucessor de política aprovado para **E**, não bloqueia B isolada.
2. **ARCH-A-004 / RA-01:** seis world `candidate` e relatório posterior de fechamento, variantes de NPC (CONFLICT-003/003B): não promover nem fundir sem veredito e prova da fonte; itens afetados de D permanecem `PENDING_EVIDENCE`.
3. **RA-03:** design em C36/M51 versus master em C45/M63; B01 deve mapear snapshot histórico e estado atual por separado. Nunca igualar fontes C41 a cursor C45.
4. **RA-04:** 14 originais de mídia no Drive, 5 pendentes, sem SHA-256 completo; D/E devem comprovar destino/integridade ou bloquear a entrada afetada.
5. **RA-05:** história sem certificado técnico de ledger/RNG; DEC-23/24 **dispensam a reconstrução**, não permitem inventar ocorrência; preservar texto literal e estado.
6. **Ficha/2010:** destino de criação guiada é decisão aceita, mas custo final de V5, poderes, idiomas, Touchstones e elegibilidade dependem de fontes/validação; nenhum XP novo nem certificação automática.
7. **B crítico:** fonte e gabarito no mesmo fixture antigo, Codex 51/90, B-Q29/30 repetidamente falhos, Web com evidência anterior insuficiente, negativos/jornadas não executados remotamente, CI sem run e rejeição CAS remota não provada. **B continua em remediação**. Nenhuma exceção DEC-19/21 dispensa essas provas.
8. **Continuidade:** controles DEC-25 ainda não operam comprovadamente em ambos os canais. Nesta sessão o checklist manual e os readbacks de commits documentais não equivalem a detecção automática de interpretação incorreta. Em mudança de fase, manter checkpoint/handoff; se a recuperação não restaurar autoridade, DEC-26 exige novo chat.

**Decisão de desenho A07:** A01–A06 possuem saída e fonte, nenhum trade-off novo exige repetição de Q-01–Q-08. Prosseguir **somente** a B01–B05 isolada, sem mudar `master`, sem ativar runtime e sem interpretar o PASS de desenho como equivalência factual. Quando B05 não tiver PASS, C01–C08 permanecem bloqueadas. Escolhas substantivas genuinamente novas seguem a autoridade aplicável, não um pedido automático de confirmação entre fases.

**Readback de A07:** o commit que acrescentar este adendo será identificável no histórico Git da branch; não se insere SHA autorreferencial. As três entradas antigas permanecem inalteradas até E. A próxima sessão deve recuperar o HEAD e conferir o commit, este adendo, A06 e gate histórico B antes de qualquer escrita.
