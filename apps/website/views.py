from datetime import datetime

from dateutil import parser
from django.shortcuts import render
from django.views.generic import CreateView

from apps.core.models import OdooReservationModel, OdooContactModel, OdooVehiculeModel, FormField
from apps.reservations.models import Reservation, VehiculeType
from apps.reservations.views import LOCAL_TZ
from apps.website.form import ReservationForm
from config import settings


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    # fields = ("address_start",
    #           "address_end",
    #           "date_start",
    #           "time_start",
    #           "car_type",
    #           "nb_passengers",
    #           "nb_luggages",
    #           "trip_type",
    #           "last_name",
    #           "first_name",
    #           "phone",
    #           "email",
    #           "note",)
    template_name = "reservations/reservation_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mapbox_token"] = settings.MAPBOX_API_KEY
        context["vehicule_types"] = VehiculeType.objects.all()
        return context


def confirm_reservation(request):
    if request.method == "POST":
        combined_str = f"{str(request.POST.get(FormField.date_start))} {request.POST.get(FormField.time_start)}"
        datetime_start = parser.parse(combined_str)
        datetime_start = LOCAL_TZ.localize(datetime_start)
        reservation_data = {
            FormField.address_start: request.POST.get(FormField.address_start),
            FormField.address_end: request.POST.get(FormField.address_end),
            FormField.datetime_start: datetime_start,
            FormField.nb_passengers: request.POST.get(FormField.nb_passengers),
            FormField.nb_luggages: request.POST.get(FormField.nb_luggages),
            FormField.email: request.POST.get(FormField.email),
            FormField.last_name: request.POST.get(FormField.last_name),
            FormField.first_name: request.POST.get(FormField.first_name),
            FormField.phone: request.POST.get(FormField.phone),
            FormField.note: request.POST.get(FormField.note),
            FormField.price: request.POST.get(FormField.price),
            FormField.duration: request.POST.get(FormField.duration),
            FormField.distance: request.POST.get(FormField.distance),
            FormField.car_type: int(request.POST.get(FormField.car_type)),
            FormField.trip_type: int(request.POST.get("trip_type")),
        }
        return render(request, "reservations/confirmation.html", context={"reservation": reservation_data})
    return render(request, "website/error.html")