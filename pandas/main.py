import pandas as pd

#1
df_vendas = pd.read_csv("vendas.csv", sep=",")
print(df_vendas)
print(df_vendas.dtypes)

#2
df_clima = pd.read_csv(
    "clima.csv",
    parse_dates=["data"],
    index_col="data"
)
print(df_clima)
print()
df_clima.info()

#3
df_log = pd.read_csv(
    "log.csv",
    comment="#",
    parse_dates=["timestamp"]
)
print(df_log)
print(df_log.dtypes)

#4
df_estoque = pd.read_csv("estoque.csv", sep=";", decimal=",")
print(df_estoque)
print(df_estoque.dtypes)

#5
df_trans = pd.read_csv("transacoes.csv", thousands=".", decimal=",")
print(df_trans)
print(df_trans.dtypes)

#6
df_sensores = pd.read_csv("sensores.csv", na_values=["NA", "-"])
print(df_sensores)
print()
df_sensores.info()

#7
df_exp = pd.read_csv("experimento.csv")
print(df_exp.head(3))
print(df_exp.tail(2))
print(df_exp.describe())

#8
df_big = pd.read_csv("bigdata.csv", parse_dates=["timestamp"])
print(df_big)
print()
df_big.info(memory_usage="deep")

#9
df_notas = pd.read_csv("notas.csv")
print(df_notas)
print(df_notas.describe())
print("\n--- Média por disciplina:")
medias = df_notas[["matematica", "portugues", "historia"]].mean()
for disciplina, media in medias.items():
    print(f"   {disciplina:<12}: {media:.2f}")

#10
for i, chunk in enumerate(pd.read_csv("transacoesbig.csv", sep=";", chunksize=20), start=1):
    print(f"Bloco {i} - Linhas: {len(chunk)}")
    print(chunk.head(3).to_string(index=False))
    print()

#11
for i, chunk in enumerate(
    pd.read_csv("sensor.csv", na_values=["NA", "-"], chunksize=10),
    start=1
):
    temp_media = chunk["temperatura"].mean()
    ausentes = chunk["temperatura"].isna().sum()
    print(f"Bloco {i:2} | Temp. media: {temp_media:.2f}°C | Ausentes na temp.: {ausentes}")