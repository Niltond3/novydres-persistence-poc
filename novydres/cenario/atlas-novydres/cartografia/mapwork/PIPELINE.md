# Pipeline operacional única

**Entrada:** `scripts/pipeline.py run`; `scripts/web_bridge.py` faz transporte,
não validações paralelas. O código é o controlador determinístico e o agente
ChatGPT Web executa, de fato, pesquisa, geração e revisão visual.

## Fluxo

Recuperar HEAD e contratos → validar autoridade e capacidades → pesquisar
análogos externos → reconciliar decisões e inventário → planejar geometria
espacial e conexões vizinhas → INF-01 a INF-07 → URB-08 → gerar imagens por
unidade → auditar cada imagem e seus vizinhos → compor tiles → revisão macro
ANTES/DEPOIS → solicitar aprovação final ao proprietário.

A aprovação documental histórica de um desenho não libera nenhuma etapa.
Uma aprovação verificável por critérios independentes libera **somente** a sucessora. Falha em qualquer dependência
(incluindo bytes, máscara, U02, conexões, plano ou hash) invalida as aprovações
descendentes. Não gerar quadras, lotes, edifícios, POIs ou arte antes dos gates
previstos. Nenhum comando desta pipeline publica cânone.

## Contrato de execução agêntica

1. Executar `pipeline.py` (ou `web_bridge.run_web` que chama essa mesma entrada).
2. Ler `status`, `next_action`, `stage` e os problemas concretos. `FAIL`
   corrigível é **ação a executar na mesma sessão**, não encerramento.
3. Gerar **nova** geometria e prévia real baseada nas fontes, confirmar bytes,
   inspecionar a imagem completa e recortes, registrar os quatro critérios;
   persistir a candidata mesmo que seja `FAIL` ou incompleta com `--record-attempt`.
4. Gravar imagens/máscaras/artefatos no Drive, recuperar os bytes e confrontar
   SHA; gravar ledger/checkpoint no GitHub usando compare-and-swap do SHA da
   branch e reler. Nunca simular readback nem alterar registro remoto sem lease.
5. Invocar **novamente a mesma** entrada oficial depois de cada ação;
   seguir a próxima ação. Não implementar laço Python que apenas repita testes.

As ações `GENERATE_AND_AUDIT_CANDIDATE`, `REPAIR_AND_REGENERATE`,
`REPAIR_UNVERIFIED_CANDIDATE`, `REPAIR_DIAGNOSTIC_AND_REGENERATE` e `REGENERATE_DIFFERENT_CANDIDATE` exigem
novos arquivos materiais, novo parecer visual vinculado aos bytes e execução
novamente. `REPLAN_STAGE` exige mudança documentada da estratégia. A cada
três falhas do mesmo problema sem melhoria material, mudar estratégia;
ao completar seis tentativas malsucedidas, `REASSESS_METHOD` exige
reconsiderar premissas, método e decomposição espacial. Não liberar PASS por
esgotamento; não repetir indefinidamente a mesma estratégia. Registros
incompletos reprovados permanecem rastreáveis e não são aceites.

`BLOCKED_CAPABILITY`: ferramenta essencial comprovadamente indisponível;
`ASK_OWNER_ONE_DECISION`: questão editorial genuína; `CHECKPOINT`: limite
de sessão e persistência confirmada para retomada; `READY_FOR_OWNER_REVIEW`:
composição técnica pronta, ainda sem canonização. Somente essas condições
justificam interrupção sem aceite. Reprovação, erro técnico corrigível e
incapacidade externa têm causas e estados distintos.

## Continuidade obrigatória pelo agente

Após cada retorno, o agente **executa** a operação; não resume um diagnóstico
como se fosse trabalho concluído. O agente é responsável pelo ciclo externo
entre invocações da mesma entrada; Python não gera imagens nem executa um
laço que repete validadores sem alterar os arquivos.

| Classe de retorno | Operação efetiva antes da próxima invocação |
| --- | --- |
| `GENERATE_AND_AUDIT_CANDIDATE` | Criar geometria e PNG originais, auditar e persistir |
| `REPAIR_*`, `REGENERATE_*`, `CORRECT_AND_REGENERATE_IMAGE` | Corrigir a causa, gerar **novos bytes**, reexaminar e persistir |
| `REPLAN_STAGE`, `REPLAN_AND_REGENERATE_IMAGE` | Alterar estratégia e guardar evidência; gerar outra candidata |
| `REASSESS_METHOD`, `REASSESS_METHOD_AND_REGENERATE_IMAGE` | Reexaminar método após seis falhas, declarar nova estratégia e reiniciar tentativas |
| `ASK_OWNER_ONE_DECISION` | Parar somente pela decisão editorial genuína e específica |
| `RESTORE_REQUIRED_HOST_TOOLS` | Registrar incapacidade comprovada da ferramenta, sem inventar prova |
| `ADVANCE_AFTER_ACCEPTANCE`, `NEXT_WORK_UNIT` | Avançar somente após aceite matemático **e** visual, e readback remoto |
| `CHECKPOINT` | Persistir e reler o estado exato, retomando a mesma etapa em outra sessão |

`PASS` escrito pelo gerador é apenas um **parecer declarado**. O veredito
da pipeline depende da conferência independente dos bytes, topologia,
recibos e critérios Markdown. Candidata reprovada é registro imutável, não
gatilho para bloqueio permanente. A retomada exige ler o último ledger e
checkpoint pelo GitHub, verificar SHA e ler arquivos reais do Drive; erro de
persistência exige readback/CAS antes de nova gravação. Não saltar fase nem
declarar etapa terminada apenas por salvar checkpoint.

Para `--audit-unit`, passar `--start-unit --request-id` e, após
replanejamento, também `--strategy-id --replan-evidence`; o sexto fracasso
não impõe limite de aprovação e a sétima tentativa é legítima com novo método.

## Evidências e recuperação

Cada tentativa identifica `request_id`, etapa, estratégia, geometria e PNG
integrais com SHA-256, observações visuais regionais, 4 critérios, defeitos,
correção, seu predecessor e recibos Drive de upload+readback. Rejeitar
reutilização de geometria ou PNG já apresentada como nova tentativa.
Verificar ledger, fonte, assets e relações antes de retomar. Operações repetidas
com o mesmo `request_id` e o mesmo conteúdo são idempotentes. Não reaproveitar
parecer antigo quando uma dependência material mudar. Git é o único histórico
operacional; jamais manter versões de contratos ou conversores legados.

Os critérios 32 e topologia detalhada pertencem exclusivamente a
`docs/infra-acceptance.md`; inspeção de imagens, adjacências, máscaras e
composição pertence exclusivamente a `VISUAL_REVIEW_PROTOCOL.md`.

### Estado autoritativo e retomada

O contrato executável é `docs/infra-acceptance.md`. Infraestrutura exige
aceite independente sequencial INF-01 a INF-07; URB-08 precede arte/composição.
Um registro histórico de desenho U02 não altera o estado do ledger.
`zones/<alvo>/checkpoint.json` vincula `criteria_sha256`,
`reference_sha256`, `ledger_sha256`, `official_accepted_stages` e o alvo.
Se qualquer vínculo divergir, reconciliar e reler GitHub antes de continuar.
Nunca editar o critério para fazer uma candidata reprovada passar.


## Sessão autônoma verificável pelo ChatGPT Web

Entrada única: scripts/pipeline.py run, materializada e verificada por
web_bridge.run_web. O Python não tem conectores; o ChatGPT executa ações
reais, em etapas, e reentra na mesma pipeline para validação.

Iniciar com --request, --district, --session-key, --autonomous-journal,
--host-branch, --host-head (HEAD inicial obtido por conector) e
--host-journal-path (caminho relativo sessions/...json, não canônico).
web_bridge
injeta --source-commit da árvore Git efetivamente verificada. Preservar
o HEAD inicial da sessão em retomadas, sem substituí-lo silenciosamente.

1. SYNC_PENDING_JOURNAL: journal local PENDING, operação e lease_head emitidos.
   Antes de agir, commitar journal em GitHub via CAS e fazer novos GETs
   de ref, commit, tree e blob por conector. Materializar bytes de
   download em arquivo separado. Em commit com resposta perdida, reler
   HEAD/journal antes de tentar novamente.
2. O ChatGPT Web executa pesquisa, classificação, correção topológica,
   geração nativa, inspeção visual, replanejamento e persistência com
   ferramentas conectadas. operation_id é chave estável. Em recuperação,
   localizar uploads anteriores com a mesma chave, sem duplicar operações.
3. Reentrar com --host-exchange apontando para JSON de kind
   COMPLETE_OPERATION, operation_id, pending_sync e result.
   result.artifacts[] exige path local, readback_path separado vindo de
   GET do provedor, sha256, provider, remote_id e blob_sha para GitHub.
   Para artefatos GitHub exigir repo_path e result.github_commits[]:
   cada commit informa branch, lease_head, commit_parent, head, ref_head,
   commit_sha e files (caminho → Git blob SHA). A cadeia começa no HEAD
   do journal PENDING e registra cada avanço CAS da mesma branch.
   result.arg_updates só pode alterar argumentos permitidos, nunca
   injetar aprovação editorial ou de infraestrutura. Imagem nova exige
   PNG verdadeiro em Drive e outro arquivo JSON kind=visual-review,
   associado ao image_sha256 e quatro observações verificáveis.
4. SYNC_COMPLETED_JOURNAL: fazer outro commit Git CAS com lease no HEAD
   confirmado da última gravação de artefato, ou no HEAD do journal
   PENDING quando não houve gravações adicionais na branch. Novos GETs independentes, e depois
   enviar kind ACK_COMPLETE, operation_id, completed_sync e
   recovery_readbacks[] para todos os artefatos concluídos.
5. A pipeline só então aplica argumentos e reavalia critérios. Se ainda
   houver trabalho, emite outro PENDING; caso contrário retorna parada
   legítima sem promoção do cânone. Reprovação é trabalho a corrigir,
   não motivo para declarar encerramento.

pending_sync e completed_sync têm os campos branch, repo_path,
lease_head, head, ref_head, commit_sha, commit_parent, tree_blob_sha,
blob_sha e readback_path. repo_path deve coincidir com
--host-journal-path; o journal só é sincronizado dentro de sessions/. O modelo obtém ref_head, commit_sha, commit_parent,
tree_blob_sha e bytes de chamadas independentes ao conector GitHub;
o Python verifica coerência de bytes e relações de CAS. Python não
consegue autenticar criptograficamente a origem de um resultado de
ferramenta, portanto jamais inventar GET, imagem ou parecer.

O caminho antigo de callbacks é apenas suporte a testes in-process;
não é necessário para o agente ChatGPT Web. GitHub mantém código,
contratos e checkpoints; Google Drive guarda imagens e arquivos.
Nenhum registro da sessão publica cânone nem substitui o aceite
independente de INF-01 a URB-08.

## Ensaio sintético isolado no controlador existente

O parâmetro `--synthetic-trial <arquivo.json>` ativa exclusivamente uma fixture
`NOVYDRES_MAPWORK_SYNTHETIC_TRIAL` no mesmo `scripts/pipeline.py run`.
A fixture deve ter `test_only=true`, `canonical_target=null`,
`publication_authorized=false`, `canonical_state_changed=false`, identidade
`synthetic-*`, SHA-256 dos critérios de `docs/infra-acceptance.md` e vínculo
com a branch, o journal e o `operation_id` **já existentes**.

Este escopo não utiliza zona real, U02, renderizador canônico nem os aceites
INF-01/URB-08. O próprio controlador exige topologia sintética validada,
PNG nativo com bytes enviados ao Drive e relidos, inspeção visual vinculada
à imagem (desnível, continuidade, coerência e formato) e ledger idempotente.
Reprovações seguem a política de reparo/replanejamento já implementada.
Um checkpoint `SYNTHETIC_ACCEPTANCE` **nunca** publica cânone, autoriza INF-01
ou implica que as outras operações do Agente 3 estejam concluídas.

A operação pendente `BUILD_REGION_FROM_APPROVED_CANON` do ensaio anterior só
pode receber um recibo de **mudança de escopo sintético**, sem alegar que Sulfok
foi construído. A próxima ação deve ser calculada novamente após
`SYNC_COMPLETED_JOURNAL` e `ACK_COMPLETE`, preservando o mesmo `operation_id`
e todos os hashes históricos. `--synthetic-trial` não cria outro journal.

## Entrega obrigatória da referência à geração nativa

Toda operação `GENERATE_WITH_CHATGPT_NATIVE_IMAGE`, `GENERATE_AND_AUDIT_CANDIDATE`
no ensaio, ou ação de correção/regeneração, é uma **edição vinculada a
referência visual**, nunca um pedido de relatório. O agente Web deve seguir o
`native_edit_request` produzido pela entrada única `scripts/pipeline.py run`.
Não reescreva esse pedido usando um resumo do diálogo: seu `prompt` determina
imagem cartográfica como saída e proíbe relatório, infográfico e selo de PASS.

1. Recuperar de Google Drive os bytes da **imagem de referência** e da **máscara**
   por GETs próprios; verificar SHA-256, formato PNG e dimensões iguais.
   Quando a referência ou máscara ainda for local, enviá-la primeiro ao Drive
   e então recuperá-la por GET distinto do arquivo original.
2. Tornar ambas as imagens visualmente acessíveis ao gerador nativo, usando-as
   como entradas da **mesma chamada de edição**. O agente deve executar a edição
   com o `prompt` exato em `native_edit_request`, não simplesmente citar os
   arquivos, seus caminhos ou seus hashes num prompt textual.
3. Registrar um `NOVYDRES_MAPWORK_NATIVE_EDIT_HANDOFF` com `request` íntegro,
   `request_sha256`, `operation_id` (nas operações Web), `inputs` nas funções
   `reference-image` e `edit-mask`, `dispatch` da chamada nativa com
   `generation_id`, `attached_inputs`, SHA do pedido/prompt e do resultado,
   e `output` com ID/bytes locais + GET independente do Drive.
4. Persistir também um parecer visual com hashes da **referência**, **máscara** e
   **imagem gerada**. Na troca com o host, apresentar cinco artefatos: `image`,
   `reference-image`, `edit-mask`, `native-edit-handoff` e `visual-review`.
   A composição canônica exige, por unidade, a receita original e o handoff
   recuperáveis com hashes reais no lote de imagens.

`--native-handoff` indica o JSON materializado da operação. Sem esse arquivo,
sem imagem/máscara baixadas independentemente, ou com imagens/IDs/hashes fora
do pedido, a pipeline **não pode reconhecer PASS**. É legítimo reutilizar a
mesma referência em outra tentativa; a nova candidata não pode reutilizar os
bytes de uma tentativa anterior como se fossem nova geração.

O módulo Python confirma os **bytes, o despacho declarado e seus vínculos**;
não tem acesso interno ao payload secreto da ferramenta de imagem. A veracidade
de `dispatch.attached_inputs` e `generation_id` é responsabilidade do host
ChatGPT Web conectado, que deve efetivamente chamar a ferramenta com os dois
anexos. Um JSON sem chamada real **não é demonstração operacional**.

No ensaio não canônico, a fixture deve indicar `native_reference_sha256`,
`native_mask_sha256` e `native_edit_goal` além da geometria e do journal já
vinculados. A ausência desses campos produz
`MATERIALIZE_SYNTHETIC_REFERENCE_AND_MASK`, não uma geração textual de imagem.
