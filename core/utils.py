import os

from json import loads
from bson.json_util import dumps

def validate_path(path: str, type="file"):
    if path.startswith("~"):
        path = path.replace("~", os.getenv("HOME"))

    if os.path.exists(path) is False:
        return None

    if type == "file":
        if os.path.isfile(path):
            return path
        else:
            return None
    elif type == "dir":
        if os.path.isdir(path):
            return path
        else:
            return None

def dict_to_response(json: dict):
    if json is None:
        json = {}

    return loads(dumps(json, default=str))