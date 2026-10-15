def ordenacao_insercao(lista):
    """Ordena uma lista usando o algoritmo de inserção (Insertion Sort)."""
    arr = lista.copy()
    for i in range(1, len(arr)):
        chave = arr[i]
        j = i - 1
        # Compara arr[j] > chave
        while j >= 0 and arr[j] > chave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = chave
    return arr

def ordenacao_intercalacao(lista):
    """Ordena uma lista usando o algoritmo de intercalação (Merge Sort)."""
    if len(lista) <= 1:
        return lista.copy()
    
    meio = len(lista) // 2
    esquerda = ordenacao_intercalacao(lista[:meio])
    direita = ordenacao_intercalacao(lista[meio:])
    
    return _mesclar(esquerda, direita)

def _mesclar(esquerda, direita):
    resultado = []
    i = j = 0
    
    while i < len(esquerda) and j < len(direita):
        if direita[j] < esquerda[i]:
            resultado.append(direita[j])
            j += 1
        else:
            resultado.append(esquerda[i])
            i += 1
            
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado