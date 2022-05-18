import cv2

vc = cv2.VideoCapture(0)

def gen():
    while True:
        retVal, frame = vc.read()
        frame = cv2.flip(frame, 0)
        frame = cv2.resize(frame, (160, 120))     
        retVal, frame = cv2.imencode(".jpg", frame)        
        yield(b'--frame\r\n'
            b'Content-Type:image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')