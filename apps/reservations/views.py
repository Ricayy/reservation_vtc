from datetime import datetime

from django.shortcuts import render
from dateutil import parser
import pytz
from apps.core.odoo_client import OdooClient
LOCAL_TZ = pytz.timezone("Europe/Paris")

def reservation(request):
    if request.method == "POST":


        reservation_data = {
            "address_start": request.POST.get("address_start"),
            "address_end": request.POST.get("address_end"),
            # "car_type": request.POST.get("car_type"),
            "nb_passengers": request.POST.get("nb_passengers"),
            "nb_luggages": request.POST.get("nb_luggages"),
            # "trip_type": request.POST.get("trip_type"),
            "last_name": request.POST.get("last_name"),
            "first_name": request.POST.get("first_name"),
            "phone": request.POST.get("phone"),
            "email": request.POST.get("email"),
            "note": request.POST.get("note"),
            "price": 30.00,
            "duration": 30,
            "distance": 15.2,
        }

        combined_str = f"{str(request.POST.get("date_start"))} {request.POST.get("time_start")}"
        datetime_start = parser.parse(combined_str)
        datetime_start = LOCAL_TZ.localize(datetime_start)
        reservation_data.update({"datetime_start": datetime_start})

        """
        Relation modèles Vehicule
        Relation modèles Trajet
        Relation modèles Contact ?
        Calcul distance, duration pour trouver price
        """

        return render(request, "confirmation.html", {"reservation": reservation_data})
    return render(request, "form.html")


def validation(request):
    if request.method == "POST":
        datetime_start = parser.parse(request.POST.get("datetime_start"))
        new_reservation = {
            "x_studio_address_start": request.POST.get("address_start"),
            "x_studio_address_end": request.POST.get("address_end"),
            "x_studio_datetime_start": datetime_start,
            "x_studio_nb_passengers": request.POST.get("nb_passengers"),
            "x_studio_nb_luggages": request.POST.get("nb_luggages"),
            "x_studio_last_name": request.POST.get("last_name"),
            "x_studio_first_name": request.POST.get("first_name"),
            "x_studio_phone": request.POST.get("phone"),
            "x_studio_email": request.POST.get("email"),
            "x_studio_note": request.POST.get("note"),
            "x_studio_price": request.POST.get("price"),
            "x_studio_duration": request.POST.get("duration"),
            "x_studio_distance": request.POST.get("distance"),
            # "x_studio_car_type": request.POST.get("car_type"),
            # "x_studio_trip_type": request.POST.get("trip_type"),
        }

        result = OdooClient().create_reservation(new_reservation)
        print(result)
        return render(request, "validation.html", {"reservation": new_reservation})
    return render(request, "error.html")

def cancel_reservation(request):
    pass