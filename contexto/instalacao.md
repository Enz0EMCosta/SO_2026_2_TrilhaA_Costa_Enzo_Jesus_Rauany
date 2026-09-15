# Instalação e Execução — Equipe Gemma

**Aluno:** Enzo Emanuel Maia Costa (202300061901)
**Trilha:** A — Ollama + Open WebUI
**Modelo:** `google/gemma-4-E2B-it-qat-q4_0-gguf` (Gemma 4, variante E2B, Instruct, QAT, GGUF Q4_0)

A equipe documentou dois ambientes de instalação, usados por integrantes diferentes: **WSL2 (Ubuntu 24.04.1 LTS)** e **máquina virtual VirtualBox (Ubuntu)**. Ambos mantêm em comum o runtime Ollama, o modelo Gemma 4 e o sistema Linux, permitindo comparar duas estratégias de virtualização sem alterar o objetivo do experimento (ver inventário completo em [`inventario-ambiente.md`](./inventario-ambiente.md)).

---

## Ambiente A — WSL2 (Ubuntu 24.04.1 LTS)

### 1. Instalação do Ollama

Instalador oficial para Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verificação da instalação e da versão:

```bash
ollama --version
```

### 2. Disponibilização do modelo

```bash
ollama pull hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf:latest
```

### 3. Inicialização do servidor

```bash
ollama serve
```

Esse comando sobe o processo responsável por gerenciar e executar os modelos locais, disponibilizando a API local do Ollama para que os comandos e aplicações (como o Open WebUI) possam se comunicar com o runtime. No ambiente WSL2, o Ollama identificou a execução por CPU e registrou 0 B de VRAM, caracterizando a CPU como o único recurso de processamento disponível para o modelo nesse ambiente.

### 4. Execução inicial pelo terminal

Após a disponibilização do modelo, foi feita uma execução inicial pelo terminal, com o objetivo de verificar se o Ollama consegue carregar o modelo e realizar uma inferência local:

```bash
ollama run hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf:latest
```

Pergunta de teste: **"O que é um Sistema Operacional, resuma em uma frase?"**

O modelo retornou corretamente o significado, confirmando que a instalação e o carregamento do modelo funcionaram nesse ambiente.

### 5. Preparação do Open WebUI

O Open WebUI foi definido como a camada de interface gráfica do sistema, permitindo que o modelo seja utilizado por meio de uma interface de conversação enquanto o Ollama permanece responsável pelo processamento local (detalhes de instalação/configuração do Open WebUI ficam a cargo do tópico do Giulian, em `camada-aplicacao.md`).

---

## Ambiente B — Máquina Virtual (VirtualBox)

### 1. Preparar o Ubuntu

```bash
sudo apt update
sudo apt install -y curl ca-certificates openssh-server
```

### 2. Habilitar o acesso via SSH

```bash
sudo systemctl enable --now ssh
hostname -I
```

Do host Windows:

```bash
ssh vboxuser@IP_DA_VM
```

### 3. Instalar o Docker (para rodar o Open WebUI)

```bash
sudo apt install -y docker.io
sudo systemctl enable --now docker
docker --version
sudo docker run --rm hello-world
```

Nesse ambiente, o Ollama roda nativamente no Ubuntu (fora de contêiner); apenas o Open WebUI roda via Docker.

### 4. Instalar o Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable --now ollama
sudo systemctl status ollama --no-pager
ollama --version
```

### 5. Baixar o modelo

```bash
ollama pull hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf:latest
ollama list
```

Tempo de download registrado: **~7 minutos e 8 segundos**.

### 6. Memória e swap

A VM (4,8 GiB de RAM) apresentou falta de memória na primeira tentativa de execução. Diagnóstico e correção:

```bash
free -h
swapon --show

sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Para persistir após reiniciar, adicionar em `/etc/fstab`:
```
/swapfile none swap sw 0 0
```

### 7. Teste do modelo

```bash
ollama run hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf:latest "Responda em português: o que é um sistema operacional? Use apenas uma frase."
```

Resposta obtida:

> Um sistema operacional é um software essencial que gerencia os recursos do hardware do computador e fornece uma plataforma para a execução de outros programas e aplicações.

A saída trouxe também um bloco de "pensamento" (thinking/reasoning) antes da resposta final — o Gemma 4 é anunciado com modos de raciocínio configuráveis, o que explica esse comportamento.

### 8. Achado: limite de contexto do Ollama

Ao repetir a pergunta já dentro do Open WebUI:

```
{"error":{"code":400,"message":"request (5447 tokens) exceeds the available context size (4096 tokens)",...}}
```

Mesmo o model card do Gemma 4 anunciando janelas de contexto grandes (128K nos modelos pequenos), o Ollama define por padrão um contexto de execução de apenas 4096 tokens (`num_ctx`), a menos que configurado explicitamente. É uma limitação real a documentar — aumentar `num_ctx` sem aumentar a RAM disponível tende a agravar o problema de memória do passo 6.

### 9. Consumo de recursos

```bash
ollama ps
free -h
```

| Item | Resultado |
|---|---|
| Processamento do modelo | 100% CPU |
| Tamanho informado pelo `ollama ps` | 3,9 GB |
| Contexto configurado | 4096 tokens |
| RAM total da VM | 4,8 GiB |
| Swap total | 4,0 GiB |
| Swap em uso na medição | 882 MiB |

---

## Resultados e Conclusão

A partir do inventário e da preparação dos dois ambientes, foi possível estabelecer uma configuração experimental capaz de executar o runtime Ollama e utilizar o modelo definido pela equipe para os experimentos. A utilização de WSL2 e VirtualBox permitiu trabalhar com duas estratégias de virtualização, mantendo como elementos comuns o Ubuntu/Linux, o Ollama e o modelo Gemma, fornecendo uma base para os experimentos posteriores relacionados ao consumo de recursos, tamanho do contexto, quantização e desempenho da inferência. Além da execução pelo terminal, o Open WebUI foi definido como camada de interface gráfica, permitindo que o modelo seja utilizado por meio de uma interface de conversação enquanto o Ollama permanece responsável pelo processamento local.

Em ambos os ambientes foi possível identificar limitações importantes: a execução ocorreu inteiramente via CPU, sem VRAM disponível, com memória disponível relativamente baixa (6,1 GiB no WSL2, 4,8 GiB na VM) e armazenamento do modelo em torno de 4,3 GB. Isso evidencia que armazenamento e, principalmente, memória disponível devem ser considerados centrais na execução local de modelos de linguagem.

A divisão entre WSL2 e máquina virtual permitiu que diferentes integrantes utilizassem configurações distintas sem alterar o objetivo principal do experimento. A preparação do ambiente e o inventário realizado fornecem a infraestrutura e o diagnóstico de limitações necessários para as próximas análises da equipe — especialmente aquelas relacionadas a consumo de memória, impacto do tamanho de contexto, quantização, armazenamento e desempenho da execução local do modelo.
