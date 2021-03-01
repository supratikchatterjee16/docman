import textract, nltk

def nltk_setup():
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

def get_extract(filepath):
	import textract
	extract = textract.process(filepath)
	text = extract.decode('utf-8')
	return text

def get_entities_nltk(str): # TF-IDF method
	import math
	from nltk.tag import pos_tag
	from nltk.corpus import stopwords
	from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer
	from operator import itemgetter
	word_tokenizer = RegexpTokenizer(r'\w+')
	words = word_tokenizer.tokenize(str.lower())
	sentences = sent_tokenize(str)
	# words_tagged = pos_tag(tokens)
	stop_words = set(stopwords.words('english'))
	tf_score = {}
	idf_score = {}
	def check_sent(word, sentences): # Count word occurance in sentences
		final = [all([w in x for w in word]) for x in sentences]
		sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
		return int(len(sent_len))
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

	# Update TF as fraction score
	tf_score.update((x, y / len(words)) for x, y in tf_score.items())
	# Update IDF as log values
	idf_score.update((x, math.log(int(len(sentences))/y)) for x, y in idf_score.items())
	# print(idf_score)
	# TF-IDF score
	tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
	def get_top_n(dict_elem, n):
		result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n])
		return result
	return get_top_n(tf_idf_score, 20)
	# entities = [x for x in tagged if x[1] == 'NNP' and not x[0] in stop_words]
	# entities = list(set([x[0] for x in entities]))
	# print(pos_tag(' '.join(entities).lower().split(' ')))
	# return entities

def get_entities_spacy(str):
	import spacy, en_core_web_lg, re
	nlp = en_core_web_lg.load()
	doc = nlp(re.sub('[\n\(\)]', ' ', str))
	entities = list(set([X.text for X in doc.ents if X.label_ == 'ORG']))
	return entities

def get_entities_ranker(str):
	stop_words = []
	from nltk.tokenize import word_tokenize
	import json
	tokens = word_tokenize(str)
	count_list = {}
	for token in tokens:
		if token in count_list.keys():
			count_list[token] += 1
		else:
			count_list[token] = 1
	count_list = dict(sorted(count_list.items(), key=lambda item: item[1], reverse = True))
	strlen = len(str)
	count_list = {k: (v, v/strlen) for k, v in count_list.items()}
	print(json.dumps(count_list, indent = 4))
	return count_list.keys()

if __name__ == '__main__':
	import json
	nltk_setup()
	arr = ['M01_Solution_Overview_Functional.pptx', 'M02-Oracle Retail Solution Blueprint.pptx', 'M03A_FoundationData-OrgHierarchy.pptx']
	for filename in arr:
		extract = get_extract(filename)
		entities = get_entities_nltk(extract)
		print('\n\n\n'+ filename)
		print(json.dumps(entities, indent=4))
