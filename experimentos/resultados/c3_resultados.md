# Resultados da Configuração 3 — Janela de contexto

A Configuração 3 avaliou o impacto da alteração da janela de contexto na execução local do modelo.

Foram comparadas duas configurações:

- contexto curto: `num_ctx = 1024`
- contexto longo: `num_ctx = 4096`

O modelo, a quantização, o ambiente e o prompt foram mantidos constantes.

## Resultados

| Execução | num_ctx | Resultado | Tempo total (s) | Carregamento (s) | Geração (s) | Tokens/s |
|---|---:|---|---:|---:|---:|---:|
| Curto 1 | 1024 | Sucesso | 392,638 | 380,046 | 8,527 | 3,635 |
| Curto 2 | 1024 | Sucesso | 425,296 | 382,574 | 38,033 | 0,710 |
| Longo 1 | 4096 | Sucesso | 511,902 | 340,999 | 33,383 | 0,869 |
| Longo 2 | 4096 | Timeout | — | — | — | — |
| Longo 3 | 4096 | Sucesso | 407,265 | 332,563 | 72,304 | 0,360 |

## Médias das execuções concluídas

| Métrica | num_ctx = 1024 | num_ctx = 4096 |
|---|---:|---:|
| Tempo total médio | 408,967 s | 459,583 s |
| Tempo médio de geração | 23,280 s | 52,844 s |
| Velocidade média | 2,172 tokens/s | 0,615 tokens/s |

## Observações

O aumento de `num_ctx` de 1024 para 4096 esteve associado a aumento do tempo médio total e do tempo de geração, além de redução da velocidade média de geração.

Também ocorreu um timeout durante uma das execuções com `num_ctx = 4096`, indicando menor previsibilidade no ambiente limitado utilizado.

O prompt efetivamente enviado possuía apenas 21 tokens. Portanto, este experimento avalia principalmente o efeito da **janela de contexto configurada**, e não o efeito de uma entrada real contendo milhares de tokens.
