import requests

url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=123%20main%20street&key=YOUR_API_KEY"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
