---
id: arch-phase-a-topology
status: CANDIDATO_PENDENTE_APROVACAO
scope: NOVYDRES_GLOBAL
classification: PLAYER_SAFE
---
# Topologia por assuntos, responsabilidades e fronteiras

## Topologia-alvo normativa proposta

    novydres/
      AGENTS.md                  # princípios mínimos e roteamento de papel (futuro, não criar agora)
      CONTEXT.md                 # descoberta e índice mínimo sem estado narrativo
      catalogo.json              # índice GERADO, conteúdo não autoritativo
      sistema/
        index.md
        governanca/{index.md,politicas/,decisoes/,aprovacoes/}
        regras/{index.md,v5/,criacao/,mecanica/}
        narrativa/{index.md,orquestracao/,papel/,preparacao/}
        arquitetura/{index.md,adr/,fase-a/}
      cenario/
        index.md
        historia/
        geografia/
        sociedade/
        politica/
        religioes/
        organizacoes/{org-id}/
        linhagens/{linhagem-id}/
      personagens/
        index.md
        {personagem-id}/{index.md,perfil.md,objetivos.md,relacoes.json,afiliacoes.json}
      cronicas/
        index.md
        {chronicle-id}/
          index.md
          configuracao.json
          biblia/
          tramas/{trama-id}/
          fios/{fio-id}/
          historias/{historia-id}/
          episodios/{episode-id}/
          cenas/{scene-id}/
          elenco/{personagem-id}/{estado.json,conhecimento.json,relacoes.json}
          registros/{eventos/,rolagens/,decisoes/,aprovacoes/,correcoes/}
          estado/{atual.json,projecoes/}
          preparacao/
          orquestracao/{ciclo.json,historico-de-transicoes/}
          auditorias/
      fontes/{index.md,registro.json,originais-textuais/,midia/}
      scripts/{catalogo/,validadores/,testes/,migracao/,fixtures/}

Os diretórios exibidos são slots; criar somente assuntos materialmente existentes e autorizados. GitHub Actions permanece em .github/workflows e é infraestrutura fiscalizada pelo detector de legado. README raiz pode existir como descrição, mas não substitui AGENTS/CONTEXT/catálogo. A estrutura POC existente deve ser absorvida como fixtures de teste ou excluída da árvore operacional na E, com histórico Git preservado; é proibido deixar uma rota antiga ativa ou uma pasta legacy/archive no HEAD final.

## Propriedade (único owner por campo)
| Área | Owner de informação | Não é dono de |
|---|---|---|
| sistema/governanca | precedência, decisões gerais, aprovações e política editorial | ato jogado específico |
| sistema/regras | regras V5, exceções formalmente aprovadas, motor e custos | estado atual do jogador |
| sistema/narrativa | contratos de papéis, orquestração e gates por tipo | ciclo efetivo de uma crônica |
| cenario | mundo global, cronologia macro, territórios, instituições e afiliações globais verificadas | percepção local de um NPC |
| personagens | identidade e traços globais transcrônicas de um ser, versão autorizada e fontes | ações, recursos e conhecimento específico em CHR-001 |
| cronicas/{id} | fatos jogados, autoria, estados e relações locais, cenas, tramas, cronologia, conhecimento situado, ciclos | cânone global e fichas de outras crônicas |
| fontes | origem textual, procedência, metadados de mídia e direitos | legitimidade de transformar cópia em cânone |
| scripts | implementações, testes e índices derivados | decisões editoriais |

Localizações e organizações globais residem em cenario; aparição/estado/interação de personagem pertencem à crônica. Uma relação global possui um owner; uma relação situacional pertence à crônica; o espelho inverso é sempre derivado. Uma decisão aplicada localmente permanece registrada na crônica com referência a sua autoridade global, se existir. Mover um arquivo não muda sua autoridade, congelamento nem público-alvo.

## Contrato de slice
Todo index.md existe somente para subject com conteúdo real e tem: subject_id imutável, kind, owner, scope, status editorial, visibility, fontes e hashes, mapa de documentos presentes, lista IDs relacionados, papéis permitidos e esquema de validação. Cada arquivo substantivo declara o mesmo subject_id e proíbe segundo owner. O índice não copia fatos nem resume segredos em título. Tamanho de arquivo resulta de coesão/limite da recuperação: preferir documentos isolados por tipo e consulta com índice, não fatiar arbitrariamente por limite de tokens. Se documento crescer a ponto de exigir leitura integral para um fato simples, separar por domínio sem quebrar proveniência.

## Padrões
- Diretório/arquivo novo: lowercase-kebab-case, extensões md/json/yaml; sem sufixo _V### de revisão. Exceções semânticas: CHR-001 e V5 enquanto edição da regra e IDs históricos preservados como dados.
- IDs canônicos distintos de path e nome exibido; ID uma vez atribuído não é reciclado, renomear label não renomeia identity.
- Arquivo corrente: index.md, perfil.md, estado.json, catalogo.json, config etc. Versão = commit SHA (objeto Git), sem campo version que simule segunda linha de tempo. schema_version é permitido para evolução do formato, NÃO para nomear cópias documentais.
- Formatos: Markdown para texto; JSON normalizado para integridade; YAML apenas se schema e parser determinísticos. Arquivos gerados contêm generated_from_commit/tree e checksum, e são recriados no mesmo commit candidato ou CI verifica igualdade.
- Consumo seletivo: nunca ler GM_HIDDEN para construir resposta PLAYER_SAFE, ainda que o agente operacional possa ler a fonte de verdade para executar validação.

## Questões de propriedade a revisar antes de migrar
Mapeamento de namespaces world/organizations vs chronicles/.../world; governance versus runtime; NPCs duplicados em sources/atlas; narrativas históricas acumulativas versus evento comprovado; binary-sources e Drive visuais; material editorial com status candidate e documento posterior de fechamento não confirmado. Não decidir por nome, data de modificação, maior número ou preferência estética; rastrear authority decision + fonte e criar registro CONFLICT quando preciso.
