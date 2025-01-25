from flask import Flask
from indexer import indexer, getQuery
app = Flask(__name__)
indexer()
@app.route("/")
def hello_world():
    l = getQuery("smart contracts")
    print(l)
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run()