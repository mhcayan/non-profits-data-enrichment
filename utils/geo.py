from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="nonprofit_geocoder", timeout=3)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


def geocode_address(address):
    try:
        location = geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None, None

if __name__ == "__main__":
    test_address = "1600 Pennsylvania Avenue NW, Washington, DC"
    # test_address = "70820"
    lat, lon = geocode_address(test_address)
    print(f"Latitude: {lat}, Longitude: {lon}")