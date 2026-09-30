from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Chess Player Analyzer API is working"
    })

@app.route("/player/<fide_id>")
def player(fide_id):
    return jsonify({
        "fide_id": fide_id,
        "message": "Player lookup will be connected next"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
