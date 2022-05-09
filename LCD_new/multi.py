import RPi.GPIO as GPIO
import os
import socket
import fcntl
import struct
import time
from time import gmtime, strftime
import Adafruit_DHT
import multiprocessing as mp
import picamera as pic
import time
from tkinter import *
cam = pic.PiCamera()
cam.resolution = (1920, 1080)
cam.framerate = 30
from motor import motoron

tk=Tk()
def capevent():
  print("capture success")
  cam.capture('capture.jpg')
  time.sleep(1)
def recevent():
  cam.start_recording('video.h264')
  time.sleep(10)
  cam.stop_recording()


motoron()  
button =Button(tk,text="photo",command=capevent)
button2=Button(tk,text="movie",command=recevent)
button.pack(side=LEFT,padx=10,pady=10)
button2.pack(side=LEFT,padx=10,pady=10)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# LCD
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
LCD_WIDTH = 16   
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 
LCD_LINE_2 = 0xC0 
E_PULSE = 0.0005
E_DELAY = 0.0005

# DHT11
sensor = Adafruit_DHT.DHT11
Celsius_pin = 27

# PAN
Transitor = 21
GPIO.setup(Transitor, GPIO.OUT)
GPIO.output(Transitor, GPIO.LOW)

# MOTOR
Survo_pin = 22
state = 0  # state == 1 -> ON, state == 0 -> OFF
'''
GPIO.setup(Survo_pin, GPIO.OUT)
servoPWM = GPIO.PWM(Survo_pin, 50)
servoPWM.start(0)
'''
# Data
Valid_temp = 10
Valid_humi = 80

def cel():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, Celsius_pin)
#         print("Temp : {0:0.1f} C Humidity : {1:0.1f} %".format(temperature, humidity))
    print("temperature:" + str(temperature))
    print("humidity: " + str(humidity))
#     time.sleep(500)
    return humidity, temperature

def lcdon():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7

  lcd_init()

def printDateTime():
  textDate = strftime("%d %A %Y", gmtime())
  textTime = strftime("%H:%M:%S", gmtime())
  lcd_string(textDate,LCD_LINE_1)
  lcd_string(textTime,LCD_LINE_2)
  return

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Cast to string
  message = str(message)
  # Send string to display
  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_on(hum, temp):
  try:
    main(hum,temp)
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()

def rp():
    while True:
        state=0
        lcdon()
        h, t = cel()
        # Display date and time
        index = 0
        while index < 5:
          printDateTime()
          time.sleep(1)
          index += 1
    #      Display text file
    #     file=open('Hello.txt','r')
    #     text=file.read()
        lcd_string("temperature:"+str(t),LCD_LINE_1)
        lcd_string("humidity:"+str(h),LCD_LINE_2)
    #     file.close()
        time.sleep(3)
        print("motor loading...")
        if state == 0 and h < Valid_humi:
          time.sleep(1)
          print("motor start")
          motoron()
          state = 1
        elif state == 1 and h >= Valid_humi:
          servoPWM.ChangeDutyCycle(3)
          time.sleep(1)
          servoPWM.ChangeDutyCycle(12)
          time.sleep(1)
          servoPWM.ChangeDutyCycle(3)
          time.sleep(1)
          servoPWM.ChangeDutyCycle(12)
          time.sleep(1)
          state = 0
        else:
          print("error")
        
        print("fan loading...")
        if t > Valid_temp:
            time.sleep(1)
            GPIO.output(Transitor, GPIO.HIGH)
            time.sleep(5)
        elif t <= Valid_temp:
            GPIO.output(Transitor, GPIO.LOW)
 
p=mp.Process(name="SubProcess",target=rp)
p.start()
tk.mainloop()
p.join()
GPIO.cleanup()
