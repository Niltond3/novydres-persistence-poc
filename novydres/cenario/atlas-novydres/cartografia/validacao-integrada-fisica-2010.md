---
document_id: MW-006-PHYSICAL-INTEGRATION-2010
subject_id: world-atlas-novydres
year: 2010
workflow_status: COMPLETED_TECHNICAL_REVIEW
compatibility_result: PASS_WITH_LIMITATIONS
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
source_mw005_commit: 360fa98635287e29cf3a641424eb80928addfcf8
---

# MW-006 — Relatório de compatibilidade física integrada (2010)

## Objeto, escopo e autoridade

Validação **cruzada** de quatro propostas geométricas não canônicas do assunto
`world-atlas-novydres`: costa/ilhas MW-002, relevo MW-003,
hidrografia MW-004 e Corredores do Ermo MW-005. Não são criadas nem alteradas geometrias nesta unidade.

As fontes editoriais e canônicas são as do mesmo snapshot de master
`27595ca32652efdef3d406eb91e4482299056bd9`, resolvidas via
`novydres/AGENTS.md`, `CONTEXT.md` e `catalogo.json`.
ADR-002, PRD-ATLAS-001 e `guide.md` governam a abordagem.
A referência MW-001 `120 × 100 km` foi aprovada **apenas para modelagem**,
não como município ou CRS real.

**Resultado:** `PASS_WITH_LIMITATIONS` para consistência espacial **sintética/candidata**.
Não equivale a aprovação geométrica do proprietário, certificação hidrológica ou fechamento GEO-002/GEO-003/GEO-004.

## Fontes candidatas verificadas por hash Git

| Camada | Arquivo (em cartografia/) | Git blob SHA | Estado |
| --- | --- | --- | --- |
| MW-002 | `macrogeometria-litoral-baia-ilhas-2010.proposal.json` | `0aefaa2161aa9b728fd03a4ec3d0daf522a81b4d` | `NOT_APPROVED` |
| MW-003 | `macrorelevo-2010.proposal.json` | `c5f6caaddfbef3a89fd5ce85a291ae972e9f35ab` | `NOT_APPROVED` |
| MW-004 | `macrohidrografia-2010.proposal.json` | `34918d5707abac23534df877a8c4b0ec4cefc834` | `NOT_APPROVED` |
| MW-005 | `macroermos-2010.proposal.json` | `2865c843b292c9d128bb2e957634de09c4e4b70a` | `NOT_APPROVED` |

A interdependência declarada é coerente: MW-003 → costa;
MW-004 → costa + relevo; MW-005 → costa + relevo + hidrografia.
`NOVYDRES-LOCAL-2010` usa metros com x leste, y norte e folha
[-60000,+60000] × [-50000,+50000], sem latitude, EPSG, âncora ou limite municipal.

## Matriz de verificação integrada

| Verificação | Resultado | Evidência/ressalva |
| --- | --- | --- |
| Ano, CRS, folha, status e hashes dependentes | **PASS** | Quatro propostas no mesmo referencial; nenhuma aprovada |
| IDs espaciais e referências de dependência | **PASS** | 44 IDs únicos em costa/ilhas, relevo, hidrografia e Ermos |
| Costa e destinos dos rios | **PASS** | Rio Vasyl descarrega na costa interna da baía, vértice 12 dentro da faixa 5–19; drenagens independentes distinguem mar externo e baía |
| Relação vale termal e água | **PASS** | Trecho morno candidato do Vasyl (índices 3–5) contido no vale termal candidato |
| Relevo, Corredores do Ermo e água | **PASS** | Âncoras de serras/tundra/baixada coerentes; 10 polígonos com classes físicas e interseções de rios cadastradas |
| Sobreposição Ermo × lagos | **PASS** | Nenhum dos 10 polígonos sobrepõe os três corpos d'água interiores candidatos |
| Cristas qualitativas × cursos naturais | **PASS** | Nenhum cruzamento sintético entre os 3 eixos de crista e 9 cursos |
| Hidrologia/altimetria reais | **NÃO VERIFICÁVEL** | Não há MDE, cotas, datum, vazão ou perfil sazonal |
| Barreiras efetivas entre núcleos | **NÃO VERIFICÁVEL** | Não há polígonos urbanos aprovados; os Ermos atuais não são cobertura exaustiva |
| Município, dimensão real e EPSG | **NÃO VERIFICÁVEL** | Quadro hipotético, sem limites nem amarração geodésica |

**Inventário auditado:** 3 ilhas secundárias; 7 áreas de relevo e 3 eixos de crista;
5 bacias, 9 cursos, 3 corpos d'água e 1 alcance termal; 10 polígonos dos Ermos.
As superfícies de Ermo somam 801,59 km² **sintéticos e não exaustivos**.
Não usar área total das camadas como área municipal.

A referência das cristas é *qualitativa*: mesmo sem cruzamentos planimétricos,
isto não demonstra divisores de águas ou declividades. Um rio que cruza uma faixa
de Ermo representa drenagem natural, não passagem construída.

## Reprodutibilidade e evidências

Foi executada durante MW-006 uma auditoria de invariantes cruzadas em JavaScript
no ambiente de análise do conector, lendo novamente os quatro arquivos do
GitHub. **Resultado: zero erros** nos testes de status, dependências, IDs, relação
rio–baía, termo–vale, classes/âncoras de Ermo e inventário de cruzamentos.
Isto **não é um job do GitHub Actions nem uma execução comprovada do Node do repositório**.

O validador reproduzível integrado `validar-integracao-fisica.mjs` executa
também **todos os quatro validadores específicos anteriores** com Node, usa
somente bibliotecas nativas e encerra com código não zero em caso de falha.
Executar na raiz do clone:

```sh
node novydres/cenario/atlas-novydres/cartografia/validar-integracao-fisica.mjs
```

**Estado de execução desta publicação:** invariantes integrados reproduzidos em JavaScript;
execução real do validador Node e de CI **não comprovadas nesta sessão**.
O relatório conserva `PASS_WITH_LIMITATIONS` como conclusão da auditoria
geométrica, **não como teste de CI**. Se Node detectar falha, prevalece `FAIL`
e a divergência deverá ser investigada, não encoberta.

## Pendências reais e classificação A/B/C

- **A — decisão substantiva:** aprovação/correção expressa da geometria de costa, relevo, hidrografia e Ermos antes de considerá-las canônicas; estabelecer depois fronteira/ancoragem quando o mapa geral exigir. A aprovação de MW-001 para modelagem não substitui isso.
- **B — condicionantes espaciais:** altimetria, águas sazonais, perímetros urbanos e continuidade efetiva dos Ermos precisam ser avaliados quando essas geometrias forem propostas; nenhum núcleo novo foi criado aqui.
- **C — fora do mandato MW-006:** raions, bairros, transportes, dutos, instituições, domínios Cainitas e runtime de crônica não foram alterados.

## Fechamento da unidade

**Concluída como validação e registro técnico**, sem canonização automática.
A base candidata MW-002…MW-005 permaneceu inalterada. Próxima tarefa
recomendada (unidade distinta): preparar um pacote de deliberação
substantiva sobre as quatro propostas físicas e suas ressalvas, para decisão
do proprietário, sem alterar fatos canônicos silenciosamente.
