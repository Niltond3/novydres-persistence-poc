# Protocolo reproduzível — três sessões independentes ChatGPT Web

Classificação: PLAYER_SAFE. Estado atual: protocolo, não execução. Não há evidência nova de sessão Web neste commit.

## Objetivo e fronteiras

Rodar três conversas novas e independentes, cada uma com 30 consultas factuais. Em cada conversa registrar também os 12 negativos e 12 jornadas. O fixture negativo/jornada atualmente não contém payload executável suficiente; nesses 24 IDs, a resposta honesta esperada do protocolo é `NOT_TESTABLE_NO_EXECUTABLE_PAYLOAD` até que o fixture operacional exista. Não converter essa limitação em PASS.

Não escrever no Git, não ativar rotas, não alterar dados operacionais, não reconciliar conflitos e não iniciar C. A conversa de avaliação é privada. Respostas factuais e conteúdo restrito podem aparecer somente na sessão privada para permitir scoring; nunca os copiar para artefato PLAYER_SAFE, handoff, issue ou resumo ao jogador. Persistir somente resultados redigidos e evidência de path/SHA/locator.

## Preparação

1. Abra três chats novos e separados no ChatGPT Web: R1, R2 e R3. Não reutilize contexto nem resultado de outra rodada.
2. Fixe os candidatos em `35862b10000883ac8e607f9de1a87d945b21c1a5` e as fontes no snapshot original `c26c0fbf15fff6c817182c06e6208e302b954f3a`. Leia os anexos sanitizados `fixtures-remediacao-consultas-sem-gabarito.json` e `fixtures-remediacao-negativos-mutuacoes.json` da branch final da remediação. Um facilitador deve confirmar antes da rodada que o blob SHA dos anexos corresponde ao readback de GitHub.
3. O avaliador mantém o fixture original `fixtures-consultas.json` e seu gabarito fora da conversa Web. Não os anexar ao modelo. Fazer scoring independente das respostas privadas depois da sessão e guardar somente ID + PASS/FAIL + citações, sem valores.
4. Para cada leitura, confirmar path e blob SHA; usar locator preciso (linha ou JSON Pointer). Se o conector não expuser SHA ou locator, marcar `NOT_OBSERVABLE` e não contar como evidência completa.
5. Cronometrar cada sessão do primeiro caso ao último por relógio da UI. Registrar chamadas, caracteres e latências somente quando a UI realmente os mostrar. Não chamar caracteres de bytes. Não estimar tokens.

## Prompt integral

Copie o bloco abaixo para cada chat novo, trocando `R1` por `R2` e `R3`. Anexe os dois fixtures sanitizados. A tabela de pins faz parte do prompt e fixa 16 arquivos candidatos e seis fontes do snapshot original c26. Cinco fontes também aparecem na árvore de design; `CYCLE_V0041.json` não foi copiado para lá e deve ser lido em c26.

```text
Você é avaliador técnico isolado da Fase B do NOVYDRES. Execute somente o protocolo desta sessão; não promova candidatos, não escreva no repositório e não inicie Fase C.

**Sessão:** substitua `R1`, `R2` ou `R3`. Esta deve ser uma conversa ChatGPT Web nova, sem histórico das outras sessões.
**Commit fixado para candidatos:** `35862b10000883ac8e607f9de1a87d945b21c1a5`. **Snapshot original fixado para fontes:** `c26c0fbf15fff6c817182c06e6208e302b954f3a`.
**Oráculo:** não carregue nem revele campos esperados do fixture original. O avaliador independente os consulta fora desta conversa.

1. Leia os dois fixtures PLAYER_SAFE anexados: `fixtures-remediacao-consultas-sem-gabarito.json` e `fixtures-remediacao-negativos-mutuacoes.json`. Confirme que a contagem é 30 perguntas, 12 negativos e 12 jornadas. Não complete payload ausente por inferência.
2. Para toda pergunta, consulte os candidatos e fontes fixados abaixo, usando o commit de design para arquivos candidatos e o snapshot c26 para fontes (nunca use branch default). Leia cada arquivo citado pela pergunta. Registre path, blob SHA, locator lido e resultado. Se uma fonte não puder ser aberta ou SHA não conferir, marque o caso `BLOCKED`; não use fonte substituta.
3. Faça as 30 consultas em ordem de ID. Responda com o valor factual apenas dentro desta sessão privada de avaliação. Não copie respostas, conteúdo de fonte, conhecimento restrito ou spoilers para relatórios PLAYER_SAFE, handoff ou outra conversa. Forneça citações por caso com path, blob SHA e locator; um revisor independente pontuará as respostas contra o oráculo local.
4. Para B-N01..B-N12, e B-M01..B-M12, use exclusivamente o payload e os critérios já presentes no fixture integral aprovado. Os anexos são sanitizados e não incluem esses payloads. Se o payload ou critério não estiver no material disponível, registre `NOT_TESTABLE_NO_EXECUTABLE_PAYLOAD` por ID. Não invente estímulos, não execute mutações Git e não reporte PASS por raciocínio hipotético.
5. Registre início/fim por relógio da interface, chamadas de navegação que a UI mostrar e caracteres transferidos que forem observáveis. Não estime tokens, bytes HTTP nem latência de serviço. Use `NOT_OBSERVABLE` quando a interface não expuser o valor.
6. Ao finalizar, gere um JSON privado para o avaliador independente com um item para cada ID, resultado, path/SHA/locator, falha e status de sigilo/autoridade. O JSON pode conter respostas somente na sessão privada; o relatório a persistir deve ser redigido para conter apenas PASS/FAIL/BLOCKED e referências, sem valores factuais. Não declare sucesso agregado baseado em autoavaliação sem readback independente.

### Pinos imutáveis
| Tipo | Caminho | Blob SHA |
|---|---|---|
| candidate | `novydres/cronicas/CHR-001/elenco/npc-samir-haddad/assunto.json` | `75a02f737d2f1dffcfb1a5d5e93664e9a4d0ecd0` |
| candidate | `novydres/cronicas/CHR-001/elenco/npc-samir-haddad/conhecimento.json` | `64af21e9ca4c0ea625af3f7f7b3a93b7a241073e` |
| candidate | `novydres/cronicas/CHR-001/elenco/npc-samir-haddad/index.md` | `12937813cc96754faf933bcdb79371301d50140e` |
| candidate | `novydres/cronicas/CHR-001/elenco/npc-samir-haddad/relacoes.json` | `47663d84c869aa52a15967a163bad2a4ef1c4f95` |
| candidate | `novydres/cronicas/CHR-001/estado/assunto.json` | `3e9216eafb2efb89d335224f51ff4134dcdc4e54` |
| candidate | `novydres/cronicas/CHR-001/estado/atual.json` | `88317332db5691d764e4543c5648e537655e8e4b` |
| candidate | `novydres/cronicas/CHR-001/estado/index.md` | `37a764d8ce6219f8c5bdc9732c18566b349f5ee1` |
| candidate | `novydres/cronicas/CHR-001/historias/m301-c01/assunto.json` | `45ae004d040c37c78bd8a9af65b0618d7c77dc60` |
| candidate | `novydres/cronicas/CHR-001/historias/m301-c01/historia.json` | `c307277c91adf0c986e82d5d8f0714a1e4896ba7` |
| candidate | `novydres/cronicas/CHR-001/historias/m301-c01/index.md` | `98d3782aee4ad7fff06c771a889074dbac8f1e8e` |
| candidate | `novydres/cronicas/CHR-001/tramas/contato-condicional-samir/assunto.json` | `a9cd81341cd621217f4f51fb7b4e5dff22b94d74` |
| candidate | `novydres/cronicas/CHR-001/tramas/contato-condicional-samir/index.md` | `34bd43743336183a5423980cda0e1ce58638bddd` |
| candidate | `novydres/cronicas/CHR-001/tramas/contato-condicional-samir/trama.json` | `1aa7682911a572d0e391e90d19f3af46ed34ba0d` |
| candidate | `novydres/personagens/npc-samir-haddad/assunto.json` | `f8775e19413f4dd72f091a9a153ccaeaddff747d` |
| candidate | `novydres/personagens/npc-samir-haddad/index.md` | `8d6ffab9e42ccbbf84dd8fd7581793998de2077e` |
| candidate | `novydres/personagens/npc-samir-haddad/perfil.json` | `17a353ccbda595b99fbf909b7ecd9d91b0e723d9` |
| source | `novydres/chronicles/CHR-001/HISTORY_INDEX_v038.json` | `9df68f771f430f8755b3d321a98a0b6c85288f36` |
| source | `novydres/chronicles/CHR-001/knowledge/NPC_KNOWLEDGE_PROVENANCE_V21.json` | `679298fec1da012572f25cfd9b9ae0a37df8586a` |
| source | `novydres/chronicles/CHR-001/knowledge/OPEN_THREADS_V23.json` | `c33f7e48b9c4b5ef98e2b6ac998b8375502308f5` |
| source | `novydres/chronicles/CHR-001/episodes/M3.01_v001.source.txt` | `43b461493b5470057ab54648c6f6d9055814e271` |
| source | `novydres/chronicles/CHR-001/LIVE_v038.json` | `9d2090a54fe60aeed3dc317aac8e6fd31433fd45` |
| source | `novydres/chronicles/CHR-001/orchestration/CYCLE_V0041.json` | `06398ed7cbc19e315fb7d59b08cc807b3e36c88d` |

### Formato mínimo de saída desta sessão
- contagem por ID e resultado, sem saída agregada desacompanhada dos itens;
- evidência path/SHA/locator para cada resposta escorada;
- casos sem fonte ou payload explicitamente BLOCKED/NOT_TESTABLE;
- violações de autoridade/sigilo relatadas somente como contagem e IDs, sem reproduzir o conteúdo;
- tokens e bytes HTTP como `NOT_OBSERVABLE` se ausentes;
- p50/p95 somente se houver três amostras comparáveis desta mesma operação, com método declarado.

Não use os resultados das sessões anteriores. Não publique ou copie o JSON privado para o repositório.
```

## Scoring e registro

Para cada rodada, manter privadamente a resposta original até a avaliação independente. Depois, produzir uma linha por ID com: rodada, ID, PASS/FAIL/BLOCKED/NOT_TESTABLE, path, blob SHA, locator, autoridade, sigilo e observação de falha. Não incluir campo de resposta factual. O avaliador compara o conteúdo privado com o gabarito local sem copiá-lo para os artefatos da branch.

Os casos B-N01..B-N12 e B-M01..B-M12 permanecem `NOT_TESTABLE_NO_EXECUTABLE_PAYLOAD` na ausência de operação, precondições, payload e readback especificados. Uma resposta verbal do modelo não testa escrita, CAS, concorrência, idempotência ou proteção de master.

## Critério de evidência

Uma sessão Web só pode ser chamada de execução real quando houver identificação da conversa, começo/fim observáveis, resposta por ID e readback independente de path/SHA/locator. Resultado agregado autodeclarado é `INSUFFICIENT_EVIDENCE`. Tokens reais e bytes HTTP devem permanecer `NOT_OBSERVABLE` quando a UI não os expuser. Três sessões não convertem automaticamente os gates Codex/CI/Git em PASS.

