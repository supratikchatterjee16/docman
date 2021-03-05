import os
import json
from operator import itemgetter

def list_dir(path):
	res = {}
	res['files_list'] = []
	for entry in os.listdir(path):
		if not entry in ['app.db', 'config.json', 'staging']:
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
		if word.lower() not in stop_words:
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

def get_keywords_simple(str):
	from nltk.tokenize import word_tokenize
	all_stopwords = ['whence', 'here', 'show', 'were', 'why', 'n’t', 'the', 'whereupon', 'not', 'more', 'how', 'eight', 'indeed', 'i', 'only', 'via', 'nine', 're', 'themselves', 'almost', 'to', 'already', 'front', 'least', 'becomes', 'thereby', 'doing', 'her', 'together', 'be', 'often', 'then', 'quite', 'less', 'many', 'they', 'ourselves', 'take', 'its', 'yours', 'each', 'would', 'may', 'namely', 'do', 'whose', 'whether', 'side', 'both', 'what', 'between', 'toward', 'our', 'whereby', "'m", 'formerly', 'myself', 'had', 'really', 'call', 'keep', "'re", 'hereupon', 'can', 'their', 'eleven', '’m', 'even', 'around', 'twenty', 'mostly', 'did', 'at', 'an', 'seems', 'serious', 'against', "n't", 'except', 'has', 'five', 'he', 'last', '‘ve', 'because', 'we', 'himself', 'yet', 'something', 'somehow', '‘m', 'towards', 'his', 'six', 'anywhere', 'us', '‘d', 'thru', 'thus', 'which', 'everything', 'become', 'herein', 'one', 'in', 'although', 'sometime', 'give', 'cannot', 'besides', 'across', 'noone', 'ever', 'that', 'over', 'among', 'during', 'however', 'when', 'sometimes', 'still', 'seemed', 'get', "'ve", 'him', 'with', 'part', 'beyond', 'everyone', 'same', 'this', 'latterly', 'no', 'regarding', 'elsewhere', 'others', 'moreover', 'else', 'back', 'alone', 'somewhere', 'are', 'will', 'beforehand', 'ten', 'very', 'most', 'three', 'former', '’re', 'otherwise', 'several', 'also', 'whatever', 'am', 'becoming', 'beside', '’s', 'nothing', 'some', 'since', 'thence', 'anyway', 'out', 'up', 'well', 'it', 'various', 'four', 'top', '‘s', 'than', 'under', 'might', 'could', 'by', 'too', 'and', 'whom', '‘ll', 'say', 'therefore', "'s", 'other', 'throughout', 'became', 'your', 'put', 'per', "'ll", 'fifteen', 'must', 'before', 'whenever', 'anyone', 'without', 'does', 'was', 'where', 'thereafter', "'d", 'another', 'yourselves', 'n‘t', 'see', 'go', 'wherever', 'just', 'seeming', 'hence', 'full', 'whereafter', 'bottom', 'whole', 'own', 'empty', 'due', 'behind', 'while', 'onto', 'wherein', 'off', 'again', 'a', 'two', 'above', 'therein', 'sixty', 'those', 'whereas', 'using', 'latter', 'used', 'my', 'herself', 'hers', 'or', 'neither', 'forty', 'thereupon', 'now', 'after', 'yourself', 'whither', 'rather', 'once', 'from', 'until', 'anything', 'few', 'into', 'such', 'being', 'make', 'mine', 'please', 'along', 'hundred', 'should', 'below', 'third', 'unless', 'upon', 'perhaps', 'ours', 'but', 'never', 'whoever', 'fifty', 'any', 'all', 'nobody', 'there', 'have', 'anyhow', 'of', 'seem', 'down', 'is', 'every', '’ll', 'much', 'none', 'further', 'me', 'who', 'nevertheless', 'about', 'everywhere', 'name', 'enough', '’d', 'next', 'meanwhile', 'though', 'through', 'on', 'first', 'been', 'hereby', 'if', 'move', 'so', 'either', 'amongst', 'for', 'twelve', 'nor', 'she', 'always', 'these', 'as', '’ve', 'amount', '‘re', 'someone', 'afterwards', 'you', 'nowhere', 'itself', 'done', 'hereafter', 'within', 'made', 'ca', 'them']
	words = {}
	for word in word_tokenize(str):
		wtr = word.lower()
		if not wtr.isalpha():
			continue
		if word in all_stopwords:
			continue
		else:
			words[wtr] = 1
	return list(words.keys())
