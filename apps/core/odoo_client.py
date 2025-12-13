import os
import xmlrpc.client

import requests
from dotenv import load_dotenv

from apps.core.models import OdooContactModel

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
    return OdooClient().query_create_user(user_data)


def create_reservation(user_data):
    return OdooClient().query_create_reservation(user_data)


def search_read_user_by_email(email):
    return OdooClient().query_search_read_user_by_email(email)["result"]


def search_read_reservations_by_user(email):
    return OdooClient().query_search_read_reservations_by_user(email)


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
                }
            }
        ).json()
        self.uid = auth_response["result"]["uid"]

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
                    {"fields": [
                        OdooContactModel.email,
                        OdooContactModel.last_name,
                        OdooContactModel.first_name,
                        OdooContactModel.phone
                    ]},
                ],
            },
        }
        return requests.post(self.url_json, json=json).json()

    def query_create_user(self, user_data):
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
                ]
            }
        }
        return requests.post(self.url_json, json=json).json()

    def query_search_read_reservations_by_user(self, email):
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
                    {"fields": [OdooContactModel.reservation_id]
                     },
                ],
            },
        }
        return requests.post(self.url_json, json=json).json()
