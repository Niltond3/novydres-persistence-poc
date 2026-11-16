---
document_id: MW-012-HYDROGRAPHY-REVIEW
subject_id: world-atlas-novydres
reference_year: 2010
work_unit: MW-012
status: THREE_PARTIAL_DECISIONS_APPROVED_AWAITING_FINAL_OWNER_REVIEW
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
source_mw011_commit: 03d4d2dbeec3d298f200de4169cbdba35dea1051
coast_working_blob_sha: d72cf3eb2b3fac9473017a6bbfdc46ea1efb8577
relief_working_blob_sha: cccc4eaac09b192a299108389bef3494f1f15bda
source_hydro_blob_sha: 57df659de492f64288c50a0001525e7ae93fa530
refined_hydro_blob_sha: 0b9747b1b82064a8ad3eaa935a4ef500271d1bf9
---

# MW-012 — Macrohidrografia refinada FIS-03 (2010)

## Alcance
Refinamento exclusivamente cartográfico, não canônico, preservando as feições GEO-003.4: Rio Vasyl / Reka Vasilya, dois afluentes, duas drenagens independentes e conexões locais de lago e piscina, cinco envelopes não exaustivos de microbacia, três corpos d'água e um trecho aquecido localizado. O quadro local NOVYDRES-LOCAL-2010 não é WGS84. Costa MW-010 e relevo MW-011 estão aprovados como bases de trabalho, não como cânone.

## Variante e correções de compatibilidade
- Rio Vasyl: inseridas inflexões intermediárias sem deslocar sua cabeceira candidata, duas confluências, pontos de referência do aporte termal ou foz no vértice 19 da costa continental.
- Afluentes e rios independentes: densificação de segmentos com pequenos desvios, mantendo nós terminais e identidades; índices das duas confluências do Vasyl reindexados para a mesma posição geométrica.
- Microbacias: envelopes de contorno mais orgânico, mas ainda não mensurados. Ajustados especificamente dois trechos marginais que, no candidato anterior, avançavam sobre a baía: borda da bacia Vasyl e borda sul da baía. Nenhuma costa ou ilhota foi deslocada.
- Lago de água doce, lagoa salobra e piscina termal: contornos internos refinados, entradas/saídas preservadas e referências às respectivas bacias mantidas. O trecho de aporte termal ocupa agora índices 9–15 da linha refinada, correspondendo aos índices originais 3–5.
- Nenhuma nova vazão, largura, altitude, nascente oficial, divisor comprovado ou topônimo foi estabelecido.
- Corredores do Ermo mantidos rigorosamente em sua geometria pré-MW-012; apenas SHA de dependência hidrográfica atualizado. FIS-04 não foi revisado.

## Verificação técnica preliminar
Transformação determinística sobre os blobs remotos de MW-011, parâmetro de modulação 0.75, com **6.909 testes geométricos positivos** na sessão: integridade de polígonos, amostragem de bordas em terra, separação dos envelopes, segmentos fluviais dentro de suas bacias, confluências, ligações com os corpos d'água, ausência de cruzamentos não declarados, preservação dos eixos de crista, piscina/trecho termal no vale, lago na tundra. Primeiro ensaio de amplitude 1.0 rejeitado por cruzamento próximo à confluência setentrional; não foi publicado. A execução real de Node/CI e o teste de navegador ainda não foram demonstrados.

## Comparação visual
Visualizador 2D: `visualizador-fisico-2010.html`, seletor **Hidrografia · FIS-03** com “Refinada MW-012”, “Anterior MW-004” e “Sobreposição” (âmbar para a versão histórica). O histórico é apenas auxílio visual; a geometria candidata corrente e autoridade da imagem está no JSON, não no arquivo HTML. Costa MW-010 e relevo MW-011 permanecem inalterados. Ilhas continuam hipótese revisável.

## Decisão expressa registrada — FIS-03.1 (16/11/2026)

**APROVADO**, limitado ao traçado refinado do Rio Vasyl e dois afluentes, suas duas confluências, desembocadura e trecho de aporte termal localizado, **somente como base de trabalho não canônica**. O proprietário respondeu **“Aprovo”** à pergunta direta de aprovação FIS-03.1, após visualização comparativa no chat. Naquele ponto da revisão, FIS-03.2, FIS-03.3 e o aceite integral ainda estavam pendentes; consultar o inventário atualizado abaixo. A geometria corrente não necessita alteração em função dessa decisão; por isso o blob JSON e suas dependências permanecem os mesmos. `approval.owner_approval_for_this_geometry=null` e o fluxo global pendente continuam válidos.

## Decisão expressa registrada — FIS-03.2 (16/11/2026)

**APROVADO**, restrito aos cinco envelopes candidatos de microbacias e duas drenagens independentes, incluindo a eliminação de invasões dos envelopes sobre a baía, **como base de trabalho não canônica**. O proprietário respondeu **“Aprovo”** à deliberação específica acompanhada da comparação 2D MW-012. Não houve solicitação de alterações de vértices. Naquele ponto da revisão, FIS-03.3 e a aprovação integral ainda estavam pendentes; consultar o inventário atualizado abaixo; os blobs estruturados e o estado global `approval.canonical_status=NOT_APPROVED` não são alterados por esta decisão parcial.

## Decisão expressa registrada — FIS-03.3 (16/11/2026)

**APROVADO** o refinamento dos três corpos d'água (lago interior, lagoa salobra e piscina termal) e das respectivas conexões (entrada e saída do lago, canal de troca mareal, escoadouro da piscina ao Vasyl), exclusivamente como **base de trabalho não canônica**. O proprietário respondeu **“Aprovo”** após comparação 2D (variante MW-012, anterior MW-004, sobreposição). Não foram demandadas modificações geométricas. A localização da piscina no vale termal e o alcance limitado do aporte térmico são preservados. O aceite integral de FIS-03 ainda depende de confirmação final específica; `approval.owner_approval_for_refined_hydro` e `approval.owner_approval_for_this_geometry` permanecem `null` até as respectivas decisões autorizadas.

## Revisão consolidada submetida ao proprietário (sem aceite integral nesta etapa)

Inventário **FIS-03.1, FIS-03.2 e FIS-03.3**: as três aprovações parciais estão registradas. Geometria proposta efetiva permanece no blob `0b9747b1b82064a8ad3eaa935a4ef500271d1bf9`, sem diferenças após as três decisões. Inventário consolidado: 1 Rio Vasyl, 2 tributários, 2 drenagens independentes, 4 conexões hídricas de lagos/lagoa/piscina (9 cursos no JSON), 5 envelopes de microbacias, 3 corpos d'água, 1 trecho termal localizado. Referências de costa e relevo mantidas inalteradas e não canônicas.

A verificação geométrica de 6.909 checagens diz respeito a **essa mesma geometria**, anterior às deliberações, sem alterações posteriores. Verificações Node/CI e execução de navegador ainda não demonstradas; devem ser corretamente identificadas como limitações, sem insinuar PASS de CI. Não existe medição de declividade, vazões, divisores reais ou temperatura. **Próximo gate único: revisão/aceite integral explícito pelo proprietário da variante consolidada FIS-03; somente depois atualizar estados estruturados, validar versão de fechamento, fazer readback remoto e decidir fechamento.** Nenhum handoff está autorizado agora.

## Decisões a solicitar ao proprietário, uma por vez
1. **FIS-03.1 — Rio Vasyl e afluentes**: APROVADO EXPRESSAMENTE em 16/11/2026, como geometria cartográfica de trabalho **não canônica**: curso principal refinado, dois afluentes, ambas as confluências, foz preexistente na baía e trecho de aporte termal localizado. O proprietário respondeu literalmente **“Aprovo”** à pergunta de aprovação da FIS-03.1 acompanhada do recorte comparativo 2D da variante MW-012. A aprovação é parcial, não encerra FIS-03 nem aprova os cinco envelopes, as drenagens independentes, os três corpos d'água e suas ligações como conjuntos. Não altera vértices nem autoriza canonização ou handoff.
2. **FIS-03.2 — Microbacias e drenagens independentes**: APROVADO EXPRESSAMENTE em 16/11/2026, como geometria cartográfica de trabalho **não canônica**: cinco envelopes não exaustivos, correções marginais para não invadir a baía e duas drenagens independentes, meridional com deságue na baía e setentrional com deságue na costa exposta. O proprietário respondeu literalmente **“Aprovo”** à questão FIS-03.2 após comparação 2D. Esta aprovação parcial não equivale a aprovar FIS-03.3 nem ao aceite consolidado e não canoniza divisores hidrográficos ou hidrologia quantitativa.
3. **FIS-03.3 — Corpos d'água e conexões**: APROVADO EXPRESSAMENTE em 16/11/2026, como geometria cartográfica de trabalho **não canônica**: lago interior de água doce com tributário de entrada e emissário até mar exterior, lagoa costeira salobra com canal de troca mareal até a baía (sem deslocamento de costa), piscina termal e seu escoadouro curto até o Rio Vasyl, mantendo aquecimento somente localizado. O proprietário respondeu literalmente **“Aprovo”** à pergunta de aprovação específica FIS-03.3 após comparação 2D em três painéis. A aprovação individual não substitui a revisão final consolidada.
4. **Revisão final consolidada**: PENDENTE. Aceite expresso da mesma versão integral após deliberações e validações.

**A:** revisão final consolidada FIS-03, validação da versão de fechamento e readback remoto ainda necessários. **B:** topo e bacias sintéticas não provam declives mensurados ou engenharia hidrotermal. **C:** FIS-04, raions, bairros, transportes, infraestrutura, história e runtime não fazem parte de MW-012.

**Gate:** não fechar a unidade, não produzir handoff e não canonizar antes de todas as aprovações, correções, validação e verificação remota de fechamento.
