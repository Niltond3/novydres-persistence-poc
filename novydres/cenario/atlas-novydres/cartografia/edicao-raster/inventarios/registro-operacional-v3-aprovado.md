# NOVYDRES — Registro operacional do inventário espacial V3 aprovado

**Estado:** CLOSED_FOR_INVENTORY_SCOPE / OWNER_APPROVED; máscaras e geografia exata seguem abertas.  
**Imagem-base:** `NOVYDRES_VISUAL_CANON_GOTHIC_PUNK_V1` — 1448×1086 px, SHA-256 PNG `50014c337fa101a5b853fa53bdba86af424c1ec103009b986544e252bec492cb`.  
**Proveniência:** inventário V3 candidato na branch `mapwork/inventario-espacial-v3-pois-ferroviarios`; decisão explícita do proprietário para unificar a Estação Sul de Carga com POI 21, seguida de aceite desta consolidação.

## Resultado fechado neste escopo

- **9 zonas** visuais de trabalho aprovadas (não são limites administrativos canônicos definitivos).
- **34 POIs ativos** e identificados (32 anteriores + POI 33 + POI 34; POI 21 recebeu equivalência de identidade).
- **POI 21:** Estação Sul de Carga / Pátio Ferroviário — mesma entidade, **identidade canonicamente aprovada**. O número 35 fica **aposentado como alias histórico de 21**, nunca segundo POI.
- **POI 33:** Expresso Transibérico/Transberíngio — corredor ferroviário linear independente.
- **POI 34:** Estação Norte de Passageiros — complexo independente.
- **M01/M02:** máscaras históricas preservadas; não são sinônimos de POIs 21, 33 ou 34.
- **Crisol:** área de estudo para redesenho insular permanece candidata.

## Pontos de conflito geográfico, não resolvidos por esta aprovação

1. O antigo POI 21 tinha âncora visual Sulfok em `(348,984)`; a estação de carga sul que figurava como POI 35 tinha âncora visual Drevnigrad em `(1104,871)`. O registro V3 aprovado assume **uma única identidade POI 21**, utiliza a segunda âncora **somente como proposta visual**, e guarda a primeira apenas como referência de auditoria. **O raion definitivo não está aprovado.**
2. GEO-013.1 estabelece a parada internacional de **passageiros** em Sulfok; a **Estação Norte POI 34** está proposta visualmente em Vasyl Bay. Não declarar a mesma instalação sem reconciliação formal.
3. GEO-013.1 não define o raion da parada internacional de **carga**. A identidade do POI 21 não resolve automaticamente se ele constitui essa parada nem o traçado ferroviário canônico.
4. O corredor oeste sobre água não pertence a Kingswell nem a nenhum raion continental por inferência do raster.

## Próximo procedimento — aprovação individual de máscaras

1. Recuperar e conferir a imagem gótica imutável (hash e dimensões); carregar os **34** POIs e **9** contornos de zonas deste inventário.
2. Selecionar **um** alvo por vez: raion, POI, corredor ou conjunto de infraestrutura. Separar corpo da estrutura, área de expansão e exclusões de vias, trilhos, pontes, costa e vizinhança.
3. Mostrar o **mapa integral** com polígono proposto e áreas protegidas, antes de criar qualquer máscara; obter aprovação expressa da delimitação.
4. Só então gerar o PNG binário da máscara e registrar JSON vetorial, versão, SHA e dependências. Máscara aprovada **não** é arte aprovada.
5. Editar a cópia cumulativa sem alterar pixels externos; validar também geometria, encaixes, sombras, fachadas, ruas e trilhos; mostrar comparação ANTES/DEPOIS integral em HTML offline, com download no chat.
6. Só persistir uma nova arte canônica mediante aceite próprio e verificação remota; não iniciar a próxima unidade com decisões substantivas abertas.

## Integridade e escopo

- Nenhum pixel da imagem gótica foi modificado neste registro.
- Nenhuma nova máscara PNG foi aprovada ou gerada.
- Inventário visual V3 fechado; perímetros e localização geográfica formal pendentes.
- O arquivo de identidade do POI 21 fica preparado no **assunto proprietário**, para promoção e propagação controlada; branch candidata **não é master**.
- Contagem validada: 9 zonas; 34 POIs ativos; 1 alias aposentado; 1 corredor linear; 2 instalações ferroviárias; nenhum `poi-35` ativo.