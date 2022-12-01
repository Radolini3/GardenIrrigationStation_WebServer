from curses import raw
from datetime import datetime
from socket import timeout
import serial
import json
import glob
import sys


# Zapisz historię pomiarów do pliku csv
def save_to_csv(tab):
    file = open("dataCapture/pomiary.csv", 'a') #otwórz plik pomiary.csv
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    file.write(dt_string)
    file.write(',')
    for i in range (0, len(tab)):  #for tyle razy ile jak duża jest tablica wejściowa

        file.write(str(tab[i])) #zapisz do pliku wartość daną na csv
        if i == len(tab)-1:
            pass
        else:
            file.write(',')
    file.write(',\n')
    file.close()
#===================================================================================================================================
#Zapisz do JSONa  - wartości z ostatniego pobrania wartości z czujników 

def JSONconfig(config):
    config = {
    "Threshold": config[1],
    "Mode": config[2],
    "IrrigTime": config[3]
    }
    config = json.dumps(config, indent = 1)
    with open("dataCapture/config.json", "w") as outfile_2:
        outfile_2.write(config)

def JSONsensors(arr):
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

#===================================================================================================================================
#Sprawdź platformę na której skrypt działa, potem sprawdź dostępne porty i zwróć użytkownikowi
def serial_ports():
    print("Checking for avaiable serial ports on your computer")

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')        # this excludes your current terminal "/dev/tty"

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []

    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result        

def detectPort():
    #Wczytaj dostępne porty szeregowy
    serialPortList = serial_ports()
    print("Avaiable ports: ")
#===================================================================================================================================
    if not serialPortList:
        print("No ports detected! Make sure you connected MCU to system / No other monitoring serial port process is running ")
        sys.exit()
    #Ponumerowana lista portów
    for i in range (0, len(serialPortList)):
        print(str(i+1) + ". " + str(serialPortList[i]))
    print("Detected port: " + serialPortList[0])
    return serialPortList[0]

print("Detected OS: " + sys.platform)
port = detectPort()
serialPort = serial.Serial(port,baudrate=38400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=None) #timeout=None każe czekać nonstop na przychodzące dane, jeśli damy jakąś stałą, to po nie otrzymaniu danych w zadanym czasie zwróci błąd potem.
print("Running - Do not close this terminal in order to mantain capturing data")
#Nieskończona pętla monitorująca port szeregowy w poszukiwaniu przychodzących danych
while True:
        while serialPort.in_waiting:
            strUART = serialPort.readline()
            rawData = strUART.decode('utf8')
            rawData = rawData.strip('\n')
            if rawData.startswith("C"):
                config = rawData.split("/")
                print(config)
                JSONconfig(config)
                continue
            sensors = rawData.split("/")
            sensors.pop(0)
            print(sensors)
            JSONsensors(sensors)
            save_to_csv(sensors)



#===================================================================================================================================
    # listSize = len(serialPortList)
    # print("Select port which is connected to microcontroller by entering number: ")
    # #Kontrola poprawności wyboru portu
    # while 1:
    #     try:
    #         answer = int(input())
    #         if answer - 1 < listSize and answer > 0:
    #             break
    #     except ValueError:
    #         print("Enter only digit / Value entered is out of range")
    #         continue
#===================================================================================================================================