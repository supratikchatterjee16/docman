import os
import sys
import json
import argparse

# create a keyvalue class
# class type(argparse.Action):
# 	# Constructor calling
# 	def __call__( self , parser, namespace, values, option_string = None):
# 		setattr(namespace, self.dest, dict())


# creating parser object
class ArgsParser(argparse.ArgumentParser):
	def error(self, message):# Modified to show help text on error
		sys.stderr.write('\033[0;31merror: %s\n\n\033[0m' % message)
		self.print_help()
		sys.exit(2)

parser = ArgsParser()
# adding arguments

parser.add_argument('--type',
	help="Type of deployment required. Options : http, unix, test",
	nargs=1,
	required=True,
	metavar="TYPE"
)
parser.add_argument('--directory',
	help="Directory where all data will be stored.",
	nargs=1,
	required=False,
	metavar="DIRECTORY"
)
parser.add_argument('--port',
	help="Port number. Valid only with --type http/test",
	nargs=1,
	required=False,
	metavar="PORT_NUMBER"
)
parser.add_argument('--y',
	help="Assume yes for all options",
	required=False,
	action='store_true'
)

# Default configurations:
config = {
	"BASE_DIR" : "",
	"SERVER_NAME" : "localhost:8000",
	"SQLALCHEMY_DATABASE_URI": "",
	"SQLALCHEMY_BINDS": {},
	"SQLALCHEMY_TRACK_MODIFICATIONS": True,
	"PERMANANENT_SESSION_LIFETIME": 7776000.0,
	"APPLICATION_ROOT": "/",
	# "PREFERRED_URL_SCHEME": "https",
	"JSON_AS_ASCII": True,
	"JSON_SORT_KEYS": True,
	"SESSION_COOKIE_SECURE": False,
	"SESSION_COOKIE_SAMESITE": "Lax",
	"SESSION_COOKIE_HTTPONLY": True,
	"SESSION_COOKIE_NAME": "localhost.dev",
	"TRAP_HTTP_EXCEPTIONS": True,
	"CAPTCHA_ENABLE": False,
	"MAIL_ENABLE": False,
	"LDAP_ENABLE": False,
	"SUBNET_MASK": 32
}


 #parsing arguments
def run():
	global parser, config
	args = parser.parse_args()
	directory = os.getcwd()

	# resolve --directory
	if args.directory:
		directory = args.directory[0]
		if not os.path.isdir(directory):
			sys.stderr.write('\033[0;31mFilepath provided not recognized as a directory\n\n\033[0m')
		try:
			os.makedirs(directory)
		except:
			pass
		try:
			os.makedirs(os.path.join(directory, 'staging'))
		except:
			pass
	else:
		if not args.y:
			resp = input('Use this folder for docman?(y/n) ')
			if resp != 'y':
				print('Directory access rejected.')
				sys.exit(2)
	# This is stored as a convenient reference point
	# Also to force users to identify the folder path to the module,
	# so that they do not consider it arbitrary
	config['BASE_DIR'] = directory
	config['STAGE_DIR'] = os.path.join(directory, 'staging')
	config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(directory, 'app.db')

	# Dump or Load configurations
	config_filepath = os.path.join(directory, 'config.json')
	if not os.path.exists(config_filepath):
		with open(config_filepath, 'w+') as config_fp:
			json.dump(config, config_fp)

	with open(config_filepath, 'r') as config_fp:
		config = json.load(config_fp)

	# resolve --type
	deployment_type = 'test'
	if args.type:
		deployment_type = args.type[0]

	# resolve --port
	port = None
	if args.port:
		port = args.port[0]
		if deployment_type == 'unix':
			sys.stderr.write('\033[1;33mWarning : Port number with unix deployment makes no sense\nIgnored.\n\n\033[0m')
	if not args.port and deployment_type != 'unix':
		port = 8766
		sys.stderr.write('\033[1;33mWarning : Port number not mentioned. Default port is 8766.\n\n\033[0m')

	# Initiate server deployment
	from docman.base import deploy
	print('Starting deployment. Type '+deployment_type)
	deploy(config, deployment_type, port=port)# None set if the argument does not exist

if __name__ == '__main__':
	run()
