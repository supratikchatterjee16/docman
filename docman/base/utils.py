import os
import json
from operator import itemgetter

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

def get_top_n(dict_elem, n): # Get top 'n' elements of a dict
	result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n])
	return result

# Document utilities
def nltk_setup():
	import nltk
	nltk.download('punkt')
	nltk.download('stopwords')
	nltk.download('brown')
	nltk.download('averaged_perceptron_tagger')
	# nltk.download('maxent_ne_chunker')
	# nltk.download('word2vec_sample')
	# nltk.donwload('webtext')
	# nltk.download('verbnet3')
	# nltk.download('penn')
	# nltk.donwload('indian')

def get_extract(filepath): # Extract the contents of a file
	import textract
	extract = textract.process(filepath)
	text = extract.decode('utf-8')
	return text

def get_keywords(str): # TF-IDF score method
	import math
	from nltk.tag import pos_tag
	from nltk.corpus import stopwords
	from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer
	def check_sent(word, sentences):
		final = [all([w in x for w in word]) for x in sentences]
		sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
		return int(len(sent_len))
	word_tokenizer = RegexpTokenizer(r'\w+')
	words = word_tokenizer.tokenize(str)
	sentences = sent_tokenize(str)
	stop_words = set(stopwords.words('english'))
	tf_score = {}
	idf_score = {}
	for word in words:
		if word.isnumeric():
			continue
		if word not in stop_words:
			if word in tf_score:
				tf_score[word] += 1
			else:
				tf_score[word] = 1
			if not word in idf_score:
				score = check_sent([word], sentences)
				idf_score[word] = score if score != 0 else 1

	tf_score.update((x, y / len(words)) for x, y in tf_score.items())
	idf_score.update((x, math.log(int(len(sentences))/y)) for x, y in idf_score.items())
	tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
	return get_top_n(tf_idf_score, 10)
