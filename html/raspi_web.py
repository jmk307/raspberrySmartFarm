from flask import Flask, request, render_template, make_response, redirect, url_for, Response
import time
from weatherCrawling import seoul
from nongsaroCrawling import plant, selectPlant, search
from celcius import humidity, temperature
from camera import *

app = Flask(__name__)
plant = selectPlant()

@app.route('/', methods = ['POST', 'GET'])
def get_camera():
    get_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    currentTemp = seoul[1]
    currentHum = seoul[2]
    currentTemp2 = temperature
    currentHum2 = humidity 
    temp = 0
    hum = 0
    plantName = '선택'
    if request.method == 'POST':
        plantName = request.form.get('plantId')
        print(plantName)               
        temp = (search(plantName))[0][0]
        hum = (search(plantName))[1][0]
        f = open("/var/www/html/temp.txt", 'w')
        f2 = open("/var/www/html/hum.txt", 'w')
        f.write(str(temp))        
        f2.write(str(hum))
        f.close()
        f2.close()        
    return render_template("index.html", cur_time = get_time, currentTemp = currentTemp, currentHum = currentHum, currentTemp2 = currentTemp2, currentHum2 = currentHum2, plant = plant, plantName = plantName, temp = temp, hum = hum)

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    port = 5000
    debug = True

    
