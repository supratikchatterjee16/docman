/** Copyright 2021, Tata Consultancy Services Pvt. Ltd.
* @author : Supratik Chatterjee
*
*/
// Global utilities
function request(method, url, data = null){
	let request = {
		method : method,
		// mode : 'cors',
		// redirect : 'manual',
		// credentials : 'include',
		// referrerPolicy : 'no-referrer',
		headers : {}
	};
	// console.log(url);

	if(data){
		request.body = data;
	}
	return new Promise(function(resolve, reject){
		fetch(url, request).then(function(resp){
			resolve(resp);
		}).catch(function(error){
			reject(error);
		});
	});
}
// Add styles for UI
function directory_styles_init(){
	let style = document.createElement("style");
	style.innerHTML = "directory{display : block;margin-left : 10pt;margin-top : 5pt;border-left : 1pt solid rgba(50, 50, 50, 0.5);}directory.name-only file{height : 0pt;display : none;}/* animate directory and file later*/directory.name-only directory{height : 0pt;display : none;}directory.name-only .fa-angle-down{transform : rotate(-90deg);}file{display:block;margin-left : 10pt;transition : all 0.2s ease;}directory .fa, .fas{margin-right : 4pt;margin-left : 4pt;transition : all 0.2s ease;}";
	document.head.appendChild(style);
}
directory_styles_init();

// Upload
function show_upload_control(event){
	const overlay = document.getElementById('overlay');
	overlay.innerHTML = "<div class=\"container-flexible\">\
		<div class=\"row\" style=\"height:20vh;\"></div>\
		<div class=\"row\" style=\"height:60vh; text-align : center;\">\
			<div class=\"col-sm-4\">\
			</div>\
			<div class=\"col-sm\">\
				<fieldset style=\"text-align:center;\">\
					<input type = \"file\" placeholder=\"Upload a file\"\ onchange=\"upload_file(event)\" multiple/>\
				</fieldset>\
			</div>\
			<div class=\"col-sm-4\">\
			</div>\
		</div>\
		<div class=\"row\" style=\"height:20vh;\"></div>\
	</div>";
	overlay.hidden = !overlay.hidden;
}

function upload_file(event){
	const files = event.target.files;
	const form = new FormData();
	for(let i =0; i<files.length; i++)
		form.append('files[]', files[i], files[i].filename);
	request('POST', '/upload', form)
	.then((success) => {
		overlay.hidden = true;
	});
}

// Search
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
	if(val.length < 1) return null;
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

// File fetch

function get_file(event){
	const form = new FormData();
	const target = event.target;
	form.append('id', target.data_id);
	request('POST', '/get_file', form)
	.then(response => {
		content_desc = response.headers.get('Content-Disposition');
		const filename = content_desc.substring(22, content_desc.length-1);
		response.blob().then(blob => {
			var url = window.URL.createObjectURL(blob);
			var a = document.createElement('a');
			a.href = url;
			a.download = filename;
			document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
			a.click();
			a.remove();  //afterwards we remove the element again
		});
	});
}

// Initial script
function fetch_all(){
	request('GET', '/fetch_result')
	.then((success) => success.json())
	.then((json) => {populateFoldersView(json);});
}
function init(){
	fetch_all();
}
