// global elements for describing elements
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

function fetch_folder_content(relative_path){
	request('POST', '/list', relative_path)
		.then((res) => res.json())
		.then((json) => {
			console.log(relative_path, json);
		});
}

function folder_click(event){
	const target = event.currentTarget;
	// console.debug('folder',target);
	// console.debug(target.title, ', ', target.prefix);
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
function filter_files(event){
	const target = event.currentTarget;
	let filter_text = target.value;

	// extract files to be hidden below
	let files_to_hide = Array.from(original_files_list).filter((element) => {
		let text = element.childNodes[1].textContent;
		element.classList.remove('collapse');
		return !text.includes(filter_text);
	});

	// hide it
	files_to_hide.forEach((element) => {element.classList.add('collapse');});
}
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

function directory_styles_init(){
	let style = document.createElement("style");
	style.innerHTML = "directory{display : block;margin-left : 10pt;margin-top : 5pt;border-left : 1pt solid rgba(50, 50, 50, 0.5);}directory.name-only file{height : 0pt;display : none;}/* animate directory and file later*/directory.name-only directory{height : 0pt;display : none;}directory.name-only .fa-angle-down{transform : rotate(-90deg);}file{display:block;margin-left : 10pt;transition : all 0.2s ease;}directory .fa, .fas{margin-right : 4pt;margin-left : 4pt;transition : all 0.2s ease;}";
	document.head.appendChild(style);
}
directory_styles_init();
