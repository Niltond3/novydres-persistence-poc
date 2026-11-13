# NOVYDRES — BOOTSTRAP OPERACIONAL CHATGPT WEB V1
Uso: nova conversa ChatGPT Web; conector GitHub conectado. Não requer Codex, servidor, automação ou armazenamento fora do GitHub.
Identificador de pacote: NOVYDRES_SCENE_EXECUTION_V1.
Manifesto candidato de entrada: novydres/MANIFEST_V15.json. Verificar sempre se existe sucessor validado (nunca tomar o número maior isolado como autoridade).

## Prompt curto de retomada (copiar para conversa nova)
"Retome NOVYDRES/CHR-001 usando exclusivamente o conector GitHub ligado a Niltond3/novydres-persistence-poc, master. Leia o manifesto operacional mais recente com linhagem comprovada, .AGENT.md, .CONTEXTG.md, decisões vigentes, G28 e runtime/scene-execution/SCENE_EXECUTION_PROTOCOL_V1.md; use SCENE_PACKET_SCHEMA_V1 e gates de NPC/mecânica. Reconstitua LIVE, HISTORY_INDEX e somente evidência histórica pertinente. Não invente conhecimento NPC, RNG ou compras. Antes de cena nova, execute SESSION_TRANSITION_V1 com minha autorização; não inicie M2.04 automaticamente. M2.03 permanece fechada. GitHub-primary, copy-on-write, um commit por cena encerrada, readback. Informe checkpoint e opções, não avance o protagonista."

## Ordem econômica
1. Git refs/heads/master; manifesto de linhagem verificada; contrato GitHub e G28.
2. LIVE e HISTORY_INDEX correntes e referências de character/knowledge/open_threads.
3. Ao citar NPC/história, consultar registros originais através do índice e correções.
4. À primeira nova cena, projetar pacote efêmero conforme JSON schema, não gravar sample como fato.
5. Turnos com buffer G28; no fechamento, commit atômico e readback.
6. Em novo chat, só presumir persistência do que possui GitHub commit confirmado.

## Limites transparentes
As três funções são fases do MESMO modelo, não agentes independentes. Contratos e testes de regressão documental não garantem cumprimento sem verificação ativa. Nunca alegar que script foi automaticamente executado se o ambiente ChatGPT Web não forneceu execução verificável.
