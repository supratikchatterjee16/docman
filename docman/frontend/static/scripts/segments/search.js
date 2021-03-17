/*
* Copyright 2021, Tata Consultancy Services Pvt. Ltd.
* @author : Supratik Chatterjee
*
*/

function createFieldSet(title){
	const field = document.createElement('fieldset');
	const legend = document.createElement('legend');
	legend.appendChild(document.createTextNode(title));
	field.appendChild(legend);
	return field;
}
function populateFoldersView(json){
	hide_search();
	const target = document.getElementById('folders_view');
	const field = createFieldSet("Files");
	json.value.forEach((val) => {
		const file = document.createElement('div');
		file.classList.add('folder-element');
		const i = document.createElement('i');
		i.classList.add('fas', 'fa-file');
		file.data_id = val.id
		file.appendChild(i);
		file.appendChild(document.createTextNode(val.name));
		file.addEventListener('click', get_file);
		field.appendChild(file);
	});
	target.innerHTML = "";
	target.appendChild(field);
}
function select_search_item(event){
	const target = event.target;
	const form = new FormData();
	form.append('type', target.type);
	form.append('id', target.data_id);
	request('POST', '/fetch_result', form)
	.then((success) => success.json())
	.then((json) => {populateFoldersView(json);});
}

function search(event){
	const val = event.target.value;
	if(val.length < 1){
		hide_search();
		return;
	}
	const form = new FormData();
	form.append('search', val);
	document.getElementById('search_results').innerHTML = '<div style="text-align:center;width:100%;">Loading...</div>';
	request('POST', '/search', form)
	.then((success) => success.json())
	.then((json) => {
		var files = null, keywords = null;
		if(json.files.length > 0){
			files = createFieldSet('Files');
			json.files.forEach((element) => {
				const div = document.createElement('div');
				div.classList.add('dropdown-item');
				div.type = 'file';
				div.data_id = element['id'];
				const text = document.createTextNode(element['name']);
				// text.addEventListener('click', select_search_item);
				div.appendChild(text);
				div.addEventListener('click', select_search_item);
				files.appendChild(div);
			});
		}
		if(json.keywords.length > 0){
			keywords = createFieldSet('Keywords');
			json.keywords.forEach((element) => {
				const div = document.createElement('div');
				div.classList.add('dropdown-item');
				div.type = 'keyword';
				div.data_id = element;
				div.innerHTML = element;
				div.addEventListener('click', select_search_item);
				keywords.appendChild(div);
			});
		}
		// Build main view
		const target = document.getElementById('search_results');
		target.innerHTML = '';
		if(files)target.appendChild(files);
		if(keywords)target.appendChild(keywords);
		if(!files && !keywords)
			target.innerHTML = '<div style="text-align:center;width:100%;">Nothing Found</div>';
	});
	document.getElementById('search_results').classList.add('show');
}
function hide_search(){document.getElementById('search_results').classList.remove('show');}
