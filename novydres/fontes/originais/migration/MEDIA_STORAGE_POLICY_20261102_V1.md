# NOVYDRES — Política de armazenamento de mídia (migração, 2026-11-02)

**Decisão explícita do usuário:** imagens e arquivos visuais originais ficam no **Google Drive**; o **GitHub guarda apenas links, metadados, proveniência e índices**. Esta decisão altera o meio de persistência visual, NÃO o estado editorial, as aprovações ou o cutover geral MIG-DEC-002.

1. Preservar cada arquivo binário original, sem recompactar, redesenhar, converter, renomear ou substituir por preview. Copiar diretamente da referência de Library autorizada para a pasta de ativos originais do Drive.
2. Readback no Drive: conferir identificador, nome, MIME e tamanho do original. Anotar quando SHA-256 de origem ou destino não estiver disponível; não alegar igualdade criptográfica sem teste.
3. No GitHub, registrar Drive file ID, URL, nome, Library ID, status editorial e resultados de validação no `migration/VISUAL_ASSET_REGISTRY_V2.json`. Ao retomar, usar a versão mais recente, respeitando G24.
4. Referências pendentes continuam sem URL; nomes semelhantes não autorizam substituição. Nunca inferir APPROVED/FROZEN de uma cópia ou do nome do arquivo.
5. Remover binários do estado HEAD do GitHub, preservando o histórico dos commits anteriores. A limpeza integral de blobs em commits antigos exigiria reescrita de histórico e NÃO está autorizada aqui.
6. O acesso às imagens passa a depender do Drive, inclusive depois que o GitHub for a fonte textual principal. URLs privadas não são URLs públicas; não ampliar permissões sem ordem do usuário.
7. A operação não altera canônico, chapa visual, POC, cenas, personagens ou decisões anteriores. MIG-DEC-002 permanece NÃO ATIVADO.

Pasta Drive verificada: https://drive.google.com/drive/folders/15eZF0RAiqSnlrWhXhgt8P58Tas49wq65
