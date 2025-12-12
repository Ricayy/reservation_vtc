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



@dataclass
class OdooReservationModel:
    """
    Dataclass contenant les noms des champs du modèle Reservation
    """
    name = "x_name"
    address_start = "x_studio_address_start"
    address_end = "x_studio_address_end"
    datetime_start = "x_studio_datetime_start"
    nb_passengers = "x_studio_nb_passengers"
    nb_luggages = "x_studio_nb_luggages"
    note = "x_studio_note"

    distance = "x_studio_distance"
    duration = "x_studio_duration"
    price = "x_studio_price"

    email = "x_studio_email"
    car_type = "x_studio_car_type"
    trip_type = "x_studio_trip_type"

@dataclass
class OdooContactModel:
    """
    Dataclass contenant les noms des champs du modèle Contact
    """
    email = "x_name"
    first_name = "x_studio_first_name"
    last_name = "x_studio_last_name"
    phone = "x_studio_phone"

@dataclass
class OdooVehiculeModel:
    """
    Dataclass contenant les noms des champs du modèle Vehicule
    """
    name = "x_name"
