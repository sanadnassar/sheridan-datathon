import geopandas as gpd

def load_rooftops(shapefile_path="backend/data/TQ_Building.shp"):
    # Load the OS building footprint shapefile
    gdf = gpd.read_file(shapefile_path)

    # Convert to meters for correct area calculations
    gdf = gdf.to_crs(epsg=3857)

    # Add building area in m2
    gdf["area_m2"] = gdf.geometry.area

    # Give each building a unique ID if none exists
    if "id" not in gdf.columns:
        gdf["id"] = gdf.index.astype(int)

    return gdf