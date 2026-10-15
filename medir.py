import time
import random
import csv
import matplotlib.pyplot as plt
from ordenacao import ordenacao_insercao, ordenacao_intercalacao
import sys

# Aumentar limite de recursão para o Merge Sort em listas grandes
sys.setrecursionlimit(2000)

class Rastreador:
    """Classe que envolve um número para contar quantas vezes ele é comparado."""
    comparacoes = 0
    
    def __init__(self, valor):
        self.valor = valor
        
    def __lt__(self, outro):
        Rastreador.comparacoes += 1
        return self.valor < outro.valor
        
    def __gt__(self, outro):
        Rastreador.comparacoes += 1
        return self.valor > outro.valor
        
    @classmethod
    def resetar_contagem(cls):
        cls.comparacoes = 0

def gerar_lista(n):
    return [random.randint(0, 10000) for _ in range(n)]

def medir_algoritmo(algoritmo, n, repeticoes=10, usa_rastreador=True):
    tempos = []
    comparacoes_total = 0
    
    for _ in range(repeticoes):
        lista_original = gerar_lista(n)
        
        if usa_rastreador:
            lista_teste = [Rastreador(x) for x in lista_original]
            Rastreador.resetar_contagem()
        else:
            lista_teste = lista_original.copy()
            
        inicio = time.perf_counter()
        algoritmo(lista_teste)
        fim = time.perf_counter()
        
        tempos.append(fim - inicio)
        if usa_rastreador:
            comparacoes_total += Rastreador.comparacoes
            
    tempo_medio = sum(tempos) / repeticoes
    comparacoes_medias = comparacoes_total // repeticoes if usa_rastreador else 0
    
    return tempo_medio, comparacoes_medias

def main():
    tamanhos = [5, 10, 20, 30, 50, 75, 100, 200, 500, 1000]
    resultados = []
    
    print("Iniciando medições... (Isso pode levar alguns segundos)")
    
    for n in tamanhos:
        t_ins, c_ins = medir_algoritmo(ordenacao_insercao, n)
        t_int, c_int = medir_algoritmo(ordenacao_intercalacao, n)
        t_py, c_py = medir_algoritmo(sorted, n)
        
        resultados.append({
            'n': n,
            'tempo_insercao': t_ins, 'comp_insercao': c_ins,
            'tempo_intercalacao': t_int, 'comp_intercalacao': c_int,
            'tempo_python': t_py, 'comp_python': c_py
        })
        print(f"Medição concluída para n={n}")
        
    # Salvar CSV
    with open('dados.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)
        
    print("dados.csv gerado com sucesso.")

    # Gerar Gráficos
    ns = [r['n'] for r in resultados]
    
    # Gráfico de Tempos
    plt.figure(figsize=(10, 5))
    plt.plot(ns, [r['tempo_insercao'] for r in resultados], marker='o', label='Inserção')
    plt.plot(ns, [r['tempo_intercalacao'] for r in resultados], marker='s', label='Intercalação')
    plt.plot(ns, [r['tempo_python'] for r in resultados], marker='^', label='Python sorted()')
    plt.title('Tempo de Execução vs Tamanho da Lista (n)')
    plt.xlabel('Tamanho da Lista (n)')
    plt.ylabel('Tempo Médio (segundos)')
    plt.legend()
    plt.grid(True)
    plt.savefig('grafico_tempo.png')
    
    # Gráfico de Comparações
    plt.figure(figsize=(10, 5))
    plt.plot(ns, [r['comp_insercao'] for r in resultados], marker='o', label='Inserção')
    plt.plot(ns, [r['comp_intercalacao'] for r in resultados], marker='s', label='Intercalação')
    plt.plot(ns, [r['comp_python'] for r in resultados], marker='^', label='Python sorted()')
    plt.title('Número de Comparações vs Tamanho da Lista (n)')
    plt.xlabel('Tamanho da Lista (n)')
    plt.ylabel('Comparações Médias')
    plt.legend()
    plt.grid(True)
    plt.savefig('grafico_comparacoes.png')
    
    print("Gráficos gerados com sucesso (grafico_tempo.png e grafico_comparacoes.png).")

if __name__ == '__main__':
    main()