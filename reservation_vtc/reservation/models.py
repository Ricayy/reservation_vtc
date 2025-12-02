from django.db import models
from django import forms

# Create your models here.
class Reservation(models.Model):
    address_start = forms.CharField(label="Start address", max_length=100)
    address_stop = forms.CharField(label="Stop address", max_length=100)
    date_start = forms.DateField(label="Start date")
    time_start = forms.TimeField(label="Start time")
    car_type = forms.CharField(label="Car type", max_length=100)
    nb_passengers = forms.IntegerField(label="Number of passengers")
    nb_luggages = forms.IntegerField(label="Number of luggages")
    trip_type = forms.CharField(label="Trip type", max_length=100)
    last_name = forms.CharField(label="Last name")
    first_name = forms.CharField(label="First name")
    phone = forms.CharField(label="Phone number")
    email = forms.EmailField(label="Email")
    note = forms.CharField(label="Note")