from datetime import datetime, timedelta

from django import forms
from django.utils import timezone

from apps.accounts.models import CustomUser
from apps.reservations.models import Reservation, VehiculeType, TripType


class ReservationForm(forms.ModelForm):
    car_type = forms.ChoiceField(
        choices=VehiculeType.choices,
        widget=forms.Select(attrs={"id": "id_car_type"}),
        required=True,
    )

    trip_type = forms.ChoiceField(
        choices=TripType.choices,
        required=True,
    )

    class Meta:
        model = Reservation
        fields = "__all__"
        widgets = {
            "date_start": forms.DateInput(attrs={"type": "date"}),
            "time_start": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address_end"].required = False
        self.fields["note"].required = False

    def clean(self):
        cleaned_data = super().clean()

        # Date et heure
        date_start = cleaned_data.get("date_start")
        time_start = cleaned_data.get("time_start")

        if date_start and time_start:
            selected_dt = datetime.combine(date_start, time_start)

            if timezone.is_naive(selected_dt):
                selected_dt = timezone.make_aware(selected_dt)

            min_dt = timezone.now() + timedelta(minutes=15)

            if selected_dt <= min_dt:
                self.add_error(
                    "date_start",
                    "La date et l’heure doivent être au moins 15 minutes dans le futur."
                )

        # Passagers
        car_type = cleaned_data.get("car_type")
        nb_passengers = cleaned_data.get("nb_passengers")

        if car_type and nb_passengers is not None:
            max_seats = Reservation.VEHICULE_DATA[car_type]["max_seats"]

            if nb_passengers < 1:
                self.add_error(
                    "nb_passengers",
                    "Le nombre de passagers doit être au minimum 1."
                )

            if nb_passengers > max_seats:
                self.add_error(
                    "nb_passengers",
                    f"Le véhicule sélectionné ne permet que {max_seats} places."
                )

        # Trajet simple -> adresse d’arrivée obligatoire
        trip_type = cleaned_data.get("trip_type")
        address_end = cleaned_data.get("address_end")

        if trip_type == TripType.SIMPLE and not address_end:
            self.add_error(
                "address_end",
                "L'adresse de destination est obligatoire pour un trajet simple."
            )

        return cleaned_data


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirmation du mot de passe", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ["email"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Les mots de passe ne correspondent pas")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"]

        user.username = email
        user.email = email
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
