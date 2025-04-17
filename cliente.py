import grpc
import esteroides_pb2
import esteroides_pb2_grpc

def main():
    try:
        channel = grpc.insecure_channel('51.21.169.186:5051')
        stub = esteroides_pb2_grpc.EsteroidesServiceStub(channel)

        # Listar esteroides atuais
        print("📦 Esteroides disponíveis:")
        resposta = stub.ListarEsteroides(esteroides_pb2.Vazio(), timeout=5)
        for e in resposta.esteroides:
            print(f"- {e.nome} | {e.preco:.2f}€ | {e.categoria} | {'✔️' if e.em_stock else '❌'}")

        # Adicionar novo esteroide
        print("\n➕ A adicionar novo esteroide...\n")
        novo = esteroides_pb2.Esteroide(
            nome="SuperBolado",
            preco=99.99,
            categoria="Injetável",
            em_stock=True
        )

        resposta_add = stub.AdicionarEsteroide(novo)
        print("📨 Servidor respondeu:", resposta_add.mensagem)

        # Listar novamente após a adição
        print("\n📥 Esteroides atualizados:")
        resposta = stub.ListarEsteroides(esteroides_pb2.Vazio())
        for e in resposta.esteroides:
            print(f"- {e.nome} | {e.preco:.2f}€ | {e.categoria} | {'✔️' if e.em_stock else '❌'}")

    except grpc.RpcError as e:
        print(f"[ERRO] Código: {e.code()}")
        print(f"[ERRO] Detalhes: {e.details()}")

if __name__ == "__main__":
    main()
