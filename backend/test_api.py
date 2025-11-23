#!/usr/bin/env python3
"""
Test script for HydraX API
Run this to test the API with sample addresses
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_health():
    """Test the health endpoint"""
    print("Testing /api/health...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("  ERROR: Could not connect to server. Is Flask running?")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_estimate(address):
    """Test the estimate endpoint with an address"""
    print(f"\nTesting /api/estimate with address: '{address}'...")
    try:
        params = {"address": address}
        response = requests.get(f"{BASE_URL}/api/estimate", params=params, timeout=30)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n  ✅ SUCCESS! Response:")
            print(json.dumps(data, indent=2))
            
            # Print key metrics
            if "water_collection" in data:
                print("\n  📊 Key Metrics:")
                print(f"    - Annual Water Collection: {data['water_collection'].get('estimated_annual_yield_liters', 0):,.0f} liters")
                print(f"    - Roof Area: {data['building_info'].get('roof_area_m2', 0):.2f} m²")
                print(f"    - Annual Rainfall: {data['rainfall_data'].get('annual_rainfall_mm', 0):.1f} mm")
                
            if "hydrax_ai_assessment" in data:
                ai = data["hydrax_ai_assessment"]
                print(f"\n  🤖 AI Assessment:")
                print(f"    - Category: {ai.get('category', 'N/A')}")
                print(f"    - Score: {ai.get('score', 0):.2f}/1.0")
                print(f"    - Summary: {ai.get('summary', 'N/A')}")
                if "estimated_cost_savings" in ai:
                    savings = ai["estimated_cost_savings"]
                    print(f"    - Annual Savings: £{savings.get('annual_savings_gbp', 0):.2f}")
        else:
            print(f"  ❌ ERROR: {response.status_code}")
            print(f"  Response: {response.text}")
            
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("  ERROR: Could not connect to server. Is Flask running?")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def main():
    print("=" * 60)
    print("HydraX API Test Suite")
    print("=" * 60)
    
    # Test health endpoint
    if not test_health():
        print("\n❌ Health check failed. Make sure Flask is running:")
        print("   python app.py")
        sys.exit(1)
    
    # Test with various London addresses
    test_addresses = [
        "10 Downing Street, London",
        "Tower Bridge, London",
        "Buckingham Palace, London",
        "221B Baker Street, London",
    ]
    
    print("\n" + "=" * 60)
    print("Testing Estimate Endpoint")
    print("=" * 60)
    
    success_count = 0
    for address in test_addresses:
        if test_estimate(address):
            success_count += 1
        print("\n" + "-" * 60)
    
    print(f"\n{'=' * 60}")
    print(f"Tests completed: {success_count}/{len(test_addresses)} successful")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()

