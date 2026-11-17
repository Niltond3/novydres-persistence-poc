---
document_id: MW-014-URBAN-NUCLEI-CANDIDATE-A
subject_id: world-atlas-novydres
work_unit: MW-014
status: OPEN_PENDING_OWNER_APPROVAL
canonical_status: NOT_APPROVED
source_master_sha: cea4284fcf9cfa6fb531b7e693181420dcbddb56
source_mw013_commit: cee95e61bcdb525e2cf8b88da842ce5ea950200f
---
# MW-014 — Macroposições urbanas, candidata A

## Base factual e escopo
São **nove raions administrativos** com nomes canônicos, mas nenhum limite aprovado. A Cidade Velha/Iknik é núcleo interno de Kingswell. A formação urbana é policêntrica, descontínua, separada por Ermos; existem exceções de conurbação. O cinturão econômico Kingswell–Sulfok é canônico, mas não exige ligação urbana contínua.

O resultado aqui é **hipótese visual e geometria de nove centros de ocupação**, um núcleo de referência para cada raion. **Não** equivale a atribuição de todo o raion, área urbana municipal, redes viárias, pontos institucionais nem distribuição dos sete milhões de habitantes.

## Alteração integral antes/depois
**ANTES** = MW-013: mesma costa e baía MW-010, três ilhas hipotéticas, relevo MW-011, hidrografia MW-012 e malha orgânica MW-013. Não há núcleo urbano geocodificado. **DEPOIS** = mesma base e novas camadas de nove polígonos de macronúcleo, mais faixa candidata de contato urbano Kingswell–Sulfok. Controles de camada são equivalentes nos dois painéis; sem omitir ilhas, afluentes ou lagoas.

Abrir `comparador-integral-nucleos-mw014-2010.html`. Os polígonos são geométricos e procedem exclusivamente de `macroposicoes-nucleos-urbanos-2010.proposal.json`, nunca da renderização como autoridade. Cores são apenas representação técnica.

## Questões de aprovação substantiva
1. **Composição geral:** distribuição dos nove macronúcleos em relação ao relevo, baía, Rio Vasyl e Ermos.
2. **Contato Kingswell–Sulfok:** aceitar, rejeitar ou ajustar a faixa contínua de ocupação proposta. Nenhuma ferrovia ou rua foi desenhada.
3. **Separações de Bukovie:** as retas diretas até Kingswell e Alexandria cruzam Ermo; isso não proíbe corredores técnicos futuros.
4. **Forma e escala:** aprovar ou pedir ajustes nos contornos urbanos antes do aceite integral. Esses contornos não são limites administrativos.

Propostas em análise **não canonizam** GEO-004.4 e não alteram arquivos proprietários de raions, crônica, política ou runtime.

## Validação
Prevalidação em JavaScript sobre dados lidos do GitHub: 1948 amostras/asserções de borda urbana, nove núcleos, um corredor candidato, zero invasões de Ermos, costa ou lagoas; segmentos diretos Kingswell–Sulfok livre de Ermo e Bukovie–Kingswell/Bukovie–Alexandria cruzando Ermo. Inventário do comparador: 1 costa, 3 ilhas, 7 relevos, 3 cristas, 10 envelopes do Ermo, 9 cursos d'água, 3 corpos d'água, 1 trecho termal, 5 bacias e limiar da baía.

**Limitações:** sem teste Node CLI, navegador, interseção exata de todos os segmentos, georreferenciamento, população espacial, fechamento municipal ou verificação de precisão de contorno. O validador `validar-macroposicoes-mw014.mjs` é reproduzível no ambiente Node. Toda posição é candidata e sem aprovação do proprietário.

## Estado de governança
A — Aprovar/refinar macronúcleos e adjacências; pendente.
B — Compatibilidade térmica e posição relativa com recursos, costa e relevo foram consideradas; redes não foram definidas.
C — Política Cainita, senhores, domínio, criaturas e cenas permanecem fora do escopo MW-014.

**MW-014 aberto. Não produzir handoff, não canonizar nem avançar para transportes até conclusão de todas as decisões e validações.**
