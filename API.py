#!/usr/bin/env python
# encoding: utf-8

__author__ = 'Dani'

import os
# Using Flask micro-framework, since Python doesn't have built-in session management
# This REST API is a proof of concept and restful capabilites test for Pathfinder
from flask import Flask, session, render_template, jsonify
import flask_restful
# Our target library
import requests
import json
import datetime
from Pathfinder import pathfinder_algorithm

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
    return json.dumps(data, cls=APIEncoder)



"""
#############
REST service
#############
HTTP Method     URI                     Action
------------    --------------------    -------
index           /pathfinder/
GET             /pathfinder/get_path    Retrieve latest found QoS path
GET             /pathfinder/get_qosDb   Retrieve stored QoS paths
POST            /pathfinder/...         ...
...


"""

# REQUESTS dispatching
# Query last Pathfinder result: returns last QoS path returned
@app.route('/pathfinder/get_path')
def get_path():
    #url = ''
    # example to actually run
    #url = 'https://api.github.com/users/runnable'

    # this issues a GET to the url. replace "get" with "post", "head",
    # "put", "patch"... to make a request using a different method
    #r = requests.get(url)
    #r = {}
    if os.path.exists('./path.json'):
        pathRes = open('./path.json', 'r')
        r = pathRes.readlines()
        pathRes.close()
    else:
        flask_restful.abort(404)

    #return json.dumps(r, indent=4)
    return r


# Query qosDb log
@app.route('/pathfinder/get_qos_log')
def get_qos_log():
    r = {}
    if os.path.exists('./qosDb.json'):
        qosDb = open('./qosDb.json', 'r')
        r = qosDb.readlines()
        qosDb.close()
    else:
        flask_restful.abort(404)

    return json.dumps(r, indent=4)






@app.route('/pathfinder/run_app')
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

    result = pathfinder_algorithm()

    #result = os.popen(queueString).read()

    return json.dumps(result, indent=4)




# Define a route for the webserver
@app.route('/pathfinder/')
def index():
    #return render_template('index.html')

    json_index = {'Pathfinder REST API Index':{'Methods':[{'get_path': "Query last QoS path returned"}, {'get_qos_log': "Query QoS log returned"}, {'example': "More to be implemented"}]}}

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
