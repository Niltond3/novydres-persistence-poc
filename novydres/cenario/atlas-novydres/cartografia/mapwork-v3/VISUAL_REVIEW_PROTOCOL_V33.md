# Protocolo V3.3 — revisão visual pelo agente, sem API de geração

**Entrada única:** `python scripts/pipeline.py run`. `v33_visual.py` é validador interno, não pipeline paralela.
A geração de imagens é feita pelo agente usando a ferramenta nativa disponível no chat, **sem chave de API, sem requisição ao endpoint e sem handshake artificial**.
O script não pode aferir sozinho se uma rua, ponte ou prédio desenhado faz sentido. Ele valida a existência dos arquivos, dimensões, hashes, integridade de máscaras e presença/escopo dos pareceres do modelo. O parecer é um juízo visual do agente, **não um teorema ou certificação matemática**.

## Sequência obrigatória

1. Executar bootstrap, pesquisa, decisões e inventário. A verificação antecipada de capacidades exige somente GitHub, pesquisa e entrega; não exige uma imagem que ainda não existe.
2. Resolver a malha espacial REAL: limites, vias, metrô, ferrovias, água, quarteirões, edifícios, POIs, vizinhos e máscaras. Nunca utilizar os 14 retângulos antigos como lotes definitivos.
3. Criar receitas e máscaras por unidade; gerar cada imagem pela ferramenta nativa do agente e materializá-la em bytes acessíveis ao compositor. Guardar `local_path`, `sha256`, `mask_sha256`, `generator_evidence`. O teste de PNG, dimensão e SHA ocorre aqui, não no preflight.
4. **Inspeção micro (LLM):** o agente deve **abrir e visualizar**, não apenas confiar em um arquivo JSON. Conferir PNG, máscara, referência U02, plano, imagens de todos os vizinhos que compartilham uma borda, ruas/trilhos/água/edifícios atravessando bordas. Para cada unidade, registrar um arquivo `*_UNIT_VISUAL_REVIEW_1` com uma linha por item e uma por vizinho. Também conferir leitura **micro→macro** e **macro→micro**. A revisão exige os SHA da imagem, máscara, referência, plano e de cada vizinho.
5. **Reparar:** nota de reprovação ou pares ainda não materializados impedem `VERIFIED`. Gerar ou corrigir somente a unidade e refazer seu parecer; alterar o vizinho invalida o SHA do parecer anterior. Limite do ledger de três tentativas por unidade. Os pares podem ser gerados antes da revisão definitiva das bordas.
6. O manifesto de composição `--image-receipts` reúne as imagens geradas e seus relatórios `visual_review` validados. Um refinamento pode fornecer `context_images` materializadas de vizinhos inalterados. Faltou um par ou seu SHA mudou: bloquear.
7. Rodar `--execute` para criar tiles reais e o comparador **sem ainda dizer que a candidata está pronta**. Resultado: `GLOBAL_VISUAL_REVIEW / AGENT_INSPECT_COMPOSED_ATLAS`, com SHA de tiles e overviews.
8. **Inspeção macro (LLM):** abrir o comparador, os overviews ANTES/DEPOIS e tiles em resolução de detalhe; inspecionar coerência regional, continuidade de infraestrutura, legibilidade/proteções, micro→macro e macro→micro. Salvar relatório `*_GLOBAL_VISUAL_REVIEW_1` com os hashes exatos de `tiles.json`, `overview-before.png`, `overview-after.png`, referência original e lote de recibos de imagem. Executar novamente com `--macro-review <arquivo>`. Apenas então receber `CANDIDATE_READY_FOR_OWNER_REVIEW`.
9. Enviar comparação para aprovação humana. **Sem aprovação humana explícita, nada de publicação ou canonização.** Nenhum relatório pode conter PASS se o agente não viu a imagem.

## Estrutura mínima de pareceres

A versão de unidade tem `schema, by=AGENT, model, status=PASS, work_unit_id, image_sha256, mask_sha256, reference_sha256, spatial_sha256, summary`, mais:
- `checks`: chaves exatas `mask_and_footprint`, `urban_structure`, `connections_and_access`, `micro_to_macro`, `macro_to_micro` com `{status:"PASS",note:"comentário visual específico"}`.
- `neighbors`: um registro `{work_unit_id,side,image_sha256,status:"PASS",note:"continuidade observada"}` para **cada borda compartilhada**. Lados N/S/E/W definidos pelo plano. Para unidades sem vizinho: lista vazia.

A versão global tem `schema, by=AGENT, model, status=PASS, summary, tiles_sha256, before_sha256, after_sha256, reference_sha256, image_receipts_sha256, reviewed_units`, mais `checks` com as chaves `regional_identity`, `transport_and_water_continuity`, `seam_and_mask_integrity`, `micro_to_macro`, `macro_to_micro`.

Cada nota é curta (uma frase), mas específica. O verificador exige `status=PASS` em todos os aspectos, os vizinhos reais e hashes atuais. Um simples `{"by":"AGENT","status":"PASS","evidence":"parece bom"}` é insuficiente.

**Limite epistêmico:** os scripts não conseguem atestar que um agente realmente inspecionou os pixels; confirmam apenas consistência documentada e hash-bound. A responsabilidade pela análise visual permanece com o modelo, e o proprietário tem aprovação final.

## Estado de Kingswell

A base espacial e as máscaras integrais ainda não estão prontas. Esta correção modifica o contrato de auditoria, não inventa a cidade nem simula um asset gerado. A V3.3 permanece candidata na branch até testes ponta a ponta reais.
