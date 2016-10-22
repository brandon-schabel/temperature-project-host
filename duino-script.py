#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep, time
import pymongo
from pymongo import MongoClient
import serial
from datetime import datetime
import re
import sys
import glob

from connect_to_arduino import connect_to_arduino

client = MongoClient('ds059316.mlab.com', 59316)

db = client['temp-database']
db.authenticate('beans', 'beans')

temperatures = db.temperatures

arduinoPort = connect_to_arduino()
ser = serial.Serial(arduinoPort)

print(ser)

counter = 0

while True:
    print('while loop')
    print(str(ser.readline()))
    counter += 1
    print(str(counter) + " temps logged this session")
    
    #get temperatures from the arduino serial
    temp = str(ser.readline())
    temp = re.findall(r"[-+]?\d*\.\d+|\d+", temp)
    temp = temp[0]

    print(float(temp))

    currentDateTime = datetime.utcnow()
    print(currentDateTime)

    if(float(temp) > 60 and float(temp) < 100):
        tempLog = {'temperature':temp,
                'date': currentDateTime,
            }
        temperatures.insert(tempLog)
    else:
        print("No value recieved")
    temperatures = db.temperatures

    print('logged ' + str(temperatures.find_one({'date':currentDateTime})))

    sleep(120)
