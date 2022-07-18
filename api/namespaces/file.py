import requests, json

from flask import Flask, g, abort, send_from_directory
from flask_restx import Namespace, Resource

from api.context import get_resources
from core.utils import dict_to_response

from vault_lib.core.colors import print_error, print_info

file_namespace = Namespace("file", "Holds file related functions for discovery")

@file_namespace.route("/file/<term>", methods=["GET"])
@file_namespace.route("/file/<section>/<term>", methods=["GET"])
@file_namespace.route("/file/<section>", methods=["POST"])
class File(Resource):
    
    @get_resources # db & plex
    def get(self, term, section=None):
        g.server.plex.connect() # connect to plex

        file = g.server.get_file(term, section, to_dict=True)
        if file is None:
            print_error("Failed to find file or section: ", term)
            abort(404)

        response = dict_to_response(file)
        return response

    @get_resources
    def post(self, section):
        pass

@file_namespace.route("/index", methods=["GET"])
@file_namespace.route("/index/<section>", methods=["GET"])
class Index(Resource): # write support for query string args (limit, key)
    
    @get_resources
    def get(self, section=None):
        if section is None:
            index = g.server.index(to_dict=True)
        else:
            index = g.server.index(section, to_dict=True)
            if index is None:
                print_error("Failed to find section for index")
                abort(404)
        
        ret = {"index":index}
        response = dict_to_response(ret)

        return response

@file_namespace.route("/search", methods=["GET"])
@file_namespace.route("/search/<section>", methods=["GET"])
class Search(Resource):
    
    @get_resources
    def get(self, section=None):
        if section is None:
            search = g.server.index(to_dict=True)
        else:
            search = g.server.index(section, to_dict=True)
            if search is None:
                print_error("Failed to find section for file search")
                abort(404)

        ret = {"search":search}
        response = dict_to_response(ret)
        
        return response

@file_namespace.route("/sections", methods=["GET", "POST"])
@file_namespace.route("/sections/<section>", methods=["GET"])
class Sections(Resource): # write support for query string args
    
    @get_resources
    def get(self, section=None):
        if section is None:
            ret = {"sections":g.server.get_sections(to_dict=True)}
        else:
            ret = g.server.get_section(section, to_dict=True)
            if ret is None:
                print("Failed to find section: ", section)
                abort(404)

        response = dict_to_response(ret)

        return response
    
    def post(self):
        pass

@file_namespace.route("/upload", methods=["POST"])
@file_namespace.route("/upload/<section>", methods=["POST"])
class Upload(Resource):
    
    def post(self, section=None):
        if section is None:
            pass
        else:
            pass

@file_namespace.route("/download/<term>", methods=["GET"])
@file_namespace.route("/download/<section>/<term>", methods=["GET"])
class Download(Resource):
    
    def get(self, term, section=None):
        if section is None:
            pass
        else:
            pass

@file_namespace.route("/archive/<hash>", methods=["GET"])
@file_namespace.route("/archive/<section>/<hash>", methods=["GET"])
class Archive(Resource):

    def get(self, hash, section=None):
        if section is None:
            pass
        else:
            pass