from flask import g, current_app

from vault_lib.core.colors import print_info
from vault_lib.server.server import VAULTServer

def get_resources(func):
    def inner(*args, **kwargs):
        if "server" not in g:
            mongo_ip = current_app.config["MONGO_IP"]
            mongo_port = int(current_app.config["MONGO_PORT"])

            plex_ip = current_app.config["PLEX_IP"]
            plex_port = int(current_app.config["PLEX_PORT"])
            token = current_app.config["PLEX_TOKEN"]

            print_info("Pushing server to request context")

            g.server = VAULTServer(mongo_ip, mongo_port, plex_ip, plex_port, token)
            # g.server.connect()
            g.server.database.connect()

            ret = func(*args, **kwargs)
        return ret
    return inner

def teardown_resources(exception):
    server = g.pop("server", None)

    if server is not None:
        print_info("Disconnecting from server")
        server.disconnect()