---
document_id: MW-014-URBAN-NUCLEI-REJECTION-A
subject_id: world-atlas-novydres
work_unit: MW-014
status: OPEN_REDESIGN_REQUIRED
candidate_a_status: REJECTED_BY_OWNER
canonical_status: NOT_APPROVED
source_master_sha: cea4284fcf9cfa6fb531b7e693181420dcbddb56
source_mw013_commit: cee95e61bcdb525e2cf8b88da842ce5ea950200f
rejected_candidate_commit: 30d373ef07635a4cdd88bc10979913666feefc7d
---
# MW-014 — Rejeição integral da proposta A e redesenho obrigatório

## Decisão expressa do proprietário (16/11/2026)
O proprietário apresentou captura da visualização recebida no chat e rejeitou **integralmente** a composição enviada, relatando regressão severa na distribuição dos elementos, sobreposição, desordem visual e impossibilidade de compreensão. A candidata A **não possui aceite visual nem espacial**. A rejeição desta entrega não invalida as bases MW-010 a MW-013 anteriormente aprovadas como hipóteses cartográficas não canônicas.

## Diagnóstico
A mensagem de apresentação incluiu um esquema SVG improvisado, desenhado separadamente do comparador integral de GitHub, com rótulos de baixa legibilidade sobrepostos a feições. O esquema substituiu, na experiência do usuário, a comparação integral ANTES/DEPOIS obrigatória no `guide.md`. Barras espessas e círculos usados para Ermos degradaram a representação orgânica aprovada em MW-013. A hierarquia de cor/forma/tipografia falhou na tela móvel. Não houve prova de legibilidade/visualização real no navegador ou captura de aprovação do comparador integral. Os testes por amostragem de geometria não equivalem a validação de qualidade visual.

## Consequências operacionais
- **Rejeitado o pacote A como um todo:** nenhuma das nove macroposições ou contornos, nem a faixa contínua Kingswell–Sulfok, está aprovada.
- **Nenhuma decisão administrativa/canônica nova:** nomes dos nove raions preservados; todas as fronteiras oficiais continuam indefinidas.
- **Retirada da árvore corrente:** `macroposicoes-nucleos-urbanos-2010.proposal.json`, `comparador-integral-nucleos-mw014-2010.html` e `validar-macroposicoes-mw014.mjs`. Estes arquivos permanecem recuperáveis exclusivamente pelo commit histórico 30d373ef07635a4cdd88bc10979913666feefc7d; não são propostas correntes nem podem ser usados para buscar aprovação.
- **Fontes físicas intactas:** costa, ilhas, relevo, hidrografia, malha de Ermos e visualizador integral MW-013 mantêm seus estados de trabalho não canônico.
- **Próxima execução ainda é MW-014:** produzir nova geometria estruturada somente com cartografia completa, ANTES/DEPOIS com enquadramento/escala comuns, todos os rios e afluentes, ilhas e Ermos íntegros, bom contraste, rótulos legíveis e inspeção em tamanho de tela móvel. Não usar desenho esquemático paralelo como substituto da prova geográfica. Revalidar compatibilidade entre ocupação e Ermos antes de pedir qualquer aprovação.
- **Um ponto de decisão por vez:** após uma representação utilizável, decidir primeiro organização geral; posteriormente contornos, adjacências e aceite consolidado. A reprovação desta proposta não autoriza inventar novas decisões nem fechar MW-014.

**MW-014 permanece ABERTO. Sem handoff de próxima unidade e sem canonização.**
