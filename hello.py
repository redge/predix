from bottle import Bottle, run
import os
from bottle import request, response
from bottle import post, get, put, delete
import re, json

from r import RedisManager
#from api import kws


port = int(os.getenv('PORT', 64781))

app = Bottle()

# change this to your redis_service_name
# NOTE: RedisManager is checking for redis-2 only. Modify if needed redis-1
red = RedisManager('redis_ryan')

@app.route('/hello')
def hello():
    vcap = os.getenv('VCAP_SERVICES')
    return "Hello World!" + str(vcap)

@app.route('/test_redis')
def test_redis():
    red.setVar('test_var', 'ok')
    result = red.getVar('test_var')
    return result


_kws = set()

@app.post('/kws')
def creation_handler():
    try:
        # parse input data
        try:
            data = request.json()
        except:
            raise ValueError

        if data is None:
            raise ValueError


        # check for existence
        if kw in _kws:
            raise KeyError

    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return
    
    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return

    # add name
    _names.add(name)
    
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'name': name})

@app.get('/kws')
def listing_handler():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps({'kws': list(_kws)})

@app.put('kws')
def update_handler(kw):
    pass

@app.delete('/kws/<id>')
def delete_handler(kw):
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
