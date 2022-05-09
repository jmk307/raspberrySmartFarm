import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
servoPWM = GPIO.PWM(22, 50)
servoPWM.start(0)
def motoron():
  print("motoron!")
  servoPWM.ChangeDutyCycle(7)
  time.sleep(1)
  servoPWM.ChangeDutyCycle(10)
  time.sleep(1)
motoron()
GPIO.cleanup()



