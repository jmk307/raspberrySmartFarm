import picamera as pic
import time
from tkinter import *
import multiprocessing as mp
cam = pic.PiCamera()
cam.resolution = (1920, 1080)
cam.framerate = 30

tk=Tk()
def capevent():
  cam.capture('capture.jpg')
  time.sleep(1)
def recevent():
  cam.start_recording('video.h264')
  time.sleep(10)
  cam.stop_recording()
  

button =Button(tk,text="photo",command=capevent)
button2=Button(tk,text="movie",command=recevent)
button.pack(side=LEFT,padx=10,pady=10)
button2.pack(side=LEFT,padx=10,pady=10)
tk.mainloop()



