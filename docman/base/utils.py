import os
import json

def list_dir(path):
	res = {}
	res['files_list'] = []
	for entry in os.listdir(path):
		if os.path.isdir(os.path.join(path,entry)):
			res[entry] = list_dir(os.path.join(path,entry))
		elif os.path.isfile(os.path.join(path, entry)) :
			res['files_list'].append(entry)
	return res # Dictionary

def pretty_print(dict, indent = 0):
	if indent == 0:
		return json.dumps(dict, sort_keys = True) # REST API JSON response
	else:
		return json.dumps(dict, indent = indent, sort_keys = True) # Human readable JSON
