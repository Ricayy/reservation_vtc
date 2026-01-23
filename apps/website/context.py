from apps.reservations.models import VehiculeType, TripType
from config import settings


def reservation_common_context():
    vehicules = VehiculeType.objects.all()
    trip_types = TripType.objects.all()

    return {
        "mapbox_token": settings.MAPBOX_API_KEY,
        "vehicule_types": vehicules,
        "vehicule_price_km": {
            str(v.id): float(v.vehicule_price_distance or 0)
            for v in vehicules
        },
        "vehicule_price_hour": {
            str(v.id): float(v.vehicule_price_hour or 0)
            for v in vehicules
        },
        "vehicule_seats": {
            str(v.id): v.vehicule_max_seats or 0
            for v in vehicules
        },
        "trip_type": {
            str(t.id): t.trip_type_name
            for t in trip_types
        },
    }
