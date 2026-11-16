# NOVYDRES — contexto operacional por assuntos (ADR-001)

A tree `4e08b9e4559922f711669294718fbdc74780d9d8` foi promovida por E02 em `74777a6328439eb02825cc09172fcb9244a1522f` com parent `c9fcfc0c558cd17d58ec8c8272da3ed70182ff37`. **Esse SHA é histórico da promoção, não um pin permanente:** reconsultar a master e usar sempre um único snapshot. E03 fica em `sistema/arquitetura/fase-e/execucao-e03.json`; até E03_PASS, sem runtime de jogo. Mesmo após PASS, só retomar cenas por solicitação própria do jogador.

## Descoberta e autoridade
`AGENTS.md` → `CONTEXT.md` → `catalogo.json` no mesmo commit são as três entradas únicas. O catálogo contém 153 assuntos derivados de `assunto.json`, `index.md` e blobs; não é outra verdade. O campo histórico `CANDIDATE` dos manifests migrados conserva a proveniência de D e não libera outra rota. A autoridade efetiva é master+gate E03. Nenhum alias, fallback, redirect, bootstrap histórico ou leitura fuzzy.

`cenario/` mantém contexto global, `personagens/` identidades, `cronicas/` campanhas/estado/conhecimento e `sistema/regras/` regras. Sucessor de G19/G23/G24, DEC-CR-014, G26/G28 e DEC-18: `sistema/arquitetura/fase-e/sucessao-operacional.md` e `sistema/narrativa/contrato.md`. Scripts TEST_ONLY e candidatos continuam provas de CI, não segunda rota de runtime. O fluxo efetivo no ChatGPT Web é via conector GitHub e CAS.

## C45: recuperação sem narrativa
`chr001-state-checkpoint` aponta para `cronicas/CHR-001/estado/recuperacao-c45.json`: M3.02, C01 fechado, C02 `NOT_STARTED`, próximo papel NARRADOR, protagonista mortal, sem Abraço. Origem histórica `c9fcfc0c558cd17d58ec8c8272da3ed70182ff37`. C41 `atual.json` é fixture, não cursor.

Recursos conferidos: XP total 675, gastos 270, remanescentes 405, crédito 0; FV máximo provisório 6, 2 superficiais, 0 agravados, 4 disponíveis. **Não conceder nem gastar recursos automaticamente.** Há 38 assuntos de conhecimento por ator, 47 registros e 44 tramas. `chr001-runtime-story-architecture` é restrito a preparação SYSTEM_AUDIT; não publicar ao jogador.

D04/D05 PASS com risco aceito; D06 PASS técnico; D07 PASS contextual de agente identificável. Nove grupos de sucessores examinados, **119 comportamentos não certificados**. `CONFLICT-001/002/003B` pendentes; cinco mídias opcionais dispensadas, ACL externa e V5 integral não certificados. Sem alteração de cânone, sem ledger universal, sem fallback.

Transação em resposta de jogo autorizada: mesmo snapshot, owner, prosa+estado no commit, `tx_id`, CAS e readback antes da entrega; em erro, suspender e reconciliar, sem rerrolagem ou duplicação.

## Convenção linguística do suplemento
Em novos textos, revisões e interações, termos fora de português/inglês exigem idioma, significado ou etimologia verificada e pronúncia aproximada em português brasileiro. A fonte única é `cenario/atlas-novydres/convencao-editorial-idiomas-e-pronuncia.json` (sujeito `world-atlas-novydres`). **Cidade Velha** é nome cotidiano predominante do núcleo; **Iknik** (ÍK-nik; raiz *ikniq*, fogo) é seu nome formal raro. **Kingswal** (KÍNGZ-uól) é o nome oficial do raion de ID `district-chelsea`, dedicado por Gilgamesh em 1423 ao progenitor dos Ventrue. A interpretação ritual “Fonte do Rei” não é tradução literal de Kingswal. Siku foi rejeitado; Chelsea permanece rótulo legado. A origem das comunidades indígenas não é negada pelo nome da administração cainita. Não alterar IDs técnicos ou a cronologia pré-1423 por essa convenção.
