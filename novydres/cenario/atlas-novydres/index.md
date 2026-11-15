---
subject_id: world-atlas-novydres
kind: world-location
owner_scope: novydres/cenario
status: CANDIDATE
visibility: SYSTEM_AUDIT
---
# Atlas de Novydres

**Única fonte editorial candidata para conteúdos geográficos ainda não aprovados:** [atlas-proposta.md](atlas-proposta.md). Cada raion e lugar possui assunto próprio em `cenario/geografia/` ou `cenario/lugares/`, com uma única projeção desta fonte. A existência de um item na proposta não aprova automaticamente seu conteúdo.

**GEO-004.2 — raions oficiais:** [raions-oficiais-2010.json](raions-oficiais-2010.json) é a fonte canônica única para a existência e os nomes dos nove raions em 2010. Os assuntos de raion apenas referenciam a lista. Não estão aprovadas as fronteiras, dimensões, macroposições ou jurisdições Cainitas.

**Fato canônico de população municipal residente em 2010:** [populacao-2010.json](populacao-2010.json). A proposta geográfica não constitui fonte autônoma para o censo.

**Localização e implantação territorial aprovadas GEO-002.1/GEO-002.2/GEO-002.3:** a fonte canônica única é [localizacao-geral-2010.json](localizacao-geral-2010.json). Configuração continental majoritária, acesso marítimo por grande baía natural, rios e lagoas naturais e fontes termais são diretrizes aprovadas; não se trata de arquipélago. A origem geológica, a concentração na Cidade Velha e a desigualdade de aquecimento estão definidas **exclusivamente** em [geotermia-aquecimento-2010.json](geotermia-aquecimento-2010.json); redes, vazão, geometrias, área e coordenadas permanecem abertas.

**Pertencimento territorial GEO-004.1:** o [assunto proprietário Chelsea](../geografia/district-chelsea/cidade-velha-2010.json) estabelece a Cidade Velha como seu núcleo histórico. A fonte geotérmica referencia esse fato sem duplicá-lo; a geometria ainda está aberta.

As cópias históricas anteriores foram retiradas da árvore atual conforme diretriz do proprietário. O histórico de commits permite auditoria; não é rota de consulta editorial vigente. Metadados `CANDIDATE` são exigência técnica do manifesto ADR-001 e não representam uma segunda fonte de conteúdo.

**GEO-004.3 — estrutura natural dos Ermos:** a fonte única é [ermos-estrutura-territorial-2010.json](ermos-estrutura-territorial-2010.json). Os Corredores do Ermo não são um décimo raion; são barreiras naturais que separam normalmente os núcleos urbanos e condicionam travessias. O modelo de crescimento e a escolha estratégica dos emissários fundadores por Gilgamesh (GEO-005.1/GEO-005.2) pertencem exclusivamente ao [assunto de história](../historia-global/formacao-policentrica-2010.json). Geometrias, posições de senhorios e travessias continuam pendentes.

**GEO-005.3 — história integrada à geografia:** a [fonte histórica única](../historia-global/formacao-policentrica-2010.json) determina que os nove raions podem derivar de outro número de senhorios fundadores, mas mudanças de domínio Cainita exigem causas históricas fortes e aprovação. Geografias, sucessões e cronologias concretas seguem abertas; não houve ratificação de transferência Ventrue entre Chelsea e Bukovie.

**GEO-005.4.1 — primeira camada de Old Town:** o povoamento mortal inicial e a influência Cainita ritual estão definidos exclusivamente no [assunto proprietário de Chelsea](../geografia/district-chelsea/origens-mortais-e-culto-fundador.json); a [continuidade política geral](../historia-global/formacao-policentrica-2010.json) apenas o referencia. Ainda não estão definidos nome ancestral, população em 1423/1500 nem o culto específico.

**GEO-005.5 — geografia ocultista:** [fonte única no assunto História](../historia-global/marcos-ocultos-e-alasca-2010.json). Existem linhas de ley e pelo menos um Earthbound no subsolo; separar nós esotéricos de geotermia natural e dutos físicos. O desenho dos nós permanece não atribuído e não modifica GEO-003/GEO-014.
