import sys
from dotenv import dotenv_values
from flask import Flask
from flask_restx import Api

from api.context import teardown_db, teardown_plex

from api.namespaces.file import file_namespace
from api.namespaces.metrics import metrics_namespace
from api.namespaces.vpkg import vpkg_namespace

class RestAPI(object):
    def __init__(self, debug=False):
        self._app = Flask(__name__)
        self._api = Api(app=self._app)
        
        self.debug = debug

        self.build_config()
        self._register_teardowns()
        self._build_namespaces()

    def build_config(self, config_file="{}/.env".format(sys.path[0])):
        keys = ["MONGO_IP", "MONGO_PORT", "PLEX_IP", "PLEX_PORT", "PLEX_TOKEN"]
        values = dotenv_values(config_file)

        for key in values:
            if key in keys:
                value = values[key]
                self._app.config[key] = value

    def _register_teardowns(self):
        self._app.teardown_appcontext(teardown_db)
        self._app.teardown_appcontext(teardown_plex)

    def _build_namespaces(self):
        self._api.add_namespace(file_namespace, path="/api/v1/")
        self._api.add_namespace(metrics_namespace, path="/api/v1/")
        self._api.add_namespace(vpkg_namespace, path="/api/v1/")

    def start(self):
        self._app.run(debug=self.debug)
    
    def stop(self):
        pass