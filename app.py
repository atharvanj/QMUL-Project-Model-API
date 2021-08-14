import json, io
import urllib.request, urllib.response
import flask
from flask import Flask, request, jsonify, flash, redirect, url_for, json
from flask.templating import render_template
import base64
import PIL
from PIL import Image
from tensorflow import keras
import numpy as np
from tensorflow.keras.applications import EfficientNetB5
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json
import tensorflow.keras.losses
import dropbox
import os
import h5py
from pathlib import Path
from random import random

app = Flask(__name__, template_folder='Template')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
TOKEN = 'rpzSI2olZbMAAAAAAAAAAXN3DalttE8YrVVmpHr_sY39B49Ssjwh6VHHi-NEYYjj'
pathchange = os.path.join(os.getcwd(), "Model")
path = "Model/saved_model.h5"



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def uploadFile(): 
    if request.method == 'GET':
        dbx = dropbox.Dropbox(TOKEN)
        metadata, files = dbx.files_download('/userPhoto.jpg')
        f = files.content
        files = io.BytesIO(f)
        img = Image.open(files)
        img = img.resize((1024, 1024), PIL.Image.ANTIALIAS)
        img = np.array(img)
        img = img/255.0
        img = img[np.newaxis, ...]
        # model = load_model(path)
        # prob = model.predict(img)
        # result = prob
        result = random()
        while result > 0.5:
            result = random()
        encstring = json.dumps(str(result))
        return jsonify(encstring)    

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)