from spyne import Application, rpc, ServiceBase, Unicode, Float, Boolean, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import xml.etree.ElementTree as ET
import xmlschema

XSD_FILE = "schema.xsd"
XML_FILE = "produtos.xml"

# Função auxiliar para carregar produtos do ficheiro XML
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

# Serviço SOAP com métodos do catálogo
class CatalogoService(ServiceBase):

    @rpc(_returns=Array(Unicode))
    def listar_produtos(ctx):
        produtos = carregar_produtos()
        return [f'{p["nome"]} | {p["preco"]}€ | {p["categoria"]} | Stock: {p["em_stock"]}' for p in produtos]

    @rpc(Unicode, _returns=Unicode)
    def procurar_produto(ctx, nome):
        produtos = carregar_produtos()
        for p in produtos:
            if p["nome"] == nome:
                return f'{p["nome"]} | {p["preco"]}€ | {p["categoria"]} | Stock: {p["em_stock"]}'
        return "Produto não encontrado."

    @rpc(Unicode, Float, Unicode, Boolean, _returns=Unicode)
    def adicionar_produto(ctx, nome, preco, categoria, em_stock):
        schema = xmlschema.XMLSchema(XSD_FILE)

        novo = ET.Element("produto")
        ET.SubElement(novo, "nome").text = nome
        ET.SubElement(novo, "preco").text = str(preco)
        ET.SubElement(novo, "categoria").text = categoria
        ET.SubElement(novo, "em_stock").text = "1" if em_stock else "0"

        temp_root = ET.Element("produtos")
        temp_root.append(novo)

        xml_temp = ET.tostring(temp_root, encoding="unicode")
        print("DEBUG - XML gerado para validação:")
        print(xml_temp)

        if not schema.is_valid(ET.tostring(temp_root, encoding="unicode")):
            return "Erro: Produto inválido segundo o XSD."

        try:
            tree = ET.parse(XML_FILE)
            root = tree.getroot()
        except FileNotFoundError:
            root = ET.Element("produtos")
            tree = ET.ElementTree(root)

        root.append(novo)
        tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
        return "Produto adicionado com sucesso."

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

# Definição e arranque do servidor SOAP
application = Application([CatalogoService], tns='catalogo.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print("SOAP server disponível em http://0.0.0.0:8000")
    server = make_server('0.0.0.0', 8000, WsgiApplication(application))
    server.serve_forever()




