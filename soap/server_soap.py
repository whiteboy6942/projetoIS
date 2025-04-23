from spyne import Application, rpc, ServiceBase, Unicode, Float, Boolean, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import xml.etree.ElementTree as ET
import xmlschema 


XML_FILE = "produtos.xml"
XSD_FILE = "schema.xsd" 


# Função para carregar produtos do XML

def carregar_produtos():
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        produtos = []

        for p in root.findall("produto"):
            produtos.append({
                "nome": p.find("nome").text,
                "preco": p.find("preco").text,
                "categoria": p.find("categoria").text,
                "em_stock": p.find("em_stock").text
            })

        return produtos
    except FileNotFoundError:
        return []


# Classe com os métodos SOAP

class CatalogoService(ServiceBase):

    # Lista todos os produtos
    @rpc(_returns=Array(Unicode))
    def listar_produtos(ctx):
        produtos = carregar_produtos()
        return [f'{p["nome"]} | {p["preco"]}€ | {p["categoria"]} | Stock: {p["em_stock"]}' for p in produtos]

    # Procura um produto pelo nome
    @rpc(Unicode, _returns=Unicode)
    def procurar_produto(ctx, nome):
        try:
            tree = ET.parse(XML_FILE)
            root = tree.getroot()
        except FileNotFoundError:
            return "Ficheiro XML não encontrado."

        for p in root.findall("produto"):
            if p.find("nome").text == nome:
                preco = p.find("preco").text
                categoria = p.find("categoria").text
                em_stock = p.find("em_stock").text
                return f"{nome} | {preco}€ | {categoria} | Em stock: {em_stock}"

        return "Produto não encontrado."

    # Adiciona um novo produto com validação XSD
    @rpc(Unicode, Float, Unicode, Boolean, _returns=Unicode)
    def adicionar_produto(ctx, nome, preco, categoria, em_stock):
        schema = xmlschema.XMLSchema(XSD_FILE)

        # Cria XML temporário com o novo produto
        novo = ET.Element("produto")
        ET.SubElement(novo, "nome").text = nome
        ET.SubElement(novo, "preco").text = str(preco)
        ET.SubElement(novo, "categoria").text = categoria
        ET.SubElement(novo, "em_stock").text = "1" if em_stock else "0"

        temp_root = ET.Element("produtos")
        temp_root.append(novo)

        # Valida contra o XSD
        xml_temp = ET.tostring(temp_root, encoding="unicode")
        if not schema.is_valid(xml_temp):
            return "Erro: Produto inválido segundo o XSD."

        # Grava no ficheiro XML
        try:
            tree = ET.parse(XML_FILE)
            root = tree.getroot()
        except FileNotFoundError:
            root = ET.Element("produtos")
            tree = ET.ElementTree(root)

        root.append(novo)
        tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
        return "Produto adicionado com sucesso."

    # Remove produto pelo nome
    @rpc(Unicode, _returns=Unicode)
    def remover_produto(ctx, nome):
        try:
            tree = ET.parse(XML_FILE)
            root = tree.getroot()
        except FileNotFoundError:
            return "Ficheiro XML não encontrado."

        for p in root.findall("produto"):
            if p.find("nome").text == nome:
                root.remove(p)
                tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
                return "Produto removido com sucesso."

        return "Produto não encontrado."

# Configuração da aplicação SOAP

application = Application(
    [CatalogoService],
    tns='catalogo.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)


# Lança o servidor SOAP

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print("SOAP server disponível em http://0.0.0.0:8000")
    server = make_server('0.0.0.0', 8000, WsgiApplication(application))
    server.serve_forever()
