from dataclasses import dataclass


@dataclass
class FormField:
    """
    Dataclass contenant les noms des champs du formulaire de réservation
    """

    address_start = "address_start"
    address_end = "address_end"
    datetime_start = "datetime_start"
    date_start = "date_start"
    time_start = "time_start"
    nb_passengers = "nb_passengers"
    nb_luggages = "nb_luggages"
    email = "email"
    first_name = "first_name"
    last_name = "last_name"
    phone = "phone"
    note = "note"
    distance = "distance"
    duration = "duration"
    price = "price"
    car_type = "car_type"
    trip_type = "trip_type"

    vehicule_id = "vehicule_id"
    vehicule_label = "vehicule_label"
    trip_type_id = "trip_type_id"
    trip_type_label = "trip_type_label"
