import requests

def get_census_tract(longitude, latitude):
    url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates"
    params = {
        "x": longitude,
        "y": latitude,
        "benchmark": "8",
        "vintage": "8",
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    try:
        tract_info = data["result"]["geographies"]["Census Tracts"][0]
        return {
            "STATE_CODE": tract_info["STATE"],
            "CENTLON": tract_info["CENTLON"],
            "GEOID": tract_info["GEOID"],
            "CENTLAT": tract_info["CENTLAT"],
            "COUNTY_CODE": tract_info["COUNTY"],
            "TRACT_CODE": tract_info["TRACT"],
            "AREAWATER": tract_info["AREAWATER"],
            "AREALAND": tract_info["AREALAND"],
            "TRACT_NAME": tract_info["NAME"]
        }
    except (KeyError, IndexError):
        return None

if __name__ == "__main__":
    # Example coordinates for Baton Rouge, LA
    latitude = 30.3728
    longitude = -91.147385
    
    tract_info = get_census_tract(longitude, latitude)
    
    if tract_info:
        print("Census Tract Info:")
        for key, value in tract_info.items():
            print(f"{key}: {value}")
    else:
        print("No census tract data found for the given coordinates.")
