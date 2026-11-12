# NOVYDRES / CHR-001 — Scene Execution Protocol V4 / gate narrativo
STATUS: ADENDO à V1–V3, G25–G28, sem alteração das versões anteriores.
Nova dependência local: PACING_TEMPORAL_FRAMING_V1, NARRATOR_PREPARATION_ADAPTER_V3, LONGITUDINAL_PROGRESS_GATE_V1; documentos CH00–CH04 de preparação global são apoio e não fonte de eventos.

## Antes da cena
1. Validar LIVE, checkpoint, fonte/eventos, decisões, dossiê efetivamente autorizado. Se dossiê ficou materialmente defasado -> STALE_PLAN_REVIEW; NÃO executar.
2. Validar razão dramática WHY_NOW, oportunidade e conflito reais, POTENTIAL_CHANGE, PC_AGENCY, CONSTRUCTION_FUNCTION, NPC_KNOWLEDGE e TIME_MODE.
3. Sem razão dramática, usar abstração/montagem/elipse e chegar a uma decisão com gatilho legítimo. Repetir acordar, café, brincadeiras ou burocracia não é progressão por si só.
4. Escopo temporal: não gastar anos por conta de escolhas não realizadas; não fixar data desconhecida. Respeitar prioridades declaradas do jogador.

## Durante
Player owns PC; Narrador owns causas externas e NPCs com autonomia. Dossiê é cenário de possibilidades, não roteiro. Tratar a relação com o sobrenatural em escala global e evitar revelação arbitrarizada. G25 e G27 para testes; janela FV após dados; nunca rolar efeito preparado de dossiê como resultado real. Só narrar consequências autorizadas.

## Fechamento e persistência
Cena encerra quando sua situação substantiva se resolve ou é transformada por retirada/fuga/desvio; não por troca de turno ou relógio. G28: um commit copy-on-write com batch ao final de cena, confirmar HEAD e readback; G26 preservado. Ato resolvido somente com ACT_RESOLUTION verificável e anti-duplicação DEC-CR-021; orçamento 675 inalterado.

## Pausa vigente para CHR-001
C09 encerrada; C10 não começou; A1 ainda OPEN, nenhum crédito novo. Este protocolo NÃO é revisão da provocação M2.04. A retomada narrativa de C10 depende de adendo prospectivo de preparação autorizado e validado separadamente; até lá, preparar documentação não é jogar.
