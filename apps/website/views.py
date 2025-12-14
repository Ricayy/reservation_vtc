from datetime import datetime

from dateutil import parser
from django.shortcuts import render
from django.views.generic import CreateView

from apps.reservations.models import Reservation, VehiculeType
from apps.website.forms import ReservationForm
from apps.website.models import FormField
from config import settings


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservations/reservation_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mapbox_token"] = settings.MAPBOX_API_KEY
        vehicules = VehiculeType.objects.all()
        context["vehicule_types"] = vehicules
        context["vehicule_prices"] = {str(v.id): float(v.vehicule_price_distance or 0) for v in vehicules}
        context["vehicule_seats"] = {str(v.id): v.vehicule_max_seats or 0 for v in vehicules}

        return context


def recap_reservation(request):
    vehicules = VehiculeType.objects.all()

    if request.method == "POST":
        form = ReservationForm(request.POST, vehicules=vehicules)
        if not form.is_valid():
            return render(request, "reservations/reservation_form.html", {
                "form": form,
                "mapbox_token": settings.MAPBOX_API_KEY,
                "vehicule_prices": {str(v.id): v.vehicule_price_distance for v in vehicules},
                "vehicule_seats": {str(v.id): v.vehicule_max_seats for v in vehicules},
            })

        data = form.cleaned_data

        new_reservation = {
            FormField.address_start: data[FormField.address_start],
            FormField.address_end: data[FormField.address_end],
            FormField.nb_passengers: data[FormField.nb_passengers],
            FormField.nb_luggages: data[FormField.nb_luggages],
            FormField.note: data[FormField.note],
            FormField.price: data[FormField.price],
            FormField.duration: data[FormField.duration],
            FormField.distance: data[FormField.distance],
            FormField.car_type: [],
            FormField.email: data[FormField.email],
            FormField.last_name: data[FormField.last_name],
            FormField.first_name: data[FormField.first_name],
            FormField.phone: data[FormField.phone],
        }
        new_reservation[FormField.car_type].append(data[FormField.car_type].id)
        new_reservation[FormField.car_type].append(data[FormField.car_type].vehicule_type_name)

        datetime_start = datetime.combine(data[FormField.date_start], data[FormField.time_start])
        new_reservation[FormField.datetime_start] = datetime_start.strftime("%Y-%m-%d %H:%M")

        return render(request, "reservations/recap.html", {
            "reservation": new_reservation,
        })

    # GET
    form = ReservationForm(vehicules=vehicules)
    return render(request, "reservations/reservation.html", {
        "form": form,
        "vehicules": vehicules,
        "vehicule_prices": {str(v.id): v.vehicule_price_distance or 0 for v in vehicules},
        "vehicule_seats": {str(v.id): v.vehicule_max_seats or 0 for v in vehicules},
    })