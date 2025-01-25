from flask import Flask, request, jsonify
from langchain_groq import ChatGroq

from indexer import indexer, getQuery, generateQuery
app = Flask(__name__)
indexer()
@app.route("/")
def hello_world():
  
    return "<p>Hello, World!</p>"

@app.post("/generateQuery")
def generate():
    request_body = request.get_json()
    print(request_body)
    if ('prompt' in request_body):
        results = generateQuery(request_body['prompt'])
        return jsonify(results.json())
    else:
        return "Query Missing"
    
@app.post("/generateCode")
def generateCode():
    request_body = request.get_json()
    print(request_body)
    if ('prompt' in request_body):
        LLM = ChatGroq(model="llama-3.3-70b-versatile",api_key="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")
        results = LLM.invoke(request_body['prompt'] + 'use JSON')
        print(results.json(), "results")
        return jsonify(results.to_json())
    else:
        return "Query Missing"
    


if __name__ == "__main__":
    app.run(port=5000, debug=True)