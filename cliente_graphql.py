import requests

URL = "http://51.21.169.186:5002/graphql"  # Substitui se mudares o IP

def listar_esteroides():
    query = """
    {
        esteroides {
            nome
            preco
            categoria
            emStock
        }
    }
    """
    resposta = requests.post(URL, json={"query": query})

    print("📘 DEBUG - Código HTTP:", resposta.status_code)
    print("📘 DEBUG - Texto da resposta:", resposta.text)

    if resposta.status_code == 200:
        try:
            dados = resposta.json()
        except Exception as e:
            print("❌ Erro ao converter JSON:", e)
            return

        if "data" in dados and "esteroides" in dados["data"]:
            esteroides = dados["data"]["esteroides"]
            print("\n📦 Esteroides disponíveis:")
            for e in esteroides:
                status = "✅" if e["emStock"] else "❌"
                print(f"- {e['nome']} | {e['preco']:.2f}€ | {e['categoria']} | {status}")
        else:
            print("❌ Erro: resposta inesperada do servidor:", dados)
    else:
        print("❌ Erro ao obter esteroides. Código HTTP:", resposta.status_code)

def adicionar_esteroide():
    nome = input("Nome: ")
    preco = float(input("Preço: "))
    categoria = input("Categoria (Oral/Injetável): ")
    emStock = input("Está em stock? (s/n): ").lower() == "s"

    mutation = f"""
    mutation {{
        adicionarEsteroide(nome: "{nome}", preco: {preco}, categoria: "{categoria}", emStock: {str(emStock).lower()}) {{
            esteroide {{
                nome
                preco
                categoria
                emStock
            }}
        }}
    }}
    """

    resposta = requests.post(URL, json={"query": mutation})

    print("📘 DEBUG - Código HTTP:", resposta.status_code)
    print("📘 DEBUG - Texto da resposta:", resposta.text)

    if resposta.status_code == 200:
        print("✅ Esteroide adicionado com sucesso!")
    else:
        print("❌ Erro ao adicionar esteroide. Código HTTP:", resposta.status_code)

if __name__ == "__main__":
    while True:
        print("\n=== CLIENTE GRAPHQL ===")
        print("1. Listar esteroides")
        print("2. Adicionar esteroide")
        print("0. Sair")
        op = input("Escolhe uma opção: ")

        if op == "1":
            listar_esteroides()
        elif op == "2":
            adicionar_esteroide()
        elif op == "0":
            break
        else:
            print("❌ Opção inválida.")
