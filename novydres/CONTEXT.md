# NOVYDRES — navegação candidata por assunto (não operacional)

Escopo deste checkpoint: 79 assuntos candidatos, incluindo a amostra histórica C41, fontes globais D03, 9 distritos, 32 locais e 20 módulos de regras; a identidade global do protagonista tem origem nominal aprovada, sem importar seu estado. **O checkpoint local da amostra C41 não equivale ao estado atual de master em C45.**

Entradas propostas para E: `AGENTS.md`, este `CONTEXT.md` e `catalogo.json`, todos lidos no mesmo commit. O catálogo é gerado de `cenario/**/assunto.json`, `personagens/**/assunto.json`, `cronicas/**/assunto.json` e `sistema/regras/**/assunto.json`, com arquivos e vínculos derivados. `novydres/scripts/catalogo-assuntos.mjs --check` rejeita divergência de bytes e IDs; o CI testa leitura por SHA e proteção de divulgação. Nenhum caminho antigo é fallback. O vínculo C41 para a identidade global do protagonista foi resolvido por ID, preservando a relação local; isso não migra recursos, conhecimento ou o checkpoint corrente de C45. A equivalência de D03 e as fases D04–D07 continuam sujeitas aos respectivos gates.

O contrato único de condução **candidato** está em `novydres/sistema/narrativa/contrato.md`, com configuração local sob o subject `chr001-table-config` recuperável pelo catálogo. O contrato consolida DEC-01–15, 18, 20, 23–27 e A04, mas não é outro bootstrap nem herda autoridade operacional. Situações fictícias N-01–N-08/N-06-RESULT e sua revisão contextual anterior permanecem fontes históricas de teste, não cenas reais.

**Não ativar este desenho** para a crônica: os contratos operacionais de `master` permanecem até E02 expressamente aprovado.
