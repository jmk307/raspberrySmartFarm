import Adafruit_DHT
import time
import pymysql
from datetime import datetime

sensor = Adafruit_DHT.DHT11
pin = 27

# def cel():    

#     humidity, temperature = Adafruit_DHT.read_retry(sensor, 27)

#     # print("temperature: " + str(temperature))
#     # print("humidity: " + str(humidity))    
   
#     return humidity, temperature
humidity, temperature = Adafruit_DHT.read_retry(sensor, 27)       

# print(humidity)