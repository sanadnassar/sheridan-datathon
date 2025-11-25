# backend/services/geocoding_service.py

import requests
from typing import Optional, Tuple
from pyproj import Transformer
from config import settings

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

# Transformer from WGS84 (EPSG:4326) to British National Grid (OSGB36, EPSG:27700)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)


class GeocodingError(Exception):
    """Raised when an address cannot be geocoded."""


def geocode_address(address: str) -> Tuple[float, float]:
    """
    Given a human-readable address string, return (easting, northing) in British National Grid (OSGB36, EPSG:27700).
    Raises GeocodingError if not found or API error.
    """
    if not settings.GOOGLE_MAPS_API_KEY:
        raise RuntimeError(
            "GOOGLE_MAPS_API_KEY is not set. Define it in your environment."
        )

    params = {
        "address": address,
        "key": settings.GOOGLE_MAPS_API_KEY,
    }

    resp = requests.get(GEOCODE_URL, params=params, timeout=10)

    if resp.status_code != 200:
        raise GeocodingError(f"Geocoding HTTP error: {resp.status_code}")

    data = resp.json()

    status = data.get("status")
    if status != "OK" or not data.get("results"):
        # Could be ZERO_RESULTS, INVALID_REQUEST, etc.
        raise GeocodingError(f"Geocoding failed with status: {status}")

    location = data["results"][0]["geometry"]["location"]
    lat = location["lat"]
    lng = location["lng"]
    
    # Convert from WGS84 (lat/lng) to British National Grid (Easting/Northing)
    # Note: transformer was created with always_xy=True so it expects (lon, lat)
    # (i.e. x=longitude, y=latitude). The previous code passed (lat, lng)
    # which swapped the inputs and produced incorrect / inconsistent results.
    easting, northing = transformer.transform(lng, lat)
    return easting, northing
