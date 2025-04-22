# Importação de bibliotecas necessárias
from flask import Flask, jsonify, request, Response
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom  

# Criação da aplicação Flask
app = Flask(__name__)

# Base de dados simulada (inicial) com esteroides
esteroides = [
    {"nome": "Dianabol", "preco": 45.0, "categoria": "Oral", "em_stock": True},
    {"nome": "Deca-Durabolin", "preco": 60.0, "categoria": "Injetável", "em_stock": False},
    {"nome": "Anavar", "preco": 55.0, "categoria": "Oral", "em_stock": True},
    {"nome": "Winstrol", "preco": 50.0, "categoria": "Oral", "em_stock": True},
    {"nome": "Trembolona", "preco": 70.0, "categoria": "Injetável", "em_stock": False},
    {"nome": "Sustanon 250", "preco": 65.0, "categoria": "Injetável", "em_stock": True}
]

# ROTAS PRINCIPAIS (CRUD)


# GET - Lista esteroides
@app.route("/esteroides", methods=["GET"])
def listar_esteroides():
    return jsonify(esteroides)

#  POST - Adiciona novo esteroide
@app.route("/esteroides", methods=["POST"])
def adicionar_esteroide():
    novo = request.get_json()
    esteroides.append(novo)
    return jsonify({"mensagem": f"Esteroide '{novo['nome']}' adicionado com sucesso!"}), 200

# PUT - Atualiza esteroide por nome
@app.route("/esteroides/<string:nome>", methods=["PUT"])
def atualizar_esteroide(nome):
    dados = request.get_json()
    for e in esteroides:
        if e["nome"].lower() == nome.lower():
            e.update(dados)
            return jsonify({"mensagem": f"Esteroide '{nome}' atualizado com sucesso."}), 200
    return jsonify({"erro": f"Esteroide '{nome}' não encontrado."}), 404

# DELETE - Remove esteroide por nome
@app.route("/esteroides/<string:nome>", methods=["DELETE"])
def remover_esteroide(nome):
    global esteroides
    esteroides = [e for e in esteroides if e["nome"].lower() != nome.lower()]
    return jsonify({"mensagem": f"Esteroide '{nome}' removido com sucesso."}), 200


# IMPORTAÇÃO DE DADOS


# Importar dados do ficheiro produtos.json (lado do servidor)
@app.route("/importar/json", methods=["POST"])
def importar_json():
    try:
        with open("produtos.json", "r") as f:
            dados = json.load(f)
        esteroides.extend(dados)
        return jsonify({"mensagem": "Dados importados com sucesso a partir de JSON."}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao importar JSON: {str(e)}"}), 500

# Importar dados do ficheiro produtos.xml (lado do servidor)
@app.route("/importar/xml", methods=["POST"])
def importar_xml():
    try:
        tree = ET.parse("produtos.xml")
        root = tree.getroot()
        for elem in root.findall("produto"):
            nome = elem.find("nome").text
            preco = float(elem.find("preco").text)
            categoria = elem.find("categoria").text
            em_stock = elem.find("em_stock").text.lower() == "true"
            esteroides.append({
                "nome": nome,
                "preco": preco,
                "categoria": categoria,
                "em_stock": em_stock
            })
        return jsonify({"mensagem": "Dados importados com sucesso a partir de XML."}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao importar XML: {str(e)}"}), 500


# EXPORTAÇÃO DE DADOS


# ✅ Exportar os dados atuais como JSON
@app.route("/exportar/json", methods=["GET"])
def exportar_json():
    return jsonify(esteroides)

# ✅ Exportar os dados atuais como XML, bem formatado
@app.route("/exportar/xml", methods=["GET"])
def exportar_xml():
    try:
        produtos = esteroides

        root = ET.Element("produtos")
        for p in produtos:
            produto_elem = ET.SubElement(root, "produto")
            for chave, valor in p.items():
                ET.SubElement(produto_elem, chave).text = str(valor)

        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")

        return Response(pretty_xml, mimetype='application/xml')

    except Exception as e:
        print("🛑 ERRO NO EXPORTAR XML:", e)
        return {"erro": str(e)}, 500


# EXECUTA A APLICAÇÃO

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



