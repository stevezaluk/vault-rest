from flask import g, abort
from flask_restx import Namespace, Resource

from api.context import get_db, get_plex

metrics_namespace = Namespace("metrics", "Contains functions related to statistics")

@metrics_namespace.route("/standards", methods=["GET"])
@metrics_namespace.route("/standards/<type>", methods=["GET", "POST"])
class Standards(Resource):

    @get_db
    def get(self, type=None):
        if type is None:
            pass
        elif type == "upload":
            pass
        elif type == "download":
            pass