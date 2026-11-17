---
document_id: MW-013-FIS04-ERMO-REFINEMENT-2010
subject_id: world-atlas-novydres
reference_year: 2010
work_unit: MW-013
workflow_status: REJECTED_REDESIGN_REQUIRED
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED
source_master_sha: cea4284fcf9cfa6fb531b7e693181420dcbddb56
source_branch_checkpoint: 7a67e197205afa87ecb20545bce847d33fc9c402
rejected_geometry_blob_sha: ea3d170930cf7e5a626bb8a800ca90004f2467a4
---
# MW-013 — Revisão de FIS-04 após rejeição da representação

## Decisão expressa do proprietário
O proprietário observou que **“essa representação não está boa”**, porque confundia os Ermos com maciços rochosos, tundra, brejos e outras unidades de relevo. A geometria MW-013 de dez pequenas manchas naturais foi **rejeitada como representação territorial de FIS-04**. Nenhuma geometria FIS-04 foi aprovada ou canonizada.

A revisão prévia passou em 11.795 asserções sintéticas, porém **essas verificações não testaram o significado territorial exigido**. O resultado não valida a cartografia dos Ermos. Os dez contornos rejeitados permanecem recuperáveis somente no histórico Git. O campo estruturado atual `wilderness_model.corridor_segments` está vazio até que uma candidata apropriada seja produzida.

## Definição correta a orientar a geometria
Os Corredores do Ermo representam **áreas de território que a expansão civilizacional não dominou de forma permanente**, independentemente da topografia dominante. São a natureza indomada, de múltiplos perigos e limites de habitabilidade, interposta entre e ao redor dos núcleos históricos de ocupação. Podem incluir montanhas, planícies, tundra, várzeas, floresta, litoral ou combinação desses ambientes. As quatro categorias canônicas GEO-003.5 são **contextos físicos**, não o critério exclusivo de delimitação.

A formação urbana policêntrica e o envio estratégico de emissários por Gilgamesh constam da fonte canônica `novydres/cenario/historia-global/formacao-policentrica-2010.json`. A expansão dessas ocupações foi condicionada pelos perigos do território; não presumir uma expansão radial de cidade contínua. O proprietário mencionou feras indomáveis, hordas, possíveis caerns Garou e riscos a Cainitas muito poderosos **como exemplos de explicações possíveis**, não como novos fatos cartográficos, domínios/caerns localizados ou aprovação de metatrama.

## Regra para a próxima variante
1. Desenhar **grandes extensões intersticiais e envolventes de natureza não submetida à ocupação**, com fronteiras irregulares e heterogêneas, sem usar o contorno de uma serra como perímetro obrigatório de Ermo.
2. Manter separadas as camadas de **território do Ermo**, **fisiografia** e **causas de perigo**. Estas últimas podem ser múltiplas ou desconhecidas.
3. Não inventar nem ratificar posições dos nove raions, dos núcleos de povoamento, das rotas de passagem, de caerns ou de criaturas; sem suas pegadas, a separação física de núcleos permanece **não demonstrada**.
4. Preservar rigorosamente costa MW-010, relevo MW-011 e hidrografia MW-012 como bases de trabalho não canônicas. A nova geometria não poderá invadir mar ou corpos lacustres como terra.
5. Travessias naturais ou artificiais podem atravessar Ermo, mas não implicam conurbação. GEO-012/013 continuam fora desta unidade.

## Estado da implementação
`macroermos-2010.proposal.json`: sem polígonos atuais, com interpretação territorial corrigida e aprovação `REJECTED_REDESIGN_REQUIRED`.
`visualizador-fisico-2010.html`: removidos os dez polígonos rejeitados, com alerta de que FIS-04 está em redesenho; as camadas MW-010 a MW-012 continuam inalteradas.
`validar-macroermos.mjs`: adaptado para verificar a ausência de geometria vigente e a preservação de estados e dependências; não confundir este teste de governança com validação de nova geometria.

**A:** nova proposta territorial de Ermo, comparação visual e todas as aprovações ainda pendentes. **B:** posição efetiva de núcleos urbanos só poderá ser comprovada em unidade posterior de ocupação. **C:** Garou, caerns, criaturas e metatrama não terão localização ou história fixadas em MW-013.

**MW-013 permanece ABERTO. Não emitir handoff.**
