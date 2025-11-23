# backend/processing/analytics.py
from .config import RUNOFF_COEFF, CAPTURE_FACTOR
from .config import AVERAGE_RAINFALL_MM_FALLBACK
from .loader import sample_rainfall_mm_at_point


def compute_rain_harvest_for_building(building_row, rainfall_mm=None):
    """
    building_row: a row from buildings GeoDataFrame with fields:
        - area_m2
        - geometry (in CANONICAL_CRS)
    rainfall_mm: optional override; if None, sampled from raster.

    Returns dict with:
        - roof_area_m2
        - rainfall_mm
        - estimated_annual_yield_m3
        - estimated_annual_yield_liters
        - estimated_annual_yield_gallons
        - stormwater_runoff_reduction_percent
        - water_savings_breakdown: dict with monthly estimates and usage comparisons
    """
    area_m2 = float(building_row["area_m2"])

    # Rainfall
    if rainfall_mm is None:
        rainfall_mm = sample_rainfall_mm_at_point(building_row.geometry)
    if rainfall_mm is None:
        rainfall_mm = AVERAGE_RAINFALL_MM_FALLBACK

    # Estimated yield in m^3/year
    rainfall_m = rainfall_mm / 1000.0
    captured_m3 = area_m2 * rainfall_m * CAPTURE_FACTOR

    # Convert to more user-friendly units
    captured_liters = captured_m3 * 1000.0
    captured_gallons = captured_m3 * 264.172  # US gallons

    # Baseline runoff m^3/year (no harvesting)
    baseline_runoff_m3 = area_m2 * rainfall_m * RUNOFF_COEFF
    if baseline_runoff_m3 > 0:
        reduction_pct = 100.0 * captured_m3 / baseline_runoff_m3
    else:
        reduction_pct = 0.0

    # Calculate water savings breakdown
    # Average UK household uses ~150 liters per person per day
    # For a typical 2.4 person household: ~131,400 liters/year
    avg_person_daily_liters = 150
    avg_household_size = 2.4
    annual_household_usage_liters = avg_person_daily_liters * avg_household_size * 365
    
    # Percentage of household water needs that could be met
    household_coverage_pct = min(100.0, (captured_liters / annual_household_usage_liters) * 100.0)
    
    # Monthly breakdown (assuming relatively even distribution, though London has seasonal variation)
    monthly_yield_liters = captured_liters / 12.0
    monthly_yield_gallons = captured_gallons / 12.0

    # Equivalent to number of showers (average shower uses ~65 liters)
    showers_per_year = captured_liters / 65.0
    
    # Equivalent to number of toilet flushes (average flush uses ~6 liters)
    toilet_flushes_per_year = captured_liters / 6.0

    return {
        "roof_area_m2": area_m2,
        "rainfall_mm": float(rainfall_mm),
        "estimated_annual_yield_m3": float(captured_m3),
        "estimated_annual_yield_liters": float(captured_liters),
        "estimated_annual_yield_gallons": float(captured_gallons),
        "stormwater_runoff_reduction_percent": float(reduction_pct),
        "water_savings_breakdown": {
            "monthly_yield_liters": round(monthly_yield_liters, 1),
            "monthly_yield_gallons": round(monthly_yield_gallons, 1),
            "household_coverage_percent": round(household_coverage_pct, 1),
            "equivalent_showers_per_year": round(showers_per_year, 0),
            "equivalent_toilet_flushes_per_year": round(toilet_flushes_per_year, 0),
            "annual_household_usage_liters": round(annual_household_usage_liters, 0),
        }
    }
