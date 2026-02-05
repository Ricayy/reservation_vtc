import ast
import io
from datetime import datetime

from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from apps.core.models import OdooReservationModel, OdooContactModel
from apps.core.odoo_client import (
    get_user_by_email,
    create_user,
    create_res,
    get_res_by_id,
    get_user_by_id,
)
from apps.website.models import FormField

from django.http import HttpResponse


def preview_order_pdf(request, id_res):
    """
    Aperçu du PDF de la réservation dans le navigateur.
    """
    try:
        pdf_file = build_order_pdf(id_res)
    except Exception as e:
        return HttpResponse(f"Erreur génération PDF : {e}")

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="order_{id_res}.pdf"'
    return response


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
        "L'équipe VTC",
    ]

    return "\n".join(base)


def build_order_pdf(id_res):
    # Récupération donnée réservation
    res_data = get_res_by_id(id_res)[0]
    user_data = get_user_by_id(res_data[OdooReservationModel.email][0])[0]
    # Normalisation des données pour l'affichage
    res_data[OdooReservationModel.email] = user_data
    res_data[OdooReservationModel.car_type] = res_data[OdooReservationModel.car_type][1]
    res_data[OdooReservationModel.trip_type] = res_data[OdooReservationModel.trip_type][
        1
    ]
    res_data[OdooReservationModel.datetime_start] = datetime.strptime(
        res_data[OdooReservationModel.datetime_start], "%Y-%m-%d %H:%M:%S"
    )
    res_data[OdooReservationModel.datetime_start] = res_data[
        OdooReservationModel.datetime_start
    ].strftime("%d/%m/%Y - %H:%M")

    # Rendu HTML
    html_string = render_to_string("reservations/order.html", {"res_data": res_data})

    # Génération PDF en mémoire
    pdf_file = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html_string), dest=pdf_file)

    if pisa_status.err:
        raise Exception("Erreur lors de la génération du PDF")

    pdf_file.seek(0)
    return pdf_file.read()


def gen_mail_and_order_pdf(new_reservation, email_user, id_trip_type, id_res):
    message = build_email_message(new_reservation, id_trip_type)
    pdf_file = build_order_pdf(id_res)
    mail = EmailMessage(
        subject="Confirmation de votre reservation VTC",
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email_user],
    )
    mail.attach(f"order_{id_res}.pdf", pdf_file, "application/pdf")
    mail.send()


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
        datetime_start = datetime.strptime(
            data[FormField.datetime_start], "%d/%m/%Y - %H:%M"
        )
        new_reservation = {
            OdooReservationModel.name: "Reservation "
            + datetime.strftime(datetime.today(), "%d/%m/%Y %H:%M"),
            OdooReservationModel.address_start: data[FormField.address_start],
            OdooReservationModel.address_end: data[FormField.address_end],
            OdooReservationModel.nb_passengers: data[FormField.nb_passengers],
            OdooReservationModel.nb_luggages: data[FormField.nb_luggages],
            OdooReservationModel.note: data[FormField.note],
            OdooReservationModel.price: data[FormField.price],
            OdooReservationModel.duration: data[FormField.duration],
            OdooReservationModel.distance: data[FormField.distance],
            OdooReservationModel.car_type: id_car_type,
            OdooReservationModel.datetime_start: datetime_start.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
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
        response = create_res(new_reservation)
        if response["result"]:
            gen_mail_and_order_pdf(
                new_reservation,
                user_data[OdooContactModel.email],
                id_trip_type,
                response["result"],
            )

            reservation = {
                "id": response["result"],
                FormField.address_start: new_reservation[
                    OdooReservationModel.address_start
                ],
                FormField.address_end: new_reservation[
                    OdooReservationModel.address_end
                ],
                FormField.trip_type: new_reservation[OdooReservationModel.trip_type],
                FormField.duration: int(new_reservation[OdooReservationModel.duration]),
                FormField.datetime_start: data[FormField.datetime_start],
            }
            return render(
                request, "reservations/validation.html", {"reservation": reservation}
            )
        else:
            error = response["error"]
    else:
        error = "Requête impossible"
    return render(request, "error.html", context=error)
