from flask import Flask, request, jsonify
from graphene import ObjectType, String, Schema, Field, List, Float, Boolean
import graphene

# --- Dados de exemplo ---
esteroides = [
    {"nome": "Dianabol", "preco": 45.0, "categoria": "Oral", "em_stock": True},
    {"nome": "Deca-Durabolin", "preco": 60.0, "categoria": "Injetável", "em_stock": False},
    {"nome": "Anavar", "preco": 55.0, "categoria": "Oral", "em_stock": True},
    {"nome": "Winstrol", "preco": 50.0, "categoria": "Oral", "em_stock": True},
    {"nome": "Trenbolona", "preco": 70.0, "categoria": "Injetável", "em_stock": False},
    {"nome": "Sustanon 250", "preco": 65.0, "categoria": "Injetável", "em_stock": True},
]

# --- GraphQL Types ---
class EsteroideType(ObjectType):
    nome = String()
    preco = Float()
    categoria = String()
    em_stock = Boolean()

# --- Root Query ---
class Query(ObjectType):
    listar_esteroides = List(EsteroideType)

    def resolve_listar_esteroides(root, info):
        return esteroides
class AdicionarEsteroide(graphene.Mutation):
    class Arguments:
        nome = graphene.String(required=True)
        preco = graphene.Float(required=True)
        categoria = graphene.String(required=True)
        em_stock = graphene.Boolean(required=True)

    ok = graphene.Boolean()
    esteroide = graphene.Field(lambda: EsteroideType)

    def mutate(root, info, nome, preco, categoria, em_stock):
        novo = {
            "nome": nome,
            "preco": preco,
            "categoria": categoria,
            "em_stock": em_stock
        }
        esteroides.append(novo)
        return AdicionarEsteroide(esteroide=novo, ok=True)

class Mutation(graphene.ObjectType):
    adicionar_esteroide = AdicionarEsteroide.Field()

# --- Flask + GraphQL ---
app = Flask(__name__)
schema = Schema(query=Query, mutation=Mutation)

@app.route("/graphql", methods=["POST"])
def graphql_api():
    data = request.get_json()
    result = schema.execute(data.get("query"))
    return jsonify(result.data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


