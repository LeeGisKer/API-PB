import requests
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_params():
    code = request.args.get('code', default = 1, type = str)
    state = request.args.get('state', default=1, type=str)
    info = json.dumps({'code': code, 'state': state})
    code_txt(info)
    return jsonify({'code': code, 'state': state})


def code_txt(info):
    fo = open('code.txt', 'w')
    fo.write(info)
    fo.close
    return

if __name__ == '__main__':
    app.run()
