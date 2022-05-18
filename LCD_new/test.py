# motor test

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
servoPWM = GPIO.PWM(22, 50)
servoPWM.start(0)
def motoron():
  servoPWM.ChangeDutyCycle(3)
  time.sleep(0.5)
  servoPWM.ChangeDutyCycle(9)
  time.sleep(0.5)


while True:
    motoron()