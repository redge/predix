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

@app.route('/tsConsumed', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world1():
    #X = np.array([[ 1., -1.,  2.],[ 2.,  0.,  0.],[ 0.,  1., -1.]])
    #X_scaled = preprocessing.scale(X)
    
    tmp = str(red.getVar('tsConsumed'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp

@app.route('/tsCostWD', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world2():
    #X = np.array([[ 1., -1.,  2.],[ 2.,  0.,  0.],[ 0.,  1., -1.]])
    #X_scaled = preprocessing.scale(X)
    
    tmp = str(red.getVar('tsCostWD'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp
    
@app.route('/tsCostWOD', methods=["GET", "POST"])
@crossdomain(origin='*')    
def hello_world3():
    #X = np.array([[ 1., -1.,  2.],[ 2.,  0.,  0.],[ 0.,  1., -1.]])
    #X_scaled = preprocessing.scale(X)
    
    tmp = str(red.getVar('tsCostWOD'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp
    
@app.route('/tsSolarP', methods=["GET", "POST"])
@crossdomain(origin='*')    
def hello_world4():
    #X = np.array([[ 1., -1.,  2.],[ 2.,  0.,  0.],[ 0.,  1., -1.]])
    #X_scaled = preprocessing.scale(X)
    
    tmp = str(red.getVar('tsSolarP'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp
    
@app.route('/tsWindSpeed', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world5():
    #X = np.array([[ 1., -1.,  2.],[ 2.,  0.,  0.],[ 0.,  1., -1.]])
    #X_scaled = preprocessing.scale(X)
    
    tmp = str(red.getVar('tsWindSpeed'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp

@app.route('/tsHumidity', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world6():
    #X = np.array([[ 1., -1.,  2.],[ 2.,  0.,  0.],[ 0.,  1., -1.]])
    #X_scaled = preprocessing.scale(X)
    
    tmp = str(red.getVar('tsHumidity'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp

@app.route('/tsPressure', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world7():
    #X = np.array([[ 1., -1.,  2.],[ 2.,  0.,  0.],[ 0.,  1., -1.]])
    #X_scaled = preprocessing.scale(X)
    
    tmp = str(red.getVar('tsPressure'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp

@app.route('/tsTemperature', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world8():
    #X = np.array([[ 1., -1.,  2.],[ 2.,  0.,  0.],[ 0.,  1., -1.]])
    #X_scaled = preprocessing.scale(X)
    
    tmp = str(red.getVar('tsTemperature'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp

@app.route('/tsSolarLux', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world9():
    #X = np.array([[ 1., -1.,  2.],[ 2.,  0.,  0.],[ 0.,  1., -1.]])
    #X_scaled = preprocessing.scale(X)
    
    tmp = str(red.getVar('tsSolarLux'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
