from .rooftops import load_rooftops
from .rain_calc import compute_rain
from ..data_loader import load_rainfall_raster, sample_rainfall

def compute_all(building_path):
    rooftops = load_rooftops(building_path)
    raster = load_rainfall_raster()

    results = []

    for idx, row in rooftops.iterrows():
        centroid = row.geometry.centroid
        rainfall_mm = sample_rainfall(raster, centroid)
        liters = compute_rain(row["area_m2"], rainfall_mm)

        results.append({
            "id": row["id"],
            "area_m2": row["area_m2"],
            "rainfall_mm": float(rainfall_mm),
            "liters_year": liters,
            "geometry": row.geometry.__geo_interface__
        })

    return results
