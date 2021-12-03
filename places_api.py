import requests
import json
import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())
PLACES_API_KEY = os.getenv("PLACES_API_KEY")

# url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=4825%20dunwoody%20station%20drive&key=ENTER_API_KEY"

# fetch address, latitude & longitude coords from Places API
def getPlaceInfo(placeName):
    url = (
        "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
        + placeName
        + "&key="
        + PLACES_API_KEY
    )

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    # convert to json so we can pull out data
    json_data = json.loads(response.text)

    try:
        # getting relevant data out of json
        address = json_data["results"][0]["formatted_address"]
        latitude = json_data["results"][0]["geometry"]["location"]["lat"]
        longitude = json_data["results"][0]["geometry"]["location"]["lng"]
        name = json_data["results"][0]["name"]

        print("Address   ========= " + address)
        print("Latitude  ========= ", latitude)
        print("Longitude ========= ", longitude)
        print("Name ========= ", name)

        # return place info in list
        return {"address": address, "lat": latitude, "lon": longitude, "name": name}
        # return [address, latitude, longitude, name]
    except KeyError:
        print(" !!! PLACES API FETCH FAILED !!!")
        return {"address": "ERROR", "lat": "ERROR", "lon": "ERROR", "name": "ERROR"}


#print (getPlaceInfo("vermack pool"))
