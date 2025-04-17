from flask import Flask, jsonify, request

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

# Rota para listar esteroides
@app.route("/esteroides", methods=["GET"])
def listar_esteroides():
    return jsonify(esteroides)

# Rota para adicionar um novo esteroide
@app.route("/esteroides", methods=["POST"])
def adicionar_esteroide():
    novo = request.get_json()
    esteroides.append(novo)
    return jsonify({"mensagem": f"Esteroide '{novo['nome']}' adicionado com sucesso!"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
