function predictPlateNumber() {
  //   let form_ = document.getElementById("image_form");
  let uploaded_image = document.getElementById("upload");
  let formData = new FormData();
  formData.append("my_image", uploaded_image.files[0]);
  console.log(uploaded_image.files);

  fetch("/extract_plate_number", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((result) => {
      console.log("Success:", result);
      return result;
    })
    .catch((error) => {
      alert("Something went wrong, please try again.");
      console.error("Error:", error);
    });
}
