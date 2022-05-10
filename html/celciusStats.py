import Adafruit_DHT
import time
import pymysql
from datetime import datetime

sensor = Adafruit_DHT.DHT11
pin = 27

def cel():    

    humidity, temperature = Adafruit_DHT.read_retry(sensor, 27)

    print("temperature: " + str(temperature))
    print("humidity: " + str(humidity))    

    conn = pymysql.connect(host = '192.168.200.107', user='root', password='raspberry', db='TEMPERATURE', charset='utf8')

    cursor = conn.cursor()

    sql = "INSERT INTO server_room (date, time, temperature, humidity) VALUES (%s, %s, %s, %s)"

    cursor.execute(sql, (datetime.today().strftime("%Y/%m/%d"), datetime.today().strftime("%H:%M:%S"), temperature, humidity))
    conn.commit()
    conn.close()   

    return humidity, temperature
        
try:
    while True:
        cel()
        time.sleep(5)
except KeyboardInterrupt:
    pass

