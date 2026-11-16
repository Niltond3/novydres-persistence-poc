# Novydres Mapwork — guia operacional de continuidade

Este arquivo contém **modelos de passagem de trabalho**, não geografia nem cânone. A fonte da verdade é o GitHub atual, sobretudo `novydres/AGENTS.md`, `novydres/CONTEXT.md`, `novydres/catalogo.json`, ADR-001, ADR-002, PRD-ATLAS-001 e os arquivos proprietários dos assuntos.

**Nunca reconstruir fatos a partir da memória de chat ou de um handoff.** Textos de handoff são localizadores e instruções, não evidência. Reconfirmar os fatos e o checkpoint no repositório.

## Modelo de encerramento de unidade

```text
NOVYDRES MAPWORK — HANDOFF MW-XXX → MW-YYY
Repositório: Niltond3/novydres-persistence-poc
Branch de trabalho: <branch>
HEAD remoto verificado: <SHA>
Unidade concluída: <objetivo + critério de aceite>
Entregas persistidas: <caminhos de arquivos e commits>
Validação: <evidências verificadas / não verificadas>
Pendências materiais: <somente impedimentos para o próximo passo>
Próxima unidade: <um objetivo, um entregável e um critério de aceite>
Referência operacional: novydres/cenario/atlas-novydres/cartografia/guide.md
```

Não copiar narrativas extensas, fatos canônicos ou histórico de discussão. Apontar para arquivos e IDs exatos. Se não houve escrita, declarar explicitamente.

## Modelo de prompt do próximo chat

```text
NOVYDRES MAPWORK — MW-YYY

Objetivo único: <objetivo>
Entregável/aceite: <entregável verificável e critério>
Repositório: Niltond3/novydres-persistence-poc

Abra o HEAD atual de master; leia AGENTS.md, CONTEXT.md e catalogo.json no mesmo SHA; siga o ADR-002, o PRD-ATLAS-001 e cartografia/guide.md. Resolva no GitHub os assuntos, fontes e dependências desta unidade. O handoff anterior serve apenas para localizar arquivos e checkpoints; valide tudo remotamente. Preserve o cânone, o escopo cartográfico e a governança.

Execute leitura, proposta/implementação autorizada e verificações proporcionais ao bloco. Só peça decisão substantiva ao proprietário. Não avance para outra unidade. Termine com handoff e prompt mínimo para MW-YYY+1 usando o modelo do guia.
```

## Política de divisão

Cada chat trata **uma unidade pequena e verificável**, não uma fase inteira obrigatoriamente. Encerre por entregável e não pelo limite de contexto. Se ficar grande, corte no último ponto coerente realmente persistido e verificado; nunca anuncie PASS sem evidência.

- **A — Bloqueante do mapa:** resolver ou propor decisão para construir/validar a geometria.
- **B — Condicionante geográfica:** registrar a consequência espacial e deixar o restante narrativo aberto.
- **C — Fora do escopo:** registrar sem investigar.

Não exigir que todas as pendências do suplemento sejam fechadas. Não usar `guide.md` como fonte de novos fatos, de estado de projeto ou como substituto dos assuntos proprietários.
