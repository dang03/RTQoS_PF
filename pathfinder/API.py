#!/usr/bin/env python
# encoding: utf-8

__author__ = 'Dani'

import os
import sys
# Using Flask micro-framework, since Python doesn't have built-in session management
# This REST API is a proof of concept and restful capabilites test for Pathfinder
from flask import Flask, jsonify, make_response
import flask_restful
# Our target library
import json
import datetime
from pathfinder.Pathfinder import pathfinder_algorithm

app = Flask(__name__)
api = flask_restful.Api(app)


# Generate a secret random key for the session
app.secret_key = os.urandom(24)


mime_types = {'json_renderer': ('application/json',),
              'xml_renderer': ('application/xml', 'text/xml',
                                'application/x-xml',)}          # xml could be an alternative data format


class APIEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%m/%d/%Y')

        """
        elif isinstance(obj, requestId):
            return str(obj)
        """
        return json.JSONEncoder.default(self, obj)

def json_renderer(**data):
    return json.dumps(data, ensure_ascii=False, cls=APIEncoder, indent=4, encoding='utf8')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



"""
#############
REST service
#############
HTTP Method     URI                     Action
------------    --------------------    -------
index           /pathfinder/
GET             /pathfinder/get_path    Retrieve latest found QoS path
GET             /pathfinder/get_qos_log Retrieve stored QoS paths
POST            /pathfinder/run_app     Trigger pathfinder to return a QoS path
POST            /pathfinder/...         ...
...


"""

# REQUESTS dispatching
# Query last Pathfinder result: returns last QoS path returned


@app.route('/pathfinder/get_path', methods=['GET'])
def get_path():
    #url = ''
    # example to actually run
    #url = 'https://api.github.com/users/runnable'

    # this issues a GET to the url. replace "get" with "post", "head",
    # "put", "patch"... to make a request using a different method
    #r = requests.get(url)
    #r = {}
    if os.path.exists('./path.json'):
        with open('./path.json', 'r') as path:
            # r = pathRes.readlines()
            res = json.load(path, encoding='utf8')
            path.close()

            res = jsonify(PATH=res)
            return res
    else:
        flask_restful.abort(404)


# Query qosDb log
@app.route('/pathfinder/get_qos_log', methods=['GET'])
def get_qos_log():
    res = []
    #res = {}
    if os.path.exists('./qosDb.json'):
        qosDb = open('./qosDb.json', 'r')
        for line in qosDb:
            res.append(json.loads(line))

        #res = qosDb.readlines()
        #[{'c': True, 'd': False}, None]

        qosDb.close()

        return jsonify(LOG=res)
        #return json.dumps(json.JSONDecoder().decode(r))


    else:
        flask_restful.abort(404)



"""
if os.path.exists('./path.json'):
        with open('./path.json', 'r') as path:
            # r = pathRes.readlines()
            res = json.load(path, encoding='utf8')
            path.close()

            res = json_renderer(data=res)
            return res
"""

@app.route('/pathfinder/run_app', methods=['POST'])
def run_app():
    """
    url = ''
    # example to actually run
    # url = 'http://httpbin.org/post'

    data = {'a': 10, 'b': [{'c': True, 'd': False}, None]}
    # example of JSON data
    #data = {'a': 10, 'b': [{'c': True, 'd': False}, None]}
    headers = {'Content-Type': 'application/json'}

    r = requests.post(url, data=json.dumps(data), headers=headers)

    return json.dumps(r.json(), indent=4)
    """

    result = pathfinder_algorithm_from_file()

    #result = os.popen(queueString).read()

    return json.dumps(result, indent=4)

@app.route('/pathfinder/run_app2', methods=['POST'])
def run_app2():

    if not request.json:
	flask_restful.abort(400)
    
    pfInput = json.load(request.json)
    try:
        result = pathfinder_algorithm(pfInput)
    except:
        return make_response(jsonify({'error': sys.exec_info()[0]}), 500)

    return json.dumps(result, indent=4), 200

# Define a route for the webserver
@app.route('/pathfinder/')
def index():
    #return render_template('index.html')

    json_index = {'Pathfinder REST API Index':{'Methods':[{'get_path': "Query last QoS path returned", 'get_qos_log': "Query QoS log returned", 'example': "More to be implemented"}]}}

    return jsonify(json_index)




if __name__ == '__main__':
    app.run(
        # host="0.0.0.0",
        #port=int("80")
        debug=True
    )

"""
# testing REST requests
r = requests.get("http://weather.yahooapis.com/forecastrss", params = {"w":"753692", "u":"c"})
if r.status_code == 200:
    print r.text
"""