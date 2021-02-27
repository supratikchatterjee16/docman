// Development Phase
// Lib UI
// Reason : Ultimately it boils down to JS implementations
// Making use of frameworks that abstract a particular challenge creates
// peculiarities.
// Task here. Abstracting the peculiarities, but making sure people are aware
// reduces dependency on library, increases understanding.
class Properties{
	// A class that dictates the properties of elements.
	constructor(){
		this.background = null;
		this.shadow = null;
	}
}
class ComponentError extends TypeError{
	constructor(_){
		super("Component not well formed");
	}
}
class ComponentArray(){

}
class Component{// This is an atom of the bigger elements
	let element = null;
	let events = {};
	let properties = new Properties();
	let children = new ComponentArray();
	constructor(element){
		this.element = null;
		if(typeof element == "object")
			this.element = element;
		else if(typeof element == "string"){
			const div = document.getElementById("div");
			div.innerHTML = element;
			this.element = div.children[0];
			if(this.element.children.length != 0){
				for(let i = 0; i < this.element.children.length; i++){
					// This is a layer added to reduce reference complexity.
					this.children.add(this.children[i]);
				}
			}
		}
		else{
			console.error("Could not load element");
		}
	}
	setEvent(event_id, func){
		this.element.addEventListener(event_id, func);
		events[event_id] = func;
	}
	addChild(obj){
		this.children.add();
	}
}

// Layouts :
// This is a bounds calculation object
// Say you wish for a certain Layout sanity to be maintained for certain components
// For example, the login form, doesn't change no matter which screen you are on.
// This layout object, makes sure that sanity check occurs and the consistency is maintained.
class LayoutError extends ValidationError{
	constructor(message){
		super("Bounds are incorrect : "+message);
	}
}
// relative and static sizing measures

// constant measures are :
// cm, mm, in, px, pt, pc
// cm 	centimeters
// mm 	millimeters
// in 	inches (1in = 96px = 2.54cm)
// px 	pixels (1px = 1/96th of 1in) this changes per device however
// pt 	points (1pt = 1/72 of 1in)
// pc 	picas (1pc = 12 pt)

// relative measures are :
// em, ex, ch, rem, vw, vh, vmin, vmax
// Each of their relavance is to be computed.
// em 	Relative to the font-size of the element (2em means 2 times the size of the current font)
// ex 	Relative to the x-height of the current font (rarely used)
// ch 	Relative to the width of the "0" (zero)
// rem 	Relative to font-size of the root element
// vw 	Relative to 1% of the width of the viewport*
// vh 	Relative to 1% of the height of the viewport*
// vmin 	Relative to 1% of viewport's* smaller dimension
// vmax 	Relative to 1% of viewport's* larger dimension
// % 	Relative to the parent element
class Layout{
	constructor(){

	}
}
