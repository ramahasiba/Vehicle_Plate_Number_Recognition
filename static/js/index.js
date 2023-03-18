var loadFile = function (event) {
  var image = document.getElementById("output");
  image.src = URL.createObjectURL(event.target.files[0]);
  document.getElementById("buttonGroup").style.display = "flex";
};

var handleDragOver = function (event) {
  event.preventDefault();
  event.dataTransfer.dropEffect = "copy";
  document.getElementById("dropZone").classList.add("highlight");
};

var handleDragLeave = function (event) {
  event.preventDefault();
  document.getElementById("dropZone").classList.remove("highlight");
};

var handleDrop = function (event) {
  event.preventDefault();
  document.getElementById("dropZone").classList.remove("highlight");
  var file = event.dataTransfer.files[0];
  var reader = new FileReader();
  reader.onload = function (event) {
    var image = document.getElementById("output");
    image.src = event.target.result;
    document.getElementById("buttonGroup").style.display = "flex";
  };
  reader.readAsDataURL(file);
};
    
function predictPlateNumber() {
  let form_ = document.getElementById("image_form");
  let uploaded_image = document.getElementById("upload");
  let formData = new FormData(form_);
  formData.append("_image", uploaded_image.files[0]);

  fetch("/extract_plate_number", {
    method: "POST",
    body: formData,
  }).then((response) => response.json())
    .then((result) => { 
      console.log("Success:", result);
      return result;
    })
    .catch((error) => {
		alert('Something went wrong, please try again.')
      console.error("Error:", error);
    });
}
 