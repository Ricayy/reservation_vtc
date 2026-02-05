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
    # Gestion context pour requête
    form = ReservationForm(request.POST)
    context = reservation_common_context()
    context["form"] = form
    print("request.POST.dict()")
    print(request.POST.dict())
    # POST
    if request.method == "POST":
        if not form.is_valid():
            return render(request, "reservations/reservation_form.html", context)

        # data = form.cleaned_data
        data = request.POST.dict()
        # print(data)
        new_reservation = {
            FormField.address_start: data[FormField.address_start],
            FormField.address_end: data[FormField.address_end],
            FormField.nb_passengers: data[FormField.nb_passengers],
            FormField.nb_luggages: data[FormField.nb_luggages],
            FormField.note: data[FormField.note],
            FormField.price: data[FormField.price],
            FormField.duration: data[FormField.duration],
            FormField.distance: data[FormField.distance],
            FormField.email: data[FormField.email],
            FormField.last_name: data[FormField.last_name],
            FormField.first_name: data[FormField.first_name],
            FormField.phone: data[FormField.phone],
            FormField.car_type: [],
            FormField.trip_type: [],
        }

        # Véhicule
        new_reservation[FormField.car_type].append(data[FormField.vehicule_id])
        new_reservation[FormField.car_type].append(data[FormField.vehicule_label])

        # Type de trajet
        new_reservation[FormField.trip_type].append(data[FormField.trip_type_id])
        new_reservation[FormField.trip_type].append(data[FormField.trip_type_label])

        # Date et heure
        date_obj = datetime.strptime(data[FormField.date_start], "%Y-%m-%d").date()
        time_obj = datetime.strptime(data[FormField.time_start], "%H:%M").time()
        datetime_start = datetime.combine(date_obj, time_obj)
        new_reservation[FormField.datetime_start] = datetime_start.strftime("%d/%m/%Y - %H:%M")

        for key in new_reservation.keys():
            if new_reservation[key] is None:
                new_reservation[key] = ""

        return render(request, "reservations/recap.html", {"reservation": new_reservation})

    # GET
    return render(request, "reservations/reservation_form.html", context)

