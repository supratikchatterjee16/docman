# Document Search

### Program Files
---
1. docman
	1. base
		* __init__.py
		* error_routes.py
		* models.py
		* routes.py
		* utils.py

	2. frontend
		* static
			* images
			* scripts
			* styles
			* webfonts
		* templates
			* errors
			* base.jinja2

2. .gitignore
3.  config.json
4.  setup.py	    

### URL Routing
---
	1. '/'
		:This URL maps to the home page.
	2. '/get_file'
		:This URL maps to "get_file" function to fetch files from directory.
	3. '/upload'
		:This URL maps to the page where documents are to be uploaded.
	4. '/search'
		:This URL maps to the "search" function that searches and list out the relevant files based on the keyword(s) provided.
	5. '/fetch_result'
		:This URL maps to the "fetch_result" function that fetches files based on filename or keyword.

### Database Tables
---
	1. documents
		: Based on the keyword search, fetches and stores the document id, document name along with its timestamp and checksum into this table.
    2. keywords
		: Stores the unique keywords extracted from the document.
    3. documents_keywords_map
		: Stores the most relevant document id for a particular keyword id.
