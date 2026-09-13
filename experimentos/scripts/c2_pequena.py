import urllib.request
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

MODEL = "hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf:latest"
PROMPT = "Explique em 3 frases o que é um sistema operacional."

def executar(numero):
    dados = json.dumps({
        "model": MODEL,
        "prompt": PROMPT,
        "stream": True,
        "think": False
    }).encode("utf-8")

    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=dados,
        headers={"Content-Type": "application/json"}
    )

    inicio = time.perf_counter()
    ttft = None
    final = None

    with urllib.request.urlopen(req, timeout=600) as resposta:
        for linha in resposta:
            obj = json.loads(linha.decode("utf-8"))

            if ttft is None and obj.get("response"):
                ttft = time.perf_counter() - inicio

            if obj.get("done"):
                final = obj

    total = time.perf_counter() - inicio

    eval_count = final.get("eval_count", 0)
    eval_duration = final.get("eval_duration", 0)

    tokens_s = (
        eval_count / (eval_duration / 1e9)
        if eval_duration else 0
    )

    return {
        "req": numero,
        "ttft": ttft,
        "total": total,
        "eval_count": eval_count,
        "prompt_eval_count": final.get("prompt_eval_count"),
        "eval_duration_ns": eval_duration,
        "load_duration_ns": final.get("load_duration"),
        "tokens_s": tokens_s
    }

inicio_lote = time.perf_counter()

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(executar, i) for i in range(1, 4)]

    resultados = []

    for future in as_completed(futures):
        resultados.append(future.result())

tempo_lote = time.perf_counter() - inicio_lote

resultados.sort(key=lambda x: x["req"])

for r in resultados:
    print(f"\nREQUISICAO {r['req']}")
    print(f"TTFT={r['ttft']:.3f} s")
    print(f"TEMPO_TOTAL={r['total']:.3f} s")
    print(f"PROMPT_EVAL_COUNT={r['prompt_eval_count']}")
    print(f"EVAL_COUNT={r['eval_count']}")
    print(f"EVAL_DURATION_NS={r['eval_duration_ns']}")
    print(f"LOAD_DURATION_NS={r['load_duration_ns']}")
    print(f"TOKENS_POR_SEGUNDO={r['tokens_s']:.3f}")

print(f"\nTEMPO_TOTAL_LOTE={tempo_lote:.3f} s")
