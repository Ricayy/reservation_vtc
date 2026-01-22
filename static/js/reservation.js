const VEHICULE_PRICES = JSON.parse(document.getElementById("vehicule-prices").textContent);
const VEHICULE_SEATS  = JSON.parse(document.getElementById("vehicule-seats").textContent);

/* ================= POIS CENTRALISÉS ================= */
const POIS = {
    aeroport: {
        cdg: { label: "Aéroport CDG", address: "Aéroport Charles de Gaulle, Roissy", coords: [2.5479,49.0097] },
        orly: { label: "Aéroport Orly", address: "Aéroport d'Orly, Orly", coords: [2.3790,48.7262] }
    },
    gare: {
        gdl: { label: "Gare de Lyon", address: "Gare de Lyon, Paris", coords: [2.3730,48.8443] },
        gdn: { label: "Gare du Nord", address: "Gare du Nord, Paris", coords: [2.3553,48.8809] }
    },
    loisir: {
        disney: { label: "Disneyland Paris", address: "Disneyland Paris, Chessy", coords: [2.7840,48.8708] },
        asterix: { label: "Parc Astérix", address: "Parc Astérix, Plailly", coords: [2.5961,49.1341] }
    },
    mise_dis: {
        1: { label: "1 heure", value: 1},
        2: { label: "2 heures", value: 2},
        3: { label: "3 heures", value: 3},
        4: { label: "4 heures", value: 4},
        5: { label: "5 heures", value: 5},
        6: { label: "6 heures", value: 6},
        7: { label: "7 heures", value: 7},
        8: { label: "8 heures", value: 8},
        9: { label: "9 heures", value: 9},
        10: { label: "10 heures", value: 10},
        11: { label: "11 heures", value: 11},
        12: { label: "12 heures", value: 12},
    },
};

/* ================= INIT ================= */
document.addEventListener("DOMContentLoaded", () => {
    let mapLoaded = false;
    let isMiseDis = false;
    let startCoords = null, endCoords = null, currentDistanceKm = 0;
    let startMarker = null, endMarker = null;

    // Initialisation distance et prix
    document.getElementById("distance").value = 0;
    document.getElementById("price").value = 0;

    // Initialisation véhicules
    const carSelect = document.getElementById("id_car_type");
    [...carSelect.options].forEach(opt => {
        if (!opt.value) return;
        opt.dataset.price = VEHICULE_PRICES[opt.value] ?? 0;
        opt.dataset.seats = VEHICULE_SEATS[opt.value] ?? 0;
    });

    // Map
    mapboxgl.accessToken = document.getElementById("map").dataset.mapboxToken;
    const map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/mapbox/streets-v12",
        center: [2.35,48.85],
        zoom: 11
    });


    map.on("load", () => {
//        map.addSource("route", { type:"geojson", data:{ type:"FeatureCollection", features:[] } });
//        map.addLayer({ id:"route", type:"line", source:"route", paint:{ "line-width":6, "line-color":"#0077ff" }});

        mapLoaded = true;
        map.addSource("route", {
            type: "geojson",
            data: { type:"FeatureCollection", features:[] }
        });

        map.addLayer({
            id: "route",
            type: "line",
            source: "route",
            paint: {
                "line-width": 6,
                "line-color": [
                    "coalesce",
                    ["get", "color"],
                    "#0077ff"
                ]
            }
        });
    });

    function updateMarker(markerVar, coords, color="blue") {
        if (!coords) return markerVar;
        if (markerVar) markerVar.setLngLat(coords);
        else markerVar = new mapboxgl.Marker({ color }).setLngLat(coords).addTo(map);
        return markerVar;
    }

    function refreshMarkers() {
        startMarker = updateMarker(startMarker, startCoords, "green");
        endMarker   = updateMarker(endMarker, endCoords, "red");
    }

    /* ================= AUTOCOMPLETE ================= */
    function setupAutocomplete(inputId, suggestionsId, type){
        const input = document.getElementById(inputId);
        const box   = document.getElementById(suggestionsId);

        input.addEventListener("input", async ()=>{
            if(input.value.length<3){ box.style.display="none"; return; }
            const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(input.value)}.json?autocomplete=true&limit=5&language=fr&country=fr&access_token=${mapboxgl.accessToken}`;
            const res = await fetch(url);
            const data = await res.json();
            if(!data.features) return;

            box.innerHTML = "";
            box.style.display = "block";

            data.features.forEach(f=>{
                const div = document.createElement("div");
                div.textContent = f.place_name;
                div.onclick = ()=>{
                    input.value = f.place_name;
                    box.style.display = "none";

                    if(type==="start") startCoords = f.geometry.coordinates;
                    else endCoords = f.geometry.coordinates;

                    isMiseDis = false;
                    refreshMarkers();
                    drawRoute();
                };
                box.appendChild(div);
            });
        });
    }

    setupAutocomplete("id_address_start", "suggestions_start", "start");
    setupAutocomplete("id_address_end", "suggestions_end", "end");

    /* ================= POI SELECT ================= */
    function setupPoi(selectId, type){
        const select = document.getElementById(selectId);
        const cat = select.dataset.category;

        select.addEventListener("change", ()=>{
            const poi = POIS[cat][select.value];
            if(!poi) return;
            const input = document.getElementById(`id_address_${type}`);

            if(cat === "mise_dis") {
                // Mise à disposition
                input.value = poi.label;
                isMiseDis = true;
                currentDistanceKm = 0;
                endCoords = null;
                map.getSource("route").setData({ type:"FeatureCollection", features:[] });
                refreshMarkers();
                updatePrice();
            } else {
                // POI classique => traite comme adresse
                input.value = poi.address;
                if(type==="start") startCoords = poi.coords;
                else endCoords = poi.coords;
                isMiseDis = false;
                refreshMarkers();
                drawRoute();
            }
        });
    }

    ["start","end"].forEach(prefix=>{
        ["aeroport","gare","loisir","mise_dis"].forEach(cat=>{
            const select = document.getElementById(`${prefix}_${cat}`);
            select.dataset.category = cat;

            for(let key in POIS[cat]){
                const opt = document.createElement("option");
                opt.value = key;
                opt.textContent = POIS[cat][key].label;
                select.appendChild(opt);
            }
            setupPoi(`${prefix}_${cat}`, prefix);
        });
    });

    /* ================= TOGGLE UI ================= */
    document.querySelectorAll(".address-toggle button").forEach(btn=>{
        btn.addEventListener("click", ()=>{
            const target = btn.dataset.target;
            const mode   = btn.dataset.mode;

            document.getElementById(`id_address_${target}`).hidden = mode!=="address";
            ["aeroport","gare","loisir","mise_dis"].forEach(c=>{
                const s = document.getElementById(`${target}_${c}`);
                if(s) s.hidden = (mode!==c);
            });
        });
    });

    /* ================= ROUTE ================= */
    function colorByCongestion(level){
        switch(level){
            case "low": return "#2ecc71";
            case "moderate": return "#f1c40f";
            case "heavy": return "#e67e22";
            case "severe": return "#e74c3c";
            default: return "#3498db";
        }
    }

    async function drawRoute() {
        if (isMiseDis || !startCoords || !endCoords) return;
        if (!mapLoaded || !map.getSource("route")) return;

        const dateInput = document.getElementById("id_date_start").value;
        const timeInput = document.getElementById("id_time_start").value;
        if (!dateInput || !timeInput) return;

        const departAt = `${dateInput}T${timeInput}`;

        const url =
            `https://api.mapbox.com/directions/v5/mapbox/driving-traffic/` +
            `${startCoords[0]},${startCoords[1]};${endCoords[0]},${endCoords[1]}` +
            `?geometries=geojson&overview=full&annotations=duration,congestion` +
            `&depart_at=${encodeURIComponent(departAt)}` +
            `&access_token=${mapboxgl.accessToken}`;

        try {
            const res = await fetch(url);
            const json = await res.json();

            if (!json.routes || !json.routes.length) {
                console.warn("Aucun itinéraire retourné par Mapbox", json);
                return;
            }

            const route = json.routes[0];

            /* ===== DISTANCE ===== */
            currentDistanceKm = route.distance / 1000;
            document.getElementById("distance").value =
                currentDistanceKm.toFixed(2);

            /* ===== DURÉE ===== */
            const durationMin = Math.round(route.duration / 60);
            document.getElementById("duration").value = durationMin;

            /* ===== ROUTE COLORÉE ===== */
            const coords = route.geometry.coordinates;
            const congestions =
                route.legs?.[0]?.annotation?.congestion || [];

            const features = [];
            for (let i = 0; i < coords.length - 1; i++) {
                features.push({
                    type: "Feature",
                    geometry: {
                        type: "LineString",
                        coordinates: [coords[i], coords[i + 1]]
                    },
                    properties: {
                        color: colorByCongestion(congestions[i])
                    }
                });
            }

            map.getSource("route").setData({
                type: "FeatureCollection",
                features
            });

            map.fitBounds([startCoords, endCoords], { padding: 60 });

            refreshMarkers();
            updatePrice();

            document.getElementById("route-info").innerHTML =
                `Durée estimée : ${durationMin} min (trafic inclus)`;
            updateRouteInfoVisibility();

        } catch (err) {
            console.error("Erreur calcul itinéraire :", err);
        }
    }


    function updateRouteInfoVisibility(){
        const info1 = document.getElementById("route-info");
        const info2 = document.getElementById("route-info-2");

        info1.dataset.visible = info1.innerHTML.trim() !== "";
        info2.dataset.visible = info2.innerHTML.trim() !== "";
    }

    document.getElementById("id_date_start").addEventListener("change", () => {
        drawRoute();
    });

    document.getElementById("id_time_start").addEventListener("change", () => {
        drawRoute();
    });



    /* ================= PRIX ================= */
    function updatePrice(){
        const opt = carSelect.selectedOptions[0];
        if(!opt) return;
        const tripType = document.getElementById("id_trip_type").value;
        let price = 0;

        if(isMiseDis){
            // Tarif horaire
            const hoursSelect = document.getElementById("end_mise_dis");
            const hours = parseInt(hoursSelect?.value || 1);

            const vehiculeType = carSelect.value.toLowerCase();
            console.log(carSelect.value.toLowerCase())
            let rate = 45;
            if(vehiculeType.includes(2)) rate = 60;
            price = hours * rate;
        } else {
            const priceKm = parseFloat(opt.dataset.price);
            price = currentDistanceKm * priceKm * (tripType==="2"?2:1);
        }

        document.getElementById("price").value = price.toFixed(2);
        const info = document.getElementById("route-info-2");
        if(isMiseDis){
            info.innerHTML = `Mise à disposition : ${price.toFixed(2)} €`;
        } else {
            info.innerHTML = `Distance : ${currentDistanceKm.toFixed(2)} km — Prix estimé : ${price.toFixed(2)} €`;
        }
        info.dataset.visible="true";
    }

    carSelect.addEventListener("change", updatePrice);
    document.getElementById("id_trip_type").addEventListener("change", updatePrice);

    /* ================= VALIDATION PASSAGERS & BAGAGES ================= */
    const passengerInput = document.getElementById("id_nb_passengers");
    const luggageInput = document.getElementById("id_nb_luggages");

    function validatePassengers() {
        const nb = parseInt(passengerInput.value || 1);
        const selectedOption = carSelect.options[carSelect.selectedIndex];
        if (!selectedOption) return;
        const maxSeats = parseInt(selectedOption.dataset.seats);
        passengerInput.value = Math.min(Math.max(nb,1), maxSeats, 7);
    }

    function validateLuggages() {
        const selectedOption = carSelect.options[carSelect.selectedIndex];
        if (!selectedOption) return;
        const nb = parseInt(luggageInput.value || 0);
        luggageInput.value = Math.min(Math.max(nb,0),10);
    }

    passengerInput.addEventListener("input", validatePassengers);
    luggageInput.addEventListener("input", validateLuggages);
    function consoleTest() {
        console.log("id_address_start " + document.getElementById("id_address_start").value);
        console.log("id_address_end " + document.getElementById("id_address_end").value);
        console.log("duration " + document.getElementById("duration").value);
        console.log("distance " + document.getElementById("distance").value);
        console.log("price " + document.getElementById("price").value);
        console.log("end_mise_dis " + document.getElementById("end_mise_dis").value);
        console.log("id_car_type " + document.getElementById("id_car_type").value);
        console.log("id_trip_type " + document.getElementById("id_trip_type").value);
        console.log("id_date_start " + document.getElementById("id_date_start").value);
        console.log("id_time_start " + document.getElementById("id_time_start").value);
    }
    carSelect.addEventListener("change", ()=>{
        validatePassengers();
        validateLuggages();
        updatePrice();
        consoleTest();
    });
});
