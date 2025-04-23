# === Importações principais ===
import grpc
from concurrent import futures
import time

# Importa os módulos gerados a partir do ficheiro .proto
import esteroides_pb2
import esteroides_pb2_grpc

# === Lista simulada de esteroides (base de dados em memória) ===
esteroides = [
    esteroides_pb2.Esteroide(nome="Dianabol", preco=45.0, categoria="Oral", em_stock=True),
    esteroides_pb2.Esteroide(nome="Deca-Durabolin", preco=60.0, categoria="Injetavel", em_stock=False),
    esteroides_pb2.Esteroide(nome="Anavar", preco=55.0, categoria="Oral", em_stock=True),
    esteroides_pb2.Esteroide(nome="Winstrol", preco=50.0, categoria="Oral", em_stock=True),
    esteroides_pb2.Esteroide(nome="Trembolona", preco=70.0, categoria="Injetavel", em_stock=False),
    esteroides_pb2.Esteroide(nome="Sustanon 250", preco=65.0, categoria="Injetavel", em_stock=True),
]

# === Classe que implementa os métodos definidos no ficheiro .proto ===
class EsteroidesService(esteroides_pb2_grpc.EsteroidesServiceServicer):

    #  Método para listar esteroides
    def ListarEsteroides(self, request, context):
        resposta = esteroides_pb2.ListaEsteroides()
        resposta.esteroides.extend(esteroides)
        return resposta

    #  Método para adicionar um esteroide à lista
    def AdicionarEsteroide(self, request, context):
        if not request.nome:
            return esteroides_pb2.RespostaMensagem(mensagem="Nome invalido")

        novo = esteroides_pb2.Esteroide(
            nome=request.nome,
            preco=request.preco,
            categoria=request.categoria,
            em_stock=request.em_stock
        )
        esteroides.append(novo)
        return esteroides_pb2.RespostaMensagem(mensagem=f"Esteroide '{request.nome}' adicionado com sucesso!")

# === Função principal para arrancar o servidor gRPC ===
def main():
    # Cria o servidor com 10 threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Regista o serviço no servidor
    esteroides_pb2_grpc.add_EsteroidesServiceServicer_to_server(EsteroidesService(), server)

    # Define a porta onde o servidor escuta
    server.add_insecure_port('0.0.0.0:5051')
    server.start()
    print("✅ Servidor gRPC ativo na porta 5051")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("🛑 Servidor encerrado")

# === Lançamento do servidor ===
if __name__ == '__main__':
    main()

