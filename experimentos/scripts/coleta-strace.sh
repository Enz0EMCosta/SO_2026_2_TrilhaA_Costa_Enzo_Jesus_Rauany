#!/usr/bin/env bash
# Coleta de chamadas de sistema — seção de syscalls
# Autor: Filipe de Carvalho Godoy
# Ambiente: Ubuntu 24.04.4 LTS (VM), Ollama 0.34.0 nativo, 4 vCPUs, 7,8 GiB RAM, sem GPU
#
# Uso: execute os blocos manualmente, em duas janelas de terminal.
# Os traces com -p ficam bloqueados aguardando atividade e precisam de
# Ctrl+C após a inferência terminar na outra janela.

MODELO="hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf:latest"
SAIDA="$HOME/strace"

# ---------------------------------------------------------------
# Pré-requisitos
# ---------------------------------------------------------------
# Yama LSM restringe ptrace a descendentes diretos por padrão (scope=1).
# Anexar a um processo já em execução exige scope=0.
sudo apt install -y strace
sudo sysctl -w kernel.yama.ptrace_scope=0
mkdir -p "$SAIDA" && cd "$SAIDA"

# O strace impõe overhead suficiente para estourar o timeout interno do
# Ollama durante o carregamento dos 4,3 GB. Sem este override, a coleta
# falha com "timed out waiting for llama-server to start".
sudo systemctl edit ollama
#   [Service]
#   Environment="OLLAMA_LOAD_TIMEOUT=30m"
sudo systemctl daemon-reload

# Inventário do ambiente
{ uname -a; free -h; nproc; df -h /; ollama --version; ollama list; \
  sysctl kernel.yama.ptrace_scope; } | tee ambiente.txt

# ---------------------------------------------------------------
# 1. Perfil agregado do cliente
# ---------------------------------------------------------------
strace -f -c -o strace-resumo-cliente.txt \
  ollama run "$MODELO" "Explique em uma frase o que e um processo."

# ---------------------------------------------------------------
# 2. Comunicação — socket/connect com argumentos visíveis
# ---------------------------------------------------------------
strace -f -e trace=network -o strace-rede.txt ollama run "$MODELO" "oi"
grep -E "socket|connect|getsockname" strace-rede.txt

# ---------------------------------------------------------------
# 3. Carga — openat nos blobs e mmap das alocações
# ---------------------------------------------------------------
# O restart é obrigatório: sem ele o modelo permanece em cache de página
# e o carregamento não se repete (56 linhas de trace contra 16.140).
sudo systemctl restart ollama && sleep 3 && pgrep -a ollama   # anotar o PID

# janela 1 — anexa ao daemon (-f segue o subprocesso "ollama runner")
sudo strace -f -e trace=openat,mmap -o strace-pesos.txt -p <PID>
# janela 2 — dispara a inferência
ollama run "$MODELO" "Explique o que e mmap."
# janela 1 — Ctrl+C após a resposta

grep -E "blobs|gguf" strace-pesos.txt | head -20
grep "mmap" strace-pesos.txt | tail -20

# ---------------------------------------------------------------
# 4. Dados — leituras com tamanhos e descritores
# ---------------------------------------------------------------
sudo systemctl restart ollama && sleep 3 && pgrep -a ollama   # PID novo

# janela 1
sudo strace -f -e trace=read,pread64,openat -e status=successful \
  -o strace-leitura.txt -p <PID>
# janela 2
ollama run "$MODELO" "ok"
# janela 1 — Ctrl+C

# vinte maiores leituras individuais
grep -E "read\(|pread64\(" strace-leitura.txt | awk '{print $NF}' \
  | sort -n | tail -20 > maiores-leituras.txt

# total de bytes por descritor
grep -oE "read\(5, .*\) = [0-9]+" strace-leitura.txt \
  | awk '{s+=$NF} END {printf "fd 5: %.2f GiB em %d chamadas\n", s/1073741824, NR}'
grep -oE "read\(4, .*\) = [0-9]+" strace-leitura.txt \
  | awk '{s+=$NF} END {printf "fd 4: %.2f GiB em %d chamadas\n", s/1073741824, NR}'

# ---------------------------------------------------------------
# 5. Perfil agregado do daemon
# ---------------------------------------------------------------
sudo systemctl restart ollama && sleep 3 && pgrep -a ollama   # PID novo

# janela 1
sudo strace -f -c -o strace-resumo-servidor.txt -p <PID>
# janela 2
ollama run "$MODELO" "ok"
# janela 1 — Ctrl+C

cat strace-resumo-servidor.txt