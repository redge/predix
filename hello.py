from flask import Flask, Response
import os
from analyze import get_data
from r import RedisManager
from resp_decoration import crossdomain
import json


red = RedisManager('redis_ryan')
get_data()

app = Flask(__name__)

port = int(os.getenv("PORT", 64781))

@app.route('/tsConsumed', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world1():
    
    tmp = json.dumps(red.getVar('tsConsumed'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp

@app.route('/tsCostWD', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world2():
    
    tmp = json.dumps(red.getVar('tsCostWD'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp
    
@app.route('/tsCostWOD', methods=["GET", "POST"])
@crossdomain(origin='*')    
def hello_world3():
    
    tmp = json.dumps(red.getVar('tsCostWOD'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp
    
@app.route('/tsSolarP', methods=["GET", "POST"])
@crossdomain(origin='*')    
def hello_world4():
    
    tmp = json.dumps(red.getVar('tsSolarP'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp
    
@app.route('/tsWindSpeed', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world5():
    
    tmp = json.dumps(red.getVar('tsWindSpeed'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp

@app.route('/tsHumidity', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world6():
    
    tmp = json.dumps(red.getVar('tsHumidity'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp

@app.route('/tsPressure', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world7():
    
    tmp = json.dumps(red.getVar('tsPressure'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp

@app.route('/tsTemperature', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world8():
    
    tmp = json.dumps(red.getVar('tsTemperature'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp

@app.route('/tsSolarLux', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world9():
    
    tmp = json.dumps(red.getVar('tsSolarLux'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp

@app.route('/tsFromExcel', methods=["GET", "POST"])
@crossdomain(origin='*')
def hello_world10():
    
    tmp = json.dumps(red.getVar('tsConsumed'))
    resp = Response(response=tmp, status=200, mimetype="application/json")
    return resp    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
