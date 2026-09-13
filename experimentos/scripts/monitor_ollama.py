import subprocess
import time
import csv
import os
from datetime import datetime

ARQUIVO = "/tmp/monitor_ollama.csv"
INTERVALO = 1.0

def encontrar_pid():
    try:
        saida = subprocess.check_output(
            ["pgrep", "-f", "/usr/local/lib/ollama/llama-server"],
            text=True
        ).strip()

        if not saida:
            return None

        return saida.splitlines()[0]

    except subprocess.CalledProcessError:
        return None

def coletar(pid):
    try:
        saida = subprocess.check_output(
            [
                "ps",
                "-p", pid,
                "-o", "%cpu=,%mem=,rss=,nlwp="
            ],
            text=True
        ).strip()

        if not saida:
            return None

        partes = saida.split()

        return {
            "cpu": float(partes[0]),
            "mem_percent": float(partes[1]),
            "rss_kb": int(partes[2]),
            "threads": int(partes[3])
        }

    except Exception:
        return None

novo_arquivo = not os.path.exists(ARQUIVO)

with open(ARQUIVO, "a", newline="") as f:
    writer = csv.writer(f)

    if novo_arquivo:
        writer.writerow([
            "timestamp",
            "pid",
            "cpu_percent",
            "mem_percent",
            "rss_kb",
            "threads"
        ])

    print("Monitor iniciado.")
    print("Arquivo:", ARQUIVO)
    print("Pressione Ctrl+C para encerrar.")

    try:
        while True:
            pid = encontrar_pid()

            if pid:
                dados = coletar(pid)

                if dados:
                    agora = datetime.now().isoformat(timespec="seconds")

                    writer.writerow([
                        agora,
                        pid,
                        dados["cpu"],
                        dados["mem_percent"],
                        dados["rss_kb"],
                        dados["threads"]
                    ])

                    f.flush()

                    print(
                        f"{agora} "
                        f"PID={pid} "
                        f"CPU={dados['cpu']}% "
                        f"RAM={dados['rss_kb']/1024:.1f} MB "
                        f"THREADS={dados['threads']}"
                    )

            time.sleep(INTERVALO)

    except KeyboardInterrupt:
        print("\nMonitor encerrado.")
