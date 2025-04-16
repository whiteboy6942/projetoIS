from zeep import Client

client = Client("http://127.0.0.1:8000/?wsdl")

nome = input("Nome do produto a procurar: ")
resultado = client.service.procurar_produto(nome)
print("Resultado:", resultado)


