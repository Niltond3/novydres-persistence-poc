# Reconciliação topológica — contrato operacional

Não substitui os 32 critérios de `docs/infra-acceptance.md`, não aprova INF-01/INF-02 e não altera a U02. Única entrada executável: `scripts/pipeline.py`.

## Autoridades separadas

1. O agente examina visualmente a U02 original (SHA-256 verificado) e a geometria candidata; registra uma observação por **par de corredores e ponto físico**. Uma interseção aparente não certifica ligação, viaduto, ponte ou nível. Incerteza permanece `UNRESOLVED`.
2. O registro segue `schemas/topology-classifications.schema.json`: hash da U02, hash determinístico do grafo fonte, corredores em ordem alfabética, ponto exato, identidade, `RESOLVED`/`UNRESOLVED`, relação, níveis preexistentes, observação geométrica e evidência visual localizada (`inspected_by: AGENT`, hash da imagem, recorte `bbox`, descrição). Elemento novo, estrutura protegida, junção metroviária/ferroviária requer decisão editorial identificada e aprovada. Não conexão no mesmo nível exige prova de barreira.
3. O código compara cada registro a interseções reais, não inventa níveis, segmenta as polilinhas com nós conectados apenas quando autorizados e conserva vértices, extremidades, atributos e conectores. Os IDs das partes e sua origem são determinísticos; a fonte e os digests ficam no candidato. Aplicação repetida com a mesma classificação é idempotente; alteração posterior do grafo é rejeitada.
4. A saída é **candidata**. `RECONCILED_NOT_ACCEPTED` não concede aceite; `BLOCKED` enumera cruzamentos pendentes individualmente e impede aprovação em `infra_checks.validate`. Etapas seguintes dependem de revisão visual, bytes reais, contrato Markdown, ledger e aceite independentes.

## Operação

```text
python scripts/pipeline.py run --district kingswell \
  --topology-source /work/INF-01-candidate.json \
  --topology-classifications /work/crossings-reviewed.json \
  --topology-out /work/topology-candidate \
  --reference /work/U02-original.png
```

Arquivos produzidos: `topology-candidate.json` e `topology-diagnostic.json`. São JSON locais de trabalho, não imagens ou recibos de Drive. O agente persiste os candidatos em GitHub e só sobe artefatos visuais reais ao Google Drive, fazendo readback efetivo.

Antes da reconciliação de etapa cumulativa, proteger a geometria já aceita, informar `protected_edge_ids` e validar a etapa anterior com `infra_checks.validate(prior=...)`. Conectores regionais continuam sujeitos a fiscalização bilateral independente. Não converter os diagnósticos R1–R5 em tentativas aprovadas.

Limite epistemológico: o validador prova consistência geométrica, hashes e presença da evidência visual; não demonstra que um modelo interpretou corretamente os pixels. A avaliação visual semântica continua obrigatória para cada classificação.
