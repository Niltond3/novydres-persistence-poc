---
document_id: MW-012-HYDROGRAPHY-REVIEW
subject_id: world-atlas-novydres
reference_year: 2010
work_unit: MW-012
status: CANDIDATE_PUBLISHED_AWAITING_OWNER_REVIEW
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

## Decisões a solicitar ao proprietário, uma por vez
1. **FIS-03.1 — Rio Vasyl e afluentes**: PENDENTE. Aprovação, rejeição ou ressalvas do percurso refinado, duas confluências e trecho local aquecido (mantidos nós de foz).
2. **FIS-03.2 — Microbacias e drenagens independentes**: PENDENTE. Envelopes não exaustivos, dois ajustes de compatibilidade costeira, curso meridional e curso do litoral exposto.
3. **FIS-03.3 — Corpos d'água e conexões**: PENDENTE. Lago interior doce, lagoa salobra com troca mareal, piscina e escoadouro termal.
4. **Revisão final consolidada**: PENDENTE. Aceite expresso da mesma versão integral após deliberações e validações.

**A:** deliberações de FIS-03 e aceite integral ainda necessários. **B:** topo e bacias sintéticas não provam declives mensurados ou engenharia hidrotermal. **C:** FIS-04, raions, bairros, transportes, infraestrutura, história e runtime não fazem parte de MW-012.

**Gate:** não fechar a unidade, não produzir handoff e não canonizar antes de todas as aprovações, correções, validação e verificação remota de fechamento.
