import datetime

from django.test import TestCase

from .models import Reservation


class MainTestCase(TestCase):
    def test_create_reservation(self):
        """
        Test de création d'une réservation dans la base de test
        """
        nb_res_before = Reservation.objects.count()

        new_res = Reservation()
        new_res.address_start = "11 rue de Belloy"
        new_res.address_end = "Paris"
        new_res.date_start = datetime.date.today()
        new_res.time_start = "18:00:00"
        new_res.car_type = "1"
        new_res.nb_passengers = 1
        new_res.nb_luggages = 0
        new_res.trip_type = "aller-simple"
        new_res.last_name = "doe"
        new_res.first_name = "john"
        new_res.phone = "0750505050"
        new_res.email = "sdfgs@gmail.com"
        new_res.note = "test note"
        new_res.price = 20.35
        new_res.duration = 30
        new_res.distance = 15.35
        new_res.date_reservation = datetime.date.today()

        new_res.save()

        nb_res_after = Reservation.objects.count()

        self.assertTrue(nb_res_after == nb_res_before + 1)

    def test_get_reservation(self):
        """
        Test de récupération d'une réservation dans la base de test
        """
        pass

    def test_get_reservation_by_id(self):
        """
        Test de récupération d'une réservation dans la base de test par id
        """
        pass

    def test_modify_reservation(self):
        """
        Test de récupération d'une réservation dans la base de test par id
        """
        pass

    def test_delete_reservation(self):
        """
        Test de récupération d'une réservation dans la base de test par id
        """
        pass

