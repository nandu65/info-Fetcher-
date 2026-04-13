from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY")  # keep secret

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    queries = data.get("queries", [])

    results = []

    for q in queries:
        q = q.strip()
        if not q:
            continue

        # 🔴 Replace with your real API
        response = requests.get(
            "https://api.example.com/search",
            headers={"Authorization": f"Bearer {API_KEY}"},
            params={"query": q}
        )

        try:
            result = response.json()
        except:
            result = {"error": "Invalid response"}

        results.append({
            "query": q,
            "data": result
        })

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
