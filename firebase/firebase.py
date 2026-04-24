import firebase_admin
import firebase_admin
import firebase_admin.exceptions
import mysql.connector
import decimal

CREDENTIALS_PATH = "lista6/serviceAccountKey.json"

try:
    if not firebase_admin._apps:
        cred = firebase_admin.credentials.Certificate(CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)

    print("Firebase inicializado com sucesso.")

except firebase_admin.exceptions.FirebaseError as e:
    print("Erro ao inicializar Firebase:", e)

db = firebase_admin.firestore.client()

# ── Inicialização MySQL ───────────────────────────────────────────────────────
try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql.",
        database="teste_database"
    )
    print("Conexão com MySQL realizada com sucesso.")

except mysql.connector.Error as e:
    print("Erro ao conectar no MySQL:", e)
    conexao = None

# ── Funções ───────────────────────────────────────────────────────────────────

def get_mysql_data():
    if conexao is None:
        print("Sem conexão com o MySQL.")
        return []

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    except mysql.connector.Error as e:
        print("Erro ao consultar MySQL:", e)
        return []


def enviar_produtos_firestore():
    mysql_records = get_mysql_data()

    if not mysql_records:
        print("Nenhum produto encontrado para enviar.")
        return

    print("Salvando dados no Firestore...")

    for record in mysql_records:
        try:
            doc_id = str(record["id"])

            if isinstance(record["preco"], decimal.Decimal):
                record["preco"] = float(record["preco"])

            del record["id"]

            db.collection("produtos_mysql").document(doc_id).set(record)
            print(f"Documento '{doc_id}' salvo no Firestore.")

        except firebase_admin.exceptions.FirebaseError as e:
            print(f"Erro ao salvar no Firestore (doc {record}):", e)

        except Exception as e:
            print("Erro inesperado ao salvar:", e)


def consultar_produtos_por_preco(valor_minimo: float = 15.0):
    """
    Consulta a coleção 'produtos_mysql' e retorna todos os produtos
    com preço superior ao valor_minimo informado.
    """
    print(f"\nConsultando produtos com preço > R$ {valor_minimo:.2f}...\n")

    try:
        docs = (
            db.collection("produtos_mysql")
              .where("preco", ">", valor_minimo)
              .order_by("preco", direction=firebase_admin.firestore.Query.DESCENDING)
              .stream()
        )

        encontrou   = False
        total       = 0
        soma_precos = 0.0

        for doc in docs:
            data = doc.to_dict()
            print(f"Nome: {data['nome']} | Preço: R$ {data['preco']:.2f}")
            encontrou    = True
            total       += 1
            soma_precos += data["preco"]

        if not encontrou:
            print("Nenhum produto encontrado com esse critério.")
        else:
            print(f"\nTotal encontrado  : {total} produto(s)")
            print(f"Preço médio       : R$ {soma_precos / total:.2f}")

    except firebase_admin.exceptions.FirebaseError as e:
        print("Erro na consulta do Firestore:", e)


def consultar_faixa_preco(preco_min: float, preco_max: float):
    """Consulta produtos dentro de uma faixa de preço."""
    print(f"\nProdutos entre R$ {preco_min:.2f} e R$ {preco_max:.2f}:\n")

    try:
        docs = (
            db.collection("produtos_mysql")
              .where("preco", ">=", preco_min)
              .where("preco", "<=", preco_max)
              .order_by("preco")
              .stream()
        )

        encontrou = False
        for doc in docs:
            data = doc.to_dict()
            print(f"Nome: {data['nome']} | Preço: R$ {data['preco']:.2f}")
            encontrou = True

        if not encontrou:
            print("Nenhum produto encontrado nessa faixa.")

    except firebase_admin.exceptions.FirebaseError as e:
        print("Erro na consulta do Firestore:", e)


def menu():
    while True:
        print("1 - Enviar produtos do MySQL para o Firestore")
        print("2 - Consultar produtos com preço > R$ 15,00")
        print("3 - Consultar produtos por faixa de preço")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            enviar_produtos_firestore()

        elif opcao == "2":
            consultar_produtos_por_preco(15.0)

        elif opcao == "3":
            try:
                preco_min = float(input("Preço mínimo: "))
                preco_max = float(input("Preço máximo: "))
                consultar_faixa_preco(preco_min, preco_max)
            except ValueError:
                print("Valor inválido. Digite números decimais.")

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


menu()

if conexao is not None:
    try:
        conexao.close()
        print("Conexão com MySQL encerrada.")
    except Exception as e:
        print("Erro ao fechar conexão:", e)