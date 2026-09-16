# Configurações dos experimentos

## Ambiente utilizado

- Sistema hospedeiro: Windows 11
- Ambiente Linux: WSL2 com Ubuntu
- Processador: Intel Core i5-12450H
- Hardware: 8 núcleos / 12 processadores lógicos
- Memória RAM física: 8 GB DDR4
- Armazenamento: SSD NVMe
- Limite configurado para o WSL2: 5 GB de RAM
- Processadores disponibilizados ao WSL2: 8
- Swap configurada no WSL2: 4 GB
- Ollama: 0.34.0
- Interface: Open WebUI
- Contexto utilizado: 4096 tokens

## Modelo

- Modelo: google/gemma-4-E2B-it-qat-q4_0-gguf
- Modelo no Ollama: hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf:latest
- Quantização: Q4_0
- Execução: local, utilizando Ollama
- API: http://127.0.0.1:11434/api/generate
- Streaming: habilitado para medição do TTFT
- Thinking: desabilitado nos testes
- Open WebUI: chamada de função configurada como Legado

## Configuração 1 — C1: execução padrão

- Descrição: configuração de referência (baseline), executando uma requisição por vez.
- Modelo e quantização: Gemma 4 E2B / Q4_0 GGUF.
- Concorrência: 1 requisição.
- Entrada pequena: prompt com 22 tokens.
- Entrada grande: prompt com 120 tokens.
- Repetições: 2 para cada tamanho de carga.
- Inicialização: o modelo foi parado antes de cada repetição para manter a condição de cold start.
- Recursos relevantes: CPU, RAM, threads, TTFT, tempo total e tokens por segundo.

## Configuração 2 — C2: concorrência

- Descrição: avaliação do comportamento do sistema com múltiplas requisições concorrentes.
- Modelo e quantização: Gemma 4 E2B / Q4_0 GGUF.
- Concorrência: 3 requisições simultâneas.
- Implementação da concorrência: Python com ThreadPoolExecutor(max_workers=3).
- Entrada pequena: mesmo prompt de 22 tokens utilizado na C1.
- Entrada grande: mesmo prompt de 120 tokens utilizado na C1.
- Repetições: 2 lotes para cada tamanho de carga.
- Cada lote: 3 requisições simultâneas.
- Inicialização: o modelo foi parado antes de cada repetição para manter a condição de cold start.
- Recursos relevantes: CPU, RAM, threads, TTFT, tempo individual, tempo total do lote e tokens por segundo.

## Controle experimental C1 x C2

Entre C1 e C2 foram mantidos o mesmo modelo, quantização, contexto, hardware, ambiente e prompts. O principal fator alterado foi a concorrência: uma requisição na C1 e três requisições simultâneas na C2.

As métricas de CPU, RAM e threads foram obtidas em execuções adicionais de monitoramento e, portanto, são mantidas separadas das duas repetições oficiais utilizadas para as métricas de desempenho.

## Configuração 3 — C3: ajuste da janela de contexto

- Descrição: comparação do impacto da janela de contexto configurada no desempenho da inferência local.
- Ambiente: Ubuntu 24.04.4 LTS em máquina virtual Oracle VirtualBox.
- Modelo: google/gemma-4-E2B-it-qat-q4_0-gguf.
- Modelo no Ollama: hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf:latest.
- Quantização: Q4_0.
- Execução: somente em CPU.
- Concorrência: 1 requisição por vez.
- Contexto curto: num_ctx = 1024.
- Contexto longo: num_ctx = 4096.
- Prompt: "Explique em uma frase o que é um sistema operacional."
- Thinking: desabilitado.
- Streaming: desabilitado.
- keep_alive: 0, descarregando o modelo após cada requisição.
- Variável alterada: tamanho da janela de contexto.
- Variáveis mantidas: modelo, prompt, ambiente e quantização.
- Recursos e métricas relevantes: tempo total, tempo de carregamento, tempo de geração, tokens por segundo e ocorrência de timeout.
