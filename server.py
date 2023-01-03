from curses.ascii import SO
import sys
from flask import Flask, render_template, json, url_for, jsonify
import csv 

app = Flask(__name__)

#Dodanie ścieżki do skryptów pythona 
sys.path.insert(0, '/dataCapture')

@app.route("/") # Endpoint strony głównej - ładowanie JSONów 
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

    with open('./dataCapture/config.json', 'r') as myfile2: # Odczytanie ustawień nawadniania
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

@app.route("/charts")	# Endpoint wykresów0 pomiarów od czasu - ładowanie z pliku csv do aplikacji 
def charts():
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

@app.route("/removehistory") # Endpoint czyszczący plik pomiary.csv 	   
def removehistory():
    f = open("dataCapture/pomiary.csv", "w")
    f.truncate()
    f.close()
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)

# Ustaw serwer lokalny widzialny w zakresie sieci WiFi
# if __name__ == '__main__':
#     app.run(host='0.0.0.0')
