
import unittest
from ordenacao import ordenacao_insercao, ordenacao_intercalacao


class TestesOrdenacao(unittest.TestCase):

    def testar_algoritmo(self, algoritmo):
        casos = [
            [],
            [7],
            [4, 4, 4, 4],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [8, 3, 6, 1, 9, 2]
        ]

        for lista in casos:
            resultado, comparacoes = algoritmo(lista)

            self.assertEqual(resultado, sorted(lista))
            self.assertGreaterEqual(comparacoes, 0)

    def test_insercao(self):
        self.testar_algoritmo(ordenacao_insercao)

    def test_intercalacao(self):
        self.testar_algoritmo(ordenacao_intercalacao)


if __name__ == "__main__":
    unittest.main()
