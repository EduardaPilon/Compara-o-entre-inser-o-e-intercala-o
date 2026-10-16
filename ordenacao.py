def ordenacao_insercao(lista):
    lista = lista.copy()
    comparacoes = 0

    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1

        while j >= 0:
            comparacoes += 1

            if lista[j] > chave:
                lista[j + 1] = lista[j]
                j -= 1
            else:
                break

        lista[j + 1] = chave

    return lista, comparacoes


def ordenacao_intercalacao(lista):
    comparacoes = [0]

    def ordenar(parte):
        if len(parte) <= 1:
            return parte

        meio = len(parte) // 2

        esquerda = ordenar(parte[:meio])
        direita = ordenar(parte[meio:])

        resultado = []
        i = 0
        j = 0

        while i < len(esquerda) and j < len(direita):
            comparacoes[0] += 1

            if esquerda[i] <= direita[j]:
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1

        resultado.extend(esquerda[i:])
        resultado.extend(direita[j:])

        return resultado

    return ordenar(lista), comparacoes[0]
