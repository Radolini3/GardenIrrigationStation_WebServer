from socket import timeout
from time import sleep
import serial
import csv
import _thread
from datetime import datetime
import re 
import json

def save_to_csv(tab):
    file = open("pomiary.csv", 'a') #otwórz plik pomiary.csv

    for i in range (0, len(tab)):  #for tyle razy ile jak duża jest tablica wejściowa
        file.write(str(tab[i])) #zapisz do pliku wartość daną na csv
        if i == len(tab)-1:
            pass
        else:
            file.write(',')

    file.write('\n')
    file.close()

def JSONdumpster(arr):
    arr = {
    "Temperature": arr[0],
    "AirHumidity": arr[1],
    "SoilSensor1": arr[2],
    "SoilSensor2": arr[3],
    "SoilSensor3": arr[4],
    "SoilSensor4": arr[5],
    "SoilSensor5": arr[6],
    "SoilSensor6": arr[7]
    }
    json_obj = json.dumps(arr, indent = 1)
    with open("dataCapture/sensors.json", "w") as outfile:
        outfile.write(json_obj)

port = "COM3"
serialPort = serial.Serial(port="COM3",baudrate=38400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=10)
while True:
    strUART = serialPort.readline()
    rawSensorData = strUART.decode('utf8')
    rawSensorData = rawSensorData.strip('\n')
    sensors = rawSensorData.split("S")
    sensors.pop(0)
    print(sensors)
    JSONdumpster(sensors)