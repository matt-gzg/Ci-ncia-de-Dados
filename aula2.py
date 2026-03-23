import numpy as np

# 1
arr = np.random.randint(100, 501, size=12)
print(arr)
matriz = arr.reshape(3, 4)
print(matriz)
matrizT = matriz.T
soma = sum(matrizT[:])
print(soma)
media = np.mean(matriz, axis=0)
print(media)
print(len(arr[arr > 400]))

# 2
arr = np.arange(10)
print(arr)
print(np.full((3, 3), True, dtype=bool))
print(arr[arr % 2 != 0])
arr[arr % 2 != 0] = -1
print(arr)
m = np.random.randint(1, 101, size=(5, 5))
print(m)
print(np.sum(m, axis=0))
print(np.max(m, axis=1))
a = np.array([1, 2, 3, 4, 5])
print(a + 2)
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(np.concatenate((a, b)))
a = np.array([10, 20, 30, 40])
print(a[::-1])

# 3
a = np.array([22, 24, 21, 23, 25, 20, 22])
print(f"Temperatura Media: {np.mean(a)}  Dia mais quente: {a.max()}")

# 4
vendas = np.random.randint(50, 201, size=(3, 4))
print(f"Vendas por produto: {vendas.sum(axis=1)}")

# 5
pontuacoes = np.array([75, 88, 92, 65, 70, 80, 95, 60, 85, 78])
print(f"Mínima: {pontuacoes.min()}  Máxima: {pontuacoes.max()}")

# 6
leituras = np.random.rand(20)
print(leituras[leituras > 0.7])

# 7
precos = np.array([120.50, 121.00, 119.80, 122.30, 120.00])
variacao = np.diff(precos) / precos[:-1] * 100
print(variacao.round(2))

# 8
print(np.eye(4))

# 9
print(np.zeros((3, 3)))
print(np.ones((2, 5)))

# 10
a = np.random.randint(0, 70, size=25)
print(a.reshape(5, 5))

# 11
arr = np.arange(10)
print(arr[arr % 2 == 0])

# 12
arr = np.array([1, 2, 3, 4, 5])
print(np.cumsum(arr))

# 13
arr = np.array([1, 2, 2, 3, 4, 4, 4, 5])
print(np.unique(arr))

# 14
print(np.linspace(0, 10, 5))

# 15
notas = np.array([80, 90, 70])
pesos = np.array([0.3, 0.5, 0.2])
print(np.average(notas, weights=pesos))

# 16
dados = np.array([[2, 4, 6], [75, 80, 90]])
print(dados.T)

# 17
m = np.random.randint(1, 10, size=(3, 4))
print(m[::-1])

# 18
a = np.array([1, 2, 3])
b = np.array([3, 2, 1])
print(a == b)

# 19
arr = np.random.randint(0, 101, size=10)
print(arr[arr > 50])

# 20
arr = np.array([1, 7, 3, 7, 5, 7])
print(np.sum(arr == 7))

# 21
arr = np.array([1.23, 2.78, 3.50, 4.11])
print(np.round(arr))

# 22
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(np.vstack((a, b)))