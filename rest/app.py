from flask import Flask, jsonify, request
from jsonpath_ng import parse as jsonpath_parse
import json

app = Flask(__name__)

@app.route('/produtos/jsonpath', methods=['GET'])
def jsonpath_query():
    query = request.args.get('query')

    if not query:
        return jsonify({"erro": "Parâmetro 'query' é obrigatório"}), 400

    try:
        with open('produtos.json') as f:
            produtos = json.load(f)

        jsonpath_expr = jsonpath_parse(query)
        resultado = [match.value for match in jsonpath_expr.find(produtos)]

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
