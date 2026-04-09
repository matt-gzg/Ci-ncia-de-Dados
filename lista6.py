#1
import pandas as pd

df = pd.read_csv(
    "vendas.csv",
    header=None,
    index_col=0, 
    na_values="ND" 
)

print("exercicio 1")
print(df.head())

#2
relatorio_anual = pd.read_excel("relatorio.xlsx", sheet_name="Resultados")

with pd.ExcelWriter("relatorio.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    relatorio_anual.to_excel(writer, sheet_name="Resultados", index=False)

df_brutos = pd.read_excel("relatorio.xlsx", sheet_name="Dados Brutos")
print('exercicio2')
print(df_brutos.head())

#3
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users")
response.raise_for_status()

usuarios = response.json()
df = pd.DataFrame(usuarios)

print('exercicio 3')
print(df.head())

# #4
from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine("sqlite:///meu_banco.db")

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            preco REAL,
            estoque INTEGER
        )
    """))
    conn.execute(text("""
        INSERT OR IGNORE INTO produtos VALUES
            (1, 'Monitor',  799.90, 10),
            (2, 'Teclado',  120.50, 25),
            (3, 'Mouse',     50.00, 40),
            (4, 'Webcam',   250.00, 15)
    """))
    conn.commit()

with engine.connect() as conn:
    df = pd.read_sql("SELECT * FROM produtos", conn)

print('exercicio 4')
print(df.head())