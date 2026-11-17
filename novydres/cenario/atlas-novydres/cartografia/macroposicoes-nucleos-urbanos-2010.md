---
document_id: MW-014-URBAN-NUCLEI-CANDIDATE-B
subject_id: world-atlas-novydres
work_unit: MW-014
work_unit_status: OPEN_ANCHORS_APPROVED_NONCANONICAL_OTHER_DECISIONS_PENDING
canonical_status: NOT_APPROVED
candidate_a_status: REJECTED_BY_OWNER
candidate_b_status: OWNER_APPROVED_NONCANONICAL_WORKING_BASELINE
candidate_b_approval_date: 2026-11-17
candidate_b_decision: APROVADO_SEM_RESSALVAS
master_bootstrap_sha: 9df23f37a96169ee005600d2d70237f408dae2e5
previous_rejection_commit: 6e0f6da5f3f5fec525916578e2e8df9996e4bb6c
---
# MW-014 — Variante B: núcleos de implantação, não polígonos administrativos

## Aprovação expressa da variante B — 17/11/2026

O proprietário aprovou a **visualização integral ANTES/DEPOIS da variante B, sem ressalvas**, com seus **nove pontos candidatos de implantação**, após a prévia apresentada no aplicativo ChatGPT. A aprovação alcança a **composição espacial e os pontos de referência** da candidata B; esta é agora **base de trabalho não canônica**.

Artefatos aprovados: `macroposicoes-nucleos-urbanos-2010.proposal.json` (nove pontos, blob histórico `0ec37a6b11a59155ad50445e64345a15dac1c192`); visualização `comparador-integral-nucleos-mw014-2010.html` (blob `53fa926ec39afccb008208ba7bfe86bdeb5201e9`). Os limites administrativos, contornos construídos, redes de transporte, distribuição da população, conurbação Kingswell–Sulfok e canonização **não foram submetidos nem aprovados**.

Diretriz adicional aprovada na mesma manifestação: atualizar `cartografia/guide.md` para exigir **HTML interativo incorporado no ChatGPT sempre que suportado**, fallback HTML **para download** caso o aplicativo não exiba a incorporação, além de PNG/SVG fiel quando viável. Essa diretriz deve morar no GitHub, não na memória do chat.

## Estado e autoridade
A proposta A foi rejeitada integralmente pelo proprietário, inclusive como apresentação. Sua geometria e visualização foram retiradas do HEAD da branch em `6e0f6da5f3f5fec525916578e2e8df9996e4bb6c`. Esta candidata B não reaproveita polígonos urbanos, nem propõe faixa construída contínua como fato, e não altera a base física aprovada apenas para trabalho em MW-010–013.

## ANTES / DEPOIS completo
O arquivo `comparador-integral-nucleos-mw014-2010.html` usa uma única instância dos dados estruturados das camadas físicas em **duas vistas de mesmo recorte e escala**, com layout empilhado no celular. O ANTES = integralidade física de MW-013; o DEPOIS = exatamente as mesmas camadas, acrescentadas 9 âncoras do tipo `Point`. Não há topônimos escritos sobre o território; números 1–9 remetem a lista externa legível e interativa. Botões de zoom sincronizam os dois mapas. A lista permite foco no mesmo local nos dois painéis; botão “Território inteiro” restaura a comparação integral.

Inventário preservado integralmente: 1 costa, 3 ilhas secundárias hipotéticas, 7 feições de relevo, 3 cristas, 10 envelopes orgânicos de Ermo, 9 cursos d'água incluindo afluentes, 3 corpos d'água, 5 bacias, trecho termal e limiar da baía. Cor e desenho das camadas físicas seguem o padrão técnico MW-013, sem esquema de círculos ou pinceladas como substituto dos Ermos. Rótulos são externos, portanto não encobrem hidrografia nem topografia.

## Proposta geométrica B
Os pontos 1–9 estão em `macroposicoes-nucleos-urbanos-2010.proposal.json`, com coordenadas locais métricas, referências de `subject_id` para os nove raions e justificativas geográficas. São **pontos de referência urbanos**: não equivalem a área construída, fronteira administrativa, centroide oficial, função política nem distribuição da população municipal.

As relações diretas Kingswell–Sulfok, Bukovie–Kingswell e Bukovie–Alexandria são hipóteses geométricas: ligação reta Kingswell–Sulfok sem invasão do Ermo no teste por amostragem; outras duas ligam centros separados por Ermo. Isso **não** atribui viabilidade de obra, caminho, estrada, ferrovia ou conurbação construída.

## Validação executada
- 9 identificadores urbanos distintos, formato exclusivamente Point, com checagem de amostras de terra firme e afastamento amostral de 1,4 km das águas e Ermos (441 testes de posição/amostragem).
- Inventário e coordenadas de costa, 3 ilhas, 7 relevos, 3 cristas, 10 Ermos, 9 cursos d’água, 3 corpos d’água, 5 bacias e trecho termal derivados e conferidos com dados estruturados.
- Três relações diretas analisadas (201 amostras em pré-estudo e 301 na validação de modelo; sem interpretação como redes).
- Script JS da visualização: sintaxe PASS. Teste com DOM simulado: PASS para criação de mapas, nove fichas, nove marcadores, sincronização de zoom e grupos físicos equivalentes nas duas vistas.
- Validador Node reproduzível: `validar-macroposicoes-mw014.mjs`.

**Limitações materiais:** a visualização real em navegador móvel ainda não foi testada por captura de tela nesta execução, nem foram certificados CRS real, topologia exata de todos os polígonos ou propriedades cadastrais. A validação sintética não significa aceite visual pelo proprietário.

## Decisões pendentes para MW-014 (uma de cada vez)
1. Organização geral dos nove pontos candidatos em relação a costa, água, relevo, termas e Ermos — **APROVADA SEM RESSALVAS como base não canônica em 17/11/2026**.
2. Configuração Kingswell–Sulfok: conurbação, continuidade econômica sem contato urbano, ou outra composição — **sem decisão**.
3. Extensão realista e morfologia das ocupações após aceite de posicionamento — **sem decisão**.
4. A versão visual e os nove pontos da candidata B foram **aprovados sem ressalvas**; o fechamento consolidado da unidade ainda exige deliberações 2–3 ou adiamento expresso compatível com o escopo, seguidas de leitura remota.

**A** — pontos urbanos aprovados como base de trabalho; configuração de continuidade e abrangência da unidade ainda abertas. **B** — efeitos espaciais de calor, água e Ermos considerados, sem projetar infraestrutura. **C** — política Cainita, criaturas e crônica não desenvolvidas.

## Estado do trabalho
**MW-014 continua ABERTO** até as decisões remanescentes e o gate final. A candidata B foi aprovada para uso como base cartográfica não canônica, sem canonizar posições. Não alterar master, raions, crônica ou runtime. Não criar handoff para unidade seguinte antes da deliberação e validações integrais.
