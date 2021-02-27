# from orm.base import application, orm
# from flask_login import login_required, current_user
# from flask import abort, render_template, redirect, make_response, request
#
# from docman.base.dangerous.models import *
# from docman.base.dangerous.utils import privilege_required
# from docman.base.security.login.models import *
# from docman.base.delivery.models import *
# import pandas
#
# @application.route('/user_info')
# @login_required
# def user_info():
# 	return 'OK', 200
#
# @application.route('/user_modify/activate', methods=['POST'])
# @login_required
# @privilege_required
# def approve_user():
# 	user_id = request.form['user_id']
# 	user = User.query.filter_by(user_id = user_id).first()
# 	user.activate(current_user.user_id)
# 	import os
# 	import config
# 	os.makedirs(os.path.join(config['BASE_DIR'], 'user_storage', user_id))
	# from workbench.base.delivery.models import Roles
# 	Roles.add_new_user(user_id)
# 	return 'OK', 200
#
# @application.route('/user_modify/access_level', methods=['POST'])
# @login_required
# @privilege_required
# def change_access_level_user():
# 	type = request.form['type']
# 	user_id = request.form['user_id']
# 	user = User.query.filter_by(user_id=user_id).first()
# 	if user.is_active():
# 		if type == 'promote':
# 			if user.promote(current_user.user_id):
# 				return 'OK', 200
# 			else:
# 				abort(405)
# 		elif type == 'demote':
# 			if user.demote(current_user.user_id):
# 				return 'OK', 200
# 			else:
# 				abort(405)
# 		else:
# 			abort(400)
# 	else:
# 		abort(428)
#
# @application.route('/user_modify/role', methods=['POST'])
# @login_required
# @privilege_required
# def change_role_user():
# 	user_id = request.form['user_id']
# 	role_id = request.form['role_id']
# 	map = UserRoleMap(user_id = user_id, role_id = role_id)
# 	if not map.create():
# 		return 'Failed', 409
# 	return 'OK', 200
#
# @application.route('/user_modify/fetch_all', methods=['GET'])
# @login_required
# @privilege_required
# def fetch_all_users(): # provide all admin changeable information
# 	query = '''select ui.user_id, ui.first_name, ui.last_name, usd.definition as status, ald.definition as access_level
# 	from user_identity ui, user_status_definition usd, user_status us, access_level_definition ald, user_access_level ual
# 	where us.user_id = ui.user_id and ual.user_id = ui.user_id and ald.access_level = ual.access_level and usd.status = us.status and ui.user_id != \'sysadmin\''''
# 	# We have to perform this action either ways. DBMS is object code level, so apply logic at DBMS level to extract faster.
# 	users = pandas.read_sql(query, orm.get_engine(application).connect())
# 	json_str = users.to_json(orient='records')
# 	response = make_response(json_str)
# 	response.mimetype = 'text/json'
# 	return response
#
# @application.route('/user_modify/fetch_role', methods=['POST'])
# @login_required
# @privilege_required
# def fetch_user_role(): # provide all admin changeable information
# 	user_id = request.form['user_id']
# 	query = '''select * from user_role_map where user_id = \'%s\'''' % user_id
# 	users = pandas.read_sql(query, orm.get_engine(application).connect())
# 	json_str = users.to_json(orient='records')
# 	response = make_response(json_str)
# 	response.mimetype = 'text/json'
# 	return response
#
# @application.route('/user_modify/suspend', methods = ['POST'])
# @login_required
# @privilege_required
# def suspend_user():
# 	user_id = request.form['user_id']
# 	user = User.query.filter_by(user_id = user_id).first()
# 	user.suspend(current_user.user_id)
# 	return 'OK', 200
#
# @application.route('/user_modify/delete', methods=['POST'])
# @login_required
# @privilege_required
# def delete_user():
# 	user_id = request.form['user_id']
# 	user = User.query.filter_by(user_id = user_id).first()
# 	user.delete(current_user.user_id)
# 	return 'OK', 200
#
# @application.route('/role_modify/create', methods=['POST'])
# @login_required
# @privilege_required
# def create_role():
# 	role_id = request.form['role_id']
# 	role_description = request.form['role_description']
# 	role_inherit = request.form['inherits']
# 	role = Roles(role_id=role_id, role_desc=role_description, inherits=role_inherit)
# 	role.create()
# 	return 'OK', 200
#
# @application.route('/role_modify/map_connection', methods=['POST'])
# @login_required
# @privilege_required
# def map_role_connection():
# 	role_id = request.form['role_id']
# 	connection_id = request.form['connection_id']
# 	map = RoleConnectionMap(role_id = role_id, connection_id = connection_id)
# 	if not map.create():
# 		return 'Failed', 409
# 	return 'OK', 200
#
# @application.route('/role_modify/map_query', methods=['POST'])
# @login_required
# @privilege_required
# def map_role_query():
# 	role_id = request.form['role_id']
# 	query_id = request.form['query_id']
# 	map = RoleQueryMap(role_id = role_id, query_id = query_id)
# 	if not map.create():
# 		return 'Failed', 409
# 	return 'OK', 200
#
# @application.route('/role_modify/fetch_all')
# @login_required
# @privilege_required
# def fetch_all_roles(): # provide a list of roles
# 	query = '''select * from roles where role_id != \'global\' or role_id != \'universe\''''
# 	roles = pandas.read_sql(query, orm.get_engine(application).connect())
# 	json_str = roles.to_json(orient='records')
# 	response = make_response(json_str)
# 	response.mimetype = 'text/json'
# 	return response
#
# @application.route('/role_modify/get_connections', methods=['POST'])
# @login_required
# @privilege_required
# def fetch_connection_map():
# 	role_id = request.form['role_id']
# 	query = '''select * from role_connection_map where role_id = \'%s\'''' % role_id
# 	roles = pandas.read_sql(query, orm.get_engine(application).connect())
# 	json_str = roles.to_json(orient='records')
# 	response = make_response(json_str)
# 	response.mimetype = 'text/json'
# 	return response
#
# @application.route('/role_modify/get_queries', methods=['POST'])
# @login_required
# @privilege_required
# def fetch_query_map():
# 	role_id = request.form['role_id']
# 	query = '''select * from role_query_map where role_id = \'%s\'''' % role_id
# 	roles = pandas.read_sql(query, orm.get_engine(application).connect())
# 	json_str = roles.to_json(orient='records')
# 	response = make_response(json_str)
# 	response.mimetype = 'text/json'
# 	return response
#
# @application.route('/role_modify/delete', methods=['POST'])
# @login_required
# @privilege_required
# def delete_role():
# 	role_id = request.form['role_id']
# 	role = Roles.query.filter_by(role_id=role_id).first()
# 	role.delete()
# 	return 'OK', 200
#
#
# @application.route('/db_modify/create_connection', methods=['POST'])
# @login_required
# @privilege_required
# def create_connection():
# 	connection_name = request.form['connection_id']
# 	connection_string = request.form['connection_string']
# 	connection = ConnectionProperties(connection_id = connection_name, connection_string = connection_string)
# 	if not connection.create():
# 		abort(400)
# 	return 'OK', 200
#
# @application.route('/db_modify/fetch_all_connections', methods=['GET'])
# @login_required
# @privilege_required
# def fetch_connections():
# 	query = 'select * from connection_properties;'
# 	df = pandas.read_sql(query, orm.get_engine(application).connect())
# 	response = make_response(df.to_json(orient='records'))
# 	response.mimetype = 'text/json'
# 	return response
#
# @application.route('/db_modify/delete_connection', methods=['POST'])# Disfunct for DB Dash
# @login_required
# @privilege_required
# def delete_connection():
# 	connection_id = request.form['connection_id']
# 	connection = ConnectionProperties.query.filter_by(connection_id = connection_id).first()
# 	connection.delete(current_user.user_id)
# 	return 'OK', 200
#
# @application.route('/db_modify/create_query', methods=['POST'])
# @login_required
# @privilege_required
# def create_query():
# 	query = QueryInfo(query_id = request.form['query_id'], query_string = request.form['query_string'])
# 	query.create(request.form['connection_id'])
# 	query.approve()# Remove this. ( caused by delay in delivery )
# 	# Approval requires a different route.
# 	return 'OK', 200
#
# @application.route('/db_modify/fetch_all_queries', methods = ['POST']) # This expects a connection_id
# @login_required
# @privilege_required
# def fetch_queries():
# 	connection_id = request.form['connection_id']
# 	if '=' in connection_id or '\'' in connection_id:
# 		abort(404)
# 	query = '''select qi.query_id, qi.query_string
# 	from query_info qi, query_connection_map qcm
# 	where qi.query_id = qcm.query_id and qcm.connection_id = \'%s\'''' % connection_id # Escapes any injection initiating character
# 	df = pandas.read_sql(query, orm.get_engine(application).connect())
# 	response = make_response(df.to_json(orient='records'))
# 	response.mimetype = 'text/json'
# 	return response
#
# @application.route('/db_modify/delete_query', methods=['POST'])
# @login_required
# @privilege_required
# def delete_query():
# 	query_id = request.form['query_id']
# 	query_approval = QueryApproval.query.filter_by(query_id = query_id).first()
# 	query_approval.delete()
# 	query = QueryInfo.query.filter_by(query_id = query_id).first()
# 	query.delete(current_user.user_id)
# 	return 'OK', 200
#
# @application.route('/view_modify/approve', methods=['POST']) # Disfunct for DB Dash
# @login_required
# @privilege_required
# def approve_view():
# 	view_path = request.form['view_path']
# 	return 'OK', 200
#
# @application.route('/view_modify/recall', methods=['POST'])# Disfunct for DB Dash
# @login_required
# @privilege_required
# def recall_view():
# 	return 'OK', 200
#
# @application.route('/view_modify/fetch_all')
# @login_required
# @privilege_required
# def fetch_all_views():
# 	# This has to be extracted from the external views list.
# 	return abort(501)
