import os
from datetime import datetime

import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import TestCase
from dotenv import load_dotenv
load_dotenv()


class OdooTestCase(TestCase):
    """
    Classe de test des requêtes Odoo

    test_odoo_auth
        Test d'authentification à Odoo
    test_odoo_search_read
        Test de recherche et de lecture de ligne par ID
    test_odoo_create
        Test de publication d'une réservation sur Odoo
    test_odoo_simple_create
        Test de publication rapide d'une réservation sur Odoo
    test_odoo_delete
        Test de suppression d'une réservation sur Odoo

    url : str
        URL du domaine odoo
    url_json : str
        URL d'appel de l'API Odoo
    db : str
        Nom de la base de données Odoo
    app : str
        Nom de l'application Odoo
    login : str
        Nom de l'utilisateur Odoo
    password : str
        Mot de passe de l'utilisateur Odoo
    fields_dict : dict
        Dictionnaire des noms de champs Odoo
    fields_list : list
        Liste des noms de champs Odoo
    """
    url = os.getenv("ODOO_URL")
    url_json = os.getenv("ODOO_URL_JSON")
    db = os.getenv("ODOO_DB")
    app = os.getenv("ODOO_APP_RESERVATION")
    login = os.getenv("ODOO_USERNAME")
    password = os.getenv("ODOO_PASSWORD")
    fields_dict = {
        "x_studio_address_start": "x_studio_address_start",
        "x_studio_address_end": "x_studio_address_end",
        "x_studio_datetime_start": "x_studio_datetime_start",
        "x_studio_nb_passengers": "x_studio_nb_passengers",
        "x_studio_nb_luggages": "x_studio_nb_luggages",
        "x_studio_last_name": "x_studio_last_name",
        "x_studio_first_name": "x_studio_first_name",
        "x_studio_phone": "x_studio_phone",
        "x_studio_email": "x_studio_email",
        "x_studio_note": "x_studio_note",
        "x_studio_price": "x_studio_price",
        "x_studio_duration": "x_studio_duration",
        "x_studio_distance": "x_studio_distance",
        # "x_studio_car_type": "x_studio_car_type",
        # "x_studio_trip_type": "x_studio_trip_type",
    }
    fields_list = [
        "x_studio_address_start",
        "x_studio_address_end",
        "x_studio_datetime_start",
        "x_studio_nb_passengers",
        "x_studio_nb_luggages",
        "x_studio_last_name",
        "x_studio_first_name",
        "x_studio_phone",
        "x_studio_email",
        "x_studio_note",
        "x_studio_price",
        "x_studio_duration",
        "x_studio_distance",
        # "x_studio_car_type",
        # "x_studio_trip_type",
    ]


    def test_odoo_auth(self):
        """
        Test d'authentification à Odoo

        :return: int
            ID user Odoo
        """

        auth_response = requests.post(
            f"{self.url}/web/session/authenticate",
            json={
                "jsonrpc": "2.0",
                "params": {
                    "db": self.db,
                    "login": self.login,
                    "password": self.password,
                }
            }
        ).json()
        print(auth_response)
        uid = auth_response["result"]["uid"]
        assert uid, "Échec authentification"
        return uid

    def test_odoo_search_read(self):
        """
        Test de lecture d'une ligne par ID
        """
        uid = self.test_odoo_auth()

        payload_search_read = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": 1,
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    uid,
                    self.password,
                    self.app,
                    "search_read",
                    [[["id", "in", [2, 3]]]],
                    {"fields": self.fields_list},
                ],
            },
        }

        response = requests.post(self.url_json, json=payload_search_read).json()
        print(response)
        self.assertTrue("result" in response)

    def test_odoo_create(self):
        """
        Test de publication d'une réservation sur Odoo
        """
        uid = self.test_odoo_auth()

        reservation_data = {
            self.fields_dict["x_studio_address_start"]: "Gare de Lyon",
            self.fields_dict["x_studio_address_end"]: "10 Rue de Paris, Paris",
            self.fields_dict["x_studio_datetime_start"]: datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            self.fields_dict["x_studio_nb_passengers"]: 3,
            self.fields_dict["x_studio_nb_luggages"]: 3,
            self.fields_dict["x_studio_last_name"]: "Dupont",
            self.fields_dict["x_studio_first_name"]: "Jean",
            self.fields_dict["x_studio_phone"]: "0781546425",
            self.fields_dict["x_studio_email"]: "jean.dupont@gmail.com",
            self.fields_dict["x_studio_note"]: "En bas d'un immeuble bleu",
            self.fields_dict["x_studio_price"]: 35.78,
            self.fields_dict["x_studio_duration"]: 20,
            self.fields_dict["x_studio_distance"]: 12.7,
            # self.fields_dict["x_studio_car_type"]: "x_studio_car_type",
            # self.fields_dict["x_studio_trip_type"]: "x_studio_trip_type",
        }

        payload_create = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": 1,
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    uid,
                    self.password,
                    self.app,
                    "create",
                    [reservation_data],
                ],
            },
        }

        create_response = requests.post(self.url_json, json=payload_create).json()
        print("Create response:", create_response)
        self.assertIn("result", create_response, "Odoo n'a pas renvoyé d'ID")
        new_reservation_id = create_response["result"]
        self.assertIsInstance(new_reservation_id, int, "ID invalide")

        payload_read = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": 2,
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    uid,
                    self.password,
                    self.app,
                    "search_read",
                    [[["id", "=", new_reservation_id]]],
                    {"fields": self.fields_list},
                ],
            },
        }

        read_response = requests.post(self.url_json, json=payload_read).json()
        print("Read response:", read_response)

        self.assertIn("result", read_response, "Échec lecture Odoo")
        self.assertEqual(len(read_response["result"]), 1)

        record = read_response["result"][0]
        print(record)
        self.assertEqual(record["x_studio_address_start"], reservation_data["x_studio_address_start"])
        self.assertEqual(record["x_studio_address_end"], reservation_data["x_studio_address_end"])
        self.assertEqual(record["x_studio_datetime_start"], reservation_data["x_studio_datetime_start"])
        self.assertEqual(record["x_studio_nb_passengers"], reservation_data["x_studio_nb_passengers"])
        self.assertEqual(record["x_studio_nb_luggages"], reservation_data["x_studio_nb_luggages"])
        self.assertEqual(record["x_studio_last_name"], reservation_data["x_studio_last_name"])
        self.assertEqual(record["x_studio_first_name"], reservation_data["x_studio_first_name"])
        self.assertEqual(record["x_studio_phone"], reservation_data["x_studio_phone"])
        self.assertEqual(record["x_studio_email"], reservation_data["x_studio_email"])
        self.assertEqual(record["x_studio_note"], reservation_data["x_studio_note"])
        self.assertEqual(record["x_studio_price"], reservation_data["x_studio_price"])
        self.assertEqual(record["x_studio_duration"], reservation_data["x_studio_duration"])
        self.assertEqual(record["x_studio_distance"], reservation_data["x_studio_distance"])
        # self.assertEqual(record["x_studio_car_type"], reservation_data["x_studio_car_type"])
        # self.assertEqual(record["x_studio_trip_type"], reservation_data["x_studio_trip_type"])

    def test_odoo_simple_create(self, uid):
        """
        Test de publication d'une réservation sur Odoo

        :return: int
            ID de la réservation créée
        """

        reservation_data = {
            self.fields_dict["x_studio_address_start"]: "Gare de Lyon",
            self.fields_dict["x_studio_address_end"]: "10 Rue de Paris, Paris",
            self.fields_dict["x_studio_datetime_start"]: datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            self.fields_dict["x_studio_nb_passengers"]: 3,
            self.fields_dict["x_studio_nb_luggages"]: 3,
            self.fields_dict["x_studio_last_name"]: "Dupont",
            self.fields_dict["x_studio_first_name"]: "Jean",
            self.fields_dict["x_studio_phone"]: "0781546425",
            self.fields_dict["x_studio_email"]: "jean.dupont@gmail.com",
            self.fields_dict["x_studio_note"]: "En bas d'un immeuble bleu",
            self.fields_dict["x_studio_price"]: 35.78,
            self.fields_dict["x_studio_duration"]: 20,
            self.fields_dict["x_studio_distance"]: 12.7,
            # self.fields_dict["x_studio_car_type"]: "x_studio_car_type",
            # self.fields_dict["x_studio_trip_type"]: "x_studio_trip_type",
        }

        payload_create = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": 1,
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    uid,
                    self.password,
                    self.app,
                    "create",
                    [reservation_data],
                ],
            },
        }

        create_response = requests.post(self.url_json, json=payload_create).json()
        new_reservation_id = create_response["result"]
        print("New reservation ID:", new_reservation_id)
        return new_reservation_id

    def test_odoo_delete(self):
        """
        Test de suppression d'une réservation sur Odoo
        """
        uid = self.test_odoo_auth()
        new_reservation_id = self.test_odoo_simple_create(uid)
        payload_delete = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": 1,
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    uid,
                    self.password,
                    self.app,
                    "unlink",
                    [[new_reservation_id]],
                ],
            },
        }

        delete_response = requests.post(self.url_json, json=payload_delete).json()
        print("Delete response:", delete_response)
        self.assertIn("result", delete_response, "Odoo n'a pas renvoyé de confirmation de suppression")
        self.assertTrue(delete_response["result"], "La suppression a échoué")

        payload_read = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": 2,
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    uid,
                    self.password,
                    self.app,
                    "search_read",
                    [[["id", "=", new_reservation_id]]],
                    {"fields": self.fields_list},
                ],
            },
        }

        read_response = requests.post(self.url_json, json=payload_read).json()
        print("Read response after delete:", read_response)
        self.assertIn("result", read_response, "Échec lecture Odoo après suppression")
        self.assertEqual(len(read_response["result"]), 0, "La réservation existe encore après suppression")
