# backend/processing/ai_model.py
from .config import (
    YIELD_HIGH_M3,
    YIELD_MEDIUM_M3,
    REDUCTION_HIGH_PCT,
    REDUCTION_MEDIUM_PCT,
)

def hydrax_ai_assessment(annual_yield_m3: float, reduction_pct: float, 
                         annual_yield_liters: float = None,
                         water_savings_breakdown: dict = None) -> dict:
    """
    AI-powered assessment of rainwater harvesting potential.
    Provides detailed analysis and recommendations.

    Returns:
        {
          "score": float (0-1),
          "category": "excellent" | "good" | "moderate" | "low",
          "summary": str,
          "recommendations": list[str],
          "estimated_cost_savings": dict,
          "environmental_impact": dict
        }
    """
    # Base score on both yield and reduction
    score_yield = min(1.0, annual_yield_m3 / YIELD_HIGH_M3)
    score_reduction = min(1.0, reduction_pct / REDUCTION_HIGH_PCT)
    score = 0.6 * score_yield + 0.4 * score_reduction

    # Calculate cost savings (UK average water cost: ~£1.50 per cubic meter)
    water_cost_per_m3 = 1.50  # GBP
    annual_cost_savings_gbp = annual_yield_m3 * water_cost_per_m3
    annual_cost_savings_usd = annual_cost_savings_gbp * 1.27  # Approximate conversion
    
    # Typical system cost range (GBP)
    if annual_yield_m3 >= YIELD_HIGH_M3:
        system_cost_range = (2000, 5000)
        payback_years = system_cost_range[0] / annual_cost_savings_gbp if annual_cost_savings_gbp > 0 else 999
    elif annual_yield_m3 >= YIELD_MEDIUM_M3:
        system_cost_range = (1000, 3000)
        payback_years = system_cost_range[0] / annual_cost_savings_gbp if annual_cost_savings_gbp > 0 else 999
    else:
        system_cost_range = (500, 1500)
        payback_years = system_cost_range[0] / annual_cost_savings_gbp if annual_cost_savings_gbp > 0 else 999

    # Environmental impact (CO2 savings from reduced water treatment)
    # Average: 0.344 kg CO2 per m3 of water
    co2_savings_kg = annual_yield_m3 * 0.344

    recommendations = []
    
    if annual_yield_m3 >= YIELD_HIGH_M3 and reduction_pct >= REDUCTION_HIGH_PCT:
        category = "excellent"
        liters_text = f"{annual_yield_liters/1000:.0f} thousand liters" if annual_yield_liters else f"{annual_yield_m3*1000/1000:.0f} thousand liters"
        summary = (
            f"This rooftop has excellent rainwater harvesting potential! "
            f"You could collect approximately {annual_yield_m3:.1f} cubic meters "
            f"({liters_text}) of water annually, "
            f"reducing stormwater runoff by {reduction_pct:.1f}%. "
            f"This represents significant water savings and environmental benefits."
        )
        recommendations = [
            "Install a comprehensive rainwater harvesting system with storage tanks",
            "Consider connecting to toilet flushing and garden irrigation systems",
            "Explore potential for greywater recycling",
            "Look into local council grants or incentives for sustainable water systems"
        ]
    elif annual_yield_m3 >= YIELD_MEDIUM_M3 and reduction_pct >= REDUCTION_MEDIUM_PCT:
        category = "good"
        liters_text = f"{annual_yield_liters/1000:.0f} thousand liters" if annual_yield_liters else f"{annual_yield_m3*1000/1000:.0f} thousand liters"
        summary = (
            f"This rooftop offers good potential for rainwater collection. "
            f"You could harvest approximately {annual_yield_m3:.1f} cubic meters "
            f"({liters_text}) per year, "
            f"reducing runoff by {reduction_pct:.1f}%. "
            f"A rainwater system here would provide meaningful water savings."
        )
        recommendations = [
            "Install a medium-capacity rainwater harvesting system",
            "Use collected water for garden irrigation and outdoor cleaning",
            "Consider connecting to toilet flushing if feasible",
            "Start with a simple barrel system and expand if needed"
        ]
    elif annual_yield_m3 >= 20:
        category = "moderate"
        liters_text = f"{annual_yield_liters/1000:.0f} thousand liters" if annual_yield_liters else f"{annual_yield_m3*1000/1000:.0f} thousand liters"
        summary = (
            f"This rooftop provides moderate harvesting potential. "
            f"You could collect around {annual_yield_m3:.1f} cubic meters "
            f"({liters_text}) annually. "
            f"While not ideal for full household use, it's great for specific applications."
        )
        recommendations = [
            "Install a small to medium rainwater collection system",
            "Focus on garden irrigation and outdoor water use",
            "Consider a simple barrel or small tank system",
            "Use collected water to reduce mains water consumption for non-potable uses"
        ]
    else:
        category = "low"
        liters_text = f"{annual_yield_liters/1000:.0f} thousand liters" if annual_yield_liters else f"{annual_yield_m3*1000/1000:.0f} thousand liters"
        summary = (
            f"This rooftop has limited rainwater harvesting potential. "
            f"Annual collection would be around {annual_yield_m3:.1f} cubic meters "
            f"({liters_text}). "
            f"Small-scale collection systems could still provide some benefits."
        )
        recommendations = [
            "Consider a simple rain barrel for garden use",
            "Focus on water-efficient landscaping to maximize impact",
            "Even small systems help reduce stormwater runoff",
            "Combine with other water-saving measures for best results"
        ]

    # Add usage-specific recommendations if breakdown is available
    if water_savings_breakdown:
        coverage = water_savings_breakdown.get("household_coverage_percent", 0)
        if coverage >= 50:
            recommendations.insert(0, 
                f"Your system could meet {coverage:.0f}% of a typical household's water needs!")
        elif coverage >= 25:
            recommendations.insert(0,
                f"Your system could cover {coverage:.0f}% of household water needs, "
                "especially for non-potable uses like toilet flushing and gardening.")

    return {
        "score": round(float(score), 2),
        "category": category,
        "summary": summary,
        "recommendations": recommendations,
        "estimated_cost_savings": {
            "annual_savings_gbp": round(annual_cost_savings_gbp, 2),
            "annual_savings_usd": round(annual_cost_savings_usd, 2),
            "system_cost_range_gbp": system_cost_range,
            "estimated_payback_years": round(payback_years, 1) if payback_years < 50 else None,
        },
        "environmental_impact": {
            "co2_savings_kg_per_year": round(co2_savings_kg, 2),
            "stormwater_reduction_percent": round(reduction_pct, 1),
        }
    }
