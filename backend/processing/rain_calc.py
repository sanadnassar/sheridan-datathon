from shapely.geometry import Point

RUNOFF_COEFF = 0.9  # UK roofs have good runoff

def compute_rain(area_m2, rainfall_mm):
    rainfall_m = rainfall_mm / 1000  # mm → m
    liters = area_m2 * rainfall_m * RUNOFF_COEFF * 1000
    return liters
