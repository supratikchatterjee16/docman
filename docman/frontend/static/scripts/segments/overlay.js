/*
* Copyright 2021, Tata Consultancy Services Pvt. Ltd.
* @author : Supratik Chatterjee
*
*/

function show_overlay(content = '<input type = \"file\" placeholder=\"Upload a file\" onchange=\"upload_file(event)\" multiple/>'){
	const overlay = document.getElementById('overlay');
	const overlay_parser = new DOMParser();
	const main_template = "<div class=\"container-flexible\">\
		<div class=\"row\" style=\"height:45vh;\"></div>\
		<div class=\"row\" style=\"height:10vh; text-align : center;\">\
			<div class=\"col-sm-4\">\
			</div>\
			<div class=\"col-sm align-middle\">\
				<fieldset class=\"align-middle\" style=\"text-align:center;\">\
				</fieldset>\
			</div>\
			<div class=\"col-sm-4\">\
			</div>\
		</div>\
		<div class=\"row\" style=\"height:45vh;\"></div>\
	</div>";
	const overlay_content = overlay_parser.parseFromString(main_template, 'text/html');
	overlay_content.getElementsByTagName('fieldset')[0].innerHTML = content;
	overlay.innerHTML = '';
	overlay.appendChild(overlay_content.getRootNode().body.firstChild);
	overlay.hidden = false;
}
function hide_overlay(){document.getElementById('overlay').hidden = true;}
function toggle_overlay(content=null){
	if(document.getElementById('overlay').hidden == true){
		(content)? show_overlay(content) : show_overlay();
	}
	else{hide_overlay();}
}
