---
document_id: MW-015-FIS01-RECONCILIACAO-VARIANTES-2010
subject_id: world-atlas-novydres
work_unit: MW-015
work_unit_status: CLOSED_FOR_THIS_SCOPE
canonical_status: NOT_APPROVED
geometry_replacement_authorized: false
source_master_sha: 5931f306c1e547d169d6e4bbb69114d616a6011c
mw010_coastal_geometry_blob: d72cf3eb2b3fac9473017a6bbfdc46ea1efb8577
mw014_source_checkpoint: aa0a5794edff80cc508a6439b1ce4dbef3ee6ca4
owner_decision: APROVADO
owner_decision_date: 2026-11-17
owner_decision_scope: MW010_SOLE_CURRENT_NONCANONICAL_WORKING_BASELINE
other_coastal_variants_current_status: NOT_MAINTAINED
---

# MW-015 — Fechamento da reconciliação costeira

**CLOSED_FOR_THIS_SCOPE.** A única base costeira candidata corrente do Mapwork permanece **MW-010**, com 44 vértices na costa continental e a baía correspondente. Nenhuma outra variante costeira é mantida como proposta alternativa ativa, concorrente ou candidata a propagação. Não houve troca de geometria, alteração de outros blocos, canonização ou aprovação de novas feições.

## Decisão expressa do proprietário

Em 17/11/2026 o proprietário decidiu: **“Manter MW-010 como base corrente não precisa preservar nenhuma variante”**.

Interpretação operacional aprovada:
- **APROVADO:** conservar exatamente MW-010 como a única costa de referência de trabalho não canônica, que já estrutura MW-011, MW-012, MW-013 e MW-014.
- **REJEITADO como opção ativa:** conservar MW-009 como segunda variante candidata, com status operacional especial, ou como alternativa a ser propagada. A aprovação anteriormente dada no âmbito isolado de MW-009 não constitui aprovação de adoção atual e não prevalece sobre esta seleção posterior.
- **Sem eliminação de histórico de auditoria:** o passado continua rastreável nos commits históricos do Git, como previsto no ADR-002. Não criar arquivos arquivados ou duplicar geometrias da MW-009 na árvore corrente. Retirar o comparador exploratório MW-015 do HEAD corrente; sua execução pretérita pode ser auditada por Git.
- **Não aprovado:** oficialização da costa, localização geodésica, contorno definitivo das ilhas, fronteiras de raions, uso da terra funcional E ou qualquer canonização.

Esta decisão resolve integralmente o único item substantivo de MW-015. Nenhum aceite visual novo é necessário, pois não existe nova geometria a avaliar: a própria costa MW-010 já havia sido aprovada para esta função e foi reafirmada expressamente. A comparação visual integral foi entregue no chat em arquivos baixáveis, sem exigir GitHub.

## Artefato efetivo

`macrogeometria-litoral-baia-ilhas-2010.proposal.json` continua com o blob `d72cf3eb2b3fac9473017a6bbfdc46ea1efb8577`, idêntico ao aprovado em MW-010 e usado por MW-014. A decisão é materializada por esta versão consolidada do relatório e pela retirada, da árvore ativa da branch MW-015, do comparador que mantinha a alternativa MW-009 visível como candidata.

Os três contornos de ilhas permanecem **hipóteses herdadas, sem aprovação de geometria**, não variantes costeiras concorrentes. Isto não revoga nenhuma restrição anterior nem cria aprovação.

## Reconciliação das dependências e validação da versão efetiva

Conferido novamente, após a decisão, diretamente na branch MW-015:
- Costa: blob `d72cf3eb2b3fac9473017a6bbfdc46ea1efb8577` = MW-010 = MW-014; 44 pares XY válidos; 3 ilhas candidatas sem mudança.
- Relevo: blob `cccc4eaac09b192a299108389bef3494f1f15bda`; 7 polígonos e 3 cristas, sem mudança ante MW-014.
- Hidrografia: blob `d0912bb8b420a8a29b0de602f4eb05f179da3b0c`; 9 cursos, 5 bacias e 3 corpos d'água, sem mudança.
- Ermos: blob `eac63da71d49fbe55d79da2ee82fbafae609decd`; 10 partes orgânicas, sem mudança.
- Âncoras urbanas: blob `0bb2f2fe0252750565b6558d1e6148bcdcc17a74`; 9 pontos XY válidos, sem mudança.
- Candidata de ocupação funcional E: blob `8a4479204d159bdf0fc7a9c563fb62444cb18b54`; 200 linhas raster de 500 m, sem mudança, **ainda pendente na MW-014**.
- Os IDs combinados de todas as feições inventariadas são únicos, todas as coordenadas dos anéis verificadas são finitas e cada anel tem ao menos 3 vértices distintos. Os 5 pontos terminais costeiros previamente inventariados têm distância calculada de 0 m à polilinha MW-010.
- **Formato já preexistente:** 25 de 28 anéis de feições auxiliares não repetem o primeiro ponto ao final, portanto requerem fechamento implícito no renderizador; isso não foi criado pela reconciliação e não foi indevidamente classificado como teste de fechamento explícito aprovado. Não foi executada certificação GIS/CI completa ou teste em navegador real. A MW-015 não altera esses dados.

**Efeito da escolha:** nenhuma migração, recorte, adaptação hidrográfica, remáscara costeira ou reaprovação de MW-011–014 é necessária por MW-015. A discrepância exploratória da MW-009 com 7 células classificadas da candidata E não se aplica, pois a MW-009 não foi adotada. Isto não é validação nem aprovação da própria candidata E.

## Fechamento e limites

- **Entregas:** relatório de reconciliação com decisão final; remoção do comparador de variantes da árvore corrente; manutenção idêntica de todas as seis fontes espaciais efetivas; aplicação da regra de visualização direta no chat no `guide.md`.
- **Estado:** `CLOSED_FOR_THIS_SCOPE` somente para decidir a base costeira única não canônica.
- **Pendências não bloqueantes deste ponto:** nenhuma. Revisões urbanas/funcionais da MW-014 permanecem abertas **na MW-014**, fora desta unidade. A costa não está canonizada.
- **Verificação remota do commit, parent, tree e blobs:** efetuada após a publicação, com os SHAs registrados no encerramento desta conversa.

Não usar memória de conversa nem este documento como substituto de bootstrap Git-native e do assunto proprietário.
