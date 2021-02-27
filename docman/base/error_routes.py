from docman.base import application
from flask import render_template

@application.errorhandler(400)
def error_400(error):
	print(error)
	return render_template("errors/400.jinja2", title="400"), 400

@application.errorhandler(401)
def error_401(error):
	return render_template("errors/401.jinja2", title = "401"),401

@application.errorhandler(403)
def error_403(error):
	return render_template("errors/401.jinja2", title = "403"),403

@application.errorhandler(404)
def error_404(error):
	return render_template("errors/404.jinja2", title = "404"),404

@application.errorhandler(405)
def error_405(error):
	return render_template("errors/405.jinja2", title = "405"),405

@application.errorhandler(406)
def error_406(error):
	return render_template("errors/406.jinja2", title = "406"),406

@application.errorhandler(408)
def error_408(error):
	return render_template("errors/406.jinja2", title = "408"),408

@application.errorhandler(500)
def error_500(error):
	return render_template("errors/500.jinja2", title = "500"),500

@application.errorhandler(501)
def error_501(error):
	return render_template("errors/501.jinja2", title = "501"),501

@application.errorhandler(502)
def error_502(error):
	return render_template("errors/502.jinja2", title = "502"),502

@application.errorhandler(503)
def error_503(error):
	return render_template("errors/503.jinja2", title = "503"),503

@application.errorhandler(504)
def error_504(error):
	return render_template("errors/504.jinja2", title = "504"),504

@application.errorhandler(505)
def error_505(error):
	return render_template("errors/505.jinja2", title = "505"),505
