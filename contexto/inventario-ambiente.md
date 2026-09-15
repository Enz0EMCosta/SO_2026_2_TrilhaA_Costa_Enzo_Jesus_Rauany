# Inventário do Ambiente Experimental — Equipe Gemma

**Responsável:** Enzo Emanuel Maia Costa (202300061901)
**Modelo analisado:** `google/gemma-4-E2B-it-qat-q4_0-gguf`

## Tarefa

Preparar e documentar o ambiente experimental utilizado pela equipe para a execução local do modelo de linguagem, realizando o inventário dos recursos computacionais, a instalação e configuração do Ollama, o download e a execução inicial do modelo, além da preparação do Open WebUI como interface de interação. Também faz parte da tarefa registrar as características do ambiente e identificar suas limitações de hardware, especialmente em relação à CPU, memória RAM, armazenamento e disponibilidade de GPU.

## Análise da tarefa

A atividade foi desenvolvida considerando duas configurações de ambiente utilizadas pelos integrantes da equipe: parte do grupo realizou a preparação utilizando **WSL2, com Ubuntu 24.04.1 LTS**, enquanto outra parte utilizou uma **máquina virtual através do VirtualBox**, também com ambiente Linux (detalhes de instalação em [`instalacao.md`](./instalacao.md)). A utilização dessas duas abordagens permitiu executar o mesmo modelo e runtime em ambientes distintos, possibilitando observar como diferentes formas de disponibilização do ambiente e de alocação de recursos podem influenciar a execução local de modelos de linguagem.

A análise do ambiente é importante porque a execução local de modelos depende diretamente dos recursos computacionais disponíveis: a quantidade de RAM, por exemplo, influencia a capacidade de carregar o modelo e manter o contexto da interação, enquanto a disponibilidade de GPU pode alterar significativamente o desempenho da inferência.

## Ambiente de referência para o inventário: WSL2 (Ubuntu 24.04.1 LTS)

| Item | Valor observado |
|---|---|
| Processador | Intel Core i5-8265U |
| Núcleos físicos | 4 |
| Threads | 8 |
| RAM disponível | ~6,1 GiB |
| Swap configurado | 2 GiB |
| GPU / VRAM | Não disponível — 0 B (execução via CPU) |
| Armazenamento ocupado pelo modelo | ~4,3 GB |

Durante a inicialização do Ollama, o runtime identificou a execução utilizando CPU, com 0 B de VRAM disponível para o processo de inferência — ou seja, todo o processamento é feito pelo processador, sem aceleração por placa de vídeo.

## Comandos utilizados

| Comando | O que verifica |
|---|---|
| `cat /etc/os-release` | Distribuição Linux instalada |
| `uname -a` | Kernel, arquitetura e demais características do sistema |
| `lscpu` | Modelo da CPU, núcleos, threads, arquitetura, frequência |
| `nproc` | Quantidade de processadores lógicos disponíveis |
| `free -h` | RAM total, em uso e swap configurado (formato legível: MiB/GiB) |
| `df -h` | Capacidade, uso e espaço disponível nos sistemas de arquivos |
| `lsblk` | Discos reconhecidos pelo sistema |
| `nvidia-smi` | Disponibilidade e uso de GPU NVIDIA (modelo, VRAM), quando aplicável |

### Saídas coletadas (evidências)

> Colar abaixo a saída bruta de cada comando rodado no ambiente WSL2, em blocos de código. Exemplo:

```
$ uname -a
[COLAR SAÍDA AQUI]

$ lscpu
[COLAR SAÍDA AQUI]

$ free -h
[COLAR SAÍDA AQUI]

$ df -h
[COLAR SAÍDA AQUI]

$ lsblk
[COLAR SAÍDA AQUI]
```

(Os mesmos comandos, rodados no ambiente VirtualBox, estão documentados junto ao passo a passo de instalação em `instalacao.md`.)

## Observações e limitações

O ambiente WSL2 analisado possui recursos modestos para execução local de modelos de linguagem: RAM disponível de aproximadamente 6,1 GiB, ausência de GPU dedicada (execução via CPU) e swap de apenas 2 GiB. O modelo instalado ocupa aproximadamente 4,3 GB de armazenamento. Isso evidencia que tanto a capacidade de armazenamento quanto, principalmente, a memória disponível, devem ser consideradas como fatores limitantes na execução de modelos locais — o que impacta diretamente as configurações experimentais que serão testadas nas próximas etapas do trabalho (consumo de memória, tamanho de contexto, quantização e desempenho).
