from flask import Flask, jsonify
from processing.rooftops import load_rooftops
from processing.compute import compute_harvest
from processing.jsonify import to_json_ready

app = Flask(__name__)

@app.route("/harvest")
def harvest():
    rooftops = load_rooftops("data/rooftops.geojson")
    result = compute_harvest(rooftops, rainfall_mm=1200)
    json_data = to_json_ready(result)
    return jsonify(json_data)

@app.route("/total")
def total():
    rooftops = load_rooftops("data/rooftops.geojson")
    result = compute_harvest(rooftops, 1200)
    total_liters = float(result["potential_liters"].sum())
    return jsonify({"total_liters": total_liters})
