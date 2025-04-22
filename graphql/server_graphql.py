from flask import Flask, request, jsonify
from schema import schema

app = Flask(__name__)

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    result = schema.execute(
        data.get("query"),
        variable_values=data.get("variables")
    )

    response = {}
    if result.errors:
        response['errors'] = [str(error) for error in result.errors]
    if result.data:
        response['data'] = result.data

    return jsonify(response)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)



