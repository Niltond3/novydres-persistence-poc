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
