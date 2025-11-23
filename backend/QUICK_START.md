# Quick Start Guide

## Will it work with real datasets?

**Yes!** The system is designed to automatically work when you replace the mock files:

1. **Replace `data/TQ_Building.db`** with your real building database
   - Should be SQLite/GeoPackage format
   - Must have geometry column with building polygons
   - Should include longitude/latitude data

2. **Replace `data/londonRain.tif`** with your real rainfall raster
   - Should be GeoTIFF format
   - Values should be annual rainfall in millimeters

The code will automatically:
- Detect and load the real data
- Use actual building areas from the database
- Extract real rainfall values from the raster
- Calculate accurate water savings

**No code changes needed!** Just replace the files.

## How is AI implemented?

Currently, the "AI" is a **rule-based expert system** (not machine learning). Here's how it works:

### Current Implementation:
- **Scoring Algorithm**: Combines yield and runoff reduction metrics
- **Categorization**: Classifies potential as excellent/good/moderate/low
- **Recommendations**: Provides contextual advice based on thresholds
- **Cost Analysis**: Calculates savings and payback periods
- **Environmental Impact**: Estimates CO2 savings

### Location: `processing/ai_model.py`

The system uses:
- Thresholds (YIELD_HIGH_M3, YIELD_MEDIUM_M3, etc.)
- Weighted scoring (60% yield, 40% reduction)
- Rule-based categorization
- Contextual recommendations

### To Upgrade to Real AI:
You could replace this with:
- Machine learning models (scikit-learn, TensorFlow)
- Trained on historical data
- More sophisticated predictions

But the current system works well for providing intelligent assessments!

## How to Test

### Step 1: Start the Server

```bash
cd /Users/Ethan/HydraX/HydraX/backend
python app.py
```

You should see:
```
[HydraX] Loaded X building footprints.
 * Running on http://127.0.0.1:5000
```

### Step 2: Test the API

**Option A: Use the test script**
```bash
python test_api.py
```

**Option B: Use curl**
```bash
# Health check
curl http://localhost:5000/api/health

# Get estimate for an address
curl "http://localhost:5000/api/estimate?address=10+Downing+Street+London"
```

**Option C: Use Python**
```python
import requests

response = requests.get(
    "http://localhost:5000/api/estimate",
    params={"address": "Tower Bridge, London"}
)
print(response.json())
```

### Step 3: Check the Response

The API returns a JSON object with:
- Building info (roof area, ID)
- Rainfall data
- Water collection estimates
- Water savings breakdown
- AI assessment with recommendations
- Cost savings
- Environmental impact

## Example Response

```json
{
  "input_address": "10 Downing Street, London",
  "geocoded_lat": 51.5034,
  "geocoded_lon": -0.1276,
  "building_info": {
    "roof_area_m2": 1963.50,
    "building_id": 12345
  },
  "water_collection": {
    "estimated_annual_yield_m3": 94.25,
    "estimated_annual_yield_liters": 94250,
    "estimated_annual_yield_gallons": 24898.5
  },
  "hydrax_ai_assessment": {
    "score": 0.75,
    "category": "good",
    "summary": "...",
    "recommendations": [...],
    "estimated_cost_savings": {
      "annual_savings_gbp": 141.38,
      "estimated_payback_years": 7.1
    }
  }
}
```

## Troubleshooting

**Server won't start?**
- Check if port 5000 is already in use
- Make sure all dependencies are installed: `pip install -r requirements.txt`

**No building found?**
- The address might not be in London
- Try a more specific address
- Check if building database is loaded correctly

**Rainfall data missing?**
- System will use fallback value (600mm/year)
- Check if `londonRain.tif` is in the `data/` directory

**Database errors?**
- Make sure `TQ_Building.db` is a valid SQLite/GeoPackage file
- Check that it contains geometry data

