#1
# import string
# from collections import Counter
 
# with open("texto.txt", "r", encoding="utf-8") as f:
#     texto = f.read()
 
# texto = texto.lower()
# texto = texto.translate(str.maketrans("", "", string.punctuation))
 
# palavras = texto.split()
# contagem = Counter(palavras)

# print("As 10 palavras mais comuns:\n")
# for i, (palavra, quantidade) in enumerate(contagem.most_common(10), start=1):
#     print(f"{i:2}. {palavra:<20} {quantidade} ocorrência(s)")

#2
# import csv

# ARQUIVO = "produtos.csv"
# CATEGORIA = "Eletrônicos"

# produtos_filtrados = []

# with open(ARQUIVO, "r", encoding="utf-8") as f:
#     reader = csv.DictReader(f)
#     for linha in reader:
#         if linha["categoria"].strip() == CATEGORIA:
#             produtos_filtrados.append({
#                 "produto": linha["produto"],
#                 "preco": float(linha["preco"])
#             })

# if not produtos_filtrados:
#     print(f"Nenhum produto encontrado na categoria '{CATEGORIA}'.")
# else:
#     total = sum(p["preco"] for p in produtos_filtrados)
#     media = total / len(produtos_filtrados)

#     print(f"Categoria: {CATEGORIA}")
#     print(f"{'-' * 40}")
#     for p in produtos_filtrados:
#         print(f"  {p['produto']:<25} R$ {p['preco']:>8.2f}")
#     print(f"{'-' * 40}")
#     print(f"  {'Total de produtos:':<25} {len(produtos_filtrados)}")
#     print(f"  {'Preço médio:':<25} R$ {media:>8.2f}")

#3
# import requests
# from bs4 import BeautifulSoup

# URL = "https://matt-gzg.github.io/botaoSecreto/"

# response = requests.get(URL)
# response.encoding = "utf-8"

# soup = BeautifulSoup(response.text, "html.parser")

# titulos_h2 = soup.find_all("h2")

# if not titulos_h2:
#     print("Nenhum título <h2> encontrado.")
# else:
#     print(f"Títulos <h2> encontrados em: {URL}\n")
#     print(f"{'#':<4} {'Texto'}")
#     print("-" * 50)
#     for i, titulo in enumerate(titulos_h2, start=1):
#         print(f"{i:<4} {titulo.get_text(strip=True)}")

#4
import requests

TOPICO = "data-science"
MAX_RESULTADOS = 5

endpoint = f"https://api.github.com/search/repositories"

params = {
    "q": TOPICO,
    "sort": "stars",
    "order": "desc",
    "per_page": MAX_RESULTADOS
}

headers = {
    "Accept": "application/vnd.github+json"
}

response = requests.get(endpoint, params=params, headers=headers)
dados = response.json()

if "errors" in dados or "message" in dados:
    print(f"Erro: {dados.get('message', 'Erro desconhecido')}")
else:
    print(f"Top {MAX_RESULTADOS} repositórios relacionados a '{TOPICO}':\n")
    print(f"{'#':<4} {'Nome':<40} {'Stars':<12} URL")
    print("-" * 100)

    for i, repo in enumerate(dados["items"], start=1):
        nome  = repo["full_name"]
        url   = repo["html_url"]
        stars = repo["stargazers_count"]
        print(f"{i:<4} {nome:<40} {stars:<12,} {url}")