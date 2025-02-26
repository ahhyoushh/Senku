import os
from flask import Flask, request, jsonify
from views import views
from flask_cors import CORS
from centers_view import centersbp

app = Flask(__name__)
CORS(app)
app.register_blueprint(views, url_prefix="/")
app.register_blueprint(centersbp, url_prefix="/centers")

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
@app.before_request
def handle_preflight():
    """✅ Automatically handle OPTIONS preflight requests"""
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight passed"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Default to 10000 if PORT is not set
    app.run(host="0.0.0.0", port=port)