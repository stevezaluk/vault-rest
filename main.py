import os, sys

from argparse import ArgumentParser

from core.utils import validate_path
from api.api import RestAPI

# \b[A-Fa-f0-9]{64}\b sha256 regex

def usage():
	print("vault-rest - VAULT archive REST api")
	print("		--start : Start the API")
	print("		--stop : Stop the API")
	print("		--config FILE : Specify .env file")
	print("		--debug : Enable debug mode for Flask application")

parser = ArgumentParser()
parser.add_argument("--start", dest="start", action="store_true", help="Start the API")
parser.add_argument("--stop", dest="stop", action="store_true", help="Stop the API")
parser.add_argument("--config", dest="config", action="store", help="Specify .env file")
parser.add_argument("--debug", dest="debug", action="store_true", help="Enable debug mode")

if __name__ == '__main__':
	# if len(sys.argv) > 1:
	# 	usage()
	# 	sys.exit()

	args = parser.parse_args()

	r = RestAPI()

	if args.debug:
		r.debug = True

	if args.config:
		config_path = validate_path(args.config)
		if config_path:
			r.build_config(args.config)
		else:
			print("[error] Invalid config file: ", args.config)
			sys.exit(1)

	if args.start:
		r.start()

	if args.stop:
		r.stop()
