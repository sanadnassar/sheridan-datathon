# backend/processing/loader.py
import geopandas as gpd
import rasterio
from rasterio.sample import sample_gen
from shapely.geometry import Point
from .config import TQ_BUILDING_PATH, RAINFALL_RASTER_PATH, CANONICAL_CRS, AVERAGE_RAINFALL_MM_FALLBACK


_buildings_gdf_cache = None
_rain_raster_cache = None


def load_buildings():
    """
    Load TQ_Building database (SQLite/GeoPackage), reproject to CANONICAL_CRS and add area + id.
    Cached after first load.
    
    The database should contain building polygons with longitude/latitude and area.
    GeoPandas can read GeoPackage format directly.
    """
    global _buildings_gdf_cache
    if _buildings_gdf_cache is not None:
        return _buildings_gdf_cache

    try:
        # Try to read as GeoPackage (SQLite with spatial data)
        # If it's a regular SQLite DB, we'll need to handle it differently
        gdf = gpd.read_file(TQ_BUILDING_PATH, driver="GPKG")
    except Exception:
        # Fallback: try reading as regular file (shapefile, geojson, etc.)
        try:
            gdf = gpd.read_file(TQ_BUILDING_PATH)
        except Exception as e:
            # If database is empty or doesn't exist, return empty GeoDataFrame
            print(f"Warning: Could not load buildings database: {e}")
            from shapely.geometry import Polygon
            gdf = gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")

    # If empty, return early
    if len(gdf) == 0:
        _buildings_gdf_cache = gdf
        return gdf

    # Ensure we have a CRS
    if gdf.crs is None:
        gdf.set_crs("EPSG:4326", inplace=True)

    # Reproject to a metric CRS for area calculations
    gdf = gdf.to_crs(CANONICAL_CRS)

    # Add area if not already present
    if "area_m2" not in gdf.columns:
        gdf["area_m2"] = gdf.geometry.area
    elif gdf["area_m2"].dtype == 'object':
        # Convert to float if it's stored as string
        gdf["area_m2"] = gdf["area_m2"].astype(float)

    # Add building_id if not present
    if "building_id" not in gdf.columns:
        gdf["building_id"] = gdf.index.astype(int)

    _buildings_gdf_cache = gdf
    return gdf


def load_rain_raster():
    """
    Open rainfall raster (GeoTIFF). Cached.
    Assumes CRS matches CANONICAL_CRS or close enough.
    """
    global _rain_raster_cache
    if _rain_raster_cache is not None:
        return _rain_raster_cache

    try:
        src = rasterio.open(RAINFALL_RASTER_PATH)
    except FileNotFoundError:
        src = None

    _rain_raster_cache = src
    return src


def sample_rainfall_mm_at_point(point):
    """
    Sample rainfall (mm/year) from raster at a shapely Point in CANONICAL_CRS.
    If raster missing or sample fails, returns AVERAGE_RAINFALL_MM_FALLBACK.
    
    The point should be in CANONICAL_CRS (EPSG:3857), but we may need to 
    transform to the raster's CRS if they differ.
    """
    raster = load_rain_raster()
    if raster is None:
        return AVERAGE_RAINFALL_MM_FALLBACK

    try:
        # Get the raster's CRS
        raster_crs = raster.crs
        
        # Transform point to raster CRS if needed
        if raster_crs is not None:
            from shapely.geometry import Point
            point_gdf = gpd.GeoDataFrame([1], geometry=[Point(point.x, point.y)], crs=CANONICAL_CRS)
            point_gdf = point_gdf.to_crs(raster_crs)
            x, y = point_gdf.geometry.iloc[0].x, point_gdf.geometry.iloc[0].y
        else:
            # Assume same CRS
            x, y = point.x, point.y
        
        # Sample the raster
        values = list(raster.sample([(x, y)]))
        if not values:
            return AVERAGE_RAINFALL_MM_FALLBACK
        val = float(values[0][0])
        
        # Handle NoData values
        if val == raster.nodata or val < 0:
            return AVERAGE_RAINFALL_MM_FALLBACK
            
        return val
    except Exception as e:
        print(f"Warning: Could not sample rainfall raster: {e}")
        return AVERAGE_RAINFALL_MM_FALLBACK
