# backend/app.py
from flask import Flask, request, jsonify
from processing.loader import load_buildings
from processing.geocode import geocode_address_to_point
from processing.analytics import compute_rain_harvest_for_building
from processing.ai_model import hydrax_ai_assessment

app = Flask(__name__)

# Load datasets at startup
try:
    buildings_gdf = load_buildings()
    print(f"[HydraX] Loaded {len(buildings_gdf)} building footprints.")
    if len(buildings_gdf) == 0:
        print("[HydraX] Warning: Building database is empty. Using mock data mode.")
except Exception as e:
    print(f"[HydraX] Error loading buildings: {e}")
    buildings_gdf = None


@app.route("/api/health")
def health():
    return {"status": "ok"}


@app.route("/api/estimate", methods=["GET"])
def estimate_for_address():
    """
    Example:
      GET /api/estimate?address=10+Downing+Street+London
    """
    address = request.args.get("address")
    if not address:
        return jsonify({"error": "Missing 'address' query parameter"}), 400

    # 1. Geocode
    point_canonical, lat, lon = geocode_address_to_point(address)
    if point_canonical is None:
        return jsonify({"error": "Address not found by geocoder"}), 404

    # 2. Find building polygon that contains the point
    if buildings_gdf is None or len(buildings_gdf) == 0:
        # Mock mode: create a dummy building for testing
        from shapely.geometry import Polygon
        import geopandas as gpd
        from processing.config import CANONICAL_CRS
        
        # Create a small square building around the point (50m x 50m)
        buffer_distance = 25  # meters
        building_geom = point_canonical.buffer(buffer_distance)
        building = gpd.GeoDataFrame([{
            "geometry": building_geom,
            "area_m2": building_geom.area,
            "building_id": 0
        }], crs=CANONICAL_CRS).iloc[0]
    else:
        matches = buildings_gdf[buildings_gdf.geometry.contains(point_canonical)]
        if matches.empty:
            return jsonify({"error": "No building footprint found at that location"}), 404
        building = matches.iloc[0]

    # 3. Compute hydrological metrics
    metrics = compute_rain_harvest_for_building(building)

    # 4. AI-style assessment
    ai_result = hydrax_ai_assessment(
        metrics["estimated_annual_yield_m3"],
        metrics["stormwater_runoff_reduction_percent"],
        metrics.get("estimated_annual_yield_liters"),
        metrics.get("water_savings_breakdown"),
    )

    # 5. Build response
    response = {
        "input_address": address,
        "geocoded_lat": lat,
        "geocoded_lon": lon,
        "building_info": {
            "roof_area_m2": round(metrics["roof_area_m2"], 2),
            "building_id": int(building.get("building_id", 0)),
        },
        "rainfall_data": {
            "annual_rainfall_mm": round(metrics["rainfall_mm"], 1),
        },
        "water_collection": {
            "estimated_annual_yield_m3": round(metrics["estimated_annual_yield_m3"], 2),
            "estimated_annual_yield_liters": round(metrics.get("estimated_annual_yield_liters", 0), 0),
            "estimated_annual_yield_gallons": round(metrics.get("estimated_annual_yield_gallons", 0), 1),
        },
        "water_savings": metrics.get("water_savings_breakdown", {}),
        "environmental_impact": {
            "stormwater_runoff_reduction_percent": round(
                metrics["stormwater_runoff_reduction_percent"], 1
            ),
        },
        "hydrax_ai_assessment": ai_result,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
