import os
import xmlrpc.client

from dotenv import load_dotenv
load_dotenv()


class OdooClient:
    def __init__(self):
        """
        Constructeur class OdooClient
        Permet l'authentification à Odoo
        """
        self.url = os.getenv("ODOO_URL")
        self.db = os.getenv("ODOO_DB")
        self.username = os.getenv("ODOO_USERNAME")
        self.password = os.getenv("ODOO_PASSWORD")
        self.app_name = os.getenv("ODOO_APP_NAME")
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
        result = self.models.execute_kw(self.db, self.auth, self.password, self.app_name, "create",
                                      [values])
        return result

