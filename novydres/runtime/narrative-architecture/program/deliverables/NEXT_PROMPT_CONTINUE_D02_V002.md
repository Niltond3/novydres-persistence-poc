# NOVYDRES · CHR-001 · DRAMATURGO — CONTINUAR D02 (NÃO D03)

STATUS: PLAYER_SAFE. D02 V002 está publicada apenas como PROGRESSO; auditoria **FAIL**, D03 **BLOQUEADA**. Novo chat, mesmo mandato D02; nunca narrar, rolar, iniciar C06, avançar a 2010, alterar cânone, LIVE, CYCLE, manifesto, ficha, XP/FV, conhecimento NPC ou episódios fechados.

## Repositório e cursores (REDESCOBRIR)
- GitHub: `Niltond3/novydres-persistence-poc`; branch **master somente leitura**; HEAD observado `124f9a9f43ed427d3db106d9187a875d74f60ac6`, NÃO presumir atual.
- Branch documental de escrita: `design/chr001-narrative-program-d01`; conteúdo D02 V002 no commit `537614af97464445f2e196e031290d53cd0200aa`. O HEAD da branch muda ao publicar este prompt, portanto SEMPRE consultar o ref API atual.
- Maior ciclo observado: `novydres/chronicles/CHR-001/orchestration/CYCLE_V0033.json` blob `51afa7fa15ba7dc49a863dfe6f6bb0c539014a6a`; status READY_FOR_DRAMATURGO; C05 CLOSED; C06 NOT_STARTED; última âncora `CHR001-M301-C05-22-20261109-001`. Validar ciclo mais novo NUMERICAMENTE, antecessores, manifesto, LIVE, e seis refs + dossier/sidecar antes de prosseguir.

## Primeira leitura obrigatória
Abrir [START_HERE_PLAYER_SAFE_V1.md](https://github.com/Niltond3/novydres-persistence-poc/blob/master/novydres/runtime/narrative-architecture/program/START_HERE_PLAYER_SAFE_V1.md); depois ler na mesma pasta `ARCHITECTURE_PLAN_V1.md`, `PROGRAM_RUNBOOK_V1.md`, `D01_MANDATE_V1.md`, `PROGRAM_HANDOFF_CONTRACT_V1.md`, e `novydres/.AGENT.md`, `novydres/.CONTEXTG.md`. Ler autoridade de governança, D1/D2/H, G28, orquestração, Dramaturgo/Narrador, CH00–CH07. Dossiês são PREP, não história jogada. Nenhum livro de referência é fonte para novos eventos.

## Arquivos da branch de design
Todos os nomes a seguir na pasta `novydres/runtime/narrative-architecture/program/deliverables/`.

**D01 PASS** — conferir auditoria e os dez: `D01_ARCHITECTURE_V001.md`, `D01_CONTRACTS_V001.json`, `D01_LIFECYCLE_V001.md`, `D01_GOVERNANCE_V001.md`, `D01_VALIDATOR_V001.mjs`, `D01_TEST_RUNNER_V001.mjs`, `D01_TEST_VECTORS_V001.json`, `AUDIT_D01_V001.json`, `HANDOFF_D01_V001.json`, `NEXT_PROMPT_D02_V001.md`.

**D02 V001 (baseline parcial)** — `D02_SOURCE_INVENTORY_V001.json` (blob 2930c663076969d7bb1071220bbe7d862409fc23), `D02_EVENT_HISTORIOGRAPHY_V001.json` (a1e5f007c8a9fad8581b1cd494f5ae1b94a40012), `D02_CAUSAL_MAP_V001.json`, `D02_COVERAGE_AND_PROVENANCE_V001.json`, `D02_DOCUMENTARY_SEQUENCE_PLAYER_SAFE_V001.mmd`, `AUDIT_D02_V001.json` (cff563cb8474826de5c6bdcef477e068fd700005), `HANDOFF_D02_V001.json` (d78004798a9416f66c33da8aae4c46c267fc46c9). NÃO tratar 661 localizadores como eventos COMMITTED.

**D02 V002 (suplementação publicada e readback PASS)**:
- `D02_SOURCE_ASSERTION_CHECKS_V002.json` — blob `3b8e2b147ecfb3b56ca7ff48d696f9fdf8dd9162`
- `D02_SEMANTIC_CASEBOOK_V002.json` — blob `36477d8a87b70868823e5325704efc409e63b0d9`
- `D02_CAUSAL_MAP_V002.json` — blob `cdd9730869adf29fbf5d0215bcc1e592fe801cf7`
- `D02_AUTHORSHIP_EVIDENCE_V002.json` — blob `22eb0c07cc1deb74bafd27dfa11cd4780f0a0bc3`
- `D02_COVERAGE_AND_PROVENANCE_V002.json` — blob `27e1c5fdfd2083c1d3e8ed9de1c701e0d9a30bba`
- `AUDIT_D02_V002.json` — blob `8a9a3d1294c5ea6bf0d3fdebba35b07d4ea18863` — status FAIL.
- `HANDOFF_D02_V002.json` — blob `5a4b0b53e8b36d527b7b7d3b8605acdbff39cb3a` — status FAIL.
- `NEXT_PROMPT_CONTINUE_D02_V002.md` — este prompt, descobrir blob SHA atual após publicação.

## Achados confirmados e limites
- Cadeia CYCLE 1–33 e refs mais recentes passaram; D01 7/7 blobs; 661/661 verificações de SHA, intervalo e texto não vazio; 633/661 excertos coincidem diretamente e **28 exigem revisão contextual**. Isso NÃO é revisão semântica conclusiva.
- 12 casos selecionados com prova em linhas no casebook V002. As outras afirmações ainda precisam de adjudicação de voz, decisão, efeito e saída.
- Versões cumulativas conferidas por prefixo; v007 invalid_partial de M2.03 é preservada como artefato histórico **inválido**, jamais fonte prevalente.
- M1.01 nasceu como prólogo anterior ao gate e foi reclassificado depois; correção M1.06 prevalece. M2.03 correção mecânica não gera novo ataque. C04.09 prevalece sobre tentativa anulada C04.08.
- O elo D02-CAUSE-002 foi rebaixado a SEQUENCE_ONLY (transcrição original ainda pendente), não publicar como causa provada. O atlas continua PARTIAL. `OPEN_THREADS_V23` tem 44 itens heterogêneos, não 44 tramas.
- Datas de commits comprovam publicação, **não autoria criativa original**: `AUTHOR_UNKNOWN` salvo prova contemporânea individual. Resumos de episódios não são transcrições literais; ledger técnico COMMITTED não foi migrado.

## Resolver integralmente antes de PASS
1. `D02-GAP-001`: M1.01–M1.09 com prólogo, fora do índice, identificação de PLAYER/NPC_CLAIM/NARRATOR, erratas, decisão/efeito/estado.
2. `D02-GAP-002`: M2.01–M2.03 com legado, shard e versões, separar voz, notas, regra, correções prevalentes e resultados.
3. `D02-GAP-003`: M2.04 C01–C17 e downtime; M3.01 C01–C05; conciliar anteriores/cumulativos e evidência original, NPC epistemologia, todos os eventos decisivos.
4. `D02-GAP-004`: autoria original por cena a partir de contemporaneidade; manter AUTHOR_UNKNOWN sem prova; plano posterior ≠ autoria original.
5. `D02-GAP-005`: todos os elos avaliados de ambos os lados como CAUSAL_CONFIRMED / SEQUENCE_ONLY / THEMATIC_ONLY / UNKNOWN, sem conspiração inferida.
6. `D02-GAP-006`: G28, rolagens e origem da aleatoriedade (VERIFIED ou UNKNOWN), Atlas V001 e COVERAGE_REPORT_V002 PARTIAL. Não inventar migração técnica.

Preservar `D01-ADM-001`: manifesto pode ter ponteiros antigos; cursor é maior ciclo validado, sem conserto silencioso. As versões V001/V002 publicadas são imutáveis; escrever apenas NOVOS arquivos V003 ou outros nomes versionados no diretório `deliverables`. Branch lease por expected_sha; commit atômico por conjunto, SHA/blob/content readback; master intocado. Auditoria editorial INDEPENDENTE obrigatória para PASS, além do validador estrutural. Saída somente PLAYER_SAFE, sem GM_HIDDEN.

## Encerramento condicionado
Se D02 atingir PASS real, publicar auditoria, handoff, artefatos finais em versões NOVAS e apenas então prompt D03 completo para novo chat. Se ainda houver lacuna, manter FAIL, publicar progresso e `NEXT_PROMPT_CONTINUE_D02_V003.md` (ou sucessor livre), **nunca D03**. A promoção operacional e eventual prompt NARRADOR são exclusivos de D12 e exigem aprovação expressa, READY_FOR_NARRATOR e autorização de cena; nenhuma dessas permissões está presente.
