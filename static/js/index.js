
var loadFile = function(event) {
	var image = document.getElementById('output');
	image.src = URL.createObjectURL(event.target.files[0]);
	document.getElementById('buttonGroup').style.display = 'flex';
};
var handleDragOver = function(event) {
	event.preventDefault();
	event.dataTransfer.dropEffect = 'copy';
	document.getElementById('dropZone').classList.add('highlight');
};
var handleDragLeave = function(event) {
	event.preventDefault();
	document.getElementById('dropZone').classList.remove('highlight');
};
var handleDrop = function(event) {
	event.preventDefault();
	document.getElementById('dropZone').classList.remove('highlight');
	var file = event.dataTransfer.files[0];
	var reader = new FileReader();
	reader.onload = function(event) {
		var image = document.getElementById('output');
		image.src = event.target.result;
		document.getElementById('buttonGroup').style.display = 'flex';
	};
	reader.readAsDataURL(file);
};
var predictPlateNumber = function() {
	// TODO: implement plate number prediction logic
	alert('Plate number prediction is not implemented yet!');
};

function displayImage(byteArray, elementId) {
	// Convert byte array to base64-encoded string
	var base64String = btoa(String.fromCharCode.apply(null, byteArray));
	
	// Create image tag with base64-encoded string as src attribute
	var imgTag = '<img src="data:image/jpeg;base64,' + base64String + '"/>';
	
	// Set innerHTML of specified HTML element to the image tag
	document.getElementById(elementId).innerHTML = imgTag;
  }
