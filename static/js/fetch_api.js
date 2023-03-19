async function predictPlateNumber() {
  //   let form_ = document.getElementById("image_form");
  let uploaded_image = document.getElementById("upload");
  let formData = new FormData();
  formData.append("my_image", uploaded_image.files[0]);
 
  let img_tag = document.getElementById("output");
  let plate_number_p_tag = document.getElementById("plate_number");
 
  fetch("/extract_plate_number", {
    method: "POST",
    body: formData,
  })
    .then(async (response) => {
      res = await response.json();
      if (res.plate_number.length == 0) {
        alert("Please try with another picture.");
      } else {
        image_source = "../images/" + res.image_name;
        img_tag.src = image_source;
        plate_number_p_tag.innerHTML = res.plate_number;
      }
      console.log("response: ", res.plate_number.length);
    })
    .catch((error) => {
      console.log("error: ", error);
      alert("Something went wrong, please try again.");
    });
}
