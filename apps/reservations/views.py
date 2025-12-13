from datetime import datetime
from django.shortcuts import render, redirect
from dateutil import parser
import pytz
from apps.core.models import OdooReservationModel, OdooContactModel
from apps.core.odoo_client import search_read_user_by_email, create_user, create_reservation
from apps.website.models import FormField

LOCAL_TZ = pytz.timezone("Europe/Paris")

def validation_reservation(request):
    """

    :param request:
    :return:
    """
    if request.method == "POST":
        new_reservation = {
            OdooReservationModel.name: "Reservation " + datetime.strftime(datetime.today(), "%d/%m/%Y %H:%M:%S"),
            OdooReservationModel.address_start: request.POST.get(FormField.address_start),
            OdooReservationModel.address_end: request.POST.get(FormField.address_end),
            OdooReservationModel.nb_passengers: request.POST.get(FormField.nb_passengers),
            OdooReservationModel.nb_luggages: request.POST.get(FormField.nb_luggages),
            OdooReservationModel.note: request.POST.get(FormField.note),
            OdooReservationModel.price: request.POST.get(FormField.price),
            OdooReservationModel.duration: request.POST.get(FormField.duration),
            OdooReservationModel.distance: request.POST.get(FormField.distance),
            OdooReservationModel.car_type: request.POST.get(FormField.car_type),
            # OdooReservationModel.trip_type: request.POST.get(FormField.trip_type),
        }

        datetime_start = parser.parse(request.POST.get(FormField.datetime_start))
        new_reservation[OdooReservationModel.datetime_start] = datetime_start.strftime("%Y-%m-%d %H:%M")

        id_odoo = search_read_user_by_email(request.POST.get(FormField.email))
        user_data = {
            OdooContactModel.email: request.POST.get(FormField.email),
            OdooContactModel.last_name: request.POST.get(FormField.last_name),
            OdooContactModel.first_name: request.POST.get(FormField.first_name),
            OdooContactModel.phone: request.POST.get(FormField.phone),
        }
        if id_odoo:
            id_user = id_odoo[0]["id"]
        else:
            id_odoo = create_user(user_data)
            id_user = id_odoo["result"]
        new_reservation[OdooReservationModel.email] = id_user

        response = create_reservation(new_reservation)
        if response["result"]:
            reservation = {
                FormField.address_start: request.POST.get(FormField.address_start),
                FormField.address_end: request.POST.get(FormField.address_end),
                FormField.datetime_start: new_reservation[OdooReservationModel.datetime_start]
            }
            return render(request, "reservations/validation.html", {"reservation": reservation})
        else:
            error = response["error"]
    else :
        error = "Requête impossible"
    return render(request, "error.html", context=error)
