from flask import Flask, request, render_template, make_response, redirect, url_for, Response
import time
from weatherCrawling import seoul
from nongsaroCrawling import plant, selectPlant, search
from celcius import humidity, temperature
from camera import *

app = Flask(__name__)
plant = selectPlant()

# 메인 화면


@app.route('/', methods=['POST', 'GET'])
def get_camera():
    get_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 현재 시각
    currentTemp = seoul[1]  # 기상청 기준 서울 현재 온도
    currentHum = seoul[2]  # 기상청 기준 서울 현재 습도
    currentTemp2 = temperature  # 스마트팜 속 현재 온도
    currentHum2 = humidity  # 스마트팜 속 현재 습도
    temp = 0  # 웹 구동했을 때 디폴트 온도
    hum = 0  # 웹 구동했을 때 디폴트 온도
    plantName = '선택'  # 웹 구동했을 때 디폴트 농작물
    if request.method == 'POST':  # 원하는 농작물 온습도를 'POST' 방식으로 전송한다면
        plantName = request.form.get('plantId')
        print(plantName)
        temp = (search(plantName))[0][0]  # 라즈베리파이 속 DB 내에 있는 작물의 적정 온도 선택
        hum = (search(plantName))[1][0]  # 라즈베리파이 속 DB 내에 있는 작물의 적정 습도 선택
        f = open("/var/www/html/temp.txt", 'w')
        f2 = open("/var/www/html/hum.txt", 'w')
        f.write(str(temp))  # 스마트팜 속 현재 온도 txt로 작성
        f2.write(str(hum))  # 스마트팜 속 현재 습도 txt로 작성
        f.close()
        f2.close()
    return render_template("index.html", cur_time=get_time, currentTemp=currentTemp, currentHum=currentHum, currentTemp2=currentTemp2, currentHum2=currentHum2, plant=plant, plantName=plantName, temp=temp, hum=hum)

# 파이캠


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


# 로컬에서 구동
if __name__ == '__main__':
    app.run(host='0.0.0.0')
    port = 5000
    debug = True
