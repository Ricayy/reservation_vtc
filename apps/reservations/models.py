from django.db import models


class CarType(models.Model):
    car_type_name = models.CharField(max_length=120)
    def __str__(self):
        return self.car_type_name

class TripType(models.Model):
    trip_type_name = models.CharField(max_length=120)
    def __str__(self):
        return self.trip_type_name


class Reservation(models.Model):
    address_start = models.CharField(null=True)
    address_end = models.CharField(null=True)
    date_start = models.DateField(null=True)
    time_start = models.TimeField(null=True)
    car_type = models.ForeignKey(CarType, on_delete=models.SET_NULL, null=True)
    nb_passengers = models.IntegerField(null=True)
    nb_luggages = models.IntegerField(null=True)
    trip_type = models.ForeignKey(TripType, on_delete=models.SET_NULL, null=True)
    last_name = models.CharField(null=True)
    first_name = models.CharField(null=True)
    phone = models.CharField(null=True)
    email = models.EmailField(null=True)
    note = models.CharField(null=True)
    price = models.FloatField(null=True)
    duration = models.IntegerField(null=True)
    distance = models.FloatField(null=True)
    date_reservation = models.DateField(null=True, auto_now_add=True)
