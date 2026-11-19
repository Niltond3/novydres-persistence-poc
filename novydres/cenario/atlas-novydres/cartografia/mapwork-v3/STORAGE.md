# Armazenamento de imagens via Google Drive

Pasta privada verificada via Google Drive plugin: `NOVYDRES_MAPWORK_V3_ASSETS`, ID `1DP7OtEmRuNl093HhQf1IjAA2vd1XPAWn`.
Base U02 imutável: ID `1PrfWEcD07Gz5eX5r2qKGaRlecixVKh6r`, SHA256 `9d55965f45181e3b943552e32df0e8ad41b63c8974ffd6e670f447ffd36eb9a0`.

O bridge ChatGPT `files__manage_library` aceita `source_file_ref` dos arquivos gerados e `destination_path="/Google Drive/NOVYDRES_MAPWORK_V3_ASSETS/<nome>.png"`. Depois do upload, recuperar o ID nativo de Drive pelo resultado e verificar tamanho/MIME/pasta com `mcp__Google_Drive__get_file_metadata`. Na recuperação, usar o conector Google Drive para ler ou materializar o asset; confirmar SHA256 **dos bytes locais**, não apenas o tamanho informado pela API.

Nomes imutáveis recomendados: `<zona>/<categoria>/<id>_<sha256-curto>.png` (pasta pode ser flat na primeira versão; use ID, não nome, como referência). Não substituir arquivos aprovados; criar novo asset e atualizar o manifesto candidato. Um arquivo Drive não se torna canônico sem aprovação visual do conjunto.

Recebimento mínimo no GitHub: `{ "drive_file_id": "ID-real", "sha256": "hex64", "path": "assets/...png" }`. Para tiles renderizados, os campos `drive_file_id:null` no manifesto de saída indicam **AINDA NÃO ENVIADO**; release não publicável enquanto houver nulls.

**Limite de segurança:** GitHub Actions não pode utilizar automaticamente a autenticação privada do plugin do ChatGPT. Sem uma credencial Google dedicada à CI, ele valida schemas e metadados, enquanto o agente valida os bytes baixados e escreve recibos de readback. O workflow não deve afirmar que executou uma auditoria remota que não fez.
