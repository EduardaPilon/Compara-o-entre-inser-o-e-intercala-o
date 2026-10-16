# Comparação de Algoritmos de Ordenação

Projeto que implementa e compara a **ordenação por inserção**, a **ordenação por
intercalação** (*merge sort*) e a função `sorted()` do Python, medindo **tempo de
execução** e **número de comparações** em listas aleatórias.

## Índice

- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como rodar](#como-rodar)
- [Resultados](#resultados)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Como os dados são obtidos](#como-os-dados-são-obtidos)
- [Métodos comparados](#métodos-comparados)

## Requisitos

- Python 3.7 ou superior;
- `matplotlib`.

## Instalação

No terminal, dentro da pasta do projeto:

```bash
python -m pip install -r requirements.txt
```

Em alguns sistemas (Linux/macOS) o executável se chama `python3`.

## Como rodar

Executar os testes:

```bash
python testes.py
```

Executar as medições (recria `dados.csv`, `tempos.png` e `comparacoes.png` do zero):

```bash
python medir.py
```

## Resultados

### Tempo de execução

![Tempo médio de execução dos algoritmos](tempos.png)

A inserção é mais rápida em listas pequenas (até n = 30). A partir de n = 50–75 a
intercalação passa a vencer e, em n = 1000, chega a ser cerca de 14 vezes mais
rápida que a inserção. O `sorted()` é sempre o mais rápido.

### Número de comparações

![Número médio de comparações dos algoritmos](comparacoes.png)

O número de comparações da inserção cresce de forma **quadrática** (≈ n²/4),
enquanto a intercalação e o `sorted()` acompanham o limite **n·log₂n**. A linha
tracejada marca exatamente esse limite de referência.

A análise completa, incluindo os pontos de virada e o caso extra das comparações
do `sorted()`, está em [`RELATORIO.md`](RELATORIO.md).

## Estrutura do projeto

| Arquivo | Descrição |
|---|---|
| `ordenacao.py` | Ordenação por inserção e ordenação por intercalação |
| `testes.py` | Testes dos casos difíceis (vazia, 1 elemento, iguais, ordenada, invertida) |
| `medir.py` | Executa as medições e gera o CSV e os gráficos |
| `dados.csv` | Números brutos das medições |
| `tempos.png` | Gráfico dos tempos médios |
| `comparacoes.png` | Gráfico das comparações médias |
| `RELATORIO.md` | Análise dos resultados |
| `README.md` | Este arquivo |
| `requirements.txt` | Dependências do projeto |

## Como os dados são obtidos

- Tamanhos medidos: **5, 10, 20, 30, 50, 75, 100, 200, 500 e 1000**;
- **50 execuções por tamanho**, usando a média;
- tempo medido com `time.perf_counter()`;
- comparações dos dois algoritmos contadas durante a execução;
- comparações do `sorted()` contadas com uma classe que implementa `__lt__`;
- semente fixa (`SEMENTE = 42`), o que torna o experimento reproduzível.

## Métodos comparados

- Ordenação por inserção;
- Ordenação por intercalação (*merge sort*);
- `sorted()` do Python (*Timsort*), usado como referência de desempenho.
