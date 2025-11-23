# backend/services/rainfall_service.py

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Runoff coefficient for UK roofs
RUNOFF_COEFF = 0.9


def load_weather_data(csv_path: str = "data/london_weather.csv") -> pd.DataFrame:
    """
    Load and process London weather data from CSV.
    
    Args:
        csv_path: Path to the weather CSV file
        
    Returns:
        DataFrame with processed weather data
    """
    # Handle relative paths
    if not os.path.isabs(csv_path) and not os.path.exists(csv_path):
        alt_paths = [
            os.path.join(os.path.dirname(__file__), "..", csv_path),
            csv_path
        ]
        for alt_path in alt_paths:
            if os.path.exists(alt_path):
                csv_path = alt_path
                break
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Weather data file not found: {csv_path}")
    
    # Load CSV
    df = pd.read_csv(csv_path)
    
    # Parse date column (format: YYYYMMDD)
    df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
    
    # Extract year and month
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    
    # Handle missing precipitation values (fill with 0)
    df['precipitation'] = pd.to_numeric(df['precipitation'], errors='coerce').fillna(0)
    
    return df


def calculate_annual_rainfall_collection(building_area_m2: float, 
                                        csv_path: str = "data/london_weather.csv") -> Dict:
    """
    Calculate annual rainfall collection for a building using historical data.
    
    Args:
        building_area_m2: Building rooftop area in square meters
        csv_path: Path to the weather CSV file
        
    Returns:
        Dictionary with annual rainfall collection data
    """
    df = load_weather_data(csv_path)
    
    # Calculate annual precipitation (sum of daily precipitation per year)
    annual_precipitation = df.groupby('year')['precipitation'].sum()
    
    # Calculate annual collection in liters
    # Formula: area (m²) * annual_rainfall (mm) / 1000 * runoff_coefficient * 1000
    annual_collection = {}
    for year, rainfall_mm in annual_precipitation.items():
        # Convert mm to meters, multiply by area, apply runoff coefficient, convert to liters
        liters = building_area_m2 * (rainfall_mm / 1000) * RUNOFF_COEFF * 1000
        annual_collection[int(year)] = {
            "rainfall_mm": float(rainfall_mm),
            "collection_liters": float(liters)
        }
    
    # Calculate average annual collection
    avg_annual_rainfall = annual_precipitation.mean()
    avg_annual_collection = building_area_m2 * (avg_annual_rainfall / 1000) * RUNOFF_COEFF * 1000
    
    return {
        "annual_data": annual_collection,
        "average_annual_rainfall_mm": float(avg_annual_rainfall),
        "average_annual_collection_liters": float(avg_annual_collection),
        "years_available": sorted(annual_collection.keys())
    }


def predict_future_rainfall(csv_path: str = "data/london_weather.csv", 
                           years_ahead: int = 10) -> Dict:
    """
    Use ML to predict annual rainfall for the next N years.
    
    Args:
        csv_path: Path to the weather CSV file
        years_ahead: Number of years to predict ahead
        
    Returns:
        Dictionary with predicted annual rainfall (in mm) for each future year
    """
    df = load_weather_data(csv_path)
    
    # Calculate annual precipitation
    annual_precipitation = df.groupby('year')['precipitation'].sum().reset_index()
    annual_precipitation.columns = ['year', 'annual_rainfall_mm']
    
    # Prepare features for ML model
    # Use year as feature, but also create lag features and rolling statistics
    annual_precipitation = annual_precipitation.sort_values('year')
    
    # Create features: year, lag-1, lag-2, rolling mean (3 years), rolling std (3 years)
    annual_precipitation['lag1'] = annual_precipitation['annual_rainfall_mm'].shift(1)
    annual_precipitation['lag2'] = annual_precipitation['annual_rainfall_mm'].shift(2)
    annual_precipitation['rolling_mean'] = annual_precipitation['annual_rainfall_mm'].rolling(window=3, min_periods=1).mean()
    annual_precipitation['rolling_std'] = annual_precipitation['annual_rainfall_mm'].rolling(window=3, min_periods=1).std()
    
    # Drop rows with NaN (from lag features)
    annual_precipitation = annual_precipitation.dropna()
    
    if len(annual_precipitation) < 3:
        # Fallback: simple linear trend if not enough data
        return _simple_linear_prediction(annual_precipitation, years_ahead)
    
    # Prepare training data
    X = annual_precipitation[['year', 'lag1', 'lag2', 'rolling_mean', 'rolling_std']].values
    y = annual_precipitation['annual_rainfall_mm'].values
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_scaled, y)
    
    # Get last year and prepare for prediction
    last_year = annual_precipitation['year'].max()
    last_rainfall = annual_precipitation[annual_precipitation['year'] == last_year]['annual_rainfall_mm'].values[0]
    last_lag1 = annual_precipitation[annual_precipitation['year'] == last_year]['lag1'].values[0]
    last_rolling_mean = annual_precipitation[annual_precipitation['year'] == last_year]['rolling_mean'].values[0]
    last_rolling_std = annual_precipitation[annual_precipitation['year'] == last_year]['rolling_std'].values[0]
    
    # Predict future years
    predictions = {}
    current_lag1 = last_rainfall
    current_lag2 = last_lag1
    current_rolling_mean = last_rolling_mean
    current_rolling_std = last_rolling_std
    
    for i in range(1, years_ahead + 1):
        future_year = last_year + i
        
        # Prepare features for this year
        features = np.array([[future_year, current_lag1, current_lag2, current_rolling_mean, current_rolling_std]])
        features_scaled = scaler.transform(features)
        
        # Predict
        predicted_rainfall = model.predict(features_scaled)[0]
        predictions[int(future_year)] = float(max(0, predicted_rainfall))  # Ensure non-negative
        
        # Update for next iteration
        current_lag2 = current_lag1
        current_lag1 = predicted_rainfall
        # Update rolling statistics (simplified)
        current_rolling_mean = (current_rolling_mean * 2 + predicted_rainfall) / 3
        if current_rolling_std > 0:
            current_rolling_std = current_rolling_std * 0.95  # Slight decay
    
    return predictions


def _simple_linear_prediction(annual_precipitation: pd.DataFrame, years_ahead: int) -> Dict:
    """
    Fallback prediction using simple linear trend.
    """
    last_year = annual_precipitation['year'].max()
    avg_rainfall = annual_precipitation['annual_rainfall_mm'].mean()
    
    predictions = {}
    for i in range(1, years_ahead + 1):
        predictions[int(last_year + i)] = float(avg_rainfall)
    
    return predictions


def calculate_predicted_collection(building_area_m2: float,
                                  predicted_rainfall: Dict) -> Dict:
    """
    Calculate predicted annual collection in liters based on predicted rainfall.
    
    Args:
        building_area_m2: Building rooftop area in square meters
        predicted_rainfall: Dictionary with year -> predicted_rainfall_mm
        
    Returns:
        Dictionary with predicted collection for each year
    """
    predicted_collection = {}
    for year, rainfall_mm in predicted_rainfall.items():
        liters = building_area_m2 * (rainfall_mm / 1000) * RUNOFF_COEFF * 1000
        predicted_collection[year] = {
            "predicted_rainfall_mm": rainfall_mm,
            "predicted_collection_liters": float(liters)
        }
    
    return predicted_collection

