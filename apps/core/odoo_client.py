import os
import xmlrpc.client

from dotenv import load_dotenv


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
        common = xmlrpc.client.ServerProxy("%s/xmlrpc/2/common" % self.url)
        self.auth = common.authenticate(self.db, self.username, self.password, {})
        self.models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(self.url))

    def create_reservation(self, values):
        """
        Méthode de publication d'une réservation dans Odoo

        :param values: Dict[str]
            Dictionnaire contenant une réservation à publier sur Odoo
        :return result:
            Résultat de la requête de création
        """
        result = self.models.execute_kw(self.db, self.auth, self.password, self.app_reservation, "create",
                                        [values])
        return result
