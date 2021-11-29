function initMap() {

    map = new google.maps.Map(document.getElementById("map"), {
        mapId: "791b24b8f922f472",
        center: { lat: 33.86537244179991, lng: -83.91752444330994 },
        zoom: 14,
    });
    //Name
    //Longitude
    //Latitude
    const markers = [
        ["place", 33.86537244179991, -83.91752444330994],
        ["place", 33.86759128901652, -83.91892051447431],
    ]
    for (let i = 0; i < markers.length; i++) {
        const currentMarker = markers[i];
        new google.maps.Marker({
            position: { lat: currentMarker[1], lng: currentMarker[2] },
            map,
            title: currentMarker[0],
        });
    }

}
//33.86537244179991, -83.91752444330994
//33.86759128901652, -83.91892051447431
//33.86823838880674, -83.92395172543416
//33.87888009586928, -83.93841400387005