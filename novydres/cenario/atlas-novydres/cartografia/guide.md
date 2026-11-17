# Novydres Mapwork — guia operacional de continuidade

Este arquivo contém **modelos de passagem de trabalho**, não geografia nem cânone. A fonte da verdade é o GitHub atual, sobretudo `novydres/AGENTS.md`, `novydres/CONTEXT.md`, `novydres/catalogo.json`, ADR-001, ADR-002, PRD-ATLAS-001 e os arquivos proprietários dos assuntos.

**Nunca reconstruir fatos a partir da memória de chat ou de um handoff.** Textos de handoff são localizadores e instruções, não evidência. Reconfirmar os fatos e o checkpoint no repositório.

## Regra de fechamento integral do ponto e liberação de handoff (aprovação do proprietário em 16/11/2026)

**É proibido criar handoff para o próximo ponto/unidade enquanto o ponto atual não estiver efetivamente fechado.** A aprovação de uma orientação parcial, a conclusão de uma subdecisão, a publicação de um checkpoint ou a proximidade do limite do contexto **não** equivalem ao fechamento.

O handoff `MW-XXX → MW-YYY` e o prompt de inicialização da próxima unidade **somente podem ser produzidos depois que todos os critérios abaixo forem cumpridos e documentados no GitHub**:

1. **Inventário de decisões do ponto:** enumerar tudo que depende da validação substantiva do proprietário, sem perguntas artificiais ou aprovações de detalhes meramente técnicos.
2. **Deliberação integral:** para **cada** questão do ponto, registrar a resposta expressa do proprietário — `APROVADO`, `REJEITADO` ou `APROVADO_COM_RESSALVAS` (ou `ADIADO` apenas se o ponto puder ser encerrado honestamente mantendo essa pendência fora do seu critério de aceite). Nenhuma aprovação implícita.
3. **Implementação concluída:** gerar e publicar **a nova versão do artefato pertinente** que materializa as decisões, suas ressalvas e rejeições; quando uma alternativa for rejeitada, a versão consolidada não poderá apresentá-la como aprovada. Para cartografia, atualizar a geometria estruturada candidata e o visualizador derivado conforme aplicável, preservando a fonte única.
4. **Validação da versão efetiva:** realizar as verificações técnicas e visuais apropriadas na **nova** versão, reconciliar dependências e corrigir problemas materiais. Testes anteriores à revisão não certificam a revisão. Limitações remanescentes devem estar explicitadas; nenhuma falha bloqueante pode ser disfarçada de PASS.
5. **Revisão final pelo proprietário:** quando o ponto exige aceite visual ou substantivo da versão consolidada, submetê-la à avaliação; obter aceite ou rejeição inequívoca **dessa versão**, inclusive das ressalvas. Uma ordem de “refinar antes de aprovar” mantém o ponto **aberto** até haver a versão refinada e sua revisão.
6. **Fechamento e readback remoto:** registrar o estado final do ponto (`CLOSED_FOR_THIS_SCOPE` com decisão/ressalvas delimitadas, ou `CLOSED_REJECTED` após rejeição explicitamente encerrada), entregas, validações, pendências não bloqueantes e commit; confirmar ref, parent, tree e blobs remotamente. **Fechamento do ponto não é canonização:** `CLOSED_CANON` depende separadamente do contrato de propagação e autorização correspondente.

**Se qualquer requisito faltar:** continuar trabalhando **na mesma unidade**, com status `OPEN` ou equivalente; não afirmar unidade concluída, não propor próxima unidade como executável e **não emitir handoff nem prompt para o próximo ponto**. Informar apenas decisões obtidas e pendências de fechamento.

**Exceção técnica para troca de conversa por limite de contexto:** pode-se registrar no GitHub um checkpoint verificável e uma **nota curta de retomada da mesma unidade MW-XXX**, sem declarar fechamento, sem inventar uma nova unidade e sem chamá-la de handoff para próximo passo. A nota indica apenas como reabrir o trabalho atual nas fontes GitHub. Não usar histórico/memória como autoridade.

Esta regra governa os modelos abaixo; **os modelos de handoff e prompt seguinte só ficam habilitados após cumprir o gate de fechamento**.

## Modelo de encerramento de unidade

```text
NOVYDRES MAPWORK — HANDOFF MW-XXX → MW-YYY
Repositório: Niltond3/novydres-persistence-poc
Branch de trabalho: <branch>
HEAD remoto verificado: <SHA>
Unidade concluída: <objetivo + critério de aceite>
Entregas persistidas: <caminhos de arquivos e commits>
Validação: <evidências verificadas / não verificadas>
Pendências materiais: <somente impedimentos para o próximo passo>
Próxima unidade: <um objetivo, um entregável e um critério de aceite>
Referência operacional: novydres/cenario/atlas-novydres/cartografia/guide.md
```

**Utilizar este modelo somente depois do gate de fechamento integral acima.** Não copiar narrativas extensas, fatos canônicos ou histórico de discussão. Apontar para arquivos e IDs exatos. Se não houve escrita, declarar explicitamente.

## Modelo de prompt do próximo chat (somente após fechamento)

```text
NOVYDRES MAPWORK — MW-YYY

Objetivo único: <objetivo>
Entregável/aceite: <entregável verificável e critério>
Repositório: Niltond3/novydres-persistence-poc

Abra o HEAD atual de master; leia AGENTS.md, CONTEXT.md e catalogo.json no mesmo SHA; siga o ADR-002, o PRD-ATLAS-001 e cartografia/guide.md. Resolva no GitHub os assuntos, fontes e dependências desta unidade. O handoff anterior serve apenas para localizar arquivos e checkpoints; valide tudo remotamente. Preserve o cânone, o escopo cartográfico e a governança.

Execute leitura, proposta/implementação autorizada, deliberação integral do proprietário e verificações proporcionais ao bloco. Não avance para outra unidade. Gere handoff para MW-YYY+1 **somente se** o ponto atual estiver completamente fechado conforme o gate; caso contrário, mantenha a unidade aberta e registre apenas checkpoint de retomada da mesma MW.
```

## Política de divisão

Cada unidade trata **um ponto pequeno e verificável**, não uma fase inteira obrigatoriamente. Não encerrar o ponto por limite de contexto; caso a conversa precise terminar antes do aceite, registrar apenas checkpoint verificado e continuar a **mesma MW** em outro chat, sem handoff de próximo ponto. Nunca anunciar PASS sem evidência.

- **A — Bloqueante do mapa:** resolver ou propor decisão para construir/validar a geometria.
- **B — Condicionante geográfica:** registrar a consequência espacial e deixar o restante narrativo aberto.
- **C — Fora do escopo:** registrar sem investigar.

Não exigir que todas as pendências do suplemento sejam fechadas. Não usar `guide.md` como fonte de novos fatos, de estado de projeto ou como substituto dos assuntos proprietários.


## Protocolo visual obrigatório para revisões cartográficas

Diretriz expressa do proprietário em MW-013 (16/11/2026): **toda proposta visual cartográfica sujeita a aprovação deve mostrar a composição territorial total, nunca somente a região, camada ou recorte modificado.**

1. Exibir sempre **ANTES e DEPOIS** simultaneamente ou em duas vistas equivalentes e claramente rotuladas, com o mesmo enquadramento integral, orientação norte, escala e geometria de referência. Recolocar o modo de visão integral por padrão.
2. Preservar **todas as camadas relevantes de contexto** nas duas vistas: contorno e baía, ilhas (inclusive as hipotéticas), relevo, rios e todos os afluentes/ramificações, corpos d'água e elementos já existentes no comparador físico. Disponibilizar bacias, cristas, termas e outras camadas técnicas por alternância quando necessário à legibilidade. Nunca omitir geografia apenas para destacar a mudança.
3. A mudança sob análise deve ser a **única diferença visual substancial** entre as duas folhas. Não alterar cores de comparação, escala, recorte, simplificação, ordem de camadas nem posições das outras feições entre elas. Geometria estruturada mantém autoridade; renderização não cria cânone.
4. Acompanhar cada comparação com **inventário factual das alterações**: quais entidades, contornos, tamanhos/contagens ou relações foram mudados e quais ficaram intactos. Identificar explicitamente hipóteses, ressalvas e pendências.
5. A versão visual comparativa deve ser reproduzível a partir dos arquivos GitHub e apresentada para aprovação antes de considerar qualquer refinamento fechado. Aprovação de composição não é aprovação de perímetro nem de estilo gráfico. Se a visualização integral não for produzível, declarar a limitação e **não pedir aceite visual**.

Este protocolo é operacional para o Atlas, não altera a geografia canônica, a crônica nem decisões de raions.


## Entrega de prévias visuais no aplicativo e alternativa de download (aprovação do proprietário em 17/11/2026)

**Obrigatório em toda unidade Mapwork que demande aprovação visual do proprietário.** Esta diretriz está persistida neste `guide.md` no GitHub; **não depende de memória do ChatGPT, prompts de handoff nem histórico de conversa**.

1. **Apresentação primária no ChatGPT:** tentar exibir diretamente na resposta uma **visualização HTML interativa** do mapa, usando um recurso de incorporação realmente disponível na interface. O visual deve partir das **mesmas geometrias estruturadas e camadas do comparador publicado no GitHub**, com a composição integral e ANTES/DEPOIS onde houver revisão. Nunca substituir a geografia por um esquema improvisado nem publicar apenas link como se a visualização estivesse incorporada.
2. **Caso a interface do aplicativo não renderize HTML interativo**, declarar essa limitação de modo explícito e **fornecer o HTML interativo como arquivo para download**, para abertura no navegador. Não afirmar que a imagem/HTML apareceu no chat sem evidência e nunca atribuir sucesso à renderização somente porque um arquivo foi criado.
3. **Fallback visual direto**, quando tecnicamente viável: fornecer junto do HTML um **PNG/SVG integral** gerado do mesmo modelo cartográfico estruturado, útil para leitura imediata no aplicativo. O fallback estático não substitui a disponibilidade do HTML interativo e não pode modificar/omitir costa, baía, ilhas, rios, afluentes, relevo ou Ermos.
4. **Identidade e legibilidade:** comparar sempre as mesmas camadas, estilo, orientação, enquadramento e escala, com alterações sob análise claramente destacadas; usar legendas legíveis no celular e controles funcionais. Registrar qual artefato e SHA foram usados na visualização e no fallback. Validar os artefatos que puderem ser testados e especificar os que **não** foram testados em navegador/dispositivo real.
5. **Porta de aprovação:** solicitar decisão visual **apenas após fornecer um meio efetivo de inspeção integral** pelo proprietário. Se a interface não exibir a mídia, o arquivo de download é rota válida para inspeção; obter aceitação expressa do proprietário da versão efetivamente analisada. Uma aprovação da imagem não canoniza automaticamente geografia nem direitos administrativos.
6. **Aplicação permanente:** consultar esta regra no `guide.md` do GitHub no bootstrap e em **toda** nova etapa que exija exame visual; nunca confiar na recordação desta conversa. Se houver versões divergentes do guia entre master e branch, reconciliar com a versão aprovada publicada e registrar o SHA do guia aplicado.

**Resumo operacional:** primeiro HTML interativo **visível no ChatGPT quando suportado**; se não for renderizado, **HTML para download obrigatório**, com PNG/SVG integral como complemento viável; nunca depender de link isolado nem declarar visualização inexistente.
