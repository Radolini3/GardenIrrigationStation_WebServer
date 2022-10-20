import sys
import os
from operator import methodcaller
from urllib import request
from flask import Flask, render_template, json, url_for
import subprocess
import dataCapture
app = Flask(__name__)

sys.path.insert(0, '/dataCapture')



@app.route("/") 
def home():
    with open('./dataCapture/sensors.json', 'r') as myfile:
        data = json.load(myfile)
        sensors = [data['Temperature'], data['AirHumidity'], data['SoilSensor1'], data['SoilSensor2'], data['SoilSensor3'], data['SoilSensor4'], data['SoilSensor5'], data['SoilSensor6']] 
    
    return render_template("home.html", airTemp = sensors[0], airH = sensors[1], SoilH1 = sensors[2], SoilH2 = sensors[3], SoilH3 = sensors[4], SoilH4 = sensors[5], SoilH5 = sensors[6], SoilH6 = sensors[7] )

@app.route("/charts")	
def charts():
    return render_template("charts.html")
    
@app.route("/about")	
def about():
    return render_template("about.html")

@app.route("/settings")	
def settings():
    return render_template("settings.html")

@app.route('/dataCapture')
def runDataCapture():
   # subprocess.call_in_new_window(['cmd' , 'python3 dataCapture\serialMonitor.py'], cwd=os.getcwd(), shell =True)
    if sys.platform.startswith('win'):
        os.system("start cmd /k python dataCapture/serialMonitor.py")
    if sys.platform.startswith('linux'):
        os.system("lxterminal -e 'python dataCapture/serialMonitor.py")
    return render_template("dataCapture.html")
    

if __name__ == "__main__":
    app.run(debug=True)


#Ustaw serwer lokalny widzialny w zakresie sieci WiFi
# if __name__ == '__main__':
#     app.run(host='0.0.0.0')
