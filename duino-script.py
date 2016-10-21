#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep, time
import pymongo
from pymongo import MongoClient
import serial
from datetime import datetime
import re

client = MongoClient('ds059316.mlab.com', 59316)
#client = MongoClient('localhost', 27017)
#mongodb://beans:beans@ds059316.mlab.com:59316/temp-database
db = client['temp-database']
db.authenticate('beans', 'beans')

temperatures = db.temperatures

ser = serial.Serial('COM6')
print(ser.name)
ser.write(b'hello')

counter = 32

while True:
    print('while loop')
    counter += 1
    
    #get temperatures from the arduino serial
    temp = str(ser.readline())
    temp = re.findall(r"[-+]?\d*\.\d+|\d+", temp)
    temp = temp[0]
    print(temp)
    print(float(temp))

    currentDateTime = datetime.utcnow()
    print(currentDateTime)

    if(float(temp) > 60 and float(temp) < 100):
        tempLog = {'temperature':temp,
                'date': currentDateTime,
                #'year': datetime.datetime.year(),
                #'month': datetime.datetime.month(),
                #'day': datetime.datetime.day(),
                #'hour': datetime.datetime.hour(),
                #'seconds' time.time.seconds(),
                #'time': datetime.datetime.time(),
            }
        temperatures.insert(tempLog)
    
    temperatures = db.temperatures

    

    print('logged ' + str(temperatures.find_one({'date':currentDateTime})))
    sleep(30)
    '''if counter ==255:
          ser.close()
          print(str(counter))
    '''
          
