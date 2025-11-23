# HydraX Backend

Backend API for calculating rainwater harvesting potential for buildings in London, UK.

## Features

- **Address Geocoding**: Converts London addresses to coordinates
- **Building Data**: Queries building database for roof area and location
- **Rainfall Data**: Extracts annual rainfall from raster data based on location
- **Water Savings Calculation**: Estimates annual water collection and savings
- **AI Assessment**: Provides intelligent recommendations and cost analysis

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Place your datasets in the `data/` directory:
   - `TQ_Building.db` - Building database (SQLite/GeoPackage format)
   - `londonRain.tif` - Annual rainfall raster (GeoTIFF format)

## Running the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /api/health
```

### Get Water Savings Estimate
```
GET /api/estimate?address=<London Address>
```

Example:
```bash
curl "http://localhost:5000/api/estimate?address=10+Downing+Street+London"
```

## Testing

Run the test script:
```bash
python test_api.py
```

Or test manually with curl:
```bash
# Health check
curl http://localhost:5000/api/health

# Get estimate
curl "http://localhost:5000/api/estimate?address=Tower+Bridge+London"
```

## Response Format

The `/api/estimate` endpoint returns:
- Building information (roof area, building ID)
- Rainfall data for the location
- Water collection estimates (m³, liters, gallons)
- Water savings breakdown (monthly, household coverage, etc.)
- AI assessment with recommendations
- Cost savings estimates
- Environmental impact metrics

## How It Works

1. **Geocoding**: Address → Latitude/Longitude (using OpenStreetMap)
2. **Building Lookup**: Find building polygon containing the coordinates
3. **Rainfall Extraction**: Sample rainfall raster at building location
4. **Calculation**: Compute water collection potential using:
   - Roof area from building database
   - Annual rainfall from raster
   - Capture efficiency factors
5. **AI Assessment**: Generate recommendations and cost analysis

## AI Implementation

The current "AI" is a **rule-based expert system** that:
- Scores buildings based on yield and runoff reduction
- Categorizes potential (excellent/good/moderate/low)
- Provides contextual recommendations
- Calculates cost savings and payback periods
- Estimates environmental impact

**Note**: This can be upgraded to use machine learning models if desired.

## Mock Data Mode

If the building database is empty, the system will:
- Create a mock building (50m × 50m) around the geocoded point
- Use fallback rainfall data (600mm/year) if raster is unavailable
- Still provide full calculations for testing

## Data Format Requirements

### Building Database (`TQ_Building.db`)
- Format: SQLite/GeoPackage
- Required: Geometry column with building polygons
- Optional: `area_m2` column (will be calculated if missing)
- CRS: Should be WGS84 (EPSG:4326) or compatible

### Rainfall Raster (`londonRain.tif`)
- Format: GeoTIFF
- Values: Annual rainfall in millimeters
- CRS: Any standard CRS (will be transformed automatically)

