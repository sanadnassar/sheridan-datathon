from services.geocoding_service import geocode_address, GeocodingError
from services.building_service import find_nearest_building, BuildingNotFoundError
from services.rainfall_service import get_current_year_rainfall_collection

addresses = [
    "10 Downing St, London",
    "221B Baker St, London"
]

for addr in addresses:
    print(f"Address: {addr}")
    try:
        easting, northing = geocode_address(addr)
        print(f"  easting,northing: ({easting:.2f}, {northing:.2f})")
    except GeocodingError as e:
        print(f"  GeocodingError: {e}")
        continue
    except Exception as e:
        print(f"  Unexpected geocode error: {e}")
        continue

    try:
        binfo = find_nearest_building(easting, northing)
        area = binfo.get("area")
        dist = binfo.get("distance")
        print(f"  building area: {area}, distance: {dist:.2f}")
    except BuildingNotFoundError as e:
        print(f"  BuildingNotFoundError: {e}")
        continue
    except Exception as e:
        print(f"  Unexpected building lookup error: {e}")
        continue

    try:
        current = get_current_year_rainfall_collection(area)
        print(f"  current_year_rainfall: {current}")
    except Exception as e:
        print(f"  Rainfall calc error: {e}")

    print('\n')
