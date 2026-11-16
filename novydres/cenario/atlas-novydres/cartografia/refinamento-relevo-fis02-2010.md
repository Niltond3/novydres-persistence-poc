---
document_id: MW-011-FIS02-RELIEF-REFINEMENT-2010
subject_id: world-atlas-novydres
reference_year: 2010
workflow_status: OPEN_PENDING_OWNER_REVIEW
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED_PROPOSAL_NOT_CONFIRMED
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
source_parent_commit: 2a3932a015c8458226410ebfcd67d399b0a33e10
current_relief_proposal_blob_sha: da9afd790822aa66d30b22a8d87f573277f4c690
source_relief_proposal_blob_sha: c28dd404b5d1fb2c6495ca104c7f457c29825644
coast_approved_working_blob_sha: d72cf3eb2b3fac9473017a6bbfdc46ea1efb8577
work_unit: MW-011
fis02_valley_owner_decision: APROVADO
fis02_valley_decision_on: 2026-11-16
fis02_valley_approval_scope: NONCANONICAL_REFINED_THERMAL_VALLEY_WORKING_GEOMETRY_ONLY
fis02_uplands_owner_decision: APROVADO
fis02_uplands_decision_on: 2026-11-16
fis02_uplands_approval_scope: THREE_NONCANONICAL_REFINED_UPLAND_POLYGONS_AND_THREE_QUALITATIVE_RIDGE_AXES
fis02_tundra_lowlands_owner_decision: PENDING
fis02_final_review: PENDING
---

# MW-011 — Revisão candidata FIS-02: macrorelevo (2010)

## Escopo, fatos protegidos e estado

O proprietário aprovou em MW-007 somente a **organização relativa** de FIS-02. A costa continental refinada de MW-010 está aprovada como **base de trabalho não canônica**; os contornos/número das ilhas continuam hipóteses. As cinco classes canônicas GEO-003.3, a orientação hidrotermal GEO-003.4 e os Ermos GEO-003.5/GEO-004.3 são preservados. Este documento registra aprovações **parciais**, sem aceite final do conjunto nem canonização do relevo.

Bootstrap: HEAD `master` 27595ca32652efdef3d406eb91e4482299056bd9; leitura conjunta AGENTS/CONTEXT/catálogo, assunto `world-atlas-novydres`, ADR-002, PRD-ATLAS-001, guide e fontes físicas. Origem de MW-010: branch `mapwork/mw-010-refinamento-costeiro-fis01`, commit `2a3932a015c8458226410ebfcd67d399b0a33e10`.

## Decisão expressa recebida — FIS-02.1 (16/11/2026)

**Estado: APROVADO**, somente quanto ao contorno refinado do vale termal `relief-thermal-valley-001`. Diante da pergunta explícita “Você aprova o contorno refinado do vale termal, rejeita ou aprova com ressalvas?”, o proprietário respondeu **“Aprovo”**.

**Alcance:** o polígono refinado já publicado na proposta MW-011 é aceito como base cartográfica de trabalho **não canônica**; sua relação com Cidade Velha/Iknik, trechos termicamente influenciados do Rio Vasyl e a piscina termal candidata é mantida. Não fixa os limites de Kingswell/Iknik, nascentes, temperaturas, altitudes ou engenharia. **Na ocasião, não abrangia** as três serras/cristas nem as duas áreas de tundra ou a baixada úmida; a decisão posterior FIS-02.2 está registrada abaixo. Não altera o status global da geometria, `owner_approval_for_this_geometry: null`.

O polígono do vale já corresponde à versão aprovada para trabalho, portanto **não há necessidade de modificar seus vértices nesta subdecisão**. A aprovação parcial não encerra MW-011 e não autoriza handoff.

## Decisão expressa recebida — FIS-02.2 (16/11/2026)

**Estado: APROVADO** para os três polígonos de serras e os respectivos eixos qualitativos de crista: `relief-northern-uplands-001`, `relief-eastern-uplands-001` e `relief-southern-uplands-001`. Perguntado se aprovava “os três sistemas de serras e seus eixos de crista refinados, ou deseja ajustes?”, o proprietário respondeu **“Aprovo”**.

**Alcance:** aceitação exata das geometrias refinadas MW-011 já publicadas, **somente como base de trabalho não canônica**. Não determina elevações, altimetria, divisor de águas medido, túnel, estrada, ferrovias, corredores de urbanização nem limites políticos. As três cristas são linhas qualitativas internas aos maciços, não levantamentos geodésicos.

**Pendências após FIS-02.2:** decisão sobre duas manchas de tundra e a baixada úmida meridional (FIS-02.3); depois disso, aceite final expresso sobre a versão integral validada. O conjunto de propostas permanece `PROPOSED_PENDING_OWNER_REVIEW` e `NOT_APPROVED`, com `owner_approval_for_this_geometry: null` até o gate final. Nenhum vértice precisa ser alterado nesta decisão parcial. Nenhum handoff é autorizado.

## Refinamento implementado (variante não canônica)

Mantidos **sete polígonos esparsos** com IDs estáveis: um vale termal interior, três faixas de elevação (setentrional, oriental e meridional), duas áreas de tundra/permafrost e uma baixada úmida meridional. Seus limites passaram de contornos macroesquemáticos a contornos com reentrâncias moderadas, sem detalhismo cadastral; as três linhas de crista qualitativas foram ajustadas e mantidas **dentro dos próprios maciços**. Nenhuma nova feição foi nomeada ou georreferenciada.

| Área (ID) | Nova amostra sintética km² | Vértices |
| --- | ---: | ---: |
| `relief-thermal-valley-001` | 272.790 | 17 |
| `relief-northern-uplands-001` | 360.370 | 16 |
| `relief-eastern-uplands-001` | 446.580 | 16 |
| `relief-southern-uplands-001` | 352.815 | 14 |
| `relief-southwestern-tundra-001` | 365.200 | 14 |
| `relief-northeastern-tundra-001` | 221.785 | 13 |
| `relief-southern-wet-lowland-001` | 128.545 | 10 |

Área sintética acumulada de amostras = **2148.085 km²**; **não representa área municipal, cobertura total de terra, área oficial de tundra ou confirmação geográfica**. Referência local continua `NOVYDRES-LOCAL-2010`, com folha de 120×100 km apenas para desenho, e não EPSG/WGS84. Permanecem sem altitudes, datum vertical, MDE, declividades, novos topônimos, limites municipais ou rotas.

**Fonte candidata corrente:** `macrorelevo-2010.proposal.json` (blob da9afd790822aa66d30b22a8d87f573277f4c690). **Comparação histórica exclusivamente visual:** `visualizador-fisico-2010.html`, alternância entre MW-003 e MW-011 e sobreposição âmbar tracejada; o original existe como bytes anteriores no Git, não como segunda proposta corrente.

## Dependências e testes preliminares da variante

- Costa continental de MW-010 e boca derivada da baía: **sem alteração de um único vértice**; ilhas apenas como geometrias dependentes não aprovadas.
- `macrohidrografia-2010.proposal.json` e `macroermos-2010.proposal.json`: **nenhum rio, bacia, lago, Ermo ou curso foi redesenhado**, somente hashes de dependência do novo relevo atualizados; FIS-03/04 permanecem candidatos.
- Reanálise geométrica determinística JS/V8 antes de publicação: **185/185 verificações positivas**, zero erros detectados, incluindo: polígonos simples; quadro; terra versus mar e ilhas; não sobreposição dos sete maciços/baixadas; eixos dentro dos maciços e sem cruzar cursos d'água candidatos; dez Ermos com âncoras de relevo existentes e compatíveis; trecho local quente e piscina termal dentro do vale; consistência do limiar da baía; inventário de 41 feições e fidelidade da inserção HTML.
- Este teste foi executado sobre a geometria candidata transformada no conector. **Não equivale a execução dos validadores Node em GitHub Actions, certificação geológica, geodésica, hidrológica ou navegador headless.** Após a gravação, conferir SHA/parent/tree/blobs e revalidar os dados remotos. Resultado técnico: **PASS_WITH_LIMITATIONS (prévia)**, condicionado ao readback. Havendo falha real, prevalece FAIL.

## Inventário das decisões substantivas ainda necessárias

1. **FIS-02.1 — Vale termal: APROVADO em 16/11/2026**, na extensão exata da seção de decisão expressa acima.
2. **FIS-02.2 — Serras e cristas: APROVADO em 16/11/2026**, com o alcance limitado à geometria de trabalho descrito acima.
3. **FIS-02.3 — Tundra e baixada:** aprovar, rejeitar ou aprovar com ressalvas as duas manchas esparsas de tundra e a baixada úmida meridional, sem afirmar cobertura territorial exaustiva ou inundação permanente.
4. **Aceite final expresso:** após eventuais correções e publicação de geometria e visualizador efetivos, aprovação da versão consolidada. Aprovações parciais não fecham FIS-02.

**A:** decisões 3–4 e revalidação final na geometria consolidada. **B:** consequência apenas espacial sobre rio/afluentes, piscina termal, bacias e fragmentos de Ermo; sem deslocá-los em FIS-02. **C:** raions, bairros, portos, transportes, histórias, clãs, runtime e engenharia detalhada.

## Gate e continuidade

**MW-011 permanece OPEN_PENDING_OWNER_REVIEW.** Nada foi canonizado, `master` não foi alterada e **nenhum handoff para MW-012 está autorizado** antes de todas as decisões, implementação efetiva, validação e aceite final do proprietário com readback remoto, conforme `cartografia/guide.md`. A geometria antiga permanece acessível somente por histórico Git; o HTML é derivado e não se torna fonte da verdade.
