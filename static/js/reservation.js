const VEHICULE_PRICE_KM = JSON.parse(document.getElementById("vehicule-price-km").textContent);
const VEHICULE_PRICE_HOUR = JSON.parse(document.getElementById("vehicule-price-hour").textContent);
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
        opt.dataset.priceKm = VEHICULE_PRICE_KM[opt.value] ?? 0;
        opt.dataset.priceHour = VEHICULE_PRICE_HOUR[opt.value] ?? 0
        opt.dataset.seats = VEHICULE_SEATS[opt.value] ?? 0;
    });

    /* ================= MAP ================= */
    mapboxgl.accessToken = document.getElementById("map").dataset.mapboxToken;
    const map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/mapbox/streets-v12",
        center: [2.35,48.85],
        zoom: 11
    });

    map.on("load", () => {
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
                "line-color": "#0077ff"
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
        const box = document.getElementById(suggestionsId);

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
                    if (type === "end") {
                        setTripType(1);
                    }
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
    function setupPoi(selectId, type) {
        const select = document.getElementById(selectId);
        const cat = select.dataset.category;

        select.addEventListener("change", () => {
            const poi = POIS[cat][select.value];
            if (!poi) return;

            const addressInput = document.getElementById(`id_address_${type}`);
            const durationInput = document.getElementById("duration");
            const distanceInput = document.getElementById("distance");
            const infoDiv = document.getElementById("route-info-2");

            /* ================= MISE À DISPOSITION ================= */
            if (cat === "mise_dis") {
                isMiseDis = true;
                setTripType(2); // ride

                // reset trajet
                addressInput.value = "";
                durationInput.value = poi.value * 60;
                currentDistanceKm = 0;
                distanceInput.value = 0;
                endCoords = null;

                if (map.getSource("route")) {
                    map.getSource("route").setData({
                        type: "FeatureCollection",
                        features: []
                    });
                }

                refreshMarkers();
                updatePrice();
                return;
            }

            /* ================= TRAJET CLASSIQUE ================= */
            isMiseDis = false;

            addressInput.value = poi.address;

            if (type === "start") {
                startCoords = poi.coords;
            } else {
                endCoords = poi.coords;
                setTripType(1); // simple
            }

            currentDistanceKm = 0;
            distanceInput.value = 0;

            drawRoute();
            refreshMarkers();
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

    function setTripType(value) {
        const tripInput = document.getElementById("trip_type");
        if (!tripInput) return;
        tripInput.value = value;
    }
    document.getElementById("id_address_end").addEventListener("input", () => {
        if (!isMiseDis) {
            setTripType(1);
        }
    });


    /* ================= ROUTE ================= */
    async function drawRoute(){
        if(isMiseDis || !startCoords || !endCoords) return;
        if(!mapLoaded) return;

        const url =
            `https://api.mapbox.com/directions/v5/mapbox/driving/` +
            `${startCoords[0]},${startCoords[1]};${endCoords[0]},${endCoords[1]}` +
            `?geometries=geojson&overview=full` +
            `&access_token=${mapboxgl.accessToken}`;

        try{
            const res = await fetch(url);
            const json = await res.json();
            if(!json.routes?.length) return;

            const route = json.routes[0];
            currentDistanceKm = route.distance / 1000;
            document.getElementById("distance").value = currentDistanceKm.toFixed(2);
            document.getElementById("duration").value = Math.round(route.duration / 60);

            map.getSource("route").setData({
                type:"FeatureCollection",
                features:[{
                    type:"Feature",
                    geometry: route.geometry
                }]
            });

            map.fitBounds([startCoords,endCoords],{padding:60});
            refreshMarkers();
            updatePrice();

        }catch(err){
            console.error(err);
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
    function formatMinutes(minutes) {
        minutes = parseInt(minutes) || 0;
        if (minutes < 60) return `${minutes} min`;

        const hours = Math.floor(minutes / 60);
        const remaining = minutes % 60;

        if (remaining === 0) return `${hours} h`;
        return `${hours} h ${remaining} min`;
    }

    function updatePrice(){
        const opt = carSelect.selectedOptions[0];
        if(!opt) return;
        let price = 0;

        if(isMiseDis){
            // Tarif horaire
            const hoursSelect = document.getElementById("end_mise_dis");
            const hours = parseInt(hoursSelect?.value || 1);

            const priceHour = parseFloat(opt.dataset.priceHour) || 0;
            price = hours * priceHour;
        } else {
            const priceKm = parseFloat(opt.dataset.priceKm) || 0;
            price = currentDistanceKm * priceKm;
        }

        document.getElementById("price").value = price.toFixed(2);

        // Récupère la durée brute
        const duration = parseInt(document.getElementById("duration").value) || 0;
        const info = document.getElementById("route-info-2");

        if(isMiseDis){
            info.innerHTML = `Mise à disposition : ${price.toFixed(2)} €`;
        } else {
            info.innerHTML = `Durée estimée : ${formatMinutes(duration)} — Prix estimé : ${price.toFixed(2)} €`;
        }

        info.dataset.visible = "true";
    }

    carSelect.addEventListener("change", updatePrice);

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


    carSelect.addEventListener("change", ()=>{
        validatePassengers();
        validateLuggages();
        updatePrice();
    });
});
