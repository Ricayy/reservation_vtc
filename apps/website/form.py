from django import forms
from apps.reservations.models import Reservation, VehiculeType

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
