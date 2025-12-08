from datetime import datetime

from django.shortcuts import render
from dateutil import parser
import pytz

from apps.core.models import OdooReservationModel
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
            OdooReservationModel().name: "reservation" + datetime.strftime(datetime.today(), "%d/%m/%Y %H:%M:%S"),
            OdooReservationModel().address_start: request.POST.get("address_start"),
            OdooReservationModel().address_end: request.POST.get("address_end"),
            OdooReservationModel().datetime_start: datetime_start,
            OdooReservationModel().nb_passengers: request.POST.get("nb_passengers"),
            OdooReservationModel().nb_luggages: request.POST.get("nb_luggages"),
            # OdooReservationModel().last_name: request.POST.get("last_name"),
            # OdooReservationModel().first_name: request.POST.get("first_name"),
            # OdooReservationModel().phone: request.POST.get("phone"),
            # OdooReservationModel().email: request.POST.get("email"),
            OdooReservationModel().note: request.POST.get("note"),
            OdooReservationModel().price: request.POST.get("price"),
            OdooReservationModel().duration: request.POST.get("duration"),
            OdooReservationModel().distance: request.POST.get("distance"),
            # OdooReservationModel().car_type: request.POST.get("car_type"),
            # OdooReservationModel().trip_type: request.POST.get("trip_type"),
        }

        result = OdooClient().create_reservation(new_reservation)
        print(result)
        return render(request, "validation.html", {"reservation": new_reservation})
    return render(request, "error.html")

def cancel_reservation(request):
    pass