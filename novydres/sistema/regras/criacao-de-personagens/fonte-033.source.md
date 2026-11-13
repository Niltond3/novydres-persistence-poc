# NOVYDRES Chronicle Core — Web First V0.2

**Status:** código local testado + persistência real no Google Drive verificada por chamadas de ferramentas deste chat. **Não é um servidor, plugin instalado nem integração que roda automaticamente sem chamadas de ferramentas.**

## Regra de arquitetura

- **ChatGPT web:** única interface de jogo; o usuário não precisa usar terminal.
- **Python temporário do ChatGPT:** valida comandos, executa números reais por `secrets.SystemRandom()` e produz a versão seguinte do registro.
- **Google Drive:** fonte autoritativa persistente em um *Google Doc com JSON único*, escrito mediante controle de revisão (`requiredRevisionId`) e leitura de confirmação.
- **Contrato de narrativa:** `.AGENT.md` e `EVENT_PROTOCOL_V1` da pasta `00_GOVERNANCA_DA_CRONICA` são obrigatórios. O ZIP V0.2 não altera o cânone do cenário nem substitui `.AGENT/.CONTEXTG` do workspace original.

Documento de estado autoritativo, ainda **vazio**:
https://docs.google.com/document/d/1-WSmz-xTI8St-Q2_Ruw9BvAVDQb4k9s0Ifs1GlYtT98/edit

Sandbox, **eventos simulados SEM valor ficcional na crônica**:
https://docs.google.com/document/d/1JCjEcLvp3egi9IVlpv5GNFbXq0zZIhpkOGRdVNrbmk4/edit

## Passo a passo para o Narrador em TODA interação com efeito persistente

1. Ler `get_document_text` do estado; guardar **texto completo e revisionId** retornados pelo Drive. Não usar a lembrança do chat como estado.
2. Executar `parse_store(body)`, `validate_store(store)` no Python da sessão. Se o JSON não for válido, **parar e relatar**, não reconstruir por imaginação.
3. Vincular literalmente a declaração do usuário, quando houver, ao comando estruturado (`declaration`, `declaration_ref`); classificação `ATTEMPT/ACTION/SPEECH/CHOICE`; registrar fontes reais de regras. A IA faz classificação contextual e **não há prova criptográfica de autoria no Web**.
4. Executar `append_event(store, cmd)` ou, em teste, `apply_pool_roll`/`apply_rouse` **somente depois de preparar e persistir especificação e evento causal**. As operações são determinísticas exceto os dados, que vêm de `secrets.SystemRandom()`.
5. Executar `plan_drive_replace(old_text, new_store)`. O plano rejeita remoção ou mutação de registros anteriores e produz `replaceAllText`.
6. Chamar `batch_update_document` com `requests:[{replaceAllText:plan}]` **e** `write_control:{requiredRevisionId:revisionId_lido}`. Exigir `replies[0].replaceAllText.occurrencesChanged == 1`. Se for 0, duplo ou a ferramenta falhar: **PENDING_PERSISTENCE**; ler novamente e reconciliar, sem repetir rolagem.
7. Reabrir `get_document_text` do Drive, executar `parse_store` + `validate_store`, conferir campos `last_seq`, `last_roll_seq` e hashes esperados. Somente então dizer **CONFIRMADO** e narrar a consequência persistente.
8. Para recomeçar outra conversa, repetir desde o passo 1. O ChatGPT não executa o código por iniciativa própria quando não está sendo chamado.

### Rolagem: duas fases de commit obrigatórias

1. Após evento causal do jogador/NPC `EVT-n`, **pré-registrar** evento `SYSTEM` com `rule_ref: V5_BASIC_POOL`, `causal_refs:[EVT-n]` e `source:{"roll_spec":{"pool":N,"hunger":H,"difficulty":D,"rule_ref":"V5_BASIC_POOL"}}`.
2. **Salvar e confirmar** esse evento de preparação no Drive antes de lançar dados. O `event_id` preparado será a referência da rolagem.
3. Executar `apply_pool_roll(store, spec, source_event_id=event_id_preparacao)` sem fornecer gerador de teste, permitindo que `secrets.SystemRandom` produza os d10.
4. Persistir a versão com os dados brutos e o hash encadeado no **mesmo Doc autoritativo** com CAS; confirmar leitura. Rolagem gerada mas não salva não pode ser repetida silenciosamente: reconstruir o resultado original se ainda disponível; caso perdido, informar incidente e obter decisão do jogador sobre recuperação, sem simular que foi a mesma rolagem.
5. Se houver consequências, criar novo evento de `WORLD_EVENT`/`MECHANICAL_RESULT` causal ao evento preparado; aplicar `deltas` usando `before/after` com causa e regra. Não confundir um teste bem-sucedido com a realização automática de uma próxima ação do PC.

`apply_rouse` exige preparação análoga com `rule_ref: V5_BASIC_ROUSE` e `source:{"roll_spec":{"rule_ref":"V5_BASIC_ROUSE"}}`. Este motor não altera automaticamente Fome — o efeito deve ter regra, causalidade e delta verificados.

## Autoria sem terminal do jogador

A V0.1 usava Ed25519 com chave privada do jogador. Isso não se encaixa em um jogo **somente web** sem interface adicional de assinatura. Na V0.2, o texto do usuário no próprio chat serve de evidência operacional, copiado literalmente com referência à mensagem quando possível. **É uma verificação procedimental, não uma prova criptográfica independente:** o modelo que interpreta a mensagem também pode errar. Para ações irreversíveis ou ambíguas, solicitar confirmação e gravar sua mensagem literal.

## API Python e testes

```bash
python3 -m unittest discover -s tests -v
python3 bridge_cli.py init
python3 bridge_cli.py validate --store empty_store_v0_2.json
```

O `bridge_cli.py` é uma interface de desenvolvimento/diagnóstico para o executor temporário do ChatGPT, **não um requisito para o usuário jogar**.

```python
from webfirst_core import parse_store, validate_store, append_event, plan_drive_replace
store = parse_store(texto_lido_do_drive)
# ... comando estritamente grounded à fala do jogador ...
novo = append_event(store, comando)
requisicao_google_docs = {"replaceAllText": plan_drive_replace(texto_lido_do_drive, novo)}
# Chamar conector Google Docs com write_control.requiredRevisionId.
# Ler de volta e validar ANTES de confirmar.
```

## Resultado dos testes

24 testes unitários passam. T01–T12 do contrato V1 cobertos por regressões, assim como: hash de eventos e rolagens, alteração de histórico, planejamento de rolagem anterior ao sorteio, duplicação de sorteio, persistência de alterações condicionais e carregamento de estado. Foi comprovado um ciclo REAL de CAS (escrita + leitura) no Drive em arquivo sandbox, além de rejeição HTTP de tentativa com `requiredRevisionId` antigo.

## Limites deliberados / Não resolvidos

- **Sem serviço externo rodando:** orquestração via ferramentas deve ser feita explicitamente pelo ChatGPT a cada mudança.
- **Sem transação atômica entre diferentes arquivos do Drive:** por isso o `CHRONICLE_STORE_V0_2` é a única fonte de verdade para eventos, ficha por deltas e rolagens nesta etapa. Outros Docs/Sheets futuros serão visões derivadas, não serão autoridades concorrentes.
- **Google Docs não é um log append-only inviolável:** há histórico do provedor e checagem por hashes, mas o proprietário pode alterar bytes e reescrever hashes. A V0.2 mantém prefixo nas operações controladas pelo programa.
- **Escala de longo prazo:** o registro em documento único precisará de sharding/arquivo de eventos e índice com migração explícita quando ficar grande; esta versão não implementa essa rotação.
- **Segredos:** o titular do Drive pode ler arquivos `GM_HIDDEN`; separar documentos não equivale a isolamento de acesso.
- **V5:** implementadas rolagens básicas de dados, dados de Fome e testes básicos de Despertar. Disciplinas, Resistência, conflito prolongado, Humanidade e homebrew Novydres exigem fontes oficiais e implementação específica.
- **Autorização, semântica e cronologia:** classificação narrativa e regras causais complexas não são verificadas completamente por código. O modelo nunca deve vender a V0.2 como garantia total contra alucinação.
- **Personagem:** ainda não existe ficha, cronologia de campanha ou eventos. O registro principal permanece vazio até definição do personagem e validação do cânone do cenário.

## Ponto de retomada

Leia, nessa ordem, `.CONTEXTG.md` V1.1, `.AGENT.md` V1, `EVENT_PROTOCOL_V1`, o arquivo `CHRONICLE_STORE_V0_2`, e os arquivos canônicos originais relevantes de Novydres. Execute a suíte e valide o estado antes de criar a primeira ficha. O sandbox NÃO deve ser importado para o estado real.
