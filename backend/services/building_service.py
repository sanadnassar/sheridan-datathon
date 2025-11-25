# backend/services/building_service.py

import sqlite3
import math
from typing import Optional, Tuple
import os

class BuildingNotFoundError(Exception):
    """Raised when no building can be found."""
    pass


def find_nearest_building(easting: float, northing: float, database_path: str = "data/buildings.db") -> dict:
    """
    Find the nearest building to the given easting/northing coordinates.
    
    Note: The database stores coordinates in British National Grid (OSGB36, EPSG:27700)
    format, even though the columns are named 'lat' and 'lon'.
    
    Args:
        easting: Easting coordinate in British National Grid (OSGB36, EPSG:27700)
        northing: Northing coordinate in British National Grid (OSGB36, EPSG:27700)
        database_path: Path to the buildings database
        
    Returns:
        dict: Dictionary containing 'area' (in sq m) and optionally 'distance' (in meters)
        
    Raises:
        BuildingNotFoundError: If no buildings are found in the database
    """
    # Handle relative path - if running from backend directory, use data/buildings.db
    if not os.path.isabs(database_path) and not os.path.exists(database_path):
        # Try alternative paths
        alt_paths = [
            os.path.join(os.path.dirname(__file__), "..", database_path),
            database_path
        ]
        for alt_path in alt_paths:
            if os.path.exists(alt_path):
                database_path = alt_path
                break
    
    if not os.path.exists(database_path):
        raise BuildingNotFoundError(f"Database file not found: {database_path}")
    
    conn = sqlite3.connect(database_path)
    
    try:
        # Load all buildings from database
        # Columns should be named 'easting' and 'northing' for clarity
        cursor = conn.cursor()
        cursor.execute("SELECT easting, northing, area FROM rooftops")
        buildings = cursor.fetchall()

        if not buildings:
            raise BuildingNotFoundError("No buildings found in database")

        # Find the nearest building
        min_distance = float('inf')
        nearest_area = None

        for db_easting, db_northing, area in buildings:
            # Calculate Euclidean distance in meters (since both are in OSGB36)
            # The database columns are easting, northing (matching the geocoded
            # output) so use them directly.
            distance = math.sqrt(
                (easting - db_easting) ** 2 + 
                (northing - db_northing) ** 2
            )
            if distance < min_distance:
                min_distance = distance
                nearest_area = area

        if nearest_area is None:
            raise BuildingNotFoundError("Could not find nearest building")

        return {
            "area": nearest_area,
            "distance": min_distance
        }
    except sqlite3.Error as e:
        raise BuildingNotFoundError(f"Database error: {e}")
    finally:
        conn.close()

