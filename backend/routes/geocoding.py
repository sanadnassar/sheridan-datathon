# backend/routes/geocoding.py

from flask import Blueprint, request, jsonify
from services.geocoding_service import geocode_address, GeocodingError

geocoding_bp = Blueprint("geocoding", __name__, url_prefix="/api")


@geocoding_bp.route("/geocode", methods=["POST"])
def geocode():
    """
    Expects JSON body: { "address": "123 Fake St, London" }
    Returns: { "easting": ..., "northing": ... } in British National Grid (OSGB36, EPSG:27700)
    or { "error": "Invalid address" }
    """
    data = request.get_json(silent=True) or {}
    address = data.get("address")

    if not address or not isinstance(address, str):
        return jsonify({"error": "address is required"}), 400

    try:
        easting, northing = geocode_address(address)
    except GeocodingError:
        return jsonify({"error": "Invalid address"}), 400
    except Exception as e:
        # Unexpected error – log in real app
        return jsonify({"error": "Internal server error"}), 500

    return jsonify({
        "address": address,
        "easting": easting,
        "northing": northing
    })
