import os

from flask import render_template, redirect, request, send_from_directory, make_response
from flask_login import login_required

from docman.base import application, config, orm
from docman.base.models import *

from docman.base.error_routes import *
from docman.base.security.login import routes

@application.before_request
def secure_before():
	# Check device fingerprint, and session cookies for Device ID
	pass

@application.after_request
def secure_after(response):
	return response

@application.teardown_request
def perform_teardown(error=None):
	pass

# Edit from below

# @login_required
@application.route('/')
def home():
	return render_template('base.jinja2')

# @application.route('/list', methods = ['GET', 'POST'])
# def list_directory():
# 	from .utils import pretty_print, list_dir
# 	rootpath = ''
# 	if request.method == 'GET':
# 		rootpath = config['BASE_DIR']
# 	else :
# 		rootpath = os.path.join(config['BASE_DIR'], *request.data.decode('utf-8').split('/')[1 : ])
# 	return pretty_print(list_dir(rootpath))

# @application.route('/get_file', methods=['POST'])
# def get_file():
# 	filepath = request.data.decode('utf-8')
# 	split_filepath = filepath.split('/')
# 	root = os.path.join(config['BASE_DIR'], *split_filepath[1:-1])
# 	response = make_response(send_from_directory(root, split_filepath[-1], as_attachment=True))
# 	response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
# 	return response

@application.route('/upload', methods=['POST'])
def upload(): # POST for upload-processing-tagging
	from .utils import get_keywords, get_extract, get_keywords_simple
	# check if the post request has the file part
	# Add in secure_filepath for directory injection prevention
	for file in request.files.getlist('files[]'):
		filename = file.filename
		filepath = os.path.join(config['BASE_DIR'], filename)
		file.save(filepath)
		file_model = Files.add_new(filename, filepath)
		keywords = get_keywords_simple(get_extract(filepath))
		for keyword in keywords:
			Keywords.map(keyword, file_model)
	return 'OK'

@application.route('/search', methods=['POST'])
def search():
	from .utils import get_keywords_simple
	keywords = []
	files = []
	term = request.form['search']
	if len(term) > 1:
		files = Files.find(term) # returns list((document_id, document_name))
	terms = get_keywords_simple(term)
	for t in terms:
		files += Keywords.get_files(t)
		keywords += Keywords.get_words(t)
	result = {
		'files' : files,
		'keywords' : keywords
	}
	print(result)
	response = make_response(result)
	return response

@application.route('/fetch_result', methods=['POST'])
def fetch_results(): # accept type and value
	type = request.form['type']
	id = request.form['id']
	res = {}
	if type == 'file':
		path = Files.get_file(id)
		res['value'] = path
	elif type == 'keyword':
		res['value'] = Keywords.get_mapped_files(id)
	return make_response(res)
