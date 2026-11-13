# CHR-001 / NPC disposition — Correção de bootstrap V1
Base: 43715dc0efcae0d374c8cc30e2bc6fc0c527c997
A primeira publicação do módulo estava STAGED e NÃO VALIDADA: o workflow 42236371175 falhou por regex literal escapada incorretamente em VALIDATOR_V1.mjs. Correção de sintaxe e cálculo de Git blob NUL realizadas antes de qualquer ativação. Este reparo corrige apenas um arquivo criado na implementação inicial que nunca passou no teste; não toca arquivos canônicos, ciclos, estados de narrativa, cenas ou versão validada.
Aguardam readback, execução dos testes e validação do estado de stage. Nenhuma cena C15 iniciada.
