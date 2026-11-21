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

Uma aprovação libera **somente** a sucessora. Falha em qualquer dependência
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
