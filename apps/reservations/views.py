from datetime import datetime

from django.shortcuts import render
from ..core.odoo_client import OdooClient


def reservation(request):
    if request.method == "POST":
        d = datetime.strptime(request.POST.get("date_start"), "%Y-%m-%d").date()
        t = datetime.strptime(request.POST.get("time_start"), "%H:%M").time()
        datetime_start = datetime.combine(d, t)

        reservation_data = {
            "x_studio_address_start": request.POST.get("address_start"),
            "x_studio_address_end": request.POST.get("address_end"),
            "x_studio_datetime_start": datetime_start,
            # "x_studio_car_type": request.POST.get("car_type"),
            "x_studio_nb_passengers": request.POST.get("nb_passengers"),
            "x_studio_nb_luggages": request.POST.get("nb_luggages"),
            # "trip_type": request.POST.get("trip_type"),
            "x_studio_last_name": request.POST.get("last_name"),
            "x_studio_first_name": request.POST.get("first_name"),
            "x_studio_phone": request.POST.get("phone"),
            "x_studio_email": request.POST.get("email"),
            "x_studio_note": request.POST.get("note"),
            "x_studio_price": 30.00,
            "x_studio_duration": 30,
            "x_studio_distance": 15.2,
        }
        result = OdooClient().create_reservation(reservation_data)
        print(result)

        return render(request, "confirmation.html", {"reservation": reservation_data})
    return render(request, "error.html")
