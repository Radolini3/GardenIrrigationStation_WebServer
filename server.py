from operator import methodcaller
from urllib import request
from flask import Flask, render_template, json, url_for

app = Flask(__name__)




@app.route("/") 
def home():
    with open('./dataCapture/sensors.json', 'r') as myfile:
        data = json.load(myfile)
        print(data)
        sensors = [data['Temperature'], data['AirHumidity'], data['SoilSensor1'], data['SoilSensor2'], data['SoilSensor3'], data['SoilSensor4'], data['SoilSensor5'], data['SoilSensor6']] 
        print(sensors)
    return render_template("home.html", airTemp = sensors[0], airH = sensors[1], SoilH1 = sensors[2], SoilH2 = sensors[3], SoilH3 = sensors[4], SoilH4 = sensors[5], SoilH5 = sensors[6], SoilH6 = sensors[7] )

@app.route("/charts")	
def charts():
    return render_template("charts.html")
    
@app.route("/about")	
def about():
    return render_template("about.html")

# @app.route("/sensorJSON")
# def open_JSON():
#     with open('./dataCapture/sensors.json', 'r') as myfile:
#         data = myfile.read()
#         print(data)
#         return render_template("sensors.json")


# @app.route('/dataCapture', methods = ['POST'])
# def getSensorData():
#     if request.is_json:
#         req = request.get_json()
#         re

#     # json_data = open(url_for('dataCapture', filename="sensors.json"))
#     # data = json.load(json_data)
#     # return render_template('sensors.json', data=data)

# @app.route('/')
# def runDataCapture():
#     file = open(r'./dataCapture/serialMonitor.py', 'r').read()
#     return exec(file)

if __name__ == "__main__":
    app.run(debug=True)