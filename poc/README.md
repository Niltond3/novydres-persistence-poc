# NOVYDRES — POC de persistência

**Ambiente isolado, dados 100% sintéticos.** Não é a fonte de verdade da crônica. Não migrar nem alterar arquivos de Drive, canônicos ou congelados.

O teste grava evento, estado, episódio e índice em **um commit por turno**, valida readback, idempotência e recuperação. Uso exclusivo: um jogador e uma sessão por vez. Não executar testes de concorrência; não usar `force` na atualização do branch.

Diretório: `poc/chr-test-001/`. Valores, nomes, números e eventos são de teste. G19/G24 são contratos vigentes na crônica real até eventual mudança aprovada.
