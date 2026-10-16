# Relatório: Comparação de Algoritmos de Ordenação

## 1. Objetivo

Implementar e comparar dois algoritmos de ordenação — **ordenação por inserção**
(*Insertion Sort*) e **ordenação por intercalação** (*Merge Sort*) — e usar a
função `sorted()` do Python como referência. Para cada tamanho de lista foram
medidos o **tempo médio de execução** e o **número médio de comparações**.

## 2. Metodologia

- Tamanhos testados: **n = 5, 10, 20, 30, 50, 75, 100, 200, 500 e 1000**.
- Para cada tamanho foram geradas **50 listas aleatórias** (`REPETICOES = 50`,
  acima do mínimo de 10) e calculada a **média**.
- Os valores aleatórios ficam entre 0 e 10000. A semente é fixa
  (`SEMENTE = 42`), de modo que as listas e o número de comparações são
  reproduzíveis.
- O tempo foi medido com `time.perf_counter()`, executando o algoritmo uma vez
  por lista. A tabela mostra o tempo em **microssegundos (µs)**; o `dados.csv`
  guarda o valor bruto em segundos.
- As comparações dos dois algoritmos implementados são contadas durante a
  própria execução.
- As comparações de `sorted()` foram contadas com uma classe `NumeroContador`
  que registra cada chamada de `__lt__` (o operador `<` usado pelo Timsort).

Duas ressalvas importantes:

1. Em listas pequenas os tempos são de poucos microssegundos, então diferenças
   de tempo menores que ~5% devem ser lidas como **empate dentro do ruído**,
   não como vantagem real de um algoritmo.
2. O **tempo** varia um pouco de execução para execução (carga da máquina, cache,
   frequência da CPU). O **número de comparações**, por outro lado, é exato para
   a mesma semente. A tabela de tempos corresponde à execução que gerou o
   `dados.csv` entregue.

## 3. Tabela de tempos médios

Tempos em **microssegundos (µs)** — 1 µs = 10⁻⁶ s.

| n | Inserção (µs) | Intercalação (µs) | `sorted()` (µs) |
|---:|---:|---:|---:|
| 5 | **3,83** | 9,67 | 1,31 |
| 10 | **6,19** | 18,70 | 1,77 |
| 20 | **16,89** | 41,05 | 2,95 |
| 30 | **35,70** | 71,42 | 3,75 |
| 50 | **83,25** | 85,43 | 5,08 |
| 75 | 168,25 | **137,71** | 7,74 |
| 100 | 254,39 | **151,74** | 8,54 |
| 200 | 1028,79 | **355,30** | 19,09 |
| 500 | 7116,93 | **950,76** | 53,89 |
| 1000 | 29690,56 | **2089,26** | 118,23 |

Em **negrito**, o menor tempo entre os dois algoritmos implementados.

## 4. Tabela de comparações médias

| n | Inserção | Intercalação | `sorted()` | n·log₂n |
|---:|---:|---:|---:|---:|
| 5 | 7,76 | **7,12** | 8,98 | 11,61 |
| 10 | 28,96 | **22,44** | 24,16 | 33,22 |
| 20 | 114,82 | **63,46** | 64,16 | 86,44 |
| 30 | 241,52 | **111,18** | 110,94 | 147,21 |
| 50 | 659,74 | **221,66** | 218,76 | 282,19 |
| 75 | 1466,10 | **375,48** | 373,80 | 467,16 |
| 100 | 2562,54 | **543,34** | 537,18 | 664,39 |
| 200 | 10173,98 | **1281,32** | 1272,60 | 1528,77 |
| 500 | 63183,10 | **3853,92** | 3827,58 | 4482,89 |
| 1000 | 250781,66 | **8707,70** | 8656,24 | 9965,78 |

A coluna `n·log₂n` é a referência teórica assintótica discutida em aula.

## 5. Gráfico dos tempos

![Gráfico dos tempos médios](tempos.png)

O eixo do tempo está em **escala logarítmica**, senão a inserção (que cresce
como n²) achataria as outras duas curvas. A inserção cruza a intercalação por
volta de **n = 50–75** e depois dispara, enquanto `sorted()` permanece sempre a
mais rápida.

## 6. Gráfico das comparações

![Gráfico das comparações médias](comparacoes.png)

Também em escala logarítmica, com a linha tracejada `n log₂ n` como referência.
A inserção cresce de forma quadrática (≈ n²/4 para dados aleatórios), enquanto
intercalação e `sorted()` acompanham a reta de `n log₂ n`.

## 7. Análise

### 7.1 Em qual n a intercalação passa a ser mais rápida?

Há **dois pontos de virada diferentes**, um para tempo e outro para comparações.

**Pelo tempo:** até n = 30 a inserção é claramente mais rápida. Em **n = 50** as
duas praticamente empatam (83,25 µs da inserção contra 85,43 µs da intercalação,
~2,6% — dentro do ruído de medição). A partir de **n = 75** a vantagem da
intercalação é clara (137,71 µs contra 168,25 µs) e só cresce: em n = 1000 a
inserção leva ~29,7 ms contra ~2,09 ms da intercalação, ou seja, a intercalação é
cerca de **14 vezes mais rápida**.

> Resumo: o cruzamento de tempo acontece em **n ≈ 50–75** e se torna inequívoco
> em **n ≥ 75**.

**Pelas comparações:** a intercalação já faz menos comparações desde **n = 5**
(7,12 contra 7,76) e a diferença fica evidente em **n = 10** (22,44 contra 28,96,
cerca de 23% menos). O cruzamento puramente teórico das comparações ocorre bem
cedo, por volta de **n ≈ 7**.

### 7.2 O gráfico de comparações e o de tempo dão o mesmo ponto de virada?

**Não.** Pelas comparações a intercalação já “ganha” em torno de n = 5–10; pelo
tempo ela só “ganha” por volta de n = 50–75.

O motivo é que o **número de comparações não é o tempo**. O tempo inclui custos
que não aparecem na contagem de comparações:

- chamadas de função e recursão;
- criação de sublistas (`parte[:meio]`, `parte[meio:]`) e de novas listas no
  `merge`;
- a cópia da lista feita pela inserção (`lista.copy()`), que também tem custo;
- laço do interpretador Python, atribuições e movimentações.

Para listas pequenas, **esses custos fixos dominam** o tempo, então a
intercalação (que tem mais trabalho de estrutura, apesar de comparar menos) só
passa a compensar em n maior. É por isso que os dois gráficos cruzam em pontos
diferentes.

### 7.3 Por que a comparação com `sorted()` não serve para decidir entre os dois algoritmos?

`sorted()` é uma função **pronta e altamente otimizada** da linguagem
(implementa o **Timsort**). Ela é mais rápida que os dois algoritmos escritos
aqui, mas isso **não diz qual dos dois algoritmos do trabalho é melhor**: são
implementações diferentes, em Python puro, com custos e otimizações diferentes.
`sorted()` serve como **linha de base / referência de desempenho da linguagem**,
não como critério para escolher entre inserção e intercalação. Além disso, o
Timsort é **adaptativo** (aproveita trechos já ordenados), propriedade que nem a
inserção nem a intercalação deste trabalho exploram da mesma forma.

### 7.4 Um caso em que a inserção ainda seria a escolha adequada

A inserção é adequada para **listas pequenas ou quase ordenadas**. Ela é simples,
usa pouca memória extra (ordena no lugar, O(1)) e, quando os dados já estão
próximos da ordem final, faz pouquíssimas comparações e movimentações. No
próprio experimento, para n ≤ 30 ela foi a mais rápida entre os dois algoritmos
(e até n = 50 o resultado é praticamente empate). Também é comum em
**implementações híbridas**: o Timsort, por exemplo, usa inserção em blocos
pequenos.

## 8. Extra: comparações do `sorted()` vs. limite `n log n`

O `sorted()` foi medido com objetos que contam chamadas de `__lt__`. Os valores
ficaram muito próximos do limite `n log₂n` e um pouco **abaixo** dele:

| n | comparações do `sorted()` | n·log₂n | razão |
|---:|---:|---:|---:|
| 100 | 537,2 | 664,4 | 0,81 |
| 500 | 3827,6 | 4482,9 | 0,85 |
| 1000 | 8656,2 | 9965,8 | 0,87 |

Como `sorted()` (e a intercalação) fazem **no máximo** da ordem de `n log₂ n`
comparações, a razão abaixo de 1 é esperada — a constante depende do algoritmo e
dos dados. Para dados aleatórios, a intercalação segue de perto a fórmula
teórica `n log₂ n − n + 1`: em n = 1000, isso dá ≈ 8967 e o medido foi 8708.

Um resultado interessante é que o `sorted()` é **adaptativo**. Contando `__lt__`
para n = 1000 em diferentes ordens de entrada (semente 42):

| Entrada | Comparações do `sorted()` | Por elemento |
|---|---:|---:|
| aleatória | 8650 | 8,65 |
| já ordenada | 999 | 1,00 |
| invertida | 999 | 1,00 |
| quase ordenada (1 troca) | 1034 | 1,03 |

Ou seja: `sorted()` vai de **O(n)** (entradas quase ordenadas, onde o Timsort
identifica “runs” e só precisa comparar vizinhos) até perto de **O(n log n)**
(entradas aleatórias). Isso confirma o limite visto em aula e mostra que o
número de comparações **depende da ordem dos dados**.

## 9. Como reproduzir

Com Python 3 e a biblioteca `matplotlib` instalada:

```bash
python testes.py
python medir.py
```

`python medir.py` **recria do zero** o `dados.csv`, o `tempos.png` e o
`comparacoes.png`. Como a semente é fixa, as listas e as contagens de
comparações são as mesmas em qualquer máquina; pequenas variações de tempo podem
ocorrer por diferenças de hardware e de carga do sistema.
