# TEMPLATE EXECUTÁVEL — NOVYDRES MAPWORK V3 / CIDADE VELHA

Alvo: **Cidade Velha (Kingswell)**, núcleo histórico de nome formal Kingswell situado no raion homônimo **Kingswell** (`district-chelsea`). Núcleo histórico e raion são entidades espaciais distintas, apesar da homonímia.

Repositório: `Niltond3/novydres-persistence-poc`. No HEAD de `master`, leia `novydres/AGENTS.md`, `CONTEXT.md` e `catalogo.json` no mesmo SHA. Siga ADR-002, PRD-ATLAS-001, `cartografia/guide.md` e `cartografia/mapwork-v3/AGENT.md`, config, schemas, scripts, templates e manifestos. **Se a V3 ainda for branch candidata**, declare-a e use o SHA verificado; não presuma integração a master.

**Sessão 1 — planejar antes de gerar:**
1. Recupere de fontes proprietárias a definição vigente de Cidade Velha, sua geografia, história, instituições, redes, restrições, visibilidade e versão global anterior aprovada. Distinga CANON, CANDIDATE e UNKNOWN, sem inferir fronteiras ou metros.
2. Inspecione as zonas adjacentes efetivamente geradas e conectores globais; reconcilie roads/tram/rail/water/Ermos. Se houver conflito com aprovado, bloqueie e apresente proposta de solução sem alterar vizinhos.
3. Pesquise na web referências reais de bairros históricos frios e densos, arquitetura envelhecida, estrutura viária, transporte, equipamentos e tecido urbano. Registre URLs e motivos de analogia, sem projetar fatos reais diretamente como cânone.
4. Faça **somente perguntas substantivas ainda abertas, uma de cada vez**. Não gere imagens artísticas enquanto houver decisão bloqueante.
5. Depois das decisões, apresente esboço técnico 2D da **cidade integral com destaque da Cidade Velha**, bairros/quadras/lotes, acessos, hidrografia, Ermos, redes e POIs, mais resumo curto; aguarde minha aprovação expressa do esboço.

**Após aprovação do esboço, sem pedir confirmação entre microtarefas:** gere por **lote** (um asset PNG RGBA e uma máscara por lote, bleed controlado), com exceções individuais para edifícios institucionais/especiais. Use perspectiva oblíqua 2D, escala única, iluminação fria coerente e variações arquitetônicas. Para cada item gere, cheque, corrija com limite, armazene no Google Drive V3, confirme ID/SHA, componha em mosaicos globais e valide continuidade. Checkpoints permitem retomar a MESMA unidade em nova sessão. Se houver bloqueio técnico persistente, pare apenas aquele item com diagnóstico.

**Fechamento:** entregue no chat HTML interativo integral ANTES (última versão global aprovada; na primeira, U02) / DEPOIS, mais zoom por lote e relatório conciso. Só após minha aprovação da composição efetiva persista release aprovada no GitHub por CAS com readback; não canonize geografia por implicação. Não entregue links GitHub como canal de inspeção visual. Não declare tarefas assíncronas invisíveis.
