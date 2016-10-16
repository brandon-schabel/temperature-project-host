from flask import Response, Flask, jsonify, make_response, url_for
from bson import json_util
from time import sleep, time
from pymongo import MongoClient
import serial
from datetime import datetime, timedelta
import re
import json
from json import dumps


app = Flask(__name__)
'''
mongo_server = "mongo_api"
mongo_port = "27017"
mongo_user = "admin"
mongo_passwd = ":mysecretpassword@"
connect_string = "mongodb://"+ mongo_user
                             + mongo_passwd
                             + mongo_server
                             + ":"
                             + mongo_port
'''

# def json_serial(obj)

client = MongoClient('ds059316.mlab.com', 59316)
#client = MongoClient('localhost', 27017)
#mongodb://beans:beans@ds059316.mlab.com:59316/temp-database
db = client['temp-database']
db.authenticate('beans', 'beans')

temperatures = db.temperatures


def temps_by_hour(howManyHours):
    # current time
    currentDateTime = datetime.now()
    lastHour = datetime.today() - timedelta(hours=howManyHours)

    return [doc['temperature'] for doc in db.temperatures.find({'date': {'$lt': currentDateTime, '$gte': lastHour}})]

print(temps_by_hour(1))

# this returns datetime as a string for us in json data


def all_temp_data_hour_serial(howManyHours):
    currentDateTime = datetime.now()
    lastHour = datetime.today() - timedelta(hours=howManyHours)

    # return [doc['temperature'] for doc in db.temperatures.find({'date':
    # {'$lt': currentDateTime, '$gte': lastHour}})]
    cursor = temperatures.find(
        {'date': {'$lt': currentDateTime, '$gte': lastHour}})

    documents = []

    for document in cursor:
        jsonObject = {'temperature': document['temperature'],
                      'date': dumps(document['date'], default=json_serial)}

        documents.append(jsonObject)

    return documents


def all_temp_data_hour(howManyHours):
    currentDateTime = datetime.now()
    lastHour = datetime.today() - timedelta(hours=howManyHours)

    # return [doc['temperature'] for doc in db.temperatures.find({'date':
    # {'$lt': currentDateTime, '$gte': lastHour}})]
    cursor = temperatures.find(
        {'date': {'$lt': currentDateTime, '$gte': lastHour}})

    documents = []

    for document in cursor:
        documents.append(document)

    return documents

# print(all_temp_data_by_hour(1))


# for x in range(0, len(documents)):
#    print(jsonify(x))

# print(jsonify(all_temp_data_by_hour(1)))

'''
@app.route('/temperatures/<int:numHours>')
def temperatures_by_hour_page(numHours):
	documents = all_temp_data_by_hour(numHours)
	jsonifiedDocs = []

	for document in documents:
		jsonified = {'temperature': document['temperature'], 'date': document['date']}
		jsonifiedDocs.append(jsonified)

	return Response(json.dumps(jsonifiedDocs), mimetype='application/json') 
'''

@app.route('/temperatures/<int:numHours>')
def temperatures_by_hour_api(numHours):
	allTemps = all_temp_data_hour_serial(numHours)

	#return Response(jsonify(allTemps))
	return jsonify(allTemps)


@app.route('/')
def index():
    # return jsonify({'temperature': documents[0]['temperature'], 'date':
    # documents[0]['date']})
    return "Hello World"


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")

#documents = all_temp_data_by_hour(1)
#print(dumps(documents[0]['date'], default = json_serial))


if __name__ == '__main__':
    #app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
