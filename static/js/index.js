
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

function predictPlateNumber(){
	const formm = document.getElementById("image_form");
	// const submitter = document.querySelector("button[value=save]");
	const formData = new FormData(formm);
	fetch("/uploadfile", {
	  method: "POST",
	  body: formData,
	})
	  .then((response) => response.json())
	  .then((result) => {
		console.log("Success:", result);
		return result;
	  })     
	  .catch((error) => {
		console.error("Error:", error);
	  });
	  reader.readAsDataURL(file);
}
  
  
