---
document_id: MW-013-CLOSURE-HANDOFF
subject_id: world-atlas-novydres
work_unit: MW-013
work_unit_status: CLOSED_FOR_SCOPE
reference_year: 2010
canonical_status: NOT_APPROVED
source_closure_commit: 89fb79f933489998e0e2be9c9cec2230861f5898
next_work_unit: MW-014
---
# NOVYDRES MAPWORK — HANDOFF MW-013 → MW-014

**Repositório:** `Niltond3/novydres-persistence-poc`  
**Branch de trabalho MW-013:** `mapwork/mw-013-refinamento-ermos-fis04`  
**Commit de fechamento verificado remotamente:** `89fb79f933489998e0e2be9c9cec2230861f5898`  
**Unidade concluída:** macrogeometria territorial FIS-04 dos Ermos de Novydres (2010), com composição A e refinamento orgânico B aprovados pelo proprietário como **base de trabalho não canônica**.

## Entregas persistidas
- `novydres/cenario/atlas-novydres/cartografia/macroermos-2010.proposal.json` — projeção FIS-04 consolidada e estado de aprovação final.
- `novydres/cenario/atlas-novydres/cartografia/malha-territorial-ermos-fis04-2010.refined.proposal.json` — geometria estruturada aprovada para trabalho, 10 envelopes / 2.349 vértices.
- `novydres/cenario/atlas-novydres/cartografia/comparador-integral-ermos-fis04-2010.html` — antes/depois completo, mesmo recorte e todas as feições físicas; ilhas e nove cursos d'água presentes.
- `novydres/cenario/atlas-novydres/cartografia/visualizador-fisico-2010.html` — atlas 2D de leitura geral atualizado com Ermos.
- `novydres/cenario/atlas-novydres/cartografia/validar-malha-territorial-fis04.mjs` e `novydres/cenario/atlas-novydres/cartografia/validar-macroermos.mjs` — validação de topologia e integridade de projeções.
- `novydres/cenario/atlas-novydres/cartografia/refinamento-ermos-fis04-2010.md` — relatório de decisões, validações e fechamento.
- `novydres/cenario/atlas-novydres/cartografia/guide.md` — diretriz expressa de apresentação visual **integral ANTES/DEPOIS**.

**Validações:** 10 componentes conectados por contato, zero invasão de costa ou água, 2.689 pontos, 180.873 interseções com bordas de costa/água e 360.367 comparações de segmentos para auto-interseção PASS; leitura remota de 11 arquivos/51 verificações de integração PASS, scripts dos visores sintaticamente válidos. **Limitações:** sem execução em navegador real, Node CLI, CI externo, geometria municipal oficial ou união materializada dos polígonos.

**Restrições:** não houve canonização; `master` inalterada; costa MW-010, relevo MW-011, hidrografia MW-012 seguem bases de trabalho não canônicas; ilhas permanecem hipótese e nenhum raion ou trajeto de transporte foi localizado. O Ermo representa natureza não submetida à ocupação, não categorias fisiográficas. Áreas fora da malha não são automaticamente urbanas. Exemplos de ameaças sobrenaturais não viraram lugares cartográficos.

**Pendências materiais para MW-014:** 
- **A:** posicionar e validar geometricamente relações entre ocupação urbana e Ermos, incluindo o caso de conurbação indicado pelo proprietário para Kingswell/Cidade Velha–Sulfok e as separações por Ermo indicadas para Bukovie–Kingswell e Bukovie–Alexandria; coordenadas e limites oficiais dos raions **ainda não estão aprovados**.
- **B:** conciliar ocupação com geotermia, rio, costa, relevo e extensão real dos Ermos; não fixar transportes ou eventos políticos.
- **C:** narrativa de ameaças, Garou, caerns, domínio Cainita e história não estritamente cartográfica — fora do escopo da próxima unidade.

## Próxima unidade pequena proposta
**MW-014 — Hipótese de macroposições dos núcleos urbanizados e adjacências espaciais entre os nove raions em 2010.**  
Entregável/aceite: geometria espacial **candidata**, demonstrando interfaces entre áreas habitadas, Ermos e possíveis conurbações, sem impor limites administrativos oficiais ainda não aprovados, comparador completo ANTES/DEPOIS para revisão, validação topológica e aprovação substantiva do proprietário. Não canonizar.

## Prompt curto para o próximo chat
```text
NOVYDRES MAPWORK — MW-014

Objetivo único: propor e validar as macroposições dos núcleos urbanizados e suas relações com os Ermos em Novydres (2010), sem fixar automaticamente os limites oficiais dos nove raions.
Entregável: geometria candidata de ocupação e adjacências, comparação visual integral ANTES/DEPOIS com ilhas, costa, relevo e toda a hidrografia, validação espacial e aprovação do proprietário.

Repositório: Niltond3/novydres-persistence-poc
Checkpoint MW-013: branch mapwork/mw-013-refinamento-ermos-fis04, commit 89fb79f933489998e0e2be9c9cec2230861f5898.

Execute bootstrap no HEAD atual de master conforme AGENTS.md, CONTEXT.md e catalogo.json; siga ADR-002, PRD-ATLAS-001 e cartografia/guide.md. Recupere no GitHub os fechamentos MW-010 a MW-013, a malha FIS-04 refinada e a geografia/história canônicas pertinentes. Preserve estados não canônicos, não altere a crônica ou runtime. Um ponto de decisão por vez; não avance para transportes ou canonização. Só feche e emita handoff após aceite integral e readback remoto.
```

**Este handoff é um localizador, não uma fonte de verdade. Verificar o HEAD remoto da branch e o HEAD atual de master no próximo chat.**
