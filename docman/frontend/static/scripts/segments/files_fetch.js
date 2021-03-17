/*
* Copyright 2021, Tata Consultancy Services Pvt. Ltd.
* @author : Supratik Chatterjee
*
*/

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
