# backend/processing/config.py
from pathlib import Path

# Base directory = backend/
BASE_DIR = Path(__file__).resolve().parent.parent

# Paths to data files
DATA_DIR = BASE_DIR / "data"
TQ_BUILDING_PATH = DATA_DIR / "TQ_Building.db"  # SQLite/GeoPackage database
RAINFALL_RASTER_PATH = DATA_DIR / "londonRain.tif"  # Annual rainfall GeoTIFF

# CRS used internally for area & point-in-polygon (meters)
CANONICAL_CRS = "EPSG:3857"

# Hydrological parameters (you can tune later)
AVERAGE_RAINFALL_MM_FALLBACK = 600.0  # used if raster sample fails
RUNOFF_COEFF = 0.95           # fraction of rainfall that becomes runoff on roofs
CAPTURE_FACTOR = 0.80         # fraction of rainfall realistically harvested

# AI rating thresholds (very simple to start)
YIELD_HIGH_M3 = 200.0
YIELD_MEDIUM_M3 = 80.0
REDUCTION_HIGH_PCT = 70.0
REDUCTION_MEDIUM_PCT = 40.0
