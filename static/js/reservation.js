const VEHICULE_PRICE_KM = JSON.parse(document.getElementById("vehicule-price-km").textContent);
const VEHICULE_PRICE_HOUR = JSON.parse(document.getElementById("vehicule-price-hour").textContent);
const VEHICULE_SEATS = JSON.parse(document.getElementById("vehicule-seats").textContent);
const VEHICULE_DATA = JSON.parse(document.getElementById("vehicule-data").textContent);
const TRIP_DATA = JSON.parse(document.getElementById("trip-data").textContent);

/* ================= POIS CENTRALISÉS ================= */
const POIS = {
    aeroport: {
        charles_de_gaulle: { label: "Aéroport CDG", address: "Aéroport Charles de Gaulle, Roissy", coords: [2.5479,49.0097] },
        orly: { label: "Aéroport Orly", address: "Aéroport d'Orly, Orly", coords: [2.3790,48.7262] },
    },
    gare: {
        gare_de_lyon: { label: "Gare de Lyon", address: "Gare de Lyon, Paris", coords: [2.3730,48.8443] },
        gare_du_nord: { label: "Gare du Nord", address: "Gare du Nord, Paris", coords: [2.3553,48.8809] },
        gare_montparnasse: { label: "Gare Montparnasse", address: "Gare Montparnasse, Paris, France", coords: [2.3200, 48.8409] },
        gare_saint_lazare: { label: "Gare Saint-Lazare", address: "Gare Saint-Lazare, Paris, France", coords: [2.3253, 48.8773] },
        gare_de_bercy: { label: "Gare de Bercy", address: "Gare de Bercy, Paris, France", coords: [2.3828, 48.8393] },
        gare_austerlitz: { label: "Gare d'Austerlitz", address: "Gare d'Austerlitz, Paris, France", coords: [2.3663, 48.8426] },
        gare_de_l_est: { label: "Gare de l'Est", address: "Gare de l'Est, Paris, France", coords: [2.3590, 48.8769] },
        gare_de_chatelet_les_halles: { label: "Gare de Châtelet Les Halles", address: "Gare de Châtelet Les Halles, Paris, France", coords: [2.3470, 48.8620] },
    },
    loisir: {
        disney: { label: "Disneyland Paris", address: "Disneyland Paris, Chessy", coords: [2.7836,48.8676] },
        asterix: { label: "Parc Astérix", address: "Parc Astérix, Plailly", coords: [2.5712,49.1343] },
        versailles: { label: "Château de Versailles", address: "Place d'Armes, 78000 Versailles, France", coords: [2.1204, 48.8049] },
        jardins_du_luxembourg: { label: "Jardins du Luxembourg", address: "Jardin du Luxembourg, Paris, France", coords: [2.3372, 48.8462] },
        bois_de_boulogne: { label: "Bois de Boulogne", address: "Bois de Boulogne, Paris, France", coords: [2.2530, 48.8630] },
        parc_des_expositions: { label: "Parc des Expositions de Villepinte", address: "Parc des Expositions, Villepinte, France", coords: [2.52074, 48.97111] },
        louvre: { label: "Musée du Louvre", address: "Musée du Louvre, Paris, France", coords: [2.3375, 48.8609] },
        notre_dame: { label: "Cathédrale Notre-Dame de Paris", address: "Cathédrale Notre-Dame, Paris, France", coords: [2.3497, 48.8532] },
        orsay: { label: "Musée d’Orsay", address: "Musée d’Orsay, Paris, France", coords: [2.3265, 48.8603] },
        arc_triomphe: { label: "Arc de Triomphe", address: "Arc de Triomphe, Paris, France", coords: [2.2949, 48.8740] },
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
    let initialMiseDisDuration = null;

    // Initialisation véhicules
    const carSelect = document.getElementById("id_car_type");
    const vehiculeIdInput = document.getElementById("vehicule_id");
    const vehiculeLabelInput = document.getElementById("vehicule_label");

    // Initialise les data-* sur les options
    [...carSelect.options].forEach(opt => {
        if (!opt.value) return;
        const data = VEHICULE_DATA[opt.value];
        if (!data) return; // sécurité si l'option n'a pas de data
        opt.dataset.id = data.id;
        opt.dataset.label = opt.textContent;
        opt.dataset.priceKm = data.price_distance;
        opt.dataset.priceHour = data.price_hour;
        opt.dataset.seats = data.max_seats;
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
    setupAutocomplete("id_address_start", "suggestions_start", "start");
    setupAutocomplete("id_address_end", "suggestions_end", "end");

    function setupAutocomplete(inputId, suggestionsId, type){
        const input = document.getElementById(inputId);
        const box = document.getElementById(suggestionsId);

        input.addEventListener("input", async ()=>{
            if(input.value.length < 3){
                box.style.display = "none";
                return;
            }

            const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(input.value)}.json?autocomplete=true&limit=5&language=fr&country=fr&access_token=${mapboxgl.accessToken}`;
            const res = await fetch(url);
            const data = await res.json();
            if(!data.features) return;

            box.innerHTML = "";
            box.style.display = "block";

            data.features.forEach(f=>{
                const div = document.createElement("div");
                div.textContent = f.place_name;
                div.onclick = () => {
                    input.value = f.place_name;
                    box.style.display = "none";

                    if(type === "start") startCoords = f.geometry.coordinates;
                    else endCoords = f.geometry.coordinates;

                    refreshMarkers();

                    if (!isMiseDis && type === "end") setTripType("simple");

                    if (!isMiseDis) {
                        drawRoute();
                    } else {
                        updatePrice();
                    }
                };
                box.appendChild(div);
            });
        });

        // Fermeture de la div quand on clique à l'extérieur
        document.addEventListener("click", (event)=>{
            if (!box.contains(event.target) && event.target !== input) {
                box.style.display = "none";
            }
        });

        // Empêche le clic à l'intérieur de fermer immédiatement
        box.addEventListener("click", (event)=>{
            event.stopPropagation();
        });
    }


    /* ================= POI SELECT ================= */
    function setupPoi(selectId, type) {
        const select = document.getElementById(selectId);
        const cat = select.dataset.category;

        select.addEventListener("change", () => {
            resetOtherPoiSelects(type, cat);
            const poi = POIS[cat][select.value];
            if (!poi) return;

            const addressInput = document.getElementById(`id_address_${type}`);
            const durationInput = document.getElementById("duration");
            const distanceInput = document.getElementById("distance");

            /* ================= MISE À DISPOSITION ================= */
            if (cat === "mise_dis") {
                isMiseDis = true;
                setTripType("hourly");

                startCoords = startCoords || null;
                endCoords = null;

                if (!addressInput.value) addressInput.value = poi.value;

                // durée selon le choix
                initialMiseDisDuration = poi.value * 60;
                durationInput.value = initialMiseDisDuration;
                distanceInput.value = 0;

                // effacer la route classique sur la carte
                if (map.getSource("route")) {
                    map.getSource("route").setData({
                        type: "FeatureCollection",
                        features: []
                    });
                }

                refreshMarkers();
                updatePrice(); // prix mis à jour selon la durée
                return;
            }

            /* ================= POI CLASSIQUE ================= */
            // ⚠️ SI on définit une adresse d'arrivée → on quitte la mise à disposition
            if (type === "end") {
                exitMiseDisMode();
                setTripType("simple");
            }

            if (type === "start") {
                startCoords = poi.coords;
            } else {
                endCoords = poi.coords;
            }

            addressInput.value = poi.address;
            currentDistanceKm = 0;
            distanceInput.value = 0;

            drawRoute();
            refreshMarkers();
        });
    }
    ["id_address_start", "id_address_end"].forEach(id=>{
        const el = document.getElementById(id);
        if(el){
            el.addEventListener("input", () => {
                if (isMiseDis) {
                    // En mode mise à disposition, juste recalculer le prix
                    updatePrice();
                    return;
                }
                // Trajet classique
                setTripType("simple");
                drawRoute();
            });
            el.addEventListener("change", () => {
                if (isMiseDis) {
                    updatePrice();
                    return;
                }
                setTripType("simple");
                drawRoute();
            });
        }
    });

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

    function exitMiseDisMode() {
        if (!isMiseDis) return;
        isMiseDis = false;
        initialMiseDisDuration = null;
        document.getElementById("duration").value = 0;
        document.getElementById("distance").value = 0;
        currentDistanceKm = 0;
        setTripType("simple");
    }

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

    function resetOtherPoiSelects(prefix, currentCategory) {
        ["aeroport", "gare", "loisir", "mise_dis"].forEach(cat => {
            if (cat === currentCategory) return;

            const select = document.getElementById(`${prefix}_${cat}`);
            if (select) {
                select.selectedIndex = 0; // reset visuel
            }
        });
    }

    function setTripType(value) {
        const tripInput = document.getElementById("trip_type");
        const tripIdInput = document.getElementById("trip_type_id");
        const tripLabelInput = document.getElementById("trip_type_label");
        if (!tripInput || !tripIdInput || !tripLabelInput) return;
        tripInput.value = value;
        tripIdInput.value = TRIP_DATA[value]?.id || "";
        tripLabelInput.value = window.TRIP_LABELS[value] || "";
    }
    document.getElementById("id_address_start").addEventListener("input", () => {
        if (isMiseDis) {
            updatePrice();
            return;
        }
        setTripType("simple");
        drawRoute();
    });

    document.getElementById("id_address_end").addEventListener("input", () => {
        exitMiseDisMode();
        setTripType("simple");
        drawRoute();
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
        const info = document.getElementById("route-info");

        info.dataset.visible = info.innerHTML.trim() !== "";
    }

    document.getElementById("id_date_start").addEventListener("change", () => {
        if (isMiseDis) return;
        drawRoute();
    });

    document.getElementById("id_time_start").addEventListener("change", () => {
        if (isMiseDis) return;
        drawRoute();
    });

    function canShowRouteInfo() {
        const carValue = carSelect.value;

        if (isMiseDis) {
            return carValue !== "";
        }
        // Pour un trajet classique
        const startFilled = document.getElementById("id_address_start").value.trim() !== "" ||
                            document.getElementById("start_gare").value !== "" ||
                            document.getElementById("start_loisir").value !== "" ||
                            document.getElementById("start_aeroport").value !== "";

        const endFilled = document.getElementById("id_address_end").value.trim() !== "" ||
                          document.getElementById("end_gare").value !== "" ||
                          document.getElementById("end_loisir").value !== "" ||
                          document.getElementById("end_aeroport").value !== "";

        return startFilled && endFilled && carValue !== "";
    }

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
        console.log("=== updatePrice called ===");
        console.log("isMiseDis:", isMiseDis);
        console.log("initialMiseDisDuration:", initialMiseDisDuration);
        console.log("startCoords:", startCoords);
        console.log("endCoords:", endCoords);
        console.log("duration input:", document.getElementById("duration").value);

        const opt = carSelect.selectedOptions[0];
        if(!opt) return;

        if (!isMiseDis && (!startCoords || !endCoords || currentDistanceKm <= 0)) {
            return;
        }
        vehiculeIdInput.value = opt.dataset.id;
        vehiculeLabelInput.value = opt.dataset.label;

        let price = 0;

        if (isMiseDis) {
            const durationMinutes = initialMiseDisDuration || 60;
            const hours = durationMinutes / 60;
            price = hours * parseFloat(opt.dataset.priceHour || 0);

            document.getElementById("route-info").innerHTML =
                `Mise à disposition à : ${price.toFixed(2)} €`;
            document.getElementById("route-info").dataset.visible = "true";
            document.getElementById("price").value = price.toFixed(2);

            // Sortir immédiatement pour ne jamais toucher au trajet classique
            return;
        }

        // TRAJET CLASSIQUE
        const duration = parseInt(document.getElementById("duration").value || 0);
        price = currentDistanceKm * parseFloat(opt.dataset.priceKm || 0);

        if (canShowRouteInfo()) {
            document.getElementById("route-info").innerHTML =
                `${window.TRANSLATIONS.duration_calcul} : ${formatMinutes(duration)} — ${window.TRANSLATIONS.price_calcul} : ${price.toFixed(2)} €`;
            document.getElementById("route-info").dataset.visible = "true";
        } else {
            document.getElementById("route-info").innerHTML = "";
            document.getElementById("route-info").dataset.visible = "false";
        }

        document.getElementById("price").value = price.toFixed(2);
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
