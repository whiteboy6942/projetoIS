#Importações principais
from flask import Flask, request, jsonify
from schema import schema  # Este é o ficheiro onde defines os tipos, queries e mutations

# Criação da app Flask
app = Flask(__name__)


# Endpoint para tratar as requisições GraphQL

@app.route("/graphql", methods=["POST"])
def graphql_server():
    #Recebe a query enviada pelo cliente (em JSON)
    data = request.get_json()

    # Executa a query ou mutation com a 'schema' definida no ficheiro schema.py
    result = schema.execute(
        data.get("query"),
        variable_values=data.get("variables")
    )

    # Prepara a resposta JSON com erros ou dados
    response = {}
    if result.errors:
        response['errors'] = [str(error) for error in result.errors]
    if result.data:
        response['data'] = result.data

    return jsonify(response)


# Arrancar o servidor na porta 5002

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
