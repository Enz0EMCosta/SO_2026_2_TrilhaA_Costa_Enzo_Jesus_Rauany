# Resultados — Configurações C1 e C2

## Configuração C1 — execução padrão

Na configuração C1 foi executada uma requisição por vez. Foram realizadas duas repetições para a carga pequena e duas para a carga grande.

### Carga pequena

| Repetição | TTFT (s) | Tempo total (s) | Tokens entrada | Tokens saída | Tokens/s |
|---|---:|---:|---:|---:|---:|
| 1 | 84.667 | 103.863 | 22 | 81 | 6.573 |
| 2 | 73.574 | 78.705 | 22 | 76 | 14.959 |

TTFT médio: 79.12 s.

### Carga grande

| Repetição | TTFT (s) | Tempo total (s) | Tokens entrada | Tokens saída | Tokens/s |
|---|---:|---:|---:|---:|---:|
| 1 | 92.794 | 195.142 | 120 | 1518 | 14.991 |
| 2 | 86.351 | 163.459 | 120 | 1061 | 13.952 |

TTFT médio: 89.57 s.

---

## Configuração C2 — 3 requisições simultâneas

Na configuração C2 foram executadas três requisições simultâneas. Cada repetição representa um lote contendo três requisições.

### Carga pequena — repetição 1

| Requisição | TTFT (s) | Tempo total (s) | Tokens entrada | Tokens saída | Tokens/s |
|---|---:|---:|---:|---:|---:|
| 1 | 73.953 | 78.216 | 22 | 85 | 16.383 |
| 2 | 81.786 | 85.847 | 22 | 74 | 18.387 |
| 3 | 78.362 | 81.642 | 22 | 60 | 18.641 |

Tempo total do lote: 85.917 s.

Total de tokens de saída: 219.

### Carga pequena — repetição 2

| Requisição | TTFT (s) | Tempo total (s) | Tokens entrada | Tokens saída | Tokens/s |
|---|---:|---:|---:|---:|---:|
| 1 | 71.605 | 76.311 | 22 | 73 | 18.683 |
| 2 | 63.737 | 71.467 | 22 | 80 | 13.863 |
| 3 | 76.627 | 80.857 | 22 | 74 | 17.024 |

Tempo total do lote: 80.874 s.

Total de tokens de saída: 227.

### Carga grande — repetição 1

| Requisição | TTFT (s) | Tempo total (s) | Tokens entrada | Tokens saída | Tokens/s |
|---|---:|---:|---:|---:|---:|
| 1 | 232.720 | 300.166 | 120 | 1108 | 16.470 |
| 2 | 93.797 | 165.570 | 120 | 1119 | 15.787 |
| 3 | 165.753 | 232.506 | 120 | 1085 | 16.311 |

Tempo total do lote: 300.189 s.

Total de tokens de saída: 3312.

### Carga grande — repetição 2

| Requisição | TTFT (s) | Tempo total (s) | Tokens entrada | Tokens saída | Tokens/s |
|---|---:|---:|---:|---:|---:|
| 1 | 216.354 | 284.914 | 120 | 1134 | 16.594 |
| 2 | 157.940 | 216.186 | 120 | 972 | 16.753 |
| 3 | 83.400 | 157.752 | 120 | 1171 | 15.892 |

Tempo total do lote: 284.947 s.

Total de tokens de saída: 3277.

---

## Comparação C1 x C2

### TTFT — carga grande

TTFT médio da C1:

89.57 s

TTFT médio das seis requisições da C2:

158.33 s

Aumento aproximado do TTFT:

76.8%

Os resultados mostram que, para a carga grande, as requisições concorrentes apresentaram maior espera até o primeiro token.

---

## Monitoramento de recursos

As métricas desta seção foram obtidas em execuções adicionais de monitoramento e não correspondem diretamente às duas repetições oficiais apresentadas anteriormente.

| Configuração | CPU média | CPU pico | RAM média | RAM pico | Threads máximas |
|---|---:|---:|---:|---:|---:|
| C1 pequena | 107.32% | 137% | 3195.68 MB | 3991.66 MB | 15 |
| C1 grande | 150.31% | 227% | 3381.68 MB | 4039.43 MB | 15 |
| C2 pequena | 104.03% | 141% | 3107.00 MB | 3956.31 MB | 15 |
| C2 grande | 231.00% | 310% | 3387.51 MB | 3938.38 MB | 15 |

Na carga grande, a CPU média passou de 150.31% na C1 para 231.00% na C2.

A memória média permaneceu próxima de 3.4 GB nas duas configurações de carga grande e o máximo de threads permaneceu em 15.

Isso indica que as três requisições não resultaram em uma multiplicação proporcional da memória ou do número de threads do processo do modelo.

---

## Q7 — Impacto da concorrência

A concorrência permitiu que três solicitações fossem submetidas no mesmo lote, porém não melhorou a responsividade individual em cargas maiores.

Na carga grande, o TTFT médio passou de aproximadamente 89.57 s na C1 para 158.33 s na C2, representando aumento aproximado de 76.8%.

Além disso, as requisições da C2 apresentaram tempos de primeiro token bastante diferentes dentro do mesmo lote. Esse comportamento evidencia espera e competição durante o processamento das solicitações concorrentes.

Portanto, existe um trade-off entre atendimento de múltiplas solicitações, latência individual e utilização dos recursos computacionais.

---

## Q8 — Competição por recursos

Os resultados mostram que o efeito da concorrência depende da carga.

Na carga grande, a CPU média aumentou de 150.31% na C1 para 231.00% na C2, com pico de 310% na execução monitorada da C2.

Por outro lado, a RAM média permaneceu próxima de 3.4 GB e o número máximo de threads permaneceu em 15.

Isso sugere que as requisições concorrentes compartilham recursos do mesmo processo responsável pelo modelo, em vez de carregar três cópias independentes completas do modelo na memória.

Como o WSL2 estava limitado a 5 GB de RAM e também foi observada utilização de swap durante o funcionamento do ambiente, a memória disponível constitui outra restrição importante.

Sob carga maior, as solicitações passam a competir principalmente por capacidade de processamento e pelos demais recursos compartilhados do processo, aumentando a latência individual.

---

## Arquivos de evidência

Os dados brutos do monitoramento estão disponíveis em:

- `C1_pequena_recursos.csv`
- `C1_grande_recursos.csv`
- `C2_pequena_recursos.csv`
- `C2_grande_recursos.csv`

Os scripts utilizados para C2 e para o monitoramento estão disponíveis em `experimentos/scripts/`.
