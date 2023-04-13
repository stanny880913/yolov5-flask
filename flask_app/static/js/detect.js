// predict upload img
async function predict_image(file) {
  const do_predict = function () {
    return new Promise((resolve, reject) => {
      //creat formdata
      var formData = new FormData();

      formData.append("file", file);
      formData.append(
        "model_choice",
        document.getElementById("model_choice").value
      );
      // Create a new XMLHttpRequest object
      const xhr = new XMLHttpRequest();
      // Specify the HTTP method and endpoint
      xhr.open("POST", "/");

      xhr.responseType = "blob";
      xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          const imageBlob = xhr.response;
          const imageURL = URL.createObjectURL(imageBlob);
          const img = new Image();
          const imageContainer = document.createElement("div");
          const deleteButton = document.createElement("button");

          //set result_img css
          img.style.margin = "5px";
          img.style.width = "300px";
          img.style.height = "200px";
          img.style.cursor = "zoom-in";
          img.style.transition = "transform 0.5s";

          imageContainer.className = "image-container";

          deleteButton.textContent = "X";
          deleteButton.className = "delete-button";
          deleteButton.onclick = () => {
            imageContainer.remove();
          };

          //set img onload event
          img.onload = function () {
            imageContainer.appendChild(img);
            imageContainer.appendChild(deleteButton);
            preview.appendChild(imageContainer);
            resolve();
          };

          img.src = imageURL;

          img.onclick = () => {
            document.getElementById("myModal").style.display = "block";
            console.log("click");
            document.getElementById("img_list").src = imageURL;
          };
        }
      };

      // send formdata
      xhr.send(formData);
    });
  };

  //send img and wait for the predict result
  await do_predict();
}
