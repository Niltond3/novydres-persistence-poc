---
document_id: MW-007-PACOTE-DECISAO-FISICA-2010
subject_id: world-atlas-novydres
reference_year: 2010
workflow_status: READY_FOR_OWNER_SUBSTANTIVE_REVIEW
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED_PROPOSAL_NOT_CONFIRMED
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
source_mw006_checkpoint: bd0b4708b81cc2dfa0105ad7b44866d0809d9638
owner_decision: PENDING
created_on: 2026-11-16
---

# MW-007 — Pacote de decisão conjunta da geografia física candidata (2010)

## 1. Objeto e autoridade

Este arquivo é uma **pauta de deliberação**, não aprovação de geometrias, alteração de fonte canônica ou substituição de `atlas-proposta.md`. O assunto proprietário é `world-atlas-novydres`; ADR-002, PRD-ATLAS-001, `cartografia/contrato-propagacao.md` e `cartografia/guide.md` regulam o procedimento. A unidade não decide raions, transportes, ocupação urbana, infraestrutura ou ficção histórica.

Bootstrap conferido no mesmo HEAD de `master` (`27595ca32652efdef3d406eb91e4482299056bd9`), com `AGENTS.md`, `CONTEXT.md`, `catalogo.json`, sujeito proprietário, índice, fontes físicas e documentação cartográfica. Propostas efetivamente recuperadas no checkpoint MW-006 (`bd0b4708b81cc2dfa0105ad7b44866d0809d9638`):

| Camada | Geometria fonte exclusiva (neste diretório) | Blob Git verificado |
| --- | --- | --- |
| MW-002, costa/baía/ilhas | `macrogeometria-litoral-baia-ilhas-2010.proposal.json` | `0aefaa2161aa9b728fd03a4ec3d0daf522a81b4d` |
| MW-003, relevo | `macrorelevo-2010.proposal.json` | `c5f6caaddfbef3a89fd5ce85a291ae972e9f35ab` |
| MW-004, hidrografia | `macrohidrografia-2010.proposal.json` | `34918d5707abac23534df877a8c4b0ec4cefc834` |
| MW-005, Ermos | `macroermos-2010.proposal.json` | `2865c843b292c9d128bb2e957634de09c4e4b70a` |

O relatório `validacao-integrada-fisica-2010.md` e o validador `validar-integracao-fisica.mjs` pertencem a MW-006; resultado documentado `PASS_WITH_LIMITATIONS` para topologia sintética. **Não há prova nesta unidade de execução do validador Node em GitHub Actions**. Nenhum arquivo geométrico foi editado por MW-007.

O quadro `NOVYDRES-LOCAL-2010`, 120 × 100 km, e o teste de 4.000–7.000 km² de terra municipal são hipóteses de modelagem já aceitas em MW-001; nenhuma das duas define perímetro municipal, EPSG, latitude/longitude, altitude ou área definitiva. A área continental de 8.188,25 km² é somente a terra recortada pela folha, incluindo o que poderá ficar fora do município. O censo canônico de 7 milhões de residentes é preservado.

**Fatos canônicos protegidos:** macrorregião no setor ocidental da Península de Seward, nas proximidades de Port Clarence, sem apagar comunidades reais; predominância continental, baía abrigada, ilhas secundárias; cinco classes de paisagem; Rio Vasyl passa pelo núcleo termal de Cidade Velha/Iknik e deságua na baía, com aquecimento localizado; quatro classes de Ermo interrompem a continuidade urbana. São fatos **qualitativos**, não os vértices destas propostas. Os nove raions continuam nove; Kingswell é nome oficial do raion com ID técnico legado `district-chelsea`.

## 2. Alcance de cada tipo de decisão

- **G — Aprovar a geometria candidata como escolha substantiva de desenho para 2010:** aprova a forma/vínculos explicitados, sujeita a propagação no assunto proprietário e consumidores; antes dessa propagação, estado `APPROVED_PENDING_PROPAGATION`, nunca `CLOSED_CANON`. Não ratifica precisão cadastral, datum, limite municipal ou equipamentos ausentes.
- **M — Aprovar somente a macro-organização morfológica:** mantém os vértices do JSON como **hipótese operacional corrigível**, sem declarar os contornos oficialmente escolhidos. As regras qualitativas já canônicas não precisam de segunda aprovação.
- **R — Solicitar revisão dirigida:** modifica só a camada identificada e revalida a cadeia de dependências depois da revisão; nenhuma variante nova é aprovada implicitamente.
- **D — Adiar:** mantém o estado atual `PROPOSED_PENDING_OWNER_REVIEW`.

**Sem resposta inequívoca do proprietário, todas as quatro decisões permanecem D (pendentes).** Um simples “aprovo o relatório” não autoriza alteração do cânone nem equivale a opção G. Uma aprovação que escolher G será registrada como decisão do proprietário, mas a propagação canônica e seus testes pertencem a unidade posterior explicitamente autorizada.

## 3. Decisões substantivas integradas

### FIS-01 — Forma da baía, litoral e ilhas (MW-002)

**Configuração candidata:** costa continental externa no lado oeste do quadro e grande reentrância abrigada por promontório setentrional; entrada delimitada cartograficamente pelos vértices costeiros 5 e 19; três ilhas pequenas (duas internas, uma externa). A boca de cerca de 18,4 km e os 1.851,25 km² de baía são métricas sintéticas da hipótese, **não medições aprovadas**.

- **G:** aceitar a linha de costa, orientação relativa da boca e os três polígonos insulares como desenho físico de referência para 2010; futuras transformações geodésicas não podem ser presumidas.
- **M (recomendado se a forma geral agrada, mas falta aferição cartográfica):** aceitar o arranjo costa ocidental → baía protegida → promontório ao norte → ilhas secundárias, mantendo contornos, largura de boca e número/posição exatos das ilhas em proposta.
- **R:** redesenhar a boca ou reduzir/redistribuir ilhas; exige recalcular polígonos derivados e revalidar relevo, drenagem e Ermos.

**Impacto:** esta é a dependência geométrica raiz de MW-003/004/005. Não implica porto, profundidade, acesso em todas as estações, substituição de Port Clarence nem fronteira municipal.

### FIS-02 — Vale termal, serras e baixadas (MW-003)

**Configuração candidata:** sete polígonos não exaustivos: vale termal interior; três massas de serra (norte, leste, sul) com três eixos qualitativos; duas regiões de tundra e uma baixada úmida. O vale é âncora fisiográfica, **não perímetro do núcleo Iknik ou de Kingswell**. Os eixos de crista não demonstram divisores de águas.

- **G:** aceitar os sete polígonos e os três eixos como macroformas de referência, com altitudes e cotas não atribuídas.
- **M (recomendado enquanto não existe altimetria):** preservar a relação vale interior → serras/contrafortes → tundra/baixadas, mantendo os limites concretos ajustáveis sem alegar terreno integralmente classificado.
- **R:** deslocar vale ou serras; exige atualizar cotas/encadeamento qualitativo e reavaliar nascentes, lagoas e polígonos de Ermo relacionados.

**Impacto:** deslocar o vale termal pode romper o vínculo do trecho aquecido do Rio Vasyl; as três serras condicionam drenagem e barramentos, mas não determinam vias nem posição dos raions.

### FIS-03 — Rio Vasyl e sistemas aquáticos (MW-004)

**Configuração candidata:** grafo de nove cursos; Rio Vasyl oriundo de contrafortes setentrionais, recebe dois afluentes, atravessa vale termal e chega à baía no vértice costeiro 12. Cinco envelopes de microbacias; um lago doce interior, uma lagoa salobra costeira com canal mareal e uma piscina termal com escoamento para o rio. A foz no setor de Sulfok **não está ratificada**; o vértice 12 é desenho, não topônimo administrativo.

- **G:** aceitar como macrotraçados de referência as linhas, destinos, confluências e três corpos d'água candidatos, sem inventar vazão, temperatura, profundidade ou divisas de drenagem demonstradas.
- **M (recomendado antes de haver MDE/cotas):** usar o grafo hidrológico como esquema conectivo de trabalho, mantendo curso exato, vértices de foz, divisores das cinco bacias e posição de corpos d'água corrigíveis.
- **R:** alterar foz, confluência ou corpo d'água específico; exige atualizar o grafo e as zonas úmidas/Ermos dependentes.

**Impacto:** a conectividade e o trecho termal local foram validados sinteticamente; não há evidência de gradientes altimétricos ou regime sazonal. Aprovar o grafo não ratifica canal subterrâneo em New London ou o trajeto por Sulfok.

### FIS-04 — Distribuição dos Corredores do Ermo (MW-005)

**Configuração candidata:** dez fragmentos naturais não exaustivos, sendo três rochosos, três de tundra, dois de várzea e dois de costa externa; soma de 801,59 km² sintéticos. Rios podem atravessar Ermos sem constituir travessias construídas. Fragmentos e vazios não são linhas administrativas.

- **G:** aceitar os dez polígonos como amostras espaciais canônicas dessas categorias, **não como perímetro exaustivo de todos os Ermos nem prova de isolamento de núcleos urbanos**.
- **M (recomendado):** conservar os dez segmentos como âncoras morfológicas operacionais, adiando o fechamento de extensão/continuidade funcional até existir geometria de núcleos; sem inventar passagens.
- **R:** ajustar a proporção/posição entre Ermos rochosos, de tundra, várzea e costa, garantindo que a revisão preserve terra/água e os cursos naturais.

**Impacto:** isolamento predominante de núcleos é cânone qualitativo, mas não há polígonos de núcleos que permitam certificá-lo. Exigir agora uma barreira totalmente contínua ou cobertura exaustiva seria precisão artificial.

## 4. Escolha conjunta, precedência e ressalvas

**Recomendação editorial MW-007:** optar por **M nas quatro decisões** se a macroconfiguração for aceitável. Isso dá continuidade ao modelo integrado como hipótese visual e espacial controlada sem a falsa ratificação de contornos absolutos; nenhum GEO é encerrado com essa escolha. A escolha **G** pode ser feita individualmente quando o proprietário quiser ratificar um contorno específico, sempre observando a propagação posterior e o efeito sobre dependências.

Ordem obrigatória de revisão material: **FIS-01 → FIS-02 → FIS-03 → FIS-04**. Revisão de costa aciona as demais; revisão do relevo aciona água e Ermo; revisão de água aciona Ermo. Não duplicar linhas/polígonos para facilitar edição.

**Limitações técnicas remanescentes (não escondê-las como PASS):** ausência de modelo de elevação e datum vertical, hidrologia sazonal, área/perímetro municipal e ancoragem EPSG; sem demonstração da separação efetiva dos futuros núcleos; geometrias escassas não representam cobertura total de terreno, drenagem ou Ermos. A validação MW-006 não testou engenharia ambiental real, portos, gelo sazonal ou viabilidade de ocupação.

**Registro A/B/C:**
- **A (decisão desta unidade):** escolha expressa G/M/R/D por FIS-01..04; sem escolha, permanece pendente, sem canonização. Futuro fechamento físico exigirá propagação e validação remota.
- **B (apenas consequências espaciais):** necessidade eventual de altimetria e limites de ocupação para aferir água e barreiras naturais; ancoragem/perímetro municipal para área real. Não resolver redes e equipamentos nesta unidade.
- **C (fora de escopo):** divisas e população por raion, transportes, dutos, instituições, domínio Cainita, história política, crônica e runtime.

**Dependências protegidas:** GEO-002.1–002.4; GEO-003.1–003.5; GEO-004.3; GEO-014.1–014.2 e as demais fontes proprietárias relacionadas; não alterar fatos aprovados nem renomear IDs técnicos nesta unidade.

## 5. Protocolo de decisão e continuação

Resposta inequívoca esperada do proprietário: indicar **FIS-01, FIS-02, FIS-03 e FIS-04** com opção **G/M/R/D** e, no caso de R, a correção substantiva desejada. A escolha deve explicitar se é aprovação de desenho de 2010 ou mera aceitação da macro-organização. **A publicação deste pacote não é consentimento.**

Esta unidade cria apenas este pacote documental. Não altera `master`, candidatos, verificadores, fontes canônicas ou conteúdos de raions/transportes. Após o proprietário decidir, uma **nova unidade** deverá registrar a decisão com sua autoridade exata, atualizar/propagar apenas os escopos autorizados, executar os validadores pertinentes e realizar readback remoto. Se a resposta for M ou D, não promover geometria a cânone.

Handoff operacional conforme `cartografia/guide.md`: iniciar a próxima conversa no HEAD atual de `master`, resolver `world-atlas-novydres` pelo catálogo e ler o pacote e quatro JSONs no checkpoint remoto da branch MW-007. Handoffs jamais substituem os arquivos GitHub.
