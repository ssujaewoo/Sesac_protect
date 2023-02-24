from flask import Flask, request, render_template, redirect, url_for, session
from tensorflow.keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps
import numpy as np
import sensor_1
import time
import subprocess
import sys
from database import *
import numpy as np
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aiot'

np.set_printoptions(suppress=True)
model = load_model("/home/pi/Downloads/webapp/keras_model.h5", compile=False)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=5)
    session.modified = True

@app.route("/", methods=['POST', 'GET']) #Main page
def index():
    
    return render_template('index.html')

@app.route("/monitor/", methods=['POST', 'GET']) #Monitoring camera
def monitor():

    return render_template('monitor.html')

@app.route("/board/<type>", methods=['POST', 'GET']) #Visual DB
def board(type = 'temp'):
    
    values = db_visual_all_pie()
    user_dict, keys = db_visual_table()
    return render_template('board.html', values=values, user_dict=user_dict, keys=keys)


@app.teardown_request
def shutdown_session(exception=None):
    pass

def camara_run():
    subprocess.run('sudo systemctl stop motion', shell=True)
    subprocess.run('fswebcam -r 300x300 --no-banner /home/pi/Downloads/webapp/image.jpg', shell=True)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open("/home/pi/Downloads/webapp/image.jpg").convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    subprocess.run('rm /home/pi/Downloads/webapp/image.jpg', shell=True)
    subprocess.run('sudo systemctl start motion', shell=True)
    return data


def predict_posture(model, image):
    prediction = model.predict(image)
    index = np.argmax(prediction)
    return index

count = 0
@app.route('/camera', methods=['POST']) #Press the start button
def camera():
    global count
    record = []
    for i in range(0, 5):
        # Camera로 Image 얻고 전처리
        data = camara_run()
        result = predict_posture(model, data)

        if (result == 0):
            record.append(0)
            # print('Good_posture')
        elif (result == 1):
            record.append(1)
            # print('Bad_posture')
        else:
            record.append(2)
            # print('empty')
        time.sleep(1.5)
    
    # print(record)

    count = count + 1
    #db upload
    good = record.count(0)
    bad = record.count(1)
    empty = record.count(2)
    db_upload(good, bad, empty, count)
    
    green_pin = 18
    yellow_pin = 23
    fan_pin = 17
    
    bad_percent = (bad / 5) * 100
    good_percent = (good / 5) * 100
    if (bad_percent >= 50.0):
        sensor_1.fan_on(fan_pin)
        time.sleep(10)
        sensor_1.fan_off(fan_pin)

    elif(good_percent >= 50.0):
        sensor_1.green_on(green_pin)
        time.sleep(10)
        sensor_1.green_off(green_pin)
        
    else:
        sensor_1.yellow_on(yellow_pin)
        time.sleep(10)
        sensor_1.yellow_off(yellow_pin)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0',9999, debug=True)