import ast
from datetime import datetime
from django.shortcuts import render
from dateutil import parser
from apps.core.models import OdooReservationModel, OdooContactModel
from apps.core.odoo_client import get_user_by_email, create_user, create_res
from apps.website.models import FormField


def validation_reservation(request):
    """
    Fonction de mise en forme des données de réservation avant la publication sur Odoo

    :param request:
    :return:
    """

    # POST
    if request.method == "POST":
        data = request.POST.dict()
        # String to list
        id_car_type = ast.literal_eval(data[FormField.car_type])[0]
        id_trip_type = ast.literal_eval(data[FormField.trip_type])[0]
        datetime_start = datetime.strptime(data[FormField.datetime_start], "%d/%m/%Y - %H:%M")
        new_reservation = {
            OdooReservationModel.name: "Reservation " + datetime.strftime(datetime.today(), "%d/%m/%Y %H:%M"),
            OdooReservationModel.address_start: data[FormField.address_start],
            OdooReservationModel.address_end: data[FormField.address_end],
            OdooReservationModel.nb_passengers: data[FormField.nb_passengers],
            OdooReservationModel.nb_luggages: data[FormField.nb_luggages],
            OdooReservationModel.note: data[FormField.note],
            OdooReservationModel.price: data[FormField.price],
            OdooReservationModel.duration: data[FormField.duration],
            OdooReservationModel.distance: data[FormField.distance],
            OdooReservationModel.car_type: id_car_type,
            OdooReservationModel.datetime_start: datetime_start.strftime("%Y-%m-%d %H:%M:%S"),
            OdooReservationModel.trip_type: id_trip_type,
        }

        id_odoo = get_user_by_email(data[FormField.email])
        user_data = {
            OdooContactModel.email: data[FormField.email],
            OdooContactModel.last_name: data[FormField.last_name],
            OdooContactModel.first_name: data[FormField.first_name],
            OdooContactModel.phone: data[FormField.phone],
        }
        if id_odoo:
            id_user = id_odoo[0]["id"]
        else:
            id_odoo = create_user(user_data)
            id_user = id_odoo["result"]
        new_reservation[OdooReservationModel.email] = id_user
        print(new_reservation)
        response = create_res(new_reservation)
        print(response)
        if response["result"]:
            reservation = {
                FormField.address_start: data[FormField.address_start],
                FormField.address_end: data[FormField.address_end],
                FormField.datetime_start: new_reservation[OdooReservationModel.datetime_start]
            }
            return render(request, "reservations/validation.html", {"reservation": reservation})
        else:
            error = response["error"]
    else :
        error = "Requête impossible"
    return render(request, "error.html", context=error)
