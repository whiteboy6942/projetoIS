import requests

URL = "http://51.21.169.186:5000/esteroides"  # Altera o IP se estiveres a correr remotamente

def listar_esteroides():
    resposta = requests.get(URL)
    if resposta.status_code == 200:
        esteroides = resposta.json()
        print("\n📋 Lista de esteroides:")
        for e in esteroides:
            status = "✔️" if e['em_stock'] else "❌"
            print(f"- {e['nome']} | {e['preco']:.2f}€ | {e['categoria']} | {status}")
    else:
        print("❌ Erro ao listar esteroides.")

def adicionar_esteroide():
    print("\n🆕 Introduz os dados do novo esteroide:")
    nome = input("Nome: ")
    preco = float(input("Preço: "))
    categoria = input("Categoria (Oral/Injetável): ")
    em_stock = input("Está em stock? (s/n): ").lower() == 's'

    novo = {
        "nome": nome,
        "preco": preco,
        "categoria": categoria,
        "em_stock": em_stock
    }

    resposta = requests.post(URL, json=novo)
    print(f"🧾 DEBUG - Código HTTP: {resposta.status_code}")
    print(f"🧾 DEBUG - Resposta: {resposta.text}")

def atualizar_esteroide():
    nome = input("\n✏️ Nome do esteroide a atualizar: ")
    preco = float(input("Novo preço: "))
    categoria = input("Nova categoria: ")
    em_stock = input("Está em stock? (s/n): ").lower() == 's'

    dados = {
        "preco": preco,
        "categoria": categoria,
        "em_stock": em_stock
    }

    resposta = requests.put(f"{URL}/{nome}", json=dados)
    print(f"🧾 DEBUG - Código HTTP: {resposta.status_code}")
    print(f"🧾 DEBUG - Resposta: {resposta.text}")

def remover_esteroide():
    nome = input("\n🗑️ Nome do esteroide a remover: ")
    resposta = requests.delete(f"{URL}/{nome}")
    print(f"🧾 DEBUG - Código HTTP: {resposta.status_code}")
    print(f"🧾 DEBUG - Resposta: {resposta.text}")

if __name__ == "__main__":
    while True:
        print("\n=== MENU REST ===")
        print("1. Listar esteroides")
        print("2. Adicionar esteroide")
        print("3. Atualizar esteroide")
        print("4. Remover esteroide")
        print("0. Sair")

        opcao = input("Escolhe uma opção: ")

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
            print("❗ Opção inválida.")
