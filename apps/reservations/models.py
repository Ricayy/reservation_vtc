from django.db import models
from django.utils.translation import gettext_lazy as _


class VehiculeType(models.TextChoices):
    CAR = 'car', _('Voiture')
    VAN = 'van', _('Van')


class TripType(models.TextChoices):
    SIMPLE = 'simple', _('Simple')
    HOURLY = 'hourly', _('Mise à disposition')


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    address_start = models.CharField(null=True)
    address_end = models.CharField(null=True)
    date_start = models.DateField(null=True)
    time_start = models.TimeField(null=True)
    car_type = models.CharField(choices=VehiculeType.choices, default=VehiculeType.CAR)
    trip_type = models.CharField(choices=TripType.choices, default=TripType.SIMPLE)
    nb_passengers = models.IntegerField(null=True, default=1)
    nb_luggages = models.IntegerField(null=True, default=0)
    last_name = models.CharField(null=True)
    first_name = models.CharField(null=True)
    phone = models.CharField(null=True)
    email = models.EmailField(null=True)
    note = models.CharField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duration = models.IntegerField(null=True)
    distance = models.FloatField(null=True)
    date_reservation = models.DateField(null=True, auto_now_add=True)

    VEHICULE_DATA = {
        VehiculeType.CAR: {'id': 1, 'max_seats': 4, 'price_distance': 1.80, 'price_hour': 45.0},
        VehiculeType.VAN: {'id': 2, 'max_seats': 7, 'price_distance': 2.50, 'price_hour': 60.0},
    }
    TRIP_DATA = {
        TripType.SIMPLE: {"id": 1},
        TripType.HOURLY: {"id": 2},
    }