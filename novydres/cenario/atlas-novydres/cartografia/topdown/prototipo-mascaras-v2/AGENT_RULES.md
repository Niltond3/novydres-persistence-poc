# NOVYDRES — Regras para agentes (POC de máscaras V2)

**Escopo:** experimento não canônico em Kingswell, derivado da POC V1 aprovada. O único alvo é a arte 2.5D dos sete edifícios de dois lotes. Este arquivo não autoriza urbanizar outros setores nem alterar fontes oficiais.

## Fontes obrigatórias (sem adivinhar)

1. Leia o `HEAD` remoto de `master`, `novydres/AGENTS.md`, `novydres/CONTEXT.md` e `novydres/catalogo.json` no **mesmo commit**; para dados cartográficos, consulte o Atlas e `cartografia/guide.md`.
2. Use a U02 aprovada como **raster de entrada imutável**; confira SHA-256 `9d55965f45181e3b943552e32df0e8ad41b63c8974ffd6e670f447ffd36eb9a0`.
3. Consulte `geometria_v2.json` para geometria/parentesco e `manifest.json` para caminhos, hashes e ordem de composição. Se um arquivo ou coordenada obrigatória estiver ausente, **pare**, registre `UNKNOWN` e não invente polígonos.
4. **Fonte visual ≠ cânone.** Todos os lotes e alturas relativos deste experimento são candidatos. Nunca trate os contornos desenhados como cadastro ou como limites administrativos aprovados.

## Como criar ou editar

1. Identifique `id`, `parent` e `footprint_px` exatos. A hierarquia é cidade → região → bairro → lote → prédio. Infraestrutura é uma camada independente protegida.
2. Renderize **um prédio por PNG RGBA** e mantenha **uma máscara estável por prédio**, ambos identificados no manifesto. A planta geral permanece superior ortográfica; **o desenho local do prédio é oblíquo 2.5D**, mostrando telhado e fachadas sul/leste, com convenção e luz iguais em todos.
3. Não altere footprint, lote ou posição do prédio para melhorar o encaixe. Ajuste apenas pixels internos à máscara autorizada. Se volume/sombra não couberem, **reprove a tentativa e proponha novo envelope para aprovação**, sem esticar a máscara silenciosamente.
4. Edite apenas o PNG do prédio-alvo. O lote apenas **compõe** os seus prédios; editar um não obriga redesenhar os demais.
5. Recompose o lote, o bairro e a cidade, sempre com o mesmo enquadramento, orientação e resolução. As regras de sobreposição são explícitas no manifesto.
6. Faça diff de pixels: qualquer alteração fora da máscara-alvo reprova a microedição; qualquer alteração fora das máscaras dos lotes reprova a implantação. Valide também integridade SHA da U02, ausência de sobreposição de máscaras, pertencimento ao lote e hashes dos assets não alterados.
7. Mostre **ANTES/DEPOIS integral e zoom local**, em arquivo HTML ou PNG disponível diretamente pelo chat. Obtenha aprovação visual explícita; não feche U03, não promova para master, não canonize nem avance para U04 automaticamente.

## Comandos (na pasta da POC)

```bash
pip install -r requirements.txt
python render_v2.py --base /caminho/T03_U02_aprovada.png --init-assets
python render_v2.py --base /caminho/T03_U02_aprovada.png --edit-b2
python render_v2.py --base /caminho/T03_U02_aprovada.png
```

`--init-assets` é apenas a implantação inicial. `--edit-b2` regrava **somente** a variante `b2_cobre.png`, não os outros sete assets ou suas máscaras. Sem flags, o script recompõe a partir dos PNGs já existentes e valida. Para qualquer outro edifício, substitua somente o PNG daquele `id`, sem mexer na máscara, e recomponha. Se o novo estilo exigir um envelope maior, **não execute automaticamente**: solicite aprovação da nova máscara.

## Não fazer

- Não gerar vários prédios como uma só textura indivisível.
- Não confundir ilustração 2.5D com câmera 3D, escala real ou cadastro.
- Não inferir instalações, facções, POIs, limites ou topologia a partir de padrões de cor.
- Não dizer `PASS` se um teste falhar ou for impossível verificar.