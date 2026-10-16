import csv
import math
import random
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from ordenacao import ordenacao_insercao, ordenacao_intercalacao


BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_CSV = BASE_DIR / "dados.csv"
ARQUIVO_TEMPOS = BASE_DIR / "tempos.png"
ARQUIVO_COMPARACOES = BASE_DIR / "comparacoes.png"

TAMANHOS = [5, 10, 20, 30, 50, 75, 100, 200, 500, 1000]
REPETICOES = 50
SEMENTE = 42


class NumeroContador:
    comparacoes = 0

    def __init__(self, valor):
        self.valor = valor

    def __lt__(self, outro):
        NumeroContador.comparacoes += 1
        return self.valor < outro.valor


def medir_tempo(funcao, lista):
    inicio = time.perf_counter()
    funcao(lista)
    fim = time.perf_counter()
    return fim - inicio


def medir():
    random.seed(SEMENTE)
    resultados = []

    for n in TAMANHOS:
        tempos_insercao = []
        tempos_intercalacao = []
        tempos_sorted = []

        comparacoes_insercao = []
        comparacoes_intercalacao = []
        comparacoes_sorted = []

        for _ in range(REPETICOES):
            lista = [random.randint(0, 10000) for _ in range(n)]

            inicio = time.perf_counter()
            _, comp = ordenacao_insercao(lista)
            tempos_insercao.append(time.perf_counter() - inicio)
            comparacoes_insercao.append(comp)

            inicio = time.perf_counter()
            _, comp = ordenacao_intercalacao(lista)
            tempos_intercalacao.append(time.perf_counter() - inicio)
            comparacoes_intercalacao.append(comp)

            tempos_sorted.append(medir_tempo(sorted, lista))

            NumeroContador.comparacoes = 0
            sorted([NumeroContador(valor) for valor in lista])
            comparacoes_sorted.append(NumeroContador.comparacoes)

        media = lambda valores: sum(valores) / len(valores)

        resultados.append({
            "n": n,
            "tempo_insercao": media(tempos_insercao),
            "tempo_intercalacao": media(tempos_intercalacao),
            "tempo_sorted": media(tempos_sorted),
            "comparacoes_insercao": media(comparacoes_insercao),
            "comparacoes_intercalacao": media(comparacoes_intercalacao),
            "comparacoes_sorted": media(comparacoes_sorted),
            "n_log2_n": n * math.log2(n),
        })

        print(f"n = {n:4d} - medições concluídas")

    return resultados


def salvar_csv(resultados):
    with open(ARQUIVO_CSV, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=resultados[0].keys())
        escritor.writeheader()
        escritor.writerows(resultados)


CORES = {
    "insercao": "#E63946",
    "intercalacao": "#1D3557",
    "sorted": "#2A9D8F",
    "referencia": "#8D99AE",
    "fundo": "#FBFCFE",
    "grade": "#C7CDD6",
    "texto": "#212529",
    "subtexto": "#6C757D",
}

SERIES = [
    ("tempo_insercao", "comparacoes_insercao", "insercao", "Inserção", "o"),
    ("tempo_intercalacao", "comparacoes_intercalacao", "intercalacao", "Intercalação", "s"),
    ("tempo_sorted", "comparacoes_sorted", "sorted", "sorted()", "^"),
]


def _preparar_eixos(fig, ax, titulo, subtitulo, xlabel, ylabel, rotulos_x):
    fig.patch.set_facecolor("white")
    ax.set_facecolor(CORES["fundo"])

    ax.grid(True, which="major", linestyle="--", linewidth=0.7,
            color=CORES["grade"], alpha=0.75)
    ax.grid(True, which="minor", linestyle=":", linewidth=0.4,
            color=CORES["grade"], alpha=0.45)
    ax.set_axisbelow(True)

    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(CORES["grade"])
        ax.spines[lado].set_linewidth(1.2)

    ax.tick_params(colors=CORES["texto"], labelsize=10)
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda y, _: f"{y:,.0f}" if y >= 1 else f"{y:g}")
    )

    ax.set_xticks(range(len(rotulos_x)))
    ax.set_xticklabels(rotulos_x)
    ax.set_xlabel(xlabel, fontsize=12, color=CORES["texto"], labelpad=8)
    ax.set_ylabel(ylabel, fontsize=12, color=CORES["texto"], labelpad=8)

    fig.suptitle(titulo, fontsize=17, fontweight="bold",
                 color=CORES["intercalacao"], x=0.5, y=0.975)
    fig.text(0.5, 0.915, subtitulo, ha="center", va="top", fontsize=10,
             color=CORES["subtexto"], style="italic")
    fig.subplots_adjust(left=0.085, right=0.97, top=0.85, bottom=0.10)


def _legenda(ax):
    ax.legend(loc="upper left", fontsize=11, frameon=True, facecolor="white",
              edgecolor=CORES["grade"], shadow=True, borderpad=0.8,
              labelspacing=0.7)


def gerar_graficos(resultados):
    tamanhos = [r["n"] for r in resultados]
    rotulos_x = [str(n) for n in tamanhos]
    base_x = list(range(len(tamanhos)))

    fig, ax = plt.subplots(figsize=(11, 6.5))
    minimo = min(r["tempo_sorted"] for r in resultados) * 1e6
    maximo = max(r["tempo_insercao"] for r in resultados) * 1e6

    for chave, _, cor, rotulo, marcador in SERIES:
        valores = [r[chave] * 1e6 for r in resultados]
        ax.plot(base_x, valores, marker=marcador, markersize=8, linewidth=2.6,
                color=CORES[cor], label=rotulo, markeredgecolor="white",
                markeredgewidth=1.2, zorder=3)
        ax.fill_between(base_x, minimo * 0.4, valores, color=CORES[cor],
                        alpha=0.07, zorder=1)

    ax.set_yscale("log")
    ax.set_ylim(minimo * 0.4, maximo * 1.7)
    _preparar_eixos(
        fig, ax,
        "Tempo de execução dos algoritmos de ordenação",
        f"Média de {REPETICOES} execuções por tamanho · eixo y em escala logarítmica (µs)",
        "Tamanho da lista (n)", "Tempo médio (µs)", rotulos_x,
    )

    idx = next((i for i, r in enumerate(resultados)
                if r["tempo_intercalacao"] < r["tempo_insercao"]), None)
    if idx is not None:
        ax.axvline(idx, color=CORES["referencia"], linestyle="--",
                   linewidth=1.3, alpha=0.9, zorder=2)
        ax.annotate(
            f"intercalação mais rápida\na partir de n = {tamanhos[idx]}",
            xy=(idx, minimo * 0.55), xytext=(idx - 1.5, minimo * 2.2),
            fontsize=9.5, color=CORES["subtexto"], ha="right",
            arrowprops=dict(arrowstyle="->", color=CORES["referencia"], lw=1.2),
        )

    razao = resultados[-1]["tempo_insercao"] / resultados[-1]["tempo_intercalacao"]
    ax.text(0.98, 0.05,
            f"Em n = {tamanhos[-1]}, a intercalação é\n~{razao:.1f}× mais rápida que a inserção",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=10,
            color=CORES["intercalacao"],
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                      edgecolor=CORES["grade"], alpha=0.95))
    _legenda(ax)
    fig.savefig(ARQUIVO_TEMPOS, dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 6.5))
    minimo = min(r["comparacoes_sorted"] for r in resultados)
    maximo = max(r["comparacoes_insercao"] for r in resultados)

    for _, chave, cor, rotulo, marcador in SERIES:
        valores = [r[chave] for r in resultados]
        ax.plot(base_x, valores, marker=marcador, markersize=8, linewidth=2.6,
                color=CORES[cor], label=rotulo, markeredgecolor="white",
                markeredgewidth=1.2, zorder=3)
        ax.fill_between(base_x, minimo * 0.4, valores, color=CORES[cor],
                        alpha=0.07, zorder=1)

    ax.plot(base_x, [r["n_log2_n"] for r in resultados], linestyle="--",
            linewidth=2.0, color=CORES["referencia"],
            label="n·log₂n (referência)", zorder=2)

    ax.set_yscale("log")
    ax.set_ylim(minimo * 0.4, maximo * 1.7)
    _preparar_eixos(
        fig, ax,
        "Número de comparações dos algoritmos de ordenação",
        f"Média de {REPETICOES} execuções por tamanho · eixo y em escala logarítmica",
        "Tamanho da lista (n)", "Número médio de comparações", rotulos_x,
    )
    ax.text(0.98, 0.05,
            "A intercalação e o sorted() crescem\ncomo n·log₂n; a inserção, como n²",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=10,
            color=CORES["intercalacao"],
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                      edgecolor=CORES["grade"], alpha=0.95))
    _legenda(ax)
    fig.savefig(ARQUIVO_COMPARACOES, dpi=200)
    plt.close(fig)


def mostrar_tabelas(resultados):
    print("\nTEMPOS MÉDIOS")
    for r in resultados:
        print(
            f'n={r["n"]:4} | '
            f'Inserção: {r["tempo_insercao"]:.8f}s | '
            f'Intercalação: {r["tempo_intercalacao"]:.8f}s | '
            f'sorted(): {r["tempo_sorted"]:.8f}s'
        )

    print("\nCOMPARAÇÕES MÉDIAS")
    for r in resultados:
        print(
            f'n={r["n"]:4} | '
            f'Inserção: {r["comparacoes_insercao"]:.2f} | '
            f'Intercalação: {r["comparacoes_intercalacao"]:.2f} | '
            f'sorted(): {r["comparacoes_sorted"]:.2f} | '
            f'n log2 n: {r["n_log2_n"]:.2f}'
        )


if __name__ == "__main__":
    resultados = medir()
    salvar_csv(resultados)
    gerar_graficos(resultados)
    mostrar_tabelas(resultados)

    print(f"\nArquivos gerados: {ARQUIVO_CSV.name}, "
          f"{ARQUIVO_TEMPOS.name} e {ARQUIVO_COMPARACOES.name}")
