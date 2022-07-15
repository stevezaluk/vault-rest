import requests, json

from flask import Flask, g, abort, send_from_directory
from flask_restx import Namespace, Resource

from api.context import get_db, get_plex
from core.utils import dict_to_response

file_namespace = Namespace("file", "Holds file related functions for discovery")

@file_namespace.route("/file/<term>", methods=["GET"])
@file_namespace.route("/file/<section>/<term>", methods=["GET"])
@file_namespace.route("/file/<section>", methods=["POST"])
class File(Resource):
    
    @get_db
    @get_plex
    def get(self, term, section=None):
        sections = g.database.get_collection(g.database.vault_db, "sections")
        if section is None:
            found = False
            sections = g.database.find(sections, {})

            for section in sections:
                collection = g.database.get_collection(g.database.vault_db, section["section_name"])
                query = g.database.build_db_query(term)

                document = g.database.find_one(collection, query)
                if document is not None:
                    found = True
                    ret = dict_to_response(document)
                    keys = ret.keys()

                    if "file_name" in keys:
                        name = ret["file_name"]
                    elif "directory_name" in keys:
                        name = ret["directory_name"]

                    ret.update({"full_path":name + section["section_path"]})
            
                    plex_item, plex_key = g.plex.get_item_key(name)
                    if plex_key:
                        metadata = {"title":plex_item.title, "type": plex_item.type, "description":plex_item.summary, "content_rating":plex_item.contentRating, "user_rating":plex_item.userRating, "plex_section":plex_item.librarySectionTitle, "added_at":str(plex_item.addedAt), "updated_at":str(plex_item.updatedAt), "view_count":plex_item.viewCount}
                        ret.update({"plex_info":metadata})

                    return ret
            
            if found is False:
                abort(404)
            
        else:
            section = g.database.find_one(sections, {"section_name":section})
            if section is None:
                print("[vault-rest] Failed to find section for file search")
                abort(404)

            collection = g.database.get_collection(g.database.vault_db, section["section_name"]) # change section_name to mongo_collection value
            query = g.database.build_db_query(term)

            document = g.database.find_one(collection, query)
            if document is None:
                print("[vault-rest] Failed to find document with query: ", query)
                abort(404)

            ret = dict_to_response(document)
            if "file_name" in ret.keys():
                name = ret["file_name"]
            elif "directory_name" in ret.keys():
                name = ret["directory_name"]

            ret.update({"full_path":name + section["section_path"]})
            
            plex_item, plex_key = g.plex.get_item_key(name)
            if plex_key:
                metadata = {"title":plex_item.title, "type": plex_item.type, "description":plex_item.summary, "content_rating":plex_item.contentRating, "user_rating":plex_item.userRating, "plex_section":plex_item.librarySectionTitle, "added_at":str(plex_item.addedAt), "updated_at":str(plex_item.updatedAt), "view_count":plex_item.viewCount}
                ret.update({"plex_info":metadata})

        return ret

    @get_db
    @get_plex
    def post(self, section):
        pass

@file_namespace.route("/index", methods=["GET"])
@file_namespace.route("/index/<section>", methods=["GET"])
class Index(Resource): # write support for query string args (limit, key)
    
    @get_db
    def get(self, section=None):
        ret = {"results":[]}

        if section is None:
            # untested
            sections = g.database.get_collection(g.database.vault_db, "sections")
            sections = g.database.find(sections, {})

            for section in sections:
                collection = g.database.get_collection(g.database.vault_db, section["section_name"])
                documents = g.database.find(collection, {})

                count = 0
                for document in documents:
                    count += 1
                    document = dict_to_response(document)
                    ret["results"].append(document)

                ret.update({"total_count":count})
        else:
            section = requests.get("http://127.0.0.1:5000/api/v1/sections/{}".format(section))
            if section.status_code == 404:
                print("[vault-rest] Failed to find section for file search")
                abort(404)

            section = json.loads(section.content)

            collection = g.database.get_collection(g.database.vault_db, section["section_name"])
            documents = g.database.find(collection, {})

            count = 0
            for document in documents:
                count += 1
                document = dict_to_response(document)
                ret["results"].append(document)
            
            ret.update({"total_count":count})
        
        return ret

@file_namespace.route("/search", methods=["GET"])
@file_namespace.route("/search/<section>", methods=["GET"])
class Search(Resource):
    
    @get_db
    @get_plex
    def get(self, section):
        if section is None:
            pass
        else:
            section = requests.get("http://127.0.0.1:5000/api/v1/sections/{}".format(section))
            if section.status_code == 404:
                print("[vault-rest] Failed to find section for file search")
                abort(404)

            section = json.loads(section.content)

            collection = g.database.get_collection(g.database.vault_db, section["section_name"])
            # unfinished

@file_namespace.route("/sections", methods=["GET", "POST"])
@file_namespace.route("/sections/<section>", methods=["GET"])
class Sections(Resource): # write support for query string args
    
    @get_db
    def get(self, section=None):
        sections = g.database.get_collection(g.database.vault_db, "sections")
        if section is None:
            ret = {"sections":[]}

            for document in g.database.find(sections, {}):
                ret["sections"].append(document)
        else:
            ret = g.database.find_one(sections, {"section_name":section})
            if ret is None:
                print("Failed to find section: ", section)
                abort(404)

        response = dict_to_response(ret)

        return response
    
    @get_db
    def post(self):
        pass

@file_namespace.route("/upload", methods=["POST"])
@file_namespace.route("/upload/<section>", methods=["POST"])
class Upload(Resource):
    
    @get_db
    @get_plex
    def post(self, section=None):
        if section is None:
            pass
        else:
            pass

@file_namespace.route("/download/<term>", methods=["GET"])
@file_namespace.route("/download/<section>/<term>", methods=["GET"])
class Download(Resource):
    
    @get_db
    def get(self, term, section=None):
        if section is None:
            pass
        else:
            pass

@file_namespace.route("/archive/<hash>", methods=["GET"])
@file_namespace.route("/archive/<section>/<hash>", methods=["GET"])
class Archive(Resource):

    @get_db
    def get(self, hash, section=None):
        if section is None:
            pass
        else:
            pass