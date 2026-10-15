import unittest
from ordenacao import ordenacao_insercao, ordenacao_intercalacao

class TestOrdenacao(unittest.TestCase):
    
    def setUp(self):
        self.algoritmos = [ordenacao_insercao, ordenacao_intercalacao]

    def test_lista_vazia(self):
        for algo in self.algoritmos:
            self.assertEqual(algo([]), [])

    def test_um_elemento(self):
        for algo in self.algoritmos:
            self.assertEqual(algo([42]), [42])

    def test_elementos_iguais(self):
        for algo in self.algoritmos:
            self.assertEqual(algo([5, 5, 5, 5]), [5, 5, 5, 5])

    def test_lista_ja_ordenada(self):
        for algo in self.algoritmos:
            self.assertEqual(algo([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_lista_invertida(self):
        for algo in self.algoritmos:
            self.assertEqual(algo([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])
            
    def test_lista_aleatoria(self):
        for algo in self.algoritmos:
            self.assertEqual(algo([3, 1, 4, 1, 5, 9, 2, 6]), [1, 1, 2, 3, 4, 5, 6, 9])

if __name__ == '__main__':
    unittest.main()