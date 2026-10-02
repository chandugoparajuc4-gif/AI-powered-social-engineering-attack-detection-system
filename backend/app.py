from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sys
from pathlib import Path


# --------------------------------------------------
# Project path
# --------------------------------------------------

PROJECT_FOLDER = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_FOLDER))


# --------------------------------------------------
# Import detector
# --------------------------------------------------

from detector import analyze_message


# --------------------------------------------------
# Create Flask application
# --------------------------------------------------

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static",
    static_url_path="/static"
)

CORS(app)


# --------------------------------------------------
# Home route
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy"
    })


# --------------------------------------------------
# Analyze message
# --------------------------------------------------

@app.route("/api/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required."
            }), 400

        message = data.get("message", "")

        if not message.strip():

            return jsonify({
                "error": "Message cannot be empty."
            }), 400

        result = analyze_message(message)

        return jsonify(result)

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# --------------------------------------------------
# Run Flask server
# --------------------------------------------------

if __name__ == "__main__":

    print("\n======================================")
    print("AI SOCIAL ENGINEERING DETECTION API")
    print("======================================")
    print("Server: http://127.0.0.1:5000")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )