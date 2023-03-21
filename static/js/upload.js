// // drag && drop upload img
// const dropbox = document.getElementById("upload_zone");
// const preview = document.getElementById("preview");

// function handleFileSelect(e) {
//   e.stopPropagation();
//   e.preventDefault();
//   const fileUploader = document.getElementById("fileUploader");
//   fileUploader.click();
// }

// const click = (e) => handleFileSelect(e);

// // prevent the default method working
// function dragenter(e) {
//   // add the styling to div
//   dropbox.classList.add("upload_zone_enter");
//   e.stopPropagation();
//   e.preventDefault();
// }

// const dragleave = () => dropbox.classList.remove("upload_zone_enter");

// // prevent the default method working
// function dragover(e) {
//   e.stopPropagation();
//   e.preventDefault();
// }
// async function handleFiles(files) {
//   for (var i = 0; i < files.length; i++) {
//     const file = files[i];
//     const imageType = /image.*/;

//     if (!file.type.match(imageType)) {
//       alert("invalid image type!!!");
//       continue;
//     }

//     //deal with the img one by one
//     await predict_image(file);
//   }
// }

// function drop(e) {
//   e.stopPropagation();
//   e.preventDefault();

//   const dt = e.dataTransfer;
//   const files = dt.files;

//   handleFiles(files);
//   dropbox.classList.remove("upload_zone_enter");
// }

// dropbox.addEventListener("DOMContentLoaded", "click", click, false);
// dropbox.addEventListener("DOMContentLoaded", "dragenter", dragenter, false);
// dropbox.addEventListener("DOMContentLoaded", "dragleave", dragleave, false);
// dropbox.addEventListener("DOMContentLoaded", "dragover", dragover, false);
// dropbox.addEventListener("DOMContentLoaded", "drop", drop, false);
