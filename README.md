# vault-rest
A REST API used to control VAULT databases and to manage uploading/downloading

# Requirements
- vault-lib (https://github.com/stevezaluk/vault-lib.git)
- flask
- flask-caching
- pymongo
- plexapi
- python-dotenv
- argparse

To install: pip3 install -r requirements.txt

# Configuration
vault-rest uses .env files to store the ip address and ports of your resources. For vault-rest to function properly you must pass a few variables to your .env file

PORT : The port you want your REST API to run on. Default is 80

MONGO_IP : The ip address of your running mongoDB instance.
MONGO_PORT : The port of your running mongoDB instance.

PLEX_IP : The ip address of your running plex instance
PLEX_PORT : The port of your running plex instance
PLEX_TOKEN : Your plex access token. See https://www.plex.tv for information on how to get one

# Usage

To start vault-rest run: ./vault-rest.py --start
To stop vault-rest run: ./vault-rest.py --stop
To pass a different .env file ./vault-rest.py --config file.env --start

# Authentication

All vault-rest endpoints require an auth0 access token to call, and the required scope:

Scopes:
read:files - Read file information
write:files - Write file information

read:stats - Read vault statistics

read:standards - Read VAULT upload standards
write:standards - Change vault upload standards

read:vpkg - Read VPKG packages
write:vpkg - Create vpkg packages from VAULT hosted files

upload:movies - Upload to movies
upload:tv - Upload to tv shows
upload:anime - Upload to anime
upload:software - Upload to software
upload:miscvideos - Upload to misc-videos
upload:games - Upload to games
upload:documents - Upload to documents

download:movies - Download to movies
download:tv - Download to tv shows
download:anime - Download to anime
download:software - Download to software
download:miscvideos - Download to misc-videos
download:games - Download to games
download:documents - Download to documents

# Caching



# Endpoints

## Logging in to your account

POST /api/v1/login

Log in to your vault account

## Get file information

GET /file/{term}

Type can be any of the types of media stored on VAULT
Term can either be a file name, file id, or a sha256 hash

Response Example of a Video File:
{
  "_id" : ObjectId("6253bc938bbac9271c5c48c5"),
  "file_name" : "ANNABELLE.mkv",
  "file_id": 1,
  "file_size" : "700.02 MB",
  "file_location" : "/Drive/media/movies",
  "file_type" : "Matroska Video File",
  "file_sha" : "d67af6de7d25d85f48cf0fd29aebeff1aabb6fd2fed431544137ccf10a46d24f",
  "uploaded_by":"zbduid12",
  "uploaded_date":"Aug 12, 2021 (4:30:52 PM)",
  "media_info" : { "resolution" : "1280x534", "encoder" : "x264", "duration" : "1 h 38 min 39 s 336 ms"},
  "plex_info": {"title":"Annabelle", "description":"...", "content_rating":"R", "release_date":"October 1st, 2019"}

}


# Create file information

POST /api/v1/file/{type}

JSON Data must contain:

file_name : The name of the file
file_location : The parent directory of the file (hosted on VAULT)
file_type : The type of file your uploading
file_sha : The SHA256 check sum of the contents of the file

Additionally if your file is a media file it must contain:
encoder : The encoding library used in your video file
duration : The duration of your video file
resolution : The resolution of the file

Your file will automatically be assigned a file_id. Also the file needs to be recognized with plex if you want metadata in your responses.

# Search for a file

GET /api/v1/search

Query:
q : The query (searches within file name, and plex title if recognized)
limit : The number of file docs you want to recieve
encoder : Search for a specific encoding library
resolution : Search by a specific resolution
type : Search by type of media
sort : Sort by order [alphabetical, ascending, descending]

# Download a file

GET /api/v1/download/{term}
GET /api/v1/download/{type}/{term}

Download a file by the specified term

# Upload a file

POST /api/v1/upload/{type}

JSON Data:

file_name : The name of the file

A entry will be created in the database for this file, so theres no need to make multiple calls to the API

# Get VAULT metrics

GET /api/v1/metrics

Returns metrics about vault archive

Example Response:
{
  "vaultdb":{
    "counts":{"movies":0, "tv_shows":0, "anime":0, "misc-videos":0, "games":0, "documents":0, "total":0},
    "most_downloaded_file":"", "least_downloaded_file":"", "total_downloads":0, "total_uploads":0
  },
  "plex":{
    "most_played_movies":"Annabelle", "most_played_tv":"Rick and Morty", "most_played_anime":"Cowboy Bebop", "most_active_user":"", "least_active_user":"",
    "user_count":10, "managed_user_count":5, "remote_user_count":5, "top_genres":["Action", "Horror"], "last_plex_scan":"Mar 8, 2022", "last_scanned_section":"Movies"
  },
  "vpkg":{
    "package_count":10, "most_installed_package":"HomeDiagnostics", "least_installed_package":"automake"
  }
}

# Get Uploading Standards

GET /api/v1/standards

Returns the uploading standards that all uploaded media content must meet

Example Response:
{
  "extensions":[".mkv", ".mp4"], "encoder":"x265", "resolution":"1920x1080", "minimum_total_upload":5, "types":"all"
}

# Get VPKG package information

GET /api/v1/vpkg/{package_name}

Return package information for a package in VPKG

Example Response:
{
  "package_name":"HomeDiagnostics",
  "package_description":"A set of internal apple tools",
  "package_author":"Apple",
  "supported_os":["macOS"],
  "created_by":"zbduid12",
  "created_date":"Aug 12, 2021",
  "associated_files":[ObjectId("1291231239013")]
}

# Create a VPKG package

POST /api/v1/vpkg

Create a new package for VPKG

JSON Data must include:

package_name : The name of your package
package_description : A breif description of your package
package_author : The author of your package
supported_os : A list of supported operating systems
associated_files : A list of objectids for files in the "software collection"
