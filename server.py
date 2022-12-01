from datetime import datetime
from curses.ascii import SO
import sys

from operator import methodcaller
from urllib import request
from flask import Flask, render_template, json, url_for, jsonify
import csv 

app = Flask(__name__)

#Dodanie ścieżki do skryptów pythona 
sys.path.insert(0, '/dataCapture')

@app.route("/") 
def home():
    #Otwórz plik sensors.json 
    with open('./dataCapture/sensors.json', 'r') as myfile:
        data = json.load(myfile)
        #Pobranie odczytów z JSON'a 
        sensors = [
          data['Temperature'],
          data['AirHumidity']]
        SoilSensors = [
         int(data['SoilSensor1']),
         int(data['SoilSensor2']),
         int(data['SoilSensor3']), 
         int(data['SoilSensor4']),
         int(data['SoilSensor5']),
         int(data['SoilSensor6'])]
        average = int(sum(SoilSensors)/len(SoilSensors)) # Średnia z ponmiarów czujników wilgotności

    with open('./dataCapture/config.json', 'r') as myfile2:
        data = json.load(myfile2)
        config = [
         data['Threshold'], 
         data['Mode'],
         data['IrrigTime']]

        if config[1] == '1':
            Mode = "Automatyczny"
        else:
            Mode = "Manualny"

    return render_template(
        "home.html",
        mode = Mode,            # tryb podlewania z mikrokontrolera
        Threshold = config[0],  # próg podlewania przy trybie automatycznym 
        irrigtime = config[2],
        avg = average,          # Srednia wilgotności gleby 
        airTemp = sensors[0],   # temperatura powietrza
        airH = sensors[1],      # Wilgotność powietrza 
        SoilH1 = SoilSensors[0],
        SoilH2 = SoilSensors[1],
        SoilH3 = SoilSensors[2],
        SoilH4 = SoilSensors[3],
        SoilH5 = SoilSensors[4],
        SoilH6 = SoilSensors[5])

@app.route("/charts")	# Wykres średniej pomiarów od czasu (dzisiejsze pomiary tylko atm)
def charts():
    # with open('./dataCapture/pomiary.csv', 'r') as csvfile:
    #     data = list(csv.reader(csvfile, delimiter=','))
    #     now = datetime.now()
    #     dt_string = now.strftime("%d/%m/%Y")
    #     for dt_string in data:
    #         todayData = data
    #     print(todayData)


    rows = []
    with open("./dataCapture/pomiary.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            rows.append(row)


    dateTime = [row[0] for row in rows]
    AirT = [row[1] for row in rows]
    AirH = [row[2] for row in rows]
    Soil1 = [row[3] for row in rows]
    Soil2 = [row[4] for row in rows]
    Soil3 = [row[5] for row in rows]
    Soil4 = [row[6] for row in rows]
    Soil5 = [row[7] for row in rows]
    Soil6 = [row[8] for row in rows]
    SoilAvg = [row[9] for row in rows]

    return render_template(
        "charts.html",
        dateTime = dateTime, 
        AirT = AirT,
        AirH = AirH,
        Soil1 = Soil1, #Kolejne odczyty z czujników
        Soil2 = Soil2,
        Soil3 = Soil3,
        Soil4 = Soil4,
        Soil5 = Soil5,
        Soil6 = Soil6,
        SoilAvg = SoilAvg) #Średnia
    
@app.route("/about")	# kilka słów o projekcie 
def about():
    return render_template("about.html")

@app.route("/settings")	    # Ustawienia (narazie do usunięcia )
def settings():
    return render_template("settings.html")

# @app.route('/dataCapture')
# def runDataCapture():
#     if sys.platform.startswith('win'):
#         os.system("start cmd /k python dataCapture/serialMonitor.py")
#     if sys.platform.startswith('linux'):
#         os.system("lxterminal -e 'python dataCapture/serialMonitor.py")
#     return render_template("dataCapture.html")

# @app.route("/waterGarden")	
# def waterGarden():
#     sendSignal()
#     return jsonify(message='success')

if __name__ == "__main__":
    app.run(debug=True)


# Ustaw serwer lokalny widzialny w zakresie sieci WiFi
# if __name__ == '__main__':
#     app.run(host='0.0.0.0')
