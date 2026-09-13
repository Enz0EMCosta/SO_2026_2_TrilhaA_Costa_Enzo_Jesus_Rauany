# Chamadas de sistema

## Método

Coleta com `strace` sobre o Ollama 0.34.0 executando
`hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf:latest` (4,3 GB, quantização q4_0), em Ubuntu 24.04.4 LTS
sobre VirtualBox — 4 vCPUs, 7,8 GiB de RAM sem swap, sem GPU. O Ollama roda nativamente como serviço
systemd sob o usuário `ollama`.

Rastrear um processo alheio exigiu contornar o módulo de segurança Yama, que por padrão
(`ptrace_scope = 1`) permite rastrear apenas descendentes diretos:

```bash
sudo sysctl -w kernel.yama.ptrace_scope=0
```

Cinco coletas foram realizadas, cada uma com uma execução do modelo:

| Coleta | Comando | Duração |
|---|---|---|
| Perfil agregado do cliente | `strace -f -c ollama run "$MODELO" "..."` | 5,5 s |
| Comunicação | `strace -f -e trace=network ollama run "$MODELO" "oi"` | ~10 s |
| Carga | `sudo strace -f -e trace=openat,mmap -p <PID>` | ~4 min |
| Dados | `sudo strace -f -e trace=read,pread64,openat -e status=successful -p <PID>` | ~4 min |
| Perfil agregado do daemon | `sudo strace -f -c -p <PID>` | ~20 min |

A flag `-f` é indispensável: o daemon cria um subprocesso `ollama runner` onde ocorre toda a
atividade pesada. Antes de cada coleta de carga foi executado `systemctl restart ollama` — sem isso o
modelo permanece em cache de página e o carregamento não se repete.

**Ressalva.** O strace intercepta cada chamada de sistema, e a lentidão resultante estourou o timeout
interno do Ollama na primeira tentativa (`timed out waiting for llama-server to start`). Foi
necessário elevar `OLLAMA_LOAD_TIMEOUT=30m` via override do systemd. Os tempos absolutos, portanto,
servem para comparação relativa entre syscalls e entre processos, não como medida de desempenho.

## Principais syscalls

| Syscall | Finalidade observada | Frequência ou evidência |
|---|---|---|
| `futex` | Sincronização entre as threads de inferência | 87,44% do tempo no daemon (8.499 chamadas); 66,89% no cliente |
| `accept4` | Daemon bloqueado aguardando conexões do cliente | 11,73% do tempo, 67 chamadas, 2,17 s por chamada |
| `read` | Transferência dos pesos do disco para os buffers | 16.445 no daemon contra 381 no cliente; 4,38 GiB lidos no total |
| `lseek` | Navegação posicional entre tensores do arquivo GGUF | 14.631 no daemon, zero no cliente |
| `mmap` | Alocação de buffers anônimos para pesos e contexto | 214 chamadas; maiores blocos de 2,44 GiB e 999 MiB, todos `MAP_ANONYMOUS` com fd `-1` |
| `openat` | Abertura do manifesto e dos cinco blobs do modelo | 142 no daemon contra 21 no cliente |
| `socket` / `connect` | Abertura do canal cliente→daemon | `connect(4, {sin_port=htons(11434), sin_addr=inet_addr("127.0.0.1")})` = `EINPROGRESS` |
| `epoll_pwait` | Espera assíncrona pela resposta do socket | 14,08% do tempo no cliente, 1.779 chamadas |
| `clone3` / `MAP_STACK` | Criação de threads e suas pilhas | 11 threads pré-existentes + 13 criadas sob demanda; 13 mapeamentos de 8 MiB com `MAP_STACK` |
| `write` | Emissão da resposta token a token e diagnóstico | 2.189 no cliente contra 904 no daemon |

## Interpretação

### O comando rastreado não é quem faz o trabalho

`ollama run` é apenas um cliente HTTP. Quem carrega os pesos e executa a inferência é o daemon
`ollama serve` e seu subprocesso `runner`.

| Métrica | `ollama run` | `ollama serve` |
|---|---|---|
| Chamadas | 11.866 | 54.465 |
| Tempo em syscalls | 5,54 s | 1.241,13 s |
| `read` | 381 | 16.445 |

No cliente, `futex`, `epoll_pwait` e `nanosleep` somam **94,72% do tempo em espera passiva** — ele
bloqueia até a resposta chegar pelo socket. Por isso a coleta cobriu os dois lados: rastrear apenas o
comando produziria um retrato incompleto.

### O carregamento não usa mmap de arquivo

Das 214 chamadas `mmap`, nenhuma mapeia o arquivo de pesos:

```
mmap(NULL, 2616033280, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0)
mmap(NULL, 1047973888, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0)
```

`MAP_ANONYMOUS` indica mapeamento sem arquivo associado, e `-1` ocupa a posição do file descriptor —
quando `mmap` mapeia um arquivo, esse campo recebe o fd correspondente. Os únicos `mmap` com
descritor usam `fd 3` com `MAP_DENYWRITE`, comportamento do carregador dinâmico ao mapear
bibliotecas compartilhadas.

O mecanismo real é: `openat` abre o blob, `mmap` aloca buffers anônimos vazios, `read`/`pread64`
transferem o conteúdo para dentro deles, `lseek` reposiciona entre tensores.

| Descritor | Blob | Bytes lidos | Chamadas |
|---|---|---|---|
| fd 5 | `sha256-fa401b55b07e...` | 3,43 GiB | 5.224 |
| fd 4 | `sha256-021059cce659...` | 0,95 GiB | 6.239 |
| | **Total** | **4,38 GiB** | 11.463 |

O total coincide com os 4,3 GB declarados pelo `ollama list`. A maior leitura individual foi de
1.926.758.400 bytes (1,79 GiB) numa única chamada.

### Memória virtual e restrição de hardware

São reservados cerca de 4,7 GiB de espaço de endereçamento em blocos anônimos, mas as páginas só
ocupam RAM física quando escritas. Numa VM com 7,8 GiB e **sem swap**, isso consome mais de metade da
memória disponível — se a reserva excedesse o total, o processo seria encerrado pelo OOM killer em
vez de paginar para disco.

### Cache de página

Uma coleta com o modelo já residente em memória produziu **56 linhas** de trace; após
`systemctl restart ollama`, o mesmo comando produziu **16.140** — diferença de 288×. Com o modelo em
cache, o daemon releu apenas o manifesto (blocos de 512 e 1024 bytes) e reaproveitou o runner ativo.

Isso explica por que a primeira execução após uma reinicialização é sempre a mais lenta, e é
relevante para a medição de tempo de inicialização: **sem limpar o cache, a medida não reflete o
carregamento real.**

### Comunicação estritamente local

```
socket(AF_INET, SOCK_STREAM|SOCK_CLOEXEC|SOCK_NONBLOCK, IPPROTO_IP) = 4
connect(4, {sa_family=AF_INET, sin_port=htons(11434), sin_addr=inet_addr("127.0.0.1")}, 16) = -1 EINPROGRESS
getsockname(4, {sa_family=AF_INET, sin_port=htons(51914), sin_addr=inet_addr("127.0.0.1")}, [112 => 16]) = 0
```

Socket TCP não-bloqueante, daí o retorno `EINPROGRESS` — que não é erro: a conexão prossegue em
segundo plano e o `epoll_pwait` avisa quando estiver pronta. O `getsockname` revela a porta efêmera
local, confirmando que ambas as pontas estão na mesma máquina. No daemon, `accept4` é a contraparte
exata, bloqueado aguardando conexões.

Toda a comunicação ocorre em loopback: nenhum pacote atravessa a interface de rede física, e prompt e
resposta nunca deixam a máquina.

### O gargalo é sincronização, não I/O

`futex` (*fast userspace mutex*) consome 87,44% do tempo no daemon, com 8.499 chamadas e 545 erros —
`ETIMEDOUT`/`EAGAIN`, timeouts normais de espera, não falhas. Com 4 vCPUs para 13+ threads há
competição real por processador, e o tempo coordenando acesso a recursos compartilhados supera
largamente o tempo gasto lendo disco.

### Registro

O Ollama não gera arquivos de log próprios. O diagnóstico sai por `write` nos descritores 1 e 2,
capturado pelo systemd e acessível via `journalctl -u ollama`. A ausência de `openat` em caminhos sob
`/var/log` confirma que o registro é delegado ao gerenciador de serviços.

### Limitações

O overhead do strace altera o objeto medido, a ponto de quebrar o timeout interno da aplicação. O
ambiente é virtualizado e sem GPU, logo não há chamadas a drivers gráficos — em hardware acelerado o
perfil seria substancialmente diferente. Cada trace cobre uma execução, sem quantificação de
variância. Por fim, ao anexar a um daemon já em execução, as syscalls de inicialização do próprio
serviço não foram capturadas.

## Evidências

Em [`evidencias/`](evidencias/):

| Arquivo | Linhas | Conteúdo |
|---|---|---|
| `ambiente.txt` | 11 | Inventário do ambiente de coleta |
| `strace-resumo-cliente.txt` | 53 | Perfil agregado de `ollama run` |
| `strace-resumo-servidor.txt` | 66 | Perfil agregado de `ollama serve` |
| `strace-rede.txt` | 212 | Socket e connect com argumentos |
| `strace-pesos.txt` | 793 | `openat` nos blobs e `mmap` das alocações |
| `strace-leitura.txt` | 16.140 | Leituras com tamanhos e descritores |
| `maiores-leituras.txt` | 20 | Vinte maiores leituras individuais |
| `sessao-completa.txt` | 349 | Log integral da sessão (`script`) |

Comandos reproduzíveis em
[`../experimentos/scripts/coleta-strace.sh`](../experimentos/scripts/coleta-strace.sh).