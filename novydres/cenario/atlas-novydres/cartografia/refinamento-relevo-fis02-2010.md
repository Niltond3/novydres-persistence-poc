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
fis02_tundra_lowlands_owner_decision: APROVADO
fis02_tundra_lowlands_decision_on: 2026-11-16
fis02_tundra_lowlands_approval_scope: TWO_NONEXHAUSTIVE_TUNDRA_POLYGONS_AND_SOUTHERN_SEASONAL_WET_LOWLAND_NONCANONICAL
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

## Decisão expressa recebida — FIS-02.3 (16/11/2026)

**Estado: APROVADO** para `relief-southwestern-tundra-001`, `relief-northeastern-tundra-001` e `relief-southern-wet-lowland-001`. À pergunta explícita “Você aprova as duas áreas de tundra e a baixada úmida meridional, ou deseja algum ajuste?”, o proprietário respondeu **“Aprovo”**.

**Alcance:** contornos refinados de duas manchas esparsas de tundra/permafrost e de uma baixada úmida meridional sujeitos a encharcamento sazonal, **somente como base de trabalho não canônica**. Não estabelecem cobertura exaustiva de tundra ou áreas úmidas, regime hidrológico mensurado, permafrost contínuo em todos os pontos, alagamento permanente ou impossibilidade categórica de expansão urbana.

Não requer alteração dos vértices já publicados. Juntamente com FIS-02.1 e FIS-02.2, **encerra a deliberação por componentes**, porém **não constitui aceite final do artefato consolidado**, nem canonização e nem autorização de handoff.

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
3. **FIS-02.3 — Tundra e baixada: APROVADO em 16/11/2026**, com o alcance cartográfico esparso e não canônico descrito acima.
4. **Aceite final expresso:** após eventuais correções e publicação de geometria e visualizador efetivos, aprovação da versão consolidada. Aprovações parciais não fecham FIS-02.

**A:** aceite final expresso da versão consolidada e seu fechamento técnico posterior; a deliberação por componentes (1–3) está concluída. **B:** consequência apenas espacial sobre rio/afluentes, piscina termal, bacias e fragmentos de Ermo; sem deslocá-los em FIS-02. **C:** raions, bairros, portos, transportes, histórias, clãs, runtime e engenharia detalhada.

## Versão consolidada submetida ao aceite final

Os sete polígonos de macrorelevo e os três eixos qualitativos de crista permanecem **exatamente** os da proposta MW-011 aprovada separadamente em FIS-02.1, FIS-02.2 e FIS-02.3; não houve ressalvas nem necessidade de ajuste geométrico. Os quatro artefatos estruturados (costa de MW-010, relevo de MW-011, hidrografia e Ermos dependentes) foram recuperados do branch remoto após as deliberações.

**Verificação adicional executada sobre os arquivos remotos antes da publicação deste registro:** 141/141 verificações determinísticas positivas, nenhuma falha: integridade dos 7 polígonos no quadro e lado terrestre da costa; simplicidade, não sobreposição e afastamento da costa; 3 cristas internas e sem interseção com os cursos d'água candidatos; referência de 10 corredores do Ermo, âncoras e relações espaciais; Rio Vasyl termal e piscina termal dentro do vale; hashes cruzados; 41 feições com coordenadas correspondentes ao HTML e comparação histórica anterior recuperada do Git; e compilação sintática do JavaScript embutido. Preservada a costa aprovada `d72cf3eb2b3fac9473017a6bbfdc46ea1efb8577`. O teste preliminar MW-011 original havia registrado 185/185.

Blobs da versão final submetida à revisão: costa `d72cf3eb2b3fac9473017a6bbfdc46ea1efb8577`; relevo `da9afd790822aa66d30b22a8d87f573277f4c690`; hidrografia `e20597f4b1fa903c04e9f5c96b8fe3b7014a20d6`; Ermos `205c693f03ed06cc053313e20db732cdca3fc55b`. Geometria estruturada permanece autoridade sobre a representação SVG.

**Limitações declaradas:** sem execução Node/CI ou teste em navegador/headless; verificação de sintaxe não prova execução visual; geometria local não georreferenciada, amostral, sem MDE/altitudes, sem certificação geodésica/hidrológica. Resultado: **PASS_WITH_LIMITATIONS**, não `CLOSED_CANON`. O visualizador sofreu apenas correção de comentário técnico (índices reais do limiar da baía 6 e 33), sem modificação de desenho ou coordenadas. Aferir readback remoto após commit.

**Falta decisão substantiva:** aceitar ou rejeitar **a versão consolidada MW-011** já implementada, ou pedir ajustes. Até esse aceite, `workflow_status` continua `OPEN_PENDING_OWNER_REVIEW` e `fis02_final_review` permanece `PENDING`. Não produzir handoff.

## Gate e continuidade

**MW-011 permanece OPEN_PENDING_OWNER_REVIEW.** Nada foi canonizado, `master` não foi alterada e **nenhum handoff para MW-012 está autorizado** antes de todas as decisões, implementação efetiva, validação e aceite final do proprietário com readback remoto, conforme `cartografia/guide.md`. A geometria antiga permanece acessível somente por histórico Git; o HTML é derivado e não se torna fonte da verdade.
