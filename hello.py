from flask import Flask, Response
import os
from scipy import special, optimize
import pandas as pd

from sklearn import preprocessing
import numpy as np
from analyze import get_data
from r import RedisManager
from resp_decoration import crossdomain


red = RedisManager('redis_ryan')
get_data()

app = Flask(__name__)

port = int(os.getenv("PORT", 64781))

@app.route('/', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world():
    #X = np.array([[ 1., -1.,  2.],[ 2.,  0.,  0.],[ 0.,  1., -1.]])
    #X_scaled = preprocessing.scale(X)
    
    tmp = str(red.getVar('tsConsumed')) + str(red.getVar('tsCostWD')) + str(red.getVar('tsCostWOD')) + str(red.getVar('tsSolarP')) + str(red.getVar('tsSolarLux')) + str(red.getVar('tsTemperature')) + str(red.getVar('tsPressure')) + str(red.getVar('tsHumidity')) + str(red.getVar('tsWindSpeed'))
    
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
