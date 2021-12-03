function initMap() {
    
    map = new google.maps.Map(document.getElementById("map"), {
        mapId: "791b24b8f922f472",
        center: { lat: 33.86537244179991, lng: -83.91752444330994 },
        zoom: 8,
    });
    //Name
    //Longitude
    //Latitude
    const markers = {
        1: [33.9912373, -83.9304757, "Publix-Atlanta Warehouse"], 
        2: [33.8392384, -83.9080992, "Publix Super Market at Loganville Town Centre"], 
        3: [33.7404975, -84.5731201, "Publix Bakery Plant"], 
        4: [33.9414943, -84.2131407, "Publix Employees Federal Credit Union"], 
        5: [34.0368919, -84.04242699999999, "Publix Facility Services"], 
        6: [33.9220009, -84.4775368, "Publix Super Markets Corporate"], 
        7: [33.9844304, -83.9847703, "840 Buford Dr"]
    }
        
    for (let i in markers) {
        const currentMarker = markers[i];
        new google.maps.Marker({
            position: { lat: currentMarker[0], lng: currentMarker[1] },
            map,
            title: currentMarker[2],
        });
    }

}
/**
 * get the coordinates from the db and put that into an array
 * Loop the array using jinja syntax
 */