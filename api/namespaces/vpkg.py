from flask import g, abort
from flask_restx import Namespace, Resource

from api.context import get_db
from core.utils import dict_to_response

vpkg_namespace = Namespace("vpkg", "VPKG related functions")

@vpkg_namespace.route("/vpkg", methods=["POST"])
@vpkg_namespace.route("/vpkg/<package_name>", methods=["GET"])
class VPKG(Resource):
    
    @get_db
    def get(self, package_name): # untested
        collection = g.database.get_collection(g.database.vault_db, "vpkg")
        query = {"package_name":package_name.lower()}

        document = g.database.find_one(collection, query)
        if document is None:
            print("[vault-rest] Failed to find package with package name: ", package_name)
            abort(404)

        return dict_to_response(document)

    @get_db
    def post(self):
        pass