# NOVYDRES — Fase B, protótipo isolado

**Gate B_REMEDIATION_REQUIRED**. Cópias de 1 NPC, 1 trama candidata, 1 história textual jogada e 1 estado no layout por assuntos, apenas na branch design. Snapshot master fonte `c26c0fbf15fff6c817182c06e6208e302b954f3a`; parent candidato inicial `cef04faa7e8e9c015a1cb3c7b5b3e607ebfcea73`. Divergência documentada em conflitos.json, sem merge, sem alteração de runtime, cânone, ciclos, XP ou FV.

Evidência executada: **30/30** comparações pareadas de valores recuperados dos documentos originais e dos candidatos; **12/12** ataques por mutação de objetos com rejeição determinística local; **12/12** jornadas de transação em simulador. **3 leituras reais** do arquivo-fonte pelo conector GitHub Web: latência p50=421ms, p95=443ms. Codex, 3 rodadas conversacionais completas por canal, tokens reais, bytes HTTP e teste real de concorrência/CI: **NOT_EXECUTED/NOT_EXPOSED**. Não confundir testes locais com CI ou execução real de agentes.

A trama é interpretação editorial *somente candidata* de fio aberto, sem admissão D04. A história preserva 8 marcadores de texto jogado sem transformá-los em ledger COMMITTED. O estado reproduz o cursor C41 e o recurso do LIVE, explicitando o cursor LIVE histórico diferente. Consultar matriz-equivalencia.json, conflitos.json e handoff-remediacao-b.md.

## Medição de navegação complementar
Três pares de consultas reais de conhecimento situado no conector Web: legado 1 leitura, p50 438 ms/p95 500 ms, 58.743 caracteres; assunto 3 leituras, p50 1.247 ms/p95 1.353 ms, 2.064 caracteres. **Há redução de texto recuperado, mas aumento real de chamadas e latência neste ensaio.** Não extrapolar para tokens, custo total ou 30 perguntas; o catálogo final ainda não existe. Detalhes em `navegacao-web.json`.
