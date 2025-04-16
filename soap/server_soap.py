from spyne import Application, rpc, ServiceBase, Integer, Unicode, Float, Boolean, Iterable, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import xml.etree.ElementTree as ET
import xmlschema

XSD_FILE = "produtos.xsd"
XML_FILE = "produtos.xml"

def carregar_produtos():
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        produtos = []

        for p in root.findall("produto"):
            nome = p.find("nome").text
            preco = float(p.find("preco").text)
            categoria = p.find("categoria").text
            em_stock = int(p.find("em_stock").text)

            produtos.append({
                "nome": nome,
                "preco": preco,
                "categoria": categoria,
                "em_stock": em_stock
            })

        return produtos
    except FileNotFoundError:
        return []

class CatalogoService(ServiceBase):

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


    @rpc(Unicode, Float, Unicode, Boolean, _returns=Unicode)
    def adicionar_produto(ctx, nome, preco, categoria, em_stock):
        schema = xmlschema.XMLSchema(XSD_FILE)

        novo = ET.Element("produto")
        ET.SubElement(novo, "nome").text = nome
        ET.SubElement(novo, "preco").text = str(preco)
        ET.SubElement(novo, "categoria").text = categoria
        ET.SubElement(novo, "em_stock").text = str(em_stock)

        temp_root = ET.Element("produtos")
        temp_root.append(novo)
        xml_temp = ET.tostring(temp_root, encoding="unicode")

        if not schema.is_valid(xml_temp):
            return "Erro: Produto inválido segundo o XSD."

        try:
            tree = ET.parse(XML_FILE)
            root = tree.getroot()
        except FileNotFoundError:
            root = ET.Element("produtos")
            tree = ET.ElementTree(root)

        root.append(novo)
        tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

    @rpc(Unicode, _returns=Unicode)
    def remover_produto(ctx, nome):
       try:
           tree = ET.parse(XML_FILE)
           root = tree.getroot()
       except FileNotFoundError:
          return "Erro: Ficheiro XML não encontrado."

       produtos = root.findall("produto")
       encontrado = False

       for p in produtos:
         if p.find("nome").text == nome:
            root.remove(p)
            encontrado = True
            break

       if not encontrado:
        return "Produto não encontrado."

       tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)
       return "Produto removido com sucesso."


    @rpc(_returns=Array(Unicode))
    def listar_produtos(ctx):
        produtos = carregar_produtos()
        nomes = [f'{p["nome"]} | {p["preco"]}€ | {p["categoria"]} | Em stock: {p["em_stock"]}' for p in produtos]
        return nomes

# Servidor SOAP
application = Application(
    [CatalogoService],
   tns='catalogo.soap',
   in_protocol=Soap11(validator='lxml'),
   out_protocol=Soap11()
)


if __name__ =='__main__':
   from wsgiref.simple_server import make_server
   print ("SOAP server disponivel em http://0.0.0.0:8000")
   server = make_server('0.0.0.0', 8000, WsgiApplication(application))
   server.serve_forever()
