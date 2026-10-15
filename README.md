
# Comparação de Algoritmos de Ordenação

Projeto para comparar a ordenação por inserção, a ordenação por intercalação e a função `sorted()` do Python.

## Requisitos

- Python 3 instalado
- Biblioteca matplotlib

## Instalação

No terminal, execute:

```bash
python -m pip install matplotlib
```

## Como executar os testes

```bash
python testes.py
```

## Como executar as medições

```bash
python medir.py
```

O programa realiza as medições, calcula as médias e gera:

- `dados.csv`: resultados numéricos;
- `tempos.png`: gráfico dos tempos médios;
- `comparacoes.png`: gráfico das comparações médias.

Os arquivos de resultados são recriados ao executar `python medir.py`.

## Métodos comparados

- Ordenação por inserção;
- Ordenação por intercalação;
- Função `sorted()` do Python.
