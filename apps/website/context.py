from config import settings
from apps.reservations.models import VehiculeType, TripType, Reservation

def reservation_common_context():
    return {
        "VEHICULE_DATA": Reservation.VEHICULE_DATA,
        "TRIP_DATA": Reservation.TRIP_DATA,
        "mapbox_token": settings.MAPBOX_API_KEY,
        "vehicule_types": VehiculeType.choices,
        "vehicule_price_km": {
            key: data["price_distance"]
            for key, data in Reservation.VEHICULE_DATA.items()
        },
        "vehicule_price_hour": {
            key: data["price_hour"]
            for key, data in Reservation.VEHICULE_DATA.items()
        },
        "vehicule_seats": {
            key: data["max_seats"]
            for key, data in Reservation.VEHICULE_DATA.items()
        },
        "trip_type": TripType.choices,
    }
