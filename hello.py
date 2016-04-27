from flask import Flask, Response
import os
from scipy import special, optimize
import pandas as pd

from sklearn import preprocessing
import numpy as np
from analyze import get_data
from r import RedisManager

red = RedisManager('redis_ryan')
get_data()

app = Flask(__name__)

port = int(os.getenv("PORT", 64781))

@app.route('/')
def hello_world():
    #X = np.array([[ 1., -1.,  2.],[ 2.,  0.,  0.],[ 0.,  1., -1.]])
    #X_scaled = preprocessing.scale(X)
    
    tmp = str(red.getVar('tsConsumed'))
    tmp = str(red.getVar('tsCostWD'))
    tmp = str(red.getVar('tsCostWOD'))
    tmp = str(red.getVar('tsSolarP'))
    tmp = str(red.getVar('tsSolarLux'))
    tmp = str(red.getVar('tsTemperature'))
    tmp = str(red.getVar('tsPressure'))
    tmp = str(red.getVar('tsHumidity'))
    tmp = str(red.getVar('tsWindSpeed'))
    
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
