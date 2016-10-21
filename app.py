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
#I was getting some weird cross origin errors when I would try to connect to the API so I had to add this CORS(app)
CORS(app)
#need to figure ouot how to hide this, also so a user can connect to their own database
client = MongoClient('ds059316.mlab.com', 59316)

#connecting to our mlab database
db = client['temp-database']
db.authenticate('beans', 'beans')

#connect to a db named temperatures
temperatures = db.temperatures

#this function returns objects straight from the Mongo database
def temps_by_hour(howManyHours):
    #gets current time, all times are in UTC.
    currentDateTime = datetime.utcnow()
    lastHour = datetime.utcnow() - timedelta(hours=howManyHours)

    return [doc['temperature'] for doc in db.temperatures.find({'date': {'$lt': currentDateTime, '$gte': lastHour}})]

print(temps_by_hour(1))

# this returns datetime as a string for us in json data
def all_temp_data_hour_serial(howManyHours):
    currentDateTime = datetime.utcnow()
    lastHour = datetime.utcnow() - timedelta(hours=howManyHours)
    
    cursor = temperatures.find(
        #this queries our mongoDB and gets a time between the set amount of hours and the current time
        #$lt stands for less than and $gte stands for greater than
        {'date': {'$lt': currentDateTime, '$gte': lastHour}})
    
    #this initializes our temperatures dictionary which will be the JSON data we will send
    temperaturesDict = {'temperatures': []}
    
    #this for loop goes through our query parameters, gets the sensor data that we want and adds it to our variable jsonObject
    #jsonObject is then appended to our temperaturesDict under the 'temperatures' key. do it would look something like {"temperatures":[{
         #                                                                                                           "temperature": '78.5},
         #                                                                                                           "date": 20161203T033027}]}
    for document in cursor:
        jsonObject = {'temperature': document['temperature'],
                      'date': dumps(document['date'], default=json_serial)}

        temperaturesDict['temperatures'].append(jsonObject)
         
    print(temperaturesDict)
    
    return temperaturesDict


def all_temp_data_hour(howManyHours):
    #same as above but not yet serialized so I can use with python
    currentDateTime = datetime.utcnow()
    lastHour = datetime.utcnow() - timedelta(hours=howManyHours)

    cursor = temperatures.find(
        {'date': {'$lt': currentDateTime, '$gte': lastHour}})

    documents = []

    for document in cursor:
        documents.append(document)

    return documents

#<int:numHours> is the variable we will use to determine the number of hours the user wants
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

    return "Welcome to Temp Display"


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")

if __name__ == '__main__':
    #app.run(debug=True)
    #get port assigned by OS else set it to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
