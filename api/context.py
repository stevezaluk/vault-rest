from flask import g, current_app

from vault_lib.connection.database import Database
from vault_lib.connection.plex import Plex

from vault_lib.core.colors import print_info

def get_db(func):
    def inner(*args, **kwargs):
        if "database" not in g:
            ip_address = current_app.config["MONGO_IP"]
            port = int(current_app.config["MONGO_PORT"])

            print_info("Connecting to database...", ip_address, port)
            g.database = Database(ip_address, port)
            g.database.connect()

            ret = func(*args, **kwargs)
        return ret
    return inner

def get_plex(func):
    def inner(*args, **kwargs):
        if "plex" not in g:
            ip_address = current_app.config["PLEX_IP"]
            port = current_app.config["PLEX_PORT"]
            token = current_app.config["PLEX_TOKEN"]

            print_info("Connecting to plex...",)
            g.plex = Plex(ip_address, port, token)
            g.plex.connect()

            ret = func(*args, **kwargs)
        return ret
    return inner

def teardown_db(exception):
    database = g.pop("database", None)

    if database is not None:
        print_info("Disconnecting from database")
        database.disconnect()

def teardown_plex(exception):
    plex = g.pop("plex", None)

    if plex is not None:
        print_info("Disconnecting from plex")
        plex.disconnect()