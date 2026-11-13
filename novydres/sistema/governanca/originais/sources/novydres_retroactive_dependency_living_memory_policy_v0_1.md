---
document_id: novydres_retroactive_dependency_living_memory_policy
version: 0.1
status: active
date: 2026-08-06
scope: retroactive_dependency_living_memory
applies_to:
  - novydres_editorial_map_*.json
  - approved_chapters
  - future_contracts
  - future_architecture_artifacts
  - future_content_artifacts
authority:
  - Senior Editor
purpose: >
  Garantir que dependências futuras com potencial de exigir retrabalho retroativo
  não sejam esquecidas após o fechamento editorial de capítulos já aprovados.
---

# Novydres — Política de Memória Viva para Dependências Retroativas

## 1. Propósito

Este documento estabelece a política permanente de **memória viva versionada** para dependências futuras capazes de exigir revalidação, patch, reabertura semântica ou reabertura estrutural de artefatos já aprovados.

O objetivo é permitir que capítulos permaneçam realmente fechados quando não existe defeito atual, sem perder o rastreamento de trabalho que poderá tornar-se obrigatório quando uma dependência futura for criada, aprovada, alterada ou consolidada.

A existência de uma dependência futura **não mantém automaticamente um capítulo aberto**.

A existência dessa dependência, porém, **deve permanecer registrada até que seja resolvida, invalidada ou consumida por uma revisão retroativa formal**.

---

## 2. Regra central

Toda decisão, contrato, capítulo, sistema, mecânica, estrutura editorial ou artefato futuro que possa materialmente afetar conteúdo já aprovado deve possuir um registro retroativo rastreável.

O registro deve responder, no mínimo:

- qual artefato futuro cria a dependência;
- quais artefatos anteriores podem ser afetados;
- qual é a natureza provável do impacto;
- qual evento transforma a dependência em revisão obrigatória;
- qual autoridade deve executar ou ordenar essa revisão;
- quando a dependência foi registrada;
- em qual versão ela foi alterada, satisfeita, invalidada ou encerrada.

Nenhuma dependência retroativa relevante deve existir apenas em memória de chat, comentário transitório, relatório isolado ou lembrança humana.

---

## 3. Fonte operacional da memória viva

O registro operacional primário deve ser o arquivo versionado:

`novydres_editorial_map_*.json`

O Editorial Map deve funcionar também como **índice de dependências retroativas**.

Ele não precisa duplicar toda a justificativa editorial. Deve registrar informação suficiente para garantir descoberta, rastreabilidade e disparo de revalidação futura.

Relatórios, contratos e decisões continuam sendo as fontes explicativas.

O Editorial Map funciona como o mecanismo que impede que a obrigação seja esquecida.

---

## 4. Princípio de retroatividade explícita

Sempre que um artefato futuro for criado e houver possibilidade material de ele afetar conteúdo anterior, o próprio registro desse artefato deve apontar retroativamente para os capítulos ou documentos potencialmente atingidos.

Exemplo conceitual:

`future_artifact_X`
→ pode afetar `05_concilio_leis_status_prestacoes`
→ motivo: redistribuição de autoridade mecânica
→ gatilho: aprovação da versão final de `future_artifact_X`
→ ação: revalidar Capítulo 05 contra a nova autoridade.

A dependência não deve depender de alguém lembrar que o Capítulo 05 precisava ser revisto.

---

## 5. Estados mínimos de uma dependência retroativa

Cada dependência deve possuir estado explícito.

Estados recomendados:

- `tracked` — registrada, mas o artefato futuro ainda não produz autoridade suficiente para revisão;
- `triggered` — o evento definido ocorreu e a revalidação retroativa tornou-se obrigatória;
- `under_review` — revisão retroativa em andamento;
- `satisfied` — revisão concluída e nenhuma mudança adicional é necessária;
- `patched` — revisão concluída por patch localizado;
- `reopened` — revisão exigiu reabertura semântica ou estrutural;
- `invalidated` — a dependência deixou de existir ou sua premissa foi rejeitada;
- `superseded` — substituída por dependência posterior mais específica.

Estados podem ser refinados pelo Senior Editor, mas o sistema nunca deve depender de ausência de valor para significar encerramento.

---

## 6. Campos mínimos recomendados no Editorial Map

Cada registro retroativo deve preservar, conceitualmente, os seguintes dados:

```json
{
  "dependency_id": "RETRO-XXX",
  "source_artifact": "artefato_futuro",
  "source_version": "x.y",
  "affected_artifacts": [
    "capitulo_ou_documento_anterior"
  ],
  "impact_types": [
    "continuity",
    "rules",
    "revelation",
    "editorial_structure",
    "usability",
    "information_ownership",
    "production"
  ],
  "reason": "descrição curta e objetiva",
  "trigger_event": "evento que torna a revisão obrigatória",
  "required_action": "revalidate",
  "status": "tracked",
  "created_in_version": "novydres_editorial_map_vX",
  "last_reviewed_in_version": "novydres_editorial_map_vX",
  "resolution_reference": null
}
```

Os nomes exatos dos campos não são congelados por este documento.

O contrato do Editorial Map pode adotar outra estrutura, desde que preserve semanticamente as mesmas garantias.

---

## 7. Eventos que devem criar uma dependência retroativa

Registrar dependência quando um trabalho futuro puder:

- contradizer lore já aprovado;
- alterar autoridade de regra existente;
- mudar o lar autoritativo de uma família de informação;
- alterar política de revelação;
- criar promessa editorial que exija atualização retroativa;
- redistribuir famílias inteiras de conteúdo;
- dividir ou fundir capítulos;
- tornar obsoleta uma explicação anterior;
- demonstrar ganho material de usabilidade que possa justificar reabertura;
- exigir reflow estrutural com consequência editorial;
- introduzir uma nova arquitetura cuja adoção dependa de conteúdo já fechado;
- substituir uma decisão anteriormente tratada como provisória;
- resolver uma questão conscientemente deferida por capítulo anterior.

---

## 8. O que não deve criar dependência retroativa obrigatória

Não registrar como obrigação de revalidação apenas porque existe:

- preferência estilística;
- ideia especulativa sem plano de adoção;
- possibilidade abstrata de melhoria;
- desejo de perfeccionismo;
- comentário editorial sem consequência identificável;
- mudança puramente cosmética;
- trabalho downstream que consome conteúdo anterior sem alterá-lo;
- nova aventura que apenas usa interfaces já aprovadas;
- paginação futura quando o conteúdo permanece semanticamente independente dela.

Esses itens podem ser registrados em backlog apropriado, mas não devem poluir a memória retroativa obrigatória.

---

## 9. Gatilho de revisão

Uma dependência `tracked` não reabre nada por si mesma.

Ela se torna `triggered` quando o evento registrado ocorre.

Exemplos:

- contrato futuro recebe aprovação;
- nova mecânica torna-se autoritativa;
- nova arquitetura editorial é adotada;
- capítulo posterior muda explicitamente uma relação institucional anterior;
- uma melhoria de usabilidade é aprovada como objetivo editorial material;
- uma decisão deferida recebe resolução final.

Ao ocorrer o gatilho, o Senior Editor deve avaliar cada `affected_artifact`.

Nenhum gap, capítulo ou contrato dependente deve ser considerado completamente encerrado enquanto houver dependência `triggered` sem disposição formal.

---

## 10. Resultado da revisão retroativa

A revisão de um artefato anterior deve terminar em uma disposição explícita.

Possíveis resultados:

- permanecer fechado;
- patch localizado;
- reabertura semântica restrita;
- reabertura estrutural;
- deferimento por nova dependência;
- nenhuma ação necessária.

O resultado deve voltar ao registro de memória viva.

A cadeia completa precisa permanecer rastreável:

dependência criada
→ evento disparador
→ revisão executada
→ decisão
→ artefato resultante
→ dependência encerrada ou substituída.

---

## 11. Relação com a política de reabertura

A memória viva não altera o critério de reabertura.

Ela garante que o critério seja reaplicado quando necessário.

Política vigente:

1. dependência futura não mantém capítulo automaticamente aberto;
2. uma dependência aprovada pode exigir revisão retroativa quando altera autoridade, conteúdo, arquitetura ou produz ganho material suficiente;
3. melhoria material de usabilidade pode justificar reabertura mesmo sem defeito objetivo;
4. esse ganho deve ser demonstrável em pelo menos um dos seguintes eixos:
   - compreensão;
   - consulta ou uso em mesa;
   - hierarquia editorial;
   - redução de ambiguidade;
   - redução de duplicação;
   - integração com a arquitetura atual do livro;
5. o ganho deve superar o custo de estabilidade e retrabalho;
6. a distinção entre patch e reabertura estrutural é causal, não quantitativa;
7. patch é adequado quando a alteração permanece local e não muda responsabilidades, sequência conceitual ou agrupamentos principais;
8. reabertura estrutural é adequada quando a melhoria exige redistribuir famílias de informação, dividir ou fundir seções, ou mudar como o capítulo é usado.

---

## 12. Responsabilidade do Senior Editor

Antes de encerrar qualquer artefato futuro, o Senior Editor deve verificar:

- ele possui dependências retroativas?
- essas dependências estão registradas no Editorial Map?
- os artefatos afetados estão identificados?
- o gatilho está definido?
- alguma dependência já foi disparada?
- existe revisão retroativa pendente?
- o resultado de revisões anteriores foi devolvido ao mapa?
- algum registro ficou órfão após supersessionamento?

Uma aprovação que cria impacto retroativo conhecido sem registrar esse impacto deve ser considerada editorialmente incompleta.

---

## 13. Regra para sub-agentes

Sub-agentes não devem editar o Editorial Map se seu escopo não conceder essa autoridade.

Quando identificarem uma nova dependência retroativa, devem:

1. registrar a descoberta em seu artefato;
2. identificar origem, alvo, motivo e gatilho;
3. recomendar criação ou atualização do registro no Editorial Map;
4. não declarar a dependência operacionalmente registrada até que o Senior Editor ou agente autorizado atualize o mapa.

Assim, a ausência de autoridade de escrita não se transforma em perda de memória.

---

## 14. Versionamento

Toda alteração de dependência retroativa deve ser preservada através das versões do Editorial Map.

Não apagar silenciosamente registros antigos.

Quando uma dependência for encerrada, preferir:

- mudar seu estado;
- registrar resolução;
- registrar versão de encerramento;
- apontar para patch, revisão, decisão ou artefato resultante.

Quando for substituída, registrar `superseded` e apontar para a nova dependência.

A história da obrigação é parte da memória editorial do projeto.

---

## 15. Regra de segurança contra esquecimento

Nenhum trabalho conhecido como potencialmente retroativo pode depender exclusivamente da frase:

> “lembrar de revisar isso depois”.

Se há retrabalho futuro identificável, deve existir registro versionado.

Se existe registro versionado e seu gatilho ocorreu, deve existir disposição formal.

Se existe disposição formal, ela deve voltar ao registro.

Esse ciclo constitui a memória viva.

---

## 16. Aplicação imediata aos Capítulos 01–06

A auditoria de reabertura dos Capítulos 01–06 deve:

- identificar dependências futuras já conhecidas;
- separar dependência real de melhoria especulativa;
- registrar quais deveriam entrar no próximo refresh autorizado do `novydres_editorial_map`;
- não modificar o mapa diretamente;
- exigir que o Senior Editor audite e incorpore os vínculos retroativos aprovados.

Especial atenção deve ser dada a dependências futuras envolvendo:

- `Jogando em Novydres`;
- arquitetura standalone;
- criação de personagens;
- regras locais e catálogos mecânicos;
- reorganização estrutural de capítulos;
- Fé / Ordem Urukiana;
- Status e ferramentas jurídicas de mesa;
- arquitetura de aventuras;
- sistema visual e reflow;
- quaisquer contratos posteriores que redistribuam autoridade atualmente localizada nos Capítulos 01–06.

---

## 17. Critério de sucesso

Esta política funciona quando é possível responder, sem recorrer à memória humana:

> “Se aprovamos este novo artefato hoje, quais documentos antigos precisamos obrigatoriamente revalidar?”

A resposta deve ser recuperável do sistema documental versionado.

Se não for, a memória viva falhou.