import io
from PIL import Image
import torch
import os
import logging
from app import app

# app = Flask(__name__, static_folder='static')
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
    return dictOfModels, listOfKeys 


def get_prediction(img_bytes, model):
    img = Image.open(io.BytesIO(img_bytes))
    # inference
    results = model(img, size=640)
    return results


