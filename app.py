from flask import Response, Flask, jsonify, make_response, url_for, render_template, \
         send_from_directory
from flask_cors import CORS, cross_origin
from bson import json_util
from time import sleep, time
from pymongo import MongoClient
import serial
from datetime import datetime, timedelta
import json
from json import dumps
import sys
import os
import pytz

app = Flask(__name__)
CORS(app)
client = MongoClient('ds059316.mlab.com', 59316)
db = client['temp-database']
db.authenticate('beans', 'beans')

temperatures = db.temperatures

def temps_by_hour(howManyHours):
    # current time
    currentDateTime = datetime.utcnow()
    lastHour = datetime.utcnow() - timedelta(hours=howManyHours)

    return [doc['temperature'] for doc in db.temperatures.find({'date': {'$lt': currentDateTime, '$gte': lastHour}})]

print(temps_by_hour(1))

# this returns datetime as a string for us in json data
def all_temp_data_hour_serial(howManyHours):
    currentDateTime = datetime.utcnow()
    lastHour = datetime.utcnow() - timedelta(hours=howManyHours)
    
    cursor = temperatures.find(
        {'date': {'$lt': currentDateTime, '$gte': lastHour}})

    temperaturesDict = {'temperatures': []}
    
    for document in cursor:
        jsonObject = {'temperature': document['temperature'],
                      'date': dumps(document['date'], default=json_serial)}

        temperaturesDict['temperatures'].append(jsonObject)

    #temperaturesDict['temperatures'].append(documents)
    print(temperaturesDict)
    
    return temperaturesDict


def all_temp_data_hour(howManyHours):
    currentDateTime = datetime.utcnow()
    lastHour = datetime.utcnow() - timedelta(hours=howManyHours)

    cursor = temperatures.find(
        {'date': {'$lt': currentDateTime, '$gte': lastHour}})

    documents = []

    for document in cursor:
        documents.append(document)

    return documents

@app.route('/temperatures/<int:numHours>')
def temperatures_by_hour_api(numHours):
    allTemps = all_temp_data_hour_serial(numHours)

    #return Response(jsonify(allTemps))
    return jsonify(allTemps)

@app.route('/tempdisplay')
def temp_display():
    return render_template("tempdisplay.html")


@app.route('/')
def index():

    return jsonify(all_temp_data_hour_serial(6))


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")

if __name__ == '__main__':
    #app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
