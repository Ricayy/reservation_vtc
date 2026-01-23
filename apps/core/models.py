from dataclasses import dataclass

@dataclass
class OdooReservationModel:
    """
    Dataclass contenant les noms des champs du modèle Reservation
    """
    id= "id"
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
    id = "id"
    email = "x_name"
    first_name = "x_studio_first_name"
    last_name = "x_studio_last_name"
    phone = "x_studio_phone"
    reservation_id = "x_studio_reservation"

@dataclass
class OdooVehiculeModel:
    """
    Dataclass contenant les noms des champs du modèle Vehicule
    """
    id = "id"
    name = "x_name"

@dataclass
class OdooReservationStateModel:
    """
    Dataclass contenant les noms des champs du modèle Etat reservation
    """
    id = "id"
    name = "x_name"
