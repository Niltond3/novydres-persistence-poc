# NOVYDRES / CHR-001 — Protocolo de seleção temporal e prelúdio de elipse V1

CLASSIFICAÇÃO: contrato operacional local PLAYER_SAFE. Fonte: `novydres/runtime/narrative-architecture/program/decisions/PLAYER_DECISION_CHR001_LIVING_ELLIPSES_V001_PLAYER_SAFE.json` (decisão do jogador). Aplicação somente prospectiva após pin por ciclo/manifesto.

## Fluxo

**0. Escolha dramatúrgica:** ler conflitos vivos, compromissos, demandas e tempo histórico. Decidir CONTINUITY / ABSTRACTION / MONTAGE / ELLIPSIS. Registrar razão. **A elipse não é etapa fixa** por cena, provocação, ato ou capítulo. Se algo interessante permanece, jogar em continuidade.

**1. Planejamento da elipse (somente ELLIPSIS ou MONTAGE longa):** horizonte, continuidades estabelecidas, personagens/instituições com autonomia e clocks, oportunidades, riscos, mudanças em emprego/negócio/patrimônio/relações/antagonismos e outros fios apropriados. Um avanço sem causa e alcance suficiente fica UNKNOWN, não vira fato. A escala de mudanças deve ser proporcional ao intervalo. Não apagar prioridades ou escolha com impacto permanente.

**2. Classificar cada efeito:**
- `INDEPENDENT_WORLD_CAUSE`: iniciativa de NPCs, mercado, instituição, circunstância; pode amadurecer durante intervalo se causa/sujeito/limites documentados.
- `ESTABLISHED_ROUTINE`: continuidade plausível de padrão previamente aprovado, sem ação especial presumida.
- `PLAYER_CHOICE_REQUIRED`: não consolidar sem resposta do jogador.
- `MECHANICAL_UNCERTAINTY`: só resolver com procedimento real, sujeito a regra vigente.
- `UNRESOLVED_OR_HIDDEN`: manter incerto ou oculto, não vazar.

**3. Prelúdio opcional:** 0–2 testes distintos ANTES do spotlight principal, apenas se decisões de Bart durante o intervalo forem necessárias para calibrar consequências. Apresentar dilema em linguagem diegética, permitir qualquer reação, aguardar resposta; anunciar pool, dificuldade, stakes, oferecer Take Half se permitido; rolar apenas com método verificável; depois janela de FV com autorização explícita. Escolhas que dispensam rolagem são escolhas, não resultados fabricados. Não tratar 2 testes como limite de mensagens ou de interação. Se precisar 3+ testes ou confronto dramático, abortar a compressão e usar cena plena/retorno ao Dramaturgo, sem perder a escolha.

**4. Abertura narrativa:** depois do prelúdio (ou diretamente se zero testes), o Narrador começa por uma síntese viva de eventos do intervalo já legitimados na abertura. Inclui efeitos concretos em domínios pertinentes, suas causas percebidas pelo protagonista e quadro imediatamente jogável. Não divulgar planos ocultos, resultados não verificados ou fatos que exigiriam uma escolha que o jogador não fez. Em CONTINUITY, dispensar resumo e abrir diretamente.

**5. Persistência:** `GM_PLAN` não é evento; a representação autorizada na abertura cria fatos diegéticos. G28 registra no fechamento da cena: boundary temporal, causas, observações/NPC claims, decisões, rolls/FV, novos conhecimentos e deltas de estado por arquivo apropriado. G26 em falha; não registrar retroativamente no checkpoint fechado. Evitar duplo lançamento de efeitos no ciclo seguinte. XP por ACT_RESOLUTION, jamais por duração do intervalo.

## Esquema lógico sugerido do pacote de Dramaturgo

`temporal_mode`, `rationale`, `time_window`, `source_checkpoint`, `world_threads[]` com `cause / actor / capability / impact_if_realized / pc_knowledge`, `pc_decisions[]`, `test_specs[]` (0–2), `opening_variants`, `spotlight_entry`, `mechanics_guard`, `provenance`, `stop_if`. Quando `CONTINUITY`, arrays de avanço e prelúdio vazios e `time_window=NONE`.

## Regra explícita de estabilidade

Não introduzir elipse apenas para atualizar empresas ou NPCs. Um personagem pode passar vários atos, cenas e provocações em um único dia dramático. Ao contrário, um mês pode passar com alterações reais em assuntos correntes, desde que seus agentes/custos sejam comprováveis e o protagonista não seja transformado em espectador passivo de suas próprias escolhas.