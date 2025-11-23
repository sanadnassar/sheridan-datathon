from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow frontend to call backend during hackathon
CORS(app, origins="*", methods=["*"], allow_headers=["*"])

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "ok"})

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    # TODO: run segmentation + area + rainfall
    return jsonify({"filename": file.filename, "message": "received"})
