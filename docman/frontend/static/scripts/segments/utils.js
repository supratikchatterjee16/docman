/*
* Copyright 2021, Tata Consultancy Services Pvt. Ltd.
* @author : Supratik Chatterjee
*
*/

function request(method, url, data = null){
	let request = {
		method : method,
		headers : {}
	};

	if(data){request.body = data;}
	return new Promise(function(resolve, reject){
		fetch(url, request).then(function(resp){
			resolve(resp);
		}).catch(function(error){
			reject(error);
		});
	});
}
