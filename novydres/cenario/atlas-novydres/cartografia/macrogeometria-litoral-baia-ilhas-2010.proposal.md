---
document_id: MW-002-MACROGEOMETRIA-COSTEIRA-NOTAS
subject_id: world-atlas-novydres
reference_year: 2010
workflow_status: PROPOSED_PENDING_OWNER_REVIEW
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
working_frame_commit: b92721da0bc85f1d497668423e2a8f64d81ba9f4
---

# MW-002 — Proposta de macrogeometria da costa, baía e ilhas (2010)

## Fonte da geometria e alcance

A única geometria candidata desta unidade está em [`macrogeometria-litoral-baia-ilhas-2010.proposal.json`](macrogeometria-litoral-baia-ilhas-2010.proposal.json). Este documento registra método e limitações, não um segundo contorno. O quadro de trabalho foi aprovado **somente para modelagem** no MW-001, commit `b92721da0bc85f1d497668423e2a8f64d81ba9f4`; não houve aprovação de costa, baía, ilhas ou perímetro urbano.

As fontes canônicas continuam `../localizacao-geral-2010.json`, `../implantacao-litoral-baia-2010.json`, `../macrorelevo-hidrografia-ermos-2010.json` e `../ermos-estrutura-territorial-2010.json`. GEO-002.4 está fechado no assunto Atlas: setor ocidental de Seward nas proximidades de Port Clarence, sem identidade geométrica com a baía real nem substituição de comunidades existentes.

## Hipótese morfológica única

- **Continente:** costa aberta aproximadamente no lado oeste da folha, linha contínua de sul a norte, com grande reentrância interna; polígonos de terra fora do quadro não são modelados.
- **Baía:** grande enseada natural abrigada por uma saliência setentrional; entrada para águas externas, definida por corda entre vértices 5 e 19 da linha costeira (índices base zero). É um limiar cartográfico de água, **não** ponte, porto, canal dragado ou batimetria.
- **Ilhas:** três polígonos pequenos *candidatos*, dois dentro da enseada e um na costa externa. O número três, suas áreas e posições **não** são cânone.
- **Água/terra:** polígonos de água e continente são **derivados** de uma única linha costeira, das bordas da folha e dos anéis das ilhas. Não copiar ou manter em paralelo um segundo desenho do mesmo litoral.

Coordenadas `NOVYDRES-LOCAL-2010` são metros de desenho com +x leste e +y norte; não são longitude/latitude nem GeoJSON WGS84. A orientação absoluta e a âncora geodésica continuam abertas. O recorte 120 × 100 km não define limite municipal.

## Validação proporcional

O arquivo [`validar-macrogeometria-litoral.mjs`](validar-macrogeometria-litoral.mjs) usa somente Node, lê o JSON e verifica: quadro MW-001 intacto; coordenadas inteiras e internas; linha de costa contínua e sem auto-interseção; topologia fechada de água/terra/baía; localização das ilhas nas águas apropriadas; ausência de sobreposição ou toque com a margem; massa insular subordinada e estados de proposta.

Execução reproduzível na raiz do repositório:

```sh
node novydres/cenario/atlas-novydres/cartografia/validar-macrogeometria-litoral.mjs
```

**Métricas sintéticas computadas, não áreas municipais oficiais:** área do quadro 12.000 km²; terra continental dentro da folha 8.188,25 km²; baía pelo fecho da boca 1.851,25 km²; soma das três ilhas 65,44 km²; boca aproximada 18,445 km. A superfície continental recortada contém território exterior ao município futuro, **logo não deve ser comparada como se fosse área municipal** com a hipótese aprovada de 4.000–7.000 km² de terras sob jurisdição.

A rotina geométrica permite atestar consistência interna; não testa marés, profundidade, sazonalidade de gelo, geologia, marcos reais ou habitabilidade. Qualquer aprovação da morfologia exige decisão substantiva do proprietário.

## Escopo preservado e decisão pendente

Não existem neste pacote fronteiras municipais, raions, bairros, portos, rotas, trilhos, malhas, ponto de foz do Rio Vasyl, termas, montanhas, extensão dos Ermos, órgãos Cainitas ou topônimos novos. Rio Vasyl terminar na baía permanece **cânone sem traçado espacial**; sua foz não é inferida desta geometria.

**Decisão para o proprietário:** aprovar, solicitar modificações ou rejeitar a hipótese *costeira* (orientação relativa, forma da enseada, abertura e ilhas). Até decisão expressa, o JSON tem status `PROPOSED_PENDING_OWNER_REVIEW`; este commit não altera o cânone nem fecha GEO-002 integralmente.

A próxima unidade deverá recuperar o snapshot atual e as fontes proprietárias; esta proposta não autoriza inferir posições administrativas ou transportes.
