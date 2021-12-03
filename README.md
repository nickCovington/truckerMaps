# Trucker Maps

Creators: Amanuel Larebo, Kofi Osae, Sai Tippana, Nicholas Covington

## Deployment Link
Sprint 1: 
https://still-beyond-26695.herokuapp.com/

Sprint 2:
TO-DO: make new heroku link

## Purpose
TruckerMaps is a logistics tool meant to help truckers by giving them an organized view of warehouses they need to reach and the time they need to be there by. 
It uses the Google Places API to ensure that the truckers are receiving quick and consistent location data and getting them to the correct location on time.
It uses the Google Maps API to give the truckers an interactive map widget which they can use to view their target locations and nearby routes.

## User Experience
Insert user stories, ideal usage, and UI navigation.

- Users will be met with a login screen where they can either sign into their account or create a new one.
- Next they will be greeted with the main dashboard navigation system. 
    - View deliveries, add locations, view/edit profile
- Delivery page: lists all current deliveries and their status 'on-time / late'
- Add Location: form for user to search an address and add it to their saved locations
- Profile: edit details such as name, email, phone, password, etc

## User Stories
- As an average user, you will be able to select a target warehouse location from Google Places to view its respective delivery data.
    - User can search for warehouse location
    - When a warehouse is clicked, user can see warehouse name
    - When a warehouse is clicked, user can see warehouse deliveries
    - When a warehouse is clicked, user can see warehouse coordinates/address
    - When a warehouse is clicked, list drivers that have delivered there

- As an average user, I can write a log of my delivery to explain why a shipment was late/damaged
    - Text submission form for trucker to leave delivery description
    - Trucker’s can view/edit log
    - Late deliveries will have option beside them to read trucker’s log

- As an average user, I can interact with a map in order to help me see the surrounding location features and determine if it's the correct area.
    - zoom in/out
    - scroll or pan around map area
    - view names and location info of nearby places/landmarks



## Cloning and usage
Note: to use this app properly, you will need to register for a Google dev account, create a new project, authenticate your account & on your project enable the Google Places API and the Google Maps Embed API.

To contribute to this app you will need to use your own Google API key.

`git clone https://github.com/nickCovington/truckerMaps.git`

`pip install flask`
`pip install flask-wtf`
`pip install python-dotenv`
`pip install flask-sqlalchemy`
`pip install requests`
`pip install flask-login`
`pip install postgres`




