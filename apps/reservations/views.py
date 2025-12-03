from django.shortcuts import render

from .models import Reservation


def reservation(request):
    if request.method == "POST":
        reservation = Reservation.objects.create(
            address_start = request.POST.get("address_start"),
            address_stop = request.POST.get("address_stop"),
            date_start = request.POST.get("date_start"),
            time_start = request.POST.get("time_start"),
            car_type = request.POST.get("car_type"),
            nb_passengers = request.POST.get("nb_passengers"),
            nb_luggages = request.POST.get("nb_luggages"),
            trip_type = request.POST.get("trip_type"),
            last_name = request.POST.get("last_name"),
            first_name = request.POST.get("first_name"),
            phone = request.POST.get("phone"),
            email = request.POST.get("email"),
            note = request.POST.get("note"),
            price = request.POST.get("price"),
            duration = request.POST.get("duration"),
            distance = request.POST.get("distance"),
            date_reservation = request.POST.get("date_reservation"),
        )

        return render(request, "confirmation.html", {
            "reservation": reservation,
        })
    # return render(request, "error.html")
