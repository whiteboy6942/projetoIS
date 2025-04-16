from flask import Flask, request, jsonify
from graphene import ObjectType, String, Schema, Field, List, Float, Boolean

# --- Dados de exemplo (normalmente lidos de JSON) ---
produtos = [
    {"nome": "Caneta", "preco": 1.5, "categoria": "Papelaria", "em_stock": True},
    {"nome": "Caderno", "preco": 3.0, "categoria": "Papelaria", "em_stock": False}
]

# --- GraphQL Types ---
class ProdutoType(ObjectType):
    nome = String()
    preco = Float()
    categoria = String()
    em_stock = Boolean()

# --- Root Query ---
class Query(ObjectType):
    listar_produtos = List(ProdutoType)

    def resolve_listar_produtos(root, info):
        return produtos

# --- Flask + GraphQL ---
app = Flask(__name__)
schema = Schema(query=Query)

@app.route("/graphql", methods=["POST"])
def graphql_api():
    data = request.get_json()
    result = schema.execute(data.get("query"))
    return jsonify(result.data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
