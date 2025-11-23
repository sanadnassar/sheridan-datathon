# backend/processing/geocode.py
import requests
import geopandas as gpd
from shapely.geometry import Point
from .config import CANONICAL_CRS

USER_AGENT = "HydraX-Datathon/1.0 (contact@example.com)"  # put some email


def geocode_address_to_point(address: str):
    """
    Geocode a London address to a shapely Point in CANONICAL_CRS.
    Returns (point, lat, lon) or (None, None, None) if not found.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "addressdetails": 1,
        "limit": 1,
        "city": "London",
        "countrycodes": "gb",
    }
    headers = {"User-Agent": USER_AGENT}

    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        return None, None, None

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])

    # Build point in WGS84 then reproject
    point_wgs = gpd.GeoSeries([Point(lon, lat)], crs="EPSG:4326")
    point_canonical = point_wgs.to_crs(CANONICAL_CRS).iloc[0]
    return point_canonical, lat, lon
