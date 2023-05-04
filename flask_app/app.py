import sys
import io
from PIL import Image
import cv2
import torch
from flask import Flask, render_template, request, make_response
from werkzeug.exceptions import BadRequest
import os
import logging


# creating flask app
app = Flask(__name__, static_folder='static')
# create a python dictionary for your models d = {<key>: <value>, <key>: <value>, ..., <key>: <value>}
dictOfModels = {}
# create a list of keys to use them in the select part of the html code
listOfKeys = []

# inference fonction


def load_model():
    models_directory = '/usr/src/flask_app/weights'
    # if len(sys.argv) > 1:
    #     models_directory = sys.argv[1]
    app.logger.debug(
        f'Detecting for yolov5 models under {models_directory}...')
    for r, d, f in os.walk(models_directory):
        for file in f:
            if ".pt" in file:
                # example: file = "model1.pt"
                # the path of each model: os.path.join(r, file)
                model_name = os.path.splitext(file)[0]
                model_path = os.path.join(r, file)
                app.logger.debug(
                    f'Loading model {model_path} with path {model_path}...')
                dictOfModels[model_name] = torch.hub.load(
                    'ultralytics/yolov5', 'custom', path=model_path)
                # you would obtain: dictOfModels = {"model1" : model1 , etc}
        for key in dictOfModels:
            listOfKeys.append(key)  # put all the keys in the listOfKeys


def get_prediction(img_bytes, model):
    img = Image.open(io.BytesIO(img_bytes))
    # inference
    results = model(img, size=640)
    return results


# get method
@app.route('/', methods=['GET'])
def get():
    # in the select we will have each key of the list in option
    return render_template("index.html", len=len(listOfKeys), listOfKeys=listOfKeys)


# Predict image
@app.route('/', methods=['POST'])
def predict():
    file = extract_img(request)
    img_bytes = file.read()

    # choice of the model
    results = get_prediction(
        img_bytes, dictOfModels[request.form.get("model_choice")])
    print(f'User selected model is: {request.form.get("model_choice")}')
    print("Result = ", results)

    # updates results.imgs with boxes and labels
    results.render()

    # encoding the resulting image and return it
    for img in results.ims:
        RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_arr = cv2.imencode('.jpg', RGB_img)[1]
        response = make_response(im_arr.tobytes())
    print("response", response.headers['Content-Type'])
    return response


def extract_img(request):
    # checking if image uploaded is valid
    if 'file' not in request.files:
        raise BadRequest("Missing file parameter!")

    file = request.files['file']

    if file.filename == '':
        raise BadRequest("Given file is invalid")

    print("file", file)
    return file


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

load_model() 
# if __name__ == '__main__':
    # starting app
    # app.run(debug=True, host='0.0.0.0')
