# Declaração de Uso de IA Generativa — Equipe Gemma

| IA generativa | Finalidade | Prompt utilizado | Saída |
|---|---|---|---|
| Claude | Planejamento geral da atividade a partir do enunciado | "Analise TODO esse documento, e a partir da análise, quero sua ajuda com um roadmap para dividir as atividades entre os membros do time de forma coerente" | Sugeriu a divisão por seções do enunciado (ambiente, camada de aplicação, modelo, processos/threads/syscalls, experimentos) e recomendou tópicos para cada membro do time, além disso, retornou um roteiro dia a dia (instalação, observação de processos/threads/syscalls, experimentos comparativos, relatório, vídeo) |
| Copilot (Github) | Organização da estrutura do repositório no GitHub | "A partir do Roadmap e divisão das tarefas anteriores, me ajude na criação de toda a estrutura de pastas no GitHub, de forma que facilite o trabalho dos membros" | Criou toda a estrutura do repositório, indicou em quais arquivos cada trecho do texto deveria entrar, a partir da pasta `contexto/`, e os comandos `git add`/`commit`/`push` para subir o conteúdo para a branch main do nosso repositório |
| *(Filipe — preencher)* | | | |
| ChatGPT | Identificar modelo ollama | " vboxuser@so2:~$ ollama --version Command 'ollama' not found, but can be installed with: sudo snap install ollama vboxuser@so2:~$ " |ollama --version systemctl is-active ollama|
| *(Fagner — preencher)* | | | |
| *(Katyane — preencher)* | | | |
| Claude | Verificação de informação crítica | “Eu preciso da ficha técnica do modelo 4n-e2b escolhido pela equipe, use esse link: [link do gemma-4-E2B-it-qat-q4_0-gguf] e do modelo gemma-3-E2B e suas principais diferenças para determinar qual o mais indicado para a trilha escolhida pela equipe” | A IA alertou sobre a divergência de família de modelo e refez a ficha técnica com os dados corretos. Apontando o 4-E2B como o mais indicado para a atividade. |
| Claude | Aprofundamento em um critério específico | “Descreva o mais afundo o critério formato exigido na ficha técnica” | Explicação da cadeia de derivação do modelo (checkpoint base → instruct → QAT → conversão GGUF) e da relevância de cada etapa para os conceitos de Sistemas Operacionais (armazenamento, I/O, chamadas de sistema no carregamento) |
| *(Vênisson — preencher)* | | | |
| Copilot | Apoio na escrita/organização do relatório | "Revise esse parágrafo do relatório em pdf do meu grupo, verifique erros de pontuação e duplicidade de palavras" | Solicitado e corrigiu erros de gramática e coesão |
| *(espaço extra — usar se algum integrante usar mais de uma ferramenta)* | | | |

