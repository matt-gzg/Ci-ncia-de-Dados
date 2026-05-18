"""
ex1:
A visualização dos dados costuma ser uma das primeiras etapas da análise exploratória.
Por meio de gráficos e histogramas, é possível identificar padrões, valores discrepantes
(outliers) e o comportamento geral das variáveis. Isso ajuda a compreender melhor o
conjunto de dados antes da aplicação de modelos estatísticos ou de aprendizado de máquina.

ex2:
Distribuição uniforme:
    - Todos os valores dentro de um intervalo possuem a mesma chance de ocorrer.
    - O histograma apresenta formato aproximadamente retangular.
    - Exemplo: números gerados aleatoriamente entre 0 e 1.

Distribuição normal:
    - Os valores tendem a se concentrar ao redor da média.
    - O histograma possui formato de sino.
    - Exemplo: alturas de pessoas e erros experimentais.
"""

import pandas as pd
import numpy as np
import time
from typing import Optional
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm


#ex3
dados = pd.DataFrame({
    'idade': [25, None, 30, None, 45, 28]
})

valor_mediano = dados['idade'].median()
dados['idade_preenchida'] = dados['idade'].fillna(valor_mediano)

print("Questão 3:")
print(dados)
print()


#ex4
def converter_para_inteiro(valor: str) -> Optional[int]:
    """
    Tenta converter o valor recebido para inteiro.
    Caso a conversão não seja possível, retorna None.
    """
    try:
        return int(valor)
    except (ValueError, TypeError):
        return None


def processar_lista(lista_valores: list[str]) -> list[Optional[int]]:
    """
    Aplica a conversão para cada elemento da lista.
    """
    return [converter_para_inteiro(item) for item in lista_valores]


entrada = ['42', '3.14', 'abc', '100', '', None, '-7']
saida = processar_lista(entrada)

print("Questão 4:")
for item_original, item_convertido in zip(entrada, saída):
    print(f"{repr(item_original):>10} -> {item_convertido}")
print()

"""
ex5:
Algoritmos como KNN, K-Means, PCA e SVM com kernel RBF utilizam medidas de distância
entre observações. Quando as variáveis possuem escalas muito diferentes, aquela com
valores maiores influencia desproporcionalmente o cálculo. A padronização garante
que todas as variáveis contribuam de forma equilibrada."""

#ex6
matriz = np.array([
    [160, 55],
    [175, 80],
    [180, 90],
    [155, 50],
    [170, 70]
])

normalizador = StandardScaler()
matriz_padronizada = normalizador.fit_transform(matriz)

print("Questão 6:")
print("Dados originais:")
print(matriz)

print("\nDados padronizados:")
print(matriz_padronizada.round(2))

print("\nMédias calculadas:")
print(normalizador.mean_)

print("\nDesvios padrão:")
print(normalizador.scale_.round(2))
print()


#ex7
print("Questão 7:")
for item in tqdm(range(100), desc="Executando", unit="it"):
    time.sleep(0.05)
print()


#ex8
nomes_pessoas = ['Alice', 'Bob', 'Carol', 'David', 'Eva']

print("Questão 8:")
for indice, nome in enumerate(
    tqdm(nomes_pessoas, desc="Processando nomes")
):
    time.sleep(0.3)
    print(f"{indice}: {nome}")
print()


#ex9
print("Questão 9:")
quantidade_epocas = 3
conjunto_lotes = range(10)

for epoca in tqdm(range(quantidade_epocas), desc="Épocas"):
    for lote in tqdm(
        conjunto_lotes,
        desc=f"Lotes da época {epoca + 1}",
        leave=False
    ):
        time.sleep(0.05)
print()


#ex10
tqdm.pandas(desc="Aplicando função")

tabela = pd.DataFrame({
    'texto': [
        'hello world',
        'data science',
        'python',
        'pandas',
        'tqdm'
    ]
})

def transformar_texto(texto: str) -> str:
    """
    Converte para letras maiúsculas e substitui espaços por "_".
    """
    time.sleep(0.2)
    return texto.upper().replace(' ', '_')


tabela['texto_transformado'] = tabela['texto'].progress_apply(
    transformar_texto
)

print("Questão 10:")
print(tabela)