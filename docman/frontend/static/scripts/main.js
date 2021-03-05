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
// UI manager sections
function fetch_folder_content(relative_path){
	request('POST', '/list', relative_path)
		.then((res) => res.json())
		.then((json) => {
			// console.log(relative_path, json);
			let descriptor = {
				'folder' : '<i class="fa fa-folder" style="color:rgb(155, 150, 153)" aria-hidden = "true"></i>',
				'file' : '<i class="fa fa-file" style="color:rgb(155, 150, 153)" aria-hidden = "true"></i>'
			};
			const target = document.getElementById('folders_view');
			const folder_set = document.createElement('fieldset');
			const folder_legend = document.createElement('legend');
			folder_legend.appendChild(document.createTextNode('Folders'));
			folder_set.appendChild(folder_legend);
			const file_set = document.createElement('fieldset');
			const file_legend = document.createElement('legend');
			file_legend.appendChild(document.createTextNode('Files'));
			file_set.appendChild(file_legend);
			let keys = Object.keys(json);
			let files = [];
			let hasFiles = false, hasFolder = false;
			keys.forEach((element) => {
				if(element == 'files_list'){
					json[element].forEach((filename) => {
						hasFiles = true;
						let file = document.createElement('div');
						file.title = relative_path + '/' + filename;
						file.innerHTML = descriptor['file'];
						file.classList.add('folder_element');
						file.onclick = file_click;
						file.appendChild(document.createTextNode(filename));
						file_set.appendChild(file);
					});
				}
				else{
					hasFolder = true;
					let folder = document.createElement('div');
					folder.title = relative_path + '/' + element;
					folder.innerHTML = descriptor['folder'];
					folder.classList.add('folder_element');
					folder.onclick = folder_click;
					folder.appendChild(document.createTextNode(element));
					folder_set.appendChild(folder);
				}
			});
			target.innerHTML = '';
			if(hasFolder)target.appendChild(folder_set);
			if(hasFiles)target.appendChild(file_set);
		});
}
function folder_click(event){
	const target = event.currentTarget;
	target.parentNode.classList.toggle('name-only');
	fetch_folder_content(target.title);
}
function get_file(filepath){
	request('POST', '/get_file', filepath)
		.then((res) => res.blob())
		.then((blob) => {
			const file = URL.createObjectURL(blob);
			window.location.assign(file);
		});
}
function file_click(event){
	const target = event.currentTarget;
	get_file(target.title);
}
function generate_folder(name, dictionary, prefix = ''){
	let directory_descriptor = {
		'folder' : '<i class="fas fa-angle-down"></i><i class="fa fa-folder"  aria-hidden = "true"></i>',
		'file' : '<i class="fa fa-file" aria-hidden = "true"></i>'
	};
	let directory_container = document.createElement("directory");
	// Create the title node
	let dir_name = document.createElement('label');
	dir_name.innerHTML = directory_descriptor['folder'];
	dir_name.appendChild(document.createTextNode(name));
	// console.log(prefix);
	dir_name.title = prefix;// console.log(prefix);
	dir_name.addEventListener('click', folder_click, {capture : false, useCapture :false}) ;
	directory_container.appendChild(dir_name);

	// iterate over keys to create new tags
	let keys = Object.keys(dictionary);
	let files = [];
	keys.forEach((element) => {
		if(element == 'files_list'){
			// Populate files in this section
			dictionary[element].forEach((filename) => {
				let file = document.createElement('file');
				file.title = prefix + '/' +filename;
				file.innerHTML = directory_descriptor['file'];
				file.onclick = file_click;
				file.appendChild(document.createTextNode(filename));
				files.push(file);
			});
		}
		else{
			directory_container.appendChild(generate_folder(element, dictionary[element], prefix + '/' + element));
		}
	});
	files.forEach((file) => {directory_container.appendChild(file);});
	directory_container.classList.toggle("name-only");
	return directory_container;
}
var original_files_list = [];
function get_files_list_into(id){
	console.info("Refreshing directory structure");
	request('GET', '/list').then((response) => {
		response.json().then((data) => {
			document.getElementById(id).innerHTML = '';
			const folder = generate_folder('/', data);
			folder.classList.toggle('name-only');
			document.getElementById(id).appendChild(folder);
		});
	}).catch((error) => {console.error(error);});
	original_files_list = document.getElementsByTagName('file');
}
function init(){
	get_files_list_into('tree');
	fetch_folder_content('');
}
// Search Functions
function filter_files(event){
	const target = event.currentTarget;
	let filter_text = target.value;

	// extract files to be hidden below
	let files_to_hide = Array.from(original_files_list).filter((element) => {
		let text = element.childNodes[1].textContent;
		element.classList.remove('collapse');
		return !text.toLowerCase().includes(filter_text.toLowerCase());
	});

	// hide it
	files_to_hide.forEach((element) => {element.classList.add('collapse');});
}
function global_search(event){

}
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
	.then((success) => success.json())
	.then((json) => {console.log(json);});
}

function confirm_file(){
	const tagged_keywords = document.getElementById('tagged_keywords').value;
	const tagged_category = document.getElementById('tagged_category').value;
	const form = new FormData();
	form.append('filename', document.getElementById('staged_filename').innerText);
	form.append('keywords', tagged_keywords);
	form.append('category', tagged_category);
	console.log(form);
	request('POST', '/add_file', form)
	.then((success) => {
		document.getElementById("overlay").hidden = true;
		get_files_list_into('tree');
	});
}
function createFieldSet(title){
	const field = document.createElement('fieldset');
	const legend = document.createElement('legend');
	legend.appendChild(document.createTextNode(title));
	field.appendChild(legend);
	return field;
}
function select_search_item(event){
	const target = event.target;
	const form = new FormData();
	form.append('type', target.type);
	form.append('id', target.data_id);
	request('POST', '/fetch_result', form)
	.then((success) => success.json())
	.then((json) => {
		console.log(json);
	});
	hide_search();
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
		var categories = null, files = null, keywords = null;
		if(json.categories.length > 0){
			categories = createFieldSet('Categories');
			json.categories.forEach((element) => {
				const div = document.createElement('div');
				div.classList.add('dropdown-item');
				div.type = 'category';
				div.data_id = element[0];
				div.innerHTML = element[1].toString();
				div.addEventListener('click', select_search_item);
				categories.appendChild(div);
			});
		}
		if(json.files.length > 0){
			files = createFieldSet('Files');
			json.files.forEach((element) => {
				const div = document.createElement('div');
				div.classList.add('dropdown-item');
				div.type = 'file';
				div.data_id = element[0];
				div.path = element[2];
				const text = document.createTextNode(element[1]);
				text.addEventListener('click', select_search_item);
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
				div.data_id = element[0];
				div.innerHTML = element[1];
				div.addEventListener('click', select_search_item);
				keywords.appendChild(div);
			});
		}
		// Build main view
		const target = document.getElementById('search_results');
		target.innerHTML = '';
		if(categories)target.appendChild(categories);
		if(files)target.appendChild(files);
		if(keywords)target.appendChild(keywords);
		if(!categories && !files && !keywords)
			target.innerHTML = '<div style="text-align:center;width:100%;">Nothing Found</div>';

	});
	document.getElementById('search_results').classList.add('show');
}
function hide_search(){document.getElementById('search_results').classList.remove('show');}

// function upload_file(event){
	// 	const files = event.target.files;
	// 	const random_path = event.target.value;
	// 	console.log(random_path);
	// 	const filename = random_path.substring(random_path.lastIndexOf('\\') + 1);
	// 	if(files && files[0]){
		// 		const form = new FormData();
		// 		form.append('new_file', files[0]);
		// 		// form.append('filename', filename);
		// 		request('POST', '/upload', form)
		// 		.then((success) => success.json())
		// 		.then((json) => {// TODO Add support for categories
			// 			const overlay = document.getElementById("overlay");
			// 			overlay.hidden = false;
			// 			overlay.innerHTML = "<div class=\"container-fluid\">\
			// 				<div class=\"row\" style=\"height:25vh\"></div>\
			// 				<div class=\"row\" style=\"height:50vh;\">\
			// 					<div class=\"col-sm-3\"></div>\
			// 					<div class=\"col-sm\" style=\"background:white;box-shadow : 0px 0px 20px #888888\">\
			// 						<div class=\"row\" style=\"height:100%;\">\
			// 							<div class=\"col-sm-8\" style=\"border-right:1pt solid rgba(150, 150, 150, 0.2)\">\
			// 								<div class=\"row\" style=\"height:50%\">\
			// 									<fieldset>\
			// 										<legend>Manage File</legend>\
			// 										<i class=\"fa fa-file\" style=\"color:rgb(155, 150, 153); font-size : 24pt;text-align : center\" aria-hidden = \"true\"></i><div id=\"staged_filename\"></div>\
			// 									</fieldset>\
			// 								</div>\
			// 								<div class=\"row\">\
			// 									<fieldset>\
			// 										<legend>Suggested Keywords</legend>\
			// 										<div id=\"suggested_keywords\"></div>\
			// 									</fieldset>\
			// 								</div>\
			// 							</div>\
			// 							<div class=\"col-sm-4\">\
			// 								<fieldset>\
			// 									<legend>Categories</legend>\
			// 									<div id=\"suggested_categories\"></div>\
			// 								</fieldset>\
			// 							</div>\
			// 						</div>\
			// 						<div class=\"row p-2 bg-white border\">\
			// 							<input type=\"text\" id=\"tagged_keywords\" placeholder=\"Relevant keywords(sperated by semi-colons)\"/>\
			// 							<input type=\"text\" id=\"tagged_category\" placeholder=\"Category(Single name)\"/>\
			// 							<button onclick=\"confirm_file()\">Finish</button>\
			// 						</div>\
			// 					</div>\
			// 					<div class=\"col-sm-3\"></div>\
			// 				</div>\
			// 				<div class=\"row\" style=\"height:25vh\"></div>\
			// 			</div>";
			// 			document.getElementById("staged_filename").appendChild(document.createTextNode(json.staged_filename));
			// 			const keywords = Object.keys(json.keywords);
			// 			const keywords_section = document.getElementById("suggested_keywords");
			// 			keywords_section.innerHTML = "";
			// 			keywords.forEach((element) => {
				// 				const keyword = document.createElement("keyword");
				// 				keyword.appendChild(document.createTextNode(element));
				// 				keywords_section.appendChild(keyword);
				// 			});
				// 		});
				// 	}
				// }
