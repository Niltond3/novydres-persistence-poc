# CHR-001 / NPC Disposition
Implementação local, `STAGED` — ver `CONTRACT_V1.md`, `ACTIVATION_V1.md`, `STATE_V001.json`.
**Não é cânone global, não substitui G25/G27, não afeta o ciclo V0012/C15.** O uso requer ativação prospectiva durante transição orquestrada G28 com readback.

Comandos (Node >=18):
```sh
node --test novydres/chronicles/CHR-001/npc-disposition/TESTS_V1.mjs
node novydres/chronicles/CHR-001/npc-disposition/VALIDATOR_V1.mjs --root .
```
A regra usa H (-2..2), R=clamp(vínculo+pressões,-3..3), P=H+R. Perfis editoriais ancorados, nunca fatos retroativos. Estado COW só para mudanças sustentadas, apenas por cena concluída G28; sem histórico de microhumores.
