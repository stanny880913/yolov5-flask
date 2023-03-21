// predict upload img 
async function predict_image(file) {
    const do_predict = function () {
        return new Promise((resolve, reject) => {
            //creat formdata
            var formData = new FormData();

            formData.append('file', file);
            formData.append('model_choice', document.getElementById('model_choice').value);
            // Create a new XMLHttpRequest object
            const xhr = new XMLHttpRequest();
            // Specify the HTTP method and endpoint
            xhr.open('POST', '/');

            xhr.responseType = 'blob';

            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                    const imageBlob = xhr.response;
                    const imageURL = URL.createObjectURL(imageBlob);
                    const img = new Image();
                    //set result_img css
                    img.style.margin = '5px';
                    img.style.width = '300px';
                    img.style.height = '200px';
                    img.style.cursor = 'zoom-in';
                    img.style.transition = 'transform 0.5s';
                    //set img iniload event
                    img.onload = function () {
                        preview.appendChild(img);
                        // URL.revokeObjectURL(imageURL);
                        resolve();
                    };
                    //set img zoom
                    img.onclick = function () {
                        img.classList.toggle('zoomed');
                    };
                    img.src = imageURL;

                    img.onclick = () => {
                        document.getElementById('myModal').style.display = 'block';
                        console.log("click");
                        document.getElementById('img01').src = imageURL;
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