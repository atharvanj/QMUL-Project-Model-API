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
from tensorflow.keras.applications import Xception
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json
import tensorflow.keras.losses
import dropbox
import os
import h5py
from pathlib import Path

# Compatible with tensorflow backend


# losses.focal_loss_fixed
app = Flask(__name__, template_folder='Template')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
TOKEN = 'rpzSI2olZbMAAAAAAAAAAXN3DalttE8YrVVmpHr_sY39B49Ssjwh6VHHi-NEYYjj'
path = os.path.join(os.getcwd(), "Model", "complete_data_xception_model.h5")
my_file = Path(path)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def uploadFile():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('index.html')), 200
    
    if request.method == 'POST':
        # check if the post request has the file part
        dbx = dropbox.Dropbox(TOKEN)
        metadata, files = dbx.files_download('/userPhoto.jpg')
        f = files.content
        # if request.files['file'].filename == '':
        #     result = 'No file selected'
        #     return flask.redirect(url_for('viewBase64', encstring = json.dumps(result)))
        # file = request.files['file']
        #if file and allowed_file(file.filename):
        files = io.BytesIO(f)
        img = Image.open(files)
        img = img.resize((1024, 1024), PIL.Image.ANTIALIAS)
        img = np.array(img)
        img = img/255.0
        img = img[np.newaxis, ...]
        model = load_model(str(path))
        # #model = model_from_json(open("Model/complete_data_efficient_model_2.h5"))
        # # model.load_weights("Model/complete_data_efficient_weights_2.h5")
        prob = model.predict(img)
        result = prob
        # else:
        #     result = 'Unsupported file format'
        # directory = os.path.join(os.getcwd(),"Model")
        # os.chdir(directory)
        # encstring = json.dumps(str(os.listdir()) + str(os.getcwd()))
        # encstring = json.dumps(str(path) + str(my_file.is_dir()) + str(my_file.exists()))
        encstring = json.dumps(str(result))
        return flask.redirect(url_for('viewBase64', encstring = encstring))
    
    print("debug check")

@app.route('/viewBase64/', methods=['GET', 'POST'])
def viewBase64():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        x = request.args.get('encstring')
        return jsonify(x)
    

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)