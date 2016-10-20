# temperature-project-host
This is an Arduino temperature logger and display project. I have the Arduino log temperature to a MongoDB and from there I have a Python Flask app that is connected to that MongoDB which sends it to the front end to display that data as a graph with PlotlyJS.

Currently I have implemented the following 
- Use a Python script to read serial data from arduino and log that data to a MongoDB. Will add the Arduino and Python script to this project, currently I am using a DS18B20 temperature sensor, the setup process with that is pretty straight forward. I would like to hook up the sensor directly to a Raspberry Pi, but that will take some modification, and have never programmed that type of thing on RPi.

- Temperature API data (http://example.com/temperatures/10) 10 can be any number, and that is the amount of hours of data it will return. Currently I have the temperature loggins every 30 seconds, I will set it to 2 - 5 minutes in the future, there is not enough temperature fluctations in a 30 second time period, but works good for development.

- Display temperature data on a graph (http://example.com/tempdisplay/) 



I want to implement the folowing:
- currently the graph on the tempdisplay page is a set amount of time my plan is to use the form on that page to set the amount of hours to display. I plan to continue to use AJAX to do this, but my knowledge of AJAX is limited.

- Eventually I would like to turn this into an Angular 2 Front End, currently my knowledge of Angular 2 is limited.

- Make an actual interactive webpage, and make setting up additional sensors a breeze.

- Modify this to work with temperature sensors, humidity sensors, and various other sensors. 

- Implement error handling

- User logins once I work on the ability to add your own sensors

- eventually will have to add a more robust way of connecting to arduino serial(listing serial ports on webpage and then using a form to connect to Arduino) and submitting the arduino data from flask to the MongoDB, similar to how I do it now but all in one package.

- That should keep me busy for a while.
