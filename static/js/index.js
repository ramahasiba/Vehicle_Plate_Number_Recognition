
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

// async function submit(){
// 	const image = document.getElementById('image');
// 	const res = await fetch("/extract_number");

// 	if (res.ok){
// 		const data = await res.json();
// 		const extractNumber = data.extractNumber;

// 		// change the src of the img
// 		image.src = data.imgsrc; 
// 		// display the extracted number 
// 		console.log("Extracted Number:",extractNumber);
// 		// return the status of the operation
// 		return {"Success": true, "Status": res.status};
// 	}
// 	else{
// 		console.error("Status:", res.status)
// 		return {"Success": false, "Status":res.status};
// 	}
// }

async function get_num() {
	let base64String = "";
	var file = document.querySelector("input[type=file]")["files"][0];
  
	var reader = new FileReader();
  
	reader.onload = function () {
	  base64String = reader.result.replace("data:", "").replace(/^.+,/, "");
  
	  imageBase64Stringsep = base64String;
	  console.log(base64String);
  
	  // Convert the base64 string to a byte array
	  var byteArray = new Uint8Array(atob(base64String).split("").map(function (c) { return c.charCodeAt(0); }));
  
	  // Convert the byte array to an image
	  var image = byteArrayToImage(byteArray);
  
	  // Append the image to the document body
	  document.body.appendChild(image);
  
	  // alert(imageBase64Stringsep);
	};
  
	const formm = document.getElementById("forr");
	// const submitter = document.querySelector("button[value=save]");
	const formData = new FormData(formm);
  
	fetch("/uploadfile", {
	  method: "POST",
	  body: formData,
	})
	  .then((response) => response.json())
	  .then((result) => {
		console.log("Success:", result);
	  })
	  .catch((error) => {
		console.error("Error:", error);
	  });
	  reader.readAsDataURL(file);
  }
  
  
