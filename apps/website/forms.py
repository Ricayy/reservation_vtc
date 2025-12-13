from django import forms

from apps.accounts.models import CustomUser
from apps.reservations.models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"
        widgets = {
            'date_start': forms.DateInput(attrs={'type': 'date'}),
            'time_start': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        car_type = cleaned_data.get("car_type")
        nb_passengers = cleaned_data.get("nb_passengers")

        if car_type and nb_passengers is not None:
            max_seats = car_type.vehicule_max_seats

            # Erreur si négatif
            if nb_passengers < 0:
                self.add_error("nb_passengers", "Le nombre de passagers ne peut pas être négatif.")

            # Erreur si trop élevé
            if nb_passengers > max_seats:
                self.add_error(
                    "nb_passengers",
                    f"Le véhicule sélectionné ne permet que {max_seats} places."
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

        user.username = email  # important
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