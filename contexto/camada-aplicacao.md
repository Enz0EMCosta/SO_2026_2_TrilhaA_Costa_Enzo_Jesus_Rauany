# Camada de aplicação

## Open WebUI
- Repositório: https://github.com/open-webui/open-webui
- Release utilizada/observada: v0.11.3
- Release: https://github.com/open-webui/open-webui/releases/tag/v0.11.3
- Imagem utilizada: ghcr.io/open-webui/open-webui:main
- Licença: Open WebUI License
- Data de acesso: 10/09/2026
- Dependências relevantes: Docker 29.1.3; Ollama 0.34.0; Python; FastAPI/Uvicorn; SvelteKit; SQLite.


## Relação com o Ollama

Descrever como o Open WebUI se comunica com o servidor Ollama.

O Open WebUI foi executado em um contêiner Docker dentro da máquina virtual Ubuntu, enquanto o Ollama foi instalado diretamente no Ubuntu. O Docker fornece o ambiente da aplicação e mantém seus dados em um volume persistente. Utilizamos --network host para compartilhar a rede do Ubuntu com o contêiner e configuramos OLLAMA_BASE_URL=http://127.0.0.1:11434. Dessa forma, o Open WebUI envia as mensagens à API do Ollama, que executa o Gemma e devolve as respostas para exibição no navegador.
