from django.shortcuts import render
from django.views.generic import CreateView

from apps.reservations.models import Reservation
from config import settings

def main(request):
    context = {
        "mapbox_token": settings.MAPBOX_API_KEY,
    }
    return render(request, 'form.html', context=context)


class ReservationCreateView(CreateView):
    model = Reservation
    fields = ("address_start",
              "address_end",
              "date_start",
              "time_start",
              "car_type",
              "nb_passengers",
              "nb_luggages",
              "trip_type",
              "last_name",
              "first_name",
              "phone",
              "email",
              "note",)