/*
* Copyright 2021, Tata Consultancy Services Pvt. Ltd.
* @author : Supratik Chatterjee
*
*/

function show_upload_control(event){
	toggle_overlay();// From overlay.js
}

function upload_file(event){
	const files = event.target.files;
	const form = new FormData();
	show_overlay("<div>Listing...</div>");
	for(let i =0; i<files.length; i++)
		form.append('files[]', files[i], files[i].filename);
	console.log('Upload');
	show_overlay("<div>Uploading...</div>");
	request('POST', '/upload', form)
	.then((success) => {
		alert("All files added succesfully");
		hide_overlay();
		fetch_all();
	});
}
