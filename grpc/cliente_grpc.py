import grpc
import esteroides_pb2
import esteroides_pb2_grpc

# Estabelece canal com o servidor gRPC na porta 5051
channel = grpc.insecure_channel('192.168.246.38:5051')
stub = esteroides_pb2_grpc.EsteroidesServiceStub(channel)

# Lista os esteroides existentes no servidor
def listar_esteroides():
    resposta = stub.ListarEsteroides(esteroides_pb2.Vazio())
    print("\n--- Esteroides no servidor ---")
    for e in resposta.esteroides:
        print(f"- {e.nome} ({e.categoria}) - {e.preco}€ - Em stock: {e.em_stock}")

# Adiciona um novo esteroide ao servidor
def adicionar_esteroide():
    nome = input("Nome: ")
    preco = float(input("Preço: "))
    categoria = input("Categoria: ")
    em_stock = input("Está em stock? (s/n): ").lower() == 's'

    novo = esteroides_pb2.Esteroide(
        nome=nome,
        preco=preco,
        categoria=categoria,
        emStock=em_stock
    )

    resultado = stub.AdicionarEsteroide(novo)
    print(f"✔️ Esteroide '{resultado.nome}' adicionado com sucesso!")

# Menu principal
if __name__ == '__main__':
    while True:
        print("\n=== CLIENTE gRPC ===")
        print("1. Listar esteroides")
        print("2. Adicionar esteroide")
        print("0. Sair")

        op = input("Escolhe uma opção: ")

        if op == '1':
            listar_esteroides()
        elif op == '2':
            adicionar_esteroide()
        elif op == '0':
            break
        else:
            print("Opção inválida.")
