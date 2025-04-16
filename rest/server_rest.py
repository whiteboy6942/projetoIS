from flask import Flask, jsonify, request
import json
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Base de dados simulada
esteroides = [
    {"nome": "Dianabol", "preco": 45.0, "categoria": "Oral", "em_stock": True},
    {"nome": "Deca-Durabolin", "preco": 60.0, "categoria": "Injetável", "em_stock": False},
    {"nome": "Anavar", "preco": 55.0, "categoria": "Oral", "em_stock": True},
    {"nome": "Winstrol", "preco": 50.0, "categoria": "Oral", "em_stock": True},
    {"nome": "Trembolona", "preco": 70.0, "categoria": "Injetável", "em_stock": False},
    {"nome": "Sustanon 250", "preco": 65.0, "categoria": "Injetável", "em_stock": True}
]

@app.route("/esteroides", methods=["GET"])
def listar_esteroides():
    return jsonify(esteroides)

@app.route("/esteroides", methods=["POST"])
def adicionar_esteroide():
    novo = request.get_json()
    esteroides.append(novo)
    return jsonify({"mensagem": f"Esteroide '{novo['nome']}' adicionado com sucesso!"}), 200

@app.route("/esteroides/<string:nome>", methods=["PUT"])
def atualizar_esteroide(nome):
    dados = request.get_json()
    for e in esteroides:
        if e["nome"].lower() == nome.lower():
            e.update(dados)
            return jsonify({"mensagem": f"Esteroide '{nome}' atualizado com sucesso."}), 200
    return jsonify({"erro": f"Esteroide '{nome}' não encontrado."}), 404

@app.route("/esteroides/<string:nome>", methods=["DELETE"])
def remover_esteroide(nome):
    global esteroides
    esteroides = [e for e in esteroides if e["nome"].lower() != nome.lower()]
    return jsonify({"mensagem": f"Esteroide '{nome}' removido com sucesso."}), 200

@app.route("/importar/json", methods=["POST"])
def importar_json():
    try:
        with open("produtos.json", "r") as f:
            dados = json.load(f)
            esteroides.extend(dados)
        return jsonify({"mensagem": "Dados importados com sucesso a partir de JSON."}), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao importar JSON: {str(e)}"}), 500

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

