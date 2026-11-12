# NOVYDRES — navegação candidata por assunto (não operacional)

Escopo deste checkpoint: protótipo de cinco subjects de B/C, derivado do cursor **C41 histórico**, não equivalência corrente a `master` em **C45**. Fonte autoritativa de tarefas: `sistema/arquitetura/plano-integral/tarefas.md`; política aceita: `sistema/arquitetura/adr/001-subject-oriented.md` §11. Ambas são documentos de desenho, não novos bootstraps operacionais.

Entradas propostas para E: `AGENTS.md`, este `CONTEXT.md` e `catalogo.json`, todos lidos no mesmo commit. O catálogo é gerado de `personagens/**/assunto.json` e `cronicas/**/assunto.json`, com arquivos e vínculos derivados. `novydres/scripts/catalogo-assuntos.mjs --check` rejeita divergência de bytes e IDs; o CI testa leitura por SHA e proteção de divulgação. Nenhum caminho antigo é fallback. O vínculo externo C41 ainda não migrado permanece `DEFERRED` até a migração completa de D.

**Não ativar este desenho** para a crônica: os contratos operacionais de `master` permanecem até E02 expressamente aprovado.
