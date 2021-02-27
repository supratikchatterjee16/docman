# Decorator to check if the user is local or not
# This is used in the dangerous sections where app update, shutdown and development is expected to be done.
from flask import request
from functools import wraps
import ipaddress

from docman.base import application

current_address_type = None

def its_local(local_type, args = {}):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			ip = None
			if request.headers.getlist("X-Forwarded-For"):
				ip = request.headers.getlist("X-Forwarded-For")[0]
			else:
				ip = request.remote_addr
			# Convert into an ipaddress object
			try:
				ip = ipaddress.ip_address(ip +'/'+ application.config['SUBNET_MASK'])
			except:
				ip = ipaddress.ip_address(ip)# +'/'+ application.config['SUBNET_MASK'])
			if local_type == 'host' and ip.is_loopback:
				return func()
			elif local_type == 'link' and ip.is_link_local:
				return func()
			elif local_type == 'identify':
				global current_address_type
				if ip.is_loopback:
					# print('Host : ', ip.is_loopback)
					current_address_type = 'host'
				elif ip.is_link_local:
					current_address_type = 'link'
				else:
					current_address_type = 'external'
				return func()
			else:
				abort(401)
		return wrapper
	return decorator
