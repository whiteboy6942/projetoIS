
import requests

# URL base da API REST
URL = "http://192.168.246.38:5000/esteroides"

# Função para listar esteroides
def listar_esteroides():
    resposta = requests.get(URL)
    if resposta.status_code == 200:
        esteroides = resposta.json()
        for e in esteroides:
            print(f"- {e['nome']} ({e['categoria']}) - {e['preco']}€ - Em stock: {e['em_stock']}")
    else:
        print("Erro ao listar esteroides.")

# Função para adicionar um novo esteroide
def adicionar_esteroide():
    nome = input("Nome: ")
    preco = float(input("Preço: "))
    categoria = input("Categoria: ")
    em_stock = input("Está em stock? (s/n): ").lower() == 's'

    novo = {
        "nome": nome,
        "preco": preco,
        "categoria": categoria,
        "em_stock": em_stock
    }

    resposta = requests.post(URL, json=novo)
    if resposta.status_code == 200:
        print("Esteroide adicionado com sucesso!")
    else:
        print("Erro ao adicionar esteroide.")

# Função para atualizar um esteroide existente
def atualizar_esteroide():
    nome = input("Nome do esteroide a atualizar: ")
    preco = float(input("Novo preço: "))
    categoria = input("Nova categoria: ")
    em_stock = input("Está em stock? (s/n): ").lower() == 's'

    atualizado = {
        "preco": preco,
        "categoria": categoria,
        "em_stock": em_stock
    }

    resposta = requests.put(f"{URL}/{nome}", json=atualizado)
    if resposta.status_code == 200:
        print("Esteroide atualizado com sucesso!")
    else:
        print("Erro ao atualizar esteroide.")

# Função para remover um esteroide pelo nome
def remover_esteroide():
    nome = input("Nome do esteroide a remover: ")
    resposta = requests.delete(f"{URL}/{nome}")
    if resposta.status_code == 200:
        print("Esteroide removido com sucesso!")
    else:
        print("Erro ao remover esteroide.")

# Menu interativo
while True:
    print("\n=== CLIENTE REST ===")
    print("1. Listar esteroides")
    print("2. Adicionar esteroide")
    print("3. Atualizar esteroide")
    print("4. Remover esteroide")
    print("0. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        listar_esteroides()
    elif opcao == '2':
        adicionar_esteroide()
    elif opcao == '3':
        atualizar_esteroide()
    elif opcao == '4':
        remover_esteroide()
    elif opcao == '0':
        break
    else:
        print("Opção inválida.")
