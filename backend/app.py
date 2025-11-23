from flask import Flask, jsonify
from processing.rooftops import load_rooftops
from processing.compute import compute_harvest
from processing.jsonify import to_json_ready

app = Flask(__name__)

import sqlite3

@app.route("/harvest")
def harvest():
    conn = sqlite3.connect("data/buildings.db")
    conn.row_factory = sqlite3.Row
    cur = conn.execute("SELECT lat, lon, area FROM rooftops LIMIT 20000;")
    rows = cur.fetchall()

    rainfall_mm = 800  # London average
    records = []
    for r in rows:
        try:
            area = float(r["area"]) if r["area"] is not None else 0.0
        except Exception:
            area = 0.0
        liters = area * rainfall_mm * 0.85
        records.append({
            "lat": r["lat"],
            "lon": r["lon"],
            "area": area,
            "liters": liters
        })

    conn.close()
    return jsonify(records)

@app.route("/total")
def total():
    # Use database instead of GeoJSON file
    rooftops = load_rooftops("data/buildings.db")
    
    if rooftops.empty:
        return jsonify({"total_liters": 0, "error": "No rooftop data available"})
    
    rainfall_mm = 1200  # Default rainfall amount
    efficiency = 0.85   # Rainwater harvesting efficiency
    
    # Calculate total harvest potential
    total_liters = float(rooftops["area"].sum() * rainfall_mm * efficiency)
    
    return jsonify({
        "total_liters": total_liters,
        "rooftop_count": len(rooftops),
        "total_area_m2": float(rooftops["area"].sum()),
        "rainfall_mm": rainfall_mm,
        "efficiency": efficiency
    })
