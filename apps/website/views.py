import json
from datetime import datetime

from django.shortcuts import render
from django.views.generic import CreateView

from apps.reservations.models import Reservation
from apps.website.context import reservation_common_context
from apps.website.forms import ReservationForm
from apps.website.models import FormField


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservations/reservation_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(reservation_common_context())
        return context


def recap_reservation(request):
    form = ReservationForm(request.POST)
    context = reservation_common_context()
    context["form"] = form

    if request.method == "POST":
        if not form.is_valid():
            return render(request, "reservations/reservation_form.html", context)

        data = request.POST.dict()
        print("data")
        print(data)

        # ── Adresses (terminal optionnel) ──────────────────────────────
        address_start = data[FormField.address_start]
        if data.get(FormField.terminal_start, ""):
            address_start += ", " + data[FormField.terminal_start]

        address_end = data.get(FormField.address_end, "")
        if data.get(FormField.terminal_end, ""):
            address_end += ", " + data[FormField.terminal_end]

        # ── Type de trajet ─────────────────────────────────────────────
        trip_type = data[FormField.trip_type]  # "simple" ou "hourly"
        vehicle_type = data[FormField.car_type]  # "car" ou "van"
        is_hourly = trip_type == "hourly"

        # ── Distance : vide ou absent pour une mise à disposition ──────
        raw_distance = data.get(FormField.distance, "").strip()
        distance_km = float(raw_distance) if raw_distance else 0.0

        # ── Durée : minutes sélectionnées dans le select mise à dispo ──
        # Le champ caché #duration est rempli par reservation.js dans les
        # deux cas (trajet classique = durée Mapbox, hourly = durée choisie).
        raw_duration = data.get(FormField.duration, "").strip()
        duration_min = int(raw_duration) if raw_duration else 0

        # ── Coordonnées (peuvent être null côté JS pour mise à dispo) ──
        start_coords = json.loads(data.get("start_coords", "null"))
        end_coords = json.loads(data.get("end_coords", "null"))

        # ── Validation métier supplémentaire ───────────────────────────
        if not is_hourly and distance_km <= 0:
            context["error"] = (
                "Impossible de calculer l'itinéraire. "
                "Vérifiez les adresses de départ et d'arrivée."
            )
            return render(request, "reservations/reservation_form.html", context)

        if is_hourly and duration_min <= 0:
            context["error"] = "Veuillez sélectionner une durée de mise à disposition."
            return render(request, "reservations/reservation_form.html", context)

        # ── Calcul du prix vérifié côté serveur ────────────────────────
        verified_price = calculate_price(
            trip_type=trip_type,
            vehicle_type=vehicle_type,
            distance_km=distance_km,
            duration_minutes=duration_min,
            start_coords=start_coords,
            end_coords=end_coords,
            start_address=data[FormField.address_start],
            end_address=address_end,
        )

        # ── Construction du récapitulatif ──────────────────────────────
        new_reservation = {
            FormField.address_start: address_start,
            FormField.address_end: address_end,
            FormField.nb_passengers: int(data[FormField.nb_passengers]),
            FormField.nb_luggages: int(data[FormField.nb_luggages]),
            FormField.note: data.get(FormField.note, ""),
            FormField.price: verified_price,
            FormField.duration: duration_min,
            FormField.distance: distance_km,
            FormField.email: data[FormField.email],
            FormField.last_name: data[FormField.last_name],
            FormField.first_name: data[FormField.first_name],
            FormField.phone: data[FormField.phone],
            FormField.car_type: {},
            FormField.trip_type: {},
        }

        # Véhicule
        new_reservation[FormField.car_type][FormField.vehicule_id] = int(
            data[FormField.vehicule_id]
        )
        new_reservation[FormField.car_type][FormField.car_type] = data[
            FormField.car_type
        ]
        new_reservation[FormField.car_type][FormField.vehicule_label] = data[
            FormField.vehicule_label
        ]

        # Type de trajet
        new_reservation[FormField.trip_type][FormField.trip_type_id] = int(
            data[FormField.trip_type_id]
        )
        new_reservation[FormField.trip_type][FormField.trip_type] = data[
            FormField.trip_type
        ]
        new_reservation[FormField.trip_type][FormField.trip_type_label] = data[
            FormField.trip_type_label
        ]

        # Date et heure
        date_obj = datetime.strptime(data[FormField.date_start], "%Y-%m-%d").date()
        time_obj = datetime.strptime(data[FormField.time_start], "%H:%M").time()
        datetime_start = datetime.combine(date_obj, time_obj)
        new_reservation[FormField.datetime_start] = datetime_start.strftime(
            "%d/%m/%Y - %H:%M"
        )

        # Remplacer les None résiduels par ""
        for key in new_reservation:
            if new_reservation[key] is None:
                new_reservation[key] = ""

        return render(
            request, "reservations/recap.html", {"reservation": new_reservation}
        )

    # GET
    return render(request, "reservations/reservation_form.html", context)


# ══════════════════════════════════════════════════════════════════
# LOGIQUE DE PRIX
# ══════════════════════════════════════════════════════════════════

PARIS_KEYWORDS = ["Paris", "paris"]

COORDS_CDG = [2.5479, 49.0097]
COORDS_ORLY = [2.3790, 48.7262]
COORDS_DISNEY = [2.7836, 48.8676]

PARIS_BBOX = {"lat_min": 48.815, "lat_max": 48.905, "lng_min": 2.224, "lng_max": 2.470}

PRICE_KM = {
    "car": 1.80,
    "van": 2.50,
}
PRICE_HOUR = {
    "car": 45.0,
    "van": 60.0,
}
MINIMUMS = {
    "cdg_orly": {"car": 70, "van": 100},
    "paris_cdg": {"car": 50, "van": 80},
    "paris_orly": {"car": 40, "van": 70},
    "paris_disney": {"car": 70, "van": 100},
    "intra_paris": {"car": 30, "van": 50},
}


def coords_match(a, b):
    if not a or not b:
        return False
    return round(a[0], 4) == round(b[0], 4) and round(a[1], 4) == round(b[1], 4)


def is_paris(coords, address):
    if address and any(kw in address for kw in PARIS_KEYWORDS):
        return True
    if coords:
        lng, lat = coords[0], coords[1]
        b = PARIS_BBOX
        if b["lat_min"] <= lat <= b["lat_max"] and b["lng_min"] <= lng <= b["lng_max"]:
            return True
    return False


def get_minimum(start_coords, end_coords, start_address, end_address, vehicle_type):
    vtype = "van" if vehicle_type == "van" else "car"

    start_cdg = coords_match(start_coords, COORDS_CDG)
    end_cdg = coords_match(end_coords, COORDS_CDG)
    start_orly = coords_match(start_coords, COORDS_ORLY)
    end_orly = coords_match(end_coords, COORDS_ORLY)
    start_disney = coords_match(start_coords, COORDS_DISNEY)
    end_disney = coords_match(end_coords, COORDS_DISNEY)
    start_paris = is_paris(start_coords, start_address)
    end_paris = is_paris(end_coords, end_address)

    if (start_cdg and end_orly) or (start_orly and end_cdg):
        return MINIMUMS["cdg_orly"][vtype]
    if (start_paris and end_cdg) or (start_cdg and end_paris):
        return MINIMUMS["paris_cdg"][vtype]
    if (start_paris and end_orly) or (start_orly and end_paris):
        return MINIMUMS["paris_orly"][vtype]
    if (start_paris and end_disney) or (start_disney and end_paris):
        return MINIMUMS["paris_disney"][vtype]
    if start_paris and end_paris:
        return MINIMUMS["intra_paris"][vtype]

    return 0


def calculate_price(
    trip_type,
    vehicle_type,
    distance_km,
    duration_minutes,
    start_coords,
    end_coords,
    start_address,
    end_address,
):
    """
    Recalcule le prix côté serveur — source de vérité unique.

    trip_type        : "simple" | "hourly"
    vehicle_type     : "car"    | "van"
    distance_km      : float  (0.0 pour une mise à disposition)
    duration_minutes : int    (durée Mapbox ou durée choisie pour hourly)
    start_coords     : [lng, lat] | None
    end_coords       : [lng, lat] | None
    start_address    : str
    end_address      : str
    """
    vtype = "van" if vehicle_type == "van" else "car"

    # ── Mise à disposition : tarif horaire ────────────────────────────
    if trip_type == "hourly":
        hours = duration_minutes / 60
        return round(hours * PRICE_HOUR[vtype], 2)

    # ── Trajet classique : tarif kilométrique + minimums ─────────────
    price = distance_km * PRICE_KM[vtype]
    minimum = get_minimum(start_coords, end_coords, start_address, end_address, vtype)
    if minimum > 0 and price < minimum:
        price = minimum

    return round(price, 2)
