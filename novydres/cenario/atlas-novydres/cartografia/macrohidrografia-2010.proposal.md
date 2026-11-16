---
document_id: MW-004-MACROHIDROGRAFIA-NOTAS
subject_id: world-atlas-novydres
reference_year: 2010
workflow_status: PROPOSED_PENDING_OWNER_REVIEW
canonical_status: NOT_APPROVED
truth_state: GM_PREPARED
source_master_sha: 27595ca32652efdef3d406eb91e4482299056bd9
dependent_relief_commit: 79772905f0e895c236b31abea059ef2ed085e866
---

# MW-004 — Macrogeometria hidrográfica candidata (2010)

## Entrega e autoridade

A geometria única está em [`macrohidrografia-2010.proposal.json`](macrohidrografia-2010.proposal.json), validável por [`validar-macrohidrografia.mjs`](validar-macrohidrografia.mjs). Os arquivos seguem o assunto `world-atlas-novydres`, ADR-002 e PRD-ATLAS-001. Nenhuma feição desta proposta está canonizada. MW-001 forneceu quadro **aprovado apenas como hipótese operacional**; costa MW-002 e relevo MW-003 são **candidatos não aprovados**. O JSON aponta para seus blobs Git, sem duplicar litoral ou polígono de relevo.

## Hipótese testável

- **Rio Vasyl / Reka Vasilya:** rede dirigida de cabeceira candidata em contrafortes setentrionais, passagem pelo vale termal e foz na baía (vértice costeiro candidato 12). Dois afluentes convergem somente em nós declarados. A posição do núcleo Iknik dentro do vale **não foi delimitada**.
- **Microbacias independentes:** drenagem meridional com saída na baía (vértice 9), drenagem setentrional para mar aberto (vértice 24), bacia de lago de água doce com saída para litoral exposto (vértice 1) e pequena bacia de lagoa costeira com canal mareal sobre o segmento 11→12. As cinco áreas são **envelopes aproximados, não divisores hidrológicos comprovados**; áreas sem polígonos permanecem sem classificação.
- **Corpos d'água:** um lago de água doce na tundra, uma lagoa costeira salobra separada da baía por terra candidata e conectada por canal mareal, e uma piscina termal localizada no vale. O afloramento liga-se ao Rio Vasyl por pequeno escoadouro, sem tornar o rio inteiro quente.
- **Relação com relevo:** origens e zonas molhadas dialogam com serras, baixadas e tundra do MW-003. Sem curvas de nível, DEM ou datum, declividade e contorno definitivo de bacias **não são demonstrados**. Nenhum nome secundário torna-se topônimo aprovado.

## Topologia e validação

O modelo usa `NOVYDRES-LOCAL-2010`, metros de desenho, não WGS84/GeoJSON. `points_xy_m` são ordenados de montante para jusante; `downstream` explicita confluência, entrada em lago, vértice ou segmento da costa. Lagos têm anéis únicos, entradas/saídas por IDs. `localized_thermal_reaches` apenas referencia índices do Rio Vasyl, sem copiar sua linha.

Rodar na raiz do repositório:

```sh
node novydres/cenario/atlas-novydres/cartografia/validar-macrohidrografia.mjs
```

O validador confere hashes Git das duas geometrias precedentes, estados de não aprovação, quadro, IDs, linhas, anéis, terra/água, vazamento pela costa, separação de microbacias, conexões e escopo. **Foi efetuada validação geométrica preliminar por JavaScript na sessão de modelagem**; a execução do arquivo Node no ambiente do repositório não é reivindicada sem evidência independente. A validação prova consistência sintética, não coerência altimétrica, hidrológica sazonal ou física costeira.

## Decisão aberta e próximo trabalho

Aprovação substantiva do proprietário ainda é necessária para o curso e a foz do Vasyl, as divisões de microbacias, os outros escoamentos e lagos, e a ligação termal. Revisões da costa/relevo forçam revalidação desta camada. Sem limites municipais, raions, transportes, pontes, dutos, portos, drenagem subterrânea ou dados de vazão. O status de GEO-003.4 continua canônico **somente em seu alcance qualitativo** no arquivo proprietário `../macrorelevo-hidrografia-ermos-2010.json`.
