import os

import requests
from dotenv import load_dotenv

from apps.core.models import OdooContactModel, OdooReservationModel

load_dotenv()


def json_search_read(db, uid, password, app, id_odoo, fields):
    return {
        "jsonrpc": "2.0",
        "method": "call",
        "id": 1,
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                db,
                uid,
                password,
                app,
                "search_read",
                [[["id", "in", id_odoo]]],
                {"fields": fields},
            ],
        },
    }


def create_user(user_data):
    """
    Fonction d'appel de la requête Odoo de création d'un utilisateur
    :param user_data:
    :return:
    """
    return OdooClient().query_create_user(user_data)


def create_res(user_data):
    """
    Fonction d'appel de la requête Odoo de création d'une réservation
    :param user_data:
    :return:
    """
    return OdooClient().query_create_reservation(user_data)


def get_user_by_email(email):
    """
    Fonction d'appel de la requête Odoo de récupération d'un utilisateur par adresse email

    :param email:
    :return:
    """
    return OdooClient().query_search_read_user_by_email(email)["result"]


def get_user_by_id(id_res):
    """
    Fonction d'appel de la requête Odoo de récupération d'un utilisateur par id Odoo

    :param id_res:
    :return:
    """
    return OdooClient().query_search_read_user_by_id(id_res)["result"]


def get_res_by_email(email):
    """
    Fonction d'appel de la requête Odoo de récupération d'une réservation par adresse email

    :param email:
    :return:
    """
    res_id = OdooClient().query_search_read_res_by_user(email)
    return OdooClient().query_search_read_res_by_id(
        res_id["result"][0][OdooContactModel.reservation_id]
    )


def get_res_by_id(id_res):
    """
    Fonction d'appel de la requête Odoo de récupération d'une réservation par id Odoo

    :param id_res:
    :return:
    """
    return OdooClient().query_search_read_res_by_id(id_res)["result"]


class OdooClient:
    def __init__(self):
        """
        Constructeur class OdooClient
        Permet l'authentification à Odoo
        """
        self.url = os.getenv("ODOO_URL")
        self.url_json = os.getenv("ODOO_URL_JSON")
        self.db = os.getenv("ODOO_DB")
        self.username = os.getenv("ODOO_USERNAME")
        self.password = os.getenv("ODOO_PASSWORD")
        self.app_reservation = os.getenv("ODOO_APP_RESERVATION")
        self.app_contact = os.getenv("ODOO_APP_CONTACT")

        auth_response = requests.post(
            f"{self.url}/web/session/authenticate",
            json={
                "jsonrpc": "2.0",
                "params": {
                    "db": self.db,
                    "login": self.username,
                    "password": self.password,
                },
            },
        ).json()
        self.uid = auth_response["result"]["uid"]

    def query_create_user(self, user_data):
        """

        :param user_data:
        :return:
        """
        json = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": 1,
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    self.uid,
                    self.password,
                    self.app_contact,
                    "create",
                    [user_data],
                ],
            },
        }
        return requests.post(self.url_json, json=json).json()

    def query_create_reservation(self, values):
        """
        Méthode de publication d'une réservation dans Odoo

        :param values: Dict[str]
            Dictionnaire contenant une réservation à publier sur Odoo
        :return:
            Résultat de la requête de création
        """
        json = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": 1,
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    self.uid,
                    self.password,
                    self.app_reservation,
                    "create",
                    [values],
                ],
            },
        }
        return requests.post(self.url_json, json=json).json()

    def query_search_read_user_by_email(self, email):
        """

        :param email:
        :return:
        """
        json = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": 1,
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    self.uid,
                    self.password,
                    self.app_contact,
                    "search_read",
                    [[[OdooContactModel.email, "in", [email]]]],
                    {
                        "fields": [
                            OdooContactModel.email,
                            OdooContactModel.last_name,
                            OdooContactModel.first_name,
                            OdooContactModel.phone,
                        ]
                    },
                ],
            },
        }
        return requests.post(self.url_json, json=json).json()

    def query_search_read_user_by_id(self, id_res):
        """

        :param id_res:
        :return:
        """
        json = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": 1,
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    self.uid,
                    self.password,
                    self.app_contact,
                    "search_read",
                    [[[OdooContactModel.id, "in", [id_res]]]],
                    {
                        "fields": [
                            OdooContactModel.email,
                            OdooContactModel.last_name,
                            OdooContactModel.first_name,
                            OdooContactModel.phone,
                        ]
                    },
                ],
            },
        }
        return requests.post(self.url_json, json=json).json()

    def query_search_read_res_by_user(self, email):
        """

        :param email:
        :return:
        """
        json = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": 1,
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    self.uid,
                    self.password,
                    self.app_contact,
                    "search_read",
                    [[[OdooContactModel.email, "in", [email]]]],
                    {"fields": [OdooContactModel.reservation_id]},
                ],
            },
        }
        return requests.post(self.url_json, json=json).json()

    def query_search_read_res_by_id(self, reservations_id):
        """

        :param reservations_id:
        :return:
        """
        json = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": 1,
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db,
                    self.uid,
                    self.password,
                    self.app_reservation,
                    "search_read",
                    [[[OdooReservationModel.id, "in", reservations_id]]],
                    {
                        "fields": [
                            OdooReservationModel.email,
                            OdooReservationModel.address_start,
                            OdooReservationModel.address_end,
                            OdooReservationModel.car_type,
                            OdooReservationModel.trip_type,
                            OdooReservationModel.datetime_start,
                            OdooReservationModel.price,
                            OdooReservationModel.distance,
                            OdooReservationModel.duration,
                            OdooReservationModel.note,
                        ]
                    },
                ],
            },
        }
        return requests.post(self.url_json, json=json).json()
