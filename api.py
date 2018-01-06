import json

def response (data, code = 200, headers = {'Content-Type':'application/json','Access-Control-Allow-Origin':'*'}):
    return json.dumps(data), code, headers

def ERROR (err_type, code = 400):
    return response({
        'info' : err_type
    }, code)
