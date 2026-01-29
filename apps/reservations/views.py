import ast
from datetime import datetime

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render

from apps.core.models import OdooReservationModel, OdooContactModel
from apps.core.odoo_client import get_user_by_email, create_user, create_res
from apps.website.models import FormField


def build_email_message(res_data, trip_type):
    address_start = res_data[OdooReservationModel.address_start]
    address_end = res_data[OdooReservationModel.address_end]
    distance = res_data[OdooReservationModel.distance]
    duration = int(res_data[OdooReservationModel.duration])
    price = res_data[OdooReservationModel.price]
    base = [
        "Bonjour,",
        "",
        "Nous vous confirmons la prise en compte de votre réservation VTC.",
        "",
        f"Départ : {address_start}",
    ]

    # Course simple
    if trip_type == 1:
        base += [
            f"Arrivée : {address_end}",
            f"Distance : {distance} km",
        ]

    # Mise à disposition
    elif trip_type == 2:
        if duration >= 60:
            duration = duration // 60
        base += [
            "Type de trajet : Mise à disposition",
            f"Durée réservée : {duration} heure(s)",
        ]

    base += [
        "",
        f"Prix estimé : {price} €",
        "",
        "Un chauffeur vous sera attribué prochainement.",
        "",
        "Cordialement,",
        "L'équipe VTC"
    ]

    return "\n".join(base)



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
        print()
        # response = create_res(new_reservation)
        # print(response)
        # print()
        response = {"result": 1}
        if response["result"]:
            message = build_email_message(new_reservation, id_trip_type)
            send_mail(
                subject="Confirmation de votre reservation VTC",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_data[OdooContactModel.email]],
                fail_silently=False,
            )

            reservation = {
                FormField.address_start: new_reservation[OdooReservationModel.address_start],
                FormField.address_end: new_reservation[OdooReservationModel.address_end],
                FormField.trip_type: new_reservation[OdooReservationModel.trip_type],
                FormField.duration: int(new_reservation[OdooReservationModel.duration]),
                FormField.datetime_start: data[FormField.datetime_start]
            }
            return render(request, "reservations/validation.html", {"reservation": reservation})
        else:
            error = response["error"]
    else :
        error = "Requête impossible"
    return render(request, "error.html", context=error)
