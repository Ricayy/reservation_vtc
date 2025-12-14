import uuid

from django.db import models


class VehiculeType(models.Model):
    id = models.AutoField(primary_key=True)
    vehicule_type_name = models.CharField(max_length=120)
    vehicule_max_seats = models.IntegerField(null=True)
    vehicule_price_distance = models.FloatField(null=True)
    def __str__(self):
        return self.vehicule_type_name

class TripType(models.Model):
    id = models.AutoField(primary_key=True)
    trip_type_name = models.CharField(max_length=120)
    def __str__(self):
        return self.trip_type_name


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    address_start = models.CharField(null=True)
    address_end = models.CharField(null=True)
    date_start = models.DateField(null=True)
    time_start = models.TimeField(null=True)
    car_type = models.ForeignKey(VehiculeType, on_delete=models.SET_NULL, null=True)
    nb_passengers = models.IntegerField(null=True, default=1)
    nb_luggages = models.IntegerField(null=True, default=0)
    trip_type = models.ForeignKey(TripType, on_delete=models.SET_NULL, null=True)
    last_name = models.CharField(null=True)
    first_name = models.CharField(null=True)
    phone = models.CharField(null=True)
    email = models.EmailField(null=True)
    note = models.CharField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    duration = models.IntegerField(null=True)
    distance = models.FloatField(null=True)
    date_reservation = models.DateField(null=True, auto_now_add=True)
    # public_token = models.UUIDField(default=uuid.uuid4, unique=True)
    #
    # def get_public_url(self):
    #     return f"/reservation/{self.public_token}/"
