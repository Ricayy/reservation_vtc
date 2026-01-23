from django.db import migrations

def create_initial_data(apps, schema_editor):
    VehiculeType = apps.get_model("reservations", "VehiculeType")
    VehiculeType.objects.create(
        vehicule_type_name="Voiture",
        vehicule_max_seats=4,
        vehicule_price_distance=1.80,
        vehicule_price_hour=45.00,
    )
    VehiculeType.objects.create(
        vehicule_type_name="Van",
        vehicule_max_seats=7,
        vehicule_price_distance=2.50,
        vehicule_price_hour=60.00,
    )

    TripType = apps.get_model("reservations", "TripType")
    TripType.objects.create(
        trip_type_name="Simple",
    )
    TripType.objects.create(
        trip_type_name="Mise à disposition",
    )

def delete_initial_data(apps, schema_editor):
    VehiculeType = apps.get_model("reservations", "VehiculeType")
    VehiculeType.objects.all().delete()
    TripType = apps.get_model("reservations", "TripType")
    TripType.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("reservations", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_initial_data, delete_initial_data),
    ]