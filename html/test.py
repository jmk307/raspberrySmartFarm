from flask import (
    Flask, request, render_template, make_response, redirect, url_for, Response
)
import cv2
app = Flask(__name__)
vc = cv2.VideoCapture(0)

def gen():
    while True:
        retVal, frame = vc.read()
        frame = cv2.resize(frame, (160, 120))
        retVal, frame = cv2.imencode(".jpg", frame)        
        yield(b'--frame\r\n'
            b'Content-Type:image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')

@app.route('/get_camera')
def get_camera():
    return render_template("get_cam.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/hello')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')