import pandas as pd
import sqlite3

def load_rooftops(database_path="data/buildings.db"):
    """
    Load rooftop data from SQLite database.
    
    Args:
        database_path (str): Path to the SQLite database file
        
    Returns:
        pandas.DataFrame: DataFrame with columns ['lat', 'lon', 'area']
    """
    conn = sqlite3.connect(database_path)
    
    try:
        # Load rooftop data from database
        df = pd.read_sql_query(
            "SELECT lat, lon, area FROM rooftops", 
            conn
        )
        
        # Add building ID if none exists
        if "id" not in df.columns:
            df["id"] = df.index.astype(int)
            
        print(f"Loaded {len(df):,} rooftops from database")
        return df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()
        
    finally:
        conn.close()

def load_rooftops_sample(database_path="data/buildings.db", limit=10000):
    """
    Load a sample of rooftop data for faster processing during development.
    
    Args:
        database_path (str): Path to the SQLite database file
        limit (int): Maximum number of rows to load
        
    Returns:
        pandas.DataFrame: DataFrame with columns ['lat', 'lon', 'area', 'id']
    """
    conn = sqlite3.connect(database_path)
    
    try:
        # Load sample rooftop data from database
        df = pd.read_sql_query(
            f"SELECT lat, lon, area FROM rooftops LIMIT {limit}", 
            conn
        )
        
        # Add building ID
        df["id"] = df.index.astype(int)
            
        print(f"Loaded sample of {len(df):,} rooftops from database")
        return df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()
        
    finally:
        conn.close()