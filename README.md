# SO_UFS_2026_2_Costa_Enzo_Godoy_Filipe

## Equipe Gemma - Sistemas Operacionais 2026.2 - Ollama + Open WebUI

**Disciplina:** Sistemas Operacionais — Atividade 1 (AV1) — 2026.2

| * | Integrante |
|---|---|
| 01 | Enzo Emanuel Maia Costa |
| 02 | Filipe de Carvalho Godoy |
| 03 | Giulian Fabio Bastos Amorim Lima |
| 04 | José Fagner Silva Junqueira |
| 05 | Katyane dos Santos |
| 06 | Rauany Ingrid Santos de Jesus |
| 07 | Vênisson Cardoso dos Santos |

**Trilha de aplicação:** Trilha A — Chat local com Ollama + Open WebUI

**Modelo selecionado:** `google/gemma-3n-E2B-it` (variante Instruct, formato GGUF, quantização Q4_0, ~2,3B de parâmetros efetivos, licença Apache 2.0) — executado via Ollama (`ollama pull gemma3n:e2b`).

**Objetivo do trabalho:** este repositório documenta a instalação e execução local de uma aplicação de IA generativa (Ollama + Open WebUI), relacionando processos, threads, chamadas de sistema e uso de recursos (CPU, memória, armazenamento) do ambiente Linux ao comportamento observado do sistema sob diferentes configurações de carga, concorrência e execução.

## Vídeo da atividade
🔗 **URL:** *Ainda gravando! O link entra aqui assim que estiver pronto — a versão mais atual sempre está em [VIDEO.md](./VIDEO.md).*

## Informações relevantes
- [Contribuição Individual](./equipe/contribuicoes.md)
- [Declaração de Uso de IA](./equipe/uso-de-ia.md)
- [Registro do modelo no Google Classroom](./contexto/registro-classroom.md)

## Organização do material
Dividimos o trabalho seguindo as partes da atividade (A, B e C do enunciado):

```
.
├── contexto/
│   ├── inventario-ambiente.md     → SO, kernel, CPU, RAM, GPU, disco, versões (Parte A, 6.1)
│   ├── camada-aplicacao.md        → ficha do Open WebUI: repo, licença, commit, dependências (6.2)
│   ├── modelo-huggingface.md      → ficha técnica do modelo: parâmetros, formato, quantização, licença
│   ├── registro-classroom.md      → cópia do registro do modelo/trilha na thread do Classroom
│   └── instalacao.md              → comandos, tempo de download/inicialização, processos criados (6.3)
├── processos-threads-syscalls/
│   ├── processos-threads.md       → PID/PPID, estados, threads, parentesco (Parte B, 7.1)
│   ├── chamadas-sistema.md        → análise das syscalls via strace (7.2)
│   └── evidencias/                → saídas de ps, pstree, htop, strace-resumo.txt
├── experimentos/
│   ├── configuracoes.md           → descrição das 3 configurações comparadas (Parte C, seção 8)
│   ├── metodologia.md             → tamanhos de entrada, repetições, métricas coletadas (8.1, 8.2)
│   ├── resultados/                → tabelas, gráficos e dados brutos das 12+ execuções
│   └── scripts/                   → scripts de execução e medição
├── conclusao/
│   ├── discussao.md                → resposta às questões de análise (seção 9)
│   ├── relacao-com-so.md           → relação explícita com Sistemas Operacionais
│   └── limitacoes.md               → limitações e ameaças à validade
├── equipe/
│   ├── contribuicoes.md            → tabela de contribuição de cada integrante
│   └── uso-de-ia.md                → declaração de uso de IA generativa (ferramenta, prompts, verificação)
└── entrega/
    ├── relatorio-tecnico.pdf       → relatório técnico completo (16 seções)
    └── VIDEO.md                    → link do vídeo, data de gravação, participantes
```

## Evidências
As evidências de processos, threads, chamadas de sistema, consumo de CPU/memória e armazenamento estão em `processos-threads-syscalls/evidencias/` e `experimentos/resultados/`.

## Reprodução dos experimentos
1. Instalar o Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
2. Baixar o modelo: `ollama pull gemma3n:e2b`
3. Subir o Open WebUI (Docker):
   ```
   docker run -d -p 3000:8080 \
     --add-host=host.docker.internal:host-gateway \
     -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
     -v open-webui:/app/backend/data \
     --name open-webui \
     ghcr.io/open-webui/open-webui:main
   ```
4. Acessar `http://localhost:3000` e seguir os scripts em `experimentos/scripts/` para reproduzir as 3 configurações testadas.

## Outras informações
- **Disciplina:** Sistemas Operacionais
- **Período:** 2026.2
- **Data de entrega:** 15/09/2026, 23h59 (repositório + relatório)
- **Apresentação oral:** 16/09/2026
