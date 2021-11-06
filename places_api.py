import requests

# url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=4825%20dunwoody%20station%20drive&key=ENTER_API_KEY"

# payload = {}
# headers = {}

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)


def getPlaceInfo(placeName):
    url = (
        "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
        + placeName
        + "&key=ENTER_API_KEY"
    )

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


getPlaceInfo("4815 dunwoody station drive")
