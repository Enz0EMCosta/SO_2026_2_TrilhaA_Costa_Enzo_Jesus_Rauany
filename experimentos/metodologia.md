# Metodologia

## Variáveis do experimento

- Tamanhos de entrada: carga pequena e carga grande.
- Entrada pequena: prompt com 22 tokens.
- Entrada grande: prompt com 120 tokens e solicitação de resposta mais extensa.
- Número de repetições: 2 por tamanho de carga em cada configuração.
- Configurações comparadas nesta etapa: C1 e C2.
- C1: 1 requisição por vez.
- C2: 3 requisições simultâneas.
- Principal variável alterada entre C1 e C2: nível de concorrência.

O modelo, a quantização, o contexto, o hardware e os prompts foram mantidos entre C1 e C2.

## Métricas

### Tempo até o primeiro token (TTFT)

O TTFT representa o intervalo entre o início da requisição e o recebimento do primeiro conteúdo de resposta do modelo.

As requisições foram realizadas com streaming habilitado e o tempo foi medido em Python utilizando `time.perf_counter()`.

### Tempo total

Intervalo entre o início da requisição e a finalização completa da geração da resposta.

### Throughput / tokens por segundo

A taxa de geração foi calculada a partir dos campos retornados pela API do Ollama:

`tokens/s = eval_count / (eval_duration / 1e9)`

O `eval_duration` é fornecido pelo Ollama em nanossegundos.

Para a C2 também foi registrado o tempo total do lote contendo as três requisições simultâneas.

### CPU

O processo monitorado foi o `llama-server`, responsável pela execução do modelo.

Durante as execuções adicionais de monitoramento foram realizadas amostragens aproximadamente a cada 1 segundo.

O percentual de CPU foi obtido a partir das informações do processo no Linux. Como o processo é multithread, valores superiores a 100% são possíveis, representando utilização de mais de um núcleo lógico.

### Memória

Foi monitorado o RSS (Resident Set Size) do processo `llama-server`, convertido de KB para MB.

### Threads

Foi registrado o número de threads do processo `llama-server` durante as execuções monitoradas.

### Armazenamento

O ambiente utilizou SSD NVMe. O modelo e os arquivos do ambiente foram armazenados localmente. Não foi realizada medição contínua de I/O de armazenamento nas execuções C1 e C2.

## Procedimento

### 1. Preparação do ambiente

O modelo `hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf:latest` foi executado localmente utilizando Ollama no WSL2.

A API utilizada foi:

`http://127.0.0.1:11434/api/generate`

As requisições utilizaram:

- `stream = true`, permitindo medir o TTFT;
- `think = false`, evitando a geração do processo de raciocínio na resposta;
- contexto de 4096 tokens.

### 2. Controle de inicialização

Antes de cada repetição oficial, o modelo foi explicitamente parado com `ollama stop`.

Dessa forma, as repetições foram realizadas em condição de cold start, permitindo observar também o custo de carregamento do modelo.

O campo `load_duration` retornado pelo Ollama foi preservado nos resultados para auxiliar na análise desse custo.

### 3. Configuração C1

Na C1 foi enviada uma requisição por vez.

Foram realizados:

- 2 testes com a entrada pequena;
- 2 testes com a entrada grande.

Para cada execução foram registrados:

- TTFT;
- tempo total;
- `prompt_eval_count`;
- `eval_count`;
- `eval_duration`;
- `load_duration`;
- tokens por segundo.

### 4. Configuração C2

Na C2 foram enviadas três requisições simultâneas utilizando Python e `ThreadPoolExecutor(max_workers=3)`.

Foram realizados:

- 2 lotes com entrada pequena;
- 2 lotes com entrada grande.

Cada lote continha 3 requisições simultâneas.

Foram registradas as métricas individuais de cada requisição e o tempo total necessário para concluir o lote.

### 5. Monitoramento de recursos

CPU, RAM e threads não foram coletados retroativamente nas repetições oficiais.

Por esse motivo, foram realizadas execuções adicionais especificamente para o monitoramento de recursos, uma para cada combinação:

- C1 pequena;
- C1 grande;
- C2 pequena;
- C2 grande.

O script `monitor_ollama.py` identificou dinamicamente o processo `llama-server` e registrou aproximadamente a cada segundo:

- timestamp;
- PID;
- percentual de CPU;
- percentual de memória;
- RSS em KB;
- número de threads.

Os dados brutos foram armazenados nos arquivos CSV presentes em `experimentos/resultados/`.

Essas execuções de monitoramento são apresentadas separadamente das duas repetições oficiais para evitar misturar resultados obtidos em execuções diferentes.

## Observações e dificuldades encontradas

Durante a preparação do ambiente foram encontradas limitações relacionadas principalmente à memória disponível. O computador possui 8 GB de RAM e o WSL2 foi limitado a 5 GB, enquanto o modelo quantizado ocupa vários gigabytes quando carregado.

Também foi observada utilização de swap durante a execução do modelo e do Open WebUI, indicando pressão de memória no ambiente.

Inicialmente, uma requisição realizada pelo Open WebUI ultrapassou o contexto disponível de 4096 tokens. Para manter o experimento compatível com o hardware disponível, o contexto não foi aumentado. O modo de thinking foi desabilitado e a chamada de função do Open WebUI foi configurada como Legado.

Outra dificuldade foi garantir uma coleta consistente das métricas. Por isso, foram utilizados scripts Python para automatizar a medição de TTFT, tempo total e tokens por segundo, além de um script separado para monitorar CPU, RAM e threads.

## Metodologia da Configuração 3

A metodologia específica da C3 deverá ser acrescentada pelo responsável por essa configuração, mantendo o mesmo padrão de documentação e indicando claramente qual variável foi alterada.
