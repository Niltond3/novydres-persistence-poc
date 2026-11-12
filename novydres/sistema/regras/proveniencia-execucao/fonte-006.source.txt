# NOVYDRES — NPC KNOWLEDGE GATE V1
Status: gate local de verificação antes de fala, decisão ou inferência de NPC; não cria conhecimento retrospectivo.

## Quatro estados separados
KNOWN: o NPC observou, ouviu, recebeu, deduziu sob evento validado ou teve prova documentada; para dedução sem certeza usar SUSPECTED.
CLAIMED: enunciado por uma fonte (inclusive o próprio NPC) sem confirmação independente; não converter em realidade por repetição.
SUSPECTED: conjectura atribuída de forma explícita ao NPC com origem; não conferir certeza nem identidade.
UNKNOWN: nenhuma evidência suficiente de que o NPC sabe; não declarar que sabe, nem que é necessariamente ignorante para sempre.

## Preflight obrigatório por afirmação que depende de informação privada
1. Extrair o conhecimento necessário para a fala/ação: proposição, NPC, ocasião e grau de certeza.
2. Consultar NPC_KNOWLEDGE_PROVENANCE vigente e o evento de origem; distinguir eventos que ocorreram para o leitor, PJ, NPC ou só narrador.
3. Checar EVENT_ID de transmissão: presença/atenção plausível, conteúdo revelado, via concreta (percepção, mensagem, investigação confirmada) e correções posteriores.
4. Se KNOWN com origem: pode usar; se SUSPECTED: só como hipótese; se CLAIMED: como relato atribuído, não verdade do cenário; se UNKNOWN: bloquear a afirmação informada. O NPC pode reagir, desconfiar ou perguntar sem saber.
5. Se NPC adquirir informação em cena, criar delta de conhecimento com source_event_id no buffer G28. A aquisição se torna fonte auditável apenas após a cena ser consolidada.
6. NÃO copiar fatos do contexto do narrador, histórico do jogador, memória do ChatGPT ou GM_HIDDEN para NPC automaticamente.
7. Segredos GM_HIDDEN e NPCs independentes podem existir no material do narrador, mas não os incluir em respostas públicas salvo descoberta legítima.

## Regressão vinculada ao M2.03
- Nadezhda em M2.03.117: nome Bartholomeu = UNKNOWN; uso antecipado foi erro do narrador, não revelação válida. DENY.
- Nadezhda desde M2.03.124: FIRST_NAME_ONLY = KNOWN, por fala do PJ 'foi Bartolomeu que te mandou'. ALLOW apenas primeiro nome.
- Paramédicos e homem ferido: nome não transmitido em registro confirmado; UNKNOWN_NO_SOURCE. DENY nome até nova evidência.
- Mulher, Gromov, homem ferido e alegações de natureza sobrenatural: CLAIMED/SUSPECTED conforme fonte; nada disso vira confirmação ontológica automática.
- Mary e crianças não recebem informação sobre documentos, ambulância e Nadezhda porque Bart voltou à casa.

## Contrato de saída
Para cada afirmação sensível: npc_id, proposition_id, confidence KNOWN|CLAIMED|SUSPECTED|UNKNOWN, source_event_id/path, audience, verdict ALLOW|QUALIFY|DENY. Se não for possível consultar origem relevante, suspender declaração positiva e pedir recuperação; não improvisar prova. Reações de NPC continuam independentes.
