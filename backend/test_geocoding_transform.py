# Simple smoke test to show transformer expects (lon, lat)
from services import geocoding_service


def show(lat, lng):
    # Correct usage: (lon, lat)
    correct = geocoding_service.transformer.transform(lng, lat)
    # Incorrect (swapped) usage: (lat, lon)
    swapped = geocoding_service.transformer.transform(lat, lng)
    print(f"lat={lat}, lng={lng}\n  correct(easting,northing) = {correct}\n  swapped(easting,northing) = {swapped}\n")


if __name__ == "__main__":
    # Two sample London coordinates
    samples = [
        (51.5074, -0.1278),  # central London
        (51.5155, -0.1419),  # near Tottenham Court Rd / Fitzrovia
    ]

    for lat, lng in samples:
        show(lat, lng)
