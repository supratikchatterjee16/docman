import os

from flask import render_template, redirect, request, send_from_directory, make_response, send_file
from flask_login import login_required

from docman.base import application, config, orm
from docman.base.models import *

from docman.base.error_routes import *
from docman.base.security.login.routes import *

@application.before_first_request
def scan_base_dir():
	from docman.base.utils import list_dir
	dir_list = list_dir(config['BASE_DIR'])
	def track_if_untracked(filename, path):
		vals = Files.add_new(filename, path)
		if not vals[1]:
			if vals[2] != 'unsupported':
				print(filename, " was added.")
			else:
				print(filename, "is unsupported, hence not tracked.")
	def check(path):
		for entry in os.listdir(path):
			if not entry in ['app.db', 'config.json', 'staging']:
				if os.path.isdir(os.path.join(path,entry)):
					check(os.path.join(path,entry))
				elif os.path.isfile(os.path.join(path, entry)) :
					track_if_untracked(entry, os.path.join(path, entry))
	check(config['BASE_DIR'])


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

@application.route('/get_file', methods=['POST'])
def get_files():
	id = request.form['id']
	path = Files.get_path(id)
	resp = send_file(path, as_attachment=True)
	# print(resp)
	return resp

@application.route('/upload', methods=['POST'])
def upload(): # POST for upload-processing-tagging
	from .utils import get_keywords, get_extract, get_keywords_simple
	# check if the post request has the file part
	# Add in secure_filepath for directory injection prevention
	for file in request.files.getlist('files[]'):
		filename = file.filename
		filepath = os.path.join(config['BASE_DIR'], filename)
		file.save(filepath)
		try:
			file_model, exists, determiner = Files.add_new(filename, filepath)
		except:
			abort(417)
	return 'OK'

def get_file_counts(arr):
	counts = {}
	if len(arr) == 0:
		return None
	for i in arr:
		try:
			counts[i['name']][0] += 1
		except:
			counts[i['name']] = (1, i)
	values_sorted = sorted(set([val[0] for val in counts.values()]), reverse = True)
	max_count = max(values_sorted)
	res = []
	for i in values_sorted:
		if i < max_count - 1:
			break
		for k,v in counts.items():
			if v[0] == i:
				res.append(v[1])
	# print(res)
	return res

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
	files = get_file_counts(files)
	result = {
		'files' : files,
		'keywords' : keywords
	}
	# print(result)
	response = make_response(result)
	return response

@application.route('/fetch_result', methods=['GET', 'POST'])
def fetch_results(): # accept type and value
	res = {}
	if request.method == 'POST':
		type = request.form['type']
		id = request.form['id']
		res = {}
		if type == 'file':
			path = Files.get_file(id)
			res['value'] = path
		elif type == 'keyword':
			res['value'] = Keywords.get_files(id)
	elif request.method == 'GET':
		res['value'] = Files.get_list()
	response = make_response(res)
	return response
