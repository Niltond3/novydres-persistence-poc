---
document_id: MW014-ERMO-G-ARTISTICO-CANDIDATE-CHECKPOINT
subject_id: world-atlas-novydres
work_unit: MW-014
status: OWNER_VISUAL_REVIEW_PENDING
owner_approval: NOT_REQUESTED_OR_GRANTED_FOR_G_GEOMETRY
canonical_status: NOT_APPROVED
source_master_sha: 5931f306c1e547d169d6e4bbb69114d616a6011c
source_branch_parent_sha: d9c0c0dcf3ab946de6e1fece878f148811d92ac5
base_coast: MW-010_ONLY
---

# MW-014 — estudo visual e geométrico candidato G (sem aprovação)

O proprietário solicitou em 17/11/2026 uma nova proposta **artisticamente finalizada** de Ermos com quatro tipos: gelado, acidentes geográficos, pântanos e tundra, usando o mapa ilustrativo fornecido como referência estética, sem copiá-lo como verdade geométrica. **F foi expressamente rejeitada** e não é base desta proposta.

Foi produzido localmente no ChatGPT um modelo G em JSON estruturado, SVG artístico, HTML interativo offline com comparação ANTES/DEPOIS e PNG. **Esses bytes NÃO estão publicados neste repositório**, apenas os hashes estão registrados aqui para auditoria; consequentemente, este checkpoint não constitui entrega da geometria estruturada no GitHub nem autorização de adoção. A fonte externa da geometria proposta permanece artefato não canônico entregue na própria conversa, sujeito à revisão expressa do proprietário.

## Dependências imutadas

- Costa MW-010 blob `d72cf3eb2b3fac9473017a6bbfdc46ea1efb8577` exclusiva.
- Relevo 7 feições e 3 cristas, água 9 cursos incluindo tributários, 5 bacias e 3 lagoas, trecho termal, 3 ilhas hipotéticas e 9 âncoras MW-014 preservados.
- Referência geográfica `NOVYDRES-LOCAL-2010`, em metros, sem lat/long e sem cadastro viário.

## Resultado geométrico candidato (não aceito)

- 22 feições de Ermo com tipos exclusivos: rochoso 6, gelado 5, pantanoso 5, tundra 6.
- Área anterior unificada 2.588,4831 km²; área candidata G 2.036,3671 km², 24,93% do continente de 8.167,7425 km².
- Por tipo: rochoso 816,44 km²; gelado 478,87 km²; pantanoso 197,36 km²; tundra 543,69 km².
- Checagem local: fronteiras poligonais válidas; sobreposição entre classes equivalente a zero na tolerância numérica; sobreposição com lagos e fora do continente equivalente a zero; nenhum dos 9 núcleos dentro de Ermo.
- SVG derivado da mesma geometria candidata estruturada; textura de construções e alleys é **puramente decorativa**, não ruas/edifícios aprovados.

## Identificação de arquivos de inspeção anexados no ChatGPT

- HTML `novydres-ermos-g-interativo.html` SHA-256 `d72f524ea0a8f86a8ea3f30a3f3e1b3c6204964fca8a5c95d38669cab9d32885`.
- SVG `novydres-ermos-g-artístico.svg` SHA-256 `2cb8f38313cc63354281da93678dd972a187adee9948413d7d8b533779620369`.
- JSON `novydres-mw014-ermos-g.proposal.json` SHA-256 `0d1e88697ba4ab85325039be11f2bd5563b8f01fce187de6668a3f537e1ecdee`.
- PNG `novydres-ermos-g-artístico.png` SHA-256 `36de5555a20270d03b6a0108679ae2df09f4971122d2224be46a601241b440aa`.
- Comparação PNG `novydres-ermos-g-comparacao.png` SHA-256 `bfd30782cff161ba4a663d6ea1d2f316526092d9a0a10506449c0f03cc2f8317`.

## Gate de aprovação

Solicitar decisão expressa apenas após inspeção do mapa. Nenhuma geometria G foi aprovada; não fechar MW-014, não canonizar, não avançar unidades e não gerar handoff. Se G for aprovada, é obrigatório persistir os polígonos estruturados integrais e o renderizador correspondente em branch, validar seus blobs/ref e examinar dependências com relevo/hidrografia antes de qualquer fechamento. Se rejeitada, manter a unidade aberta e registrar rejeição.
