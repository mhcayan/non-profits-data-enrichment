from geopy.geocoders import Nominatim

def get_lat_lon(address):

    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(address)
    
    if location:
        return location.latitude, location.longitude
    else:
        return None

# Example Usage
# address = "1600 Amphitheatre Parkway, Mountain View, CA"
address = '6811 JEFFERSON HWY, BATON ROUGE, LA, 70806'
print(address)
coords = get_lat_lon(address)

if coords:
    print(f"Latitude: {coords[0]}, Longitude: {coords[1]}")
else:
    print("Address not found.")