from django import forms

from apps.accounts.models import CustomUser
from apps.reservations.models import Reservation, VehiculeType, TripType


class ReservationForm(forms.ModelForm):
    car_type = forms.ModelChoiceField(
        queryset=VehiculeType.objects.all(),
        empty_label="Sélectionnez un véhicule",
        to_field_name="id"
    )
    trip_type = forms.ModelChoiceField(
        queryset=TripType.objects.all(),
        to_field_name="id"
    )

    class Meta:
        model = Reservation
        fields = "__all__"
        widgets = {
            'date_start': forms.DateInput(attrs={'type': 'date'}),
            'time_start': forms.TimeInput(attrs={'type': 'time'}),
            'car_type': forms.Select(attrs={'id': 'id_car_type'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address_end"].required = False
        self.fields["note"].required = False

    def clean(self):
        cleaned_data = super().clean()
        car_type = cleaned_data.get("car_type")
        nb_passengers = cleaned_data.get("nb_passengers")

        if car_type and nb_passengers is not None:
            max_seats = car_type.vehicule_max_seats
            if nb_passengers < 0:
                self.add_error("nb_passengers", "Le nombre de passagers ne peut pas être négatif.")
            if nb_passengers > max_seats:
                self.add_error(
                    "nb_passengers",
                    f"Le véhicule sélectionné ne permet que {max_seats} places."
                )
        trip_type = cleaned_data.get("trip_type")
        address_end = cleaned_data.get("address_end")

        # 1 = trajet simple
        if trip_type and trip_type.id == 1 and not address_end:
            self.add_error(
                "address_end",
                "L'adresse de destination est obligatoire pour un trajet simple."
            )
        return cleaned_data


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput
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
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput
    )