import random
import unittest

from ordenacao import ordenacao_insercao, ordenacao_intercalacao


class TestesOrdenacao(unittest.TestCase):

    CASOS = [
        [],
        [7],
        [4, 4, 4, 4],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [8, 3, 6, 1, 9, 2],
    ]

    def _verificar_algoritmo(self, algoritmo):
        for lista in self.CASOS:
            with self.subTest(algoritmo=algoritmo.__name__, lista=lista):
                original = list(lista)
                resultado, comparacoes = algoritmo(lista)

                self.assertEqual(resultado, sorted(lista))
                self.assertGreaterEqual(comparacoes, 0)
                self.assertEqual(
                    lista, original,
                    "o algoritmo não deve alterar a lista de entrada",
                )

    def test_insercao(self):
        self._verificar_algoritmo(ordenacao_insercao)

    def test_intercalacao(self):
        self._verificar_algoritmo(ordenacao_intercalacao)

    def test_contagens_insercao(self):
        self.assertEqual(ordenacao_insercao([1, 2, 3, 4, 5])[1], 4)
        self.assertEqual(ordenacao_insercao([5, 4, 3, 2, 1])[1], 10)
        self.assertEqual(ordenacao_insercao([4, 4, 4, 4])[1], 3)
        self.assertEqual(ordenacao_insercao([])[1], 0)
        self.assertEqual(ordenacao_insercao([7])[1], 0)

    def test_listas_aleatorias_grandes(self):
        random.seed(0)
        for _ in range(50):
            lista = [random.randint(-100, 100) for _ in range(200)]
            with self.subTest():
                self.assertEqual(ordenacao_insercao(lista)[0], sorted(lista))
                self.assertEqual(ordenacao_intercalacao(lista)[0], sorted(lista))

    def test_intercalacao_cresce_como_n_log_n(self):
        for n in [1, 2, 5, 16, 100, 1000]:
            lista = list(range(n, 0, -1))
            _, comparacoes = ordenacao_intercalacao(lista)
            limite = n * max(1, n.bit_length())
            self.assertLessEqual(comparacoes, limite)


if __name__ == "__main__":
    unittest.main()
