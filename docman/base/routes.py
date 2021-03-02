from docman.base import application, config

import os
from flask import render_template, redirect, request, send_from_directory, make_response
from flask_login import login_required
from docman.base.security.login import routes
from docman.base.error_routes import *

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

@application.route('/list', methods = ['GET', 'POST'])
def list_directory():
	from .utils import pretty_print, list_dir
	rootpath = ''
	if request.method == 'GET':
		rootpath = config['BASE_DIR']
	else :
		rootpath = os.path.join(config['BASE_DIR'], *request.data.decode('utf-8').split('/')[1 : ])
	return pretty_print(list_dir(rootpath))

@application.route('/get_file', methods=['POST'])
def get_file():
	filepath = request.data.decode('utf-8')
	split_filepath = filepath.split('/')
	root = os.path.join(config['BASE_DIR'], *split_filepath[1:-1])
	response = make_response(send_from_directory(root, split_filepath[-1], as_attachment=True))
	response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
	return response

@application.route('/upload', methods=['POST'])
def upload(): # POST for upload-processing-tagging
	from .utils import get_keywords, get_extract
	# check if the post request has the file part
	# Add in secure_filepath for directory injection prevention
	file = request.files['new_file']
	filename = file.filename
	filepath = os.path.join(config['STAGE_DIR'], filename)
	file.save(filepath)
	extract = get_extract(filepath)
	keywords = get_keywords(extract)
	suggest = {}
	suggest['staged_filename'] = filename
	suggest['keywords'] = keywords
	suggest['categories'] = {} # provision to be added on later on
	response = make_response(suggest)
	return response
