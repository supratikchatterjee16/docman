/*
* Copyright 2021, Tata Consultancy Services Pvt. Ltd.
* @author : Supratik Chatterjee
*
*/

// Initial script
function fetch_all(){
	request('GET', '/fetch_result')
	.then((success) => success.json())
	.then((json) => {populateFoldersView(json);});
}
function init(){
	fetch_all();
}
