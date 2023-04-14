from PIL import Image
import cv2
from flask import Flask, render_template, request, make_response
from werkzeug.exceptions import BadRequest
import logging
from utils import load_model, get_prediction


# creating flask app
app = Flask(__name__, static_folder='static')
# # create a python dictionary for your models d = {<key>: <value>, <key>: <value>, ..., <key>: <value>}
# dictOfModels = {}
# # create a list of keys to use them in the select part of the html code
# listOfKeys = []

dictOfModels, listOfKeys=load_model()

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
