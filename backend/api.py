from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "FineDay AI backend is running!"})

@app.route("/api/test")
def test():
    return jsonify({"status": "ok", "route": "/api/test"})

if __name__ == "__main__":
    app.run()
