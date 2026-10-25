import os
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
    query = request.args.get("q", "").strip()
    results = []
    error = None

    if query:
        try:
            response = requests.get(
                "https://openi.nlm.nih.gov/api/search",
                params={"query": query, "m": 1, "n": 20},
                timeout=20
            )
            response.raise_for_status()
            data = response.json()
            results = data if isinstance(data, list) else data.get("list", [])
        except Exception:
            error = "Search failed. Please try again."

    return render_template(
        "index.html",
        query=query,
        results=results,
        error=error
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
