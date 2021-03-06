import json

from datetime import datetime

from docman.base import orm
from docman import config

class Files(orm.Model, json.JSONEncoder):
	__tablename__ = 'documents'
	__table_args__ = (
		orm.PrimaryKeyConstraint('document_id'),
	)
	document_id = orm.Column(orm.Integer, primary_key = True)
	document_name = orm.Column(orm.String(200), unique=True)
	# NOTE : checksum for 2 files can thereotically be same.
	insert_timestamp = orm.Column(orm.DateTime, default=datetime.now())
	last_updated = orm.Column(orm.DateTime, onupdate=datetime.now())
	path = orm.Column(orm.String(1000), nullable = True)
	@staticmethod
	def add_new(filename, filepath):
		file = Files.query.filter_by(document_name = filename).first()
		if file == None:
			file = Files(document_name = filename, path=filepath)
			orm.session.add(file)
			orm.session.commit()
		return file
	@staticmethod
	def find(term):
		term = '%' + term + '%'
		res = Files.query.filter(Files.document_name.ilike(term)).all()
		return [{'id' :file.document_id, 'name' : file.document_name} for file in res]
	@staticmethod
	def get_file(id):
		file = Files.query.filter_by(document_id = id).first()
		return [{'id' : file.document_id, 'name' : file.document_name}]
	@staticmethod
	def get_list():
		files = Files.query.all()
		return [{'id' : file.document_id, 'name' : file.document_name} for file in files]

class Keywords(orm.Model):
	__tablename__ = 'keywords'
	__table_args__ = (
		orm.PrimaryKeyConstraint('keyword_id'),
	)
	keyword_id = orm.Column(orm.Integer, primary_key = True)
	keyword = orm.Column(orm.String(45), unique = True, index=True)
	@staticmethod
	def map(str, files_obj):
		instance = Keywords.query.filter_by(keyword=str).first()
		if instance == None:
			instance = Keywords()
			instance.keyword = str
			orm.session.add(instance)
			orm.session.commit()
		# print(instance.keyword_id)
		files_keywords_map = FilesKeywordsMap(document_id = files_obj.document_id, keyword_id = instance.keyword_id)
		orm.session.add(files_keywords_map)
		orm.session.commit()
	@staticmethod
	def get_files(word):
		keywords = Keywords.query.filter(Keywords.keyword.ilike(word)).all()
		keyword_ids = [keyword.keyword_id for keyword in keywords]
		maps = FilesKeywordsMap.query.filter(FilesKeywordsMap.keyword_id.in_(keyword_ids)).all()
		document_ids = [map.document_id for map in maps]
		files = Files.query.filter(Files.document_id.in_(document_ids)).all()
		return [{'id' :file.document_id, 'name' : file.document_name} for file in files]
	@staticmethod
	def get_words(word):
		word = '%' + word + '%'
		keywords = Keywords.query.filter(Keywords.keyword.ilike(word)).all()
		return [keyword.keyword for keyword in keywords]
	@staticmethod
	def get_file(id):
		return Files(path).query.filter_by(id=id).first()

class FilesKeywordsMap(orm.Model):
	__tablename__ = 'documents_keywords_map'
	__table_args__ = (
		orm.PrimaryKeyConstraint('map_id'),
	)
	map_id = orm.Column(orm.Integer, primary_key = True)
	document_id = orm.Column(orm.Integer, orm.ForeignKey('documents.document_id'))
	keyword_id = orm.Column(orm.Integer, orm.ForeignKey('keywords.keyword_id'))
	def map(self, document, keyword):
		self.document_id = document.document_id
		self.keyword_id = keyword.keyword_id
		orm.session.add(self)

# class Categories(orm.Model):
# 	__tablename__ = 'categories'
# 	__table_args__ = (
# 		orm.PrimaryKeyConstraint('category_id'),
# 	)
# 	category_id = orm.Column(orm.Integer, primary_key = True)
# 	category = orm.Column(orm.String, unique=True, index=True)
# 	category_path = orm.Column(orm.String, unique=True, index=True)
# 	def get_or_create(self, category):
# 		category_dir = os.path.join(config['BASE_DIR'], category)
# 		instance = self.query.filter_by(category = category).first()
# 		if instance is None:
# 			self.category = category
# 			orm.session.add(self)
# 			instance = self
# 		return instance
# 	@staticmethod
# 	def find(term):
# 		term = '%' + term + '%'
# 		res = Categories.query.filter(Categories.category.ilike(term)).all()
# 		return [(category.category_id, category.category) for category in res]
# 	@staticmethod
# 	def get_mapped_files(val):
# 		maps = FilesCategoriesMap.query.filter_by(category_id = val).all()
# 		print([map.document_id for map in maps])
# 		print(Files.document_id.in_([map.document_id for map in maps]))
# 		res = Files.query.filter(Files.document_id.in_([map.document_id for map in maps])).all()
# 		return [(r.document_id, r.document_name) for r in res]

# class FilesCategoriesMap(orm.Model):
# 	__tablename__ = 'documents_categories_map'
# 	__table_args__ = (
# 	orm.PrimaryKeyConstraint('map_id'),
# 	)
# 	map_id = orm.Column(orm.Integer, primary_key = True)
# 	document_id = orm.Column(orm.Integer, orm.ForeignKey('documents.document_id'))
# 	category_id = orm.Column(orm.Integer, orm.ForeignKey('categories.category_id'))
# 	def map(self, document, keyword):
# 		self.document_id = document.document_id
# 		self.category_id = keyword.category_id
# 		orm.session.add(self)
