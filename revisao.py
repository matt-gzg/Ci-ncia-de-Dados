import math
import collections

def ex1():
    nome = "Tashuia"
    idade = 21
    altura = 1.99
    cidade = "Jardim Alegre (famoso Happy Garden)"

    print(f"{nome}, {idade} anos, " f"{altura}m - {cidade}")

def ex2():
    animais = ["mamaco", "avestruz", "ligre", "tigro", "ema"]
    animais.append("golira")
    animais.append("pato")
    animais.remove("ligre")
    print(animais)

def ex3():
    notas = [10, 5.6, 9.4, 7.8, 8.8, 4.3, 2.1, 6, 7, 7.2]
    print(f"Maior nota: {max(notas)}, Menor nota: {min(notas)}, Média: {sum(notas)/len(notas)}")

def ex4():
    impares = [x for x in range(1, 20, 2)]
    print(impares)

def ex5():
    contato = {
        "tashuia": 123456,
        "baiva": 123123,
        "mourice": 999
    }
    nome = input("Insira o nome a buscar na lista de contatos: ")
    if contato[nome]:
        print(f"Nome: {nome}, Número: {contato.get(nome)}")

def ex6(tupla1, tupla2):
    print(math.sqrt((tupla2[0] - tupla1[0])**2 + (tupla2[1] - tupla1[1])**2))

def ex7(frase):
    print(len(frase.split()))
    contagem = collections.Counter(frase.split())
    palavras = contagem.most_common(3)
    print(palavras)

def ex8(*args):
    print({
        "max" : max(args),
        "min" : min(args),
        "media" : sum(args) / len(args)
    })

def ex9():
    class Produto:
        def __init__(self, nome, preco, estoque):
            self.nome = nome
            self.preco = preco
            self.estoque = estoque

        def vender(self, qtdade):
            if self.estoque > 0:
                self.estoque -= qtdade
            
        def repor(self, qtdade):
            if qtdade > 0:
                self.estoque += qtdade
        
        def exibir(self):
            print(f"O produto é {self.nome}, O preço é {self.preco}, {self.estoque} disponíveis")

    p1 = Produto("arroz", 29.90, 20)
    p1.exibir()
    p1.vender(10)
    p1.exibir()
    p1.repor(90)
    p1.exibir()

def ex10():
    class Veiculo:
        def __init__(self, marca, modelo, ano):
            self.marca = marca
            self.modelo = modelo
            self.ano = ano

        def tipo_habilitacao(self):
            pass

    class Carro(Veiculo):
        def __init__(self, marca, modelo, ano, rodas):
            super().__init__(marca, modelo, ano)
            self.rodas = rodas

        def tipo_habilitacao(self):
            print("Tipo B")

    class Moto(Veiculo):
        def __init__(self, marca, modelo, ano, cilindradas):
            super().__init__(marca, modelo, ano)
            self.cilindradas = cilindradas

        def tipo_habilitacao(self):
            print("Tipo A")
            
    c1 = Carro("Fiat", "Palio", 2001, 4)
    m1 = Moto("Honda", "Pop100", 2009, 20)
    c1.tipo_habilitacao()
    m1.tipo_habilitacao()

def ex11():
    class Livro:
        def __init__(self, titulo, autor, isbn):
            self.titulo = titulo
            self.autor = autor
            self.isbn = isbn
            self.disponivel = True
 
        def exibir(self):
            status = "disponivel" if self.disponivel else "emprestado"
            print(f"{self.isbn} - {self.titulo} ({self.autor}) [{status}]")
 
    class Usuario:
        def __init__(self, nome, cpf):
            self.nome = nome
            self.cpf = cpf
            self.livros_emprestados = []
 
        def exibir(self):
            print(f"{self.nome} - cpf: {self.cpf}")
            if self.livros_emprestados:
                print("  livros em mãos:")
                for livro in self.livros_emprestados:
                    print(f"    - {livro.titulo}")
            else:
                print("  nenhum livro emprestado")
 
    class Biblioteca:
        def __init__(self, nome):
            self.nome = nome
            self.livros = []
 
        def adicionar_livro(self, livro):
            self.livros.append(livro)
            print(f"livro {livro.titulo} adicionado")
 
        def buscar_por_titulo(self, titulo):
            resultado = [l for l in self.livros if titulo.lower() in l.titulo.lower()]
            if not resultado:
                print(f"nenhum livro encontrado com o titulo {titulo}")
            return resultado
 
        def buscar_por_isbn(self, isbn):
            for livro in self.livros:
                if livro.isbn == isbn:
                    return livro
            return None
 
        def emprestar(self, isbn, usuario):
            livro = self.buscar_por_isbn(isbn)
            if livro is None:
                print(f"isbn {isbn} nao encontrado")
            elif not livro.disponivel:
                print(f"{livro.titulo} ja esta emprestado")
            else:
                livro.disponivel = False
                usuario.livros_emprestados.append(livro)
                print(f"{livro.titulo} emprestado para {usuario.nome}")
 
        def devolver(self, isbn, usuario):
            livro = self.buscar_por_isbn(isbn)
            if livro is None:
                print(f"isbn {isbn} nao encontrado")
            elif livro not in usuario.livros_emprestados:
                print(f"{usuario.nome} nao tem {livro.titulo}")
            else:
                livro.disponivel = True
                usuario.livros_emprestados.remove(livro)
                print(f"{livro.titulo} devolvido por {usuario.nome}")
 
        def exibir_acervo(self):
            print(f"\nacervo - {self.nome}")
            if not self.livros:
                print("  acervo vazio")
            for livro in self.livros:
                livro.exibir()
            print()
 
    bib = Biblioteca("Biblioteca Central")
 
    bib.adicionar_livro(Livro("Dom Casmurro",           "Machado de Assis", "978-1"))
    bib.adicionar_livro(Livro("O Cortiço",              "Aluísio Azevedo",  "978-2"))
    bib.adicionar_livro(Livro("Vidas Secas",            "Graciliano Ramos", "978-3"))
    bib.adicionar_livro(Livro("Grande Sertão: Veredas", "Guimarães Rosa",   "978-4"))
 
    tashuia = Usuario("Tashuia", "111.222.333-44")
    baiva   = Usuario("Baiva",   "555.666.777-88")
 
    bib.exibir_acervo()
 
    bib.emprestar("978-1", tashuia)
    bib.emprestar("978-3", tashuia)
    bib.emprestar("978-1", baiva)
    bib.emprestar("978-9", baiva)
 
    print()
    tashuia.exibir()
    baiva.exibir()
 
    bib.exibir_acervo()
 
    encontrados = bib.buscar_por_titulo("vidas")
    if encontrados:
        print("busca por vidas:")
        for l in encontrados:
            l.exibir()
 
    print()
 
    bib.devolver("978-1", tashuia)
    bib.devolver("978-1", baiva)
 
    print()
    tashuia.exibir()
 
    bib.exibir_acervo()

# ex1()
# ex2()
# ex3()
# ex4()
#ex5()
#ex6((2,3), (6,5))
#ex7("Hello World baiva baiva baiva pao")
#ex8(2, 4, 1, 3)
#ex9()
# ex10()
ex11()