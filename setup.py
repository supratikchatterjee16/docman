from setuptools import setup, Extension, find_packages

requirements_noversion = [
'Flask',
'Flask-Babel',
'Flask-BabelEx',
'Flask-Compress',
'Flask-HTTPAuth',
'Flask-Login',
'Flask-Mail',
'Flask-Migrate',
'Flask-ReCaptcha',
'Flask-Security',
'flask-session-captcha',
'Flask-SQLAlchemy',
'Flask-SSLify',
'Flask-Table',
'Flask-WTF',
'gunicorn',
'ipaddress',
'nltk',
'numpy',
'openpyxl',
'pandas',
'parsedatetime',
'parsel',
'passlib',
'Pillow',
'plotly',
'PyPDF2',
'pymongo',
'pyperclip',
'psycopg2-binary',
'requests',
'spacy',
'SQLAlchemy',
'urllib3',
'seaborn',
'textract',
]
setup(
	# Meta information
	name				= 'docman',
	version				= '0.0.1',
	author				= 'Supratik Chatterjee',
	author_email		= 'chatterjee.supratik@tcs.com',
	# license			= '2-clause BSD',
	url					= 'https://github.com/supratikchatterjee16',
	description			= 'Documents manager server with CLI interface',
	keywords			= ['Python Search Engine Document KMS'],
	install_requires	= requirements_noversion,
	# build information
	py_modules			= ['docman'],
	packages			= find_packages(),
	package_dir			= {'docman' : './docman'},
	include_package_data= True,
	package_data		= {'docman' : [
								'frontend/*',
								'frontend/*/*',
								'frontend/*/*/*',
								'frontend/*/*/*/*',
								'frontend/*/*/*/*/*',
								'frontend/*/*/*/*/*/*',
								]},

	zip_safe			= True,
	# https://stackoverflow.com/questions/14399534/reference-requirements-txt-for-the-install-requires-kwarg-in-setuptools-setup-py
	entry_points		= {'console_scripts' : ['docman = docman:run'],},
	# ext_modules			= [bjoern_extension],
	classifiers			= [
		"Programming Language :: Python :: 3",
		"Operating System :: OS Independent",
	],
)
