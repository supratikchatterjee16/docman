import string, random

from docman.base import orm, application
from docman.base.security.login.models import User

def create_or_update_admin():
	from docman.base.security.local import current_address_type
	sysadmin = User.query.filter_by(user_id='sysadmin').first()
	admin_pass = ''.join(random.choice(string.ascii_letters + string.digits + '<[(@!?/_-+.,:;)]>') for i in range(16))
	if sysadmin:
		sysadmin.set_password(admin_pass)
	else:
		sysadmin = User(user_id='sysadmin')
		sysadmin.set_password(password=admin_pass)
		orm.session.commit()
	try :
		import pyperclip
		pyperclip.copy(admin_pass)
	except :# The next is for the docker installation, where clipbboard will not be provided by design
		print('Clipboard is absent on host')
	finally :
		try:
			with open('/admin_pass.info','w') as pass_file:
				pass_file.write(admin_pass)
		except:
			print('Non sudo user executing.')
		print(admin_pass)
