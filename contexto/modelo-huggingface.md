# Modelo Hugging Face

- Nome: `google/gemma-4-E2B-it-qat-q4_0-gguf`
- Repositório: https://huggingface.co/google/gemma-4-E2B-it-qat-q4_0-gguf
- Parâmetros: aproximadamente 2,3 bilhões de parâmetros efetivos; cerca de 5,1 bilhões considerando as camadas de embedding (PLE)
- Formato: GGUF
- Quantização: Q4_0, derivada de Quantization-Aware Training (QAT)
- Licença: Apache 2.0
- Variante utilizada no Ollama: `hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf:latest`

## Observações

As informações técnicas foram obtidas principalmente a partir do model card oficial do modelo no Hugging Face e confrontadas com as características observadas no ambiente experimental da equipe.

O arquivo Q4_0 é informado na página do Hugging Face com aproximadamente 3,35 GB. No ambiente utilizado pela equipe, a variante disponibilizada pelo Ollama ocupou aproximadamente 4,3 GB. Essa diferença foi mantida no registro porque o tamanho informado no repositório do modelo não representa necessariamente todo o espaço ocupado pela variante no ambiente do Ollama.

O modelo possui janela de contexto máxima informada de até 128 mil tokens. Entretanto, devido às limitações de memória e processamento dos ambientes utilizados pela equipe, os experimentos foram realizados com valores menores, incluindo 1024 e 4096 tokens.

A execução utilizada nos experimentos foi realizada em CPU, sem depender de GPU para a inferência.
