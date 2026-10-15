
import csv
import random
import time
import math
import matplotlib.pyplot as plt

from ordenacao import ordenacao_insercao, ordenacao_intercalacao


TAMANHOS = [5, 10, 20, 30, 50, 75, 100, 200, 500, 1000]
REPETICOES = 10


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
    resultados = []

    for n in TAMANHOS:
        tempos_insercao = []
        tempos_intercalacao = []
        tempos_sorted = []

        comparacoes_insercao = []
        comparacoes_intercalacao = []
        comparacoes_sorted = []

        for repeticao in range(REPETICOES):
            lista = [random.randint(0, 10000) for i in range(n)]

            # Ordenacao por insercao
            inicio = time.perf_counter()
            _, comp = ordenacao_insercao(lista)
            fim = time.perf_counter()

            tempos_insercao.append(fim - inicio)
            comparacoes_insercao.append(comp)

            # Ordenacao por intercalacao
            inicio = time.perf_counter()
            _, comp = ordenacao_intercalacao(lista)
            fim = time.perf_counter()

            tempos_intercalacao.append(fim - inicio)
            comparacoes_intercalacao.append(comp)

            # sorted() do Python
            inicio = time.perf_counter()
            sorted(lista)
            fim = time.perf_counter()

            tempos_sorted.append(fim - inicio)

            # Comparacoes do sorted()
            NumeroContador.comparacoes = 0
            lista_contador = [NumeroContador(valor) for valor in lista]
            sorted(lista_contador)

            comparacoes_sorted.append(NumeroContador.comparacoes)

        linha = {
            "n": n,
            "tempo_insercao": sum(tempos_insercao) / REPETICOES,
            "tempo_intercalacao": sum(tempos_intercalacao) / REPETICOES,
            "tempo_sorted": sum(tempos_sorted) / REPETICOES,
            "comparacoes_insercao": sum(comparacoes_insercao) / REPETICOES,
            "comparacoes_intercalacao": sum(comparacoes_intercalacao) / REPETICOES,
            "comparacoes_sorted": sum(comparacoes_sorted) / REPETICOES
        }

        resultados.append(linha)

        print("Tamanho:", n, "- medições concluídas")

    return resultados


def salvar_csv(resultados):
    with open("dados.csv", "w", newline="", encoding="utf-8") as arquivo:
        campos = resultados[0].keys()
        escritor = csv.DictWriter(arquivo, fieldnames=campos)

        escritor.writeheader()
        escritor.writerows(resultados)


def gerar_graficos(resultados):
    tamanhos = [r["n"] for r in resultados]

    plt.figure()
    plt.plot(tamanhos, [r["tempo_insercao"] for r in resultados],
             marker="o", label="Inserção")
    plt.plot(tamanhos, [r["tempo_intercalacao"] for r in resultados],
             marker="o", label="Intercalação")
    plt.plot(tamanhos, [r["tempo_sorted"] for r in resultados],
             marker="o", label="sorted()")
    plt.xlabel("Tamanho da lista (n)")
    plt.ylabel("Tempo médio (segundos)")
    plt.title("Comparação dos tempos de ordenação")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("tempos.png")
    plt.close()

    plt.figure()
    plt.plot(tamanhos, [r["comparacoes_insercao"] for r in resultados],
             marker="o", label="Inserção")
    plt.plot(tamanhos, [r["comparacoes_intercalacao"] for r in resultados],
             marker="o", label="Intercalação")
    plt.plot(tamanhos, [r["comparacoes_sorted"] for r in resultados],
             marker="o", label="sorted()")
    plt.xlabel("Tamanho da lista (n)")
    plt.ylabel("Número médio de comparações")
    plt.title("Comparação das comparações")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("comparacoes.png")
    plt.close()


def mostrar_tabelas(resultados):
    print("\nRESULTADOS")
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
            f'sorted(): {r["comparacoes_sorted"]:.2f}'
        )


if __name__ == "__main__":
    resultados = medir()
    salvar_csv(resultados)
    gerar_graficos(resultados)
    mostrar_tabelas(resultados)

    print("\nArquivos gerados: dados.csv, tempos.png e comparacoes.png")
