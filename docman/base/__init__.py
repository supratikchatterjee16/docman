import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

frontend_filepath_temp = os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)
root_filepath = frontend_filepath_temp[1 : -1]
del frontend_filepath_temp

application = Flask(__name__,
	template_folder = os.path.join('/', *root_filepath, 'frontend', 'templates'),
	static_folder = os.path.join('/', *root_filepath, 'frontend', 'static'),
)# Add the template_folder and static_folder

orm = SQLAlchemy()
login_manager = LoginManager()
# csrf = CSRFProtect()

def create():
	global application, orm, login_manager, config
	application.config.update(config)
	application.config.update(SECRET_KEY = os.urandom(32))
	from docman.base import routes, models
	orm.init_app(application)
	login_manager.init_app(application)
	with application.app_context():
		orm.create_all(bind=None)# Only the main connection
	# print('Routes : ', application.url_map)
	return application

def deploy(_config, deployment_type, port=None):
	def unix_deployment(app, *args):
		import bjoern
		# Unix Sockets should be kept in /tmp/ or /var/run.
		# Windows systems do not have these directories hence...
		bjoern.run(app, 'unix:'+os.path.join(config['BASE_DIR'],'docman.sock'), reuse_port=True)

	def test_deployment(app, port):
		app.run(
			host='0.0.0.0',
			port=port,
			threaded = True,
			debug = True,
			use_debugger = True,
		)
		# ssl_context = ('/home/supratik/Documents/server.crt', '/home/supratik/Documents/server.key')
	def http_deployment(app, port):
		import bjoern
		# This deployment occurs with a seperate edge server(NGINX) handling secure context.
		bjoern.run(app, '0.0.0.0', port, reuse_port = True)
	type = {
		'http' : http_deployment,
		'unix' : unix_deployment,
		'test' : test_deployment
	}
	print('Creating application')
	global config
	config = _config
	config['ROOT_PATH'] = os.path.join('/', *root_filepath)
	app = create()
	type[deployment_type](app, port)
