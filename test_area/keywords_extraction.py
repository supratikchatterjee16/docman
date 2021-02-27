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

def get_entities_nltk(str):
	from nltk.tokenize import word_tokenize
	from nltk.tag import pos_tag
	tokens = word_tokenize(str)
	# print('\nTokens : ', tokens)
	tagged = pos_tag(tokens)
	# print('\nTags : ', tagged)
	entities = [x for x in tagged if x[1] == 'NNP' and x[0][0].isupper()]
	# print('\nEntites : ', entities)
	entities = list(set([x[0] for x in entities]))
	print(pos_tag(' '.join(entities).lower().split(' ')))
	return entities

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
	nltk_setup()
	extract = get_extract('wireframe_db_dash.pdf')
	entities = get_entities_ranker(extract)
	print('\n\n\n')
	print("Finally : ", entities)
